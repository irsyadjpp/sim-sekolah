package play_based_learning

import (
	"time"

	"github.com/google/uuid"
)

// PlayActivityType Request/Response DTOs

// CreatePlayActivityTypeRequest DTO for creating play activity type
type CreatePlayActivityTypeRequest struct {
	ActivityCode     string    `json:"activity_code" binding:"required"`
	ActivityName     string    `json:"activity_name" binding:"required"`
	Description      string    `json:"description" binding:"required"`
	LearningOutcomes string    `json:"learning_outcomes"`
	MaterialsNeeded  string    `json:"materials_needed"`
	SuggestedAge     string    `json:"suggested_age"`
	PlayDomain       string    `json:"play_domain"`
	PhaseID          uuid.UUID `json:"phase_id"`
}

// UpdatePlayActivityTypeRequest DTO for updating play activity type
type UpdatePlayActivityTypeRequest struct {
	ActivityName     *string    `json:"activity_name"`
	Description      *string    `json:"description"`
	LearningOutcomes *string    `json:"learning_outcomes"`
	MaterialsNeeded  *string    `json:"materials_needed"`
	SuggestedAge     *string    `json:"suggested_age"`
	PlayDomain       *string    `json:"play_domain"`
	PhaseID          *uuid.UUID `json:"phase_id"`
	IsActive         *bool      `json:"is_active"`
}

// PlayActivityTypeResponse DTO for play activity type response
type PlayActivityTypeResponse struct {
	ID               uuid.UUID `json:"id"`
	ActivityCode     string    `json:"activity_code"`
	ActivityName     string    `json:"activity_name"`
	Description      string    `json:"description"`
	LearningOutcomes string    `json:"learning_outcomes"`
	MaterialsNeeded  string    `json:"materials_needed"`
	SuggestedAge     string    `json:"suggested_age"`
	PlayDomain       string    `json:"play_domain"`
	PhaseID          uuid.UUID `json:"phase_id"`
	IsActive         bool      `json:"is_active"`
	CreatedAt        time.Time `json:"created_at"`
	UpdatedAt        time.Time `json:"updated_at"`
}

// PlayBasedActivity Request/Response DTOs

// CreatePlayBasedActivityRequest DTO for creating play-based activity
type CreatePlayBasedActivityRequest struct {
	ModuleID              uuid.UUID `json:"module_id" binding:"required"`
	ActivityTypeID        uuid.UUID `json:"activity_type_id" binding:"required"`
	ActivityName          string    `json:"activity_name" binding:"required"`
	DurationMinutes       int       `json:"duration_minutes"`
	SocialInteractionType string    `json:"social_interaction_type" binding:"required"`
	PhysicalActivityLevel string    `json:"physical_activity_level" binding:"required"`
	LearningGoals         string    `json:"learning_goals"`
	Instructions          string    `json:"instructions"`
	SafetyConsiderations  string    `json:"safety_considerations"`
	AssessmentMethod      string    `json:"assessment_method"`
}

// UpdatePlayBasedActivityRequest DTO for updating play-based activity
type UpdatePlayBasedActivityRequest struct {
	ActivityTypeID        *string `json:"activity_type_id"`
	ActivityName          *string `json:"activity_name"`
	DurationMinutes       *int    `json:"duration_minutes"`
	SocialInteractionType *string `json:"social_interaction_type"`
	PhysicalActivityLevel *string `json:"physical_activity_level"`
	LearningGoals         *string `json:"learning_goals"`
	Instructions          *string `json:"instructions"`
	SafetyConsiderations  *string `json:"safety_considerations"`
	AssessmentMethod      *string `json:"assessment_method"`
}

// PlayBasedActivityResponse DTO for play-based activity response
type PlayBasedActivityResponse struct {
	ID                    uuid.UUID                 `json:"id"`
	ModuleID              uuid.UUID                 `json:"module_id"`
	ActivityTypeID        uuid.UUID                 `json:"activity_type_id"`
	ActivityName          string                    `json:"activity_name"`
	DurationMinutes       int                       `json:"duration_minutes"`
	SocialInteractionType string                    `json:"social_interaction_type"`
	PhysicalActivityLevel string                    `json:"physical_activity_level"`
	LearningGoals         string                    `json:"learning_goals"`
	Instructions          string                    `json:"instructions"`
	SafetyConsiderations  string                    `json:"safety_considerations"`
	AssessmentMethod      string                    `json:"assessment_method"`
	CreatedAt             time.Time                 `json:"created_at"`
	UpdatedAt             time.Time                 `json:"updated_at"`
	ActivityType          *PlayActivityTypeResponse `json:"activity_type,omitempty"`
}

