package curriculum

import (
	"context"
	"errors"
	"fmt"
	"strings"
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"

	"sim-sekolah/internal/academic_year"
	"sim-sekolah/internal/system"
)

type CurriculumService interface {
	InitializeDocument(ctx context.Context, req InitializeCurriculumRequest) (*CurriculumDocument, error)
	GetDocuments(ctx context.Context) ([]CurriculumDocument, error)
	GetDocumentByID(ctx context.Context, docID uuid.UUID) (*CurriculumDocument, error)
	CheckReadiness(ctx context.Context, schoolID uuid.UUID) (*ReadinessResponse, error)
	TriggerChapterFormulation(ctx context.Context, userID uuid.UUID, req TriggerChapterRequest) (*TriggerChapterResponse, error)
	GetChapter(ctx context.Context, docID uuid.UUID, chapterNumber int) (*CurriculumChapter, error)
	UpdateChapterContent(ctx context.Context, chapterID uuid.UUID, req UpdateChapterRequest) error
	FinalizeDocument(ctx context.Context, docID uuid.UUID) error
	UpdateCurriculumType(ctx context.Context, docID uuid.UUID, req UpdateCurriculumTypeRequest) error

	// Co-curricular Activities
	GetAllKokurikulerActivities(ctx context.Context) ([]KokurikulerActivity, error)
	GetKokurikulerActivityByID(ctx context.Context, id string) (*KokurikulerActivity, error)
	CreateKokurikulerActivity(ctx context.Context, req CreateKokurikulerActivityRequest) (*KokurikulerActivity, error)
	UpdateKokurikulerActivity(ctx context.Context, id string, req UpdateKokurikulerActivityRequest) (*KokurikulerActivity, error)
	DeleteKokurikulerActivity(ctx context.Context, id string) error

	// Extra-curricular Activities
	GetAllEkstrakurikulerActivities(ctx context.Context) ([]EkstrakurikulerActivity, error)
	GetEkstrakurikulerActivityByID(ctx context.Context, id string) (*EkstrakurikulerActivity, error)
	CreateEkstrakurikulerActivity(ctx context.Context, req CreateEkstrakurikulerActivityRequest) (*EkstrakurikulerActivity, error)
	UpdateEkstrakurikulerActivity(ctx context.Context, id string, req UpdateEkstrakurikulerActivityRequest) (*EkstrakurikulerActivity, error)
	DeleteEkstrakurikulerActivity(ctx context.Context, id string) error

	// Analysis Data Integration (FR 4.2.1-4.2.5)
	IntegrateSWOTData(ctx context.Context, req AnalysisDataIntegrationRequest) (*AnalysisDataIntegrationResponse, error)
	IntegrateRootCauseData(ctx context.Context, req AnalysisDataIntegrationRequest) (*AnalysisDataIntegrationResponse, error)
	IntegrateFishboneData(ctx context.Context, req AnalysisDataIntegrationRequest) (*AnalysisDataIntegrationResponse, error)
	IntegrateStudentNeedsData(ctx context.Context, req AnalysisDataIntegrationRequest) (*AnalysisDataIntegrationResponse, error)
	GenerateKSPWithAnalysis(ctx context.Context, req KSPExportWithAnalysisRequest) (*KSPExportWithAnalysisResponse, error)
}

type curriculumService struct {
	repo     CurriculumRepository
	ayRepo   academic_year.AcademicYearRepository
	queueSvc *system.QueueService
}

func NewCurriculumService(repo CurriculumRepository, ayRepo academic_year.AcademicYearRepository, queueSvc *system.QueueService) CurriculumService {
	return &curriculumService{repo: repo, ayRepo: ayRepo, queueSvc: queueSvc}
}

