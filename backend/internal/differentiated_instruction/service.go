package differentiated_instruction

import (
	"context"
	"errors"
	"time"

	"github.com/google/uuid"
)

type DIService interface {
	// DI Strategy CRUD
	CreateDIStrategy(ctx context.Context, req *CreateDIStrategyRequest) (*DIStrategyResponse, error)
	GetDIStrategyByID(ctx context.Context, id uuid.UUID) (*DIStrategyResponse, error)
	GetAllDIStrategies(ctx context.Context) ([]DIStrategyResponse, error)
	GetActiveDIStrategies(ctx context.Context) ([]DIStrategyResponse, error)
	GetDIStrategiesByTargetGroup(ctx context.Context, targetGroup string) ([]DIStrategyResponse, error)
	UpdateDIStrategy(ctx context.Context, id uuid.UUID, req *UpdateDIStrategyRequest) (*DIStrategyResponse, error)
	DeleteDIStrategy(ctx context.Context, id uuid.UUID) error

	// Module Differentiation CRUD
	CreateModuleDifferentiation(ctx context.Context, req *CreateModuleDifferentiationRequest) (*ModuleDifferentiationResponse, error)
	GetModuleDifferentiationByID(ctx context.Context, id uuid.UUID) (*ModuleDifferentiationDetailResponse, error)
	GetDifferentiationsByModuleID(ctx context.Context, moduleID uuid.UUID) ([]ModuleDifferentiationDetailResponse, error)
	GetDifferentiationsByStudentID(ctx context.Context, studentID uuid.UUID) ([]ModuleDifferentiationDetailResponse, error)
	UpdateModuleDifferentiation(ctx context.Context, id uuid.UUID, req *UpdateModuleDifferentiationRequest) (*ModuleDifferentiationResponse, error)
	DeleteModuleDifferentiation(ctx context.Context, id uuid.UUID) error
	DeleteDifferentiationsByModuleID(ctx context.Context, moduleID uuid.UUID) error
	GetModuleDISummary(ctx context.Context, moduleID uuid.UUID) (*ModuleDISummaryResponse, error)

	// Student DI Need CRUD
	CreateStudentDINeed(ctx context.Context, req *CreateStudentDINeedRequest) (*StudentDINeedResponse, error)
	GetStudentDINeedByID(ctx context.Context, id uuid.UUID) (*StudentDINeedResponse, error)
	GetDINeedsByStudentID(ctx context.Context, studentID uuid.UUID) ([]StudentDINeedResponse, error)
	GetActiveDINeedsByStudentID(ctx context.Context, studentID uuid.UUID) ([]StudentDINeedResponse, error)
	GetDINeedsByStudentAndSubject(ctx context.Context, studentID, subjectID uuid.UUID) ([]StudentDINeedResponse, error)
	UpdateStudentDINeed(ctx context.Context, id uuid.UUID, req *UpdateStudentDINeedRequest) (*StudentDINeedResponse, error)
	DeleteStudentDINeed(ctx context.Context, id uuid.UUID) error
	GetStudentDINeedSummary(ctx context.Context, studentID uuid.UUID) (*StudentDINeedSummaryResponse, error)
}

type diService struct {
	repo DIRepository
}

func NewDIService(repo DIRepository) DIService {
	return &diService{repo: repo}
}

// Helper functions to convert models to response DTOs

func strategyToResponse(strategy *DIStrategy) *DIStrategyResponse {
	return &DIStrategyResponse{
		ID:            strategy.ID,
		StrategyCode:  strategy.StrategyCode,
		StrategyName:  strategy.StrategyName,
		Description:   strategy.Description,
		Applicability: strategy.Applicability,
		Examples:      strategy.Examples,
		TargetGroup:   strategy.TargetGroup,
		IsActive:      strategy.IsActive,
		CreatedAt:     strategy.CreatedAt,
		UpdatedAt:     strategy.UpdatedAt,
	}
}

