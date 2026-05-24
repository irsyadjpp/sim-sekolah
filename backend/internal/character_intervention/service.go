package character_intervention

import (
	"context"
	"errors"
	"time"

	"github.com/google/uuid"
)

type CharacterInterventionService interface {
	// CharacterIntervention
	GetAll(ctx context.Context) ([]CharacterInterventionResponse, error)
	GetByID(ctx context.Context, id string) (*CharacterInterventionResponse, error)
	GetByDimension(ctx context.Context, dimension string) ([]CharacterInterventionResponse, error)
	GetByAgeGroup(ctx context.Context, ageGroup string) ([]CharacterInterventionResponse, error)
	GetActive(ctx context.Context) ([]CharacterInterventionResponse, error)
	Create(ctx context.Context, req CreateCharacterInterventionRequest) (*CharacterInterventionResponse, error)
	Update(ctx context.Context, id string, req UpdateCharacterInterventionRequest) (*CharacterInterventionResponse, error)
	Delete(ctx context.Context, id string) error

	// StudentCharacterIntervention
	GetAllStudentInterventions(ctx context.Context) ([]StudentInterventionResponse, error)
	GetStudentInterventionByID(ctx context.Context, id string) (*StudentInterventionResponse, error)
	GetStudentInterventionsByStudent(ctx context.Context, studentID string) ([]StudentInterventionResponse, error)
	GetStudentInterventionsByTeacher(ctx context.Context, teacherID string) ([]StudentInterventionResponse, error)
	GetActiveStudentInterventions(ctx context.Context) ([]StudentInterventionResponse, error)
	GetStudentInterventionsByStatus(ctx context.Context, status string) ([]StudentInterventionResponse, error)
	CreateStudentIntervention(ctx context.Context, req CreateStudentInterventionRequest) (*StudentInterventionResponse, error)
	UpdateStudentIntervention(ctx context.Context, id string, req UpdateStudentInterventionRequest) (*StudentInterventionResponse, error)
	DeleteStudentIntervention(ctx context.Context, id string) error

	// CharacterInterventionProgress
	GetAllProgress(ctx context.Context) ([]InterventionProgressResponse, error)
	GetProgressByID(ctx context.Context, id string) (*InterventionProgressResponse, error)
	GetProgressByAssignment(ctx context.Context, assignmentID string) ([]InterventionProgressResponse, error)
	GetProgressByObserver(ctx context.Context, observerID string) ([]InterventionProgressResponse, error)
	CreateProgress(ctx context.Context, req CreateInterventionProgressRequest) (*InterventionProgressResponse, error)
	UpdateProgress(ctx context.Context, id string, req UpdateInterventionProgressRequest) (*InterventionProgressResponse, error)
	DeleteProgress(ctx context.Context, id string) error

	// InterventionRecommendation
	GetAllRecommendations(ctx context.Context) ([]InterventionRecommendationResponse, error)
	GetRecommendationByID(ctx context.Context, id string) (*InterventionRecommendationResponse, error)
	GetRecommendationsByStudent(ctx context.Context, studentID string) ([]InterventionRecommendationResponse, error)
	GetPendingRecommendations(ctx context.Context) ([]InterventionRecommendationResponse, error)
	CreateRecommendation(ctx context.Context, req CreateInterventionRecommendationRequest) (*InterventionRecommendationResponse, error)
	UpdateRecommendation(ctx context.Context, id string, req UpdateInterventionRecommendationRequest) (*InterventionRecommendationResponse, error)
	DeleteRecommendation(ctx context.Context, id string) error

	// CharacterMilestone
	GetAllMilestones(ctx context.Context) ([]CharacterMilestoneResponse, error)
	GetMilestoneByID(ctx context.Context, id string) (*CharacterMilestoneResponse, error)
	GetMilestonesByStudent(ctx context.Context, studentID string) ([]CharacterMilestoneResponse, error)
	GetMilestonesByDimension(ctx context.Context, dimension string) ([]CharacterMilestoneResponse, error)
	GetMilestonesByObserver(ctx context.Context, observerID string) ([]CharacterMilestoneResponse, error)
	CreateMilestone(ctx context.Context, req CreateCharacterMilestoneRequest) (*CharacterMilestoneResponse, error)
	UpdateMilestone(ctx context.Context, id string, req UpdateCharacterMilestoneRequest) (*CharacterMilestoneResponse, error)
	DeleteMilestone(ctx context.Context, id string) error

	// Summary
	GetInterventionSummary(ctx context.Context) (*InterventionSummaryResponse, error)
}

