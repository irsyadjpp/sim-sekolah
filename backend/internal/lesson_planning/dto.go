package lesson_planning

import (
	"time"

	"github.com/google/uuid"
)

// CreateLessonPlanRequest is the request body for creating a lesson plan
type CreateLessonPlanRequest struct {
	Title              string                            `json:"title" validate:"required,max=200"`
	SubjectID          string                            `json:"subject_id" validate:"omitempty,uuid"`
	ClassroomID        string                            `json:"classroom_id" validate:"omitempty,uuid"`
	ATPID              string                            `json:"atp_id" validate:"omitempty,uuid"`
	TeachingModuleID   string                            `json:"teaching_module_id" validate:"omitempty,uuid"`
	TemplateID         string                            `json:"template_id" validate:"omitempty,uuid"`
	MeetingDate        string                            `json:"meeting_date" validate:"omitempty"`
	MeetingNumber      int                               `json:"meeting_number" validate:"omitempty,min=1"`
	DurationMinutes    int                               `json:"duration_minutes" validate:"omitempty,min=1"`
	LearningObjectives string                            `json:"learning_objectives" validate:"omitempty"`
	CoreMaterial       string                            `json:"core_material" validate:"omitempty"`
	TeachingMethods    string                            `json:"teaching_methods" validate:"omitempty"`
	AssessmentMethods  string                            `json:"assessment_methods" validate:"omitempty"`
	Status             string                            `json:"status" validate:"omitempty,oneof=DRAFT REVIEW APPROVED PUBLISHED"`
	AcademicYearID     string                            `json:"academic_year_id" validate:"omitempty,uuid"`
	Semester           int                               `json:"semester" validate:"omitempty,min=1,max=2"`
	Sections           []CreateLessonPlanSectionRequest  `json:"sections" validate:"omitempty,dive"`
	Resources          []CreateLessonPlanResourceRequest `json:"resources" validate:"omitempty,dive"`
}

// UpdateLessonPlanRequest is the request body for updating a lesson plan
type UpdateLessonPlanRequest struct {
	Title              string                            `json:"title" validate:"omitempty,max=200"`
	SubjectID          string                            `json:"subject_id" validate:"omitempty,uuid"`
	ClassroomID        string                            `json:"classroom_id" validate:"omitempty,uuid"`
	ATPID              string                            `json:"atp_id" validate:"omitempty,uuid"`
	TeachingModuleID   string                            `json:"teaching_module_id" validate:"omitempty,uuid"`
	MeetingDate        string                            `json:"meeting_date" validate:"omitempty"`
	MeetingNumber      int                               `json:"meeting_number" validate:"omitempty,min=1"`
	DurationMinutes    int                               `json:"duration_minutes" validate:"omitempty,min=1"`
	LearningObjectives string                            `json:"learning_objectives" validate:"omitempty"`
	CoreMaterial       string                            `json:"core_material" validate:"omitempty"`
	TeachingMethods    string                            `json:"teaching_methods" validate:"omitempty"`
	AssessmentMethods  string                            `json:"assessment_methods" validate:"omitempty"`
	Status             string                            `json:"status" validate:"omitempty,oneof=DRAFT REVIEW APPROVED PUBLISHED"`
	AcademicYearID     string                            `json:"academic_year_id" validate:"omitempty,uuid"`
	Semester           int                               `json:"semester" validate:"omitempty,min=1,max=2"`
	Sections           []CreateLessonPlanSectionRequest  `json:"sections" validate:"omitempty,dive"`
	Resources          []CreateLessonPlanResourceRequest `json:"resources" validate:"omitempty,dive"`
}

// CreateLessonPlanTemplateRequest is the request body for creating a lesson plan template
type CreateLessonPlanTemplateRequest struct {
	Title                  string `json:"title" validate:"required,max=200"`
	Description            string `json:"description" validate:"omitempty"`
	SubjectID              string `json:"subject_id" validate:"omitempty,uuid"`
	GradeLevel             string `json:"grade_level" validate:"omitempty"`
	Category               string `json:"category" validate:"omitempty,max=100"`
	DefaultDurationMinutes int    `json:"default_duration_minutes" validate:"omitempty,min=1"`
	DefaultSections        string `json:"default_sections" validate:"omitempty"`
	IsActive               bool   `json:"is_active"`
}