func moduleDifferentiationToResponse(diff *ModuleDifferentiation) *ModuleDifferentiationResponse {
	var strategyResp *DIStrategyResponse
	if diff.Strategy.ID != uuid.Nil {
		strategyResp = strategyToResponse(&diff.Strategy)
	}

	return &ModuleDifferentiationResponse{
		ID:             diff.ID,
		ModuleID:       diff.ModuleID,
		StrategyID:     diff.StrategyID,
		TargetStudents: diff.TargetStudents,
		Modifications:  diff.Modifications,
		Resources:      diff.Resources,
		AssessmentType: diff.AssessmentType,
		Notes:          diff.Notes,
		CreatedAt:      diff.CreatedAt,
		UpdatedAt:      diff.UpdatedAt,
		Strategy:       strategyResp,
	}
}

func moduleDifferentiationToDetailResponse(diff *ModuleDifferentiation) *ModuleDifferentiationDetailResponse {
	var strategyName, strategyCode, strategyDesc string
	if diff.Strategy.ID != uuid.Nil {
		strategyName = diff.Strategy.StrategyName
		strategyCode = diff.Strategy.StrategyCode
		strategyDesc = diff.Strategy.Description
	}

	return &ModuleDifferentiationDetailResponse{
		ID:                  diff.ID,
		ModuleID:            diff.ModuleID,
		StrategyID:          diff.StrategyID,
		StrategyName:        strategyName,
		StrategyCode:        strategyCode,
		StrategyDescription: strategyDesc,
		TargetStudents:      diff.TargetStudents,
		Modifications:       diff.Modifications,
		Resources:           diff.Resources,
		AssessmentType:      diff.AssessmentType,
		Notes:               diff.Notes,
		CreatedAt:           diff.CreatedAt,
		UpdatedAt:           diff.UpdatedAt,
	}
}

func studentDINeedToResponse(need *StudentDINeed) *StudentDINeedResponse {
	return &StudentDINeedResponse{
		ID:                    need.ID,
		StudentID:             need.StudentID,
		SubjectID:             need.SubjectID,
		NeedType:              need.NeedType,
		Severity:              need.Severity,
		Description:           need.Description,
		RecommendedStrategies: need.RecommendedStrategies,
		AssessmentDate:        need.AssessmentDate,
		IsActive:              need.IsActive,
		CreatedAt:             need.CreatedAt,
		UpdatedAt:             need.UpdatedAt,
	}
}

// DI Strategy CRUD

func (s *diService) CreateDIStrategy(ctx context.Context, req *CreateDIStrategyRequest) (*DIStrategyResponse, error) {
	// Check if strategy code already exists
	existing, _ := s.repo.GetDIStrategyByCode(ctx, req.StrategyCode)
	if existing != nil {
		return nil, errors.New("strategy code already exists")
	}

	strategy := &DIStrategy{
		ID:            uuid.New(),
		StrategyCode:  req.StrategyCode,
		StrategyName:  req.StrategyName,
		Description:   req.Description,
		Applicability: req.Applicability,
		Examples:      req.Examples,
		TargetGroup:   req.TargetGroup,
		IsActive:      true,
	}

	err := s.repo.CreateDIStrategy(ctx, strategy)
	if err != nil {
		return nil, err
	}

	return strategyToResponse(strategy), nil
}

func (s *diService) GetDIStrategyByID(ctx context.Context, id uuid.UUID) (*DIStrategyResponse, error) {
	strategy, err := s.repo.GetDIStrategyByID(ctx, id)
	if err != nil {
		return nil, err
	}
	return strategyToResponse(strategy), nil
}

func (s *diService) GetAllDIStrategies(ctx context.Context) ([]DIStrategyResponse, error) {
	strategies, err := s.repo.GetAllDIStrategies(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]DIStrategyResponse, len(strategies))
	for i, s := range strategies {
		responses[i] = *strategyToResponse(&s)
	}
	return responses, nil
}

