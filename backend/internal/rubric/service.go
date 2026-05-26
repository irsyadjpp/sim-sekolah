package rubric

import (
	"context"
	"fmt"

	"github.com/google/uuid"
)

type Service interface {
	// Rubric operations
	CreateRubric(ctx context.Context, request CreateRubricRequest) (*RubricResponse, error)
	GetRubricByID(id uuid.UUID) (*RubricResponse, error)
	GetRubrics(filter map[string]interface{}) ([]RubricResponse, error)
	UpdateRubric(ctx context.Context, id uuid.UUID, request UpdateRubricRequest) (*RubricResponse, error)
	DeleteRubric(ctx context.Context, id uuid.UUID) error
	GetRubricTemplates(assessmentType string) ([]RubricResponse, error)
	CopyRubric(ctx context.Context, id uuid.UUID, request RubricCopyRequest) (*RubricResponse, error)

	// RubricCriteria operations
	CreateCriteria(ctx context.Context, rubricID uuid.UUID, request CreateRubricCriteriaRequest) (*RubricCriteriaResponse, error)
	GetCriteriaByID(id uuid.UUID) (*RubricCriteriaResponse, error)
	GetCriteriaByRubric(rubricID uuid.UUID) ([]RubricCriteriaResponse, error)
	UpdateCriteria(ctx context.Context, id uuid.UUID, request UpdateRubricCriteriaRequest) (*RubricCriteriaResponse, error)
	DeleteCriteria(ctx context.Context, id uuid.UUID) error

	// RubricLevel operations
	CreateLevel(ctx context.Context, rubricID uuid.UUID, request CreateRubricLevelRequest) (*RubricLevelResponse, error)
	GetLevelByID(id uuid.UUID) (*RubricLevelResponse, error)
	GetLevelsByRubric(rubricID uuid.UUID) ([]RubricLevelResponse, error)
	UpdateLevel(ctx context.Context, id uuid.UUID, request UpdateRubricLevelRequest) (*RubricLevelResponse, error)
	DeleteLevel(ctx context.Context, id uuid.UUID) error

	// RubricCriteriaLevel operations
	CreateCriteriaLevel(ctx context.Context, criteriaID uuid.UUID, request CreateRubricCriteriaLevelRequest) (*RubricCriteriaLevelResponse, error)
	GetCriteriaLevels(criteriaID uuid.UUID) ([]RubricCriteriaLevelResponse, error)
	UpdateCriteriaLevel(ctx context.Context, id uuid.UUID, request UpdateRubricCriteriaLevelRequest) (*RubricCriteriaLevelResponse, error)
	DeleteCriteriaLevel(ctx context.Context, id uuid.UUID) error
}

type service struct {
	repo Repository
}

func NewService(repo Repository) Service {
	return &service{repo: repo}
}

// Rubric operations
func (s *service) CreateRubric(ctx context.Context, request CreateRubricRequest) (*RubricResponse, error) {
	var subjectID *uuid.UUID
	if request.SubjectID != "" {
		parsedID, err := uuid.Parse(request.SubjectID)
		if err != nil {
			return nil, fmt.Errorf("invalid subject ID: %w", err)
		}
		subjectID = &parsedID
	}

	rubric := &Rubric{
		ID:             uuid.New(),
		Title:          request.Title,
		Description:    request.Description,
		SubjectID:      subjectID,
		AssessmentType: request.AssessmentType,
		GradeLevel:     request.GradeLevel,
		MaxScore:       request.MaxScore,
		IsTemplate:     request.IsTemplate,
		IsActive:       true,
	}

	if rubric.MaxScore == 0 {
		rubric.MaxScore = 100
	}
	if rubric.GradeLevel == "" {
		rubric.GradeLevel = GradeAll
	}

	err := s.repo.CreateRubric(ctx, rubric)
	if err != nil {
		return nil, err
	}

	// Create criteria if provided
	for _, criteriaReq := range request.Criteria {
		_, err := s.CreateCriteria(ctx, rubric.ID, criteriaReq)
		if err != nil {
			return nil, fmt.Errorf("failed to create criteria: %w", err)
		}
	}

	// Create levels if provided
	for _, levelReq := range request.Levels {
		_, err := s.CreateLevel(ctx, rubric.ID, levelReq)
		if err != nil {
			return nil, fmt.Errorf("failed to create level: %w", err)
		}
	}

	return s.GetRubricByID(rubric.ID)
}

func (s *service) GetRubricByID(id uuid.UUID) (*RubricResponse, error) {
	rubric, err := s.repo.GetRubricByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToRubricResponse(rubric), nil
}

