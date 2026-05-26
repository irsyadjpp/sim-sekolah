package p5

import (
	"time"

	"github.com/google/uuid"
)

// CreateProjectRequest is the request body for creating a P5 project
type CreateProjectRequest struct {
	Title              string                   `json:"title" validate:"required,max=200"`
	Description        string                   `json:"description" validate:"omitempty"`
	SubjectID          string                   `json:"subject_id" validate:"omitempty,uuid"`
	ClassroomID        string                   `json:"classroom_id" validate:"omitempty,uuid"`
	ProjectTheme       string                   `json:"project_theme" validate:"required,max=100"`
	AcademicYearID     string                   `json:"academic_year_id" validate:"omitempty,uuid"`
	Semester           int                      `json:"semester" validate:"omitempty,min=1,max=2"`
	StartDate          string                   `json:"start_date" validate:"omitempty"`
	EndDate            string                   `json:"end_date" validate:"omitempty"`
	TotalWeeks         int                      `json:"total_weeks" validate:"omitempty,min=1"`
	ProjectType        string                   `json:"project_type" validate:"required,oneof=INDIVIDU KELOMPOK KELAS"`
	MaxTeamSize        int                      `json:"max_team_size" validate:"omitempty,min=1,max=10"`
	RequiredDimensions string                   `json:"required_dimensions" validate:"omitempty"`
	TeachingModuleID   string                   `json:"teaching_module_id" validate:"omitempty,uuid"`
	RubricID           string                   `json:"rubric_id" validate:"omitempty,uuid"`
	Milestones         []CreateMilestoneRequest `json:"milestones" validate:"omitempty,dive"`
}

// UpdateProjectRequest is the request body for updating a P5 project
type UpdateProjectRequest struct {
	Title              string                   `json:"title" validate:"omitempty,max=200"`
	Description        string                   `json:"description" validate:"omitempty"`
	SubjectID          string                   `json:"subject_id" validate:"omitempty,uuid"`
	ClassroomID        string                   `json:"classroom_id" validate:"omitempty,uuid"`
	ProjectTheme       string                   `json:"project_theme" validate:"omitempty,max=100"`
	AcademicYearID     string                   `json:"academic_year_id" validate:"omitempty,uuid"`
	Semester           int                      `json:"semester" validate:"omitempty,min=1,max=2"`
	StartDate          string                   `json:"start_date" validate:"omitempty"`
	EndDate            string                   `json:"end_date" validate:"omitempty"`
	TotalWeeks         int                      `json:"total_weeks" validate:"omitempty,min=1"`
	ProjectType        string                   `json:"project_type" validate:"omitempty,oneof=INDIVIDU KELOMPOK KELAS"`
	MaxTeamSize        int                      `json:"max_team_size" validate:"omitempty,min=1,max=10"`
	RequiredDimensions string                   `json:"required_dimensions" validate:"omitempty"`
	Status             string                   `json:"status" validate:"omitempty,oneof=PERENCANAAN BERJALAN DIHENTIKAN SELESAI DIBATALKAN"`
	Progress           int                      `json:"progress" validate:"omitempty,min=0,max=100"`
	TeachingModuleID   string                   `json:"teaching_module_id" validate:"omitempty,uuid"`
	RubricID           string                   `json:"rubric_id" validate:"omitempty,uuid"`
	Milestones         []CreateMilestoneRequest `json:"milestones" validate:"omitempty,dive"`
}

// CreateTeamRequest is the request body for creating a project team
type CreateTeamRequest struct {
	ProjectID    string `json:"project_id" validate:"required,uuid"`
	TeamName     string `json:"team_name" validate:"required,max=100"`
	MaxMembers   int    `json:"max_members" validate:"omitempty,min=1,max=10"`
	TeamLeaderID string `json:"team_leader_id" validate:"omitempty,uuid"`
}

// UpdateTeamRequest is the request body for updating a project team
type UpdateTeamRequest struct {
	TeamName     string `json:"team_name" validate:"omitempty,max=100"`
	MaxMembers   int    `json:"max_members" validate:"omitempty,min=1,max=10"`
	TeamLeaderID string `json:"team_leader_id" validate:"omitempty,uuid"`
	IsActive     bool   `json:"is_active"`
}

// CreateTeamMemberRequest is the request body for adding a student to a team
type CreateTeamMemberRequest struct {
	StudentID string `json:"student_id" validate:"required,uuid"`
	Role      string `json:"role" validate:"omitempty,oneof=KETUA ANGGOTA PENGAMAT"`
	JoinedAt  string `json:"joined_at" validate:"omitempty"`
}

// UpdateTeamMemberRequest is the request body for updating a team member
type UpdateTeamMemberRequest struct {
	Role     string `json:"role" validate:"omitempty,oneof=KETUA ANGGOTA PENGAMAT"`
	IsActive bool   `json:"is_active"`
}

