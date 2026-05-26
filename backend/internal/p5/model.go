package p5

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/subject"

	"github.com/google/uuid"
)

// Project represents a P5 (Proyek Penguatan Profil Pelajar Pancasila) project
type Project struct {
	ID             uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Title          string     `gorm:"type:varchar(200);not null" json:"title"`
	Description    string     `gorm:"type:text" json:"description"`
	SubjectID      *uuid.UUID `gorm:"type:uuid;index" json:"subject_id"`
	ClassroomID    *uuid.UUID `gorm:"type:uuid;index" json:"classroom_id"`
	ProjectTheme   string     `gorm:"type:varchar(100);not null;index" json:"project_theme"` // e.g., "Kewirausahaan", "Bhinneka Tunggal Ika"
	AcademicYearID *uuid.UUID `gorm:"type:uuid;index" json:"academic_year_id"`
	Semester       int        `gorm:"type:integer;default:1" json:"semester"` // 1 or 2

	// Project Timing
	StartDate  string `gorm:"type:varchar(50)" json:"start_date"` // e.g., "Minggu ke-1"
	EndDate    string `gorm:"type:varchar(50)" json:"end_date"`
	TotalWeeks int    `gorm:"type:integer;default:4" json:"total_weeks"` // Duration in weeks

	// Project Details
	ProjectType        string `gorm:"type:varchar(50);not null;index" json:"project_type"` // INDIVIDUAL, GROUP, CLASS
	MaxTeamSize        int    `gorm:"type:integer;default:5" json:"max_team_size"`
	RequiredDimensions string `gorm:"type:text" json:"required_dimensions"` // Profile dimensions required (JSON array)

	// Status and Progress
	Status   string `gorm:"type:varchar(20);default:'PLANNING'" json:"status"` // PLANNING, ONGOING, PAUSED, COMPLETED, CANCELLED
	Progress int    `gorm:"type:integer;default:0" json:"progress"`            // Progress percentage (0-100)

	// Integration
	TeachingModuleID *uuid.UUID `gorm:"type:uuid;index" json:"teaching_module_id"` // Link to TeachingModule
	RubricID         *uuid.UUID `gorm:"type:uuid;index" json:"rubric_id"`          // Assessment rubric

	common.Auditable

	Subject        *subject.Subject       `gorm:"foreignKey:SubjectID" json:"subject,omitempty"`
	Teams          []ProjectTeam          `gorm:"foreignKey:ProjectID" json:"teams,omitempty"`
	Milestones     []ProjectMilestone     `gorm:"foreignKey:ProjectID" json:"milestones,omitempty"`
	Participations []StudentParticipation `gorm:"foreignKey:ProjectID" json:"participations,omitempty"`
}

func (Project) TableName() string {
	return "p5_projects"
}

// ProjectTeam represents student teams for P5 projects
type ProjectTeam struct {
	ID           uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ProjectID    uuid.UUID  `gorm:"type:uuid;not null;index" json:"project_id"`
	TeamName     string     `gorm:"type:varchar(100);not null" json:"team_name"`
	TeamCode     string     `gorm:"type:varchar(20);uniqueIndex:not null" json:"team_code"` // Auto-generated unique code
	MaxMembers   int        `gorm:"type:integer;default:5" json:"max_members"`
	CurrentSize  int        `gorm:"type:integer;default:0" json:"current_size"`
	TeamLeaderID *uuid.UUID `gorm:"type:uuid" json:"team_leader_id"`
	IsActive     bool       `gorm:"default:true" json:"is_active"`

	common.Auditable

	Project *Project     `gorm:"foreignKey:ProjectID" json:"project,omitempty"`
	Members []TeamMember `gorm:"foreignKey:TeamID" json:"members,omitempty"`
}

func (ProjectTeam) TableName() string {
	return "p5_project_teams"
}

// TeamMember represents students in a project team
type TeamMember struct {
	ID        uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	TeamID    uuid.UUID `gorm:"type:uuid;not null;index" json:"team_id"`
	StudentID uuid.UUID `gorm:"type:uuid;not null;index" json:"student_id"`
	Role      string    `gorm:"type:varchar(50);default:'ANGGOTA'" json:"role"` // KETUA, ANGGOTA, PENGAMAT
	JoinedAt  string    `gorm:"type:varchar(50)" json:"joined_at"`
	IsActive  bool      `gorm:"default:true" json:"is_active"`

	common.Auditable

	Team *ProjectTeam `gorm:"foreignKey:TeamID" json:"team,omitempty"`
}

func (TeamMember) TableName() string {
	return "p5_team_members"
}