func (s *service) GetRubrics(filter map[string]interface{}) ([]RubricResponse, error) {
	rubrics, err := s.repo.GetRubrics(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]RubricResponse, len(rubrics))
	for i, rubric := range rubrics {
		responses[i] = *s.modelToRubricResponse(&rubric)
	}
	return responses, nil
}

func (s *service) UpdateRubric(ctx context.Context, id uuid.UUID, request UpdateRubricRequest) (*RubricResponse, error) {
	rubric, err := s.repo.GetRubricByID(id)
	if err != nil {
		return nil, err
	}

	if request.Title != "" {
		rubric.Title = request.Title
	}
	if request.Description != "" {
		rubric.Description = request.Description
	}
	if request.SubjectID != "" {
		parsedID, err := uuid.Parse(request.SubjectID)
		if err != nil {
			return nil, fmt.Errorf("invalid subject ID: %w", err)
		}
		rubric.SubjectID = &parsedID
	}
	if request.AssessmentType != "" {
		rubric.AssessmentType = request.AssessmentType
	}
	if request.GradeLevel != "" {
		rubric.GradeLevel = request.GradeLevel
	}
	if request.MaxScore != 0 {
		rubric.MaxScore = request.MaxScore
	}
	rubric.IsTemplate = request.IsTemplate
	rubric.IsActive = request.IsActive

	err = s.repo.UpdateRubric(ctx, rubric)
	if err != nil {
		return nil, err
	}

	return s.GetRubricByID(rubric.ID)
}

func (s *service) DeleteRubric(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteRubric(ctx, id)
}

func (s *service) GetRubricTemplates(assessmentType string) ([]RubricResponse, error) {
	rubrics, err := s.repo.GetRubricTemplates(assessmentType)
	if err != nil {
		return nil, err
	}

	responses := make([]RubricResponse, len(rubrics))
	for i, rubric := range rubrics {
		responses[i] = *s.modelToRubricResponse(&rubric)
	}
	return responses, nil
}

func (s *service) CopyRubric(ctx context.Context, id uuid.UUID, request RubricCopyRequest) (*RubricResponse, error) {
	rubric, err := s.repo.CopyRubric(ctx, id, request.NewTitle)
	if err != nil {
		return nil, err
	}
	return s.modelToRubricResponse(rubric), nil
}

// RubricCriteria operations
func (s *service) CreateCriteria(ctx context.Context, rubricID uuid.UUID, request CreateRubricCriteriaRequest) (*RubricCriteriaResponse, error) {
	criteria := &RubricCriteria{
		ID:          uuid.New(),
		RubricID:    rubricID,
		Title:       request.Title,
		Description: request.Description,
		Weight:      request.Weight,
		Sequence:    request.Sequence,
		IsRequired:  request.IsRequired,
	}

	if criteria.Weight == 0 {
		criteria.Weight = 1.0
	}
	if criteria.Sequence == 0 {
		criteria.Sequence = 1
	}

	err := s.repo.CreateCriteria(ctx, criteria)
	if err != nil {
		return nil, err
	}

	// Create criteria levels if provided
	for _, levelReq := range request.Levels {
		_, err := s.CreateCriteriaLevel(ctx, criteria.ID, levelReq)
		if err != nil {
			return nil, fmt.Errorf("failed to create criteria level: %w", err)
		}
	}

	return s.GetCriteriaByID(criteria.ID)
}

func (s *service) GetCriteriaByID(id uuid.UUID) (*RubricCriteriaResponse, error) {
	criteria, err := s.repo.GetCriteriaByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToCriteriaResponse(criteria), nil
}

func (s *service) GetCriteriaByRubric(rubricID uuid.UUID) ([]RubricCriteriaResponse, error) {
	criteriaList, err := s.repo.GetCriteriaByRubric(rubricID)
	if err != nil {
		return nil, err
	}

	responses := make([]RubricCriteriaResponse, len(criteriaList))
	for i, criteria := range criteriaList {
		responses[i] = *s.modelToCriteriaResponse(&criteria)
	}
	return responses, nil
}

func (s *service) UpdateCriteria(ctx context.Context, id uuid.UUID, request UpdateRubricCriteriaRequest) (*RubricCriteriaResponse, error) {
	criteria, err := s.repo.GetCriteriaByID(id)
	if err != nil {
		return nil, err
	}

	if request.Title != "" {
		criteria.Title = request.Title
	}
	if request.Description != "" {
		criteria.Description = request.Description
	}
	if request.Weight != 0 {
		criteria.Weight = request.Weight
	}
	if request.Sequence != 0 {
		criteria.Sequence = request.Sequence
	}
	criteria.IsRequired = request.IsRequired

	err = s.repo.UpdateCriteria(ctx, criteria)
	if err != nil {
		return nil, err
	}

	return s.GetCriteriaByID(criteria.ID)
}

