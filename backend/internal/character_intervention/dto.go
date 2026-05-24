package character_intervention

import (
	"time"

	"github.com/google/uuid"
)

// CharacterIntervention DTOs

type CreateCharacterInterventionRequest struct {
	InterventionName   string   `json:"intervention_name" binding:"required"`
	CharacterDimension string   `json:"character_dimension" binding:"required,oneof=BERAKHLAK BERKEBHINEASAN BERNILAI_SANTUN MANDIRI BERTANGGUNG_JAWAB GOTONG_ROYONG"`
	TargetAgeGroup     string   `json:"target_age_group" binding:"omitempty,oneof=FASE_A FASE_B FASE_C"`
	InterventionType   string   `json:"intervention_type" binding:"required,oneof=POSITIVE_REINFORCEMENT BEHAVIOR_MODIFICATION MENTORING GROUP_ACTIVITY COUNSELING"`
	Description        string   `json:"description" binding:"required"`
	Strategies         []string `json:"strategies"`
	Resources          []string `json:"resources"`
	DurationWeeks      int      `json:"duration_weeks" binding:"omitempty,min=1,max=52"`
	SuccessCriteria    []string `json:"success_criteria"`
	IsActive           *bool    `json:"is_active"`
}

type UpdateCharacterInterventionRequest struct {
	InterventionName   string   `json:"intervention_name" binding:"omitempty"`
	CharacterDimension string   `json:"character_dimension" binding:"omitempty,oneof=BERAKHLAK BERKEBHINEASAN BERNILAI_SANTUN MANDIRI BERTANGGUNG_JAWAB GOTONG_ROYONG"`
	TargetAgeGroup     string   `json:"target_age_group" binding:"omitempty,oneof=FASE_A FASE_B FASE_C"`
	InterventionType   string   `json:"intervention_type" binding:"omitempty,oneof=POSITIVE_REINFORCEMENT BEHAVIOR_MODIFICATION MENTORING GROUP_ACTIVITY COUNSELING"`
	Description        string   `json:"description" binding:"omitempty"`
	Strategies         []string `json:"strategies"`
	Resources          []string `json:"resources"`
	DurationWeeks      int      `json:"duration_weeks" binding:"omitempty,min=1,max=52"`
	SuccessCriteria    []string `json:"success_criteria"`
	IsActive           *bool    `json:"is_active"`
}

type CharacterInterventionResponse struct {
	ID                 string    `json:"id"`
	InterventionName   string    `json:"intervention_name"`
	CharacterDimension string    `json:"character_dimension"`
	TargetAgeGroup     string    `json:"target_age_group"`
	InterventionType   string    `json:"intervention_type"`
	Description        string    `json:"description"`
	Strategies         []string  `json:"strategies"`
	Resources          []string  `json:"resources"`
	DurationWeeks      int       `json:"duration_weeks"`
	SuccessCriteria    []string  `json:"success_criteria"`
	IsActive           bool      `json:"is_active"`
	CreatedAt          time.Time `json:"created_at"`
	UpdatedAt          time.Time `json:"updated_at"`
	CreatedBy          *string   `json:"created_by,omitempty"`
	UpdatedBy          *string   `json:"updated_by,omitempty"`
}

// StudentCharacterIntervention DTOs

type CreateStudentInterventionRequest struct {
	StudentID            string   `json:"student_id" binding:"required"`
	InterventionID       string   `json:"intervention_id" binding:"required"`
	TeacherID            string   `json:"teacher_id" binding:"required"`
	TargetStartDate      string   `json:"target_start_date" binding:"required"` // RFC3339 format
	TargetEndDate        string   `json:"target_end_date" binding:"required"`   // RFC3339 format
	CurrentStatus        string   `json:"current_status" binding:"omitempty,oneof=PLANNED ACTIVE PAUSED COMPLETED CANCELLED"`
	PriorityLevel        string   `json:"priority_level" binding:"omitempty,oneof=LOW MEDIUM HIGH URGENT"`
	BaselineAssessment   string   `json:"baseline_assessment"`
	CustomizedStrategies []string `json:"customized_strategies"`
	Notes                string   `json:"notes"`
}

