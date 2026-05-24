package olah_aspect

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"

	"github.com/gofiber/fiber/v2"
)

// OlahAspectHandler holds injected service dependency
type OlahAspectHandler struct {
	svc OlahAspectService
}

// NewOlahAspectHandler creates an OlahAspectHandler with injected OlahAspectService
func NewOlahAspectHandler(svc OlahAspectService) *OlahAspectHandler {
	return &OlahAspectHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Olah Aspects
// @Tags Olah Aspect
// @Produce json
// @Security BearerAuth
// @Param page   query int    false "Page"   default(1)
// @Param limit  query int    false "Limit"  default(10)
// @Param search query string false "Search by name, code, or definition"
// @Success 200 {object} common.PaginationResponse
// @Router /olah-aspects [get]
func (h *OlahAspectHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")
	data, total, err := h.svc.GetAll(pagination, search)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data aspek olah", err)
	}
	return common.Paginated(c, "Data aspek olah berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetByID godoc
// @Summary Get Olah Aspect By ID
// @Tags Olah Aspect
// @Produce json
// @Security BearerAuth
// @Param id path string true "Olah Aspect ID (UUID)"
// @Success 200 {object} common.Response
// @Router /olah-aspects/{id} [get]
func (h *OlahAspectHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Aspek olah tidak ditemukan", err)
	}
	return common.Success(c, "Detail aspek olah berhasil diambil", data)
}

// GetByCode godoc
// @Summary Get Olah Aspect By Code
// @Tags Olah Aspect
// @Produce json
// @Security BearerAuth
// @Param code path string true "Olah Aspect Code (e.g., OLAH_PIKIR)"
// @Success 200 {object} common.Response
// @Router /olah-aspects/code/{code} [get]
func (h *OlahAspectHandler) GetByCode(c *fiber.Ctx) error {
	data, err := h.svc.GetByCode(c.Params("code"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Aspek olah tidak ditemukan", err)
	}
	return common.Success(c, "Detail aspek olah berhasil diambil", data)
}

// Create godoc
// @Summary Create Olah Aspect
// @Tags Olah Aspect
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreateOlahAspectRequest true "Create Olah Aspect Request"
// @Success 201 {object} common.Response
// @Router /olah-aspects [post]
func (h *OlahAspectHandler) Create(c *fiber.Ctx) error {
	var req CreateOlahAspectRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		// Check if it's a validation error
		if err.Error() == "kode aspek olah tidak valid. Hanya 4 aspek olah yang diperbolehkan: OLAH_PIKIR, OLAH_HATI, OLAH_RASA, OLAH_RAGA" {
			return common.ErrorFromService(c, fiber.StatusBadRequest, err.Error(), err)
		}
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat aspek olah", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "CREATE", "olah_aspect", data.ID.String(), c.IP())
	}

	return common.Created(c, "Aspek olah berhasil dibuat", data)
}

// Update godoc
// @Summary Update Olah Aspect
// @Tags Olah Aspect
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string               true "Olah Aspect ID (UUID)"
// @Param request body UpdateOlahAspectRequest true "Update Olah Aspect Request"
// @Success 200 {object} common.Response
// @Router /olah-aspects/{id} [put]
func (h *OlahAspectHandler) Update(c *fiber.Ctx) error {
	var req UpdateOlahAspectRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		// Check if it's a validation error
		if err.Error() == "kode aspek olah tidak valid. Hanya 4 aspek olah yang diperbolehkan: OLAH_PIKIR, OLAH_HATI, OLAH_RASA, OLAH_RAGA" {
			return common.ErrorFromService(c, fiber.StatusBadRequest, err.Error(), err)
		}
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui aspek olah", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "UPDATE", "olah_aspect", c.Params("id"), c.IP())
	}

	return common.Success(c, "Aspek olah berhasil diperbarui", data)
}

// Delete godoc
// @Summary Delete Olah Aspect
// @Tags Olah Aspect
// @Produce json
// @Security BearerAuth
// @Param id path string true "Olah Aspect ID (UUID)"
// @Success 200 {object} common.Response
// @Router /olah-aspects/{id} [delete]
func (h *OlahAspectHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus aspek olah", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "olah_aspect", c.Params("id"), c.IP())
	}

	return common.Success(c, "Aspek olah berhasil dihapus", nil)
}
