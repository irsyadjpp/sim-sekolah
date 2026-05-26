package rubric

import (
	"time"

	"github.com/google/uuid"
)

// CreateRubricRequest is the request body for creating a rubric
type CreateRubricRequest struct {
	Title          string                        `json:"title" validate:"required,max=200"`
	Description    string                        `json:"description" validate:"omitempty"`
	SubjectID      string                        `json:"subject_id" validate:"omitempty,uuid"`
	AssessmentType string                        `json:"assessment_type" validate:"required,oneof=PROJECT PRESENTATION WRITTEN_WORK PRACTICAL BEHAVIORAL ORAL OBSERVATION"`
	GradeLevel     string                        `json:"grade_level" validate:"omitempty"`
	MaxScore       float64                       `json:"max_score" validate:"omitempty,min=0"`
	IsTemplate     bool                          `json:"is_template"`
	Criteria       []CreateRubricCriteriaRequest `json:"criteria" validate:"omitempty,dive"`
	Levels         []CreateRubricLevelRequest    `json:"levels" validate:"omitempty,dive"`
}

// UpdateRubricRequest is the request body for updating a rubric
type UpdateRubricRequest struct {
	Title          string                        `json:"title" validate:"omitempty,max=200"`
	Description    string                        `json:"description" validate:"omitempty"`
	SubjectID      string                        `json:"subject_id" validate:"omitempty,uuid"`
	AssessmentType string                        `json:"assessment_type" validate:"omitempty,oneof=PROJECT PRESENTATION WRITTEN_WORK PRACTICAL BEHAVIORAL ORAL OBSERVATION"`
	GradeLevel     string                        `json:"grade_level" validate:"omitempty"`
	MaxScore       float64                       `json:"max_score" validate:"omitempty,min=0"`
	IsTemplate     bool                          `json:"is_template"`
	IsActive       bool                          `json:"is_active"`
	Criteria       []CreateRubricCriteriaRequest `json:"criteria" validate:"omitempty,dive"`
	Levels         []CreateRubricLevelRequest    `json:"levels" validate:"omitempty,dive"`
}

// CreateRubricCriteriaRequest is the request body for creating rubric criteria
type CreateRubricCriteriaRequest struct {
	Title       string                             `json:"title" validate:"required,max=200"`
	Description string                             `json:"description" validate:"omitempty"`
	Weight      float64                            `json:"weight" validate:"omitempty,min=0"`
	Sequence    int                                `json:"sequence" validate:"omitempty,min=1"`
	IsRequired  bool                               `json:"is_required"`
	Levels      []CreateRubricCriteriaLevelRequest `json:"levels" validate:"omitempty,dive"`
}

// UpdateRubricCriteriaRequest is the request body for updating rubric criteria
type UpdateRubricCriteriaRequest struct {
	Title       string                             `json:"title" validate:"omitempty,max=200"`
	Description string                             `json:"description" validate:"omitempty"`
	Weight      float64                            `json:"weight" validate:"omitempty,min=0"`
	Sequence    int                                `json:"sequence" validate:"omitempty,min=1"`
	IsRequired  bool                               `json:"is_required"`
	Levels      []CreateRubricCriteriaLevelRequest `json:"levels" validate:"omitempty,dive"`
}

// CreateRubricLevelRequest is the request body for creating rubric levels
type CreateRubricLevelRequest struct {
	LevelCode     string  `json:"level_code" validate:"required,max=20"`
	LevelName     string  `json:"level_name" validate:"required,max=100"`
	PointValue    float64 `json:"point_value" validate:"required,min=0"`
	MinPercentage float64 `json:"min_percentage" validate:"omitempty,min=0,max=100"`
	MaxPercentage float64 `json:"max_percentage" validate:"omitempty,min=0,max=100"`
	Sequence      int     `json:"sequence" validate:"omitempty,min=1"`
	Color         string  `json:"color" validate:"omitempty,max=20"`
}