func (s *curriculumService) InitializeDocument(ctx context.Context, req InitializeCurriculumRequest) (*CurriculumDocument, error) {
	// Check if academic year is active
	ay, err := s.ayRepo.GetByID(ctx, req.AcademicYearID.String())
	if err != nil {
		return nil, errors.New("academic year not found")
	}
	if !ay.IsActive {
		return nil, errors.New("academic year is not active")
	}

	// Check if already exists
	existing, err := s.repo.GetDocumentBySchoolAndYear(ctx, req.SchoolID, req.AcademicYearID)
	if err == nil && existing != nil {
		return nil, errors.New("curriculum document already exists for this academic year")
	} else if err != gorm.ErrRecordNotFound {
		return nil, err
	}

	doc := &CurriculumDocument{
		AcademicYearID:           req.AcademicYearID,
		SchoolID:                 req.SchoolID,
		Status:                   "DRAFT",
		CurriculumType:           req.CurriculumType,
		CurriculumClassification: req.CurriculumClassification,
	}

	// Validate curriculum type if provided
	if req.CurriculumType != "" && !IsValidCurriculumType(req.CurriculumType) {
		return nil, errors.New("tipe kurikulum tidak valid")
	}

	// Validate classification if provided
	if req.CurriculumClassification != "" && !IsValidCurriculumClassification(req.CurriculumClassification) {
		return nil, errors.New("klasifikasi kurikulum tidak valid")
	}

	if err := s.repo.CreateDocument(ctx, doc); err != nil {
		return nil, err
	}
	return doc, nil
}

func (s *curriculumService) GetDocuments(ctx context.Context) ([]CurriculumDocument, error) {
	return s.repo.GetDocuments(ctx)
}

func (s *curriculumService) GetDocumentByID(ctx context.Context, docID uuid.UUID) (*CurriculumDocument, error) {
	return s.repo.GetDocumentByID(ctx, docID)
}

func (s *curriculumService) CheckReadiness(ctx context.Context, schoolID uuid.UUID) (*ReadinessResponse, error) {
	data, err := s.repo.GetReadinessData(ctx, schoolID)
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, errors.New("school readiness data not found")
		}
		return nil, err
	}

	missing := []string{}
	if data.PersentaseProfilDasar < 90 {
		missing = append(missing, "Basic Profile Data")
	}
	if data.PersentaseDataGuru < 90 {
		missing = append(missing, "Teacher Data")
	}
	if data.PersentaseDataSiswa < 90 {
		missing = append(missing, "Student Data")
	}
	if data.PersentaseKarakteristikLokal < 90 {
		missing = append(missing, "Local Context Data")
	}

	score := (data.PersentaseProfilDasar + data.PersentaseDataGuru + data.PersentaseDataSiswa + data.PersentaseKarakteristikLokal) / 4.0

	return &ReadinessResponse{
		SchoolID:              schoolID,
		IsReadyToFormulate:    len(missing) == 0,
		ReadinessScorePercent: score,
		MissingParameters:     missing,
	}, nil
}

func (s *curriculumService) TriggerChapterFormulation(ctx context.Context, userID uuid.UUID, req TriggerChapterRequest) (*TriggerChapterResponse, error) {
	doc, err := s.repo.GetDocumentByID(ctx, req.CurriculumDocumentID)
	if err != nil {
		return nil, errors.New("curriculum document not found")
	}

	if doc.Status == "FINAL" {
		return nil, errors.New("cannot formulate chapters for a final document")
	}

	// For enqueueing, we use the CurriculumDocumentID.
	// The worker will parse the payload properly based on the ID.
	var queueID uuid.UUID
	if s.queueSvc != nil {
		queueID, err = s.queueSvc.Enqueue(ctx, "FORMULATE_CURRICULUM_CHAPTER", req.CurriculumDocumentID, userID)
		if err != nil {
			return nil, err
		}
	} else {
		return nil, errors.New("queue service is not initialized")
	}

	return &TriggerChapterResponse{
		Message: "Tugas perumusan berhasil dimasukkan ke antrean",
		QueueID: queueID,
		Status:  "QUEUED",
	}, nil
}

func (s *curriculumService) GetChapter(ctx context.Context, docID uuid.UUID, chapterNumber int) (*CurriculumChapter, error) {
	return s.repo.GetChapter(ctx, docID, chapterNumber)
}

func (s *curriculumService) UpdateChapterContent(ctx context.Context, chapterID uuid.UUID, req UpdateChapterRequest) error {
	return s.repo.UpdateChapterContent(ctx, chapterID, req.Content)
}

func (s *curriculumService) FinalizeDocument(ctx context.Context, docID uuid.UUID) error {
	count, err := s.repo.CountChapters(ctx, docID)
	if err != nil {
		return err
	}
	if count < 5 {
		return errors.New("all 5 chapters must be completed before finalizing")
	}

	return s.repo.UpdateDocumentStatus(ctx, docID, "FINAL")
}

