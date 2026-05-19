package student

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"

	"github.com/gofiber/fiber/v2"
)

// StudentHandler holds injected service dependency.
type StudentHandler struct {
	svc StudentService
}

// NewStudentHandler creates a StudentHandler with an injected StudentService.
func NewStudentHandler(svc StudentService) *StudentHandler {
	return &StudentHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Students
// @Tags Student
// @Produce json
// @Security BearerAuth
// @Param page   query int    false "Page"   default(1)
// @Param limit  query int    false "Limit"  default(10)
// @Param search query string false "Search by name, NISN, or NIS"
// @Success 200 {object} common.PaginationResponse
// @Router /students [get]
func (h *StudentHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")
	data, total, err := h.svc.GetAll(c.UserContext(), pagination, search)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data siswa", err)
	}
	return common.Paginated(c, "Data siswa berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetBySchool godoc
// @Summary Get Students By School
// @Tags Student
// @Produce json
// @Security BearerAuth
// @Param schoolId path string true "School ID"
// @Success 200 {object} common.Response
// @Router /students/school/{schoolId} [get]
func (h *StudentHandler) GetBySchool(c *fiber.Ctx) error {
	data, err := h.svc.GetBySchoolID(c.UserContext(), c.Params("schoolId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data siswa", err)
	}
	return common.Success(c, "Data siswa berhasil diambil", data)
}

// GetByID godoc
// @Summary Get Student By ID (lengkap dengan data orang tua)
// @Tags Student
// @Produce json
// @Security BearerAuth
// @Param id path string true "Student ID"
// @Success 200 {object} common.Response
// @Router /students/{id} [get]
func (h *StudentHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Siswa tidak ditemukan", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "READ", "student", c.Params("id"), c.IP())
	}

	return common.Success(c, "Detail siswa berhasil diambil", data)
}

// Create godoc
// @Summary Create Student
// @Tags Student
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreateStudentRequest true "Create Student"
// @Success 201 {object} common.Response
// @Router /students [post]
func (h *StudentHandler) Create(c *fiber.Ctx) error {
	var req CreateStudentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat data siswa", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "CREATE", "student", data.ID.String(), c.IP())
	}

	return common.Created(c, "Data siswa berhasil dibuat", data)
}

// Update godoc
// @Summary Update Student
// @Tags Student
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id path string true "Student ID"
// @Param request body UpdateStudentRequest true "Update Student"
// @Success 200 {object} common.Response
// @Router /students/{id} [put]
func (h *StudentHandler) Update(c *fiber.Ctx) error {
	var req UpdateStudentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui data siswa", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "UPDATE", "student", c.Params("id"), c.IP())
	}

	return common.Success(c, "Data siswa berhasil diperbarui", data)
}

// Delete godoc
// @Summary Delete Student
// @Tags Student
// @Produce json
// @Security BearerAuth
// @Param id path string true "Student ID"
// @Success 200 {object} common.Response
// @Router /students/{id} [delete]
func (h *StudentHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus data siswa", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "student", c.Params("id"), c.IP())
	}

	return common.Success(c, "Data siswa berhasil dihapus", nil)
}

// ============================================================
// PARENT HANDLERS
// ============================================================

// UpsertParent godoc
// @Summary Upsert Parent Data
// @Description Tambah atau perbarui data orang tua (FATHER, MOTHER, GUARDIAN)
// @Tags Student
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string              true "Student ID"
// @Param request body UpsertParentRequest true "Parent Data"
// @Success 200 {object} common.Response
// @Router /students/{id}/parents [post]
func (h *StudentHandler) UpsertParent(c *fiber.Ctx) error {
	studentID := c.Params("id")
	var req UpsertParentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.UpsertParent(c.UserContext(), studentID, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menyimpan data orang tua", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "UPDATE", "student_parent", studentID, c.IP())
	}

	return common.Success(c, "Data orang tua berhasil disimpan", data)
}

// DeleteParent godoc
// @Summary Delete Parent Data
// @Tags Student
// @Produce json
// @Security BearerAuth
// @Param id       path string true "Student ID"
// @Param parentId path string true "Parent ID"
// @Success 200 {object} common.Response
// @Router /students/{id}/parents/{parentId} [delete]
func (h *StudentHandler) DeleteParent(c *fiber.Ctx) error {
	if err := h.svc.DeleteParent(c.UserContext(), c.Params("id"), c.Params("parentId")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus data orang tua", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "student_parent", c.Params("parentId"), c.IP())
	}

	return common.Success(c, "Data orang tua berhasil dihapus", nil)
}