type characterInterventionService struct {
	repo CharacterInterventionRepository
}

func NewCharacterInterventionService(repo CharacterInterventionRepository) CharacterInterventionService {
	return &characterInterventionService{repo: repo}
}

// CharacterIntervention Methods
func (s *characterInterventionService) GetAll(ctx context.Context) ([]CharacterInterventionResponse, error) {
	interventions, err := s.repo.GetAll(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]CharacterInterventionResponse, len(interventions))
	for i, intervention := range interventions {
		responses[i] = *s.interventionToResponse(&intervention)
	}
	return responses, nil
}

func (s *characterInterventionService) GetByID(ctx context.Context, id string) (*CharacterInterventionResponse, error) {
	intervention, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("intervention tidak ditemukan")
	}
	return s.interventionToResponse(intervention), nil
}

func (s *characterInterventionService) GetByDimension(ctx context.Context, dimension string) ([]CharacterInterventionResponse, error) {
	interventions, err := s.repo.GetByDimension(ctx, dimension)
	if err != nil {
		return nil, err
	}

	responses := make([]CharacterInterventionResponse, len(interventions))
	for i, intervention := range interventions {
		responses[i] = *s.interventionToResponse(&intervention)
	}
	return responses, nil
}

func (s *characterInterventionService) GetByAgeGroup(ctx context.Context, ageGroup string) ([]CharacterInterventionResponse, error) {
	interventions, err := s.repo.GetByAgeGroup(ctx, ageGroup)
	if err != nil {
		return nil, err
	}

	responses := make([]CharacterInterventionResponse, len(interventions))
	for i, intervention := range interventions {
		responses[i] = *s.interventionToResponse(&intervention)
	}
	return responses, nil
}

func (s *characterInterventionService) GetActive(ctx context.Context) ([]CharacterInterventionResponse, error) {
	interventions, err := s.repo.GetActive(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]CharacterInterventionResponse, len(interventions))
	for i, intervention := range interventions {
		responses[i] = *s.interventionToResponse(&intervention)
	}
	return responses, nil
}

func (s *characterInterventionService) Create(ctx context.Context, req CreateCharacterInterventionRequest) (*CharacterInterventionResponse, error) {
	intervention := &CharacterIntervention{
		ID:                 uuid.New(),
		InterventionName:   req.InterventionName,
		CharacterDimension: req.CharacterDimension,
		TargetAgeGroup:     req.TargetAgeGroup,
		InterventionType:   req.InterventionType,
		Description:        req.Description,
		Strategies:         req.Strategies,
		Resources:          req.Resources,
		DurationWeeks:      req.DurationWeeks,
		SuccessCriteria:    req.SuccessCriteria,
		IsActive:           true,
	}

	if req.IsActive != nil {
		intervention.IsActive = *req.IsActive
	}

	if intervention.DurationWeeks == 0 {
		intervention.DurationWeeks = 4
	}

	if err := s.repo.Create(ctx, intervention); err != nil {
		return nil, err
	}
	return s.interventionToResponse(intervention), nil
}

func (s *characterInterventionService) Update(ctx context.Context, id string, req UpdateCharacterInterventionRequest) (*CharacterInterventionResponse, error) {
	intervention, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("intervention tidak ditemukan")
	}

	if req.InterventionName != "" {
		intervention.InterventionName = req.InterventionName
	}
	if req.CharacterDimension != "" {
		intervention.CharacterDimension = req.CharacterDimension
	}
	if req.TargetAgeGroup != "" {
		intervention.TargetAgeGroup = req.TargetAgeGroup
	}
	if req.InterventionType != "" {
		intervention.InterventionType = req.InterventionType
	}
	if req.Description != "" {
		intervention.Description = req.Description
	}
	if req.Strategies != nil {
		intervention.Strategies = req.Strategies
	}
	if req.Resources != nil {
		intervention.Resources = req.Resources
	}
	if req.DurationWeeks > 0 {
		intervention.DurationWeeks = req.DurationWeeks
	}
	if req.SuccessCriteria != nil {
		intervention.SuccessCriteria = req.SuccessCriteria
	}
	if req.IsActive != nil {
		intervention.IsActive = *req.IsActive
	}

	if err := s.repo.Update(ctx, intervention); err != nil {
		return nil, err
	}
	return s.interventionToResponse(intervention), nil
}