// UpdateLessonPlanTemplateRequest is the request body for updating a lesson plan template
type UpdateLessonPlanTemplateRequest struct {
	Title                  string `json:"title" validate:"omitempty,max=200"`
	Description            string `json:"description" validate:"omitempty"`
	SubjectID              string `json:"subject_id" validate:"omitempty,uuid"`
	GradeLevel             string `json:"grade_level" validate:"omitempty"`
	Category               string `json:"category" validate:"omitempty,max=100"`
	DefaultDurationMinutes int    `json:"default_duration_minutes" validate:"omitempty,min=1"`
	DefaultSections        string `json:"default_sections" validate:"omitempty"`
	IsActive               bool   `json:"is_active"`
}

// CreateLessonPlanSectionRequest is the request body for creating a lesson plan section
type CreateLessonPlanSectionRequest struct {
	SectionType     string `json:"section_type" validate:"required,oneof=OPENING CORE_ACTIVITY CLOSING ASSESSMENT REFLECTION"`
	Title           string `json:"title" validate:"required,max=200"`
	Content         string `json:"content" validate:"required"`
	DurationMinutes int    `json:"duration_minutes" validate:"omitempty,min=1"`
	Sequence        int    `json:"sequence" validate:"omitempty,min=1"`
}

// UpdateLessonPlanSectionRequest is the request body for updating a lesson plan section
type UpdateLessonPlanSectionRequest struct {
	SectionType     string `json:"section_type" validate:"omitempty,oneof=OPENING CORE_ACTIVITY CLOSING ASSESSMENT REFLECTION"`
	Title           string `json:"title" validate:"omitempty,max=200"`
	Content         string `json:"content" validate:"omitempty"`
	DurationMinutes int    `json:"duration_minutes" validate:"omitempty,min=1"`
	Sequence        int    `json:"sequence" validate:"omitempty,min=1"`
}

// CreateLessonPlanResourceRequest is the request body for creating a lesson plan resource
type CreateLessonPlanResourceRequest struct {
	ResourceType string `json:"resource_type" validate:"required,oneof=MATERIAL MEDIA TOOL REFERENCE"`
	Title        string `json:"title" validate:"required,max=200"`
	Description  string `json:"description" validate:"omitempty"`
	URL          string `json:"url" validate:"omitempty,url"`
	FilePath     string `json:"file_path" validate:"omitempty"`
	FileSize     int64  `json:"file_size" validate:"omitempty"`
	MimeType     string `json:"mime_type" validate:"omitempty,max=100"`
}

// UpdateLessonPlanResourceRequest is the request body for updating a lesson plan resource
type UpdateLessonPlanResourceRequest struct {
	ResourceType string `json:"resource_type" validate:"omitempty,oneof=MATERIAL MEDIA TOOL REFERENCE"`
	Title        string `json:"title" validate:"omitempty,max=200"`
	Description  string `json:"description" validate:"omitempty"`
	URL          string `json:"url" validate:"omitempty,url"`
	FilePath     string `json:"file_path" validate:"omitempty"`
	FileSize     int64  `json:"file_size" validate:"omitempty"`
	MimeType     string `json:"mime_type" validate:"omitempty,max=100"`
}

