package numeracy

import (
	"time"

	"github.com/google/uuid"
)

// NumeracyIndicatorRequest represents request body for creating/updating numeracy indicator
type NumeracyIndicatorRequest struct {
	PhaseID       uuid.UUID `json:"phase_id" validate:"required"`
	NumeracyType  string    `json:"numeracy_type" validate:"required"`
	IndicatorCode string    `json:"indicator_code" validate:"required"`
	IndicatorName string    `json:"indicator_name" validate:"required"`
	Description   string    `json:"description" validate:"required"`
	GradeLevel    string    `json:"grade_level"`
	MinAge        int       `json:"min_age"`
	MaxAge        int       `json:"max_age"`
	Difficulty    string    `json:"difficulty"`
	Examples      string    `json:"examples"`
	IsActive      *bool     `json:"is_active"`
}

// NumeracyIndicatorResponse represents response body for numeracy indicator
type NumeracyIndicatorResponse struct {
	ID            uuid.UUID `json:"id"`
	PhaseID       uuid.UUID `json:"phase_id"`
	PhaseName     string    `json:"phase_name,omitempty"`
	NumeracyType  string    `json:"numeracy_type"`
	TypeName      string    `json:"type_name,omitempty"`
	IndicatorCode string    `json:"indicator_code"`
	IndicatorName string    `json:"indicator_name"`
	Description   string    `json:"description"`
	GradeLevel    string    `json:"grade_level"`
	MinAge        int       `json:"min_age"`
	MaxAge        int       `json:"max_age"`
	Difficulty    string    `json:"difficulty"`
	Examples      string    `json:"examples"`
	IsActive      bool      `json:"is_active"`
	CreatedAt     time.Time `json:"created_at"`
	UpdatedAt     time.Time `json:"updated_at"`
}

// NumeracyAssessmentRequest represents request body for creating/updating numeracy assessment
type NumeracyAssessmentRequest struct {
	StudentID      uuid.UUID `json:"student_id" validate:"required"`
	IndicatorID    uuid.UUID `json:"indicator_id" validate:"required"`
	AssessmentDate time.Time `json:"assessment_date" validate:"required"`
	AssessmentType string    `json:"assessment_type" validate:"required"`
	Score          float64   `json:"score" validate:"min=0,max=100"`
	MasteryLevel   string    `json:"mastery_level" validate:"required"`
	ResponseTime   int       `json:"response_time"`
	Attempts       int       `json:"attempts"`
	TeacherID      uuid.UUID `json:"teacher_id"`
	Notes          string    `json:"notes"`
	EvidenceFiles  string    `json:"evidence_files"`
}

// NumeracyAssessmentResponse represents response body for numeracy assessment
type NumeracyAssessmentResponse struct {
	ID             uuid.UUID `json:"id"`
	StudentID      uuid.UUID `json:"student_id"`
	StudentName    string    `json:"student_name,omitempty"`
	IndicatorID    uuid.UUID `json:"indicator_id"`
	IndicatorName  string    `json:"indicator_name,omitempty"`
	IndicatorCode  string    `json:"indicator_code,omitempty"`
	AssessmentDate time.Time `json:"assessment_date"`
	AssessmentType string    `json:"assessment_type"`
	Score          float64   `json:"score"`
	MasteryLevel   string    `json:"mastery_level"`
	LevelName      string    `json:"level_name,omitempty"`
	ResponseTime   int       `json:"response_time"`
	Attempts       int       `json:"attempts"`
	TeacherID      uuid.UUID `json:"teacher_id"`
	TeacherName    string    `json:"teacher_name,omitempty"`
	Notes          string    `json:"notes"`
	EvidenceFiles  string    `json:"evidence_files"`
	CreatedAt      time.Time `json:"created_at"`
	UpdatedAt      time.Time `json:"updated_at"`
}

// NumeracyGrowthRequest represents request body for creating/updating numeracy growth
type NumeracyGrowthRequest struct {
	StudentID         uuid.UUID `json:"student_id" validate:"required"`
	Period            string    `json:"period" validate:"required"`
	AcademicYearID    uuid.UUID `json:"academic_year_id" validate:"required"`
	OverallScore      float64   `json:"overall_score" validate:"min=0,max=100"`
	NumbersScore      float64   `json:"numbers_score" validate:"min=0,max=100"`
	OperationsScore   float64   `json:"operations_score" validate:"min=0,max=100"`
	GeometryScore     float64   `json:"geometry_score" validate:"min=0,max=100"`
	MeasurementScore  float64   `json:"measurement_score" validate:"min=0,max=100"`
	DataAnalysisScore float64   `json:"data_analysis_score" validate:"min=0,max=100"`
	MasteryRate       float64   `json:"mastery_rate" validate:"min=0,max=100"`
	GrowthRate        float64   `json:"growth_rate"`
	Percentile        int       `json:"percentile" validate:"min=0,max=100"`
	TeacherID         uuid.UUID `json:"teacher_id"`
	Notes             string    `json:"notes"`
}

