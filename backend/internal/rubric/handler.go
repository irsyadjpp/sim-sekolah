package rubric

import (
	"strconv"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type Handler interface {
	// Rubric routes
	CreateRubric(c *fiber.Ctx) error
	GetRubricByID(c *fiber.Ctx) error
	GetRubrics(c *fiber.Ctx) error
	UpdateRubric(c *fiber.Ctx) error
	DeleteRubric(c *fiber.Ctx) error
	GetRubricTemplates(c *fiber.Ctx) error
	CopyRubric(c *fiber.Ctx) error

	// RubricCriteria routes
	CreateCriteria(c *fiber.Ctx) error
	GetCriteriaByID(c *fiber.Ctx) error
	GetCriteriaByRubric(c *fiber.Ctx) error
	UpdateCriteria(c *fiber.Ctx) error
	DeleteCriteria(c *fiber.Ctx) error

	// RubricLevel routes
	CreateLevel(c *fiber.Ctx) error
	GetLevelByID(c *fiber.Ctx) error
	GetLevelsByRubric(c *fiber.Ctx) error
	UpdateLevel(c *fiber.Ctx) error
	DeleteLevel(c *fiber.Ctx) error

	// RubricCriteriaLevel routes
	CreateCriteriaLevel(c *fiber.Ctx) error
	GetCriteriaLevels(c *fiber.Ctx) error
	UpdateCriteriaLevel(c *fiber.Ctx) error
	DeleteCriteriaLevel(c *fiber.Ctx) error

	// Route registration
	RegisterRoutes(group fiber.Router)
}

type handler struct {
	service Service
}

func NewHandler(service Service) Handler {
	return &handler{service: service}
}

// Rubric handlers
func (h *handler) CreateRubric(c *fiber.Ctx) error {
	var request CreateRubricRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateRubric(c.UserContext(), request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) GetRubricByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid rubric ID"})
	}

	response, err := h.service.GetRubricByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Rubric not found"})
	}

	return c.JSON(response)
}

