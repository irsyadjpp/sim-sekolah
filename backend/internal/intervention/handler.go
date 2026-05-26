package intervention

import (
	"github.com/gofiber/fiber/v2"
)

type InterventionHandler struct {
	service InterventionService
}

func NewInterventionHandler(service InterventionService) *InterventionHandler {
	return &InterventionHandler{service: service}
}

// RemedialProgram handlers
func (h *InterventionHandler) CreateRemedialProgram(c *fiber.Ctx) error {
	var request RemedialProgramRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	program, err := h.service.CreateRemedialProgram(&request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Remedial program created successfully",
		"data":    program,
	})
}

func (h *InterventionHandler) GetRemedialProgramByID(c *fiber.Ctx) error {
	id := c.Params("id")
	program, err := h.service.GetRemedialProgramByID(id)
	if err != nil {
		return c.Status(404).JSON(fiber.Map{
			"status":  "error",
			"message": "Remedial program not found",
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data":   program,
	})
}

func (h *InterventionHandler) GetAllRemedialPrograms(c *fiber.Ctx) error {
	programs, err := h.service.GetAllRemedialPrograms()
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"programs": programs,
		},
	})
}

func (h *InterventionHandler) UpdateRemedialProgram(c *fiber.Ctx) error {
	id := c.Params("id")
	var request RemedialProgramRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	program, err := h.service.UpdateRemedialProgram(id, &request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Remedial program updated successfully",
		"data":    program,
	})
}

func (h *InterventionHandler) DeleteRemedialProgram(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.service.DeleteRemedialProgram(id); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Remedial program deleted successfully",
	})
}

// EnrichmentProgram handlers
func (h *InterventionHandler) CreateEnrichmentProgram(c *fiber.Ctx) error {
	var request EnrichmentProgramRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	program, err := h.service.CreateEnrichmentProgram(&request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Enrichment program created successfully",
		"data":    program,
	})
}

func (h *InterventionHandler) GetEnrichmentProgramByID(c *fiber.Ctx) error {
	id := c.Params("id")
	program, err := h.service.GetEnrichmentProgramByID(id)
	if err != nil {
		return c.Status(404).JSON(fiber.Map{
			"status":  "error",
			"message": "Enrichment program not found",
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data":   program,
	})
}

func (h *InterventionHandler) GetAllEnrichmentPrograms(c *fiber.Ctx) error {
	programs, err := h.service.GetAllEnrichmentPrograms()
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"programs": programs,
		},
	})
}

func (h *InterventionHandler) UpdateEnrichmentProgram(c *fiber.Ctx) error {
	id := c.Params("id")
	var request EnrichmentProgramRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	program, err := h.service.UpdateEnrichmentProgram(id, &request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Enrichment program updated successfully",
		"data":    program,
	})
}

func (h *InterventionHandler) DeleteEnrichmentProgram(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.service.DeleteEnrichmentProgram(id); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Enrichment program deleted successfully",
	})
}

// StudentAssignment handlers
func (h *InterventionHandler) CreateStudentAssignment(c *fiber.Ctx) error {
	var request StudentInterventionAssignmentRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	assignment, err := h.service.CreateStudentAssignment(&request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Student assignment created successfully",
		"data":    assignment,
	})
}

func (h *InterventionHandler) GetStudentAssignmentByID(c *fiber.Ctx) error {
	id := c.Params("id")
	assignment, err := h.service.GetStudentAssignmentByID(id)
	if err != nil {
		return c.Status(404).JSON(fiber.Map{
			"status":  "error",
			"message": "Student assignment not found",
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data":   assignment,
	})
}

func (h *InterventionHandler) GetAssignmentsByStudent(c *fiber.Ctx) error {
	studentID := c.Params("studentId")
	assignments, err := h.service.GetAssignmentsByStudent(studentID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"assignments": assignments,
		},
	})
}

func (h *InterventionHandler) UpdateStudentAssignment(c *fiber.Ctx) error {
	id := c.Params("id")
	var request StudentInterventionAssignmentRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	assignment, err := h.service.UpdateStudentAssignment(id, &request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Student assignment updated successfully",
		"data":    assignment,
	})
}

func (h *InterventionHandler) DeleteStudentAssignment(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.service.DeleteStudentAssignment(id); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Student assignment deleted successfully",
	})
}

// Summary handlers
func (h *InterventionHandler) GetInterventionSummary(c *fiber.Ctx) error {
	schoolID := c.Query("school_id")
	if schoolID == "" {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "school_id query parameter is required",
		})
	}

	summary, err := h.service.GetInterventionSummary(schoolID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data":   summary,
	})
}
