package differentiated_instruction

import (
	"time"

	"github.com/google/uuid"
)

// DIStrategy Request/Response DTOs

// CreateDIStrategyRequest DTO for creating DI strategy
type CreateDIStrategyRequest struct {
	StrategyCode  string `json:"strategy_code" binding:"required"`
	StrategyName  string `json:"strategy_name" binding:"required"`
	Description   string `json:"description" binding:"required"`
	Applicability string `json:"applicability"`
	Examples      string `json:"examples"`
	TargetGroup   string `json:"target_group"`
}

// UpdateDIStrategyRequest DTO for updating DI strategy
type UpdateDIStrategyRequest struct {
	StrategyName  *string `json:"strategy_name"`
	Description   *string `json:"description"`
	Applicability *string `json:"applicability"`
	Examples      *string `json:"examples"`
	TargetGroup   *string `json:"target_group"`
	IsActive      *bool   `json:"is_active"`
}

// DIStrategyResponse DTO for DI strategy response
type DIStrategyResponse struct {
	ID            uuid.UUID `json:"id"`
	StrategyCode  string    `json:"strategy_code"`
	StrategyName  string    `json:"strategy_name"`
	Description   string    `json:"description"`
	Applicability string    `json:"applicability"`
	Examples      string    `json:"examples"`
	TargetGroup   string    `json:"target_group"`
	IsActive      bool      `json:"is_active"`
	CreatedAt     time.Time `json:"created_at"`
	UpdatedAt     time.Time `json:"updated_at"`
}

// ModuleDifferentiation Request/Response DTOs

// CreateModuleDifferentiationRequest DTO for creating module differentiation
type CreateModuleDifferentiationRequest struct {
	ModuleID       uuid.UUID `json:"module_id" binding:"required"`
	StrategyID     uuid.UUID `json:"strategy_id" binding:"required"`
	TargetStudents string    `json:"target_students"`
	Modifications  string    `json:"modifications"`
	Resources      string    `json:"resources"`
	AssessmentType string    `json:"assessment_type"`
	Notes          string    `json:"notes"`
}

// UpdateModuleDifferentiationRequest DTO for updating module differentiation
type UpdateModuleDifferentiationRequest struct {
	StrategyID     *string `json:"strategy_id"`
	TargetStudents *string `json:"target_students"`
	Modifications  *string `json:"modifications"`
	Resources      *string `json:"resources"`
	AssessmentType *string `json:"assessment_type"`
	Notes          *string `json:"notes"`
}

// ModuleDifferentiationResponse DTO for module differentiation response
type ModuleDifferentiationResponse struct {
	ID             uuid.UUID           `json:"id"`
	ModuleID       uuid.UUID           `json:"module_id"`
	StrategyID     uuid.UUID           `json:"strategy_id"`
	TargetStudents string              `json:"target_students"`
	Modifications  string              `json:"modifications"`
	Resources      string              `json:"resources"`
	AssessmentType string              `json:"assessment_type"`
	Notes          string              `json:"notes"`
	CreatedAt      time.Time           `json:"created_at"`
	UpdatedAt      time.Time           `json:"updated_at"`
	Strategy       *DIStrategyResponse `json:"strategy,omitempty"`
}

// ModuleDifferentiationDetailResponse extended response with strategy details
type ModuleDifferentiationDetailResponse struct {
	ID                  uuid.UUID `json:"id"`
	ModuleID            uuid.UUID `json:"module_id"`
	StrategyID          uuid.UUID `json:"strategy_id"`
	StrategyName        string    `json:"strategy_name,omitempty"`
	StrategyCode        string    `json:"strategy_code,omitempty"`
	StrategyDescription string    `json:"strategy_description,omitempty"`
	TargetStudents      string    `json:"target_students"`
	Modifications       string    `json:"modifications"`
	Resources           string    `json:"resources"`
	AssessmentType      string    `json:"assessment_type"`
	Notes               string    `json:"notes"`
	CreatedAt           time.Time `json:"created_at"`
	UpdatedAt           time.Time `json:"updated_at"`
}

// StudentDINeed Request/Response DTOs

// CreateStudentDINeedRequest DTO for creating student DI need
type CreateStudentDINeedRequest struct {
	StudentID             uuid.UUID `json:"student_id" binding:"required"`
	SubjectID             uuid.UUID `json:"subject_id"`
	NeedType              string    `json:"need_type" binding:"required"`
	Severity              string    `json:"severity" binding:"required"`
	Description           string    `json:"description"`
	RecommendedStrategies string    `json:"recommended_strategies"`
	AssessmentDate        string    `json:"assessment_date" binding:"required"`
}

// UpdateStudentDINeedRequest DTO for updating student DI need
type UpdateStudentDINeedRequest struct {
	SubjectID             *uuid.UUID `json:"subject_id"`
	NeedType              *string    `json:"need_type"`
	Severity              *string    `json:"severity"`
	Description           *string    `json:"description"`
	RecommendedStrategies *string    `json:"recommended_strategies"`
	IsActive              *bool      `json:"is_active"`
}

// StudentDINeedResponse DTO for student DI need response
type StudentDINeedResponse struct {
	ID                    uuid.UUID `json:"id"`
	StudentID             uuid.UUID `json:"student_id"`
	SubjectID             uuid.UUID `json:"subject_id"`
	NeedType              string    `json:"need_type"`
	Severity              string    `json:"severity"`
	Description           string    `json:"description"`
	RecommendedStrategies string    `json:"recommended_strategies"`
	AssessmentDate        time.Time `json:"assessment_date"`
	IsActive              bool      `json:"is_active"`
	CreatedAt             time.Time `json:"created_at"`
	UpdatedAt             time.Time `json:"updated_at"`
}

// StudentDINeedSummaryResponse for student DI needs overview
type StudentDINeedSummaryResponse struct {
	StudentID       uuid.UUID               `json:"student_id"`
	TotalNeeds      int                     `json:"total_needs"`
	ActiveNeeds     int                     `json:"active_needs"`
	NeedsByType     map[string]int          `json:"needs_by_type"`
	NeedsBySeverity map[string]int          `json:"needs_by_severity"`
	RecentNeeds     []StudentDINeedResponse `json:"recent_needs,omitempty"`
}

// ModuleDISummaryResponse for module DI overview
type ModuleDISummaryResponse struct {
	ModuleID              uuid.UUID                       `json:"module_id"`
	TotalDifferentiations int                             `json:"total_differentiations"`
	StrategiesUsed        []DIStrategyResponse            `json:"strategies_used,omitempty"`
	StudentsCovered       int                             `json:"students_covered"`
	Differentiations      []ModuleDifferentiationResponse `json:"differentiations,omitempty"`
}