func (s *curriculumService) UpdateCurriculumType(ctx context.Context, docID uuid.UUID, req UpdateCurriculumTypeRequest) error {
	// Validate curriculum type
	if !IsValidCurriculumType(req.CurriculumType) {
		return errors.New("tipe kurikulum tidak valid")
	}

	return s.repo.UpdateCurriculumType(ctx, docID, req.CurriculumType)
}

// Co-curricular Activities Methods
func (s *curriculumService) GetAllKokurikulerActivities(ctx context.Context) ([]KokurikulerActivity, error) {
	return s.repo.GetAllKokurikulerActivities(ctx)
}

func (s *curriculumService) GetKokurikulerActivityByID(ctx context.Context, id string) (*KokurikulerActivity, error) {
	return s.repo.GetKokurikulerActivityByID(ctx, id)
}

func (s *curriculumService) CreateKokurikulerActivity(ctx context.Context, req CreateKokurikulerActivityRequest) (*KokurikulerActivity, error) {
	isActive := true
	if req.IsActive != nil {
		isActive = *req.IsActive
	}

	activity := &KokurikulerActivity{
		ID:                   uuid.New(),
		CurriculumDocumentID: uuid.MustParse(req.CurriculumDocumentID),
		ActivityName:         req.ActivityName,
		Description:          req.Description,
		Schedule:             req.Schedule,
		IsActive:             isActive,
	}

	if req.LinkedSubjectID != "" {
		activity.LinkedSubjectID = uuid.MustParse(req.LinkedSubjectID)
	}

	if err := s.repo.CreateKokurikulerActivity(ctx, activity); err != nil {
		return nil, err
	}
	return activity, nil
}

func (s *curriculumService) UpdateKokurikulerActivity(ctx context.Context, id string, req UpdateKokurikulerActivityRequest) (*KokurikulerActivity, error) {
	activity, err := s.repo.GetKokurikulerActivityByID(ctx, id)
	if err != nil {
		return nil, errors.New("aktivitas kokurikuler tidak ditemukan")
	}

	if req.ActivityName != "" {
		activity.ActivityName = req.ActivityName
	}
	if req.LinkedSubjectID != "" {
		activity.LinkedSubjectID = uuid.MustParse(req.LinkedSubjectID)
	}
	if req.Description != "" {
		activity.Description = req.Description
	}
	if req.Schedule != "" {
		activity.Schedule = req.Schedule
	}
	if req.IsActive != nil {
		activity.IsActive = *req.IsActive
	}

	if err := s.repo.UpdateKokurikulerActivity(ctx, activity); err != nil {
		return nil, err
	}
	return activity, nil
}

func (s *curriculumService) DeleteKokurikulerActivity(ctx context.Context, id string) error {
	return s.repo.DeleteKokurikulerActivity(ctx, id)
}

// Extra-curricular Activities Methods
func (s *curriculumService) GetAllEkstrakurikulerActivities(ctx context.Context) ([]EkstrakurikulerActivity, error) {
	return s.repo.GetAllEkstrakurikulerActivities(ctx)
}

func (s *curriculumService) GetEkstrakurikulerActivityByID(ctx context.Context, id string) (*EkstrakurikulerActivity, error) {
	return s.repo.GetEkstrakurikulerActivityByID(ctx, id)
}

func (s *curriculumService) CreateEkstrakurikulerActivity(ctx context.Context, req CreateEkstrakurikulerActivityRequest) (*EkstrakurikulerActivity, error) {
	isActive := true
	if req.IsActive != nil {
		isActive = *req.IsActive
	}

	activity := &EkstrakurikulerActivity{
		ID:                   uuid.New(),
		CurriculumDocumentID: uuid.MustParse(req.CurriculumDocumentID),
		ActivityName:         req.ActivityName,
		ActivityCategory:     req.ActivityCategory,
		Description:          req.Description,
		Schedule:             req.Schedule,
		IsActive:             isActive,
	}

	if req.InstructorID != "" {
		activity.InstructorID = uuid.MustParse(req.InstructorID)
	}

	if err := s.repo.CreateEkstrakurikulerActivity(ctx, activity); err != nil {
		return nil, err
	}
	return activity, nil
}

