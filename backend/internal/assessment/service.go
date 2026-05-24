package assessment

import (
	"context"
	"errors"
	"time"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type AssessmentService interface {
	GetByTeachingAssignment(ctx context.Context, assignmentID string) ([]Assessment, error)
	GetByID(ctx context.Context, id string) (*Assessment, error)
	Create(ctx context.Context, assignmentID string, req CreateAssessmentRequest) (*Assessment, error)
	Update(ctx context.Context, id string, req UpdateAssessmentRequest) (*Assessment, error)
	Delete(ctx context.Context, id string) error

	GetScores(ctx context.Context, assessmentID string) ([]AssessmentScore, error)
	UpsertScores(ctx context.Context, assessmentID string, req UpsertScoresRequest) error

	// Attendance
	GetAttendances(ctx context.Context, classroomID string, date string) ([]DailyAttendance, error)
	UpsertAttendances(ctx context.Context, classroomID string, date string, req UpsertAttendancesRequest) error

	// Age Appropriate Types
	GetAgeAppropriateTypes() []AgeAppropriateTypeResponse

	// SD Assessment Criteria
	GetAllSDAssessmentCriteria(ctx context.Context) ([]SDAssessmentCriteriaResponse, error)
	GetSDAssessmentCriteriaByType(ctx context.Context, assessmentType string) ([]SDAssessmentCriteriaResponse, error)
	GetSDAssessmentCriteriaByPhase(ctx context.Context, phaseID string) ([]SDAssessmentCriteriaResponse, error)
	CreateSDAssessmentCriteria(ctx context.Context, req CreateSDAssessmentCriteriaRequest) (*SDAssessmentCriteriaResponse, error)
	UpdateSDAssessmentCriteria(ctx context.Context, id string, req UpdateSDAssessmentCriteriaRequest) (*SDAssessmentCriteriaResponse, error)
	DeleteSDAssessmentCriteria(ctx context.Context, id string) error
}

type assessmentService struct {
	repo AssessmentRepository
}

func NewAssessmentService(repo AssessmentRepository) AssessmentService {
	return &assessmentService{repo: repo}
}

func (s *assessmentService) GetByTeachingAssignment(ctx context.Context, assignmentID string) ([]Assessment, error) {
	return s.repo.GetByTeachingAssignment(ctx, assignmentID)
}

func (s *assessmentService) GetByID(ctx context.Context, id string) (*Assessment, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *assessmentService) Create(ctx context.Context, assignmentID string, req CreateAssessmentRequest) (*Assessment, error) {
	// 1. Verifikasi kepemilikan Teaching Assignment
	if err := common.CheckTeachingAssignmentOwnership(ctx, assignmentID); err != nil {
		return nil, err
	}

	assignmentUUID, _ := uuid.Parse(assignmentID)
	date, err := time.Parse("2006-01-02", req.AssessmentDate)
	if err != nil {
		return nil, errors.New("format tanggal tidak valid, gunakan YYYY-MM-DD")
	}

	assessment := &Assessment{
		ID:                   uuid.New(),
		TeachingAssignmentID: assignmentUUID,
		AssessmentName:       req.AssessmentName,
		AssessmentType:       req.AssessmentType,
		AgeAppropriateType:   req.AgeAppropriateType,
		AssessmentDate:       date,
	}

	// Validate age appropriate type if provided
	if req.AgeAppropriateType != "" && !IsValidAgeAppropriateType(req.AgeAppropriateType) {
		return nil, errors.New("tipe asesmen yang sesuai usia tidak valid")
	}

	if err := s.repo.Create(ctx, assessment); err != nil {
		return nil, err
	}
	return assessment, nil
}

func (s *assessmentService) Update(ctx context.Context, id string, req UpdateAssessmentRequest) (*Assessment, error) {
	a, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("assessment tidak ditemukan")
	}

	// 1. Verifikasi kepemilikan via Teaching Assignment
	if err := common.CheckTeachingAssignmentOwnership(ctx, a.TeachingAssignmentID.String()); err != nil {
		return nil, err
	}

	if req.AssessmentName != "" {
		a.AssessmentName = req.AssessmentName
	}
	if req.AssessmentType != "" {
		a.AssessmentType = req.AssessmentType
	}
	if req.AgeAppropriateType != "" {
		if req.AgeAppropriateType != "" && !IsValidAgeAppropriateType(req.AgeAppropriateType) {
			return nil, errors.New("tipe asesmen yang sesuai usia tidak valid")
		}
		a.AgeAppropriateType = req.AgeAppropriateType
	}
	if req.AssessmentDate != "" {
		date, err := time.Parse("2006-01-02", req.AssessmentDate)
		if err != nil {
			return nil, errors.New("format tanggal tidak valid")
		}
		a.AssessmentDate = date
	}

	if err := s.repo.Update(ctx, a); err != nil {
		return nil, err
	}
	return a, nil
}

