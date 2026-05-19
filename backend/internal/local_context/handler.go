package local_context

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type LocalContextHandler struct {
	svc LocalContextService
}

func NewLocalContextHandler(svc LocalContextService) *LocalContextHandler {
	return &LocalContextHandler{svc: svc}
}

// GetAllCategoriesHandler godoc
func (h *LocalContextHandler) GetAllCategories(c *fiber.Ctx) error {
	data, err := h.svc.GetAllCategories()
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil kategori konteks", err.Error())
	}
	return common.Success(c, "Kategori konteks berhasil diambil", data)
}

// GetAllContextsHandler godoc
func (h *LocalContextHandler) GetAllContexts(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")
	categoryID := c.Query("category_id", "")
	scopeType := c.Query("scope_type", "")

	data, total, err := h.svc.GetAll(pagination, search, categoryID, scopeType)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data konteks", err.Error())
	}

	return common.Paginated(c, "Data konteks berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// CreateContextHandler godoc
func (h *LocalContextHandler) CreateContext(c *fiber.Ctx) error {
	var req CreateContextRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal membuat konteks", err.Error())
	}
	return common.Created(c, "Konteks berhasil dibuat", data)
}

// UpdateContextHandler godoc
func (h *LocalContextHandler) UpdateContext(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateContextRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	data, err := h.svc.Update(c.UserContext(), id, req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal memperbarui konteks", err.Error())
	}
	return common.Success(c, "Konteks berhasil diperbarui", data)
}

// DeleteContextHandler godoc
func (h *LocalContextHandler) DeleteContext(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.Delete(c.UserContext(), id); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal menghapus konteks", err.Error())
	}
	return common.Success(c, "Konteks berhasil dihapus", nil)
}
