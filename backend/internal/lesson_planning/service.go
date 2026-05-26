package lesson_planning

import (
	"context"
	"fmt"

	"github.com/google/uuid"
)

type Service interface {
	// Lesson Plan operations
	CreateLessonPlan(ctx context.Context, request CreateLessonPlanRequest) (*LessonPlanResponse, error)
	GetLessonPlanByID(id uuid.UUID) (*LessonPlanResponse, error)
	GetLessonPlans(filter map[string]interface{}) ([]LessonPlanResponse, error)
	UpdateLessonPlan(ctx context.Context, id uuid.UUID, request UpdateLessonPlanRequest) (*LessonPlanResponse, error)
	DeleteLessonPlan(ctx context.Context, id uuid.UUID) error
	CopyLessonPlan(ctx context.Context, id uuid.UUID, request LessonPlanCopyRequest) (*LessonPlanResponse, error)
	CreateFromTemplate(ctx context.Context, request CreateFromTemplateRequest) (*LessonPlanResponse, error)

	// Lesson Plan Template operations
	CreateTemplate(ctx context.Context, request CreateLessonPlanTemplateRequest) (*LessonPlanTemplateResponse, error)
	GetTemplateByID(id uuid.UUID) (*LessonPlanTemplateResponse, error)
	GetTemplates(filter map[string]interface{}) ([]LessonPlanTemplateResponse, error)
	UpdateTemplate(ctx context.Context, id uuid.UUID, request UpdateLessonPlanTemplateRequest) (*LessonPlanTemplateResponse, error)
	DeleteTemplate(ctx context.Context, id uuid.UUID) error

	// Lesson Plan Section operations
	CreateSection(ctx context.Context, lessonPlanID uuid.UUID, request CreateLessonPlanSectionRequest) (*LessonPlanSectionResponse, error)
	GetSectionByID(id uuid.UUID) (*LessonPlanSectionResponse, error)
	GetSectionsByLessonPlan(lessonPlanID uuid.UUID) ([]LessonPlanSectionResponse, error)
	UpdateSection(ctx context.Context, id uuid.UUID, request UpdateLessonPlanSectionRequest) (*LessonPlanSectionResponse, error)
	DeleteSection(ctx context.Context, id uuid.UUID) error

	// Lesson Plan Resource operations
	CreateResource(ctx context.Context, lessonPlanID uuid.UUID, request CreateLessonPlanResourceRequest) (*LessonPlanResourceResponse, error)
	GetResourceByID(id uuid.UUID) (*LessonPlanResourceResponse, error)
	GetResourcesByLessonPlan(lessonPlanID uuid.UUID) ([]LessonPlanResourceResponse, error)
	UpdateResource(ctx context.Context, id uuid.UUID, request UpdateLessonPlanResourceRequest) (*LessonPlanResourceResponse, error)
	DeleteResource(ctx context.Context, id uuid.UUID) error
}

type service struct {
	repo Repository
}

func NewService(repo Repository) Service {
	return &service{repo: repo}
}

