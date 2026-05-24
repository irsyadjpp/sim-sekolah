package play_based_learning

import (
	"context"
	"errors"
	"time"

	"github.com/google/uuid"
)

type PlayBasedLearningService interface {
	// Play Activity Type CRUD
	CreatePlayActivityType(ctx context.Context, req *CreatePlayActivityTypeRequest) (*PlayActivityTypeResponse, error)
	GetPlayActivityTypeByID(ctx context.Context, id uuid.UUID) (*PlayActivityTypeResponse, error)
	GetAllPlayActivityTypes(ctx context.Context) ([]PlayActivityTypeResponse, error)
	GetActivePlayActivityTypes(ctx context.Context) ([]PlayActivityTypeResponse, error)
	GetPlayActivityTypesByPhase(ctx context.Context, phaseID uuid.UUID) ([]PlayActivityTypeResponse, error)
	GetPlayActivityTypesByDomain(ctx context.Context, domain string) ([]PlayActivityTypeResponse, error)
	UpdatePlayActivityType(ctx context.Context, id uuid.UUID, req *UpdatePlayActivityTypeRequest) (*PlayActivityTypeResponse, error)
	DeletePlayActivityType(ctx context.Context, id uuid.UUID) error

	// Play Based Activity CRUD
	CreatePlayBasedActivity(ctx context.Context, req *CreatePlayBasedActivityRequest) (*PlayBasedActivityResponse, error)
	GetPlayBasedActivityByID(ctx context.Context, id uuid.UUID) (*PlayBasedActivityDetailResponse, error)
	GetPlayBasedActivitiesByModuleID(ctx context.Context, moduleID uuid.UUID) ([]PlayBasedActivityDetailResponse, error)
	UpdatePlayBasedActivity(ctx context.Context, id uuid.UUID, req *UpdatePlayBasedActivityRequest) (*PlayBasedActivityResponse, error)
	DeletePlayBasedActivity(ctx context.Context, id uuid.UUID) error
	DeletePlayBasedActivitiesByModuleID(ctx context.Context, moduleID uuid.UUID) error
	GetPlayBasedLearningSummary(ctx context.Context, moduleID uuid.UUID) (*PlayBasedLearningSummaryResponse, error)

	// Play Observation CRUD
	CreatePlayObservation(ctx context.Context, req *CreatePlayObservationRequest) (*PlayObservationResponse, error)
	GetPlayObservationByID(ctx context.Context, id uuid.UUID) (*PlayObservationResponse, error)
	GetPlayObservationsByActivityID(ctx context.Context, activityID uuid.UUID) ([]PlayObservationResponse, error)
	GetPlayObservationsByStudentID(ctx context.Context, studentID uuid.UUID) ([]PlayObservationResponse, error)
	GetPlayObservationsByStudentAndActivity(ctx context.Context, studentID, activityID uuid.UUID) ([]PlayObservationResponse, error)
	UpdatePlayObservation(ctx context.Context, id uuid.UUID, req *UpdatePlayObservationRequest) (*PlayObservationResponse, error)
	DeletePlayObservation(ctx context.Context, id uuid.UUID) error
	GetStudentPlaySummary(ctx context.Context, studentID uuid.UUID) (*StudentPlaySummaryResponse, error)
}

type playBasedLearningService struct {
	repo PlayBasedLearningRepository
}

func NewPlayBasedLearningService(repo PlayBasedLearningRepository) PlayBasedLearningService {
	return &playBasedLearningService{repo: repo}
}

// Helper functions to convert models to response DTOs

func activityTypeToResponse(activityType *PlayActivityType) *PlayActivityTypeResponse {
	return &PlayActivityTypeResponse{
		ID:               activityType.ID,
		ActivityCode:     activityType.ActivityCode,
		ActivityName:     activityType.ActivityName,
		Description:      activityType.Description,
		LearningOutcomes: activityType.LearningOutcomes,
		MaterialsNeeded:  activityType.MaterialsNeeded,
		SuggestedAge:     activityType.SuggestedAge,
		PlayDomain:       activityType.PlayDomain,
		PhaseID:          activityType.PhaseID,
		IsActive:         activityType.IsActive,
		CreatedAt:        activityType.CreatedAt,
		UpdatedAt:        activityType.UpdatedAt,
	}
}

