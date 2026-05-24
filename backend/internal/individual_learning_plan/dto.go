package individual_learning_plan

import (
	"time"

	"github.com/google/uuid"
)

// ILP Request/Response DTOs

// CreateILPRequest DTO for creating individual learning plan
type CreateILPRequest struct {
	StudentID      uuid.UUID `json:"student_id" binding:"required"`
	AcademicYearID uuid.UUID `json:"academic_year_id" binding:"required"`
	Title          string    `json:"title" binding:"required"`
	Goals          string    `json:"goals"`
	Strategies     string    `json:"strategies"`
	Accommodations string    `json:"accommodations"`
	ParentNotes    string    `json:"parent_notes"`
	TeacherNotes   string    `json:"teacher_notes"`
}

// UpdateILPRequest DTO for updating individual learning plan
type UpdateILPRequest struct {
	Title          *string `json:"title"`
	Goals          *string `json:"goals"`
	Strategies     *string `json:"strategies"`
	Accommodations *string `json:"accommodations"`
	ParentNotes    *string `json:"parent_notes"`
	TeacherNotes   *string `json:"teacher_notes"`
	Status         *string `json:"status"`
}

// ILPResponse DTO for individual learning plan response
type ILPResponse struct {
	ID             uuid.UUID `json:"id"`
	StudentID      uuid.UUID `json:"student_id"`
	AcademicYearID uuid.UUID `json:"academic_year_id"`
	Title          string    `json:"title"`
	Goals          string    `json:"goals"`
	Strategies     string    `json:"strategies"`
	Accommodations string    `json:"accommodations"`
	ParentNotes    string    `json:"parent_notes"`
	TeacherNotes   string    `json:"teacher_notes"`
	Status         string    `json:"status"`
	CreatedAt      time.Time `json:"created_at"`
	UpdatedAt      time.Time `json:"updated_at"`
}

// CreateMilestoneRequest DTO for creating ILP milestone
type CreateMilestoneRequest struct {
	ILPID         uuid.UUID `json:"ilp_id" binding:"required"`
	MilestoneName string    `json:"milestone_name" binding:"required"`
	TargetDate    string    `json:"target_date" binding:"required"`
	Notes         string    `json:"notes"`
}

// UpdateMilestoneRequest DTO for updating ILP milestone
type UpdateMilestoneRequest struct {
	MilestoneName *string `json:"milestone_name"`
	TargetDate    *string `json:"target_date"`
	Achieved      *bool   `json:"achieved"`
	Notes         *string `json:"notes"`
}

// MilestoneResponse DTO for milestone response
type MilestoneResponse struct {
	ID            uuid.UUID  `json:"id"`
	ILPID         uuid.UUID  `json:"ilp_id"`
	MilestoneName string     `json:"milestone_name"`
	TargetDate    time.Time  `json:"target_date"`
	Achieved      bool       `json:"achieved"`
	AchievedDate  *time.Time `json:"achieved_date,omitempty"`
	Notes         string     `json:"notes"`
	CreatedAt     time.Time  `json:"created_at"`
	UpdatedAt     time.Time  `json:"updated_at"`
}

// ILPTemplateResponse DTO for ILP template response
type ILPTemplateResponse struct {
	ID                uuid.UUID `json:"id"`
	TemplateCode      string    `json:"template_code"`
	TemplateName      string    `json:"template_name"`
	PhaseID           uuid.UUID `json:"phase_id"`
	Description       string    `json:"description"`
	DefaultGoals      string    `json:"default_goals"`
	DefaultStrategies string    `json:"default_strategies"`
	IsActive          bool      `json:"is_active"`
	CreatedAt         time.Time `json:"created_at"`
	UpdatedAt         time.Time `json:"updated_at"`
}

// ILPDetailResponse extended response with related data
type ILPDetailResponse struct {
	ID             uuid.UUID           `json:"id"`
	StudentID      uuid.UUID           `json:"student_id"`
	StudentName    string              `json:"student_name,omitempty"`
	AcademicYearID uuid.UUID           `json:"academic_year_id"`
	AcademicYear   string              `json:"academic_year,omitempty"`
	Title          string              `json:"title"`
	Goals          string              `json:"goals"`
	Strategies     string              `json:"strategies"`
	Accommodations string              `json:"accommodations"`
	ParentNotes    string              `json:"parent_notes"`
	TeacherNotes   string              `json:"teacher_notes"`
	Status         string              `json:"status"`
	CreatedAt      time.Time           `json:"created_at"`
	UpdatedAt      time.Time           `json:"updated_at"`
	Milestones     []MilestoneResponse `json:"milestones,omitempty"`
}

// ILPSummaryResponse for dashboard overview
type ILPSummaryResponse struct {
	TotalILPs      int            `json:"total_ilps"`
	ActiveILPs     int            `json:"active_ilps"`
	CompletedILPs  int            `json:"completed_ilps"`
	RecentILPs     []ILPResponse  `json:"recent_ilps,omitempty"`
	MilestoneStats map[string]int `json:"milestone_stats"`
}
