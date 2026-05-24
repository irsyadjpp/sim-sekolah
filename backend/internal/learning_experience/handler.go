package learning_experience

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type LearningExperienceHandler struct {
	service LearningExperienceService
}

func NewLearningExperienceHandler(service LearningExperienceService) *LearningExperienceHandler {
	return &LearningExperienceHandler{service: service}
}

// Learning Experience CRUD Handlers

func (h *LearningExperienceHandler) CreateLearningExperience(c *fiber.Ctx) error {
	var req CreateLearningExperienceRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateLearningExperience(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat learning experience", err)
	}

	return common.Success(c, "Learning experience berhasil dibuat", result)
}

func (h *LearningExperienceHandler) GetLearningExperienceByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetLearningExperienceByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Learning experience tidak ditemukan", err)
	}

	return common.Success(c, "Learning experience berhasil diambil", result)
}

func (h *LearningExperienceHandler) GetAllLearningExperiences(c *fiber.Ctx) error {
	result, err := h.service.GetAllLearningExperiences(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil learning experiences", err)
	}

	return common.Success(c, "Learning experiences berhasil diambil", fiber.Map{
		"experiences": result,
		"total":       len(result),
	})
}

func (h *LearningExperienceHandler) GetActiveLearningExperiences(c *fiber.Ctx) error {
	result, err := h.service.GetActiveLearningExperiences(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil learning experiences aktif", err)
	}

	return common.Success(c, "Learning experiences aktif berhasil diambil", fiber.Map{
		"experiences": result,
		"total":       len(result),
	})
}

func (h *LearningExperienceHandler) UpdateLearningExperience(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdateLearningExperienceRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateLearningExperience(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate learning experience", err)
	}

	return common.Success(c, "Learning experience berhasil diupdate", result)
}

func (h *LearningExperienceHandler) DeleteLearningExperience(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeleteLearningExperience(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus learning experience", err)
	}

	return common.Success(c, "Learning experience berhasil dihapus", nil)
}

// Activity Experience Mapping Handlers

func (h *LearningExperienceHandler) LinkActivityToExperience(c *fiber.Ctx) error {
	var req ActivityExperienceMappingRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	err := h.service.LinkActivityToExperience(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghubungkan activity ke experience", err)
	}

	return common.Success(c, "Activity berhasil dihubungkan ke experience", nil)
}

func (h *LearningExperienceHandler) UnlinkActivityFromExperience(c *fiber.Ctx) error {
	activityID, err := uuid.Parse(c.Params("activityId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Activity ID tidak valid", err)
	}

	err = h.service.UnlinkActivityFromExperience(c.Context(), activityID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memutuskan hubungan activity dari experience", err)
	}

	return common.Success(c, "Activity berhasil diputus dari experience", nil)
}

func (h *LearningExperienceHandler) GetExperienceByActivityID(c *fiber.Ctx) error {
	activityID, err := uuid.Parse(c.Params("activityId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Activity ID tidak valid", err)
	}

	result, err := h.service.GetExperienceByActivityID(c.Context(), activityID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Experience tidak ditemukan", err)
	}

	return common.Success(c, "Experience berhasil diambil", result)
}

// Student Experience Progression Handlers

func (h *LearningExperienceHandler) CreateStudentProgression(c *fiber.Ctx) error {
	var req CreateStudentProgressionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateStudentProgression(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat student progression", err)
	}

	return common.Success(c, "Student progression berhasil dibuat", result)
}

func (h *LearningExperienceHandler) GetStudentProgressionByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetStudentProgressionByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Student progression tidak ditemukan", err)
	}

	return common.Success(c, "Student progression berhasil diambil", result)
}

func (h *LearningExperienceHandler) UpdateStudentProgression(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdateStudentProgressionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateStudentProgression(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate student progression", err)
	}

	return common.Success(c, "Student progression berhasil diupdate", result)
}

func (h *LearningExperienceHandler) DeleteStudentProgression(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeleteStudentProgression(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus student progression", err)
	}

	return common.Success(c, "Student progression berhasil dihapus", nil)
}

func (h *LearningExperienceHandler) GetStudentProgressions(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	var subjectID uuid.UUID
	subjectIdParam := c.Query("subjectId")
	if subjectIdParam != "" {
		subjectID, err = uuid.Parse(subjectIdParam)
		if err != nil {
			return common.ErrorFromService(c, fiber.StatusBadRequest, "Subject ID tidak valid", err)
		}
	}

	result, err := h.service.GetStudentProgressions(c.Context(), studentID, subjectID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student progressions", err)
	}

	return common.Success(c, "Student progressions berhasil diambil", fiber.Map{
		"progressions": result,
		"total":        len(result),
	})
}

func (h *LearningExperienceHandler) GetStudentProgressionSummary(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	subjectID, err := uuid.Parse(c.Params("subjectId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Subject ID tidak valid", err)
	}

	result, err := h.service.GetStudentProgressionSummary(c.Context(), studentID, subjectID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student progression summary", err)
	}

	return common.Success(c, "Student progression summary berhasil diambil", result)
}