func (s *diService) GetActiveDIStrategies(ctx context.Context) ([]DIStrategyResponse, error) {
	strategies, err := s.repo.GetActiveDIStrategies(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]DIStrategyResponse, len(strategies))
	for i, s := range strategies {
		responses[i] = *strategyToResponse(&s)
	}
	return responses, nil
}

func (s *diService) GetDIStrategiesByTargetGroup(ctx context.Context, targetGroup string) ([]DIStrategyResponse, error) {
	strategies, err := s.repo.GetDIStrategiesByTargetGroup(ctx, targetGroup)
	if err != nil {
		return nil, err
	}

	responses := make([]DIStrategyResponse, len(strategies))
	for i, s := range strategies {
		responses[i] = *strategyToResponse(&s)
	}
	return responses, nil
}

func (s *diService) UpdateDIStrategy(ctx context.Context, id uuid.UUID, req *UpdateDIStrategyRequest) (*DIStrategyResponse, error) {
	strategy, err := s.repo.GetDIStrategyByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.StrategyName != nil {
		strategy.StrategyName = *req.StrategyName
	}
	if req.Description != nil {
		strategy.Description = *req.Description
	}
	if req.Applicability != nil {
		strategy.Applicability = *req.Applicability
	}
	if req.Examples != nil {
		strategy.Examples = *req.Examples
	}
	if req.TargetGroup != nil {
		strategy.TargetGroup = *req.TargetGroup
	}
	if req.IsActive != nil {
		strategy.IsActive = *req.IsActive
	}

	err = s.repo.UpdateDIStrategy(ctx, strategy)
	if err != nil {
		return nil, err
	}

	return strategyToResponse(strategy), nil
}

func (s *diService) DeleteDIStrategy(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteDIStrategy(ctx, id)
}

// Module Differentiation CRUD

func (s *diService) CreateModuleDifferentiation(ctx context.Context, req *CreateModuleDifferentiationRequest) (*ModuleDifferentiationResponse, error) {
	// Validate strategy exists
	strategy, err := s.repo.GetDIStrategyByID(ctx, req.StrategyID)
	if err != nil || strategy == nil {
		return nil, errors.New("strategy not found")
	}

	differentiation := &ModuleDifferentiation{
		ID:             uuid.New(),
		ModuleID:       req.ModuleID,
		StrategyID:     req.StrategyID,
		TargetStudents: req.TargetStudents,
		Modifications:  req.Modifications,
		Resources:      req.Resources,
		AssessmentType: req.AssessmentType,
		Notes:          req.Notes,
	}

	err = s.repo.CreateModuleDifferentiation(ctx, differentiation)
	if err != nil {
		return nil, err
	}

	// Reload with strategy
	differentiation, err = s.repo.GetModuleDifferentiationByID(ctx, differentiation.ID)
	if err != nil {
		return nil, err
	}

	return moduleDifferentiationToResponse(differentiation), nil
}

func (s *diService) GetModuleDifferentiationByID(ctx context.Context, id uuid.UUID) (*ModuleDifferentiationDetailResponse, error) {
	differentiation, err := s.repo.GetModuleDifferentiationByID(ctx, id)
	if err != nil {
		return nil, err
	}
	return moduleDifferentiationToDetailResponse(differentiation), nil
}

func (s *diService) GetDifferentiationsByModuleID(ctx context.Context, moduleID uuid.UUID) ([]ModuleDifferentiationDetailResponse, error) {
	differentiations, err := s.repo.GetDifferentiationsByModuleID(ctx, moduleID)
	if err != nil {
		return nil, err
	}

	responses := make([]ModuleDifferentiationDetailResponse, len(differentiations))
	for i, d := range differentiations {
		responses[i] = *moduleDifferentiationToDetailResponse(&d)
	}
	return responses, nil
}