func (s *service) DeleteCriteria(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteCriteria(ctx, id)
}

// RubricLevel operations
func (s *service) CreateLevel(ctx context.Context, rubricID uuid.UUID, request CreateRubricLevelRequest) (*RubricLevelResponse, error) {
	level := &RubricLevel{
		ID:            uuid.New(),
		RubricID:      rubricID,
		LevelCode:     request.LevelCode,
		LevelName:     request.LevelName,
		PointValue:    request.PointValue,
		MinPercentage: request.MinPercentage,
		MaxPercentage: request.MaxPercentage,
		Sequence:      request.Sequence,
		Color:         request.Color,
	}

	if level.Sequence == 0 {
		level.Sequence = 1
	}

	err := s.repo.CreateLevel(ctx, level)
	if err != nil {
		return nil, err
	}

	return s.modelToLevelResponse(level), nil
}

func (s *service) GetLevelByID(id uuid.UUID) (*RubricLevelResponse, error) {
	level, err := s.repo.GetLevelByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToLevelResponse(level), nil
}

func (s *service) GetLevelsByRubric(rubricID uuid.UUID) ([]RubricLevelResponse, error) {
	levels, err := s.repo.GetLevelsByRubric(rubricID)
	if err != nil {
		return nil, err
	}

	responses := make([]RubricLevelResponse, len(levels))
	for i, level := range levels {
		responses[i] = *s.modelToLevelResponse(&level)
	}
	return responses, nil
}

func (s *service) UpdateLevel(ctx context.Context, id uuid.UUID, request UpdateRubricLevelRequest) (*RubricLevelResponse, error) {
	level, err := s.repo.GetLevelByID(id)
	if err != nil {
		return nil, err
	}

	if request.LevelCode != "" {
		level.LevelCode = request.LevelCode
	}
	if request.LevelName != "" {
		level.LevelName = request.LevelName
	}
	if request.PointValue != 0 {
		level.PointValue = request.PointValue
	}
	if request.MinPercentage != 0 {
		level.MinPercentage = request.MinPercentage
	}
	if request.MaxPercentage != 0 {
		level.MaxPercentage = request.MaxPercentage
	}
	if request.Sequence != 0 {
		level.Sequence = request.Sequence
	}
	if request.Color != "" {
		level.Color = request.Color
	}

	err = s.repo.UpdateLevel(ctx, level)
	if err != nil {
		return nil, err
	}

	return s.modelToLevelResponse(level), nil
}

func (s *service) DeleteLevel(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteLevel(ctx, id)
}

// RubricCriteriaLevel operations
func (s *service) CreateCriteriaLevel(ctx context.Context, criteriaID uuid.UUID, request CreateRubricCriteriaLevelRequest) (*RubricCriteriaLevelResponse, error) {
	levelID, err := uuid.Parse(request.LevelID)
	if err != nil {
		return nil, fmt.Errorf("invalid level ID: %w", err)
	}

	criteriaLevel := &RubricCriteriaLevel{
		ID:          uuid.New(),
		CriteriaID:  criteriaID,
		LevelID:     levelID,
		Description: request.Description,
		Examples:    request.Examples,
	}

	err = s.repo.CreateCriteriaLevel(ctx, criteriaLevel)
	if err != nil {
		return nil, err
	}

	return s.modelToCriteriaLevelResponse(criteriaLevel), nil
}

func (s *service) GetCriteriaLevels(criteriaID uuid.UUID) ([]RubricCriteriaLevelResponse, error) {
	criteriaLevels, err := s.repo.GetCriteriaLevels(criteriaID)
	if err != nil {
		return nil, err
	}

	responses := make([]RubricCriteriaLevelResponse, len(criteriaLevels))
	for i, criteriaLevel := range criteriaLevels {
		responses[i] = *s.modelToCriteriaLevelResponse(&criteriaLevel)
	}
	return responses, nil
}