func playBasedActivityToResponse(activity *PlayBasedActivity) *PlayBasedActivityResponse {
	var activityTypeResp *PlayActivityTypeResponse
	if activity.ActivityType.ID != uuid.Nil {
		activityTypeResp = activityTypeToResponse(&activity.ActivityType)
	}

	return &PlayBasedActivityResponse{
		ID:                    activity.ID,
		ModuleID:              activity.ModuleID,
		ActivityTypeID:        activity.ActivityTypeID,
		ActivityName:          activity.ActivityName,
		DurationMinutes:       activity.DurationMinutes,
		SocialInteractionType: activity.SocialInteractionType,
		PhysicalActivityLevel: activity.PhysicalActivityLevel,
		LearningGoals:         activity.LearningGoals,
		Instructions:          activity.Instructions,
		SafetyConsiderations:  activity.SafetyConsiderations,
		AssessmentMethod:      activity.AssessmentMethod,
		CreatedAt:             activity.CreatedAt,
		UpdatedAt:             activity.UpdatedAt,
		ActivityType:          activityTypeResp,
	}
}

func playBasedActivityToDetailResponse(activity *PlayBasedActivity) *PlayBasedActivityDetailResponse {
	var typeName, typeCode, typeDesc string
	if activity.ActivityType.ID != uuid.Nil {
		typeName = activity.ActivityType.ActivityName
		typeCode = activity.ActivityType.ActivityCode
		typeDesc = activity.ActivityType.Description
	}

	return &PlayBasedActivityDetailResponse{
		ID:                      activity.ID,
		ModuleID:                activity.ModuleID,
		ActivityTypeID:          activity.ActivityTypeID,
		ActivityTypeName:        typeName,
		ActivityTypeCode:        typeCode,
		ActivityTypeDescription: typeDesc,
		ActivityName:            activity.ActivityName,
		DurationMinutes:         activity.DurationMinutes,
		SocialInteractionType:   activity.SocialInteractionType,
		PhysicalActivityLevel:   activity.PhysicalActivityLevel,
		LearningGoals:           activity.LearningGoals,
		Instructions:            activity.Instructions,
		SafetyConsiderations:    activity.SafetyConsiderations,
		AssessmentMethod:        activity.AssessmentMethod,
		CreatedAt:               activity.CreatedAt,
		UpdatedAt:               activity.UpdatedAt,
	}
}

func playObservationToResponse(observation *PlayObservation) *PlayObservationResponse {
	return &PlayObservationResponse{
		ID:                 observation.ID,
		ActivityID:         observation.ActivityID,
		StudentID:          observation.StudentID,
		EngagementLevel:    observation.EngagementLevel,
		SocialInteraction:  observation.SocialInteraction,
		SkillsDemonstrated: observation.SkillsDemonstrated,
		ChallengesObserved: observation.ChallengesObserved,
		TeacherNotes:       observation.TeacherNotes,
		ObservationDate:    observation.ObservationDate,
		CreatedAt:          observation.CreatedAt,
		UpdatedAt:          observation.UpdatedAt,
	}
}

// Play Activity Type CRUD

