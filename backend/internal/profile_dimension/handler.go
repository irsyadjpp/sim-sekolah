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
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data dimensi profil", err)
	}
	return common.Paginated(c, "Data dimensi profil berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

func (h *ProfileDimensionHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Dimensi profil tidak ditemukan", err)
	}
	return common.Success(c, "Detail dimensi profil berhasil diambil", data)
}

func (h *ProfileDimensionHandler) Create(c *fiber.Ctx) error {
	var req CreateProfileDimensionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		// Check if it's a validation error
		if err.Error() == "kode dimensi profil tidak valid. Hanya 8 dimensi profil lulusan Deep Learning yang diperbolehkan: DIM_KEIMANAN, DIM_KEWARGAAN, DIM_PENALARAN, DIM_KREATIVITAS, DIM_KOLABORASI, DIM_KEMANDIRIAN, DIM_KESEHATAN, DIM_KOMUNIKASI" {
			return common.ErrorFromService(c, fiber.StatusBadRequest, err.Error(), err)
		}
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat dimensi profil", err)
	}
	return common.Created(c, "Dimensi profil berhasil dibuat", data)
}

func (h *ProfileDimensionHandler) Update(c *fiber.Ctx) error {
	var req UpdateProfileDimensionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		// Check if it's a validation error
		if err.Error() == "kode dimensi profil tidak valid. Hanya 8 dimensi profil lulusan Deep Learning yang diperbolehkan: DIM_KEIMANAN, DIM_KEWARGAAN, DIM_PENALARAN, DIM_KREATIVITAS, DIM_KOLABORASI, DIM_KEMANDIRIAN, DIM_KESEHATAN, DIM_KOMUNIKASI" {
			return common.ErrorFromService(c, fiber.StatusBadRequest, err.Error(), err)
		}
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui dimensi profil", err)
	}
	return common.Success(c, "Dimensi profil berhasil diperbarui", data)
}

func (h *ProfileDimensionHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus dimensi profil", err)
	}
	return common.Success(c, "Dimensi profil berhasil dihapus", nil)
}
