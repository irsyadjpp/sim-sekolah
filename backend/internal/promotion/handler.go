package promotion

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type PromotionHandler struct {
	svc PromotionService
}

func NewPromotionHandler(svc PromotionService) *PromotionHandler {
	return &PromotionHandler{svc: svc}
}

// Promote godoc
// @Summary Promote Students to Next Classroom
// @Tags Admin Promotion Management
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body PromoteRequest true "Promotion Request"
// @Success 200 {object} common.Response
// @Router /academic/promotion [post]
func (h *PromotionHandler) Promote(c *fiber.Ctx) error {
	var req PromoteRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}

	operatorID, ok := c.Locals("user_id").(string)
	if !ok || operatorID == "" {
		return common.Error(c, fiber.StatusUnauthorized, "Unauthorized", "Operator ID missing")
	}

	err := h.svc.PromoteStudents(c.UserContext(), req, operatorID)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to process class promotion", err.Error())
	}
	return common.Success(c, "Mass student class promotion processed successfully", nil)
}

// Graduate godoc
// @Summary Graduate Students Massively
// @Tags Admin Promotion Management
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body GraduateRequest true "Graduation Request"
// @Success 200 {object} common.Response
// @Router /academic/graduation [post]
func (h *PromotionHandler) Graduate(c *fiber.Ctx) error {
	var req GraduateRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}

	err := h.svc.GraduateStudents(c.UserContext(), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to process student graduation", err.Error())
	}
	return common.Success(c, "Mass student graduation processed successfully", nil)
}
