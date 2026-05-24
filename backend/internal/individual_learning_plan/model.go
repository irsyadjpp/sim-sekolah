package individual_learning_plan

import (
	"time"

	"github.com/google/uuid"

	"sim-sekolah/internal/common"
)

// ILP Status constants
const (
	ILPStatusActive    = "ACTIVE"
	ILPStatusCompleted = "COMPLETED"
	ILPStatusArchived  = "ARCHIVED"
)

// IsValidILPStatus validates ILP status
func IsValidILPStatus(status string) bool {
	validStatuses := map[string]bool{
		ILPStatusActive:    true,
		ILPStatusCompleted: true,
		ILPStatusArchived:  true,
	}
	return validStatuses[status]
}

// IndividualLearningPlan represents an individual learning plan for SD students
type IndividualLearningPlan struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID      uuid.UUID `gorm:"type:uuid;not null;index" json:"student_id"`
	AcademicYearID uuid.UUID `gorm:"type:uuid;not null;index" json:"academic_year_id"`
	Title          string    `gorm:"type:varchar(150);not null" json:"title"`
	Goals          string    `gorm:"type:text" json:"goals"`          // JSON array of learning goals
	Strategies     string    `gorm:"type:text" json:"strategies"`     // JSON array of learning strategies
	Accommodations string    `gorm:"type:text" json:"accommodations"` // JSON array of special accommodations
	ParentNotes    string    `gorm:"type:text" json:"parent_notes"`
	TeacherNotes   string    `gorm:"type:text" json:"teacher_notes"`
	Status         string    `gorm:"type:varchar(20);default:'ACTIVE'" json:"status"`

	common.Auditable
}

func (IndividualLearningPlan) TableName() string {
	return "trx_individual_learning_plan"
}

// ILPMilestone represents milestones within an ILP
type ILPMilestone struct {
	ID            uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ILPID         uuid.UUID  `gorm:"type:uuid;not null;index" json:"ilp_id"`
	MilestoneName string     `gorm:"type:varchar(100);not null" json:"milestone_name"`
	TargetDate    time.Time  `gorm:"type:date" json:"target_date"`
	Achieved      bool       `gorm:"type:boolean;default:false" json:"achieved"`
	AchievedDate  *time.Time `gorm:"type:date" json:"achieved_date,omitempty"`
	Notes         string     `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (ILPMilestone) TableName() string {
	return "trx_ilp_milestone"
}

// ILPTemplate represents SD-appropriate ILP templates
type ILPTemplate struct {
	ID                uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	TemplateCode      string    `gorm:"type:varchar(20);uniqueIndex;not null" json:"template_code"`
	TemplateName      string    `gorm:"type:varchar(100);not null" json:"template_name"`
	PhaseID           uuid.UUID `gorm:"type:uuid;index" json:"phase_id"`
	Description       string    `gorm:"type:text" json:"description"`
	DefaultGoals      string    `gorm:"type:text" json:"default_goals"`      // JSON array
	DefaultStrategies string    `gorm:"type:text" json:"default_strategies"` // JSON array
	IsActive          bool      `gorm:"type:boolean;default:true" json:"is_active"`

	common.Auditable
}

func (ILPTemplate) TableName() string {
	return "master_ilp_template"
}