// CreateMilestoneRequest is the request body for creating a project milestone
type CreateMilestoneRequest struct {
	Title          string  `json:"title" validate:"required,max=200"`
	Description    string  `json:"description" validate:"omitempty"`
	Sequence       int     `json:"sequence" validate:"omitempty,min=1"`
	StartDate      string  `json:"start_date" validate:"omitempty"`
	EndDate        string  `json:"end_date" validate:"omitempty"`
	RequiredHours  float64 `json:"required_hours" validate:"omitempty,min=0"`
	Deliverables   string  `json:"deliverables" validate:"omitempty"`
	AssessmentType string  `json:"assessment_type" validate:"omitempty,oneof=FORMATIF SUMATIF"`
}

// UpdateMilestoneRequest is the request body for updating a project milestone
type UpdateMilestoneRequest struct {
	Title          string  `json:"title" validate:"omitempty,max=200"`
	Description    string  `json:"description" validate:"omitempty"`
	Sequence       int     `json:"sequence" validate:"omitempty,min=1"`
	StartDate      string  `json:"start_date" validate:"omitempty"`
	EndDate        string  `json:"end_date" validate:"omitempty"`
	RequiredHours  float64 `json:"required_hours" validate:"omitempty,min=0"`
	Deliverables   string  `json:"deliverables" validate:"omitempty"`
	AssessmentType string  `json:"assessment_type" validate:"omitempty,oneof=FORMATIF SUMATIF"`
	Status         string  `json:"status" validate:"omitempty,oneof=BELUM_MULAI SEDANG_BERJALAN SELESAI TERTUNDA"`
	CompletionDate *string `json:"completion_date" validate:"omitempty"`
}

// CreateParticipationRequest is the request body for creating student participation
type CreateParticipationRequest struct {
	ProjectID       string  `json:"project_id" validate:"required,uuid"`
	StudentID       string  `json:"student_id" validate:"required,uuid"`
	TeamID          string  `json:"team_id" validate:"omitempty,uuid"`
	Role            string  `json:"role" validate:"omitempty,oneof=KETUA ANGGOTA"`
	OverallProgress float64 `json:"overall_progress" validate:"omitempty,min=0,max=100"`
	EngagementLevel string  `json:"engagement_level" validate:"omitempty,oneof=TINGGI SEDANG RENDAH"`
	AttendanceRate  float64 `json:"attendance_rate" validate:"omitempty,min=0,max=100"`
}

// UpdateParticipationRequest is the request body for updating student participation
type UpdateParticipationRequest struct {
	OverallProgress float64  `json:"overall_progress" validate:"omitempty,min=0,max=100"`
	EngagementLevel string   `json:"engagement_level" validate:"omitempty,oneof=TINGGI SEDANG RENDAH"`
	AttendanceRate  float64  `json:"attendance_rate" validate:"omitempty,min=0,max=100"`
	DimensionGrowth string   `json:"dimension_growth" validate:"omitempty"`
	ChallengesFaced string   `json:"challenges_faced" validate:"omitempty"`
	SupportNeeded   string   `json:"support_needed" validate:"omitempty"`
	FinalScore      *float64 `json:"final_score" validate:"omitempty,min=0,max=100"`
	Grade           *string  `json:"grade" validate:"omitempty"`
	TeacherFeedback string   `json:"teacher_feedback" validate:"omitempty"`
}

// ProjectResponse represents the response for project operations
type ProjectResponse struct {
	ID                 uuid.UUID               `json:"id"`
	Title              string                  `json:"title"`
	Description        string                  `json:"description"`
	SubjectID          *uuid.UUID              `json:"subject_id"`
	SubjectName        *string                 `json:"subject_name,omitempty"`
	ClassroomID        *uuid.UUID              `json:"classroom_id"`
	ProjectTheme       string                  `json:"project_theme"`
	AcademicYearID     *uuid.UUID              `json:"academic_year_id"`
	Semester           int                     `json:"semester"`
	StartDate          string                  `json:"start_date"`
	EndDate            string                  `json:"end_date"`
	TotalWeeks         int                     `json:"total_weeks"`
	ProjectType        string                  `json:"project_type"`
	ProjectTypeName    string                  `json:"project_type_name"`
	MaxTeamSize        int                     `json:"max_team_size"`
	RequiredDimensions string                  `json:"required_dimensions"`
	Status             string                  `json:"status"`
	StatusName         string                  `json:"status_name"`
	Progress           int                     `json:"progress"`
	TeachingModuleID   *uuid.UUID              `json:"teaching_module_id"`
	RubricID           *uuid.UUID              `json:"rubric_id"`
	Teams              []TeamResponse          `json:"teams,omitempty"`
	Milestones         []MilestoneResponse     `json:"milestones,omitempty"`
	Participations     []ParticipationResponse `json:"participations,omitempty"`
	CreatedAt          time.Time               `json:"created_at"`
	UpdatedAt          time.Time               `json:"updated_at"`
}

