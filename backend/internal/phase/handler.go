package phase

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"

	"github.com/gofiber/fiber/v2"
)

// PhaseHandler holds injected service dependency.
type PhaseHandler struct {
	svc PhaseService
}

// NewPhaseHandler creates a PhaseHandler with an injected PhaseService.
func NewPhaseHandler(svc PhaseService) *PhaseHandler {
	return &PhaseHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Phases
// @Tags Phase
// @Produce json
// @Security BearerAuth
// @Param page   query int    false "Page"   default(1)
// @Param limit  query int    false "Limit"  default(10)
// @Param search query string false "Search by name or code"
// @Success 200 {object} common.PaginationResponse
// @Router /phases [get]
func (h *PhaseHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")
	data, total, err := h.svc.GetAll(pagination, search)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data fase", err.Error())
	}
	return common.Paginated(c, "Data fase berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetByID godoc
// @Summary Get Phase By ID
// @Tags Phase
// @Produce json
// @Security BearerAuth
// @Param id path string true "Phase ID (UUID)"
// @Success 200 {object} common.Response
// @Router /phases/{id} [get]
func (h *PhaseHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Fase tidak ditemukan", err.Error())
	}
	return common.Success(c, "Detail fase berhasil diambil", data)
}

// Create godoc
// @Summary Create Phase
// @Tags Phase
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreatePhaseRequest true "Create Phase Request"
// @Success 201 {object} common.Response
// @Router /phases [post]
func (h *PhaseHandler) Create(c *fiber.Ctx) error {
	var req CreatePhaseRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}
	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal membuat fase", err.Error())
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "CREATE", "phase", data.ID.String(), c.IP())
	}

	return common.Created(c, "Fase berhasil dibuat", data)
}

// Update godoc
// @Summary Update Phase
// @Tags Phase
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string            true "Phase ID (UUID)"
// @Param request body UpdatePhaseRequest true "Update Phase Request"
// @Success 200 {object} common.Response
// @Router /phases/{id} [put]
func (h *PhaseHandler) Update(c *fiber.Ctx) error {
	var req UpdatePhaseRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}
	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal memperbarui fase", err.Error())
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "UPDATE", "phase", c.Params("id"), c.IP())
	}

	return common.Success(c, "Fase berhasil diperbarui", data)
}

// Delete godoc
// @Summary Delete Phase
// @Tags Phase
// @Produce json
// @Security BearerAuth
// @Param id path string true "Phase ID (UUID)"
// @Success 200 {object} common.Response
// @Router /phases/{id} [delete]
func (h *PhaseHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal menghapus fase", err.Error())
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "phase", c.Params("id"), c.IP())
	}

	return common.Success(c, "Fase berhasil dihapus", nil)
}
