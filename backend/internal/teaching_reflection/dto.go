package teaching_reflection

import "time"

// TeachingReflectionRequest represents request payload for teaching reflections
type TeachingReflectionRequest struct {
	TeacherID          string    `json:"teacher_id" validate:"required,uuid"`
	SubjectID          *string   `json:"subject_id"`
	ClassroomID        *string   `json:"classroom_id"`
	ReflectionDate     time.Time `json:"reflection_date"`
	ReflectionType     string    `json:"reflection_type"`
	Status             string    `json:"status"`
	LessonTopic        string    `json:"lesson_topic"`
	WhatWentWell       []string  `json:"what_went_well"`
	WhatCouldImprove   []string  `json:"what_could_improve"`
	StudentEngagement  string    `json:"student_engagement"`
	TeachingStrategies []string  `json:"teaching_strategies"`
	Challenges         []string  `json:"challenges"`
	Solutions          []string  `json:"solutions"`
	NextSteps          []string  `json:"next_steps"`
	SelfRating         *float64  `json:"self_rating"`
	Notes              string    `json:"notes"`
	IsPrivate          bool      `json:"is_private"`
}

// TeachingReflectionResponse represents response payload for teaching reflections
type TeachingReflectionResponse struct {
	ID                 string    `json:"id"`
	TeacherID          string    `json:"teacher_id"`
	SubjectID          *string   `json:"subject_id"`
	ClassroomID        *string   `json:"classroom_id"`
	ReflectionDate     time.Time `json:"reflection_date"`
	ReflectionType     string    `json:"reflection_type"`
	Status             string    `json:"status"`
	LessonTopic        string    `json:"lesson_topic"`
	WhatWentWell       []string  `json:"what_went_well"`
	WhatCouldImprove   []string  `json:"what_could_improve"`
	StudentEngagement  string    `json:"student_engagement"`
	TeachingStrategies []string  `json:"teaching_strategies"`
	Challenges         []string  `json:"challenges"`
	Solutions          []string  `json:"solutions"`
	NextSteps          []string  `json:"next_steps"`
	SelfRating         *float64  `json:"self_rating"`
	Notes              string    `json:"notes"`
	IsPrivate          bool      `json:"is_private"`
	CreatedAt          time.Time `json:"created_at"`
	UpdatedAt          time.Time `json:"updated_at"`
}

// EffectivenessMetricsRequest represents request payload for effectiveness metrics
type EffectivenessMetricsRequest struct {
	TeacherID            string    `json:"teacher_id" validate:"required,uuid"`
	SubjectID            *string   `json:"subject_id"`
	MeasurementDate      time.Time `json:"measurement_date"`
	StudentSatisfaction  *float64  `json:"student_satisfaction"`
	LearningOutcomes     *float64  `json:"learning_outcomes"`
	EngagementLevel      *float64  `json:"engagement_level"`
	TimeManagement       *float64  `json:"time_management"`
	ContentDelivery      *float64  `json:"content_delivery"`
	OverallEffectiveness *float64  `json:"overall_effectiveness"`
	Strengths            []string  `json:"strengths"`
	ImprovementAreas     []string  `json:"improvement_areas"`
	BenchmarkComparison  *float64  `json:"benchmark_comparison"`
	Notes                string    `json:"notes"`
}

// EffectivenessMetricsResponse represents response payload for effectiveness metrics
type EffectivenessMetricsResponse struct {
	ID                   string    `json:"id"`
	TeacherID            string    `json:"teacher_id"`
	SubjectID            *string   `json:"subject_id"`
	MeasurementDate      time.Time `json:"measurement_date"`
	StudentSatisfaction  *float64  `json:"student_satisfaction"`
	LearningOutcomes     *float64  `json:"learning_outcomes"`
	EngagementLevel      *float64  `json:"engagement_level"`
	TimeManagement       *float64  `json:"time_management"`
	ContentDelivery      *float64  `json:"content_delivery"`
	OverallEffectiveness *float64  `json:"overall_effectiveness"`
	Strengths            []string  `json:"strengths"`
	ImprovementAreas     []string  `json:"improvement_areas"`
	BenchmarkComparison  *float64  `json:"benchmark_comparison"`
	Notes                string    `json:"notes"`
	CreatedAt            time.Time `json:"created_at"`
	UpdatedAt            time.Time `json:"updated_at"`
}

// QualityIndicatorsRequest represents request payload for quality indicators
type QualityIndicatorsRequest struct {
	TeacherID         string     `json:"teacher_id" validate:"required,uuid"`
	AssessmentDate    time.Time  `json:"assessment_date"`
	IndicatorCategory string     `json:"indicator_category"`
	IndicatorName     string     `json:"indicator_name" validate:"required"`
	QualityRating     string     `json:"quality_rating"`
	Score             *float64   `json:"score"`
	Evidence          []string   `json:"evidence"`
	Feedback          string     `json:"feedback"`
	ActionRequired    bool       `json:"action_required"`
	ActionPlan        string     `json:"action_plan"`
	TargetDate        *time.Time `json:"target_date"`
}

// QualityIndicatorsResponse represents response payload for quality indicators
type QualityIndicatorsResponse struct {
	ID                string     `json:"id"`
	TeacherID         string     `json:"teacher_id"`
	AssessmentDate    time.Time  `json:"assessment_date"`
	IndicatorCategory string     `json:"indicator_category"`
	IndicatorName     string     `json:"indicator_name"`
	QualityRating     string     `json:"quality_rating"`
	Score             *float64   `json:"score"`
	Evidence          []string   `json:"evidence"`
	Feedback          string     `json:"feedback"`
	ActionRequired    bool       `json:"action_required"`
	ActionPlan        string     `json:"action_plan"`
	TargetDate        *time.Time `json:"target_date"`
	CreatedAt         time.Time  `json:"created_at"`
	UpdatedAt         time.Time  `json:"updated_at"`
}

// ReflectionTrendResponse represents response payload for reflection trends
type ReflectionTrendResponse struct {
	ID                string    `json:"id"`
	TeacherID         string    `json:"teacher_id"`
	TrendPeriod       string    `json:"trend_period"`
	StartDate         time.Time `json:"start_date"`
	EndDate           time.Time `json:"end_date"`
	TotalReflections  int       `json:"total_reflections"`
	AverageSelfRating *float64  `json:"average_self_rating"`
	CommonThemes      []string  `json:"common_themes"`
	ImprovementAreas  []string  `json:"improvement_areas"`
	GrowthIndicators  []string  `json:"growth_indicators"`
	Recommendations   []string  `json:"recommendations"`
	CreatedAt         time.Time `json:"created_at"`
	UpdatedAt         time.Time `json:"updated_at"`
}

// ReflectionSummaryResponse represents summary statistics
type ReflectionSummaryResponse struct {
	TotalReflections     int64   `json:"total_reflections"`
	SubmittedReflections int64   `json:"submitted_reflections"`
	AverageSelfRating    float64 `json:"average_self_rating"`
	MostUsedType         string  `json:"most_used_type"`
	RecentActivity       int64   `json:"recent_activity"` // Last 30 days
}
