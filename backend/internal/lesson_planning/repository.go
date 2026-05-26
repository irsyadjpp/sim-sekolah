package lesson_planning

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Repository interface {
	// Lesson Plan operations
	CreateLessonPlan(ctx context.Context, plan *LessonPlan) error
	GetLessonPlanByID(id uuid.UUID) (*LessonPlan, error)
	GetLessonPlans(filter map[string]interface{}) ([]LessonPlan, error)
	UpdateLessonPlan(ctx context.Context, plan *LessonPlan) error
	DeleteLessonPlan(ctx context.Context, id uuid.UUID) error
	CopyLessonPlan(ctx context.Context, originalID uuid.UUID, newTitle string) (*LessonPlan, error)
	CreateFromTemplate(ctx context.Context, templateID uuid.UUID, plan *LessonPlan) error

	// Lesson Plan Template operations
	CreateTemplate(ctx context.Context, template *LessonPlanTemplate) error
	GetTemplateByID(id uuid.UUID) (*LessonPlanTemplate, error)
	GetTemplates(filter map[string]interface{}) ([]LessonPlanTemplate, error)
	UpdateTemplate(ctx context.Context, template *LessonPlanTemplate) error
	DeleteTemplate(ctx context.Context, id uuid.UUID) error

	// Lesson Plan Section operations
	CreateSection(ctx context.Context, section *LessonPlanSection) error
	GetSectionByID(id uuid.UUID) (*LessonPlanSection, error)
	GetSectionsByLessonPlan(lessonPlanID uuid.UUID) ([]LessonPlanSection, error)
	UpdateSection(ctx context.Context, section *LessonPlanSection) error
	DeleteSection(ctx context.Context, id uuid.UUID) error

	// Lesson Plan Resource operations
	CreateResource(ctx context.Context, resource *LessonPlanResource) error
	GetResourceByID(id uuid.UUID) (*LessonPlanResource, error)
	GetResourcesByLessonPlan(lessonPlanID uuid.UUID) ([]LessonPlanResource, error)
	UpdateResource(ctx context.Context, resource *LessonPlanResource) error
	DeleteResource(ctx context.Context, id uuid.UUID) error
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

// Lesson Plan operations
func (r *repository) CreateLessonPlan(ctx context.Context, plan *LessonPlan) error {
	return r.db.WithContext(ctx).Create(plan).Error
}

func (r *repository) GetLessonPlanByID(id uuid.UUID) (*LessonPlan, error) {
	var plan LessonPlan
	err := r.db.Preload("Subject").Preload("Template").Preload("Sections").Preload("Resources").
		Where("id = ? AND deleted_at IS NULL", id).First(&plan).Error
	if err != nil {
		return nil, err
	}
	return &plan, nil
}

func (r *repository) GetLessonPlans(filter map[string]interface{}) ([]LessonPlan, error) {
	var plans []LessonPlan
	query := r.db.Where("deleted_at IS NULL")

	if subjectID, ok := filter["subject_id"].(string); ok && subjectID != "" {
		query = query.Where("subject_id = ?", subjectID)
	}
	if classroomID, ok := filter["classroom_id"].(string); ok && classroomID != "" {
		query = query.Where("classroom_id = ?", classroomID)
	}
	if status, ok := filter["status"].(string); ok && status != "" {
		query = query.Where("status = ?", status)
	}
	if academicYearID, ok := filter["academic_year_id"].(string); ok && academicYearID != "" {
		query = query.Where("academic_year_id = ?", academicYearID)
	}
	if semester, ok := filter["semester"].(int); ok && semester > 0 {
		query = query.Where("semester = ?", semester)
	}

	err := query.Preload("Subject").Preload("Template").Preload("Sections").Preload("Resources").
		Order("created_at DESC").Find(&plans).Error
	return plans, err
}

func (r *repository) UpdateLessonPlan(ctx context.Context, plan *LessonPlan) error {
	return r.db.WithContext(ctx).Save(plan).Error
}

func (r *repository) DeleteLessonPlan(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&LessonPlan{}).Error
}

func (r *repository) CopyLessonPlan(ctx context.Context, originalID uuid.UUID, newTitle string) (*LessonPlan, error) {
	var original LessonPlan
	err := r.db.Preload("Sections").Preload("Resources").Where("id = ?", originalID).First(&original).Error
	if err != nil {
		return nil, err
	}

	// Create new lesson plan
	newPlan := &LessonPlan{
		ID:                 uuid.New(),
		Title:              newTitle,
		SubjectID:          original.SubjectID,
		ClassroomID:        original.ClassroomID,
		ATPID:              original.ATPID,
		TeachingModuleID:   original.TeachingModuleID,
		TemplateID:         original.TemplateID,
		MeetingDate:        original.MeetingDate,
		MeetingNumber:      original.MeetingNumber,
		DurationMinutes:    original.DurationMinutes,
		LearningObjectives: original.LearningObjectives,
		CoreMaterial:       original.CoreMaterial,
		TeachingMethods:    original.TeachingMethods,
		AssessmentMethods:  original.AssessmentMethods,
		Status:             LessonPlanStatusDraft,
		Version:            1,
		AcademicYearID:     original.AcademicYearID,
		Semester:           original.Semester,
	}

	err = r.db.WithContext(ctx).Create(newPlan).Error
	if err != nil {
		return nil, err
	}

	// Copy sections
	for _, section := range original.Sections {
		newSection := &LessonPlanSection{
			ID:              uuid.New(),
			LessonPlanID:    newPlan.ID,
			SectionType:     section.SectionType,
			Title:           section.Title,
			Content:         section.Content,
			DurationMinutes: section.DurationMinutes,
			Sequence:        section.Sequence,
		}
		err = r.db.WithContext(ctx).Create(newSection).Error
		if err != nil {
			return nil, err
		}
	}

	// Copy resources
	for _, resource := range original.Resources {
		newResource := &LessonPlanResource{
			ID:           uuid.New(),
			LessonPlanID: newPlan.ID,
			ResourceType: resource.ResourceType,
			Title:        resource.Title,
			Description:  resource.Description,
			URL:          resource.URL,
			FilePath:     resource.FilePath,
			FileSize:     resource.FileSize,
			MimeType:     resource.MimeType,
		}
		err = r.db.WithContext(ctx).Create(newResource).Error
		if err != nil {
			return nil, err
		}
	}

	return r.GetLessonPlanByID(newPlan.ID)
}

