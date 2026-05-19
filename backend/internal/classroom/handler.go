package classroom

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type ClassroomHandler struct {
	svc ClassroomService
}

func NewClassroomHandler(svc ClassroomService) *ClassroomHandler {
	return &ClassroomHandler{svc: svc}
}

// GetAllClassroomsHandler godoc
func (h *ClassroomHandler) GetAllClassrooms(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	schoolID := c.Query("schoolId", "")
	data, total, err := h.svc.GetAll(c.UserContext(), pagination, schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data rombel", err)
	}
	return common.Paginated(c, "Data rombel berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetClassroomByIDHandler godoc
func (h *ClassroomHandler) GetClassroomByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Rombel tidak ditemukan", err)
	}
	return common.Success(c, "Detail rombel berhasil diambil", data)
}

// CreateClassroomHandler godoc
func (h *ClassroomHandler) CreateClassroom(c *fiber.Ctx) error {
	var req CreateClassroomRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat rombel", err)
	}
	return common.Created(c, "Rombel berhasil dibuat", data)
}

// UpdateClassroomHandler godoc
func (h *ClassroomHandler) UpdateClassroom(c *fiber.Ctx) error {
	var req UpdateClassroomRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}

	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui rombel", err)
	}
	return common.Success(c, "Rombel berhasil diperbarui", data)
}

// DeleteClassroomHandler godoc
func (h *ClassroomHandler) DeleteClassroom(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus rombel", err)
	}
	return common.Success(c, "Rombel berhasil dihapus", nil)
}