func (s *assessmentService) Delete(ctx context.Context, id string) error {
	a, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("assessment tidak ditemukan")
	}

	// 1. Verifikasi kepemilikan
	if err := common.CheckTeachingAssignmentOwnership(ctx, a.TeachingAssignmentID.String()); err != nil {
		return err
	}

	return s.repo.Delete(ctx, id)
}

func (s *assessmentService) GetScores(ctx context.Context, assessmentID string) ([]AssessmentScore, error) {
	return s.repo.GetScoresByAssessment(ctx, assessmentID)
}

func (s *assessmentService) UpsertScores(ctx context.Context, assessmentID string, req UpsertScoresRequest) error {
	a, err := s.repo.GetByID(ctx, assessmentID)
	if err != nil {
		return errors.New("assessment tidak ditemukan")
	}

	// 1. Verifikasi kepemilikan
	if err := common.CheckTeachingAssignmentOwnership(ctx, a.TeachingAssignmentID.String()); err != nil {
		return err
	}

	assessUUID, _ := uuid.Parse(assessmentID)
	var scores []AssessmentScore

	for _, item := range req.Scores {
		studentUUID, _ := uuid.Parse(item.StudentID)
		scores = append(scores, AssessmentScore{
			AssessmentID: assessUUID,
			StudentID:    studentUUID,
			Score:        item.Score,
			Notes:        item.Notes,
		})
	}

	return s.repo.UpsertScores(ctx, assessmentID, scores)
}

func (s *assessmentService) GetAttendances(ctx context.Context, classroomID string, date string) ([]DailyAttendance, error) {
	if classroomID == "" || date == "" {
		return nil, errors.New("classroom_id and date are required")
	}
	return s.repo.GetAttendancesByClassroomAndDate(ctx, classroomID, date)
}

func (s *assessmentService) UpsertAttendances(ctx context.Context, classroomID string, date string, req UpsertAttendancesRequest) error {
	parsedClassroomID, err := uuid.Parse(classroomID)
	if err != nil {
		return errors.New("invalid classroom ID format")
	}

	parsedDate, err := time.Parse("2006-01-02", date)
	if err != nil {
		return errors.New("invalid date format, must be YYYY-MM-DD")
	}

	var attendances []DailyAttendance
	for _, item := range req.Attendances {
		studentUUID, err := uuid.Parse(item.StudentID)
		if err != nil {
			return errors.New("invalid student ID: " + item.StudentID)
		}
		attendances = append(attendances, DailyAttendance{
			ClassroomID: parsedClassroomID,
			StudentID:   studentUUID,
			Date:        parsedDate,
			Status:      item.Status,
			Notes:       item.Notes,
		})
	}

	return s.repo.UpsertAttendances(ctx, attendances)
}

func (s *assessmentService) GetAgeAppropriateTypes() []AgeAppropriateTypeResponse {
	return []AgeAppropriateTypeResponse{
		{ID: AssessmentTypeFaseAObservation, Description: GetAgeAppropriateTypeDescription(AssessmentTypeFaseAObservation)},
		{ID: AssessmentTypeFaseAPortfolio, Description: GetAgeAppropriateTypeDescription(AssessmentTypeFaseAPortfolio)},
		{ID: AssessmentTypeFaseBPerformance, Description: GetAgeAppropriateTypeDescription(AssessmentTypeFaseBPerformance)},
		{ID: AssessmentTypeFaseBProject, Description: GetAgeAppropriateTypeDescription(AssessmentTypeFaseBProject)},
		{ID: AssessmentTypeFaseCProjectComplex, Description: GetAgeAppropriateTypeDescription(AssessmentTypeFaseCProjectComplex)},
		{ID: AssessmentTypeFaseCCollaborative, Description: GetAgeAppropriateTypeDescription(AssessmentTypeFaseCCollaborative)},
		{ID: AssessmentTypeFaseCPeerAssessment, Description: GetAgeAppropriateTypeDescription(AssessmentTypeFaseCPeerAssessment)},
	}
}

// SD Assessment Criteria Methods
func (s *assessmentService) GetAllSDAssessmentCriteria(ctx context.Context) ([]SDAssessmentCriteriaResponse, error) {
	criteria, err := s.repo.GetAllSDAssessmentCriteria(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]SDAssessmentCriteriaResponse, len(criteria))
	for i, criterion := range criteria {
		responses[i] = s.sdCriteriaToResponse(&criterion)
	}
	return responses, nil
}

