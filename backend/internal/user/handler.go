package user

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type UserHandler struct {
	svc UserService
}

func NewUserHandler(svc UserService) *UserHandler {
	return &UserHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Users
// @Tags Admin User Management
// @Produce json
// @Security BearerAuth
// @Param page   query int    false "Page"   default(1)
// @Param limit  query int    false "Limit"  default(10)
// @Param search query string false "Search by name or username"
// @Success 200 {object} common.PaginationResponse
// @Router /users [get]
func (h *UserHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")

	data, total, err := h.svc.GetAll(c.UserContext(), pagination, search)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data user", err)
	}
	return common.Paginated(c, "Data user berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

// GetByID godoc
// @Summary Get User By ID
// @Tags Admin User Management
// @Produce json
// @Security BearerAuth
// @Param id path string true "User ID"
// @Success 200 {object} common.Response
// @Router /users/{id} [get]
func (h *UserHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "User tidak ditemukan", err)
	}
	return common.Success(c, "Data user berhasil diambil", data)
}

// UpdateStatus godoc
// @Summary Update User Status
// @Tags Admin User Management
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string                  true "User ID"
// @Param request body UpdateUserStatusRequest true "Status Update Request"
// @Success 200 {object} common.Response
// @Router /users/{id}/status [patch]
func (h *UserHandler) UpdateStatus(c *fiber.Ctx) error {
	var req UpdateUserStatusRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	data, err := h.svc.UpdateStatus(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate status user", err)
	}
	return common.Success(c, "Status user berhasil diupdate", data)
}

// AssignRoles godoc
// @Summary Assign Roles
// @Tags Admin User Management
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string            true "User ID"
// @Param request body AssignRoleRequest true "Roles to Assign"
// @Success 200 {object} common.Response
// @Router /users/{id}/roles [put]
func (h *UserHandler) AssignRoles(c *fiber.Ctx) error {
	var req AssignRoleRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.AssignRoles(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengassign role", err)
	}
	return common.Success(c, "Role berhasil diassign", data)
}

// ResetPassword godoc
// @Summary Reset User Password
// @Tags Admin User Management
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string               true "User ID"
// @Param request body ResetPasswordRequest true "New Password"
// @Success 200 {object} common.Response
// @Router /users/{id}/reset-password [post]
func (h *UserHandler) ResetPassword(c *fiber.Ctx) error {
	var req ResetPasswordRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.ResetPassword(c.UserContext(), c.Params("id"), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mereset password", err)
	}
	return common.Success(c, "Password berhasil direset", nil)
}

// GetAllRoles godoc
// @Summary Get All Roles
// @Tags Admin User Management
// @Produce json
// @Security BearerAuth
// @Success 200 {object} common.Response
// @Router /users/roles [get]
func (h *UserHandler) GetAllRoles(c *fiber.Ctx) error {
	data, err := h.svc.GetAllRoles(c.UserContext())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data roles", err)
	}
	return common.Success(c, "Data roles berhasil diambil", data)
}
