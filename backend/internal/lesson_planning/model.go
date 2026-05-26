package lesson_planning

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/subject"

	"github.com/google/uuid"
)

// LessonPlan represents a comprehensive lesson plan (RPP)
type LessonPlan struct {
	ID               uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Title            string     `gorm:"type:varchar(200);not null" json:"title"`
	SubjectID        *uuid.UUID `gorm:"type:uuid;index" json:"subject_id"`
	ClassroomID      *uuid.UUID `gorm:"type:uuid;index" json:"classroom_id"`
	ATPID            *uuid.UUID `gorm:"type:uuid;index" json:"atp_id"`             // Link to ATP if applicable
	TeachingModuleID *uuid.UUID `gorm:"type:uuid;index" json:"teaching_module_id"` // Link to TeachingModule
	TemplateID       *uuid.UUID `gorm:"type:uuid;index" json:"template_id"`        // If created from template

	// Scheduling
	MeetingDate     *string `gorm:"type:varchar(50)" json:"meeting_date"` // e.g., "Pertemuan 1"
	MeetingNumber   int     `gorm:"type:integer;default:1" json:"meeting_number"`
	DurationMinutes int     `gorm:"type:integer;default:45" json:"duration_minutes"` // Duration in minutes

	// Content
	LearningObjectives string `gorm:"type:text" json:"learning_objectives"`
	CoreMaterial       string `gorm:"type:text" json:"core_material"`
	TeachingMethods    string `gorm:"type:text" json:"teaching_methods"`   // Methods used (comma-separated)
	AssessmentMethods  string `gorm:"type:text" json:"assessment_methods"` // Assessment methods

	// Status and Metadata
	Status         string     `gorm:"type:varchar(20);default:'DRAFT'" json:"status"` // DRAFT, REVIEW, APPROVED, PUBLISHED
	Version        int        `gorm:"type:integer;default:1" json:"version"`
	AcademicYearID *uuid.UUID `gorm:"type:uuid;index" json:"academic_year_id"`
	Semester       int        `gorm:"type:integer;default:1" json:"semester"` // 1 or 2

	common.Auditable

	Subject   *subject.Subject     `gorm:"foreignKey:SubjectID" json:"subject,omitempty"`
	Template  *LessonPlanTemplate  `gorm:"foreignKey:TemplateID" json:"template,omitempty"`
	Sections  []LessonPlanSection  `gorm:"foreignKey:LessonPlanID" json:"sections,omitempty"`
	Resources []LessonPlanResource `gorm:"foreignKey:LessonPlanID" json:"resources,omitempty"`
}

func (LessonPlan) TableName() string {
	return "master_lesson_plan"
}

// LessonPlanTemplate represents reusable lesson plan templates
type LessonPlanTemplate struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Title       string     `gorm:"type:varchar(200);not null" json:"title"`
	Description string     `gorm:"type:text" json:"description"`
	SubjectID   *uuid.UUID `gorm:"type:uuid;index" json:"subject_id"`
	GradeLevel  string     `gorm:"type:varchar(50);index" json:"grade_level"` // 1-6, LOWER, UPPER, ALL
	Category    string     `gorm:"type:varchar(100)" json:"category"`         // e.g., "Numerasi", "Literasi", "P5"

	// Structure
	DefaultDurationMinutes int    `gorm:"type:integer;default:45" json:"default_duration_minutes"`
	DefaultSections        string `gorm:"type:text" json:"default_sections"` // JSON array of default sections

	IsActive bool `gorm:"default:true" json:"is_active"`
	IsSystem bool `gorm:"default:false" json:"is_system"` // System templates vs user templates

	common.Auditable

	Subject *subject.Subject `gorm:"foreignKey:SubjectID" json:"subject,omitempty"`
	Plans   []LessonPlan     `gorm:"foreignKey:TemplateID" json:"plans,omitempty"`
}

func (LessonPlanTemplate) TableName() string {
	return "master_lesson_plan_template"
}

