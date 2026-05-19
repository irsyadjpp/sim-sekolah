package cp

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"

	"github.com/gofiber/fiber/v2"
)

// CPHandler holds injected service dependency.
type CPHandler struct {
	svc CPService
}

// NewCPHandler creates a CPHandler with an injected CPService.
func NewCPHandler(svc CPService) *CPHandler {
	return &CPHandler{svc: svc}
}

// GetAll godoc
// @Summary Get All Learning Outcomes
// @Tags Learning Outcomes
// @Produce json
// @Security BearerAuth
// @Param page   query int    false "Page"   default(1)
// @Param limit  query int    false "Limit"  default(10)
// @Param search query string false "Search by text or code"
// @Success 200 {object} common.PaginationResponse
// @Router /learning-outcomes [get]
func (h *CPHandler) GetAll(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")
	data, total, err := h.svc.GetAll(pagination, search)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to fetch learning outcomes", err.Error())
	}
	return common.Paginated(c, "Learning outcomes retrieved successfully", data, pagination.Page, pagination.Limit, total)
}

// GetByID godoc
// @Summary Get Learning Outcome By ID
// @Tags Learning Outcomes
// @Produce json
// @Security BearerAuth
// @Param id path string true "Learning Outcome ID (UUID)"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{id} [get]
func (h *CPHandler) GetByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Learning outcome not found", err.Error())
	}
	return common.Success(c, "Learning outcome retrieved successfully", data)
}

// Create godoc
// @Summary Create Learning Outcome
// @Tags Learning Outcomes
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreateCPRequest true "Create Learning Outcome Request"
// @Success 201 {object} common.Response
// @Router /learning-outcomes [post]
func (h *CPHandler) Create(c *fiber.Ctx) error {
	var req CreateCPRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}
	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to create learning outcome", err.Error())
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "CREATE", "learning_outcome", data.ID.String(), c.IP())
	}

	return common.Created(c, "Learning outcome created successfully", data)
}

// Update godoc
// @Summary Update Learning Outcome
// @Tags Learning Outcomes
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param id      path string          true "Learning Outcome ID (UUID)"
// @Param request body UpdateCPRequest true "Update Learning Outcome Request"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{id} [put]
func (h *CPHandler) Update(c *fiber.Ctx) error {
	var req UpdateCPRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}
	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to update learning outcome", err.Error())
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "UPDATE", "learning_outcome", data.ID.String(), c.IP())
	}

	return common.Success(c, "Learning outcome updated successfully", data)
}

// Delete godoc
// @Summary Delete Learning Outcome
// @Tags Learning Outcomes
// @Produce json
// @Security BearerAuth
// @Param id path string true "Learning Outcome ID (UUID)"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{id} [delete]
func (h *CPHandler) Delete(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.Delete(c.UserContext(), id); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to delete learning outcome", err.Error())
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "learning_outcome", id, c.IP())
	}

	return common.Success(c, "Learning outcome deleted successfully", nil)
}

// ========================
// Detail Handlers
// ========================

// GetAllDetails godoc
// @Summary Get All Learning Outcome Details
// @Tags Learning Outcome Details
// @Produce json
// @Security BearerAuth
// @Param cpId path string true "Learning Outcome ID (UUID)"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{cpId}/details [get]
func (h *CPHandler) GetAllDetails(c *fiber.Ctx) error {
	data, err := h.svc.GetAllDetails(c.Params("cpId"))
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to fetch learning outcome details", err.Error())
	}
	return common.Success(c, "Learning outcome details retrieved successfully", data)
}

// CreateDetail godoc
// @Summary Create Learning Outcome Detail
// @Tags Learning Outcome Details
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param cpId    path string                true "Learning Outcome ID (UUID)"
// @Param request body CreateCPDetailRequest true "Create Detail Request"
// @Success 201 {object} common.Response
// @Router /learning-outcomes/{cpId}/details [post]
func (h *CPHandler) CreateDetail(c *fiber.Ctx) error {
	var req CreateCPDetailRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}
	data, err := h.svc.CreateDetail(c.UserContext(), c.Params("cpId"), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to create detail", err.Error())
	}
	return common.Created(c, "Detail created successfully", data)
}

// UpdateDetail godoc
// @Summary Update Learning Outcome Detail
// @Tags Learning Outcome Details
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param cpId    path string                true "Learning Outcome ID (UUID)"
// @Param id      path string                true "Detail ID (UUID)"
// @Param request body UpdateCPDetailRequest true "Update Detail Request"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{cpId}/details/{id} [put]
func (h *CPHandler) UpdateDetail(c *fiber.Ctx) error {
	var req UpdateCPDetailRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}
	data, err := h.svc.UpdateDetail(c.UserContext(), c.Params("cpId"), c.Params("id"), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to update detail", err.Error())
	}
	return common.Success(c, "Detail updated successfully", data)
}

// DeleteDetail godoc
// @Summary Delete Learning Outcome Detail
// @Tags Learning Outcome Details
// @Produce json
// @Security BearerAuth
// @Param cpId path string true "Learning Outcome ID (UUID)"
// @Param id   path string true "Detail ID (UUID)"
// @Success 200 {object} common.Response
// @Router /learning-outcomes/{cpId}/details/{id} [delete]
func (h *CPHandler) DeleteDetail(c *fiber.Ctx) error {
	if err := h.svc.DeleteDetail(c.UserContext(), c.Params("cpId"), c.Params("id")); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to delete detail", err.Error())
	}
	return common.Success(c, "Detail deleted successfully", nil)
}

// TP Handlers
func (h *CPHandler) GetAllObjectives(c *fiber.Ctx) error {
	data, err := h.svc.GetAllObjectives(c.Params("cpId"))
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to fetch objectives", err.Error())
	}
	return common.Success(c, "Objectives retrieved successfully", data)
}

func (h *CPHandler) CreateObjective(c *fiber.Ctx) error {
	var req CreateTPRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}
	data, err := h.svc.CreateObjective(c.UserContext(), c.Params("cpId"), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to create objective", err.Error())
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil && data != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "CREATE", "learning_objective", data.ID.String(), c.IP())
	}

	return common.Created(c, "Objective created successfully", data)
}

func (h *CPHandler) DeleteObjective(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteObjective(c.UserContext(), c.Params("cpId"), id); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to delete objective", err.Error())
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "learning_objective", id, c.IP())
	}

	return common.Success(c, "Objective deleted successfully", nil)
}
