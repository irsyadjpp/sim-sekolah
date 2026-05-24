package individual_learning_plan

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type ILPHandler struct {
	service ILPService
}

func NewILPHandler(service ILPService) *ILPHandler {
	return &ILPHandler{service: service}
}

// Individual Learning Plan Handlers

func (h *ILPHandler) CreateILP(c *fiber.Ctx) error {
	var req CreateILPRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateILP(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat ILP", err)
	}

	return common.Success(c, "ILP berhasil dibuat", result)
}

func (h *ILPHandler) GetILPByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetILPByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "ILP tidak ditemukan", err)
	}

	return common.Success(c, "ILP berhasil diambil", result)
}

func (h *ILPHandler) GetILPByStudentID(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	result, err := h.service.GetILPByStudentID(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil ILP siswa", err)
	}

	return common.Success(c, "ILP siswa berhasil diambil", fiber.Map{
		"ilps":  result,
		"total": len(result),
	})
}

func (h *ILPHandler) GetILPByStudentAndAcademicYear(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	academicYearID, err := uuid.Parse(c.Params("academicYearId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Academic Year ID tidak valid", err)
	}

	result, err := h.service.GetILPByStudentAndAcademicYear(c.Context(), studentID, academicYearID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "ILP tidak ditemukan", err)
	}

	return common.Success(c, "ILP berhasil diambil", result)
}

func (h *ILPHandler) GetAllILPs(c *fiber.Ctx) error {
	result, err := h.service.GetAllILPs(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil ILPs", err)
	}

	return common.Success(c, "ILPs berhasil diambil", fiber.Map{
		"ilps":  result,
		"total": len(result),
	})
}

func (h *ILPHandler) UpdateILP(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdateILPRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateILP(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate ILP", err)
	}

	return common.Success(c, "ILP berhasil diupdate", result)
}

func (h *ILPHandler) DeleteILP(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeleteILP(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus ILP", err)
	}

	return common.Success(c, "ILP berhasil dihapus", nil)
}

// ILP Milestone Handlers

func (h *ILPHandler) CreateMilestone(c *fiber.Ctx) error {
	var req CreateMilestoneRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateMilestone(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat milestone", err)
	}

	return common.Success(c, "Milestone berhasil dibuat", result)
}

func (h *ILPHandler) GetMilestoneByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetMilestoneByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Milestone tidak ditemukan", err)
	}

	return common.Success(c, "Milestone berhasil diambil", result)
}

func (h *ILPHandler) GetMilestonesByILPID(c *fiber.Ctx) error {
	ilpID, err := uuid.Parse(c.Params("ilpId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ILP ID tidak valid", err)
	}

	result, err := h.service.GetMilestonesByILPID(c.Context(), ilpID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil milestones", err)
	}

	return common.Success(c, "Milestones berhasil diambil", fiber.Map{
		"milestones": result,
		"total":      len(result),
	})
}

func (h *ILPHandler) UpdateMilestone(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdateMilestoneRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateMilestone(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate milestone", err)
	}

	return common.Success(c, "Milestone berhasil diupdate", result)
}

func (h *ILPHandler) DeleteMilestone(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeleteMilestone(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus milestone", err)
	}

	return common.Success(c, "Milestone berhasil dihapus", nil)
}

// ILP Template Handlers

func (h *ILPHandler) CreateTemplate(c *fiber.Ctx) error {
	var req CreateTemplateRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateTemplate(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat template", err)
	}

	return common.Success(c, "Template berhasil dibuat", result)
}

func (h *ILPHandler) GetTemplateByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetTemplateByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Template tidak ditemukan", err)
	}

	return common.Success(c, "Template berhasil diambil", result)
}

func (h *ILPHandler) GetAllTemplates(c *fiber.Ctx) error {
	result, err := h.service.GetAllTemplates(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil templates", err)
	}

	return common.Success(c, "Templates berhasil diambil", fiber.Map{
		"templates": result,
		"total":     len(result),
	})
}

func (h *ILPHandler) GetActiveTemplates(c *fiber.Ctx) error {
	result, err := h.service.GetActiveTemplates(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil active templates", err)
	}

	return common.Success(c, "Active templates berhasil diambil", fiber.Map{
		"templates": result,
		"total":     len(result),
	})
}

func (h *ILPHandler) GetTemplatesByPhase(c *fiber.Ctx) error {
	phaseID, err := uuid.Parse(c.Params("phaseId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Phase ID tidak valid", err)
	}

	result, err := h.service.GetTemplatesByPhase(c.Context(), phaseID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil templates", err)
	}

	return common.Success(c, "Templates berhasil diambil", fiber.Map{
		"templates": result,
		"total":     len(result),
	})
}

func (h *ILPHandler) UpdateTemplate(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdateTemplateRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateTemplate(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate template", err)
	}

	return common.Success(c, "Template berhasil diupdate", result)
}

func (h *ILPHandler) DeleteTemplate(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeleteTemplate(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus template", err)
	}

	return common.Success(c, "Template berhasil dihapus", nil)
}

// Summary Handler

func (h *ILPHandler) GetILPSummary(c *fiber.Ctx) error {
	result, err := h.service.GetILPSummary(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil ILP summary", err)
	}

	return common.Success(c, "ILP summary berhasil diambil", result)
}
