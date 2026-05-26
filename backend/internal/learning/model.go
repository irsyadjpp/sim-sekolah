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
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ClassroomID    uuid.UUID `gorm:"type:uuid;not null" json:"classroom_id"`
	SubjectID      uuid.UUID `gorm:"type:uuid;not null" json:"subject_id"`
	Title          string    `gorm:"type:varchar(200);not null" json:"title"`        // ATP title for better identification
	AcademicYearID uuid.UUID `gorm:"type:uuid;index" json:"academic_year_id"`        // Link to academic year
	Semester       int       `gorm:"type:integer;default:1" json:"semester"`         // 1 or 2
	TotalMeetings  int       `gorm:"type:integer;default:0" json:"total_meetings"`   // Total estimated meetings
	TotalHours     float64   `gorm:"type:decimal(5,2);default:0" json:"total_hours"` // Total learning hours
	Status         string    `gorm:"type:varchar(20);default:'DRAFT'" json:"status"` // DRAFT, APPROVED, PUBLISHED
	Version        int       `gorm:"type:integer;default:1" json:"version"`          // ATP version for change tracking

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
	ATPID          uuid.UUID `gorm:"type:uuid;primaryKey" json:"atp_id"`
	ObjectiveID    uuid.UUID `gorm:"type:uuid;primaryKey" json:"objective_id"`
	Sequence       int       `gorm:"not null" json:"sequence"`
	MeetingNumber  int       `gorm:"type:integer;default:0" json:"meeting_number"`         // Which meeting this TP is taught in
	EstimatedHours float64   `gorm:"type:decimal(5,2);default:1.0" json:"estimated_hours"` // Time allocation for this TP
	LearningFlow   string    `gorm:"type:varchar(50)" json:"learning_flow"`                // INTRODUCTORY, DEVELOPMENT, PRACTICE, ASSESSMENT, REINFORCEMENT

	Objective *cp.LearningObjective `gorm:"foreignKey:ObjectiveID" json:"objective,omitempty"`
}

func (ATPDetail) TableName() string {
	return "trx_atp_detail"
}

// ATP status constants
const (
	ATPStatusDraft     = "DRAFT"
	ATPStatusApproved  = "APPROVED"
	ATPStatusPublished = "PUBLISHED"
)

// Learning flow constants
const (
	LearningFlowIntroductory  = "INTRODUCTORY"
	LearningFlowDevelopment   = "DEVELOPMENT"
	LearningFlowPractice      = "PRACTICE"
	LearningFlowAssessment    = "ASSESSMENT"
	LearningFlowReinforcement = "REINFORCEMENT"
)

// GetATPStatusDescription returns Indonesian description for ATP status
func GetATPStatusDescription(status string) string {
	descriptions := map[string]string{
		ATPStatusDraft:     "Draf",
		ATPStatusApproved:  "Disetujui",
		ATPStatusPublished: "Diterbitkan",
	}
	if desc, exists := descriptions[status]; exists {
		return desc
	}
	return status
}

// GetLearningFlowDescription returns Indonesian description for learning flow
func GetLearningFlowDescription(flow string) string {
	descriptions := map[string]string{
		LearningFlowIntroductory:  "Pengenalan",
		LearningFlowDevelopment:   "Pengembangan",
		LearningFlowPractice:      "Praktik",
		LearningFlowAssessment:    "Penilaian",
		LearningFlowReinforcement: "Penguatan",
	}
	if desc, exists := descriptions[flow]; exists {
		return desc
	}
	return flow
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
