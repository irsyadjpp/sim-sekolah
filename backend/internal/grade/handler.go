package grade

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type GradeHandler struct {
	svc GradeService
}

func NewGradeHandler(svc GradeService) *GradeHandler {
	return &GradeHandler{svc: svc}
}

// GetAllGradesHandler godoc
func (h *GradeHandler) GetAllGrades(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	data, total, err := h.svc.GetAll(c.UserContext(), pagination)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data kelas", err.Error())
	}
	return common.Paginated(c, "Data kelas berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetGradesByPhaseHandler godoc
func (h *GradeHandler) GetGradesByPhase(c *fiber.Ctx) error {
	data, err := h.svc.GetByPhaseID(c.UserContext(), c.Params("phaseId"))
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data kelas", err.Error())
	}
	return common.Success(c, "Data kelas berhasil diambil", data)
}

// GetGradeByIDHandler godoc
func (h *GradeHandler) GetGradeByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Kelas tidak ditemukan", err.Error())
	}
	return common.Success(c, "Detail kelas berhasil diambil", data)
}

// CreateGradeHandler godoc
func (h *GradeHandler) CreateGrade(c *fiber.Ctx) error {
	var req CreateGradeRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal membuat kelas", err.Error())
	}
	return common.Created(c, "Kelas berhasil dibuat", data)
}

// UpdateGradeHandler godoc
func (h *GradeHandler) UpdateGrade(c *fiber.Ctx) error {
	var req UpdateGradeRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}

	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal memperbarui kelas", err.Error())
	}
	return common.Success(c, "Kelas berhasil diperbarui", data)
}

// DeleteGradeHandler godoc
func (h *GradeHandler) DeleteGrade(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal menghapus kelas", err.Error())
	}
	return common.Success(c, "Kelas berhasil dihapus", nil)
}
