package school

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

// SchoolHandler holds injected service dependency.
type SchoolHandler struct {
	svc SchoolService
}

// NewSchoolHandler creates a SchoolHandler with an injected SchoolService.
func NewSchoolHandler(svc SchoolService) *SchoolHandler {
	return &SchoolHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Schools
// @Tags School
// @Produce json
// @Security BearerAuth
// @Param page   query int    false "Page"   default(1)
// @Param limit  query int    false "Limit"  default(10)
// @Param search query string false "Search by name or NPSN"
// @Success 200 {object} common.PaginationResponse
// @Router /schools [get]
func (h *SchoolHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")
	data, total, err := h.svc.GetAll(c.UserContext(), pagination, search)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data sekolah", err)
	}
	return common.Paginated(c, "Data sekolah berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetByID godoc
// @Summary Get School By ID
// @Tags School
// @Produce json
// @Security BearerAuth
// @Param id path string true "School ID"
// @Success 200 {object} common.Response
// @Router /schools/{id} [get]
func (h *SchoolHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Sekolah tidak ditemukan", err)
	}
	return common.Success(c, "Detail sekolah berhasil diambil", data)
}

// Create godoc
// @Summary Create School
// @Tags School
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreateSchoolRequest true "Create School"
// @Success 201 {object} common.Response
// @Router /schools [post]
func (h *SchoolHandler) Create(c *fiber.Ctx) error {
	var req CreateSchoolRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat sekolah", err)
	}
	return common.Created(c, "Sekolah berhasil dibuat", data)
}

// Update godoc
// @Summary Update School
// @Tags School
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string            true "School ID"
// @Param request body UpdateSchoolRequest true "Update School"
// @Success 200 {object} common.Response
// @Router /schools/{id} [put]
func (h *SchoolHandler) Update(c *fiber.Ctx) error {
	var req UpdateSchoolRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui sekolah", err)
	}
	return common.Success(c, "Sekolah berhasil diperbarui", data)
}

// Delete godoc
// @Summary Delete School
// @Tags School
// @Produce json
// @Security BearerAuth
// @Param id path string true "School ID"
// @Success 200 {object} common.Response
// @Router /schools/{id} [delete]
func (h *SchoolHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus sekolah", err)
	}
	return common.Success(c, "Sekolah berhasil dihapus", nil)
}
