package learning_experience

import (
	"context"
	"errors"
	"time"

	"github.com/google/uuid"
)

type LearningExperienceService interface {
	// Learning Experience CRUD
	CreateLearningExperience(ctx context.Context, req *CreateLearningExperienceRequest) (*LearningExperienceResponse, error)
	GetLearningExperienceByID(ctx context.Context, id uuid.UUID) (*LearningExperienceResponse, error)
	GetAllLearningExperiences(ctx context.Context) ([]LearningExperienceResponse, error)
	GetActiveLearningExperiences(ctx context.Context) ([]LearningExperienceResponse, error)
	UpdateLearningExperience(ctx context.Context, id uuid.UUID, req *UpdateLearningExperienceRequest) (*LearningExperienceResponse, error)
	DeleteLearningExperience(ctx context.Context, id uuid.UUID) error
	GetLearningExperienceByCode(ctx context.Context, code string) (*LearningExperienceResponse, error)

	// Activity Experience Mapping
	LinkActivityToExperience(ctx context.Context, req *ActivityExperienceMappingRequest) error
	UnlinkActivityFromExperience(ctx context.Context, activityID uuid.UUID) error
	GetExperienceByActivityID(ctx context.Context, activityID uuid.UUID) (*LearningExperienceResponse, error)

	// Student Experience Progression
	CreateStudentProgression(ctx context.Context, req *CreateStudentProgressionRequest) (*StudentExperienceProgressionResponse, error)
	GetStudentProgressionByID(ctx context.Context, id uuid.UUID) (*StudentExperienceProgressionResponse, error)
	UpdateStudentProgression(ctx context.Context, id uuid.UUID, req *UpdateStudentProgressionRequest) (*StudentExperienceProgressionResponse, error)
	DeleteStudentProgression(ctx context.Context, id uuid.UUID) error
	GetStudentProgressions(ctx context.Context, studentID uuid.UUID, subjectID uuid.UUID) ([]StudentExperienceProgressionResponse, error)
	GetStudentProgressionSummary(ctx context.Context, studentID uuid.UUID, subjectID uuid.UUID) (*StudentProgressionSummaryResponse, error)
}

type learningExperienceService struct {
	repo LearningExperienceRepository
}

func NewLearningExperienceService(repo LearningExperienceRepository) LearningExperienceService {
	return &learningExperienceService{repo: repo}
}

// Helper function to convert model to response DTO
func modelToResponse(exp *LearningExperience) *LearningExperienceResponse {
	return &LearningExperienceResponse{
		ID:             exp.ID,
		ExperienceCode: exp.ExperienceCode,
		ExperienceName: exp.ExperienceName,
		Description:    exp.Description,
		SequenceOrder:  exp.SequenceOrder,
		KeyIndicators:  exp.KeyIndicators,
		IsActive:       exp.IsActive,
		CreatedAt:      exp.CreatedAt,
		UpdatedAt:      exp.UpdatedAt,
	}
}

func progressionToResponse(prog *StudentExperienceProgression) *StudentExperienceProgressionResponse {
	return &StudentExperienceProgressionResponse{
		ID:             prog.ID,
		StudentID:      prog.StudentID,
		SubjectID:      prog.SubjectID,
		ExperienceID:   prog.ExperienceID,
		MasteryLevel:   prog.MasteryLevel,
		LastAssessedAt: &prog.LastAssessedAt,
		Notes:          prog.Notes,
		CreatedAt:      prog.CreatedAt,
		UpdatedAt:      prog.UpdatedAt,
	}
}

// Learning Experience CRUD

func (s *learningExperienceService) CreateLearningExperience(ctx context.Context, req *CreateLearningExperienceRequest) (*LearningExperienceResponse, error) {
	// Validate experience code
	if !IsValidExperienceCode(req.ExperienceCode) {
		return nil, errors.New("invalid experience code")
	}

	// Check if experience code already exists
	existing, _ := s.repo.GetLearningExperienceByCode(ctx, req.ExperienceCode)
	if existing != nil {
		return nil, errors.New("experience code already exists")
	}

	exp := &LearningExperience{
		ID:             uuid.New(),
		ExperienceCode: req.ExperienceCode,
		ExperienceName: req.ExperienceName,
		Description:    req.Description,
		SequenceOrder:  req.SequenceOrder,
		KeyIndicators:  req.KeyIndicators,
		IsActive:       true,
	}

	err := s.repo.CreateLearningExperience(ctx, exp)
	if err != nil {
		return nil, err
	}

	return modelToResponse(exp), nil
}

