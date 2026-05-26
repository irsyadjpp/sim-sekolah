package lesson_planning

import (
	"strconv"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type Handler interface {
	// Lesson Plan routes
	CreateLessonPlan(c *fiber.Ctx) error
	GetLessonPlanByID(c *fiber.Ctx) error
	GetLessonPlans(c *fiber.Ctx) error
	UpdateLessonPlan(c *fiber.Ctx) error
	DeleteLessonPlan(c *fiber.Ctx) error
	CopyLessonPlan(c *fiber.Ctx) error
	CreateFromTemplate(c *fiber.Ctx) error

	// Template routes
	CreateTemplate(c *fiber.Ctx) error
	GetTemplateByID(c *fiber.Ctx) error
	GetTemplates(c *fiber.Ctx) error
	UpdateTemplate(c *fiber.Ctx) error
	DeleteTemplate(c *fiber.Ctx) error

	// Section routes
	CreateSection(c *fiber.Ctx) error
	GetSectionByID(c *fiber.Ctx) error
	GetSectionsByLessonPlan(c *fiber.Ctx) error
	UpdateSection(c *fiber.Ctx) error
	DeleteSection(c *fiber.Ctx) error

	// Resource routes
	CreateResource(c *fiber.Ctx) error
	GetResourceByID(c *fiber.Ctx) error
	GetResourcesByLessonPlan(c *fiber.Ctx) error
	UpdateResource(c *fiber.Ctx) error
	DeleteResource(c *fiber.Ctx) error

	// Route registration
	RegisterRoutes(group fiber.Router)
}

type handler struct {
	service Service
}

func NewHandler(service Service) Handler {
	return &handler{service: service}
}

// Lesson Plan handlers
func (h *handler) CreateLessonPlan(c *fiber.Ctx) error {
	var request CreateLessonPlanRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateLessonPlan(c.UserContext(), request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) GetLessonPlanByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid lesson plan ID"})
	}

	response, err := h.service.GetLessonPlanByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Lesson plan not found"})
	}

	return c.JSON(response)
}