func (s *characterInterventionService) Delete(ctx context.Context, id string) error {
	_, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("intervention tidak ditemukan")
	}
	return s.repo.Delete(ctx, id)
}

// StudentCharacterIntervention Methods
func (s *characterInterventionService) GetAllStudentInterventions(ctx context.Context) ([]StudentInterventionResponse, error) {
	assignments, err := s.repo.GetAllStudentInterventions(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]StudentInterventionResponse, len(assignments))
	for i, assignment := range assignments {
		responses[i] = *s.studentInterventionToResponse(&assignment)
	}
	return responses, nil
}

func (s *characterInterventionService) GetStudentInterventionByID(ctx context.Context, id string) (*StudentInterventionResponse, error) {
	assignment, err := s.repo.GetStudentInterventionByID(ctx, id)
	if err != nil {
		return nil, errors.New("student intervention tidak ditemukan")
	}
	return s.studentInterventionToResponse(assignment), nil
}

func (s *characterInterventionService) GetStudentInterventionsByStudent(ctx context.Context, studentID string) ([]StudentInterventionResponse, error) {
	assignments, err := s.repo.GetStudentInterventionsByStudent(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]StudentInterventionResponse, len(assignments))
	for i, assignment := range assignments {
		responses[i] = *s.studentInterventionToResponse(&assignment)
	}
	return responses, nil
}

func (s *characterInterventionService) GetStudentInterventionsByTeacher(ctx context.Context, teacherID string) ([]StudentInterventionResponse, error) {
	assignments, err := s.repo.GetStudentInterventionsByTeacher(ctx, teacherID)
	if err != nil {
		return nil, err
	}

	responses := make([]StudentInterventionResponse, len(assignments))
	for i, assignment := range assignments {
		responses[i] = *s.studentInterventionToResponse(&assignment)
	}
	return responses, nil
}

func (s *characterInterventionService) GetActiveStudentInterventions(ctx context.Context) ([]StudentInterventionResponse, error) {
	assignments, err := s.repo.GetActiveStudentInterventions(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]StudentInterventionResponse, len(assignments))
	for i, assignment := range assignments {
		responses[i] = *s.studentInterventionToResponse(&assignment)
	}
	return responses, nil
}

func (s *characterInterventionService) GetStudentInterventionsByStatus(ctx context.Context, status string) ([]StudentInterventionResponse, error) {
	assignments, err := s.repo.GetStudentInterventionsByStatus(ctx, status)
	if err != nil {
		return nil, err
	}

	responses := make([]StudentInterventionResponse, len(assignments))
	for i, assignment := range assignments {
		responses[i] = *s.studentInterventionToResponse(&assignment)
	}
	return responses, nil
}

func (s *characterInterventionService) CreateStudentIntervention(ctx context.Context, req CreateStudentInterventionRequest) (*StudentInterventionResponse, error) {
	studentUUID, err := uuid.Parse(req.StudentID)
	if err != nil {
		return nil, errors.New("invalid student ID format")
	}

	interventionUUID, err := uuid.Parse(req.InterventionID)
	if err != nil {
		return nil, errors.New("invalid intervention ID format")
	}

	teacherUUID, err := uuid.Parse(req.TeacherID)
	if err != nil {
		return nil, errors.New("invalid teacher ID format")
	}

	targetStartDate, err := time.Parse(time.RFC3339, req.TargetStartDate)
	if err != nil {
		return nil, errors.New("invalid target start date format")
	}

	targetEndDate, err := time.Parse(time.RFC3339, req.TargetEndDate)
	if err != nil {
		return nil, errors.New("invalid target end date format")
	}

	assignment := &StudentCharacterIntervention{
		ID:                   uuid.New(),
		StudentID:            studentUUID,
		InterventionID:       interventionUUID,
		TeacherID:            teacherUUID,
		AssignmentDate:       time.Now(),
		TargetStartDate:      targetStartDate,
		TargetEndDate:        targetEndDate,
		CurrentStatus:        req.CurrentStatus,
		PriorityLevel:        req.PriorityLevel,
		BaselineAssessment:   req.BaselineAssessment,
		CustomizedStrategies: req.CustomizedStrategies,
		Notes:                req.Notes,
	}

	if assignment.CurrentStatus == "" {
		assignment.CurrentStatus = AssignmentStatusActive
	}

	if assignment.PriorityLevel == "" {
		assignment.PriorityLevel = PriorityLevelMedium
	}

	if err := s.repo.CreateStudentIntervention(ctx, assignment); err != nil {
		return nil, err
	}
	return s.studentInterventionToResponse(assignment), nil
}

