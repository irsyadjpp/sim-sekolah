package teaching_reflection

import (
	"time"

	"github.com/lib/pq"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// ReflectionType Constants
const (
	ReflectionTypeDaily    = "DAILY"
	ReflectionTypeWeekly   = "WEEKLY"
	ReflectionTypeUnit     = "UNIT"
	ReflectionTypeTerm     = "TERM"
	ReflectionTypeIncident = "INCIDENT"
)

// ReflectionStatus Constants
const (
	ReflectionStatusDraft     = "DRAFT"
	ReflectionStatusSubmitted = "SUBMITTED"
	ReflectionStatusReviewed  = "REVIEWED"
)

// QualityRating Constants
const (
	QualityRatingExcellent        = "EXCELLENT"
	QualityRatingGood             = "GOOD"
	QualityRatingSatisfactory     = "SATISFACTORY"
	QualityRatingNeedsImprovement = "NEEDS_IMPROVEMENT"
)

// TeachingReflection represents teacher self-reflection
type TeachingReflection struct {
	ID                 uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	TeacherID          uuid.UUID      `gorm:"type:uuid;not null" json:"teacher_id"`
	SubjectID          *uuid.UUID     `gorm:"type:uuid" json:"subject_id"`
	ClassroomID        *uuid.UUID     `gorm:"type:uuid" json:"classroom_id"`
	ReflectionDate     time.Time      `gorm:"type:date;not null;default:CURRENT_DATE" json:"reflection_date"`
	ReflectionType     string         `gorm:"type:varchar(20);default:DAILY" json:"reflection_type"`
	Status             string         `gorm:"type:varchar(20);default:DRAFT" json:"status"`
	LessonTopic        string         `gorm:"type:varchar(200)" json:"lesson_topic"`
	WhatWentWell       pq.StringArray `gorm:"type:jsonb" json:"what_went_well"`
	WhatCouldImprove   pq.StringArray `gorm:"type:jsonb" json:"what_could_improve"`
	StudentEngagement  string         `gorm:"type:text" json:"student_engagement"`
	TeachingStrategies pq.StringArray `gorm:"type:jsonb" json:"teaching_strategies"`
	Challenges         pq.StringArray `gorm:"type:jsonb" json:"challenges"`
	Solutions          pq.StringArray `gorm:"type:jsonb" json:"solutions"`
	NextSteps          pq.StringArray `gorm:"type:jsonb" json:"next_steps"`
	SelfRating         *float64       `gorm:"type:numeric(3,2)" json:"self_rating"`
	Notes              string         `gorm:"type:text" json:"notes"`
	IsPrivate          bool           `gorm:"default:false" json:"is_private"`

	common.Auditable
}

func (TeachingReflection) TableName() string {
	return "teaching_reflections"
}

// EffectivenessMetrics represents teaching effectiveness measurements
type EffectivenessMetrics struct {
	ID                   uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	TeacherID            uuid.UUID      `gorm:"type:uuid;not null" json:"teacher_id"`
	SubjectID            *uuid.UUID     `gorm:"type:uuid" json:"subject_id"`
	MeasurementDate      time.Time      `gorm:"type:date;not null;default:CURRENT_DATE" json:"measurement_date"`
	StudentSatisfaction  *float64       `gorm:"type:numeric(3,2)" json:"student_satisfaction"`
	LearningOutcomes     *float64       `gorm:"type:numeric(3,2)" json:"learning_outcomes"`
	EngagementLevel      *float64       `gorm:"type:numeric(3,2)" json:"engagement_level"`
	TimeManagement       *float64       `gorm:"type:numeric(3,2)" json:"time_management"`
	ContentDelivery      *float64       `gorm:"type:numeric(3,2)" json:"content_delivery"`
	OverallEffectiveness *float64       `gorm:"type:numeric(3,2)" json:"overall_effectiveness"`
	Strengths            pq.StringArray `gorm:"type:jsonb" json:"strengths"`
	ImprovementAreas     pq.StringArray `gorm:"type:jsonb" json:"improvement_areas"`
	BenchmarkComparison  *float64       `gorm:"type:numeric(3,2)" json:"benchmark_comparison"`
	Notes                string         `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (EffectivenessMetrics) TableName() string {
	return "teaching_effectiveness_metrics"
}

// QualityIndicators represents teaching quality indicators
type QualityIndicators struct {
	ID                uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	TeacherID         uuid.UUID      `gorm:"type:uuid;not null" json:"teacher_id"`
	AssessmentDate    time.Time      `gorm:"type:date;not null;default:CURRENT_DATE" json:"assessment_date"`
	IndicatorCategory string         `gorm:"type:varchar(50)" json:"indicator_category"`
	IndicatorName     string         `gorm:"type:varchar(100);not null" json:"indicator_name"`
	QualityRating     string         `gorm:"type:varchar(30)" json:"quality_rating"`
	Score             *float64       `gorm:"type:numeric(3,2)" json:"score"`
	Evidence          pq.StringArray `gorm:"type:jsonb" json:"evidence"`
	Feedback          string         `gorm:"type:text" json:"feedback"`
	ActionRequired    bool           `gorm:"default:false" json:"action_required"`
	ActionPlan        string         `gorm:"type:text" json:"action_plan"`
	TargetDate        *time.Time     `gorm:"type:date" json:"target_date"`

	common.Auditable
}

func (QualityIndicators) TableName() string {
	return "teaching_quality_indicators"
}

// ReflectionTrend represents reflection trends over time
type ReflectionTrend struct {
	ID                uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	TeacherID         uuid.UUID      `gorm:"type:uuid;not null" json:"teacher_id"`
	TrendPeriod       string         `gorm:"type:varchar(20)" json:"trend_period"`
	StartDate         time.Time      `gorm:"type:date" json:"start_date"`
	EndDate           time.Time      `gorm:"type:date" json:"end_date"`
	TotalReflections  int            `gorm:"default:0" json:"total_reflections"`
	AverageSelfRating *float64       `gorm:"type:numeric(3,2)" json:"average_self_rating"`
	CommonThemes      pq.StringArray `gorm:"type:jsonb" json:"common_themes"`
	ImprovementAreas  pq.StringArray `gorm:"type:jsonb" json:"improvement_areas"`
	GrowthIndicators  pq.StringArray `gorm:"type:jsonb" json:"growth_indicators"`
	Recommendations   pq.StringArray `gorm:"type:jsonb" json:"recommendations"`

	common.Auditable
}

func (ReflectionTrend) TableName() string {
	return "reflection_trends"
}
