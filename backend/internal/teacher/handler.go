package teacher

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

// TeacherHandler holds injected service dependency.
type TeacherHandler struct {
	svc TeacherService
}

// NewTeacherHandler creates a TeacherHandler with an injected TeacherService.
func NewTeacherHandler(svc TeacherService) *TeacherHandler {
	return &TeacherHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Teachers
// @Description Ambil semua data guru dengan pencarian
// @Tags Teacher
// @Produce json
// @Security BearerAuth
// @Param page   query int    false "Page"   default(1)
// @Param limit  query int    false "Limit"  default(10)
// @Param search query string false "Search by name, NIP, email"
// @Success 200 {object} common.PaginationResponse
// @Router /teachers [get]
func (h *TeacherHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")

	data, total, err := h.svc.GetAll(c.UserContext(), pagination, search)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data guru", err)
	}
	return common.Paginated(c, "Data guru berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetBySchool godoc
// @Summary Get Teachers By School
// @Tags Teacher
// @Produce json
// @Security BearerAuth
// @Param schoolId path string true "School ID"
// @Success 200 {object} common.Response
// @Router /teachers/school/{schoolId} [get]
func (h *TeacherHandler) GetBySchool(c *fiber.Ctx) error {
	data, err := h.svc.GetBySchoolID(c.UserContext(), c.Params("schoolId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data guru", err)
	}
	return common.Success(c, "Data guru berhasil diambil", data)
}

// GetByID godoc
// @Summary Get Teacher By ID
// @Tags Teacher
// @Produce json
// @Security BearerAuth
// @Param id path string true "Teacher ID"
// @Success 200 {object} common.Response
// @Router /teachers/{id} [get]
func (h *TeacherHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Guru tidak ditemukan", err)
	}
	return common.Success(c, "Detail guru berhasil diambil", data)
}

// Create godoc
// @Summary Create Teacher
// @Tags Teacher
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreateTeacherRequest true "Create Teacher"
// @Success 201 {object} common.Response
// @Router /teachers [post]
func (h *TeacherHandler) Create(c *fiber.Ctx) error {
	var req CreateTeacherRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat data guru", err)
	}
	return common.Created(c, "Data guru berhasil dibuat", data)
}

// Update godoc
// @Summary Update Teacher
// @Tags Teacher
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id path string true "Teacher ID"
// @Param request body UpdateTeacherRequest true "Update Teacher"
// @Success 200 {object} common.Response
// @Router /teachers/{id} [put]
func (h *TeacherHandler) Update(c *fiber.Ctx) error {
	var req UpdateTeacherRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}

	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui data guru", err)
	}
	return common.Success(c, "Data guru berhasil diperbarui", data)
}

// Delete godoc
// @Summary Delete Teacher
// @Tags Teacher
// @Produce json
// @Security BearerAuth
// @Param id path string true "Teacher ID"
// @Success 200 {object} common.Response
// @Router /teachers/{id} [delete]
func (h *TeacherHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus data guru", err)
	}
	return common.Success(c, "Data guru berhasil dihapus", nil)
}
