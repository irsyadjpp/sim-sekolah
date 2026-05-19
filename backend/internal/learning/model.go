package learning

import (
	"sim-sekolah/internal/classroom"
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/cp"
	"sim-sekolah/internal/deep_learning/elemen_desain"
	"sim-sekolah/internal/deep_learning/tahapan_kognitif"
	"sim-sekolah/internal/profile_dimension"
	"sim-sekolah/internal/subject"

	"github.com/google/uuid"
)

// ATP (Alur Tujuan Pembelajaran)
type ATP struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ClassroomID uuid.UUID `gorm:"type:uuid;not null" json:"classroom_id"`
	SubjectID   uuid.UUID `gorm:"type:uuid;not null" json:"subject_id"`

	common.Auditable

	Classroom *classroom.Classroom `gorm:"foreignKey:ClassroomID" json:"classroom,omitempty"`
	Subject   *subject.Subject     `gorm:"foreignKey:SubjectID" json:"subject,omitempty"`
	Details   []ATPDetail          `gorm:"foreignKey:ATPID" json:"details,omitempty"`
}

func (ATP) TableName() string {
	return "trx_atp"
}

// ATPDetail handles the sequence of TPs in an ATP
type ATPDetail struct {
	ATPID       uuid.UUID `gorm:"type:uuid;primaryKey" json:"atp_id"`
	ObjectiveID uuid.UUID `gorm:"type:uuid;primaryKey" json:"objective_id"`
	Sequence    int       `gorm:"not null" json:"sequence"`

	Objective *cp.LearningObjective `gorm:"foreignKey:ObjectiveID" json:"objective,omitempty"`
}

func (ATPDetail) TableName() string {
	return "trx_atp_detail"
}

// TeachingModule (Modul Ajar / RPP)
type TeachingModule struct {
	ID     uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ATPID  uuid.UUID `gorm:"type:uuid;not null" json:"atp_id"`
	Title  string    `gorm:"type:varchar(150);not null" json:"title"`
	Status string    `gorm:"type:varchar(20);default:'DRAFT'" json:"status"` // DRAFT, FINAL

	common.Auditable

	Activities []ModuleActivity              `gorm:"foreignKey:ModuleID" json:"activities,omitempty"`
	Elements   []elemen_desain.DesignElement `gorm:"many2many:trx_module_element_mapping;" json:"elements,omitempty"`
}

func (TeachingModule) TableName() string {
	return "trx_teaching_module"
}

// ModuleActivity maps to Deep Learning cognitive stages
type ModuleActivity struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ModuleID    uuid.UUID `gorm:"type:uuid;not null" json:"module_id"`
	StageID     uuid.UUID `gorm:"type:uuid;not null" json:"stage_id"`
	Description string    `gorm:"type:text;not null" json:"description"`

	Stage *tahapan_kognitif.CognitiveStage `gorm:"foreignKey:StageID" json:"stage,omitempty"`
}

func (ModuleActivity) TableName() string {
	return "trx_teaching_module_activity"
}

// ProjectModule (Modul Projek P5)
type ProjectModule struct {
	ID    uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Title string    `gorm:"type:varchar(150);not null" json:"title"`

	common.Auditable

	Dimensions []profile_dimension.ProfileDimension `gorm:"many2many:trx_project_dimension_mapping;" json:"dimensions,omitempty"`
}

func (ProjectModule) TableName() string {
	return "trx_project_module"
}
