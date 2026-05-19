package curriculum

import (
	"context"
	"errors"

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
		AcademicYearID: req.AcademicYearID,
		SchoolID:       req.SchoolID,
		Status:         "DRAFT",
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