func (s *diService) GetDifferentiationsByStudentID(ctx context.Context, studentID uuid.UUID) ([]ModuleDifferentiationDetailResponse, error) {
	differentiations, err := s.repo.GetDifferentiationsByStudentID(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]ModuleDifferentiationDetailResponse, len(differentiations))
	for i, d := range differentiations {
		responses[i] = *moduleDifferentiationToDetailResponse(&d)
	}
	return responses, nil
}

func (s *diService) UpdateModuleDifferentiation(ctx context.Context, id uuid.UUID, req *UpdateModuleDifferentiationRequest) (*ModuleDifferentiationResponse, error) {
	differentiation, err := s.repo.GetModuleDifferentiationByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.StrategyID != nil {
		strategyUUID := uuid.MustParse(*req.StrategyID)
		differentiation.StrategyID = strategyUUID
	}
	if req.TargetStudents != nil {
		differentiation.TargetStudents = *req.TargetStudents
	}
	if req.Modifications != nil {
		differentiation.Modifications = *req.Modifications
	}
	if req.Resources != nil {
		differentiation.Resources = *req.Resources
	}
	if req.AssessmentType != nil {
		differentiation.AssessmentType = *req.AssessmentType
	}
	if req.Notes != nil {
		differentiation.Notes = *req.Notes
	}

	err = s.repo.UpdateModuleDifferentiation(ctx, differentiation)
	if err != nil {
		return nil, err
	}

	// Reload with strategy
	differentiation, err = s.repo.GetModuleDifferentiationByID(ctx, id)
	if err != nil {
		return nil, err
	}

	return moduleDifferentiationToResponse(differentiation), nil
}

func (s *diService) DeleteModuleDifferentiation(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteModuleDifferentiation(ctx, id)
}

func (s *diService) DeleteDifferentiationsByModuleID(ctx context.Context, moduleID uuid.UUID) error {
	return s.repo.DeleteDifferentiationsByModuleID(ctx, moduleID)
}

func (s *diService) GetModuleDISummary(ctx context.Context, moduleID uuid.UUID) (*ModuleDISummaryResponse, error) {
	differentiations, err := s.repo.GetDifferentiationsByModuleID(ctx, moduleID)
	if err != nil {
		return nil, err
	}

	// Collect unique strategies
	strategiesMap := make(map[uuid.UUID]DIStrategyResponse)
	for _, d := range differentiations {
		if d.Strategy.ID != uuid.Nil {
			strategiesMap[d.Strategy.ID] = *strategyToResponse(&d.Strategy)
		}
	}

	strategies := make([]DIStrategyResponse, 0, len(strategiesMap))
	for _, s := range strategiesMap {
		strategies = append(strategies, s)
	}

	diffResponses := make([]ModuleDifferentiationResponse, len(differentiations))
	for i, d := range differentiations {
		diffResponses[i] = *moduleDifferentiationToResponse(&d)
	}

	return &ModuleDISummaryResponse{
		ModuleID:              moduleID,
		TotalDifferentiations: len(differentiations),
		StrategiesUsed:        strategies,
		StudentsCovered:       0, // Would need to parse JSON array to count
		Differentiations:      diffResponses,
	}, nil
}

// Student DI Need CRUD

func (s *diService) CreateStudentDINeed(ctx context.Context, req *CreateStudentDINeedRequest) (*StudentDINeedResponse, error) {
	assessmentDate, err := time.Parse("2006-01-02", req.AssessmentDate)
	if err != nil {
		return nil, errors.New("invalid assessment date format")
	}

	need := &StudentDINeed{
		ID:                    uuid.New(),
		StudentID:             req.StudentID,
		SubjectID:             req.SubjectID,
		NeedType:              req.NeedType,
		Severity:              req.Severity,
		Description:           req.Description,
		RecommendedStrategies: req.RecommendedStrategies,
		AssessmentDate:        assessmentDate,
		IsActive:              true,
	}

	err = s.repo.CreateStudentDINeed(ctx, need)
	if err != nil {
		return nil, err
	}

	return studentDINeedToResponse(need), nil
}

