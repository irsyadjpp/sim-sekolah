package intervention

import (
	"time"

	"github.com/lib/pq"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// InterventionType Constants
const (
	InterventionTypeRemedial   = "REMEDIAL"
	InterventionTypeEnrichment = "ENRICHMENT"
)

// InterventionStatus Constants
const (
	InterventionStatusPlanned    = "PLANNED"
	InterventionStatusActive     = "ACTIVE"
	InterventionStatusInProgress = "IN_PROGRESS"
	InterventionStatusCompleted  = "COMPLETED"
	InterventionStatusCancelled  = "CANCELLED"
)

// PriorityLevel Constants
const (
	PriorityLevelLow    = "LOW"
	PriorityLevelMedium = "MEDIUM"
	PriorityLevelHigh   = "HIGH"
)

// RemedialProgram represents remedial intervention programs
type RemedialProgram struct {
	ID              uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ProgramName     string         `gorm:"type:varchar(100);not null" json:"program_name"`
	SubjectID       *uuid.UUID     `gorm:"type:uuid" json:"subject_id"`
	TargetGrade     string         `gorm:"type:varchar(50)" json:"target_grade"`
	Description     string         `gorm:"type:text" json:"description"`
	LearningGaps    pq.StringArray `gorm:"type:jsonb" json:"learning_gaps"`
	Strategies      pq.StringArray `gorm:"type:jsonb" json:"strategies"`
	Resources       pq.StringArray `gorm:"type:jsonb" json:"resources"`
	DurationWeeks   int            `gorm:"default:4" json:"duration_weeks"`
	SessionsPerWeek int            `gorm:"default:2" json:"sessions_per_week"`
	SuccessCriteria pq.StringArray `gorm:"type:jsonb" json:"success_criteria"`
	IsActive        bool           `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (RemedialProgram) TableName() string {
	return "remedial_programs"
}

// EnrichmentProgram represents enrichment intervention programs
type EnrichmentProgram struct {
	ID              uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ProgramName     string         `gorm:"type:varchar(100);not null" json:"program_name"`
	SubjectID       *uuid.UUID     `gorm:"type:uuid" json:"subject_id"`
	TargetGrade     string         `gorm:"type:varchar(50)" json:"target_grade"`
	Description     string         `gorm:"type:text" json:"description"`
	AdvancedTopics  pq.StringArray `gorm:"type:jsonb" json:"advanced_topics"`
	Projects        pq.StringArray `gorm:"type:jsonb" json:"projects"`
	Resources       pq.StringArray `gorm:"type:jsonb" json:"resources"`
	DurationWeeks   int            `gorm:"default:4" json:"duration_weeks"`
	SessionsPerWeek int            `gorm:"default:2" json:"sessions_per_week"`
	SuccessCriteria pq.StringArray `gorm:"type:jsonb" json:"success_criteria"`
	IsActive        bool           `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (EnrichmentProgram) TableName() string {
	return "enrichment_programs"
}

// StudentInterventionAssignment represents student-specific intervention assignments
type StudentInterventionAssignment struct {
	ID               uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID        uuid.UUID `gorm:"type:uuid;not null" json:"student_id"`
	ProgramID        uuid.UUID `gorm:"type:uuid;not null" json:"program_id"`
	InterventionType string    `gorm:"type:varchar(20);not null" json:"intervention_type"`
	TeacherID        uuid.UUID `gorm:"type:uuid;not null" json:"teacher_id"`
	AssignmentDate   time.Time `gorm:"type:date;not null;default:CURRENT_DATE" json:"assignment_date"`
	StartDate        time.Time `gorm:"type:date;not null" json:"start_date"`
	EndDate          time.Time `gorm:"type:date;not null" json:"end_date"`
	Status           string    `gorm:"type:varchar(20);default:PLANNED" json:"status"`
	PriorityLevel    string    `gorm:"type:varchar(20);default:MEDIUM" json:"priority_level"`
	BaselineScore    *float64  `gorm:"type:numeric(5,2)" json:"baseline_score"`
	TargetScore      *float64  `gorm:"type:numeric(5,2)" json:"target_score"`
	CurrentScore     *float64  `gorm:"type:numeric(5,2)" json:"current_score"`
	Progress         *float64  `gorm:"type:numeric(3,2)" json:"progress"` // percentage
	CustomizedPlan   string    `gorm:"type:text" json:"customized_plan"`
	Notes            string    `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (StudentInterventionAssignment) TableName() string {
	return "student_intervention_assignments"
}

// InterventionWorkflow represents automated intervention workflows
type InterventionWorkflow struct {
	ID                uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	WorkflowName      string         `gorm:"type:varchar(100);not null" json:"workflow_name"`
	InterventionType  string         `gorm:"type:varchar(20);not null" json:"intervention_type"`
	TriggerConditions pq.StringArray `gorm:"type:jsonb" json:"trigger_conditions"`
	WorkflowSteps     pq.StringArray `gorm:"type:jsonb" json:"workflow_steps"`
	AutoAssignment    bool           `gorm:"default:false" json:"auto_assignment"`
	NotificationRules pq.StringArray `gorm:"type:jsonb" json:"notification_rules"`
	IsActive          bool           `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (InterventionWorkflow) TableName() string {
	return "intervention_workflows"
}

// InterventionAnalytics represents aggregated intervention analytics
type InterventionAnalytics struct {
	ID                         uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID                   uuid.UUID      `gorm:"type:uuid;not null" json:"school_id"`
	AcademicYearID             uuid.UUID      `gorm:"type:uuid;not null" json:"academic_year_id"`
	AnalyticsDate              time.Time      `gorm:"type:date;not null;default:CURRENT_DATE" json:"analytics_date"`
	TotalRemedialAssignments   int            `gorm:"default:0" json:"total_remedial_assignments"`
	TotalEnrichmentAssignments int            `gorm:"default:0" json:"total_enrichment_assignments"`
	ActiveInterventions        int            `gorm:"default:0" json:"active_interventions"`
	CompletedInterventions     int            `gorm:"default:0" json:"completed_interventions"`
	AverageImprovement         *float64       `gorm:"type:numeric(5,2)" json:"average_improvement"`
	SuccessRate                *float64       `gorm:"type:numeric(5,2)" json:"success_rate"`
	MostEffectiveStrategies    pq.StringArray `gorm:"type:jsonb" json:"most_effective_strategies"`
	CommonLearningGaps         pq.StringArray `gorm:"type:jsonb" json:"common_learning_gaps"`

	common.Auditable
}

func (InterventionAnalytics) TableName() string {
	return "intervention_analytics"
}
