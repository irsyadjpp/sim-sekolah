package learning

import (
	"time"

	"github.com/google/uuid"
)

// CreateATPRequest is the request body for creating ATP
type CreateATPRequest struct {
	ClassroomID    string                   `json:"classroom_id" validate:"required,uuid"`
	SubjectID      string                   `json:"subject_id" validate:"required,uuid"`
	Title          string                   `json:"title" validate:"required,max=200"`
	AcademicYearID string                   `json:"academic_year_id" validate:"omitempty,uuid"`
	Semester       int                      `json:"semester" validate:"omitempty,min=1,max=2"`
	TotalMeetings  int                      `json:"total_meetings" validate:"omitempty,min=0"`
	TotalHours     float64                  `json:"total_hours" validate:"omitempty,min=0"`
	Status         string                   `json:"status" validate:"omitempty,oneof=DRAFT APPROVED PUBLISHED"`
	Details        []CreateATPDetailRequest `json:"details" validate:"omitempty,dive"`
}

// UpdateATPRequest is the request body for updating ATP
type UpdateATPRequest struct {
	ClassroomID    string                   `json:"classroom_id" validate:"omitempty,uuid"`
	SubjectID      string                   `json:"subject_id" validate:"omitempty,uuid"`
	Title          string                   `json:"title" validate:"omitempty,max=200"`
	AcademicYearID string                   `json:"academic_year_id" validate:"omitempty,uuid"`
	Semester       int                      `json:"semester" validate:"omitempty,min=1,max=2"`
	TotalMeetings  int                      `json:"total_meetings" validate:"omitempty,min=0"`
	TotalHours     float64                  `json:"total_hours" validate:"omitempty,min=0"`
	Status         string                   `json:"status" validate:"omitempty,oneof=DRAFT APPROVED PUBLISHED"`
	Details        []CreateATPDetailRequest `json:"details" validate:"omitempty,dive"`
}

// CreateATPDetailRequest is the request body for creating ATP detail
type CreateATPDetailRequest struct {
	ObjectiveID    string  `json:"objective_id" validate:"required,uuid"`
	Sequence       int     `json:"sequence" validate:"required,min=1"`
	MeetingNumber  int     `json:"meeting_number" validate:"omitempty,min=0"`
	EstimatedHours float64 `json:"estimated_hours" validate:"omitempty,min=0"`
	LearningFlow   string  `json:"learning_flow" validate:"omitempty,oneof=INTRODUCTORY DEVELOPMENT PRACTICE ASSESSMENT REINFORCEMENT"`
}

// UpdateATPDetailRequest is the request body for updating ATP detail
type UpdateATPDetailRequest struct {
	ObjectiveID    string  `json:"objective_id" validate:"omitempty,uuid"`
	Sequence       int     `json:"sequence" validate:"omitempty,min=1"`
	MeetingNumber  int     `json:"meeting_number" validate:"omitempty,min=0"`
	EstimatedHours float64 `json:"estimated_hours" validate:"omitempty,min=0"`
	LearningFlow   string  `json:"learning_flow" validate:"omitempty,oneof=INTRODUCTORY DEVELOPMENT PRACTICE ASSESSMENT REINFORCEMENT"`
}

// ATPResponse represents the response for ATP operations
type ATPResponse struct {
	ID             uuid.UUID           `json:"id"`
	ClassroomID    uuid.UUID           `json:"classroom_id"`
	SubjectID      uuid.UUID           `json:"subject_id"`
	Title          string              `json:"title"`
	AcademicYearID *uuid.UUID          `json:"academic_year_id"`
	Semester       int                 `json:"semester"`
	TotalMeetings  int                 `json:"total_meetings"`
	TotalHours     float64             `json:"total_hours"`
	Status         string              `json:"status"`
	StatusName     string              `json:"status_name"`
	Version        int                 `json:"version"`
	Details        []ATPDetailResponse `json:"details"`
	CreatedAt      time.Time           `json:"created_at"`
	UpdatedAt      time.Time           `json:"updated_at"`
}

// ATPDetailResponse represents the response for ATP detail operations
type ATPDetailResponse struct {
	ATPID            uuid.UUID `json:"atp_id"`
	ObjectiveID      uuid.UUID `json:"objective_id"`
	Sequence         int       `json:"sequence"`
	MeetingNumber    int       `json:"meeting_number"`
	EstimatedHours   float64   `json:"estimated_hours"`
	LearningFlow     string    `json:"learning_flow"`
	LearningFlowName string    `json:"learning_flow_name"`
}
