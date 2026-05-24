package differentiated_instruction

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type DIHandler struct {
	service DIService
}

func NewDIHandler(service DIService) *DIHandler {
	return &DIHandler{service: service}
}

// DI Strategy Handlers

func (h *DIHandler) CreateDIStrategy(c *fiber.Ctx) error {
	var req CreateDIStrategyRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateDIStrategy(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat DI strategy", err)
	}

	return common.Success(c, "DI strategy berhasil dibuat", result)
}

func (h *DIHandler) GetDIStrategyByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetDIStrategyByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "DI strategy tidak ditemukan", err)
	}

	return common.Success(c, "DI strategy berhasil diambil", result)
}

func (h *DIHandler) GetAllDIStrategies(c *fiber.Ctx) error {
	result, err := h.service.GetAllDIStrategies(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil DI strategies", err)
	}

	return common.Success(c, "DI strategies berhasil diambil", fiber.Map{
		"strategies": result,
		"total":      len(result),
	})
}

func (h *DIHandler) GetActiveDIStrategies(c *fiber.Ctx) error {
	result, err := h.service.GetActiveDIStrategies(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil active DI strategies", err)
	}

	return common.Success(c, "Active DI strategies berhasil diambil", fiber.Map{
		"strategies": result,
		"total":      len(result),
	})
}

func (h *DIHandler) GetDIStrategiesByTargetGroup(c *fiber.Ctx) error {
	targetGroup := c.Params("targetGroup")

	result, err := h.service.GetDIStrategiesByTargetGroup(c.Context(), targetGroup)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil DI strategies", err)
	}

	return common.Success(c, "DI strategies berhasil diambil", fiber.Map{
		"strategies": result,
		"total":      len(result),
	})
}

func (h *DIHandler) UpdateDIStrategy(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdateDIStrategyRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateDIStrategy(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate DI strategy", err)
	}

	return common.Success(c, "DI strategy berhasil diupdate", result)
}

func (h *DIHandler) DeleteDIStrategy(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeleteDIStrategy(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus DI strategy", err)
	}

	return common.Success(c, "DI strategy berhasil dihapus", nil)
}

// Module Differentiation Handlers

func (h *DIHandler) CreateModuleDifferentiation(c *fiber.Ctx) error {
	var req CreateModuleDifferentiationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateModuleDifferentiation(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat module differentiation", err)
	}

	return common.Success(c, "Module differentiation berhasil dibuat", result)
}

func (h *DIHandler) GetModuleDifferentiationByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetModuleDifferentiationByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Module differentiation tidak ditemukan", err)
	}

	return common.Success(c, "Module differentiation berhasil diambil", result)
}

func (h *DIHandler) GetDifferentiationsByModuleID(c *fiber.Ctx) error {
	moduleID, err := uuid.Parse(c.Params("moduleId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Module ID tidak valid", err)
	}

	result, err := h.service.GetDifferentiationsByModuleID(c.Context(), moduleID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil module differentiations", err)
	}

	return common.Success(c, "Module differentiations berhasil diambil", fiber.Map{
		"differentiations": result,
		"total":            len(result),
	})
}

func (h *DIHandler) GetDifferentiationsByStudentID(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	result, err := h.service.GetDifferentiationsByStudentID(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student differentiations", err)
	}

	return common.Success(c, "Student differentiations berhasil diambil", fiber.Map{
		"differentiations": result,
		"total":            len(result),
	})
}

func (h *DIHandler) UpdateModuleDifferentiation(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdateModuleDifferentiationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateModuleDifferentiation(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate module differentiation", err)
	}

	return common.Success(c, "Module differentiation berhasil diupdate", result)
}

func (h *DIHandler) DeleteModuleDifferentiation(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeleteModuleDifferentiation(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus module differentiation", err)
	}

	return common.Success(c, "Module differentiation berhasil dihapus", nil)
}

func (h *DIHandler) DeleteDifferentiationsByModuleID(c *fiber.Ctx) error {
	moduleID, err := uuid.Parse(c.Params("moduleId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Module ID tidak valid", err)
	}

	err = h.service.DeleteDifferentiationsByModuleID(c.Context(), moduleID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus module differentiations", err)
	}

	return common.Success(c, "Module differentiations berhasil dihapus", nil)
}

func (h *DIHandler) GetModuleDISummary(c *fiber.Ctx) error {
	moduleID, err := uuid.Parse(c.Params("moduleId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Module ID tidak valid", err)
	}

	result, err := h.service.GetModuleDISummary(c.Context(), moduleID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil module DI summary", err)
	}

	return common.Success(c, "Module DI summary berhasil diambil", result)
}

// Student DI Need Handlers

func (h *DIHandler) CreateStudentDINeed(c *fiber.Ctx) error {
	var req CreateStudentDINeedRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateStudentDINeed(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat student DI need", err)
	}

	return common.Success(c, "Student DI need berhasil dibuat", result)
}

func (h *DIHandler) GetStudentDINeedByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetStudentDINeedByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Student DI need tidak ditemukan", err)
	}

	return common.Success(c, "Student DI need berhasil diambil", result)
}

func (h *DIHandler) GetDINeedsByStudentID(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	result, err := h.service.GetDINeedsByStudentID(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student DI needs", err)
	}

	return common.Success(c, "Student DI needs berhasil diambil", fiber.Map{
		"needs": result,
		"total": len(result),
	})
}

func (h *DIHandler) GetActiveDINeedsByStudentID(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	result, err := h.service.GetActiveDINeedsByStudentID(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil active student DI needs", err)
	}

	return common.Success(c, "Active student DI needs berhasil diambil", fiber.Map{
		"needs": result,
		"total": len(result),
	})
}

func (h *DIHandler) GetDINeedsByStudentAndSubject(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	subjectID, err := uuid.Parse(c.Params("subjectId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Subject ID tidak valid", err)
	}

	result, err := h.service.GetDINeedsByStudentAndSubject(c.Context(), studentID, subjectID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student DI needs", err)
	}

	return common.Success(c, "Student DI needs berhasil diambil", fiber.Map{
		"needs": result,
		"total": len(result),
	})
}

func (h *DIHandler) UpdateStudentDINeed(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdateStudentDINeedRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateStudentDINeed(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate student DI need", err)
	}

	return common.Success(c, "Student DI need berhasil diupdate", result)
}

func (h *DIHandler) DeleteStudentDINeed(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeleteStudentDINeed(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus student DI need", err)
	}

	return common.Success(c, "Student DI need berhasil dihapus", nil)
}

func (h *DIHandler) GetStudentDINeedSummary(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	result, err := h.service.GetStudentDINeedSummary(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student DI need summary", err)
	}

	return common.Success(c, "Student DI need summary berhasil diambil", result)
}
