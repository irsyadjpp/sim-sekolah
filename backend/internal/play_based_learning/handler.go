package play_based_learning

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type PlayBasedLearningHandler struct {
	service PlayBasedLearningService
}

func NewPlayBasedLearningHandler(service PlayBasedLearningService) *PlayBasedLearningHandler {
	return &PlayBasedLearningHandler{service: service}
}

// Play Activity Type Handlers

func (h *PlayBasedLearningHandler) CreatePlayActivityType(c *fiber.Ctx) error {
	var req CreatePlayActivityTypeRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreatePlayActivityType(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat play activity type", err)
	}

	return common.Success(c, "Play activity type berhasil dibuat", result)
}

func (h *PlayBasedLearningHandler) GetPlayActivityTypeByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetPlayActivityTypeByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Play activity type tidak ditemukan", err)
	}

	return common.Success(c, "Play activity type berhasil diambil", result)
}

func (h *PlayBasedLearningHandler) GetAllPlayActivityTypes(c *fiber.Ctx) error {
	result, err := h.service.GetAllPlayActivityTypes(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil play activity types", err)
	}

	return common.Success(c, "Play activity types berhasil diambil", fiber.Map{
		"activity_types": result,
		"total":          len(result),
	})
}

func (h *PlayBasedLearningHandler) GetActivePlayActivityTypes(c *fiber.Ctx) error {
	result, err := h.service.GetActivePlayActivityTypes(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil active play activity types", err)
	}

	return common.Success(c, "Active play activity types berhasil diambil", fiber.Map{
		"activity_types": result,
		"total":          len(result),
	})
}

func (h *PlayBasedLearningHandler) GetPlayActivityTypesByPhase(c *fiber.Ctx) error {
	phaseID, err := uuid.Parse(c.Params("phaseId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Phase ID tidak valid", err)
	}

	result, err := h.service.GetPlayActivityTypesByPhase(c.Context(), phaseID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil play activity types", err)
	}

	return common.Success(c, "Play activity types berhasil diambil", fiber.Map{
		"activity_types": result,
		"total":          len(result),
	})
}

func (h *PlayBasedLearningHandler) GetPlayActivityTypesByDomain(c *fiber.Ctx) error {
	domain := c.Params("domain")

	result, err := h.service.GetPlayActivityTypesByDomain(c.Context(), domain)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil play activity types", err)
	}

	return common.Success(c, "Play activity types berhasil diambil", fiber.Map{
		"activity_types": result,
		"total":          len(result),
	})
}

func (h *PlayBasedLearningHandler) UpdatePlayActivityType(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdatePlayActivityTypeRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdatePlayActivityType(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate play activity type", err)
	}

	return common.Success(c, "Play activity type berhasil diupdate", result)
}

func (h *PlayBasedLearningHandler) DeletePlayActivityType(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeletePlayActivityType(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus play activity type", err)
	}

	return common.Success(c, "Play activity type berhasil dihapus", nil)
}

// Play Based Activity Handlers

func (h *PlayBasedLearningHandler) CreatePlayBasedActivity(c *fiber.Ctx) error {
	var req CreatePlayBasedActivityRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreatePlayBasedActivity(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat play based activity", err)
	}

	return common.Success(c, "Play based activity berhasil dibuat", result)
}

func (h *PlayBasedLearningHandler) GetPlayBasedActivityByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetPlayBasedActivityByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Play based activity tidak ditemukan", err)
	}

	return common.Success(c, "Play based activity berhasil diambil", result)
}

func (h *PlayBasedLearningHandler) GetPlayBasedActivitiesByModuleID(c *fiber.Ctx) error {
	moduleID, err := uuid.Parse(c.Params("moduleId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Module ID tidak valid", err)
	}

	result, err := h.service.GetPlayBasedActivitiesByModuleID(c.Context(), moduleID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil play based activities", err)
	}

	return common.Success(c, "Play based activities berhasil diambil", fiber.Map{
		"activities": result,
		"total":      len(result),
	})
}

