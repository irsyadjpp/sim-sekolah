package academic_year

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type AcademicYearHandler struct {
	svc AcademicYearService
}

func NewAcademicYearHandler(svc AcademicYearService) *AcademicYearHandler {
	return &AcademicYearHandler{svc: svc}
}

// GetAllAcademicYearsHandler godoc
func (h *AcademicYearHandler) GetAllAcademicYears(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	data, total, err := h.svc.GetAll(c.UserContext(), pagination)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data tahun ajaran", err.Error())
	}
	return common.Paginated(c, "Data tahun ajaran berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetAcademicYearByIDHandler godoc
func (h *AcademicYearHandler) GetAcademicYearByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetByID(c.UserContext(), id)
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Tahun ajaran tidak ditemukan", err.Error())
	}
	return common.Success(c, "Detail tahun ajaran berhasil diambil", data)
}

// CreateAcademicYearHandler godoc
func (h *AcademicYearHandler) CreateAcademicYear(c *fiber.Ctx) error {
	var req CreateAcademicYearRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal membuat tahun ajaran", err.Error())
	}
	return common.Created(c, "Tahun ajaran berhasil dibuat", data)
}

// UpdateAcademicYearHandler godoc
func (h *AcademicYearHandler) UpdateAcademicYear(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateAcademicYearRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}

	data, err := h.svc.Update(c.UserContext(), id, req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal memperbarui tahun ajaran", err.Error())
	}
	return common.Success(c, "Tahun ajaran berhasil diperbarui", data)
}

// DeleteAcademicYearHandler godoc
func (h *AcademicYearHandler) DeleteAcademicYear(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.Delete(c.UserContext(), id); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal menghapus tahun ajaran", err.Error())
	}
	return common.Success(c, "Tahun ajaran berhasil dihapus", nil)
}

// SetActiveAcademicYearHandler godoc
func (h *AcademicYearHandler) SetActiveAcademicYear(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.SetActive(c.UserContext(), id); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengaktifkan tahun ajaran", err.Error())
	}
	return common.Success(c, "Tahun ajaran berhasil diaktifkan", nil)
}