// UpdateRubricLevelRequest is the request body for updating rubric levels
type UpdateRubricLevelRequest struct {
	LevelCode     string  `json:"level_code" validate:"omitempty,max=20"`
	LevelName     string  `json:"level_name" validate:"omitempty,max=100"`
	PointValue    float64 `json:"point_value" validate:"omitempty,min=0"`
	MinPercentage float64 `json:"min_percentage" validate:"omitempty,min=0,max=100"`
	MaxPercentage float64 `json:"max_percentage" validate:"omitempty,min=0,max=100"`
	Sequence      int     `json:"sequence" validate:"omitempty,min=1"`
	Color         string  `json:"color" validate:"omitempty,max=20"`
}

// CreateRubricCriteriaLevelRequest is the request body for creating criteria level descriptions
type CreateRubricCriteriaLevelRequest struct {
	LevelID     string `json:"level_id" validate:"required,uuid"`
	Description string `json:"description" validate:"required"`
	Examples    string `json:"examples" validate:"omitempty"`
}

// UpdateRubricCriteriaLevelRequest is the request body for updating criteria level descriptions
type UpdateRubricCriteriaLevelRequest struct {
	LevelID     string `json:"level_id" validate:"omitempty,uuid"`
	Description string `json:"description" validate:"omitempty"`
	Examples    string `json:"examples" validate:"omitempty"`
}

// RubricResponse represents the response for rubric operations
type RubricResponse struct {
	ID                 uuid.UUID                `json:"id"`
	Title              string                   `json:"title"`
	Description        string                   `json:"description"`
	SubjectID          *uuid.UUID               `json:"subject_id"`
	SubjectName        *string                  `json:"subject_name,omitempty"`
	AssessmentType     string                   `json:"assessment_type"`
	AssessmentTypeName string                   `json:"assessment_type_name"`
	GradeLevel         string                   `json:"grade_level"`
	MaxScore           float64                  `json:"max_score"`
	IsTemplate         bool                     `json:"is_template"`
	IsActive           bool                     `json:"is_active"`
	Criteria           []RubricCriteriaResponse `json:"criteria,omitempty"`
	Levels             []RubricLevelResponse    `json:"levels,omitempty"`
	CreatedAt          time.Time                `json:"created_at"`
	UpdatedAt          time.Time                `json:"updated_at"`
}

// RubricCriteriaResponse represents the response for rubric criteria operations
type RubricCriteriaResponse struct {
	ID          uuid.UUID                     `json:"id"`
	RubricID    uuid.UUID                     `json:"rubric_id"`
	Title       string                        `json:"title"`
	Description string                        `json:"description"`
	Weight      float64                       `json:"weight"`
	Sequence    int                           `json:"sequence"`
	IsRequired  bool                          `json:"is_required"`
	Levels      []RubricCriteriaLevelResponse `json:"levels,omitempty"`
	CreatedAt   time.Time                     `json:"created_at"`
	UpdatedAt   time.Time                     `json:"updated_at"`
}

// RubricLevelResponse represents the response for rubric level operations
type RubricLevelResponse struct {
	ID            uuid.UUID `json:"id"`
	RubricID      uuid.UUID `json:"rubric_id"`
	LevelCode     string    `json:"level_code"`
	LevelName     string    `json:"level_name"`
	PointValue    float64   `json:"point_value"`
	MinPercentage float64   `json:"min_percentage"`
	MaxPercentage float64   `json:"max_percentage"`
	Sequence      int       `json:"sequence"`
	Color         string    `json:"color"`
	CreatedAt     time.Time `json:"created_at"`
	UpdatedAt     time.Time `json:"updated_at"`
}

// RubricCriteriaLevelResponse represents the response for criteria level operations
type RubricCriteriaLevelResponse struct {
	ID          uuid.UUID `json:"id"`
	CriteriaID  uuid.UUID `json:"criteria_id"`
	LevelID     uuid.UUID `json:"level_id"`
	LevelCode   string    `json:"level_code,omitempty"`
	LevelName   string    `json:"level_name,omitempty"`
	Description string    `json:"description"`
	Examples    string    `json:"examples"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// RubricListResponse represents response for rubric list with pagination
type RubricListResponse struct {
	TotalCount int              `json:"total_count"`
	Items      []RubricResponse `json:"items"`
}

// RubricCopyRequest is the request body for copying a rubric
type RubricCopyRequest struct {
	NewTitle string `json:"new_title" validate:"required,max=200"`
}