// ProjectMilestone represents project milestones/phases
type ProjectMilestone struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ProjectID      uuid.UUID `gorm:"type:uuid;not null;index" json:"project_id"`
	Title          string    `gorm:"type:varchar(200);not null" json:"title"`
	Description    string    `gorm:"type:text" json:"description"`
	Sequence       int       `gorm:"type:integer;default:1" json:"sequence"` // Order in project
	StartDate      string    `gorm:"type:varchar(50)" json:"start_date"`     // e.g., "Minggu ke-1"
	EndDate        string    `gorm:"type:varchar(50)" json:"end_date"`
	RequiredHours  float64   `gorm:"type:decimal(5,2);default:2.0" json:"required_hours"` // Hours needed
	Deliverables   string    `gorm:"type:text" json:"deliverables"`                       // Expected deliverables (JSON array)
	AssessmentType string    `gorm:"type:varchar(50)" json:"assessment_type"`             // FORMATIVE, SUMMATIVE

	Status         string  `gorm:"type:varchar(20);default:'NOT_STARTED'" json:"status"` // NOT_STARTED, IN_PROGRESS, COMPLETED, DELAYED
	CompletionDate *string `gorm:"type:varchar(50)" json:"completion_date"`

	common.Auditable

	Project *Project `gorm:"foreignKey:ProjectID" json:"project,omitempty"`
}

func (ProjectMilestone) TableName() string {
	return "p5_project_milestones"
}

// StudentParticipation tracks individual student participation in P5 projects
type StudentParticipation struct {
	ID        uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ProjectID uuid.UUID  `gorm:"type:uuid;not null;index" json:"project_id"`
	StudentID uuid.UUID  `gorm:"type:uuid;not null;index" json:"student_id"`
	TeamID    *uuid.UUID `gorm:"type:uuid;index" json:"team_id"`
	Role      string     `gorm:"type:varchar(50);default:'ANGGOTA'" json:"role"` // KETUA, ANGGOTA

	// Progress Tracking
	OverallProgress float64 `gorm:"type:decimal(5,2);default:0.0" json:"overall_progress"`     // 0-100
	EngagementLevel string  `gorm:"type:varchar(20);default:'SEDANG'" json:"engagement_level"` // TINGGI, SEDANG, RENDAH
	AttendanceRate  float64 `gorm:"type:decimal(5,2);default:0.0" json:"attendance_rate"`      // Percentage

	// Dimension Growth
	DimensionGrowth string `gorm:"type:text" json:"dimension_growth"` // JSON object with dimension progress
	ChallengesFaced string `gorm:"type:text" json:"challenges_faced"`
	SupportNeeded   string `gorm:"type:text" json:"support_needed"`

	// Final Assessment
	FinalScore      *float64 `gorm:"type:decimal(5,2)" json:"final_score"`
	Grade           *string  `gorm:"type:varchar(20)" json:"grade"` // A, B, C, etc.
	TeacherFeedback string   `gorm:"type:text" json:"teacher_feedback"`

	common.Auditable

	Project *Project `gorm:"foreignKey:ProjectID" json:"project,omitempty"`
}

func (StudentParticipation) TableName() string {
	return "p5_student_participation"
}

// Project status constants
const (
	ProjectStatusPlanning  = "PERENCANAAN"
	ProjectStatusOngoing   = "BERJALAN"
	ProjectStatusPaused    = "DIHENTIKAN"
	ProjectStatusCompleted = "SELESAI"
	ProjectStatusCancelled = "DIBATALKAN"
)

// Project type constants
const (
	ProjectTypeIndividual = "INDIVIDU"
	ProjectTypeGroup      = "KELOMPOK"
	ProjectTypeClass      = "KELAS"
)

// Milestone status constants
const (
	MilestoneStatusNotStarted = "BELUM_MULAI"
	MilestoneStatusInProgress = "SEDANG_BERJALAN"
	MilestoneStatusCompleted  = "SELESAI"
	MilestoneStatusDelayed    = "TERTUNDA"
)

// Role constants
const (
	RoleLeader   = "KETUA"
	RoleMember   = "ANGGOTA"
	RoleObserver = "PENGAMAT"
)

// GetProjectStatusDescription returns Indonesian description for project status
func GetProjectStatusDescription(status string) string {
	descriptions := map[string]string{
		ProjectStatusPlanning:  "Perencanaan",
		ProjectStatusOngoing:   "Berjalan",
		ProjectStatusPaused:    "Dihentikan",
		ProjectStatusCompleted: "Selesai",
		ProjectStatusCancelled: "Dibatalkan",
	}
	if desc, exists := descriptions[status]; exists {
		return desc
	}
	return status
}

// GetProjectTypeDescription returns Indonesian description for project type
func GetProjectTypeDescription(projectType string) string {
	descriptions := map[string]string{
		ProjectTypeIndividual: "Individu",
		ProjectTypeGroup:      "Kelompok",
		ProjectTypeClass:      "Kelas",
	}
	if desc, exists := descriptions[projectType]; exists {
		return desc
	}
	return projectType
}

// GetMilestoneStatusDescription returns Indonesian description for milestone status
func GetMilestoneStatusDescription(status string) string {
	descriptions := map[string]string{
		MilestoneStatusNotStarted: "Belum Mulai",
		MilestoneStatusInProgress: "Sedang Berjalan",
		MilestoneStatusCompleted:  "Selesai",
		MilestoneStatusDelayed:    "Tertunda",
	}
	if desc, exists := descriptions[status]; exists {
		return desc
	}
	return status
}

// GetRoleDescription returns Indonesian description for role
func GetRoleDescription(role string) string {
	descriptions := map[string]string{
		RoleLeader:   "Ketua",
		RoleMember:   "Anggota",
		RoleObserver: "Pengamat",
	}
	if desc, exists := descriptions[role]; exists {
		return desc
	}
	return role
}
