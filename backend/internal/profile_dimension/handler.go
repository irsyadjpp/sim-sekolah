package profile_dimension

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type ProfileDimensionHandler struct {
	svc ProfileDimensionService
}

func NewProfileDimensionHandler(svc ProfileDimensionService) *ProfileDimensionHandler {
	return &ProfileDimensionHandler{svc: svc}
}

func (h *ProfileDimensionHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")

	data, total, err := h.svc.GetAll(pagination, search)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data dimensi profil", err.Error())
	}
	return common.Paginated(c, "Data dimensi profil berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

func (h *ProfileDimensionHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Dimensi profil tidak ditemukan", err.Error())
	}
	return common.Success(c, "Detail dimensi profil berhasil diambil", data)
}

func (h *ProfileDimensionHandler) Create(c *fiber.Ctx) error {
	var req CreateProfileDimensionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}
	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal membuat dimensi profil", err.Error())
	}
	return common.Created(c, "Dimensi profil berhasil dibuat", data)
}

func (h *ProfileDimensionHandler) Update(c *fiber.Ctx) error {
	var req UpdateProfileDimensionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}
	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal memperbarui dimensi profil", err.Error())
	}
	return common.Success(c, "Dimensi profil berhasil diperbarui", data)
}

func (h *ProfileDimensionHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal menghapus dimensi profil", err.Error())
	}
	return common.Success(c, "Dimensi profil berhasil dihapus", nil)
}