func (s *characterInterventionService) UpdateStudentIntervention(ctx context.Context, id string, req UpdateStudentInterventionRequest) (*StudentInterventionResponse, error) {
	assignment, err := s.repo.GetStudentInterventionByID(ctx, id)
	if err != nil {
		return nil, errors.New("student intervention tidak ditemukan")
	}

	if req.TargetStartDate != "" {
		targetStartDate, err := time.Parse(time.RFC3339, req.TargetStartDate)
		if err != nil {
			return nil, errors.New("invalid target start date format")
		}
		assignment.TargetStartDate = targetStartDate
	}

	if req.TargetEndDate != "" {
		targetEndDate, err := time.Parse(time.RFC3339, req.TargetEndDate)
		if err != nil {
			return nil, errors.New("invalid target end date format")
		}
		assignment.TargetEndDate = targetEndDate
	}

	if req.CurrentStatus != "" {
		assignment.CurrentStatus = req.CurrentStatus
	}
	if req.PriorityLevel != "" {
		assignment.PriorityLevel = req.PriorityLevel
	}
	if req.BaselineAssessment != "" {
		assignment.BaselineAssessment = req.BaselineAssessment
	}
	if req.CustomizedStrategies != nil {
		assignment.CustomizedStrategies = req.CustomizedStrategies
	}
	if req.Notes != "" {
		assignment.Notes = req.Notes
	}

	if err := s.repo.UpdateStudentIntervention(ctx, assignment); err != nil {
		return nil, err
	}
	return s.studentInterventionToResponse(assignment), nil
}

func (s *characterInterventionService) DeleteStudentIntervention(ctx context.Context, id string) error {
	_, err := s.repo.GetStudentInterventionByID(ctx, id)
	if err != nil {
		return errors.New("student intervention tidak ditemukan")
	}
	return s.repo.DeleteStudentIntervention(ctx, id)
}

// CharacterInterventionProgress Methods
func (s *characterInterventionService) GetAllProgress(ctx context.Context) ([]InterventionProgressResponse, error) {
	progress, err := s.repo.GetAllProgress(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]InterventionProgressResponse, len(progress))
	for i, p := range progress {
		responses[i] = *s.progressToResponse(&p)
	}
	return responses, nil
}

func (s *characterInterventionService) GetProgressByID(ctx context.Context, id string) (*InterventionProgressResponse, error) {
	p, err := s.repo.GetProgressByID(ctx, id)
	if err != nil {
		return nil, errors.New("progress tidak ditemukan")
	}
	return s.progressToResponse(p), nil
}

func (s *characterInterventionService) GetProgressByAssignment(ctx context.Context, assignmentID string) ([]InterventionProgressResponse, error) {
	progress, err := s.repo.GetProgressByAssignment(ctx, assignmentID)
	if err != nil {
		return nil, err
	}

	responses := make([]InterventionProgressResponse, len(progress))
	for i, p := range progress {
		responses[i] = *s.progressToResponse(&p)
	}
	return responses, nil
}

func (s *characterInterventionService) GetProgressByObserver(ctx context.Context, observerID string) ([]InterventionProgressResponse, error) {
	progress, err := s.repo.GetProgressByObserver(ctx, observerID)
	if err != nil {
		return nil, err
	}

	responses := make([]InterventionProgressResponse, len(progress))
	for i, p := range progress {
		responses[i] = *s.progressToResponse(&p)
	}
	return responses, nil
}

