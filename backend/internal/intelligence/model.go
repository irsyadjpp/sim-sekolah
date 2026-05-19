package intelligence

import (
	"time"

	"github.com/google/uuid"
	"github.com/lib/pq"
)

type StudentProfileExt struct {
	StudentID         uuid.UUID      `gorm:"type:uuid;primaryKey" json:"student_id"`
	LearningStyle     string         `gorm:"type:varchar(50)" json:"learning_style"`
	DominantInterests pq.StringArray `gorm:"type:text[]" json:"dominant_interests"`
	SpecialNeedsNotes string         `gorm:"type:text" json:"special_needs_notes"`
	BaselineLiteracy  string         `gorm:"type:varchar(50);default:'NEEDS_IMPROVEMENT'" json:"baseline_literacy"`
	BaselineNumeracy  string         `gorm:"type:varchar(50);default:'NEEDS_IMPROVEMENT'" json:"baseline_numeracy"`
	UpdatedAt         time.Time      `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"updated_at"`
}

func (StudentProfileExt) TableName() string {
	return "cur_student_profile_ext"
}

type ObservationTag struct {
	ID        string `gorm:"type:varchar(20);primaryKey" json:"id"`
	Category  string `gorm:"type:varchar(50);not null" json:"category"`
	TagName   string `gorm:"type:varchar(100);not null" json:"tag_name"`
	Sentiment string `gorm:"type:varchar(10);not null" json:"sentiment"`
}

func (ObservationTag) TableName() string {
	return "sys_observation_tags"
}

type AnecdotalObservation struct {
	ID              uuid.UUID        `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID       uuid.UUID        `gorm:"type:uuid;not null" json:"student_id"`
	TeacherID       uuid.UUID        `gorm:"type:uuid;not null" json:"teacher_id"`
	ObservationDate time.Time        `gorm:"type:date;not null" json:"observation_date"`
	ContextActivity string           `gorm:"type:varchar(100)" json:"context_activity"`
	Notes           string           `gorm:"type:text;not null" json:"notes"`
	CreatedAt       time.Time        `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"created_at"`
	Tags            []ObservationTag `gorm:"many2many:trx_observation_tag_mapping;joinForeignKey:observation_id;joinReferences:tag_id" json:"tags"`
}

func (AnecdotalObservation) TableName() string {
	return "trx_anecdotal_observation"
}

type ObservationTagMapping struct {
	ObservationID uuid.UUID `gorm:"type:uuid;primaryKey" json:"observation_id"`
	TagID         string    `gorm:"type:varchar(20);primaryKey" json:"tag_id"`
}

func (ObservationTagMapping) TableName() string {
	return "trx_observation_tag_mapping"
}

type AssessmentInstrument struct {
	ID                  uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	TeachingModuleID    *uuid.UUID `gorm:"type:uuid" json:"teaching_module_id,omitempty"`
	LearningObjectiveID uuid.UUID  `gorm:"type:uuid;not null" json:"learning_objective_id"`
	Title               string     `gorm:"type:varchar(150);not null" json:"title"`
	AssessmentType      string     `gorm:"type:varchar(20);not null" json:"assessment_type"` // FORMATIF, SUMATIF
	ScoringMethod       string     `gorm:"type:varchar(20);not null" json:"scoring_method"`  // NUMERIC, RUBRIC, OBSERVATION
	CreatedAt           time.Time  `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"created_at"`
}

func (AssessmentInstrument) TableName() string {
	return "trx_assessment_instrument"
}

type StudentAssessmentResult struct {
	ID                uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	InstrumentID      uuid.UUID `gorm:"type:uuid;not null" json:"instrument_id"`
	StudentID         uuid.UUID `gorm:"type:uuid;not null" json:"student_id"`
	NumericScore      *float64  `gorm:"type:numeric(5,2)" json:"numeric_score,omitempty"`
	RubricAchievement string    `gorm:"type:varchar(50)" json:"rubric_achievement,omitempty"`
	NarrativeFeedback string    `gorm:"type:text" json:"narrative_feedback,omitempty"`
	AssessedAt        time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"assessed_at"`
}