// Lesson Plan operations
func (s *service) CreateLessonPlan(ctx context.Context, request CreateLessonPlanRequest) (*LessonPlanResponse, error) {
	var subjectID, classroomID, atpID, teachingModuleID, templateID, academicYearID *uuid.UUID

	if request.SubjectID != "" {
		id, err := uuid.Parse(request.SubjectID)
		if err != nil {
			return nil, fmt.Errorf("invalid subject ID: %w", err)
		}
		subjectID = &id
	}
	if request.ClassroomID != "" {
		id, err := uuid.Parse(request.ClassroomID)
		if err != nil {
			return nil, fmt.Errorf("invalid classroom ID: %w", err)
		}
		classroomID = &id
	}
	if request.ATPID != "" {
		id, err := uuid.Parse(request.ATPID)
		if err != nil {
			return nil, fmt.Errorf("invalid ATP ID: %w", err)
		}
		atpID = &id
	}
	if request.TeachingModuleID != "" {
		id, err := uuid.Parse(request.TeachingModuleID)
		if err != nil {
			return nil, fmt.Errorf("invalid teaching module ID: %w", err)
		}
		teachingModuleID = &id
	}
	if request.TemplateID != "" {
		id, err := uuid.Parse(request.TemplateID)
		if err != nil {
			return nil, fmt.Errorf("invalid template ID: %w", err)
		}
		templateID = &id
	}
	if request.AcademicYearID != "" {
		id, err := uuid.Parse(request.AcademicYearID)
		if err != nil {
			return nil, fmt.Errorf("invalid academic year ID: %w", err)
		}
		academicYearID = &id
	}

	plan := &LessonPlan{
		ID:                 uuid.New(),
		Title:              request.Title,
		SubjectID:          subjectID,
		ClassroomID:        classroomID,
		ATPID:              atpID,
		TeachingModuleID:   teachingModuleID,
		TemplateID:         templateID,
		MeetingDate:        &request.MeetingDate,
		MeetingNumber:      request.MeetingNumber,
		DurationMinutes:    request.DurationMinutes,
		LearningObjectives: request.LearningObjectives,
		CoreMaterial:       request.CoreMaterial,
		TeachingMethods:    request.TeachingMethods,
		AssessmentMethods:  request.AssessmentMethods,
		Status:             request.Status,
		Version:            1,
		AcademicYearID:     academicYearID,
		Semester:           request.Semester,
	}

	// Set defaults
	if plan.Status == "" {
		plan.Status = LessonPlanStatusDraft
	}
	if plan.DurationMinutes == 0 {
		plan.DurationMinutes = 45
	}
	if plan.MeetingNumber == 0 {
		plan.MeetingNumber = 1
	}
	if plan.Semester == 0 {
		plan.Semester = 1
	}

	err := s.repo.CreateLessonPlan(ctx, plan)
	if err != nil {
		return nil, err
	}

	// Create sections if provided
	for _, sectionReq := range request.Sections {
		_, err := s.CreateSection(ctx, plan.ID, sectionReq)
		if err != nil {
			return nil, fmt.Errorf("failed to create section: %w", err)
		}
	}

	// Create resources if provided
	for _, resourceReq := range request.Resources {
		_, err := s.CreateResource(ctx, plan.ID, resourceReq)
		if err != nil {
			return nil, fmt.Errorf("failed to create resource: %w", err)
		}
	}

	return s.GetLessonPlanByID(plan.ID)
}

func (s *service) GetLessonPlanByID(id uuid.UUID) (*LessonPlanResponse, error) {
	plan, err := s.repo.GetLessonPlanByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToLessonPlanResponse(plan), nil
}

func (s *service) GetLessonPlans(filter map[string]interface{}) ([]LessonPlanResponse, error) {
	plans, err := s.repo.GetLessonPlans(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]LessonPlanResponse, len(plans))
	for i, plan := range plans {
		responses[i] = *s.modelToLessonPlanResponse(&plan)
	}
	return responses, nil
}

func (s *service) UpdateLessonPlan(ctx context.Context, id uuid.UUID, request UpdateLessonPlanRequest) (*LessonPlanResponse, error) {
	plan, err := s.repo.GetLessonPlanByID(id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if request.Title != "" {
		plan.Title = request.Title
	}
	// Add other field updates similarly...

	err = s.repo.UpdateLessonPlan(ctx, plan)
	if err != nil {
		return nil, err
	}

	return s.GetLessonPlanByID(plan.ID)
}

func (s *service) DeleteLessonPlan(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteLessonPlan(ctx, id)
}

func (s *service) CopyLessonPlan(ctx context.Context, id uuid.UUID, request LessonPlanCopyRequest) (*LessonPlanResponse, error) {
	plan, err := s.repo.CopyLessonPlan(ctx, id, request.NewTitle)
	if err != nil {
		return nil, err
	}
	return s.modelToLessonPlanResponse(plan), nil
}

func (s *service) CreateFromTemplate(ctx context.Context, request CreateFromTemplateRequest) (*LessonPlanResponse, error) {
	templateID, err := uuid.Parse(request.TemplateID)
	if err != nil {
		return nil, fmt.Errorf("invalid template ID: %w", err)
	}

	// Create lesson plan from request
	plan := &LessonPlan{
		ID:    uuid.New(),
		Title: request.LessonPlanRequest.Title,
	}
	// Set other fields from request...

	err = s.repo.CreateFromTemplate(ctx, templateID, plan)
	if err != nil {
		return nil, err
	}

	return s.GetLessonPlanByID(plan.ID)
}

// Template operations
func (s *service) CreateTemplate(ctx context.Context, request CreateLessonPlanTemplateRequest) (*LessonPlanTemplateResponse, error) {
	var subjectID *uuid.UUID
	if request.SubjectID != "" {
		id, err := uuid.Parse(request.SubjectID)
		if err != nil {
			return nil, fmt.Errorf("invalid subject ID: %w", err)
		}
		subjectID = &id
	}

	template := &LessonPlanTemplate{
		ID:                     uuid.New(),
		Title:                  request.Title,
		Description:            request.Description,
		SubjectID:              subjectID,
		GradeLevel:             request.GradeLevel,
		Category:               request.Category,
		DefaultDurationMinutes: request.DefaultDurationMinutes,
		DefaultSections:        request.DefaultSections,
		IsActive:               request.IsActive,
		IsSystem:               false,
	}

	err := s.repo.CreateTemplate(ctx, template)
	if err != nil {
		return nil, err
	}

	return s.modelToTemplateResponse(template), nil
}

func (s *service) GetTemplateByID(id uuid.UUID) (*LessonPlanTemplateResponse, error) {
	template, err := s.repo.GetTemplateByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToTemplateResponse(template), nil
}

func (s *service) GetTemplates(filter map[string]interface{}) ([]LessonPlanTemplateResponse, error) {
	templates, err := s.repo.GetTemplates(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]LessonPlanTemplateResponse, len(templates))
	for i, template := range templates {
		responses[i] = *s.modelToTemplateResponse(&template)
	}
	return responses, nil
}