func (s *characterInterventionService) CreateProgress(ctx context.Context, req CreateInterventionProgressRequest) (*InterventionProgressResponse, error) {
	observerUUID, err := uuid.Parse(req.ObserverID)
	if err != nil {
		return nil, errors.New("invalid observer ID format")
	}

	progress := &CharacterInterventionProgress{
		ID:                   uuid.New(),
		AssignmentID:         req.AssignmentID,
		ObserverID:           observerUUID,
		ObservationDate:      time.Now(),
		ProgressRating:       req.ProgressRating,
		BehavioralIndicators: req.BehavioralIndicators,
		SpecificAchievements: req.SpecificAchievements,
		Challenges:           req.Challenges,
		SupportProvided:      req.SupportProvided,
		NextSteps:            req.NextSteps,
		Notes:                req.Notes,
	}

	if err := s.repo.CreateProgress(ctx, progress); err != nil {
		return nil, err
	}
	return s.progressToResponse(progress), nil
}

func (s *characterInterventionService) UpdateProgress(ctx context.Context, id string, req UpdateInterventionProgressRequest) (*InterventionProgressResponse, error) {
	progress, err := s.repo.GetProgressByID(ctx, id)
	if err != nil {
		return nil, errors.New("progress tidak ditemukan")
	}

	if req.ProgressRating != "" {
		progress.ProgressRating = req.ProgressRating
	}
	if req.BehavioralIndicators != nil {
		progress.BehavioralIndicators = req.BehavioralIndicators
	}
	if req.SpecificAchievements != nil {
		progress.SpecificAchievements = req.SpecificAchievements
	}
	if req.Challenges != nil {
		progress.Challenges = req.Challenges
	}
	if req.SupportProvided != "" {
		progress.SupportProvided = req.SupportProvided
	}
	if req.NextSteps != nil {
		progress.NextSteps = req.NextSteps
	}
	if req.Notes != "" {
		progress.Notes = req.Notes
	}

	if err := s.repo.UpdateProgress(ctx, progress); err != nil {
		return nil, err
	}
	return s.progressToResponse(progress), nil
}

func (s *characterInterventionService) DeleteProgress(ctx context.Context, id string) error {
	_, err := s.repo.GetProgressByID(ctx, id)
	if err != nil {
		return errors.New("progress tidak ditemukan")
	}
	return s.repo.DeleteProgress(ctx, id)
}

// InterventionRecommendation Methods
func (s *characterInterventionService) GetAllRecommendations(ctx context.Context) ([]InterventionRecommendationResponse, error) {
	recommendations, err := s.repo.GetAllRecommendations(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]InterventionRecommendationResponse, len(recommendations))
	for i, rec := range recommendations {
		responses[i] = *s.recommendationToResponse(&rec)
	}
	return responses, nil
}

func (s *characterInterventionService) GetRecommendationByID(ctx context.Context, id string) (*InterventionRecommendationResponse, error) {
	rec, err := s.repo.GetRecommendationByID(ctx, id)
	if err != nil {
		return nil, errors.New("recommendation tidak ditemukan")
	}
	return s.recommendationToResponse(rec), nil
}

func (s *characterInterventionService) GetRecommendationsByStudent(ctx context.Context, studentID string) ([]InterventionRecommendationResponse, error) {
	recommendations, err := s.repo.GetRecommendationsByStudent(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]InterventionRecommendationResponse, len(recommendations))
	for i, rec := range recommendations {
		responses[i] = *s.recommendationToResponse(&rec)
	}
	return responses, nil
}

func (s *characterInterventionService) GetPendingRecommendations(ctx context.Context) ([]InterventionRecommendationResponse, error) {
	recommendations, err := s.repo.GetPendingRecommendations(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]InterventionRecommendationResponse, len(recommendations))
	for i, rec := range recommendations {
		responses[i] = *s.recommendationToResponse(&rec)
	}
	return responses, nil
}