// LessonPlanResponse represents the response for lesson plan operations
type LessonPlanResponse struct {
	ID                 uuid.UUID                    `json:"id"`
	Title              string                       `json:"title"`
	SubjectID          *uuid.UUID                   `json:"subject_id"`
	SubjectName        *string                      `json:"subject_name,omitempty"`
	ClassroomID        *uuid.UUID                   `json:"classroom_id"`
	ATPID              *uuid.UUID                   `json:"atp_id"`
	TeachingModuleID   *uuid.UUID                   `json:"teaching_module_id"`
	TemplateID         *uuid.UUID                   `json:"template_id"`
	MeetingDate        *string                      `json:"meeting_date"`
	MeetingNumber      int                          `json:"meeting_number"`
	DurationMinutes    int                          `json:"duration_minutes"`
	LearningObjectives string                       `json:"learning_objectives"`
	CoreMaterial       string                       `json:"core_material"`
	TeachingMethods    string                       `json:"teaching_methods"`
	AssessmentMethods  string                       `json:"assessment_methods"`
	Status             string                       `json:"status"`
	StatusName         string                       `json:"status_name"`
	Version            int                          `json:"version"`
	AcademicYearID     *uuid.UUID                   `json:"academic_year_id"`
	Semester           int                          `json:"semester"`
	Sections           []LessonPlanSectionResponse  `json:"sections,omitempty"`
	Resources          []LessonPlanResourceResponse `json:"resources,omitempty"`
	CreatedAt          time.Time                    `json:"created_at"`
	UpdatedAt          time.Time                    `json:"updated_at"`
}

// LessonPlanTemplateResponse represents the response for lesson plan template operations
type LessonPlanTemplateResponse struct {
	ID                     uuid.UUID  `json:"id"`
	Title                  string     `json:"title"`
	Description            string     `json:"description"`
	SubjectID              *uuid.UUID `json:"subject_id"`
	SubjectName            *string    `json:"subject_name,omitempty"`
	GradeLevel             string     `json:"grade_level"`
	Category               string     `json:"category"`
	DefaultDurationMinutes int        `json:"default_duration_minutes"`
	DefaultSections        string     `json:"default_sections"`
	IsActive               bool       `json:"is_active"`
	IsSystem               bool       `json:"is_system"`
	CreatedAt              time.Time  `json:"created_at"`
	UpdatedAt              time.Time  `json:"updated_at"`
}

// LessonPlanSectionResponse represents the response for lesson plan section operations
type LessonPlanSectionResponse struct {
	ID              uuid.UUID `json:"id"`
	LessonPlanID    uuid.UUID `json:"lesson_plan_id"`
	SectionType     string    `json:"section_type"`
	SectionTypeName string    `json:"section_type_name"`
	Title           string    `json:"title"`
	Content         string    `json:"content"`
	DurationMinutes int       `json:"duration_minutes"`
	Sequence        int       `json:"sequence"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
}

// LessonPlanResourceResponse represents the response for lesson plan resource operations
type LessonPlanResourceResponse struct {
	ID               uuid.UUID `json:"id"`
	LessonPlanID     uuid.UUID `json:"lesson_plan_id"`
	ResourceType     string    `json:"resource_type"`
	ResourceTypeName string    `json:"resource_type_name"`
	Title            string    `json:"title"`
	Description      string    `json:"description"`
	URL              string    `json:"url"`
	FilePath         string    `json:"file_path"`
	FileSize         int64     `json:"file_size"`
	MimeType         string    `json:"mime_type"`
	CreatedAt        time.Time `json:"created_at"`
	UpdatedAt        time.Time `json:"updated_at"`
}

// LessonPlanListResponse represents response for lesson plan list with pagination
type LessonPlanListResponse struct {
	TotalCount int                  `json:"total_count"`
	Items      []LessonPlanResponse `json:"items"`
}

// TemplateListResponse represents response for template list
type TemplateListResponse struct {
	TotalCount int                          `json:"total_count"`
	Items      []LessonPlanTemplateResponse `json:"items"`
}

// LessonPlanCopyRequest is the request body for copying a lesson plan
type LessonPlanCopyRequest struct {
	NewTitle string `json:"new_title" validate:"required,max=200"`
}

// CreateFromTemplateRequest is the request body for creating lesson plan from template
type CreateFromTemplateRequest struct {
	LessonPlanRequest CreateLessonPlanRequest `json:"lesson_plan" validate:"required"`
	TemplateID        string                  `json:"template_id" validate:"required,uuid"`
}