func (r *repository) CreateFromTemplate(ctx context.Context, templateID uuid.UUID, plan *LessonPlan) error {
	// Get template to apply default values
	var template LessonPlanTemplate
	err := r.db.Where("id = ? AND is_active = ?", templateID, true).First(&template).Error
	if err != nil {
		return err
	}

	// Apply template defaults if not set
	if plan.DurationMinutes == 0 && template.DefaultDurationMinutes > 0 {
		plan.DurationMinutes = template.DefaultDurationMinutes
	}

	// Note: Default sections would be parsed and applied here in a full implementation
	// For now, we just link the template
	plan.TemplateID = &templateID

	return r.db.WithContext(ctx).Create(plan).Error
}

// Lesson Plan Template operations
func (r *repository) CreateTemplate(ctx context.Context, template *LessonPlanTemplate) error {
	return r.db.WithContext(ctx).Create(template).Error
}

func (r *repository) GetTemplateByID(id uuid.UUID) (*LessonPlanTemplate, error) {
	var template LessonPlanTemplate
	err := r.db.Preload("Subject").Where("id = ?", id).First(&template).Error
	if err != nil {
		return nil, err
	}
	return &template, nil
}

func (r *repository) GetTemplates(filter map[string]interface{}) ([]LessonPlanTemplate, error) {
	var templates []LessonPlanTemplate
	query := r.db.Where("deleted_at IS NULL")

	if subjectID, ok := filter["subject_id"].(string); ok && subjectID != "" {
		query = query.Where("subject_id = ?", subjectID)
	}
	if gradeLevel, ok := filter["grade_level"].(string); ok && gradeLevel != "" {
		query = query.Where("grade_level = ? OR grade_level = ?", gradeLevel, "ALL")
	}
	if category, ok := filter["category"].(string); ok && category != "" {
		query = query.Where("category = ?", category)
	}
	if isActive, ok := filter["is_active"].(bool); ok {
		query = query.Where("is_active = ?", isActive)
	}

	err := query.Preload("Subject").Order("created_at DESC").Find(&templates).Error
	return templates, err
}

func (r *repository) UpdateTemplate(ctx context.Context, template *LessonPlanTemplate) error {
	return r.db.WithContext(ctx).Save(template).Error
}

func (r *repository) DeleteTemplate(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&LessonPlanTemplate{}).Error
}

// Lesson Plan Section operations
func (r *repository) CreateSection(ctx context.Context, section *LessonPlanSection) error {
	return r.db.WithContext(ctx).Create(section).Error
}

func (r *repository) GetSectionByID(id uuid.UUID) (*LessonPlanSection, error) {
	var section LessonPlanSection
	err := r.db.Where("id = ?", id).First(&section).Error
	if err != nil {
		return nil, err
	}
	return &section, nil
}

func (r *repository) GetSectionsByLessonPlan(lessonPlanID uuid.UUID) ([]LessonPlanSection, error) {
	var sections []LessonPlanSection
	err := r.db.Where("lesson_plan_id = ?", lessonPlanID).Order("sequence ASC").Find(&sections).Error
	return sections, err
}

func (r *repository) UpdateSection(ctx context.Context, section *LessonPlanSection) error {
	return r.db.WithContext(ctx).Save(section).Error
}

func (r *repository) DeleteSection(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&LessonPlanSection{}).Error
}

// Lesson Plan Resource operations
func (r *repository) CreateResource(ctx context.Context, resource *LessonPlanResource) error {
	return r.db.WithContext(ctx).Create(resource).Error
}

func (r *repository) GetResourceByID(id uuid.UUID) (*LessonPlanResource, error) {
	var resource LessonPlanResource
	err := r.db.Where("id = ?", id).First(&resource).Error
	if err != nil {
		return nil, err
	}
	return &resource, nil
}

func (r *repository) GetResourcesByLessonPlan(lessonPlanID uuid.UUID) ([]LessonPlanResource, error) {
	var resources []LessonPlanResource
	err := r.db.Where("lesson_plan_id = ?", lessonPlanID).Order("created_at ASC").Find(&resources).Error
	return resources, err
}

func (r *repository) UpdateResource(ctx context.Context, resource *LessonPlanResource) error {
	return r.db.WithContext(ctx).Save(resource).Error
}

func (r *repository) DeleteResource(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&LessonPlanResource{}).Error
}
