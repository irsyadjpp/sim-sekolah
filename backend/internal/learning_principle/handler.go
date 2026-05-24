package learning_principle

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"

	"github.com/gofiber/fiber/v2"
)

// LearningPrincipleHandler holds injected service dependency
type LearningPrincipleHandler struct {
	svc LearningPrincipleService
}

// NewLearningPrincipleHandler creates a LearningPrincipleHandler with injected LearningPrincipleService
func NewLearningPrincipleHandler(svc LearningPrincipleService) *LearningPrincipleHandler {
	return &LearningPrincipleHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Learning Principles
// @Tags Learning Principle
// @Produce json
// @Security BearerAuth
// @Param page   query int    false "Page"   default(1)
// @Param limit  query int    false "Limit"  default(10)
// @Param search query string false "Search by name, code, or description"
// @Success 200 {object} common.PaginationResponse
// @Router /learning-principles [get]
func (h *LearningPrincipleHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")
	data, total, err := h.svc.GetAll(pagination, search)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data prinsip pembelajaran", err)
	}
	return common.Paginated(c, "Data prinsip pembelajaran berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetByID godoc
// @Summary Get Learning Principle By ID
// @Tags Learning Principle
// @Produce json
// @Security BearerAuth
// @Param id path string true "Learning Principle ID (UUID)"
// @Success 200 {object} common.Response
// @Router /learning-principles/{id} [get]
func (h *LearningPrincipleHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Prinsip pembelajaran tidak ditemukan", err)
	}
	return common.Success(c, "Detail prinsip pembelajaran berhasil diambil", data)
}

// GetByCode godoc
// @Summary Get Learning Principle By Code
// @Tags Learning Principle
// @Produce json
// @Security BearerAuth
// @Param code path string true "Learning Principle Code (e.g., BERKESADARAN)"
// @Success 200 {object} common.Response
// @Router /learning-principles/code/{code} [get]
func (h *LearningPrincipleHandler) GetByCode(c *fiber.Ctx) error {
	data, err := h.svc.GetByCode(c.Params("code"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Prinsip pembelajaran tidak ditemukan", err)
	}
	return common.Success(c, "Detail prinsip pembelajaran berhasil diambil", data)
}

// Create godoc
// @Summary Create Learning Principle
// @Tags Learning Principle
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreateLearningPrincipleRequest true "Create Learning Principle Request"
// @Success 201 {object} common.Response
// @Router /learning-principles [post]
func (h *LearningPrincipleHandler) Create(c *fiber.Ctx) error {
	var req CreateLearningPrincipleRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		// Check if it's a validation error
		if err.Error() == "kode prinsip pembelajaran tidak valid. Hanya 3 prinsip pembelajaran yang diperbolehkan: BERKESADARAN, BERMAKNA, MENGENGIRAKAN" {
			return common.ErrorFromService(c, fiber.StatusBadRequest, err.Error(), err)
		}
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat prinsip pembelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "CREATE", "learning_principle", data.ID.String(), c.IP())
	}

	return common.Created(c, "Prinsip pembelajaran berhasil dibuat", data)
}

// Update godoc
// @Summary Update Learning Principle
// @Tags Learning Principle
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string                        true "Learning Principle ID (UUID)"
// @Param request body UpdateLearningPrincipleRequest true "Update Learning Principle Request"
// @Success 200 {object} common.Response
// @Router /learning-principles/{id} [put]
func (h *LearningPrincipleHandler) Update(c *fiber.Ctx) error {
	var req UpdateLearningPrincipleRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		// Check if it's a validation error
		if err.Error() == "kode prinsip pembelajaran tidak valid. Hanya 3 prinsip pembelajaran yang diperbolehkan: BERKESADARAN, BERMAKNA, MENGENGIRAKAN" {
			return common.ErrorFromService(c, fiber.StatusBadRequest, err.Error(), err)
		}
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui prinsip pembelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "UPDATE", "learning_principle", c.Params("id"), c.IP())
	}

	return common.Success(c, "Prinsip pembelajaran berhasil diperbarui", data)
}

// Delete godoc
// @Summary Delete Learning Principle
// @Tags Learning Principle
// @Produce json
// @Security BearerAuth
// @Param id path string true "Learning Principle ID (UUID)"
// @Success 200 {object} common.Response
// @Router /learning-principles/{id} [delete]
func (h *LearningPrincipleHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus prinsip pembelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "learning_principle", c.Params("id"), c.IP())
	}

	return common.Success(c, "Prinsip pembelajaran berhasil dihapus", nil)
}