// PlayBasedActivityDetailResponse extended response with activity type details
type PlayBasedActivityDetailResponse struct {
	ID                      uuid.UUID `json:"id"`
	ModuleID                uuid.UUID `json:"module_id"`
	ActivityTypeID          uuid.UUID `json:"activity_type_id"`
	ActivityTypeName        string    `json:"activity_type_name,omitempty"`
	ActivityTypeCode        string    `json:"activity_type_code,omitempty"`
	ActivityTypeDescription string    `json:"activity_type_description,omitempty"`
	ActivityName            string    `json:"activity_name"`
	DurationMinutes         int       `json:"duration_minutes"`
	SocialInteractionType   string    `json:"social_interaction_type"`
	PhysicalActivityLevel   string    `json:"physical_activity_level"`
	LearningGoals           string    `json:"learning_goals"`
	Instructions            string    `json:"instructions"`
	SafetyConsiderations    string    `json:"safety_considerations"`
	AssessmentMethod        string    `json:"assessment_method"`
	CreatedAt               time.Time `json:"created_at"`
	UpdatedAt               time.Time `json:"updated_at"`
}

// PlayObservation Request/Response DTOs

// CreatePlayObservationRequest DTO for creating play observation
type CreatePlayObservationRequest struct {
	ActivityID         uuid.UUID `json:"activity_id" binding:"required"`
	StudentID          uuid.UUID `json:"student_id" binding:"required"`
	EngagementLevel    string    `json:"engagement_level"`
	SocialInteraction  string    `json:"social_interaction"`
	SkillsDemonstrated string    `json:"skills_demonstrated"`
	ChallengesObserved string    `json:"challenges_observed"`
	TeacherNotes       string    `json:"teacher_notes"`
	ObservationDate    string    `json:"observation_date" binding:"required"`
}

// UpdatePlayObservationRequest DTO for updating play observation
type UpdatePlayObservationRequest struct {
	EngagementLevel    *string `json:"engagement_level"`
	SocialInteraction  *string `json:"social_interaction"`
	SkillsDemonstrated *string `json:"skills_demonstrated"`
	ChallengesObserved *string `json:"challenges_observed"`
	TeacherNotes       *string `json:"teacher_notes"`
	ObservationDate    *string `json:"observation_date"`
}

// PlayObservationResponse DTO for play observation response
type PlayObservationResponse struct {
	ID                 uuid.UUID `json:"id"`
	ActivityID         uuid.UUID `json:"activity_id"`
	StudentID          uuid.UUID `json:"student_id"`
	EngagementLevel    string    `json:"engagement_level"`
	SocialInteraction  string    `json:"social_interaction"`
	SkillsDemonstrated string    `json:"skills_demonstrated"`
	ChallengesObserved string    `json:"challenges_observed"`
	TeacherNotes       string    `json:"teacher_notes"`
	ObservationDate    string    `json:"observation_date"`
	CreatedAt          time.Time `json:"created_at"`
	UpdatedAt          time.Time `json:"updated_at"`
}

// PlayBasedLearningSummaryResponse for module overview
type PlayBasedLearningSummaryResponse struct {
	ModuleID             uuid.UUID                   `json:"module_id"`
	TotalActivities      int                         `json:"total_activities"`
	TotalDurationMinutes int                         `json:"total_duration_minutes"`
	ActivityTypes        []PlayActivityTypeResponse  `json:"activity_types,omitempty"`
	Activities           []PlayBasedActivityResponse `json:"activities,omitempty"`
}

// StudentPlaySummaryResponse for student play-based learning overview
type StudentPlaySummaryResponse struct {
	StudentID          uuid.UUID                 `json:"student_id"`
	TotalObservations  int                       `json:"total_observations"`
	AverageEngagement  string                    `json:"average_engagement,omitempty"`
	RecentObservations []PlayObservationResponse `json:"recent_observations,omitempty"`
	SkillsByDomain     map[string]int            `json:"skills_by_domain,omitempty"`
}