func (s *curriculumService) UpdateEkstrakurikulerActivity(ctx context.Context, id string, req UpdateEkstrakurikulerActivityRequest) (*EkstrakurikulerActivity, error) {
	activity, err := s.repo.GetEkstrakurikulerActivityByID(ctx, id)
	if err != nil {
		return nil, errors.New("aktivitas ekstrakurikuler tidak ditemukan")
	}

	if req.ActivityName != "" {
		activity.ActivityName = req.ActivityName
	}
	if req.ActivityCategory != "" {
		activity.ActivityCategory = req.ActivityCategory
	}
	if req.Description != "" {
		activity.Description = req.Description
	}
	if req.Schedule != "" {
		activity.Schedule = req.Schedule
	}
	if req.InstructorID != "" {
		activity.InstructorID = uuid.MustParse(req.InstructorID)
	}
	if req.IsActive != nil {
		activity.IsActive = *req.IsActive
	}

	if err := s.repo.UpdateEkstrakurikulerActivity(ctx, activity); err != nil {
		return nil, err
	}
	return activity, nil
}

func (s *curriculumService) DeleteEkstrakurikulerActivity(ctx context.Context, id string) error {
	return s.repo.DeleteEkstrakurikulerActivity(ctx, id)
}

// Analysis Data Integration Methods (FR 4.2.1-4.2.5)

func (s *curriculumService) IntegrateSWOTData(ctx context.Context, req AnalysisDataIntegrationRequest) (*AnalysisDataIntegrationResponse, error) {
	// Placeholder implementation for SWOT data integration
	// In production, this would:
	// 1. Fetch SWOT data from strategic_planning module
	// 2. Process and format the data for KSP inclusion
	// 3. Generate appropriate content sections
	// 4. Store integration record

	integrationID := uuid.New().String()

	swotData := &SWOTDataForKSP{
		SessionID:     req.SWOTSessionID,
		SessionName:   "SWOT Analysis Session",
		Strengths:     []SWOTItem{},
		Weaknesses:    []SWOTItem{},
		Opportunities: []SWOTItem{},
		Threats:       []SWOTItem{},
		AnalysisDate:  time.Now().Format(time.RFC3339),
	}

	response := &AnalysisDataIntegrationResponse{
		CurriculumDocumentID: req.CurriculumDocumentID,
		IntegrationID:        integrationID,
		AnalysisData: AnalysisDataSummary{
			SWOTData: swotData,
		},
		GeneratedContent: GeneratedContent{
			ExecutiveSummary: "Ringkasan eksekutif berdasarkan analisis SWOT...",
			AnalysisSection:  "Bagian analisis SWOT yang terintegrasi...",
			Recommendations:  []string{"Rekomendasi berdasarkan SWOT..."},
			ActionPlan:       "Rencana aksi berdasarkan analisis SWOT...",
			Charts:           map[string]string{"swot_chart": "/charts/swot/analysis.png"},
		},
		Status:  "SUCCESS",
		Message: "SWOT data berhasil diintegrasikan ke KSP",
	}

	return response, nil
}

func (s *curriculumService) IntegrateRootCauseData(ctx context.Context, req AnalysisDataIntegrationRequest) (*AnalysisDataIntegrationResponse, error) {
	// Placeholder implementation for Root Cause data integration
	integrationID := uuid.New().String()

	rootCauseData := &RootCauseDataForKSP{
		RootCauseID:      req.RootCauseID,
		ProblemStatement: "Identifikasi masalah utama...",
		RootCauses:       []RootCauseItem{},
		FiveWhysAnalysis: []FiveWhysStep{},
		Solutions:        []SolutionItem{},
		AnalysisDate:     time.Now().Format(time.RFC3339),
	}

	response := &AnalysisDataIntegrationResponse{
		CurriculumDocumentID: req.CurriculumDocumentID,
		IntegrationID:        integrationID,
		AnalysisData: AnalysisDataSummary{
			RootCauseData: rootCauseData,
		},
		GeneratedContent: GeneratedContent{
			ExecutiveSummary: "Ringkasan eksekutif berdasarkan analisis akar masalah...",
			AnalysisSection:  "Bagian analisis akar masalah yang terintegrasi...",
			Recommendations:  []string{"Rekomendasi berdasarkan root cause analysis..."},
			ActionPlan:       "Rencana aksi berdasarkan solusi yang diidentifikasi...",
			Charts:           map[string]string{"root_cause_chart": "/charts/root-cause/analysis.png"},
		},
		Status:  "SUCCESS",
		Message: "Root Cause data berhasil diintegrasikan ke KSP",
	}

	return response, nil
}