func (s *characterInterventionService) CreateRecommendation(ctx context.Context, req CreateInterventionRecommendationRequest) (*InterventionRecommendationResponse, error) {
	studentUUID, err := uuid.Parse(req.StudentID)
	if err != nil {
		return nil, errors.New("invalid student ID format")
	}

	var p5AssessmentUUID *uuid.UUID
	if req.P5AssessmentID != nil && *req.P5AssessmentID != "" {
		parsed, err := uuid.Parse(*req.P5AssessmentID)
		if err != nil {
			return nil, errors.New("invalid P5 assessment ID format")
		}
		p5AssessmentUUID = &parsed
	}

	interventionUUIDs := make([]uuid.UUID, len(req.RecommendedInterventions))
	for i, id := range req.RecommendedInterventions {
		parsed, err := uuid.Parse(id)
		if err != nil {
			return nil, errors.New("invalid intervention ID format")
		}
		interventionUUIDs[i] = parsed
	}

	recommendation := &InterventionRecommendation{
		ID:                          uuid.New(),
		StudentID:                   studentUUID,
		P5AssessmentID:              p5AssessmentUUID,
		RecommendedInterventions:    interventionUUIDs,
		RecommendationDate:          time.Now(),
		RecommendationSource:        req.RecommendationSource,
		ConfidenceScore:             req.ConfidenceScore,
		Rationale:                   req.Rationale,
		PriorityRanking:             req.PriorityRanking,
		ImplementationTimelineWeeks: req.ImplementationTimelineWeeks,
		AdditionalNotes:             req.AdditionalNotes,
	}

	if recommendation.ImplementationTimelineWeeks == 0 {
		recommendation.ImplementationTimelineWeeks = 4
	}

	if err := s.repo.CreateRecommendation(ctx, recommendation); err != nil {
		return nil, err
	}
	return s.recommendationToResponse(recommendation), nil
}

func (s *characterInterventionService) UpdateRecommendation(ctx context.Context, id string, req UpdateInterventionRecommendationRequest) (*InterventionRecommendationResponse, error) {
	recommendation, err := s.repo.GetRecommendationByID(ctx, id)
	if err != nil {
		return nil, errors.New("recommendation tidak ditemukan")
	}

	if req.IsAccepted != nil {
		recommendation.IsAccepted = req.IsAccepted
		if *req.IsAccepted && req.AcceptedBy != nil {
			acceptedByUUID, err := uuid.Parse(*req.AcceptedBy)
			if err != nil {
				return nil, errors.New("invalid accepted by ID format")
			}
			recommendation.AcceptedBy = &acceptedByUUID
			now := time.Now()
			recommendation.AcceptedDate = &now
		}
	}

	if err := s.repo.UpdateRecommendation(ctx, recommendation); err != nil {
		return nil, err
	}
	return s.recommendationToResponse(recommendation), nil
}

func (s *characterInterventionService) DeleteRecommendation(ctx context.Context, id string) error {
	_, err := s.repo.GetRecommendationByID(ctx, id)
	if err != nil {
		return errors.New("recommendation tidak ditemukan")
	}
	return s.repo.DeleteRecommendation(ctx, id)
}

// CharacterMilestone Methods
func (s *characterInterventionService) GetAllMilestones(ctx context.Context) ([]CharacterMilestoneResponse, error) {
	milestones, err := s.repo.GetAllMilestones(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]CharacterMilestoneResponse, len(milestones))
	for i, milestone := range milestones {
		responses[i] = *s.milestoneToResponse(&milestone)
	}
	return responses, nil
}

func (s *characterInterventionService) GetMilestoneByID(ctx context.Context, id string) (*CharacterMilestoneResponse, error) {
	milestone, err := s.repo.GetMilestoneByID(ctx, id)
	if err != nil {
		return nil, errors.New("milestone tidak ditemukan")
	}
	return s.milestoneToResponse(milestone), nil
}

func (s *characterInterventionService) GetMilestonesByStudent(ctx context.Context, studentID string) ([]CharacterMilestoneResponse, error) {
	milestones, err := s.repo.GetMilestonesByStudent(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]CharacterMilestoneResponse, len(milestones))
	for i, milestone := range milestones {
		responses[i] = *s.milestoneToResponse(&milestone)
	}
	return responses, nil
}

func (s *characterInterventionService) GetMilestonesByDimension(ctx context.Context, dimension string) ([]CharacterMilestoneResponse, error) {
	milestones, err := s.repo.GetMilestonesByDimension(ctx, dimension)
	if err != nil {
		return nil, err
	}

	responses := make([]CharacterMilestoneResponse, len(milestones))
	for i, milestone := range milestones {
		responses[i] = *s.milestoneToResponse(&milestone)
	}
	return responses, nil
}

