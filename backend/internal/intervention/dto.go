package intervention

import "time"

// RemedialProgramRequest represents request payload for remedial programs
type RemedialProgramRequest struct {
	ProgramName     string   `json:"program_name" validate:"required"`
	SubjectID       *string  `json:"subject_id"`
	TargetGrade     string   `json:"target_grade"`
	Description     string   `json:"description"`
	LearningGaps    []string `json:"learning_gaps"`
	Strategies      []string `json:"strategies"`
	Resources       []string `json:"resources"`
	DurationWeeks   int      `json:"duration_weeks"`
	SessionsPerWeek int      `json:"sessions_per_week"`
	SuccessCriteria []string `json:"success_criteria"`
	IsActive        bool     `json:"is_active"`
}

// RemedialProgramResponse represents response payload for remedial programs
type RemedialProgramResponse struct {
	ID              string    `json:"id"`
	ProgramName     string    `json:"program_name"`
	SubjectID       *string   `json:"subject_id"`
	TargetGrade     string    `json:"target_grade"`
	Description     string    `json:"description"`
	LearningGaps    []string  `json:"learning_gaps"`
	Strategies      []string  `json:"strategies"`
	Resources       []string  `json:"resources"`
	DurationWeeks   int       `json:"duration_weeks"`
	SessionsPerWeek int       `json:"sessions_per_week"`
	SuccessCriteria []string  `json:"success_criteria"`
	IsActive        bool      `json:"is_active"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
}

// EnrichmentProgramRequest represents request payload for enrichment programs
type EnrichmentProgramRequest struct {
	ProgramName     string   `json:"program_name" validate:"required"`
	SubjectID       *string  `json:"subject_id"`
	TargetGrade     string   `json:"target_grade"`
	Description     string   `json:"description"`
	AdvancedTopics  []string `json:"advanced_topics"`
	Projects        []string `json:"projects"`
	Resources       []string `json:"resources"`
	DurationWeeks   int      `json:"duration_weeks"`
	SessionsPerWeek int      `json:"sessions_per_week"`
	SuccessCriteria []string `json:"success_criteria"`
	IsActive        bool     `json:"is_active"`
}

// EnrichmentProgramResponse represents response payload for enrichment programs
type EnrichmentProgramResponse struct {
	ID              string    `json:"id"`
	ProgramName     string    `json:"program_name"`
	SubjectID       *string   `json:"subject_id"`
	TargetGrade     string    `json:"target_grade"`
	Description     string    `json:"description"`
	AdvancedTopics  []string  `json:"advanced_topics"`
	Projects        []string  `json:"projects"`
	Resources       []string  `json:"resources"`
	DurationWeeks   int       `json:"duration_weeks"`
	SessionsPerWeek int       `json:"sessions_per_week"`
	SuccessCriteria []string  `json:"success_criteria"`
	IsActive        bool      `json:"is_active"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
}

// StudentInterventionAssignmentRequest represents request payload for student assignments
type StudentInterventionAssignmentRequest struct {
	StudentID        string    `json:"student_id" validate:"required,uuid"`
	ProgramID        string    `json:"program_id" validate:"required,uuid"`
	InterventionType string    `json:"intervention_type" validate:"required"`
	TeacherID        string    `json:"teacher_id" validate:"required,uuid"`
	StartDate        time.Time `json:"start_date" validate:"required"`
	EndDate          time.Time `json:"end_date" validate:"required"`
	Status           string    `json:"status"`
	PriorityLevel    string    `json:"priority_level"`
	BaselineScore    *float64  `json:"baseline_score"`
	TargetScore      *float64  `json:"target_score"`
	CurrentScore     *float64  `json:"current_score"`
	Progress         *float64  `json:"progress"`
	CustomizedPlan   string    `json:"customized_plan"`
	Notes            string    `json:"notes"`
}

// StudentInterventionAssignmentResponse represents response payload for student assignments
type StudentInterventionAssignmentResponse struct {
	ID               string    `json:"id"`
	StudentID        string    `json:"student_id"`
	ProgramID        string    `json:"program_id"`
	InterventionType string    `json:"intervention_type"`
	TeacherID        string    `json:"teacher_id"`
	AssignmentDate   time.Time `json:"assignment_date"`
	StartDate        time.Time `json:"start_date"`
	EndDate          time.Time `json:"end_date"`
	Status           string    `json:"status"`
	PriorityLevel    string    `json:"priority_level"`
	BaselineScore    *float64  `json:"baseline_score"`
	TargetScore      *float64  `json:"target_score"`
	CurrentScore     *float64  `json:"current_score"`
	Progress         *float64  `json:"progress"`
	CustomizedPlan   string    `json:"customized_plan"`
	Notes            string    `json:"notes"`
	CreatedAt        time.Time `json:"created_at"`
	UpdatedAt        time.Time `json:"updated_at"`
}

// InterventionAnalyticsResponse represents response payload for analytics
type InterventionAnalyticsResponse struct {
	ID                         string    `json:"id"`
	SchoolID                   string    `json:"school_id"`
	AcademicYearID             string    `json:"academic_year_id"`
	AnalyticsDate              time.Time `json:"analytics_date"`
	TotalRemedialAssignments   int       `json:"total_remedial_assignments"`
	TotalEnrichmentAssignments int       `json:"total_enrichment_assignments"`
	ActiveInterventions        int       `json:"active_interventions"`
	CompletedInterventions     int       `json:"completed_interventions"`
	AverageImprovement         *float64  `json:"average_improvement"`
	SuccessRate                *float64  `json:"success_rate"`
	MostEffectiveStrategies    []string  `json:"most_effective_strategies"`
	CommonLearningGaps         []string  `json:"common_learning_gaps"`
	CreatedAt                  time.Time `json:"created_at"`
	UpdatedAt                  time.Time `json:"updated_at"`
}

// InterventionSummaryResponse represents summary statistics
type InterventionSummaryResponse struct {
	TotalAssignments       int64   `json:"total_assignments"`
	RemedialAssignments    int64   `json:"remedial_assignments"`
	EnrichmentAssignments  int64   `json:"enrichment_assignments"`
	ActiveInterventions    int64   `json:"active_interventions"`
	CompletedInterventions int64   `json:"completed_interventions"`
	AverageImprovement     float64 `json:"average_improvement"`
	SuccessRate            float64 `json:"success_rate"`
}