func (h *handler) GetRubrics(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if assessmentType := c.Query("assessment_type"); assessmentType != "" {
		filter["assessment_type"] = assessmentType
	}
	if subjectID := c.Query("subject_id"); subjectID != "" {
		filter["subject_id"] = subjectID
	}
	if gradeLevel := c.Query("grade_level"); gradeLevel != "" {
		filter["grade_level"] = gradeLevel
	}
	if isTemplateStr := c.Query("is_template"); isTemplateStr != "" {
		if isTemplate, err := strconv.ParseBool(isTemplateStr); err == nil {
			filter["is_template"] = isTemplate
		}
	}
	if isActiveStr := c.Query("is_active"); isActiveStr != "" {
		if isActive, err := strconv.ParseBool(isActiveStr); err == nil {
			filter["is_active"] = isActive
		}
	}

	response, err := h.service.GetRubrics(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) UpdateRubric(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid rubric ID"})
	}

	var request UpdateRubricRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.UpdateRubric(c.UserContext(), id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) DeleteRubric(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid rubric ID"})
	}

	err = h.service.DeleteRubric(c.UserContext(), id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Rubric deleted successfully"})
}

func (h *handler) GetRubricTemplates(c *fiber.Ctx) error {
	assessmentType := c.Query("assessment_type")

	response, err := h.service.GetRubricTemplates(assessmentType)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) CopyRubric(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid rubric ID"})
	}

	var request RubricCopyRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CopyRubric(c.UserContext(), id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

// RubricCriteria handlers
func (h *handler) CreateCriteria(c *fiber.Ctx) error {
	rubricID, err := uuid.Parse(c.Params("rubricId"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid rubric ID"})
	}

	var request CreateRubricCriteriaRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateCriteria(c.UserContext(), rubricID, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) GetCriteriaByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid criteria ID"})
	}

	response, err := h.service.GetCriteriaByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Criteria not found"})
	}

	return c.JSON(response)
}

func (h *handler) GetCriteriaByRubric(c *fiber.Ctx) error {
	rubricID, err := uuid.Parse(c.Params("rubricId"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid rubric ID"})
	}

	response, err := h.service.GetCriteriaByRubric(rubricID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) UpdateCriteria(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid criteria ID"})
	}

	var request UpdateRubricCriteriaRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.UpdateCriteria(c.UserContext(), id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) DeleteCriteria(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid criteria ID"})
	}

	err = h.service.DeleteCriteria(c.UserContext(), id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Criteria deleted successfully"})
}

// RubricLevel handlers
func (h *handler) CreateLevel(c *fiber.Ctx) error {
	rubricID, err := uuid.Parse(c.Params("rubricId"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid rubric ID"})
	}

	var request CreateRubricLevelRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateLevel(c.UserContext(), rubricID, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) GetLevelByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid level ID"})
	}

	response, err := h.service.GetLevelByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{"error": "Level not found"})
	}

	return c.JSON(response)
}

func (h *handler) GetLevelsByRubric(c *fiber.Ctx) error {
	rubricID, err := uuid.Parse(c.Params("rubricId"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid rubric ID"})
	}

	response, err := h.service.GetLevelsByRubric(rubricID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) UpdateLevel(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid level ID"})
	}

	var request UpdateRubricLevelRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.UpdateLevel(c.UserContext(), id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) DeleteLevel(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid level ID"})
	}

	err = h.service.DeleteLevel(c.UserContext(), id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Level deleted successfully"})
}

// RubricCriteriaLevel handlers
func (h *handler) CreateCriteriaLevel(c *fiber.Ctx) error {
	criteriaID, err := uuid.Parse(c.Params("criteriaId"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid criteria ID"})
	}

	var request CreateRubricCriteriaLevelRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.CreateCriteriaLevel(c.UserContext(), criteriaID, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *handler) GetCriteriaLevels(c *fiber.Ctx) error {
	criteriaID, err := uuid.Parse(c.Params("criteriaId"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid criteria ID"})
	}

	response, err := h.service.GetCriteriaLevels(criteriaID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) UpdateCriteriaLevel(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid criteria level ID"})
	}

	var request UpdateRubricCriteriaLevelRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": err.Error()})
	}

	response, err := h.service.UpdateCriteriaLevel(c.UserContext(), id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(response)
}

func (h *handler) DeleteCriteriaLevel(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{"error": "Invalid criteria level ID"})
	}

	err = h.service.DeleteCriteriaLevel(c.UserContext(), id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Criteria level deleted successfully"})
}

func (h *handler) RegisterRoutes(group fiber.Router) {
	// Rubric routes
	rubrics := group.Group("/rubrics")
	rubrics.Post("/", h.CreateRubric)
	rubrics.Get("/", h.GetRubrics)
	rubrics.Get("/templates", h.GetRubricTemplates)
	rubrics.Get("/:id", h.GetRubricByID)
	rubrics.Put("/:id", h.UpdateRubric)
	rubrics.Delete("/:id", h.DeleteRubric)
	rubrics.Post("/:id/copy", h.CopyRubric)

	// RubricCriteria routes
	criteria := group.Group("/rubrics/:rubricId/criteria")
	criteria.Post("/", h.CreateCriteria)
	criteria.Get("/", h.GetCriteriaByRubric)
	criteria.Get("/:id", h.GetCriteriaByID)
	criteria.Put("/:id", h.UpdateCriteria)
	criteria.Delete("/:id", h.DeleteCriteria)

	// RubricLevel routes
	levels := group.Group("/rubrics/:rubricId/levels")
	levels.Post("/", h.CreateLevel)
	levels.Get("/", h.GetLevelsByRubric)
	levels.Get("/:id", h.GetLevelByID)
	levels.Put("/:id", h.UpdateLevel)
	levels.Delete("/:id", h.DeleteLevel)

	// RubricCriteriaLevel routes
	criteriaLevels := group.Group("/rubrics/criteria/:criteriaId/levels")
	criteriaLevels.Post("/", h.CreateCriteriaLevel)
	criteriaLevels.Get("/", h.GetCriteriaLevels)
	criteriaLevels.Put("/:id", h.UpdateCriteriaLevel)
	criteriaLevels.Delete("/:id", h.DeleteCriteriaLevel)
}
