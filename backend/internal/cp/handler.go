package cp

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"

	"github.com/gofiber/fiber/v2"
)

// CPHandler holds injected service dependency.
type CPHandler struct {
	svc CPService
}

// NewCPHandler creates a CPHandler with an injected CPService.
func NewCPHandler(svc CPService) *CPHandler {
	return &CPHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Learning Outcomes
// @Tags Learning Outcomes
// @Produce json
// @Security BearerAuth
// @Param page   query int    false "Page"   default(1)
// @Param limit  query int    false "Limit"  default(10)
// @Param search query string false "Search by text or code"
// @Success 200 {object} common.PaginationResponse
// @Router /learning-outcomes [get]
func (h *CPHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")
	data, total, err := h.svc.GetAll(pagination, search)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil capaian pembelajaran", err)
	}
	return common.Paginated(c, "Capaian pembelajaran berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetByID godoc
// @Summary Get Learning Outcome By ID
// @Tags Learning Outcomes
// @Produce json
// @Security BearerAuth
// @Param id path string true "Learning Outcome ID (UUID)"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{id} [get]
func (h *CPHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Capaian pembelajaran tidak ditemukan", err)
	}
	return common.Success(c, "Capaian pembelajaran berhasil diambil", data)
}

// Create godoc
// @Summary Create Learning Outcome
// @Tags Learning Outcomes
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreateCPRequest true "Create Learning Outcome Request"
// @Success 201 {object} common.Response
// @Router /learning-outcomes [post]
func (h *CPHandler) Create(c *fiber.Ctx) error {
	var req CreateCPRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat capaian pembelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "CREATE", "learning_outcome", data.ID.String(), c.IP())
	}

	return common.Created(c, "Capaian pembelajaran berhasil dibuat", data)
}

// Update godoc
// @Summary Update Learning Outcome
// @Tags Learning Outcomes
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string          true "Learning Outcome ID (UUID)"
// @Param request body UpdateCPRequest true "Update Learning Outcome Request"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{id} [put]
func (h *CPHandler) Update(c *fiber.Ctx) error {
	var req UpdateCPRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui capaian pembelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "UPDATE", "learning_outcome", data.ID.String(), c.IP())
	}

	return common.Success(c, "Capaian pembelajaran berhasil diperbarui", data)
}

// Delete godoc
// @Summary Delete Learning Outcome
// @Tags Learning Outcomes
// @Produce json
// @Security BearerAuth
// @Param id path string true "Learning Outcome ID (UUID)"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{id} [delete]
func (h *CPHandler) Delete(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.Delete(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus capaian pembelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "learning_outcome", id, c.IP())
	}

	return common.Success(c, "Capaian pembelajaran berhasil dihapus", nil)
}

// ========================
// Detail Handlers
// ========================

// GetAllDetails godoc
// @Summary Get All Learning Outcome Details
// @Tags Learning Outcome Details
// @Produce json
// @Security BearerAuth
// @Param cpId path string true "Learning Outcome ID (UUID)"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{cpId}/details [get]
func (h *CPHandler) GetAllDetails(c *fiber.Ctx) error {
	data, err := h.svc.GetAllDetails(c.Params("cpId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil detail capaian pembelajaran", err)
	}
	return common.Success(c, "Detail capaian pembelajaran berhasil diambil", data)
}

// CreateDetail godoc
// @Summary Create Learning Outcome Detail
// @Tags Learning Outcome Details
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param cpId    path string                true "Learning Outcome ID (UUID)"
// @Param request body CreateCPDetailRequest true "Create Detail Request"
// @Success 201 {object} common.Response
// @Router /learning-outcomes/{cpId}/details [post]
func (h *CPHandler) CreateDetail(c *fiber.Ctx) error {
	var req CreateCPDetailRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.CreateDetail(c.UserContext(), c.Params("cpId"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat detail", err)
	}
	return common.Created(c, "Detail berhasil dibuat", data)
}

// UpdateDetail godoc
// @Summary Update Learning Outcome Detail
// @Tags Learning Outcome Details
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param cpId    path string                true "Learning Outcome ID (UUID)"
// @Param id      path string                true "Detail ID (UUID)"
// @Param request body UpdateCPDetailRequest true "Update Detail Request"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{cpId}/details/{id} [put]
func (h *CPHandler) UpdateDetail(c *fiber.Ctx) error {
	var req UpdateCPDetailRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.UpdateDetail(c.UserContext(), c.Params("cpId"), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui detail", err)
	}
	return common.Success(c, "Detail berhasil diperbarui", data)
}

// DeleteDetail godoc
// @Summary Delete Learning Outcome Detail
// @Tags Learning Outcome Details
// @Produce json
// @Security BearerAuth
// @Param cpId path string true "Learning Outcome ID (UUID)"
// @Param id   path string true "Detail ID (UUID)"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{cpId}/details/{id} [delete]
func (h *CPHandler) DeleteDetail(c *fiber.Ctx) error {
	if err := h.svc.DeleteDetail(c.UserContext(), c.Params("cpId"), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus detail", err)
	}
	return common.Success(c, "Detail berhasil dihapus", nil)
}

// TP Handlers
func (h *CPHandler) GetAllObjectives(c *fiber.Ctx) error {
	data, err := h.svc.GetAllObjectives(c.Params("cpId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil tujuan pembelajaran", err)
	}
	return common.Success(c, "Tujuan pembelajaran berhasil diambil", data)
}

func (h *CPHandler) CreateObjective(c *fiber.Ctx) error {
	var req CreateTPRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.CreateObjective(c.UserContext(), c.Params("cpId"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat tujuan pembelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "CREATE", "learning_objective", data.ID.String(), c.IP())
	}

	return common.Created(c, "Tujuan pembelajaran berhasil dibuat", data)
}

func (h *CPHandler) GetObjectiveByID(c *fiber.Ctx) error {
	data, err := h.svc.GetObjectiveByID(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Tujuan pembelajaran tidak ditemukan", err)
	}
	return common.Success(c, "Tujuan pembelajaran berhasil diambil", data)
}

func (h *CPHandler) UpdateObjective(c *fiber.Ctx) error {
	var req UpdateTPRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.UpdateObjective(c.UserContext(), c.Params("cpId"), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate tujuan pembelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "UPDATE", "learning_objective", data.ID.String(), c.IP())
	}

	return common.Success(c, "Tujuan pembelajaran berhasil diupdate", data)
}

func (h *CPHandler) DeleteObjective(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteObjective(c.UserContext(), c.Params("cpId"), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus tujuan pembelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "learning_objective", id, c.IP())
	}

	return common.Success(c, "Tujuan pembelajaran berhasil dihapus", nil)
}
