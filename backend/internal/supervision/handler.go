package supervision

import (
	"github.com/gofiber/fiber/v2"
)

type SupervisionHandler struct {
	service SupervisionService
}

func NewSupervisionHandler(service SupervisionService) *SupervisionHandler {
	return &SupervisionHandler{service: service}
}

// SupervisionCycle handlers
func (h *SupervisionHandler) CreateCycle(c *fiber.Ctx) error {
	var request SupervisionCycleRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	cycle, err := h.service.CreateCycle(&request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Supervision cycle created successfully",
		"data":    cycle,
	})
}

func (h *SupervisionHandler) GetCycleByID(c *fiber.Ctx) error {
	id := c.Params("id")
	cycle, err := h.service.GetCycleByID(id)
	if err != nil {
		return c.Status(404).JSON(fiber.Map{
			"status":  "error",
			"message": "Supervision cycle not found",
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data":   cycle,
	})
}

func (h *SupervisionHandler) GetAllCycles(c *fiber.Ctx) error {
	cycles, err := h.service.GetAllCycles()
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"cycles": cycles,
		},
	})
}

func (h *SupervisionHandler) GetCyclesBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	cycles, err := h.service.GetCyclesBySchool(schoolID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"cycles": cycles,
		},
	})
}

func (h *SupervisionHandler) GetCyclesByAcademicYear(c *fiber.Ctx) error {
	academicYearID := c.Params("academicYearId")
	cycles, err := h.service.GetCyclesByAcademicYear(academicYearID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"cycles": cycles,
		},
	})
}

func (h *SupervisionHandler) GetActiveCycles(c *fiber.Ctx) error {
	cycles, err := h.service.GetActiveCycles()
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"cycles": cycles,
		},
	})
}

func (h *SupervisionHandler) UpdateCycle(c *fiber.Ctx) error {
	id := c.Params("id")
	var request SupervisionCycleRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	cycle, err := h.service.UpdateCycle(id, &request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Supervision cycle updated successfully",
		"data":    cycle,
	})
}

func (h *SupervisionHandler) DeleteCycle(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.service.DeleteCycle(id); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Supervision cycle deleted successfully",
	})
}

// TeacherObservation handlers
func (h *SupervisionHandler) CreateObservation(c *fiber.Ctx) error {
	var request TeacherObservationRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	observation, err := h.service.CreateObservation(&request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Observation created successfully",
		"data":    observation,
	})
}

func (h *SupervisionHandler) GetObservationByID(c *fiber.Ctx) error {
	id := c.Params("id")
	observation, err := h.service.GetObservationByID(id)
	if err != nil {
		return c.Status(404).JSON(fiber.Map{
			"status":  "error",
			"message": "Observation not found",
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data":   observation,
	})
}

func (h *SupervisionHandler) GetAllObservations(c *fiber.Ctx) error {
	observations, err := h.service.GetAllObservations()
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"observations": observations,
		},
	})
}

func (h *SupervisionHandler) GetObservationsByTeacher(c *fiber.Ctx) error {
	teacherID := c.Params("teacherId")
	observations, err := h.service.GetObservationsByTeacher(teacherID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"observations": observations,
		},
	})
}

func (h *SupervisionHandler) GetObservationsByObserver(c *fiber.Ctx) error {
	observerID := c.Params("observerId")
	observations, err := h.service.GetObservationsByObserver(observerID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"observations": observations,
		},
	})
}

func (h *SupervisionHandler) GetObservationsByCycle(c *fiber.Ctx) error {
	cycleID := c.Params("cycleId")
	observations, err := h.service.GetObservationsByCycle(cycleID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"observations": observations,
		},
	})
}

func (h *SupervisionHandler) GetObservationsByStatus(c *fiber.Ctx) error {
	status := c.Params("status")
	observations, err := h.service.GetObservationsByStatus(status)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"observations": observations,
		},
	})
}

func (h *SupervisionHandler) UpdateObservation(c *fiber.Ctx) error {
	id := c.Params("id")
	var request TeacherObservationRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	observation, err := h.service.UpdateObservation(id, &request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Observation updated successfully",
		"data":    observation,
	})
}

func (h *SupervisionHandler) DeleteObservation(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.service.DeleteObservation(id); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Observation deleted successfully",
	})
}

// SupervisionFeedback handlers
func (h *SupervisionHandler) CreateFeedback(c *fiber.Ctx) error {
	var request SupervisionFeedbackRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	feedback, err := h.service.CreateFeedback(&request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Feedback created successfully",
		"data":    feedback,
	})
}

func (h *SupervisionHandler) GetFeedbackByID(c *fiber.Ctx) error {
	id := c.Params("id")
	feedback, err := h.service.GetFeedbackByID(id)
	if err != nil {
		return c.Status(404).JSON(fiber.Map{
			"status":  "error",
			"message": "Feedback not found",
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data":   feedback,
	})
}

func (h *SupervisionHandler) GetAllFeedback(c *fiber.Ctx) error {
	feedbacks, err := h.service.GetAllFeedback()
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"feedbacks": feedbacks,
		},
	})
}

func (h *SupervisionHandler) GetFeedbackByTeacher(c *fiber.Ctx) error {
	teacherID := c.Params("teacherId")
	feedbacks, err := h.service.GetFeedbackByTeacher(teacherID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"feedbacks": feedbacks,
		},
	})
}

func (h *SupervisionHandler) GetFeedbackByObservation(c *fiber.Ctx) error {
	observationID := c.Params("observationId")
	feedbacks, err := h.service.GetFeedbackByObservation(observationID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"feedbacks": feedbacks,
		},
	})
}

func (h *SupervisionHandler) UpdateFeedback(c *fiber.Ctx) error {
	id := c.Params("id")
	var request SupervisionFeedbackRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	feedback, err := h.service.UpdateFeedback(id, &request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Feedback updated successfully",
		"data":    feedback,
	})
}

func (h *SupervisionHandler) DeleteFeedback(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.service.DeleteFeedback(id); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Feedback deleted successfully",
	})
}

// SupervisionAnalytics handlers
func (h *SupervisionHandler) GetAnalyticsBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	analytics, err := h.service.GetAnalyticsBySchool(schoolID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"analytics": analytics,
		},
	})
}

func (h *SupervisionHandler) GetAnalyticsByAcademicYear(c *fiber.Ctx) error {
	academicYearID := c.Params("academicYearId")
	analytics, err := h.service.GetAnalyticsByAcademicYear(academicYearID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"analytics": analytics,
		},
	})
}

func (h *SupervisionHandler) GetLatestAnalytics(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	analytics, err := h.service.GetLatestAnalytics(schoolID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data":   analytics,
	})
}

func (h *SupervisionHandler) GenerateAnalytics(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	academicYearID := c.Params("academicYearId")

	analytics, err := h.service.GenerateAnalytics(schoolID, academicYearID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Analytics generated successfully",
		"data":    analytics,
	})
}

// Summary handlers
func (h *SupervisionHandler) GetSupervisionSummary(c *fiber.Ctx) error {
	schoolID := c.Query("school_id")
	if schoolID == "" {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "school_id query parameter is required",
		})
	}

	summary, err := h.service.GetSupervisionSummary(schoolID)
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
