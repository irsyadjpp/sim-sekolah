package teaching_reflection

import (
	"github.com/gofiber/fiber/v2"
)

type TeachingReflectionHandler struct {
	service TeachingReflectionService
}

func NewTeachingReflectionHandler(service TeachingReflectionService) *TeachingReflectionHandler {
	return &TeachingReflectionHandler{service: service}
}

func (h *TeachingReflectionHandler) CreateReflection(c *fiber.Ctx) error {
	var request TeachingReflectionRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	reflection, err := h.service.CreateReflection(&request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Teaching reflection created successfully",
		"data":    reflection,
	})
}

func (h *TeachingReflectionHandler) GetReflectionByID(c *fiber.Ctx) error {
	id := c.Params("id")
	reflection, err := h.service.GetReflectionByID(id)
	if err != nil {
		return c.Status(404).JSON(fiber.Map{
			"status":  "error",
			"message": "Reflection not found",
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data":   reflection,
	})
}

func (h *TeachingReflectionHandler) GetReflectionsByTeacher(c *fiber.Ctx) error {
	teacherID := c.Params("teacherId")
	reflections, err := h.service.GetReflectionsByTeacher(teacherID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status": "success",
		"data": fiber.Map{
			"reflections": reflections,
		},
	})
}

func (h *TeachingReflectionHandler) UpdateReflection(c *fiber.Ctx) error {
	id := c.Params("id")
	var request TeachingReflectionRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	reflection, err := h.service.UpdateReflection(id, &request)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Teaching reflection updated successfully",
		"data":    reflection,
	})
}

func (h *TeachingReflectionHandler) DeleteReflection(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.service.DeleteReflection(id); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": err.Error(),
		})
	}

	return c.JSON(fiber.Map{
		"status":  "success",
		"message": "Teaching reflection deleted successfully",
	})
}

func (h *TeachingReflectionHandler) GetReflectionSummary(c *fiber.Ctx) error {
	teacherID := c.Params("teacherId")
	summary, err := h.service.GetReflectionSummary(teacherID)
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