// TeamResponse represents the response for team operations
type TeamResponse struct {
	ID           uuid.UUID            `json:"id"`
	ProjectID    uuid.UUID            `json:"project_id"`
	TeamName     string               `json:"team_name"`
	TeamCode     string               `json:"team_code"`
	MaxMembers   int                  `json:"max_members"`
	CurrentSize  int                  `json:"current_size"`
	TeamLeaderID *uuid.UUID           `json:"team_leader_id"`
	IsActive     bool                 `json:"is_active"`
	Members      []TeamMemberResponse `json:"members,omitempty"`
	CreatedAt    time.Time            `json:"created_at"`
	UpdatedAt    time.Time            `json:"updated_at"`
}

// TeamMemberResponse represents the response for team member operations
type TeamMemberResponse struct {
	ID        uuid.UUID `json:"id"`
	TeamID    uuid.UUID `json:"team_id"`
	StudentID uuid.UUID `json:"student_id"`
	Role      string    `json:"role"`
	RoleName  string    `json:"role_name"`
	JoinedAt  string    `json:"joined_at"`
	IsActive  bool      `json:"is_active"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// MilestoneResponse represents the response for milestone operations
type MilestoneResponse struct {
	ID             uuid.UUID `json:"id"`
	ProjectID      uuid.UUID `json:"project_id"`
	Title          string    `json:"title"`
	Description    string    `json:"description"`
	Sequence       int       `json:"sequence"`
	StartDate      string    `json:"start_date"`
	EndDate        string    `json:"end_date"`
	RequiredHours  float64   `json:"required_hours"`
	Deliverables   string    `json:"deliverables"`
	AssessmentType string    `json:"assessment_type"`
	Status         string    `json:"status"`
	StatusName     string    `json:"status_name"`
	CompletionDate *string   `json:"completion_date"`
	CreatedAt      time.Time `json:"created_at"`
	UpdatedAt      time.Time `json:"updated_at"`
}

// ParticipationResponse represents the response for participation operations
type ParticipationResponse struct {
	ID              uuid.UUID  `json:"id"`
	ProjectID       uuid.UUID  `json:"project_id"`
	StudentID       uuid.UUID  `json:"student_id"`
	TeamID          *uuid.UUID `json:"team_id"`
	Role            string     `json:"role"`
	RoleName        string     `json:"role_name"`
	OverallProgress float64    `json:"overall_progress"`
	EngagementLevel string     `json:"engagement_level"`
	AttendanceRate  float64    `json:"attendance_rate"`
	DimensionGrowth string     `json:"dimension_growth"`
	ChallengesFaced string     `json:"challenges_faced"`
	SupportNeeded   string     `json:"support_needed"`
	FinalScore      *float64   `json:"final_score"`
	Grade           *string    `json:"grade"`
	TeacherFeedback string     `json:"teacher_feedback"`
	CreatedAt       time.Time  `json:"created_at"`
	UpdatedAt       time.Time  `json:"updated_at"`
}

// ProjectListResponse represents response for project list
type ProjectListResponse struct {
	TotalCount int               `json:"total_count"`
	Items      []ProjectResponse `json:"items"`
}

// TeamListResponse represents response for team list
type TeamListResponse struct {
	TotalCount int            `json:"total_count"`
	Items      []TeamResponse `json:"items"`
}

// MilestoneListResponse represents response for milestone list
type MilestoneListResponse struct {
	TotalCount int                 `json:"total_count"`
	Items      []MilestoneResponse `json:"items"`
}

// ParticipationListResponse represents response for participation list
type ParticipationListResponse struct {
	TotalCount int                     `json:"total_count"`
	Items      []ParticipationResponse `json:"items"`
}

// ProjectProgressResponse represents response for project progress
type ProjectProgressResponse struct {
	ProjectID           uuid.UUID `json:"project_id"`
	OverallProgress     int       `json:"overall_progress"`
	TeamCount           int       `json:"team_count"`
	TotalStudents       int       `json:"total_students"`
	CompletedMilestones int       `json:"completed_milestones"`
	TotalMilestones     int       `json:"total_milestones"`
}

// AutoGenerateTeamsRequest is the request body for auto-generating teams
type AutoGenerateTeamsRequest struct {
	ProjectID     string `json:"project_id" validate:"required,uuid"`
	TeamSize      int    `json:"team_size" validate:"required,min=1,max=10"`
	BalancingMode string `json:"balancing_mode" validate:"required,oneof=RANDOM BALANCED_MIXED"` // RANDOM = random assignment, BALANCED = balance by performance, MIXED = combination
}
