package subject

import (
	"strconv"

	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"

	"github.com/gofiber/fiber/v2"
)

// SubjectHandler holds injected service dependency.
type SubjectHandler struct {
	svc SubjectService
}

// NewSubjectHandler creates a SubjectHandler with an injected SubjectService.
func NewSubjectHandler(svc SubjectService) *SubjectHandler {
	return &SubjectHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Subjects
// @Tags Subject
// @Produce json
// @Security BearerAuth
// @Param page     query int    false "Page"     default(1)
// @Param limit    query int    false "Limit"    default(10)
// @Param search   query string false "Search by name or code"
// @Param is_active query bool   false "Filter by active status"
// @Success 200 {object} common.PaginationResponse
// @Router /subjects [get]
func (h *SubjectHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")

	var isActive *bool
	if isActiveQuery := c.Query("is_active"); isActiveQuery != "" {
		parsed, err := strconv.ParseBool(isActiveQuery)
		if err == nil {
			isActive = &parsed
		}
	}

	data, total, err := h.svc.GetAll(pagination, search, isActive)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data mata pelajaran", err)
	}
	return common.Paginated(c, "Data mata pelajaran berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetByID godoc
// @Summary Get Subject By ID
// @Tags Subject
// @Produce json
// @Security BearerAuth
// @Param id path string true "Subject ID (UUID)"
// @Success 200 {object} common.Response
// @Router /subjects/{id} [get]
func (h *SubjectHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Mata pelajaran tidak ditemukan", err)
	}
	return common.Success(c, "Detail mata pelajaran berhasil diambil", data)
}

// Create godoc
// @Summary Create Subject
// @Tags Subject
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreateSubjectRequest true "Create Subject Request"
// @Success 201 {object} common.Response
// @Router /subjects [post]
func (h *SubjectHandler) Create(c *fiber.Ctx) error {
	var req CreateSubjectRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat mata pelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "CREATE", "subject", data.ID.String(), c.IP())
	}

	return common.Created(c, "Mata pelajaran berhasil dibuat", data)
}

// Update godoc
// @Summary Update Subject
// @Tags Subject
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string               true "Subject ID (UUID)"
// @Param request body UpdateSubjectRequest true "Update Subject Request"
// @Success 200 {object} common.Response
// @Router /subjects/{id} [put]
func (h *SubjectHandler) Update(c *fiber.Ctx) error {
	var req UpdateSubjectRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui mata pelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "UPDATE", "subject", c.Params("id"), c.IP())
	}

	return common.Success(c, "Mata pelajaran berhasil diperbarui", data)
}

// Delete godoc
// @Summary Delete Subject
// @Tags Subject
// @Produce json
// @Security BearerAuth
// @Param id path string true "Subject ID (UUID)"
// @Success 200 {object} common.Response
// @Router /subjects/{id} [delete]
func (h *SubjectHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus mata pelajaran", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "subject", c.Params("id"), c.IP())
	}

	return common.Success(c, "Mata pelajaran berhasil dihapus", nil)
}

// ========================
// Subject Element Handlers
// ========================

// GetAllElements godoc
// @Summary Get All Subject Elements
// @Tags Subject Element
// @Produce json
// @Security BearerAuth
// @Param subjectId path string true "Subject ID (UUID)"
// @Success 200 {object} common.Response
// @Router /subjects/{subjectId}/elements [get]
func (h *SubjectHandler) GetAllElements(c *fiber.Ctx) error {
	data, err := h.svc.GetAllElements(c.Params("subjectId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data elemen", err)
	}
	return common.Success(c, "Data elemen berhasil diambil", data)
}

// CreateElement godoc
// @Summary Create Subject Element
// @Tags Subject Element
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param subjectId path string true "Subject ID (UUID)"
// @Param request body CreateSubjectElementRequest true "Create Element Request"
// @Success 201 {object} common.Response
// @Router /subjects/{subjectId}/elements [post]
func (h *SubjectHandler) CreateElement(c *fiber.Ctx) error {
	var req CreateSubjectElementRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.CreateElement(c.UserContext(), c.Params("subjectId"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat elemen", err)
	}
	return common.Created(c, "Elemen berhasil dibuat", data)
}

// UpdateElement godoc
// @Summary Update Subject Element
// @Tags Subject Element
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param subjectId path string true "Subject ID (UUID)"
// @Param id path string true "Element ID (UUID)"
// @Param request body UpdateSubjectElementRequest true "Update Element Request"
// @Success 200 {object} common.Response
// @Router /subjects/{subjectId}/elements/{id} [put]
func (h *SubjectHandler) UpdateElement(c *fiber.Ctx) error {
	var req UpdateSubjectElementRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.UpdateElement(c.UserContext(), c.Params("subjectId"), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui elemen", err)
	}
	return common.Success(c, "Elemen berhasil diperbarui", data)
}

// DeleteElement godoc
// @Summary Delete Subject Element
// @Tags Subject Element
// @Produce json
// @Security BearerAuth
// @Param subjectId path string true "Subject ID (UUID)"
// @Param id path string true "Element ID (UUID)"
// @Success 200 {object} common.Response
// @Router /subjects/{subjectId}/elements/{id} [delete]
func (h *SubjectHandler) DeleteElement(c *fiber.Ctx) error {
	if err := h.svc.DeleteElement(c.UserContext(), c.Params("subjectId"), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus elemen", err)
	}
	return common.Success(c, "Elemen berhasil dihapus", nil)
}