func (s *service) UpdateTemplate(ctx context.Context, id uuid.UUID, request UpdateLessonPlanTemplateRequest) (*LessonPlanTemplateResponse, error) {
	template, err := s.repo.GetTemplateByID(id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if request.Title != "" {
		template.Title = request.Title
	}
	// Add other field updates...

	err = s.repo.UpdateTemplate(ctx, template)
	if err != nil {
		return nil, err
	}

	return s.modelToTemplateResponse(template), nil
}

func (s *service) DeleteTemplate(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteTemplate(ctx, id)
}

// Section operations
func (s *service) CreateSection(ctx context.Context, lessonPlanID uuid.UUID, request CreateLessonPlanSectionRequest) (*LessonPlanSectionResponse, error) {
	section := &LessonPlanSection{
		ID:              uuid.New(),
		LessonPlanID:    lessonPlanID,
		SectionType:     request.SectionType,
		Title:           request.Title,
		Content:         request.Content,
		DurationMinutes: request.DurationMinutes,
		Sequence:        request.Sequence,
	}

	if section.DurationMinutes == 0 {
		section.DurationMinutes = 10
	}
	if section.Sequence == 0 {
		section.Sequence = 1
	}

	err := s.repo.CreateSection(ctx, section)
	if err != nil {
		return nil, err
	}

	return s.modelToSectionResponse(section), nil
}

func (s *service) GetSectionByID(id uuid.UUID) (*LessonPlanSectionResponse, error) {
	section, err := s.repo.GetSectionByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToSectionResponse(section), nil
}

func (s *service) GetSectionsByLessonPlan(lessonPlanID uuid.UUID) ([]LessonPlanSectionResponse, error) {
	sections, err := s.repo.GetSectionsByLessonPlan(lessonPlanID)
	if err != nil {
		return nil, err
	}

	responses := make([]LessonPlanSectionResponse, len(sections))
	for i, section := range sections {
		responses[i] = *s.modelToSectionResponse(&section)
	}
	return responses, nil
}

func (s *service) UpdateSection(ctx context.Context, id uuid.UUID, request UpdateLessonPlanSectionRequest) (*LessonPlanSectionResponse, error) {
	section, err := s.repo.GetSectionByID(id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if request.Title != "" {
		section.Title = request.Title
	}
	// Add other field updates...

	err = s.repo.UpdateSection(ctx, section)
	if err != nil {
		return nil, err
	}

	return s.modelToSectionResponse(section), nil
}

func (s *service) DeleteSection(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteSection(ctx, id)
}

// Resource operations
func (s *service) CreateResource(ctx context.Context, lessonPlanID uuid.UUID, request CreateLessonPlanResourceRequest) (*LessonPlanResourceResponse, error) {
	resource := &LessonPlanResource{
		ID:           uuid.New(),
		LessonPlanID: lessonPlanID,
		ResourceType: request.ResourceType,
		Title:        request.Title,
		Description:  request.Description,
		URL:          request.URL,
		FilePath:     request.FilePath,
		FileSize:     request.FileSize,
		MimeType:     request.MimeType,
	}

	err := s.repo.CreateResource(ctx, resource)
	if err != nil {
		return nil, err
	}

	return s.modelToResourceResponse(resource), nil
}

func (s *service) GetResourceByID(id uuid.UUID) (*LessonPlanResourceResponse, error) {
	resource, err := s.repo.GetResourceByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToResourceResponse(resource), nil
}

func (s *service) GetResourcesByLessonPlan(lessonPlanID uuid.UUID) ([]LessonPlanResourceResponse, error) {
	resources, err := s.repo.GetResourcesByLessonPlan(lessonPlanID)
	if err != nil {
		return nil, err
	}

	responses := make([]LessonPlanResourceResponse, len(resources))
	for i, resource := range resources {
		responses[i] = *s.modelToResourceResponse(&resource)
	}
	return responses, nil
}

func (s *service) UpdateResource(ctx context.Context, id uuid.UUID, request UpdateLessonPlanResourceRequest) (*LessonPlanResourceResponse, error) {
	resource, err := s.repo.GetResourceByID(id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if request.Title != "" {
		resource.Title = request.Title
	}
	// Add other field updates...

	err = s.repo.UpdateResource(ctx, resource)
	if err != nil {
		return nil, err
	}

	return s.modelToResourceResponse(resource), nil
}

func (s *service) DeleteResource(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteResource(ctx, id)
}

// Helper functions for model-to-response conversion
func (s *service) modelToLessonPlanResponse(plan *LessonPlan) *LessonPlanResponse {
	var subjectName *string
	if plan.Subject != nil {
		name := plan.Subject.SubjectName
		subjectName = &name
	}

	sectionResponses := make([]LessonPlanSectionResponse, len(plan.Sections))
	for i, section := range plan.Sections {
		sectionResponses[i] = *s.modelToSectionResponse(&section)
	}

	resourceResponses := make([]LessonPlanResourceResponse, len(plan.Resources))
	for i, resource := range plan.Resources {
		resourceResponses[i] = *s.modelToResourceResponse(&resource)
	}

	return &LessonPlanResponse{
		ID:                 plan.ID,
		Title:              plan.Title,
		SubjectID:          plan.SubjectID,
		SubjectName:        subjectName,
		ClassroomID:        plan.ClassroomID,
		ATPID:              plan.ATPID,
		TeachingModuleID:   plan.TeachingModuleID,
		TemplateID:         plan.TemplateID,
		MeetingDate:        plan.MeetingDate,
		MeetingNumber:      plan.MeetingNumber,
		DurationMinutes:    plan.DurationMinutes,
		LearningObjectives: plan.LearningObjectives,
		CoreMaterial:       plan.CoreMaterial,
		TeachingMethods:    plan.TeachingMethods,
		AssessmentMethods:  plan.AssessmentMethods,
		Status:             plan.Status,
		StatusName:         GetLessonPlanStatusDescription(plan.Status),
		Version:            plan.Version,
		AcademicYearID:     plan.AcademicYearID,
		Semester:           plan.Semester,
		Sections:           sectionResponses,
		Resources:          resourceResponses,
		CreatedAt:          plan.CreatedAt,
		UpdatedAt:          plan.UpdatedAt,
	}
}

func (s *service) modelToTemplateResponse(template *LessonPlanTemplate) *LessonPlanTemplateResponse {
	var subjectName *string
	if template.Subject != nil {
		name := template.Subject.SubjectName
		subjectName = &name
	}

	return &LessonPlanTemplateResponse{
		ID:                     template.ID,
		Title:                  template.Title,
		Description:            template.Description,
		SubjectID:              template.SubjectID,
		SubjectName:            subjectName,
		GradeLevel:             template.GradeLevel,
		Category:               template.Category,
		DefaultDurationMinutes: template.DefaultDurationMinutes,
		DefaultSections:        template.DefaultSections,
		IsActive:               template.IsActive,
		IsSystem:               template.IsSystem,
		CreatedAt:              template.CreatedAt,
		UpdatedAt:              template.UpdatedAt,
	}
}

func (s *service) modelToSectionResponse(section *LessonPlanSection) *LessonPlanSectionResponse {
	return &LessonPlanSectionResponse{
		ID:              section.ID,
		LessonPlanID:    section.LessonPlanID,
		SectionType:     section.SectionType,
		SectionTypeName: GetSectionTypeDescription(section.SectionType),
		Title:           section.Title,
		Content:         section.Content,
		DurationMinutes: section.DurationMinutes,
		Sequence:        section.Sequence,
		CreatedAt:       section.CreatedAt,
		UpdatedAt:       section.UpdatedAt,
	}
}

func (s *service) modelToResourceResponse(resource *LessonPlanResource) *LessonPlanResourceResponse {
	return &LessonPlanResourceResponse{
		ID:               resource.ID,
		LessonPlanID:     resource.LessonPlanID,
		ResourceType:     resource.ResourceType,
		ResourceTypeName: GetResourceTypeDescription(resource.ResourceType),
		Title:            resource.Title,
		Description:      resource.Description,
		URL:              resource.URL,
		FilePath:         resource.FilePath,
		FileSize:         resource.FileSize,
		MimeType:         resource.MimeType,
		CreatedAt:        resource.CreatedAt,
		UpdatedAt:        resource.UpdatedAt,
	}
}