func (s *diService) GetStudentDINeedByID(ctx context.Context, id uuid.UUID) (*StudentDINeedResponse, error) {
	need, err := s.repo.GetStudentDINeedByID(ctx, id)
	if err != nil {
		return nil, err
	}
	return studentDINeedToResponse(need), nil
}

func (s *diService) GetDINeedsByStudentID(ctx context.Context, studentID uuid.UUID) ([]StudentDINeedResponse, error) {
	needs, err := s.repo.GetDINeedsByStudentID(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]StudentDINeedResponse, len(needs))
	for i, n := range needs {
		responses[i] = *studentDINeedToResponse(&n)
	}
	return responses, nil
}

func (s *diService) GetActiveDINeedsByStudentID(ctx context.Context, studentID uuid.UUID) ([]StudentDINeedResponse, error) {
	needs, err := s.repo.GetActiveDINeedsByStudentID(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]StudentDINeedResponse, len(needs))
	for i, n := range needs {
		responses[i] = *studentDINeedToResponse(&n)
	}
	return responses, nil
}

func (s *diService) GetDINeedsByStudentAndSubject(ctx context.Context, studentID, subjectID uuid.UUID) ([]StudentDINeedResponse, error) {
	needs, err := s.repo.GetDINeedsByStudentAndSubject(ctx, studentID, subjectID)
	if err != nil {
		return nil, err
	}

	responses := make([]StudentDINeedResponse, len(needs))
	for i, n := range needs {
		responses[i] = *studentDINeedToResponse(&n)
	}
	return responses, nil
}

func (s *diService) UpdateStudentDINeed(ctx context.Context, id uuid.UUID, req *UpdateStudentDINeedRequest) (*StudentDINeedResponse, error) {
	need, err := s.repo.GetStudentDINeedByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.SubjectID != nil {
		need.SubjectID = *req.SubjectID
	}
	if req.NeedType != nil {
		need.NeedType = *req.NeedType
	}
	if req.Severity != nil {
		need.Severity = *req.Severity
	}
	if req.Description != nil {
		need.Description = *req.Description
	}
	if req.RecommendedStrategies != nil {
		need.RecommendedStrategies = *req.RecommendedStrategies
	}
	if req.IsActive != nil {
		need.IsActive = *req.IsActive
	}

	err = s.repo.UpdateStudentDINeed(ctx, need)
	if err != nil {
		return nil, err
	}

	return studentDINeedToResponse(need), nil
}

func (s *diService) DeleteStudentDINeed(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteStudentDINeed(ctx, id)
}

func (s *diService) GetStudentDINeedSummary(ctx context.Context, studentID uuid.UUID) (*StudentDINeedSummaryResponse, error) {
	needs, err := s.repo.GetDINeedsByStudentID(ctx, studentID)
	if err != nil {
		return nil, err
	}

	totalNeeds := len(needs)
	activeNeeds := 0
	needsByType := make(map[string]int)
	needsBySeverity := make(map[string]int)

	var recentNeeds []StudentDINeedResponse
	recentCount := 5
	if totalNeeds < recentCount {
		recentCount = totalNeeds
	}

	for i, need := range needs {
		if need.IsActive {
			activeNeeds++
		}
		needsByType[need.NeedType]++
		needsBySeverity[need.Severity]++
		if i < recentCount {
			recentNeeds = append(recentNeeds, *studentDINeedToResponse(&need))
		}
	}

	return &StudentDINeedSummaryResponse{
		StudentID:       studentID,
		TotalNeeds:      totalNeeds,
		ActiveNeeds:     activeNeeds,
		NeedsByType:     needsByType,
		NeedsBySeverity: needsBySeverity,
		RecentNeeds:     recentNeeds,
	}, nil
}