func (s *learningExperienceService) GetLearningExperienceByID(ctx context.Context, id uuid.UUID) (*LearningExperienceResponse, error) {
	exp, err := s.repo.GetLearningExperienceByID(ctx, id)
	if err != nil {
		return nil, err
	}
	return modelToResponse(exp), nil
}

func (s *learningExperienceService) GetAllLearningExperiences(ctx context.Context) ([]LearningExperienceResponse, error) {
	experiences, err := s.repo.GetAllLearningExperiences(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]LearningExperienceResponse, len(experiences))
	for i, exp := range experiences {
		responses[i] = *modelToResponse(&exp)
	}
	return responses, nil
}

func (s *learningExperienceService) GetActiveLearningExperiences(ctx context.Context) ([]LearningExperienceResponse, error) {
	experiences, err := s.repo.GetActiveLearningExperiences(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]LearningExperienceResponse, len(experiences))
	for i, exp := range experiences {
		responses[i] = *modelToResponse(&exp)
	}
	return responses, nil
}

func (s *learningExperienceService) UpdateLearningExperience(ctx context.Context, id uuid.UUID, req *UpdateLearningExperienceRequest) (*LearningExperienceResponse, error) {
	exp, err := s.repo.GetLearningExperienceByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.ExperienceName != "" {
		exp.ExperienceName = req.ExperienceName
	}
	if req.Description != "" {
		exp.Description = req.Description
	}
	if req.SequenceOrder != 0 {
		exp.SequenceOrder = req.SequenceOrder
	}
	if req.KeyIndicators != "" {
		exp.KeyIndicators = req.KeyIndicators
	}
	if req.IsActive != nil {
		exp.IsActive = *req.IsActive
	}

	err = s.repo.UpdateLearningExperience(ctx, exp)
	if err != nil {
		return nil, err
	}

	return modelToResponse(exp), nil
}

func (s *learningExperienceService) DeleteLearningExperience(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteLearningExperience(ctx, id)
}

func (s *learningExperienceService) GetLearningExperienceByCode(ctx context.Context, code string) (*LearningExperienceResponse, error) {
	exp, err := s.repo.GetLearningExperienceByCode(ctx, code)
	if err != nil {
		return nil, err
	}
	return modelToResponse(exp), nil
}

// Activity Experience Mapping

func (s *learningExperienceService) LinkActivityToExperience(ctx context.Context, req *ActivityExperienceMappingRequest) error {
	// Validate experience exists
	exp, err := s.repo.GetLearningExperienceByID(ctx, req.ExperienceID)
	if err != nil || exp == nil {
		return errors.New("experience not found")
	}

	mapping := &ActivityExperienceMapping{
		ActivityID:   req.ActivityID,
		ExperienceID: req.ExperienceID,
		CreatedAt:    time.Now(),
	}

	return s.repo.CreateActivityExperienceMapping(ctx, mapping)
}

func (s *learningExperienceService) UnlinkActivityFromExperience(ctx context.Context, activityID uuid.UUID) error {
	return s.repo.DeleteActivityExperienceMapping(ctx, activityID)
}

func (s *learningExperienceService) GetExperienceByActivityID(ctx context.Context, activityID uuid.UUID) (*LearningExperienceResponse, error) {
	exp, err := s.repo.GetExperienceByActivityID(ctx, activityID)
	if err != nil {
		return nil, err
	}
	return modelToResponse(exp), nil
}

// Student Experience Progression

func (s *learningExperienceService) CreateStudentProgression(ctx context.Context, req *CreateStudentProgressionRequest) (*StudentExperienceProgressionResponse, error) {
	// Validate experience exists
	exp, err := s.repo.GetLearningExperienceByID(ctx, req.ExperienceID)
	if err != nil || exp == nil {
		return nil, errors.New("experience not found")
	}

	now := time.Now()
	progression := &StudentExperienceProgression{
		ID:             uuid.New(),
		StudentID:      req.StudentID,
		SubjectID:      req.SubjectID,
		ExperienceID:   req.ExperienceID,
		MasteryLevel:   req.MasteryLevel,
		LastAssessedAt: now,
		Notes:          req.Notes,
	}

	err = s.repo.CreateStudentProgression(ctx, progression)
	if err != nil {
		return nil, err
	}

	return progressionToResponse(progression), nil
}