func (StudentAssessmentResult) TableName() string {
	return "trx_student_assessment_result"
}

type EarlyWarningAlert struct {
	ID                uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID         uuid.UUID  `gorm:"type:uuid;not null" json:"student_id"`
	ClassroomID       uuid.UUID  `gorm:"type:uuid;not null" json:"classroom_id"`
	AlertType         string     `gorm:"type:varchar(50);not null" json:"alert_type"`     // LITERACY_DELAY, ATTENDANCE_DROP, BEHAVIORAL_CONCERN
	SeverityLevel     string     `gorm:"type:varchar(20);not null" json:"severity_level"` // LOW, MEDIUM, HIGH
	TriggerReason     string     `gorm:"type:text;not null" json:"trigger_reason"`
	Status            string     `gorm:"type:varchar(20);default:'OPEN'" json:"status"` // OPEN, INTERVENED, RESOLVED
	InterventionNotes string     `gorm:"type:text" json:"intervention_notes,omitempty"`
	DetectedAt        time.Time  `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"detected_at"`
	ResolvedAt        *time.Time `gorm:"type:timestamptz" json:"resolved_at,omitempty"`
}

func (EarlyWarningAlert) TableName() string {
	return "anl_early_warning_alert"
}

// DTOs for REST API Requests
type UpsertProfileExtRequest struct {
	LearningStyle     string   `json:"learning_style"`
	DominantInterests []string `json:"dominant_interests"`
	SpecialNeedsNotes string   `json:"special_needs_notes"`
	BaselineLiteracy  string   `json:"baseline_literacy"`
	BaselineNumeracy  string   `json:"baseline_numeracy"`
}

type CreateAnecdotalRequest struct {
	StudentID       string   `json:"student_id" validate:"required,uuid"`
	ContextActivity string   `json:"context_activity"`
	Notes           string   `json:"notes" validate:"required"`
	TagIDs          []string `json:"tag_ids"`
}

type CreateInstrumentRequest struct {
	TeachingModuleID    string `json:"teaching_module_id" validate:"omitempty,uuid"`
	LearningObjectiveID string `json:"learning_objective_id" validate:"required,uuid"`
	Title               string `json:"title" validate:"required,max=150"`
	AssessmentType      string `json:"assessment_type" validate:"required,oneof=FORMATIF SUMATIF"`
	ScoringMethod       string `json:"scoring_method" validate:"required,oneof=NUMERIC RUBRIC OBSERVATION"`
}

type SubmitResultRequest struct {
	StudentID         string   `json:"student_id" validate:"required,uuid"`
	NumericScore      *float64 `json:"numeric_score"`
	RubricAchievement string   `json:"rubric_achievement"`
	NarrativeFeedback string   `json:"narrative_feedback"`
}

type SubmitResultsBatchRequest struct {
	Results []SubmitResultRequest `json:"results" validate:"required,dive"`
}

type EarlyWarningInterventionRequest struct {
	Status            string `json:"status" validate:"required,oneof=OPEN INTERVENED RESOLVED"`
	InterventionNotes string `json:"intervention_notes" validate:"required"`
}

type Student360ProfileResponse struct {
	StudentID          string                 `json:"student_id"`
	FullName           string                 `json:"full_name"`
	NIS                string                 `json:"nis"`
	NISN               string                 `json:"nisn"`
	ProfileExt         *StudentProfileExt     `json:"profile_ext"`
	Anecdotals         []AnecdotalObservation `json:"anecdotals"`
	TagCloud           map[string]int         `json:"tag_cloud"`
	AcademicProgress   map[string]interface{} `json:"academic_progress"` // Progress TP
	EarlyWarningAlerts []EarlyWarningAlert    `json:"early_warning_alerts"`
}