func (h *PlayBasedLearningHandler) UpdatePlayBasedActivity(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdatePlayBasedActivityRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdatePlayBasedActivity(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate play based activity", err)
	}

	return common.Success(c, "Play based activity berhasil diupdate", result)
}

func (h *PlayBasedLearningHandler) DeletePlayBasedActivity(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeletePlayBasedActivity(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus play based activity", err)
	}

	return common.Success(c, "Play based activity berhasil dihapus", nil)
}

func (h *PlayBasedLearningHandler) DeletePlayBasedActivitiesByModuleID(c *fiber.Ctx) error {
	moduleID, err := uuid.Parse(c.Params("moduleId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Module ID tidak valid", err)
	}

	err = h.service.DeletePlayBasedActivitiesByModuleID(c.Context(), moduleID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus play based activities", err)
	}

	return common.Success(c, "Play based activities berhasil dihapus", nil)
}

func (h *PlayBasedLearningHandler) GetPlayBasedLearningSummary(c *fiber.Ctx) error {
	moduleID, err := uuid.Parse(c.Params("moduleId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Module ID tidak valid", err)
	}

	result, err := h.service.GetPlayBasedLearningSummary(c.Context(), moduleID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil play based learning summary", err)
	}

	return common.Success(c, "Play based learning summary berhasil diambil", result)
}

// Play Observation Handlers

func (h *PlayBasedLearningHandler) CreatePlayObservation(c *fiber.Ctx) error {
	var req CreatePlayObservationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreatePlayObservation(c.Context(), &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat play observation", err)
	}

	return common.Success(c, "Play observation berhasil dibuat", result)
}

func (h *PlayBasedLearningHandler) GetPlayObservationByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	result, err := h.service.GetPlayObservationByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Play observation tidak ditemukan", err)
	}

	return common.Success(c, "Play observation berhasil diambil", result)
}

func (h *PlayBasedLearningHandler) GetPlayObservationsByActivityID(c *fiber.Ctx) error {
	activityID, err := uuid.Parse(c.Params("activityId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Activity ID tidak valid", err)
	}

	result, err := h.service.GetPlayObservationsByActivityID(c.Context(), activityID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil play observations", err)
	}

	return common.Success(c, "Play observations berhasil diambil", fiber.Map{
		"observations": result,
		"total":        len(result),
	})
}

func (h *PlayBasedLearningHandler) GetPlayObservationsByStudentID(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	result, err := h.service.GetPlayObservationsByStudentID(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil play observations", err)
	}

	return common.Success(c, "Play observations berhasil diambil", fiber.Map{
		"observations": result,
		"total":        len(result),
	})
}

func (h *PlayBasedLearningHandler) GetPlayObservationsByStudentAndActivity(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	activityID, err := uuid.Parse(c.Params("activityId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Activity ID tidak valid", err)
	}

	result, err := h.service.GetPlayObservationsByStudentAndActivity(c.Context(), studentID, activityID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil play observations", err)
	}

	return common.Success(c, "Play observations berhasil diambil", fiber.Map{
		"observations": result,
		"total":        len(result),
	})
}

func (h *PlayBasedLearningHandler) UpdatePlayObservation(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	var req UpdatePlayObservationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdatePlayObservation(c.Context(), id, &req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate play observation", err)
	}

	return common.Success(c, "Play observation berhasil diupdate", result)
}

func (h *PlayBasedLearningHandler) DeletePlayObservation(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", err)
	}

	err = h.service.DeletePlayObservation(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus play observation", err)
	}

	return common.Success(c, "Play observation berhasil dihapus", nil)
}

func (h *PlayBasedLearningHandler) GetStudentPlaySummary(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("studentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", err)
	}

	result, err := h.service.GetStudentPlaySummary(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student play summary", err)
	}

	return common.Success(c, "Student play summary berhasil diambil", result)
}