func (s *playBasedLearningService) CreatePlayActivityType(ctx context.Context, req *CreatePlayActivityTypeRequest) (*PlayActivityTypeResponse, error) {
	// Check if activity code already exists
	existing, _ := s.repo.GetPlayActivityTypeByCode(ctx, req.ActivityCode)
	if existing != nil {
		return nil, errors.New("activity code already exists")
	}

	activityType := &PlayActivityType{
		ID:               uuid.New(),
		ActivityCode:     req.ActivityCode,
		ActivityName:     req.ActivityName,
		Description:      req.Description,
		LearningOutcomes: req.LearningOutcomes,
		MaterialsNeeded:  req.MaterialsNeeded,
		SuggestedAge:     req.SuggestedAge,
		PlayDomain:       req.PlayDomain,
		PhaseID:          req.PhaseID,
		IsActive:         true,
	}

	err := s.repo.CreatePlayActivityType(ctx, activityType)
	if err != nil {
		return nil, err
	}

	return activityTypeToResponse(activityType), nil
}

func (s *playBasedLearningService) GetPlayActivityTypeByID(ctx context.Context, id uuid.UUID) (*PlayActivityTypeResponse, error) {
	activityType, err := s.repo.GetPlayActivityTypeByID(ctx, id)
	if err != nil {
		return nil, err
	}
	return activityTypeToResponse(activityType), nil
}

func (s *playBasedLearningService) GetAllPlayActivityTypes(ctx context.Context) ([]PlayActivityTypeResponse, error) {
	activityTypes, err := s.repo.GetAllPlayActivityTypes(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]PlayActivityTypeResponse, len(activityTypes))
	for i, at := range activityTypes {
		responses[i] = *activityTypeToResponse(&at)
	}
	return responses, nil
}

func (s *playBasedLearningService) GetActivePlayActivityTypes(ctx context.Context) ([]PlayActivityTypeResponse, error) {
	activityTypes, err := s.repo.GetActivePlayActivityTypes(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]PlayActivityTypeResponse, len(activityTypes))
	for i, at := range activityTypes {
		responses[i] = *activityTypeToResponse(&at)
	}
	return responses, nil
}

func (s *playBasedLearningService) GetPlayActivityTypesByPhase(ctx context.Context, phaseID uuid.UUID) ([]PlayActivityTypeResponse, error) {
	activityTypes, err := s.repo.GetPlayActivityTypesByPhase(ctx, phaseID)
	if err != nil {
		return nil, err
	}

	responses := make([]PlayActivityTypeResponse, len(activityTypes))
	for i, at := range activityTypes {
		responses[i] = *activityTypeToResponse(&at)
	}
	return responses, nil
}

func (s *playBasedLearningService) GetPlayActivityTypesByDomain(ctx context.Context, domain string) ([]PlayActivityTypeResponse, error) {
	activityTypes, err := s.repo.GetPlayActivityTypesByDomain(ctx, domain)
	if err != nil {
		return nil, err
	}

	responses := make([]PlayActivityTypeResponse, len(activityTypes))
	for i, at := range activityTypes {
		responses[i] = *activityTypeToResponse(&at)
	}
	return responses, nil
}

func (s *playBasedLearningService) UpdatePlayActivityType(ctx context.Context, id uuid.UUID, req *UpdatePlayActivityTypeRequest) (*PlayActivityTypeResponse, error) {
	activityType, err := s.repo.GetPlayActivityTypeByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.ActivityName != nil {
		activityType.ActivityName = *req.ActivityName
	}
	if req.Description != nil {
		activityType.Description = *req.Description
	}
	if req.LearningOutcomes != nil {
		activityType.LearningOutcomes = *req.LearningOutcomes
	}
	if req.MaterialsNeeded != nil {
		activityType.MaterialsNeeded = *req.MaterialsNeeded
	}
	if req.SuggestedAge != nil {
		activityType.SuggestedAge = *req.SuggestedAge
	}
	if req.PlayDomain != nil {
		activityType.PlayDomain = *req.PlayDomain
	}
	if req.PhaseID != nil {
		activityType.PhaseID = *req.PhaseID
	}
	if req.IsActive != nil {
		activityType.IsActive = *req.IsActive
	}

	err = s.repo.UpdatePlayActivityType(ctx, activityType)
	if err != nil {
		return nil, err
	}

	return activityTypeToResponse(activityType), nil
}