type UpdateStudentInterventionRequest struct {
	TargetStartDate      string   `json:"target_start_date"` // RFC3339 format
	TargetEndDate        string   `json:"target_end_date"`   // RFC3339 format
	CurrentStatus        string   `json:"current_status" binding:"omitempty,oneof=PLANNED ACTIVE PAUSED COMPLETED CANCELLED"`
	PriorityLevel        string   `json:"priority_level" binding:"omitempty,oneof=LOW MEDIUM HIGH URGENT"`
	BaselineAssessment   string   `json:"baseline_assessment"`
	CustomizedStrategies []string `json:"customized_strategies"`
	Notes                string   `json:"notes"`
}

type StudentInterventionResponse struct {
	ID                   string    `json:"id"`
	StudentID            string    `json:"student_id"`
	InterventionID       string    `json:"intervention_id"`
	TeacherID            string    `json:"teacher_id"`
	AssignmentDate       time.Time `json:"assignment_date"`
	TargetStartDate      time.Time `json:"target_start_date"`
	TargetEndDate        time.Time `json:"target_end_date"`
	CurrentStatus        string    `json:"current_status"`
	PriorityLevel        string    `json:"priority_level"`
	BaselineAssessment   string    `json:"baseline_assessment"`
	CustomizedStrategies []string  `json:"customized_strategies"`
	Notes                string    `json:"notes"`
	CreatedAt            time.Time `json:"created_at"`
	UpdatedAt            time.Time `json:"updated_at"`
}

// CharacterInterventionProgress DTOs

type CreateInterventionProgressRequest struct {
	AssignmentID         uuid.UUID `json:"assignment_id" binding:"required"`
	ObserverID           string    `json:"observer_id" binding:"required"`
	ProgressRating       string    `json:"progress_rating" binding:"omitempty,oneof=NO_PROGRESS MINIMAL MODERATE SIGNIFICANT EXCELLENT"`
	BehavioralIndicators []string  `json:"behavioral_indicators"`
	SpecificAchievements []string  `json:"specific_achievements"`
	Challenges           []string  `json:"challenges"`
	SupportProvided      string    `json:"support_provided"`
	NextSteps            []string  `json:"next_steps"`
	Notes                string    `json:"notes"`
}

type UpdateInterventionProgressRequest struct {
	ProgressRating       string   `json:"progress_rating" binding:"omitempty,oneof=NO_PROGRESS MINIMAL MODERATE SIGNIFICANT EXCELLENT"`
	BehavioralIndicators []string `json:"behavioral_indicators"`
	SpecificAchievements []string `json:"specific_achievements"`
	Challenges           []string `json:"challenges"`
	SupportProvided      string   `json:"support_provided"`
	NextSteps            []string `json:"next_steps"`
	Notes                string   `json:"notes"`
}

type InterventionProgressResponse struct {
	ID                   string    `json:"id"`
	AssignmentID         string    `json:"assignment_id"`
	ObservationDate      time.Time `json:"observation_date"`
	ObserverID           string    `json:"observer_id"`
	ProgressRating       string    `json:"progress_rating"`
	BehavioralIndicators []string  `json:"behavioral_indicators"`
	SpecificAchievements []string  `json:"specific_achievements"`
	Challenges           []string  `json:"challenges"`
	SupportProvided      string    `json:"support_provided"`
	NextSteps            []string  `json:"next_steps"`
	Notes                string    `json:"notes"`
	CreatedAt            time.Time `json:"created_at"`
	UpdatedAt            time.Time `json:"updated_at"`
}

// InterventionRecommendation DTOs

type CreateInterventionRecommendationRequest struct {
	StudentID                   string   `json:"student_id" binding:"required"`
	P5AssessmentID              *string  `json:"p5_assessment_id"`
	RecommendedInterventions    []string `json:"recommended_interventions" binding:"required"`
	RecommendationSource        string   `json:"recommendation_source" binding:"required,oneof=P5_ASSESSMENT TEACHER_OBSERVATION PARENT_FEEDBACK PEER_FEEDBACK"`
	ConfidenceScore             *float64 `json:"confidence_score" binding:"omitempty,min=0,max=1"`
	Rationale                   string   `json:"rationale"`
	PriorityRanking             []int    `json:"priority_ranking"`
	ImplementationTimelineWeeks int      `json:"implementation_timeline_weeks" binding:"omitempty,min=1,max=52"`
	AdditionalNotes             string   `json:"additional_notes"`
}

