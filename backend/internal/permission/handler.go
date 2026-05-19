package permission

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type PermissionHandler struct {
	svc PermissionService
}

func NewPermissionHandler(svc PermissionService) *PermissionHandler {
	return &PermissionHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Permissions
// @Tags Admin Permission Management
// @Produce json
// @Security BearerAuth
// @Success 200 {object} common.Response
// @Router /permissions [get]
func (h *PermissionHandler) GetAll(c *fiber.Ctx) error {
	data, err := h.svc.GetAll(c.UserContext())
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data perizinan", err.Error())
	}
	return common.Success(c, "Data perizinan berhasil diambil", data)
}

// GetByID godoc
// @Summary Get Permission By ID
// @Tags Admin Permission Management
// @Produce json
// @Security BearerAuth
// @Param id path string true "Permission ID"
// @Success 200 {object} common.Response
// @Router /permissions/{id} [get]
func (h *PermissionHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Perizinan tidak ditemukan", err.Error())
	}
	return common.Success(c, "Data perizinan berhasil diambil", data)
}

// Create godoc
// @Summary Create New Permission
// @Tags Admin Permission Management
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body Permission true "Create Permission Request"
// @Success 201 {object} common.Response
// @Router /permissions [post]
func (h *PermissionHandler) Create(c *fiber.Ctx) error {
	var req Permission
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}

	if err := h.svc.Create(c.UserContext(), &req); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal membuat perizinan baru", err.Error())
	}
	return common.Success(c, "Perizinan baru berhasil dibuat", req)
}

// Delete godoc
// @Summary Delete Permission
// @Tags Admin Permission Management
// @Produce json
// @Security BearerAuth
// @Param id path string true "Permission ID"
// @Success 200 {object} common.Response
// @Router /permissions/{id} [delete]
func (h *PermissionHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal menghapus perizinan", err.Error())
	}
	return common.Success(c, "Perizinan berhasil dihapus", nil)
}

// GetPermissionsByRoleID godoc
// @Summary Get Permissions By Role ID
// @Tags Admin Permission Management
// @Produce json
// @Security BearerAuth
// @Param role_id path string true "Role ID"
// @Success 200 {object} common.Response
// @Router /permissions/roles/{role_id} [get]
func (h *PermissionHandler) GetPermissionsByRoleID(c *fiber.Ctx) error {
	data, err := h.svc.GetPermissionsByRoleID(c.UserContext(), c.Params("role_id"))
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data perizinan peran", err.Error())
	}
	return common.Success(c, "Data perizinan peran berhasil diambil", data)
}

// AssignPermissionsToRole godoc
// @Summary Assign Permissions To Role
// @Tags Admin Permission Management
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param role_id path string true "Role ID"
// @Param request body AssignPermissionsRequest true "Permissions to Assign"
// @Success 200 {object} common.Response
// @Router /permissions/roles/{role_id} [post]
func (h *PermissionHandler) AssignPermissionsToRole(c *fiber.Ctx) error {
	var req AssignPermissionsRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	err := h.svc.AssignPermissionsToRole(c.UserContext(), c.Params("role_id"), req.PermissionIDs)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal memetakan perizinan ke peran", err.Error())
	}
	return common.Success(c, "Perizinan peran berhasil diperbarui dan disinkronkan ke cache", nil)
}