func (s *characterInterventionService) GetMilestonesByObserver(ctx context.Context, observerID string) ([]CharacterMilestoneResponse, error) {
	milestones, err := s.repo.GetMilestonesByObserver(ctx, observerID)
	if err != nil {
		return nil, err
	}

	responses := make([]CharacterMilestoneResponse, len(milestones))
	for i, milestone := range milestones {
		responses[i] = *s.milestoneToResponse(&milestone)
	}
	return responses, nil
}

func (s *characterInterventionService) CreateMilestone(ctx context.Context, req CreateCharacterMilestoneRequest) (*CharacterMilestoneResponse, error) {
	studentUUID, err := uuid.Parse(req.StudentID)
	if err != nil {
		return nil, errors.New("invalid student ID format")
	}

	observerUUID, err := uuid.Parse(req.ObserverID)
	if err != nil {
		return nil, errors.New("invalid observer ID format")
	}

	milestone := &CharacterMilestone{
		ID:                   uuid.New(),
		StudentID:            studentUUID,
		CharacterDimension:   req.CharacterDimension,
		MilestoneDescription: req.MilestoneDescription,
		MilestoneDate:        time.Now(),
		AchievementLevel:     req.AchievementLevel,
		Evidence:             req.Evidence,
		ObserverID:           observerUUID,
		CelebrationMethod:    req.CelebrationMethod,
		Notes:                req.Notes,
	}

	if err := s.repo.CreateMilestone(ctx, milestone); err != nil {
		return nil, err
	}
	return s.milestoneToResponse(milestone), nil
}

func (s *characterInterventionService) UpdateMilestone(ctx context.Context, id string, req UpdateCharacterMilestoneRequest) (*CharacterMilestoneResponse, error) {
	milestone, err := s.repo.GetMilestoneByID(ctx, id)
	if err != nil {
		return nil, errors.New("milestone tidak ditemukan")
	}

	if req.MilestoneDescription != "" {
		milestone.MilestoneDescription = req.MilestoneDescription
	}
	if req.AchievementLevel != "" {
		milestone.AchievementLevel = req.AchievementLevel
	}
	if req.Evidence != nil {
		milestone.Evidence = req.Evidence
	}
	if req.CelebrationMethod != "" {
		milestone.CelebrationMethod = req.CelebrationMethod
	}
	if req.Notes != "" {
		milestone.Notes = req.Notes
	}

	if err := s.repo.UpdateMilestone(ctx, milestone); err != nil {
		return nil, err
	}
	return s.milestoneToResponse(milestone), nil
}

func (s *characterInterventionService) DeleteMilestone(ctx context.Context, id string) error {
	_, err := s.repo.GetMilestoneByID(ctx, id)
	if err != nil {
		return errors.New("milestone tidak ditemukan")
	}
	return s.repo.DeleteMilestone(ctx, id)
}

// Summary Method
func (s *characterInterventionService) GetInterventionSummary(ctx context.Context) (*InterventionSummaryResponse, error) {
	return s.repo.GetInterventionSummary(ctx)
}

// Helper methods for converting models to responses
func (s *characterInterventionService) interventionToResponse(intervention *CharacterIntervention) *CharacterInterventionResponse {
	var createdBy *string
	if intervention.CreatedBy != nil {
		id := intervention.CreatedBy.String()
		createdBy = &id
	}

	var updatedBy *string
	if intervention.UpdatedBy != nil {
		id := intervention.UpdatedBy.String()
		updatedBy = &id
	}

	return &CharacterInterventionResponse{
		ID:                 intervention.ID.String(),
		InterventionName:   intervention.InterventionName,
		CharacterDimension: intervention.CharacterDimension,
		TargetAgeGroup:     intervention.TargetAgeGroup,
		InterventionType:   intervention.InterventionType,
		Description:        intervention.Description,
		Strategies:         intervention.Strategies,
		Resources:          intervention.Resources,
		DurationWeeks:      intervention.DurationWeeks,
		SuccessCriteria:    intervention.SuccessCriteria,
		IsActive:           intervention.IsActive,
		CreatedAt:          intervention.CreatedAt,
		UpdatedAt:          intervention.UpdatedAt,
		CreatedBy:          createdBy,
		UpdatedBy:          updatedBy,
	}
}