func (s *playBasedLearningService) DeletePlayActivityType(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeletePlayActivityType(ctx, id)
}

// Play Based Activity CRUD

func (s *playBasedLearningService) CreatePlayBasedActivity(ctx context.Context, req *CreatePlayBasedActivityRequest) (*PlayBasedActivityResponse, error) {
	// Validate social interaction type
	if !IsValidSocialInteraction(req.SocialInteractionType) {
		return nil, errors.New("invalid social interaction type")
	}

	// Validate physical activity level
	if !IsValidPhysicalActivity(req.PhysicalActivityLevel) {
		return nil, errors.New("invalid physical activity level")
	}

	// Validate activity type exists
	activityType, err := s.repo.GetPlayActivityTypeByID(ctx, req.ActivityTypeID)
	if err != nil || activityType == nil {
		return nil, errors.New("activity type not found")
	}

	activity := &PlayBasedActivity{
		ID:                    uuid.New(),
		ModuleID:              req.ModuleID,
		ActivityTypeID:        req.ActivityTypeID,
		ActivityName:          req.ActivityName,
		DurationMinutes:       req.DurationMinutes,
		SocialInteractionType: req.SocialInteractionType,
		PhysicalActivityLevel: req.PhysicalActivityLevel,
		LearningGoals:         req.LearningGoals,
		Instructions:          req.Instructions,
		SafetyConsiderations:  req.SafetyConsiderations,
		AssessmentMethod:      req.AssessmentMethod,
	}

	err = s.repo.CreatePlayBasedActivity(ctx, activity)
	if err != nil {
		return nil, err
	}

	// Reload with activity type
	activity, err = s.repo.GetPlayBasedActivityByID(ctx, activity.ID)
	if err != nil {
		return nil, err
	}

	return playBasedActivityToResponse(activity), nil
}

func (s *playBasedLearningService) GetPlayBasedActivityByID(ctx context.Context, id uuid.UUID) (*PlayBasedActivityDetailResponse, error) {
	activity, err := s.repo.GetPlayBasedActivityByID(ctx, id)
	if err != nil {
		return nil, err
	}
	return playBasedActivityToDetailResponse(activity), nil
}

func (s *playBasedLearningService) GetPlayBasedActivitiesByModuleID(ctx context.Context, moduleID uuid.UUID) ([]PlayBasedActivityDetailResponse, error) {
	activities, err := s.repo.GetPlayBasedActivitiesByModuleID(ctx, moduleID)
	if err != nil {
		return nil, err
	}

	responses := make([]PlayBasedActivityDetailResponse, len(activities))
	for i, a := range activities {
		responses[i] = *playBasedActivityToDetailResponse(&a)
	}
	return responses, nil
}

func (s *playBasedLearningService) UpdatePlayBasedActivity(ctx context.Context, id uuid.UUID, req *UpdatePlayBasedActivityRequest) (*PlayBasedActivityResponse, error) {
	activity, err := s.repo.GetPlayBasedActivityByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.ActivityTypeID != nil {
		activityUUID := uuid.MustParse(*req.ActivityTypeID)
		activity.ActivityTypeID = activityUUID
	}
	if req.ActivityName != nil {
		activity.ActivityName = *req.ActivityName
	}
	if req.DurationMinutes != nil {
		activity.DurationMinutes = *req.DurationMinutes
	}
	if req.SocialInteractionType != nil {
		if !IsValidSocialInteraction(*req.SocialInteractionType) {
			return nil, errors.New("invalid social interaction type")
		}
		activity.SocialInteractionType = *req.SocialInteractionType
	}
	if req.PhysicalActivityLevel != nil {
		if !IsValidPhysicalActivity(*req.PhysicalActivityLevel) {
			return nil, errors.New("invalid physical activity level")
		}
		activity.PhysicalActivityLevel = *req.PhysicalActivityLevel
	}
	if req.LearningGoals != nil {
		activity.LearningGoals = *req.LearningGoals
	}
	if req.Instructions != nil {
		activity.Instructions = *req.Instructions
	}
	if req.SafetyConsiderations != nil {
		activity.SafetyConsiderations = *req.SafetyConsiderations
	}
	if req.AssessmentMethod != nil {
		activity.AssessmentMethod = *req.AssessmentMethod
	}

	err = s.repo.UpdatePlayBasedActivity(ctx, activity)
	if err != nil {
		return nil, err
	}

	// Reload with activity type
	activity, err = s.repo.GetPlayBasedActivityByID(ctx, id)
	if err != nil {
		return nil, err
	}

	return playBasedActivityToResponse(activity), nil
}