func (s *curriculumService) IntegrateFishboneData(ctx context.Context, req AnalysisDataIntegrationRequest) (*AnalysisDataIntegrationResponse, error) {
	// Placeholder implementation for Fishbone data integration
	integrationID := uuid.New().String()

	fishboneData := &FishboneDataForKSP{
		DiagramID:        req.FishboneDiagramID,
		DiagramName:      "Fishbone Diagram Analysis",
		ProblemStatement: "Identifikasi masalah menggunakan fishbone diagram...",
		Categories:       []FishboneCategory{},
		AnalysisDate:     time.Now().Format(time.RFC3339),
	}

	response := &AnalysisDataIntegrationResponse{
		CurriculumDocumentID: req.CurriculumDocumentID,
		IntegrationID:        integrationID,
		AnalysisData: AnalysisDataSummary{
			FishboneData: fishboneData,
		},
		GeneratedContent: GeneratedContent{
			ExecutiveSummary: "Ringkasan eksekutif berdasarkan analisis fishbone...",
			AnalysisSection:  "Bagian analisis fishbone yang terintegrasi...",
			Recommendations:  []string{"Rekomendasi berdasarkan fishbone analysis..."},
			ActionPlan:       "Rencana aksi berdasarkan kategori penyebab...",
			Charts:           map[string]string{"fishbone_chart": "/charts/fishbone/analysis.png"},
		},
		Status:  "SUCCESS",
		Message: "Fishbone data berhasil diintegrasikan ke KSP",
	}

	return response, nil
}

func (s *curriculumService) IntegrateStudentNeedsData(ctx context.Context, req AnalysisDataIntegrationRequest) (*AnalysisDataIntegrationResponse, error) {
	// Placeholder implementation for Student Needs data integration
	integrationID := uuid.New().String()

	studentNeedsData := &StudentNeedsDataForKSP{
		ProfileID:            req.StudentNeedsProfileID,
		ProfileName:          "Student Needs Profile",
		ProfileDimension:     "Akademik",
		Needs:                []StudentNeedItem{},
		PriorityDistribution: map[string]int{},
		AnalysisDate:         time.Now().Format(time.RFC3339),
	}

	response := &AnalysisDataIntegrationResponse{
		CurriculumDocumentID: req.CurriculumDocumentID,
		IntegrationID:        integrationID,
		AnalysisData: AnalysisDataSummary{
			StudentNeedsData: studentNeedsData,
		},
		GeneratedContent: GeneratedContent{
			ExecutiveSummary: "Ringkasan eksekutif berdasarkan analisis kebutuhan siswa...",
			AnalysisSection:  "Bagian analisis kebutuhan siswa yang terintegrasi...",
			Recommendations:  []string{"Rekomendasi berdasarkan student needs analysis..."},
			ActionPlan:       "Rencana aksi berdasarkan kebutuhan prioritas...",
			Charts:           map[string]string{"student_needs_chart": "/charts/student-needs/analysis.png"},
		},
		Status:  "SUCCESS",
		Message: "Student Needs data berhasil diintegrasikan ke KSP",
	}

	return response, nil
}

func (s *curriculumService) GenerateKSPWithAnalysis(ctx context.Context, req KSPExportWithAnalysisRequest) (*KSPExportWithAnalysisResponse, error) {
	// Placeholder implementation for KSP generation with analysis data
	// In production, this would:
	// 1. Fetch the curriculum document
	// 2. If IncludeAnalysisData is true, fetch integrated analysis data
	// 3. Generate the document with analysis data included
	// 4. Create PDF/Word export
	// 5. Return download URL

	exportID := uuid.New().String()
	generatedAt := time.Now()
	expiresAt := generatedAt.Add(24 * time.Hour) // Expires in 24 hours

	documentURL := fmt.Sprintf("/exports/ksp/%s.%s", exportID, strings.ToLower(req.Format))

	response := &KSPExportWithAnalysisResponse{
		ExportID:    exportID,
		DocumentURL: documentURL,
		Format:      req.Format,
		FileSize:    1024 * 1024, // 1MB placeholder
		GeneratedAt: generatedAt.Format(time.RFC3339),
		ExpiresAt:   expiresAt.Format(time.RFC3339),
	}

	return response, nil
}