func (s *assessmentService) GetSDAssessmentCriteriaByType(ctx context.Context, assessmentType string) ([]SDAssessmentCriteriaResponse, error) {
	criteria, err := s.repo.GetSDAssessmentCriteriaByType(ctx, assessmentType)
	if err != nil {
		return nil, err
	}

	responses := make([]SDAssessmentCriteriaResponse, len(criteria))
	for i, criterion := range criteria {
		responses[i] = s.sdCriteriaToResponse(&criterion)
	}
	return responses, nil
}

func (s *assessmentService) GetSDAssessmentCriteriaByPhase(ctx context.Context, phaseID string) ([]SDAssessmentCriteriaResponse, error) {
	criteria, err := s.repo.GetSDAssessmentCriteriaByPhase(ctx, phaseID)
	if err != nil {
		return nil, err
	}

	responses := make([]SDAssessmentCriteriaResponse, len(criteria))
	for i, criterion := range criteria {
		responses[i] = s.sdCriteriaToResponse(&criterion)
	}
	return responses, nil
}

func (s *assessmentService) CreateSDAssessmentCriteria(ctx context.Context, req CreateSDAssessmentCriteriaRequest) (*SDAssessmentCriteriaResponse, error) {
	// Validate assessment type if provided
	if req.AssessmentType != "" && !IsValidAgeAppropriateType(req.AssessmentType) {
		return nil, errors.New("tipe asesmen tidak valid")
	}

	isActive := true
	if req.IsActive != nil {
		isActive = *req.IsActive
	}

	criterion := &SDAssessmentCriteria{
		ID:             uuid.New(),
		AssessmentType: req.AssessmentType,
		CriteriaName:   req.CriteriaName,
		Description:    req.Description,
		RubricElements: req.RubricElements,
		IsActive:       isActive,
	}

	if req.PhaseID != "" {
		criterion.PhaseID = uuid.MustParse(req.PhaseID)
	}

	criterion.CreatedAt = time.Now()
	criterion.UpdatedAt = time.Now()

	if err := s.repo.CreateSDAssessmentCriteria(ctx, criterion); err != nil {
		return nil, err
	}

	res := s.sdCriteriaToResponse(criterion)
	return &res, nil
}

func (s *assessmentService) UpdateSDAssessmentCriteria(ctx context.Context, id string, req UpdateSDAssessmentCriteriaRequest) (*SDAssessmentCriteriaResponse, error) {
	criterion, err := s.repo.GetSDAssessmentCriteriaByID(ctx, id)
	if err != nil {
		return nil, errors.New("kriteria asesmen SD tidak ditemukan")
	}

	if req.AssessmentType != "" {
		if !IsValidAgeAppropriateType(req.AssessmentType) {
			return nil, errors.New("tipe asesmen tidak valid")
		}
		criterion.AssessmentType = req.AssessmentType
	}
	if req.PhaseID != "" {
		criterion.PhaseID = uuid.MustParse(req.PhaseID)
	}
	if req.CriteriaName != "" {
		criterion.CriteriaName = req.CriteriaName
	}
	if req.Description != "" {
		criterion.Description = req.Description
	}
	if req.RubricElements != "" {
		criterion.RubricElements = req.RubricElements
	}
	if req.IsActive != nil {
		criterion.IsActive = *req.IsActive
	}

	criterion.UpdatedAt = time.Now()

	if err := s.repo.UpdateSDAssessmentCriteria(ctx, criterion); err != nil {
		return nil, err
	}

	res := s.sdCriteriaToResponse(criterion)
	return &res, nil
}

func (s *assessmentService) DeleteSDAssessmentCriteria(ctx context.Context, id string) error {
	return s.repo.DeleteSDAssessmentCriteria(ctx, id)
}

func (s *assessmentService) sdCriteriaToResponse(criterion *SDAssessmentCriteria) SDAssessmentCriteriaResponse {
	var phaseID string
	if criterion.PhaseID != uuid.Nil {
		phaseID = criterion.PhaseID.String()
	}

	return SDAssessmentCriteriaResponse{
		ID:              criterion.ID.String(),
		AssessmentType:  criterion.AssessmentType,
		PhaseID:         phaseID,
		CriteriaName:    criterion.CriteriaName,
		Description:     criterion.Description,
		RubricElements:  criterion.RubricElements,
		IsActive:        criterion.IsActive,
		TypeDescription: GetAgeAppropriateTypeDescription(criterion.AssessmentType),
		CreatedAt:       criterion.CreatedAt.Format(time.RFC3339),
		UpdatedAt:       criterion.UpdatedAt.Format(time.RFC3339),
	}
}