func (s *characterInterventionService) studentInterventionToResponse(assignment *StudentCharacterIntervention) *StudentInterventionResponse {
	return &StudentInterventionResponse{
		ID:                   assignment.ID.String(),
		StudentID:            assignment.StudentID.String(),
		InterventionID:       assignment.InterventionID.String(),
		TeacherID:            assignment.TeacherID.String(),
		AssignmentDate:       assignment.AssignmentDate,
		TargetStartDate:      assignment.TargetStartDate,
		TargetEndDate:        assignment.TargetEndDate,
		CurrentStatus:        assignment.CurrentStatus,
		PriorityLevel:        assignment.PriorityLevel,
		BaselineAssessment:   assignment.BaselineAssessment,
		CustomizedStrategies: assignment.CustomizedStrategies,
		Notes:                assignment.Notes,
		CreatedAt:            assignment.CreatedAt,
		UpdatedAt:            assignment.UpdatedAt,
	}
}

func (s *characterInterventionService) progressToResponse(progress *CharacterInterventionProgress) *InterventionProgressResponse {
	return &InterventionProgressResponse{
		ID:                   progress.ID.String(),
		AssignmentID:         progress.AssignmentID.String(),
		ObservationDate:      progress.ObservationDate,
		ObserverID:           progress.ObserverID.String(),
		ProgressRating:       progress.ProgressRating,
		BehavioralIndicators: progress.BehavioralIndicators,
		SpecificAchievements: progress.SpecificAchievements,
		Challenges:           progress.Challenges,
		SupportProvided:      progress.SupportProvided,
		NextSteps:            progress.NextSteps,
		Notes:                progress.Notes,
		CreatedAt:            progress.CreatedAt,
		UpdatedAt:            progress.UpdatedAt,
	}
}

func (s *characterInterventionService) recommendationToResponse(rec *InterventionRecommendation) *InterventionRecommendationResponse {
	var p5AssessmentID *string
	if rec.P5AssessmentID != nil {
		id := rec.P5AssessmentID.String()
		p5AssessmentID = &id
	}

	var acceptedBy *string
	if rec.AcceptedBy != nil {
		id := rec.AcceptedBy.String()
		acceptedBy = &id
	}

	interventionIDs := make([]string, len(rec.RecommendedInterventions))
	for i, id := range rec.RecommendedInterventions {
		interventionIDs[i] = id.String()
	}

	return &InterventionRecommendationResponse{
		ID:                          rec.ID.String(),
		StudentID:                   rec.StudentID.String(),
		P5AssessmentID:              p5AssessmentID,
		RecommendedInterventions:    interventionIDs,
		RecommendationDate:          rec.RecommendationDate,
		RecommendationSource:        rec.RecommendationSource,
		ConfidenceScore:             rec.ConfidenceScore,
		Rationale:                   rec.Rationale,
		PriorityRanking:             rec.PriorityRanking,
		ImplementationTimelineWeeks: rec.ImplementationTimelineWeeks,
		AdditionalNotes:             rec.AdditionalNotes,
		IsAccepted:                  rec.IsAccepted,
		AcceptedBy:                  acceptedBy,
		AcceptedDate:                rec.AcceptedDate,
		CreatedAt:                   rec.CreatedAt,
		UpdatedAt:                   rec.UpdatedAt,
	}
}

func (s *characterInterventionService) milestoneToResponse(milestone *CharacterMilestone) *CharacterMilestoneResponse {
	return &CharacterMilestoneResponse{
		ID:                   milestone.ID.String(),
		StudentID:            milestone.StudentID.String(),
		CharacterDimension:   milestone.CharacterDimension,
		MilestoneDescription: milestone.MilestoneDescription,
		MilestoneDate:        milestone.MilestoneDate,
		AchievementLevel:     milestone.AchievementLevel,
		Evidence:             milestone.Evidence,
		ObserverID:           milestone.ObserverID.String(),
		CelebrationMethod:    milestone.CelebrationMethod,
		Notes:                milestone.Notes,
		CreatedAt:            milestone.CreatedAt,
		UpdatedAt:            milestone.UpdatedAt,
	}
}