func (s *playBasedLearningService) DeletePlayBasedActivity(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeletePlayBasedActivity(ctx, id)
}

func (s *playBasedLearningService) DeletePlayBasedActivitiesByModuleID(ctx context.Context, moduleID uuid.UUID) error {
	return s.repo.DeletePlayBasedActivitiesByModuleID(ctx, moduleID)
}

func (s *playBasedLearningService) GetPlayBasedLearningSummary(ctx context.Context, moduleID uuid.UUID) (*PlayBasedLearningSummaryResponse, error) {
	activities, err := s.repo.GetPlayBasedActivitiesByModuleID(ctx, moduleID)
	if err != nil {
		return nil, err
	}

	totalActivities := len(activities)
	totalDuration := 0

	// Collect unique activity types
	activityTypesMap := make(map[uuid.UUID]PlayActivityTypeResponse)
	for _, a := range activities {
		if a.ActivityType.ID != uuid.Nil {
			activityTypesMap[a.ActivityType.ID] = *activityTypeToResponse(&a.ActivityType)
		}
		totalDuration += a.DurationMinutes
	}

	activityTypes := make([]PlayActivityTypeResponse, 0, len(activityTypesMap))
	for _, at := range activityTypesMap {
		activityTypes = append(activityTypes, at)
	}

	activityResponses := make([]PlayBasedActivityResponse, len(activities))
	for i, a := range activities {
		activityResponses[i] = *playBasedActivityToResponse(&a)
	}

	return &PlayBasedLearningSummaryResponse{
		ModuleID:             moduleID,
		TotalActivities:      totalActivities,
		TotalDurationMinutes: totalDuration,
		ActivityTypes:        activityTypes,
		Activities:           activityResponses,
	}, nil
}

// Play Observation CRUD

func (s *playBasedLearningService) CreatePlayObservation(ctx context.Context, req *CreatePlayObservationRequest) (*PlayObservationResponse, error) {
	// Validate observation date format
	_, err := time.Parse("2006-01-02", req.ObservationDate)
	if err != nil {
		return nil, errors.New("invalid observation date format")
	}

	observation := &PlayObservation{
		ID:                 uuid.New(),
		ActivityID:         req.ActivityID,
		StudentID:          req.StudentID,
		EngagementLevel:    req.EngagementLevel,
		SocialInteraction:  req.SocialInteraction,
		SkillsDemonstrated: req.SkillsDemonstrated,
		ChallengesObserved: req.ChallengesObserved,
		TeacherNotes:       req.TeacherNotes,
		ObservationDate:    req.ObservationDate,
	}

	err = s.repo.CreatePlayObservation(ctx, observation)
	if err != nil {
		return nil, err
	}

	return playObservationToResponse(observation), nil
}

func (s *playBasedLearningService) GetPlayObservationByID(ctx context.Context, id uuid.UUID) (*PlayObservationResponse, error) {
	observation, err := s.repo.GetPlayObservationByID(ctx, id)
	if err != nil {
		return nil, err
	}
	return playObservationToResponse(observation), nil
}