type UpdateInterventionRecommendationRequest struct {
	IsAccepted *bool   `json:"is_accepted"`
	AcceptedBy *string `json:"accepted_by"`
}

type InterventionRecommendationResponse struct {
	ID                          string     `json:"id"`
	StudentID                   string     `json:"student_id"`
	P5AssessmentID              *string    `json:"p5_assessment_id"`
	RecommendedInterventions    []string   `json:"recommended_interventions"`
	RecommendationDate          time.Time  `json:"recommendation_date"`
	RecommendationSource        string     `json:"recommendation_source"`
	ConfidenceScore             *float64   `json:"confidence_score"`
	Rationale                   string     `json:"rationale"`
	PriorityRanking             []int      `json:"priority_ranking"`
	ImplementationTimelineWeeks int        `json:"implementation_timeline_weeks"`
	AdditionalNotes             string     `json:"additional_notes"`
	IsAccepted                  *bool      `json:"is_accepted"`
	AcceptedBy                  *string    `json:"accepted_by"`
	AcceptedDate                *time.Time `json:"accepted_date"`
	CreatedAt                   time.Time  `json:"created_at"`
	UpdatedAt                   time.Time  `json:"updated_at"`
}

// CharacterMilestone DTOs

type CreateCharacterMilestoneRequest struct {
	StudentID            string   `json:"student_id" binding:"required"`
	CharacterDimension   string   `json:"character_dimension" binding:"required,oneof=BERAKHLAK BERKEBHINEASAN BERNILAI_SANTUN MANDIRI BERTANGGUNG_JAWAB GOTONG_ROYONG"`
	MilestoneDescription string   `json:"milestone_description" binding:"required"`
	AchievementLevel     string   `json:"achievement_level" binding:"required,oneof=EMERGING DEVELOPING PROFICIENT EXEMPLARY"`
	Evidence             []string `json:"evidence"`
	ObserverID           string   `json:"observer_id" binding:"required"`
	CelebrationMethod    string   `json:"celebration_method" binding:"omitempty,oneof=VERBAL_PRAISE CERTIFICATE CLASS_RECOGNITION PARENT_NOTIFICATION"`
	Notes                string   `json:"notes"`
}

type UpdateCharacterMilestoneRequest struct {
	MilestoneDescription string   `json:"milestone_description" binding:"omitempty"`
	AchievementLevel     string   `json:"achievement_level" binding:"omitempty,oneof=EMERGING DEVELOPING PROFICIENT EXEMPLARY"`
	Evidence             []string `json:"evidence"`
	CelebrationMethod    string   `json:"celebration_method" binding:"omitempty,oneof=VERBAL_PRAISE CERTIFICATE CLASS_RECOGNITION PARENT_NOTIFICATION"`
	Notes                string   `json:"notes"`
}

type CharacterMilestoneResponse struct {
	ID                   string    `json:"id"`
	StudentID            string    `json:"student_id"`
	CharacterDimension   string    `json:"character_dimension"`
	MilestoneDescription string    `json:"milestone_description"`
	MilestoneDate        time.Time `json:"milestone_date"`
	AchievementLevel     string    `json:"achievement_level"`
	Evidence             []string  `json:"evidence"`
	ObserverID           string    `json:"observer_id"`
	CelebrationMethod    string    `json:"celebration_method"`
	Notes                string    `json:"notes"`
	CreatedAt            time.Time `json:"created_at"`
	UpdatedAt            time.Time `json:"updated_at"`
}

// Summary Response

type InterventionSummaryResponse struct {
	TotalInterventions       int `json:"total_interventions"`
	ActiveInterventions      int `json:"active_interventions"`
	CompletedInterventions   int `json:"completed_interventions"`
	TotalStudentAssignments  int `json:"total_student_assignments"`
	ActiveStudentAssignments int `json:"active_student_assignments"`
	TotalProgressRecords     int `json:"total_progress_records"`
	TotalMilestones          int `json:"total_milestones"`
	TotalRecommendations     int `json:"total_recommendations"`
	PendingRecommendations   int `json:"pending_recommendations"`
}