func (s *service) UpdateCriteriaLevel(ctx context.Context, id uuid.UUID, request UpdateRubricCriteriaLevelRequest) (*RubricCriteriaLevelResponse, error) {
	criteriaLevel, err := s.repo.GetCriteriaByID(id)
	if err != nil {
		return nil, err
	}

	// Find the specific criteria level to update
	criteriaLevels, err := s.repo.GetCriteriaLevels(criteriaLevel.ID)
	if err != nil {
		return nil, err
	}

	if len(criteriaLevels) == 0 {
		return nil, fmt.Errorf("criteria level not found")
	}

	// For now, just update the first one (this would need refinement in production)
	cl := &criteriaLevels[0]

	if request.LevelID != "" {
		levelID, err := uuid.Parse(request.LevelID)
		if err != nil {
			return nil, fmt.Errorf("invalid level ID: %w", err)
		}
		cl.LevelID = levelID
	}
	if request.Description != "" {
		cl.Description = request.Description
	}
	if request.Examples != "" {
		cl.Examples = request.Examples
	}

	err = s.repo.UpdateCriteriaLevel(ctx, cl)
	if err != nil {
		return nil, err
	}

	return s.modelToCriteriaLevelResponse(cl), nil
}

func (s *service) DeleteCriteriaLevel(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteCriteriaLevel(ctx, id)
}

// Helper functions for model-to-response conversion
func (s *service) modelToRubricResponse(rubric *Rubric) *RubricResponse {
	var subjectName *string
	if rubric.Subject != nil {
		name := rubric.Subject.SubjectName
		subjectName = &name
	}

	criteriaResponses := make([]RubricCriteriaResponse, len(rubric.Criteria))
	for i, criteria := range rubric.Criteria {
		criteriaResponses[i] = *s.modelToCriteriaResponse(&criteria)
	}

	levelResponses := make([]RubricLevelResponse, len(rubric.Levels))
	for i, level := range rubric.Levels {
		levelResponses[i] = *s.modelToLevelResponse(&level)
	}

	return &RubricResponse{
		ID:                 rubric.ID,
		Title:              rubric.Title,
		Description:        rubric.Description,
		SubjectID:          rubric.SubjectID,
		SubjectName:        subjectName,
		AssessmentType:     rubric.AssessmentType,
		AssessmentTypeName: GetAssessmentTypeDescription(rubric.AssessmentType),
		GradeLevel:         rubric.GradeLevel,
		MaxScore:           rubric.MaxScore,
		IsTemplate:         rubric.IsTemplate,
		IsActive:           rubric.IsActive,
		Criteria:           criteriaResponses,
		Levels:             levelResponses,
		CreatedAt:          rubric.CreatedAt,
		UpdatedAt:          rubric.UpdatedAt,
	}
}

func (s *service) modelToCriteriaResponse(criteria *RubricCriteria) *RubricCriteriaResponse {
	levelResponses := make([]RubricCriteriaLevelResponse, len(criteria.Levels))
	for i, level := range criteria.Levels {
		levelResponses[i] = *s.modelToCriteriaLevelResponse(&level)
	}

	return &RubricCriteriaResponse{
		ID:          criteria.ID,
		RubricID:    criteria.RubricID,
		Title:       criteria.Title,
		Description: criteria.Description,
		Weight:      criteria.Weight,
		Sequence:    criteria.Sequence,
		IsRequired:  criteria.IsRequired,
		Levels:      levelResponses,
		CreatedAt:   criteria.CreatedAt,
		UpdatedAt:   criteria.UpdatedAt,
	}
}

func (s *service) modelToLevelResponse(level *RubricLevel) *RubricLevelResponse {
	return &RubricLevelResponse{
		ID:            level.ID,
		RubricID:      level.RubricID,
		LevelCode:     level.LevelCode,
		LevelName:     level.LevelName,
		PointValue:    level.PointValue,
		MinPercentage: level.MinPercentage,
		MaxPercentage: level.MaxPercentage,
		Sequence:      level.Sequence,
		Color:         level.Color,
		CreatedAt:     level.CreatedAt,
		UpdatedAt:     level.UpdatedAt,
	}
}

func (s *service) modelToCriteriaLevelResponse(criteriaLevel *RubricCriteriaLevel) *RubricCriteriaLevelResponse {
	var levelCode, levelName string
	if criteriaLevel.Level != nil {
		levelCode = criteriaLevel.Level.LevelCode
		levelName = criteriaLevel.Level.LevelName
	}

	return &RubricCriteriaLevelResponse{
		ID:          criteriaLevel.ID,
		CriteriaID:  criteriaLevel.CriteriaID,
		LevelID:     criteriaLevel.LevelID,
		LevelCode:   levelCode,
		LevelName:   levelName,
		Description: criteriaLevel.Description,
		Examples:    criteriaLevel.Examples,
		CreatedAt:   criteriaLevel.CreatedAt,
		UpdatedAt:   criteriaLevel.UpdatedAt,
	}
}
