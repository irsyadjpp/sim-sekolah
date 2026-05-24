package differentiated_instruction

import (
	"time"

	"github.com/google/uuid"

	"sim-sekolah/internal/common"
)

// DIStrategy represents a differentiated instruction strategy
type DIStrategy struct {
	ID            uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StrategyCode  string    `gorm:"type:varchar(20);uniqueIndex;not null" json:"strategy_code"`
	StrategyName  string    `gorm:"type:varchar(100);not null" json:"strategy_name"`
	Description   string    `gorm:"type:text;not null" json:"description"`
	Applicability string    `gorm:"type:text" json:"applicability"`       // JSON array of when to use
	Examples      string    `gorm:"type:text" json:"examples"`            // JSON array of examples
	TargetGroup   string    `gorm:"type:varchar(50)" json:"target_group"` // ADVANCED, STRUGGLING, SPECIAL_NEEDS, ALL
	IsActive      bool      `gorm:"type:boolean;default:true" json:"is_active"`

	common.Auditable
}

func (DIStrategy) TableName() string {
	return "master_di_strategy"
}

// ModuleDifferentiation represents DI applied to a teaching module
type ModuleDifferentiation struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ModuleID       uuid.UUID `gorm:"type:uuid;not null;index" json:"module_id"`
	StrategyID     uuid.UUID `gorm:"type:uuid;not null;index" json:"strategy_id"`
	TargetStudents string    `gorm:"type:text" json:"target_students"`        // JSON array of student IDs
	Modifications  string    `gorm:"type:text" json:"modifications"`          // JSON array of modifications
	Resources      string    `gorm:"type:text" json:"resources"`              // JSON array of resources
	AssessmentType string    `gorm:"type:varchar(50)" json:"assessment_type"` // FORMATIVE, SUMMATIVE, OBSERVATION
	Notes          string    `gorm:"type:text" json:"notes"`

	common.Auditable

	// Relations
	Strategy DIStrategy `gorm:"foreignKey:StrategyID" json:"strategy,omitempty"`
}

func (ModuleDifferentiation) TableName() string {
	return "trx_module_differentiation"
}

// StudentDINeed represents DI needs assessment for a student
type StudentDINeed struct {
	ID                    uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID             uuid.UUID `gorm:"type:uuid;not null;index" json:"student_id"`
	SubjectID             uuid.UUID `gorm:"type:uuid;index" json:"subject_id"`
	NeedType              string    `gorm:"type:varchar(50);not null" json:"need_type"` // CONTENT, PROCESS, PRODUCT, ENVIRONMENT
	Severity              string    `gorm:"type:varchar(20);not null" json:"severity"`  // LOW, MEDIUM, HIGH
	Description           string    `gorm:"type:text" json:"description"`
	RecommendedStrategies string    `gorm:"type:text" json:"recommended_strategies"` // JSON array
	AssessmentDate        time.Time `gorm:"type:date" json:"assessment_date"`
	IsActive              bool      `gorm:"type:boolean;default:true" json:"is_active"`

	common.Auditable
}

func (StudentDINeed) TableName() string {
	return "trx_student_di_need"
}
