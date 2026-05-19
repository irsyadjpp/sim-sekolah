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
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	operatorID, ok := c.Locals("user_id").(string)
	if !ok || operatorID == "" {
		return common.Error(c, fiber.StatusUnauthorized, "Tidak terautentikasi", "ID operator tidak ditemukan")
	}

	err := h.svc.PromoteStudents(c.UserContext(), req, operatorID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memproses kenaikan kelas", err)
	}
	return common.Success(c, "Kenaikan kelas massal berhasil diproses", nil)
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
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	err := h.svc.GraduateStudents(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memproses kelulusan murid", err)
	}
	return common.Success(c, "Kelulusan massal berhasil diproses", nil)
}
