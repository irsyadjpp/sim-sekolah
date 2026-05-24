package learning_experience

import (
	"time"

	"github.com/google/uuid"
)

// Learning Experience Request/Response DTOs

// CreateLearningExperienceRequest DTO for creating learning experience
type CreateLearningExperienceRequest struct {
	ExperienceCode string `json:"experience_code" binding:"required"`
	ExperienceName string `json:"experience_name" binding:"required"`
	Description    string `json:"description" binding:"required"`
	SequenceOrder  int    `json:"sequence_order" binding:"required,min=1,max=3"`
	KeyIndicators  string `json:"key_indicators"`
}

// UpdateLearningExperienceRequest DTO for updating learning experience
type UpdateLearningExperienceRequest struct {
	ExperienceName string `json:"experience_name"`
	Description    string `json:"description"`
	SequenceOrder  int    `json:"sequence_order"`
	KeyIndicators  string `json:"key_indicators"`
	IsActive       *bool  `json:"is_active"`
}

// LearningExperienceResponse DTO for learning experience response
type LearningExperienceResponse struct {
	ID             uuid.UUID `json:"id"`
	ExperienceCode string    `json:"experience_code"`
	ExperienceName string    `json:"experience_name"`
	Description    string    `json:"description"`
	SequenceOrder  int       `json:"sequence_order"`
	KeyIndicators  string    `json:"key_indicators"`
	IsActive       bool      `json:"is_active"`
	CreatedAt      time.Time `json:"created_at"`
	UpdatedAt      time.Time `json:"updated_at"`
}

// ActivityExperienceMappingRequest DTO for linking activity to experience
type ActivityExperienceMappingRequest struct {
	ActivityID   uuid.UUID `json:"activity_id" binding:"required"`
	ExperienceID uuid.UUID `json:"experience_id" binding:"required"`
}

// ActivityExperienceMappingResponse DTO for activity-experience mapping response
type ActivityExperienceMappingResponse struct {
	ActivityID   uuid.UUID `json:"activity_id"`
	ExperienceID uuid.UUID `json:"experience_id"`
	CreatedAt    time.Time `json:"created_at"`
}

// CreateStudentProgressionRequest DTO for creating student progression
type CreateStudentProgressionRequest struct {
	StudentID    uuid.UUID `json:"student_id" binding:"required"`
	SubjectID    uuid.UUID `json:"subject_id" binding:"required"`
	ExperienceID uuid.UUID `json:"experience_id" binding:"required"`
	MasteryLevel float64   `json:"mastery_level" binding:"required,min=0,max=1"`
	Notes        string    `json:"notes"`
}

// UpdateStudentProgressionRequest DTO for updating student progression
type UpdateStudentProgressionRequest struct {
	MasteryLevel   *float64   `json:"mastery_level" binding:"omitempty,min=0,max=1"`
	Notes          *string    `json:"notes"`
	LastAssessedAt *time.Time `json:"last_assessed_at"`
}

// StudentExperienceProgressionResponse DTO for student progression response
type StudentExperienceProgressionResponse struct {
	ID             uuid.UUID  `json:"id"`
	StudentID      uuid.UUID  `json:"student_id"`
	SubjectID      uuid.UUID  `json:"subject_id"`
	ExperienceID   uuid.UUID  `json:"experience_id"`
	MasteryLevel   float64    `json:"mastery_level"`
	LastAssessedAt *time.Time `json:"last_assessed_at"`
	Notes          string     `json:"notes"`
	CreatedAt      time.Time  `json:"created_at"`
	UpdatedAt      time.Time  `json:"updated_at"`
}

// StudentProgressionDetailResponse extended response with related data
type StudentProgressionDetailResponse struct {
	ID             uuid.UUID  `json:"id"`
	StudentID      uuid.UUID  `json:"student_id"`
	StudentName    string     `json:"student_name,omitempty"`
	SubjectID      uuid.UUID  `json:"subject_id"`
	SubjectName    string     `json:"subject_name,omitempty"`
	ExperienceID   uuid.UUID  `json:"experience_id"`
	ExperienceCode string     `json:"experience_code,omitempty"`
	ExperienceName string     `json:"experience_name,omitempty"`
	MasteryLevel   float64    `json:"mastery_level"`
	LastAssessedAt *time.Time `json:"last_assessed_at"`
	Notes          string     `json:"notes"`
	CreatedAt      time.Time  `json:"created_at"`
	UpdatedAt      time.Time  `json:"updated_at"`
}

// StudentProgressionSummaryResponse for dashboard overview
type StudentProgressionSummaryResponse struct {
	StudentID       uuid.UUID                          `json:"student_id"`
	StudentName     string                             `json:"student_name,omitempty"`
	SubjectID       uuid.UUID                          `json:"subject_id"`
	SubjectName     string                             `json:"subject_name,omitempty"`
	Progressions    []StudentProgressionDetailResponse `json:"progressions"`
	AverageMastery  float64                            `json:"average_mastery"`
	ReadinessStatus string                             `json:"readiness_status"` // READY, NEEDS_IMPROVEMENT, NOT_READY
}