func (s *playBasedLearningService) GetPlayObservationsByActivityID(ctx context.Context, activityID uuid.UUID) ([]PlayObservationResponse, error) {
	observations, err := s.repo.GetPlayObservationsByActivityID(ctx, activityID)
	if err != nil {
		return nil, err
	}

	responses := make([]PlayObservationResponse, len(observations))
	for i, o := range observations {
		responses[i] = *playObservationToResponse(&o)
	}
	return responses, nil
}

func (s *playBasedLearningService) GetPlayObservationsByStudentID(ctx context.Context, studentID uuid.UUID) ([]PlayObservationResponse, error) {
	observations, err := s.repo.GetPlayObservationsByStudentID(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]PlayObservationResponse, len(observations))
	for i, o := range observations {
		responses[i] = *playObservationToResponse(&o)
	}
	return responses, nil
}

func (s *playBasedLearningService) GetPlayObservationsByStudentAndActivity(ctx context.Context, studentID, activityID uuid.UUID) ([]PlayObservationResponse, error) {
	observations, err := s.repo.GetPlayObservationsByStudentAndActivity(ctx, studentID, activityID)
	if err != nil {
		return nil, err
	}

	responses := make([]PlayObservationResponse, len(observations))
	for i, o := range observations {
		responses[i] = *playObservationToResponse(&o)
	}
	return responses, nil
}

func (s *playBasedLearningService) UpdatePlayObservation(ctx context.Context, id uuid.UUID, req *UpdatePlayObservationRequest) (*PlayObservationResponse, error) {
	observation, err := s.repo.GetPlayObservationByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.EngagementLevel != nil {
		observation.EngagementLevel = *req.EngagementLevel
	}
	if req.SocialInteraction != nil {
		observation.SocialInteraction = *req.SocialInteraction
	}
	if req.SkillsDemonstrated != nil {
		observation.SkillsDemonstrated = *req.SkillsDemonstrated
	}
	if req.ChallengesObserved != nil {
		observation.ChallengesObserved = *req.ChallengesObserved
	}
	if req.TeacherNotes != nil {
		observation.TeacherNotes = *req.TeacherNotes
	}
	if req.ObservationDate != nil {
		_, err := time.Parse("2006-01-02", *req.ObservationDate)
		if err != nil {
			return nil, errors.New("invalid observation date format")
		}
		observation.ObservationDate = *req.ObservationDate
	}

	err = s.repo.UpdatePlayObservation(ctx, observation)
	if err != nil {
		return nil, err
	}

	return playObservationToResponse(observation), nil
}

func (s *playBasedLearningService) DeletePlayObservation(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeletePlayObservation(ctx, id)
}

func (s *playBasedLearningService) GetStudentPlaySummary(ctx context.Context, studentID uuid.UUID) (*StudentPlaySummaryResponse, error) {
	observations, err := s.repo.GetPlayObservationsByStudentID(ctx, studentID)
	if err != nil {
		return nil, err
	}

	totalObservations := len(observations)

	// Calculate average engagement (simplified)
	engagementCount := make(map[string]int)
	skillsByDomain := make(map[string]int)

	var recentObservations []PlayObservationResponse
	recentCount := 5
	if totalObservations < recentCount {
		recentCount = totalObservations
	}

	for i, obs := range observations {
		if obs.EngagementLevel != "" {
			engagementCount[obs.EngagementLevel]++
		}
		if i < recentCount {
			recentObservations = append(recentObservations, *playObservationToResponse(&obs))
		}
		// Skills by domain would need parsing of the JSON array
	}

	averageEngagement := ""
	if len(engagementCount) > 0 {
		// Simple logic: take the most common engagement level
		maxCount := 0
		for level, count := range engagementCount {
			if count > maxCount {
				maxCount = count
				averageEngagement = level
			}
		}
	}

	return &StudentPlaySummaryResponse{
		StudentID:          studentID,
		TotalObservations:  totalObservations,
		AverageEngagement:  averageEngagement,
		RecentObservations: recentObservations,
		SkillsByDomain:     skillsByDomain,
	}, nil
}