func (s *learningExperienceService) GetStudentProgressionByID(ctx context.Context, id uuid.UUID) (*StudentExperienceProgressionResponse, error) {
	prog, err := s.repo.GetStudentProgressionByID(ctx, id)
	if err != nil {
		return nil, err
	}
	return progressionToResponse(prog), nil
}

func (s *learningExperienceService) UpdateStudentProgression(ctx context.Context, id uuid.UUID, req *UpdateStudentProgressionRequest) (*StudentExperienceProgressionResponse, error) {
	prog, err := s.repo.GetStudentProgressionByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.MasteryLevel != nil {
		prog.MasteryLevel = *req.MasteryLevel
	}
	if req.Notes != nil {
		prog.Notes = *req.Notes
	}
	if req.LastAssessedAt != nil {
		prog.LastAssessedAt = *req.LastAssessedAt
	} else {
		prog.LastAssessedAt = time.Now()
	}

	err = s.repo.UpdateStudentProgression(ctx, prog)
	if err != nil {
		return nil, err
	}

	return progressionToResponse(prog), nil
}

func (s *learningExperienceService) DeleteStudentProgression(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteStudentProgression(ctx, id)
}

func (s *learningExperienceService) GetStudentProgressions(ctx context.Context, studentID uuid.UUID, subjectID uuid.UUID) ([]StudentExperienceProgressionResponse, error) {
	progressions, err := s.repo.GetStudentProgressions(ctx, studentID, subjectID)
	if err != nil {
		return nil, err
	}

	responses := make([]StudentExperienceProgressionResponse, len(progressions))
	for i, prog := range progressions {
		responses[i] = *progressionToResponse(&prog)
	}
	return responses, nil
}

func (s *learningExperienceService) GetStudentProgressionSummary(ctx context.Context, studentID uuid.UUID, subjectID uuid.UUID) (*StudentProgressionSummaryResponse, error) {
	progressions, err := s.repo.GetStudentProgressionsBySubject(ctx, studentID, subjectID)
	if err != nil {
		return nil, err
	}

	// Calculate average mastery
	totalMastery := 0.0
	for _, prog := range progressions {
		totalMastery += prog.MasteryLevel
	}

	averageMastery := 0.0
	if len(progressions) > 0 {
		averageMastery = totalMastery / float64(len(progressions))
	}

	// Determine readiness status
	readinessStatus := "NOT_READY"
	if averageMastery >= 0.8 {
		readinessStatus = "READY"
	} else if averageMastery >= 0.5 {
		readinessStatus = "NEEDS_IMPROVEMENT"
	}

	detailedResponses := make([]StudentProgressionDetailResponse, len(progressions))
	for i, prog := range progressions {
		// Get experience details
		exp, _ := s.repo.GetLearningExperienceByID(ctx, prog.ExperienceID)

		detailedResponses[i] = StudentProgressionDetailResponse{
			ID:             prog.ID,
			StudentID:      prog.StudentID,
			SubjectID:      prog.SubjectID,
			ExperienceID:   prog.ExperienceID,
			ExperienceCode: "",
			ExperienceName: "",
			MasteryLevel:   prog.MasteryLevel,
			LastAssessedAt: &prog.LastAssessedAt,
			Notes:          prog.Notes,
			CreatedAt:      prog.CreatedAt,
			UpdatedAt:      prog.UpdatedAt,
		}

		if exp != nil {
			detailedResponses[i].ExperienceCode = exp.ExperienceCode
			detailedResponses[i].ExperienceName = exp.ExperienceName
		}
	}

	return &StudentProgressionSummaryResponse{
		StudentID:       studentID,
		SubjectID:       subjectID,
		Progressions:    detailedResponses,
		AverageMastery:  averageMastery,
		ReadinessStatus: readinessStatus,
	}, nil
}