func (h *handler) GetLessonPlans(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if subjectID := c.Query("subject_id"); subjectID != "" {
		filter["subject_id"] = subjectID
	}
	if classroomID := c.Query("classroom_id"); classroomID != "" {
		filter["classroom_id"] = classroomID
	}
	if status := c.Query("status"); status != "" {
		filter["status"] = status
	}

	response, err := h.service.GetLessonPlans(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) UpdateLessonPlan(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid lesson plan ID"})
	}

	var request UpdateLessonPlanRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.UpdateLessonPlan(c.UserContext(), id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) DeleteLessonPlan(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid lesson plan ID"})
	}

	err = h.service.DeleteLessonPlan(c.UserContext(), id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Lesson plan deleted successfully"})
}

func (h *handler) CopyLessonPlan(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid lesson plan ID"})
	}

	var request LessonPlanCopyRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CopyLessonPlan(c.UserContext(), id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) CreateFromTemplate(c *fiber.Ctx) error {
	var request CreateFromTemplateRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateFromTemplate(c.UserContext(), request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

// Template handlers
func (h *handler) CreateTemplate(c *fiber.Ctx) error {
	var request CreateLessonPlanTemplateRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateTemplate(c.UserContext(), request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) GetTemplateByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid template ID"})
	}

	response, err := h.service.GetTemplateByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Template not found"})
	}

	return c.JSON(response)
}

func (h *handler) GetTemplates(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if subjectID := c.Query("subject_id"); subjectID != "" {
		filter["subject_id"] = subjectID
	}
	if gradeLevel := c.Query("grade_level"); gradeLevel != "" {
		filter["grade_level"] = gradeLevel
	}
	if category := c.Query("category"); category != "" {
		filter["category"] = category
	}
	if isActiveStr := c.Query("is_active"); isActiveStr != "" {
		if isActive, err := strconv.ParseBool(isActiveStr); err == nil {
			filter["is_active"] = isActive
		}
	}

	response, err := h.service.GetTemplates(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) UpdateTemplate(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid template ID"})
	}

	var request UpdateLessonPlanTemplateRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.UpdateTemplate(c.UserContext(), id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) DeleteTemplate(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid template ID"})
	}

	err = h.service.DeleteTemplate(c.UserContext(), id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Template deleted successfully"})
}

// Section handlers (simplified)
func (h *handler) CreateSection(c *fiber.Ctx) error {
	lessonPlanID, err := uuid.Parse(c.Params("lessonPlanId"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid lesson plan ID"})
	}

	var request CreateLessonPlanSectionRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateSection(c.UserContext(), lessonPlanID, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) GetSectionByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid section ID"})
	}

	response, err := h.service.GetSectionByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Section not found"})
	}

	return c.JSON(response)
}

func (h *handler) GetSectionsByLessonPlan(c *fiber.Ctx) error {
	lessonPlanID, err := uuid.Parse(c.Params("lessonPlanId"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid lesson plan ID"})
	}

	response, err := h.service.GetSectionsByLessonPlan(lessonPlanID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) UpdateSection(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid section ID"})
	}

	var request UpdateLessonPlanSectionRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.UpdateSection(c.UserContext(), id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) DeleteSection(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid section ID"})
	}

	err = h.service.DeleteSection(c.UserContext(), id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Section deleted successfully"})
}

// Resource handlers (simplified)
func (h *handler) CreateResource(c *fiber.Ctx) error {
	lessonPlanID, err := uuid.Parse(c.Params("lessonPlanId"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid lesson plan ID"})
	}

	var request CreateLessonPlanResourceRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateResource(c.UserContext(), lessonPlanID, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) GetResourceByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid resource ID"})
	}

	response, err := h.service.GetResourceByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Resource not found"})
	}

	return c.JSON(response)
}

func (h *handler) GetResourcesByLessonPlan(c *fiber.Ctx) error {
	lessonPlanID, err := uuid.Parse(c.Params("lessonPlanId"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid lesson plan ID"})
	}

	response, err := h.service.GetResourcesByLessonPlan(lessonPlanID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) UpdateResource(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid resource ID"})
	}

	var request UpdateLessonPlanResourceRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.UpdateResource(c.UserContext(), id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) DeleteResource(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid resource ID"})
	}

	err = h.service.DeleteResource(c.UserContext(), id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Resource deleted successfully"})
}

func (h *handler) RegisterRoutes(group fiber.Router) {
	// Lesson Plan routes
	lessonPlans := group.Group("/lesson-plans")
	lessonPlans.Post("/", h.CreateLessonPlan)
	lessonPlans.Get("/", h.GetLessonPlans)
	lessonPlans.Get("/:id", h.GetLessonPlanByID)
	lessonPlans.Put("/:id", h.UpdateLessonPlan)
	lessonPlans.Delete("/:id", h.DeleteLessonPlan)
	lessonPlans.Post("/:id/copy", h.CopyLessonPlan)
	lessonPlans.Post("/from-template", h.CreateFromTemplate)

	// Template routes
	templates := group.Group("/lesson-plan-templates")
	templates.Post("/", h.CreateTemplate)
	templates.Get("/", h.GetTemplates)
	templates.Get("/:id", h.GetTemplateByID)
	templates.Put("/:id", h.UpdateTemplate)
	templates.Delete("/:id", h.DeleteTemplate)

	// Section routes
	sections := group.Group("/lesson-plans/:lessonPlanId/sections")
	sections.Post("/", h.CreateSection)
	sections.Get("/", h.GetSectionsByLessonPlan)
	sections.Get("/:id", h.GetSectionByID)
	sections.Put("/:id", h.UpdateSection)
	sections.Delete("/:id", h.DeleteSection)

	// Resource routes
	resources := group.Group("/lesson-plans/:lessonPlanId/resources")
	resources.Post("/", h.CreateResource)
	resources.Get("/", h.GetResourcesByLessonPlan)
	resources.Get("/:id", h.GetResourceByID)
	resources.Put("/:id", h.UpdateResource)
	resources.Delete("/:id", h.DeleteResource)
}
