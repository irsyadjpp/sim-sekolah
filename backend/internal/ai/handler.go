package ai

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type AIHandler struct {
	svc AIService
}

func NewAIHandler(svc AIService) *AIHandler {
	return &AIHandler{svc: svc}
}

// GenerateNarrativeHandler godoc
func (h *AIHandler) GenerateNarrative(c *fiber.Ctx) error {
	var req GenerateNarrativeRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	narrative, err := h.svc.GenerateNarrative(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal generate narasi AI", err)
	}

	return common.Success(c, "Narasi berhasil di-generate", GenerateNarrativeResponse{Narrative: narrative})
}
