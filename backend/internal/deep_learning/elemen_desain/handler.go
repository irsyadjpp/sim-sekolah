package elemen_desain

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type Handler struct {
	service Service
}

func NewHandler(service Service) *Handler {
	return &Handler{service: service}
}

// RegisterRoutes registers the design element routes
func (h *Handler) RegisterRoutes(group fiber.Router) {
	designElements := group.Group("/elemen-desain")
	{
		designElements.Get("", h.GetAll)
		designElements.Get("/framework-groups", h.GetFrameworkGroups)
		designElements.Get("/framework/:type", h.GetByFrameworkType)
		designElements.Get("/:id", h.GetByID)
		designElements.Post("", h.Create)
		designElements.Put("/:id", h.Update)
		designElements.Delete("/:id", h.Delete)
	}
}

// GetAll handles GET /elemen-desain
func (h *Handler) GetAll(c *fiber.Ctx) error {
	elements, err := h.service.GetAll()
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil elemen desain", err)
	}

	return common.Success(c, "Elemen desain berhasil diambil", fiber.Map{
		"elements": elements,
		"total":    len(elements),
	})
}

// GetFrameworkGroups handles GET /elemen-desain/framework-groups
func (h *Handler) GetFrameworkGroups(c *fiber.Ctx) error {
	groups, err := h.service.GetFrameworkGroups()
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil grup framework", err)
	}

	return common.Success(c, "Grup framework berhasil diambil", fiber.Map{"groups": groups})
}

// GetByFrameworkType handles GET /elemen-desain/framework/:type
func (h *Handler) GetByFrameworkType(c *fiber.Ctx) error {
	frameworkType := c.Params("type")
	if frameworkType == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Tipe framework diperlukan", nil)
	}

	elements, err := h.service.GetByFrameworkType(frameworkType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, err.Error(), err)
	}

	return common.Success(c, "Elemen desain berhasil diambil", fiber.Map{
		"elements": elements,
		"total":    len(elements),
	})
}

// GetByID handles GET /elemen-desain/:id
func (h *Handler) GetByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	element, err := h.service.GetByID(id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Elemen desain tidak ditemukan", err)
	}

	return common.Success(c, "Elemen desain berhasil diambil", element)
}

// Create handles POST /elemen-desain
func (h *Handler) Create(c *fiber.Ctx) error {
	var req CreateDesignElementRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	element, err := h.service.Create(req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat elemen desain", err)
	}

	return common.Success(c, "Elemen desain berhasil dibuat", element)
}

// Update handles PUT /elemen-desain/:id
func (h *Handler) Update(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	var req UpdateDesignElementRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	element, err := h.service.Update(id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate elemen desain", err)
	}

	return common.Success(c, "Elemen desain berhasil diupdate", element)
}

// Delete handles DELETE /elemen-desain/:id
func (h *Handler) Delete(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	if err := h.service.Delete(id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus elemen desain", err)
	}

	return common.Success(c, "Elemen desain berhasil dihapus", nil)
}
