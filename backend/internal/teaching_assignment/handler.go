package teaching_assignment

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type TeachingAssignmentHandler struct {
	svc TeachingAssignmentService
}

func NewTeachingAssignmentHandler(svc TeachingAssignmentService) *TeachingAssignmentHandler {
	return &TeachingAssignmentHandler{svc: svc}
}

// GetAssignmentsHandler godoc
func (h *TeachingAssignmentHandler) GetAssignments(c *fiber.Ctx) error {
	data, err := h.svc.GetByClassroom(c.UserContext(), c.Params("classroomId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data penugasan", err)
	}
	return common.Success(c, "Data penugasan berhasil diambil", data)
}

// CreateAssignmentHandler godoc
func (h *TeachingAssignmentHandler) CreateAssignment(c *fiber.Ctx) error {
	classroomID := c.Params("classroomId")
	var req CreateTeachingAssignmentRequest

	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}

	req.ClassroomID = classroomID

	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat penugasan", err)
	}
	return common.Created(c, "Penugasan berhasil dibuat", data)
}

// UpdateAssignmentHandler godoc
func (h *TeachingAssignmentHandler) UpdateAssignment(c *fiber.Ctx) error {
	var req UpdateTeachingAssignmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}

	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui penugasan", err)
	}
	return common.Success(c, "Penugasan berhasil diperbarui", data)
}

// DeleteAssignmentHandler godoc
func (h *TeachingAssignmentHandler) DeleteAssignment(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus penugasan", err)
	}
	return common.Success(c, "Penugasan berhasil dihapus", nil)
}