// NumeracyGrowthResponse represents response body for numeracy growth
type NumeracyGrowthResponse struct {
	ID                uuid.UUID `json:"id"`
	StudentID         uuid.UUID `json:"student_id"`
	StudentName       string    `json:"student_name,omitempty"`
	Period            string    `json:"period"`
	PeriodName        string    `json:"period_name,omitempty"`
	AcademicYearID    uuid.UUID `json:"academic_year_id"`
	AcademicYear      string    `json:"academic_year,omitempty"`
	OverallScore      float64   `json:"overall_score"`
	NumbersScore      float64   `json:"numbers_score"`
	OperationsScore   float64   `json:"operations_score"`
	GeometryScore     float64   `json:"geometry_score"`
	MeasurementScore  float64   `json:"measurement_score"`
	DataAnalysisScore float64   `json:"data_analysis_score"`
	MasteryRate       float64   `json:"mastery_rate"`
	GrowthRate        float64   `json:"growth_rate"`
	Percentile        int       `json:"percentile"`
	TeacherID         uuid.UUID `json:"teacher_id"`
	TeacherName       string    `json:"teacher_name,omitempty"`
	Notes             string    `json:"notes"`
	CreatedAt         time.Time `json:"created_at"`
	UpdatedAt         time.Time `json:"updated_at"`
}

// NumeracyInterventionRequest represents request body for creating/updating numeracy intervention
type NumeracyInterventionRequest struct {
	StudentID        uuid.UUID `json:"student_id" validate:"required"`
	IndicatorID      uuid.UUID `json:"indicator_id" validate:"required"`
	InterventionType string    `json:"intervention_type" validate:"required"`
	StartDate        time.Time `json:"start_date" validate:"required"`
	EndDate          time.Time `json:"end_date"`
	Status           string    `json:"status" validate:"required"`
	Activities       string    `json:"activities"`
	TeacherID        uuid.UUID `json:"teacher_id"`
	Outcome          string    `json:"outcome"`
	Effectiveness    string    `json:"effectiveness"`
}

// NumeracyInterventionResponse represents response body for numeracy intervention
type NumeracyInterventionResponse struct {
	ID               uuid.UUID `json:"id"`
	StudentID        uuid.UUID `json:"student_id"`
	StudentName      string    `json:"student_name,omitempty"`
	IndicatorID      uuid.UUID `json:"indicator_id"`
	IndicatorName    string    `json:"indicator_name,omitempty"`
	IndicatorCode    string    `json:"indicator_code,omitempty"`
	InterventionType string    `json:"intervention_type"`
	TypeName         string    `json:"type_name,omitempty"`
	StartDate        time.Time `json:"start_date"`
	EndDate          time.Time `json:"end_date"`
	Status           string    `json:"status"`
	StatusName       string    `json:"status_name,omitempty"`
	Activities       string    `json:"activities"`
	TeacherID        uuid.UUID `json:"teacher_id"`
	TeacherName      string    `json:"teacher_name,omitempty"`
	Outcome          string    `json:"outcome"`
	Effectiveness    string    `json:"effectiveness"`
	CreatedAt        time.Time `json:"created_at"`
	UpdatedAt        time.Time `json:"updated_at"`
}

// NumeracyAnalyticsRequest represents request for numeracy analytics
type NumeracyAnalyticsRequest struct {
	StudentID    *uuid.UUID `json:"student_id,omitempty"`
	ClassroomID  *uuid.UUID `json:"classroom_id,omitempty"`
	PhaseID      *uuid.UUID `json:"phase_id,omitempty"`
	StartDate    *time.Time `json:"start_date,omitempty"`
	EndDate      *time.Time `json:"end_date,omitempty"`
	NumeracyType *string    `json:"numeracy_type,omitempty"`
}

// NumeracyAnalyticsResponse represents numeracy analytics data
type NumeracyAnalyticsResponse struct {
	TotalAssessments    int64                `json:"total_assessments"`
	AverageScore        float64              `json:"average_score"`
	MasteryRate         float64              `json:"mastery_rate"`
	ByNumeracyType      []NumeracyTypeStats  `json:"by_numeracy_type"`
	ByMasteryLevel      []MasteryLevelStats  `json:"by_mastery_level"`
	GrowthTrend         []GrowthTrendData    `json:"growth_trend"`
	TopPerformers       []StudentPerformance `json:"top_performers,omitempty"`
	StudentsNeedSupport []StudentPerformance `json:"students_need_support,omitempty"`
}

// NumeracyTypeStats represents statistics by numeracy type
type NumeracyTypeStats struct {
	NumeracyType string  `json:"numeracy_type"`
	TypeName     string  `json:"type_name"`
	Count        int64   `json:"count"`
	AverageScore float64 `json:"average_score"`
}

// MasteryLevelStats represents statistics by mastery level
type MasteryLevelStats struct {
	MasteryLevel string  `json:"mastery_level"`
	LevelName    string  `json:"level_name"`
	Count        int64   `json:"count"`
	Percentage   float64 `json:"percentage"`
}

// GrowthTrendData represents growth trend over time
type GrowthTrendData struct {
	Period       string  `json:"period"`
	AverageScore float64 `json:"average_score"`
	MasteryRate  float64 `json:"mastery_rate"`
}

// StudentPerformance represents student performance data
type StudentPerformance struct {
	StudentID    uuid.UUID `json:"student_id"`
	StudentName  string    `json:"student_name"`
	AverageScore float64   `json:"average_score"`
	MasteryRate  float64   `json:"mastery_rate"`
}