// LessonPlanSection represents sections of a lesson plan
type LessonPlanSection struct {
	ID              uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	LessonPlanID    uuid.UUID `gorm:"type:uuid;not null;index" json:"lesson_plan_id"`
	SectionType     string    `gorm:"type:varchar(50);not null" json:"section_type"` // OPENING, CORE_ACTIVITY, CLOSING, ASSESSMENT, REFLECTION
	Title           string    `gorm:"type:varchar(200);not null" json:"title"`
	Content         string    `gorm:"type:text;not null" json:"content"`
	DurationMinutes int       `gorm:"type:integer;default:10" json:"duration_minutes"`
	Sequence        int       `gorm:"type:integer;default:1" json:"sequence"`

	common.Auditable

	LessonPlan *LessonPlan `gorm:"foreignKey:LessonPlanID" json:"lesson_plan,omitempty"`
}

func (LessonPlanSection) TableName() string {
	return "master_lesson_plan_section"
}

// LessonPlanResource represents resources/media used in lesson plan
type LessonPlanResource struct {
	ID           uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	LessonPlanID uuid.UUID `gorm:"type:uuid;not null;index" json:"lesson_plan_id"`
	ResourceType string    `gorm:"type:varchar(50);not null" json:"resource_type"` // MATERIAL, MEDIA, TOOL, REFERENCE
	Title        string    `gorm:"type:varchar(200);not null" json:"title"`
	Description  string    `gorm:"type:text" json:"description"`
	URL          string    `gorm:"type:varchar(500)" json:"url"`       // URL to resource
	FilePath     string    `gorm:"type:varchar(500)" json:"file_path"` // Local file path
	FileSize     int64     `gorm:"type:bigint" json:"file_size"`       // File size in bytes
	MimeType     string    `gorm:"type:varchar(100)" json:"mime_type"`

	common.Auditable

	LessonPlan *LessonPlan `gorm:"foreignKey:LessonPlanID" json:"lesson_plan,omitempty"`
}

func (LessonPlanResource) TableName() string {
	return "master_lesson_plan_resource"
}

// Lesson plan status constants
const (
	LessonPlanStatusDraft     = "DRAFT"
	LessonPlanStatusReview    = "REVIEW"
	LessonPlanStatusApproved  = "APPROVED"
	LessonPlanStatusPublished = "PUBLISHED"
)

// Section type constants
const (
	SectionTypeOpening      = "PENDAHULUAN"
	SectionTypeCoreActivity = "KEGIATAN_INTI"
	SectionTypeClosing      = "PENUTUP"
	SectionTypeAssessment   = "ASESMEN"
	SectionTypeReflection   = "REFLEKSI"
)

// Resource type constants
const (
	ResourceTypeMaterial  = "MATERI"
	ResourceTypeMedia     = "MEDIA"
	ResourceTypeTool      = "ALAT"
	ResourceTypeReference = "REFERENCE"
)

// GetLessonPlanStatusDescription returns Indonesian description for lesson plan status
func GetLessonPlanStatusDescription(status string) string {
	descriptions := map[string]string{
		LessonPlanStatusDraft:     "Draf",
		LessonPlanStatusReview:    "Review",
		LessonPlanStatusApproved:  "Disetujui",
		LessonPlanStatusPublished: "Diterbitkan",
	}
	if desc, exists := descriptions[status]; exists {
		return desc
	}
	return status
}

// GetSectionTypeDescription returns Indonesian description for section type
func GetSectionTypeDescription(sectionType string) string {
	descriptions := map[string]string{
		SectionTypeOpening:      "Pendahuluan",
		SectionTypeCoreActivity: "Kegiatan Inti",
		SectionTypeClosing:      "Penutup",
		SectionTypeAssessment:   "Penilaian",
		SectionTypeReflection:   "Refleksi",
	}
	if desc, exists := descriptions[sectionType]; exists {
		return desc
	}
	return sectionType
}

// GetResourceTypeDescription returns Indonesian description for resource type
func GetResourceTypeDescription(resourceType string) string {
	descriptions := map[string]string{
		ResourceTypeMaterial:  "Bahan Ajar",
		ResourceTypeMedia:     "Media",
		ResourceTypeTool:      "Alat",
		ResourceTypeReference: "Referensi",
	}
	if desc, exists := descriptions[resourceType]; exists {
		return desc
	}
	return resourceType
}
