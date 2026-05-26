package supervision

import "time"

// SupervisionCycleRequest represents request payload for creating/updating supervision cycles
type SupervisionCycleRequest struct {
	CycleName        string    `json:"cycle_name" validate:"required"`
	AcademicYearID   string    `json:"academic_year_id" validate:"required,uuid"`
	SchoolID         string    `json:"school_id" validate:"required,uuid"`
	StartDate        time.Time `json:"start_date" validate:"required"`
	EndDate          time.Time `json:"end_date" validate:"required"`
	Status           string    `json:"status"`
	Description      string    `json:"description"`
	SupervisorID     string    `json:"supervisor_id" validate:"required,uuid"`
	Goals            []string  `json:"goals"`
	ExpectedOutcomes []string  `json:"expected_outcomes"`
	IsActive         bool      `json:"is_active"`
}

// SupervisionCycleResponse represents response payload for supervision cycles
type SupervisionCycleResponse struct {
	ID               string    `json:"id"`
	CycleName        string    `json:"cycle_name"`
	AcademicYearID   string    `json:"academic_year_id"`
	SchoolID         string    `json:"school_id"`
	StartDate        time.Time `json:"start_date"`
	EndDate          time.Time `json:"end_date"`
	Status           string    `json:"status"`
	Description      string    `json:"description"`
	SupervisorID     string    `json:"supervisor_id"`
	Goals            []string  `json:"goals"`
	ExpectedOutcomes []string  `json:"expected_outcomes"`
	IsActive         bool      `json:"is_active"`
	CreatedAt        time.Time `json:"created_at"`
	UpdatedAt        time.Time `json:"updated_at"`
}

// TeacherObservationRequest represents request payload for creating/updating observations
type TeacherObservationRequest struct {
	SupervisionCycleID  *string    `json:"supervision_cycle_id"`
	TeacherID           string     `json:"teacher_id" validate:"required,uuid"`
	ObserverID          string     `json:"observer_id" validate:"required,uuid"`
	SubjectID           *string    `json:"subject_id"`
	ClassroomID         *string    `json:"classroom_id"`
	ObservationDate     time.Time  `json:"observation_date" validate:"required"`
	ObservationType     string     `json:"observation_type"`
	Status              string     `json:"status"`
	StartTime           *time.Time `json:"start_time"`
	EndTime             *time.Time `json:"end_time"`
	LessonTopic         string     `json:"lesson_topic"`
	ClassGrade          string     `json:"class_grade"`
	Strengths           []string   `json:"strengths"`
	AreasForImprovement []string   `json:"areas_for_improvement"`
	Notes               string     `json:"notes"`
	Score               *float64   `json:"score"`
	MaxScore            float64    `json:"max_score"`
}

// TeacherObservationResponse represents response payload for observations
type TeacherObservationResponse struct {
	ID                  string     `json:"id"`
	SupervisionCycleID  *string    `json:"supervision_cycle_id"`
	TeacherID           string     `json:"teacher_id"`
	ObserverID          string     `json:"observer_id"`
	SubjectID           *string    `json:"subject_id"`
	ClassroomID         *string    `json:"classroom_id"`
	ObservationDate     time.Time  `json:"observation_date"`
	ObservationType     string     `json:"observation_type"`
	Status              string     `json:"status"`
	StartTime           *time.Time `json:"start_time"`
	EndTime             *time.Time `json:"end_time"`
	LessonTopic         string     `json:"lesson_topic"`
	ClassGrade          string     `json:"class_grade"`
	Strengths           []string   `json:"strengths"`
	AreasForImprovement []string   `json:"areas_for_improvement"`
	Notes               string     `json:"notes"`
	Score               *float64   `json:"score"`
	MaxScore            float64    `json:"max_score"`
	CreatedAt           time.Time  `json:"created_at"`
	UpdatedAt           time.Time  `json:"updated_at"`
}

// SupervisionFeedbackRequest represents request payload for creating/updating feedback
type SupervisionFeedbackRequest struct {
	ObservationID      string     `json:"observation_id" validate:"required,uuid"`
	TeacherID          string     `json:"teacher_id" validate:"required,uuid"`
	FeedbackDate       time.Time  `json:"feedback_date"`
	FeedbackProviderID string     `json:"feedback_provider_id" validate:"required,uuid"`
	Status             string     `json:"status"`
	Strengths          []string   `json:"strengths"`
	ImprovementAreas   []string   `json:"improvement_areas"`
	Recommendations    []string   `json:"recommendations"`
	ActionPlan         string     `json:"action_plan"`
	FollowUpDate       *time.Time `json:"follow_up_date"`
	TeacherResponse    string     `json:"teacher_response"`
	ResponseDate       *time.Time `json:"response_date"`
	IsAcknowledged     bool       `json:"is_acknowledged"`
	OverallRating      *float64   `json:"overall_rating"`
	Comments           string     `json:"comments"`
}

// SupervisionFeedbackResponse represents response payload for feedback
type SupervisionFeedbackResponse struct {
	ID                 string     `json:"id"`
	ObservationID      string     `json:"observation_id"`
	TeacherID          string     `json:"teacher_id"`
	FeedbackDate       time.Time  `json:"feedback_date"`
	FeedbackProviderID string     `json:"feedback_provider_id"`
	Status             string     `json:"status"`
	Strengths          []string   `json:"strengths"`
	ImprovementAreas   []string   `json:"improvement_areas"`
	Recommendations    []string   `json:"recommendations"`
	ActionPlan         string     `json:"action_plan"`
	FollowUpDate       *time.Time `json:"follow_up_date"`
	TeacherResponse    string     `json:"teacher_response"`
	ResponseDate       *time.Time `json:"response_date"`
	IsAcknowledged     bool       `json:"is_acknowledged"`
	OverallRating      *float64   `json:"overall_rating"`
	Comments           string     `json:"comments"`
	CreatedAt          time.Time  `json:"created_at"`
	UpdatedAt          time.Time  `json:"updated_at"`
}

// SupervisionAnalyticsResponse represents response payload for analytics
type SupervisionAnalyticsResponse struct {
	ID                     string    `json:"id"`
	SchoolID               string    `json:"school_id"`
	AcademicYearID         string    `json:"academic_year_id"`
	SupervisionCycleID     *string   `json:"supervision_cycle_id"`
	AnalyticsDate          time.Time `json:"analytics_date"`
	TotalObservations      int64     `json:"total_observations"`
	CompletedObservations  int64     `json:"completed_observations"`
	AverageScore           *float64  `json:"average_score"`
	TeachersSupervised     int64     `json:"teachers_supervised"`
	ImprovementRate        *float64  `json:"improvement_rate"`
	FeedbackCompletionRate *float64  `json:"feedback_completion_rate"`
	TopStrengths           []string  `json:"top_strengths"`
	CommonImprovementAreas []string  `json:"common_improvement_areas"`
	CreatedAt              time.Time `json:"created_at"`
	UpdatedAt              time.Time `json:"updated_at"`
}

// SupervisionSummaryResponse represents summary statistics
type SupervisionSummaryResponse struct {
	TotalCycles           int64   `json:"total_cycles"`
	ActiveCycles          int64   `json:"active_cycles"`
	TotalObservations     int64   `json:"total_observations"`
	PendingObservations   int64   `json:"pending_observations"`
	CompletedObservations int64   `json:"completed_observations"`
	AverageScore          float64 `json:"average_score"`
	TeachersSupervised    int64   `json:"teachers_supervised"`
}
