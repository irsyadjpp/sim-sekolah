package character_intervention

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type CharacterInterventionHandler struct {
	service CharacterInterventionService
}

func NewCharacterInterventionHandler(service CharacterInterventionService) *CharacterInterventionHandler {
	return &CharacterInterventionHandler{service: service}
}

// CharacterIntervention Handlers

func (h *CharacterInterventionHandler) GetAll(c *fiber.Ctx) error {
	result, err := h.service.GetAll(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil interventions", err)
	}

	return common.Success(c, "Interventions berhasil diambil", fiber.Map{
		"interventions": result,
		"total":         len(result),
	})
}

func (h *CharacterInterventionHandler) GetByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Intervention tidak ditemukan", err)
	}

	return common.Success(c, "Intervention berhasil diambil", result)
}

func (h *CharacterInterventionHandler) GetByDimension(c *fiber.Ctx) error {
	dimension := c.Params("dimension")
	if dimension == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Dimension tidak valid", nil)
	}

	result, err := h.service.GetByDimension(c.Context(), dimension)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil interventions", err)
	}

	return common.Success(c, "Interventions berhasil diambil", fiber.Map{
		"interventions": result,
		"total":         len(result),
	})
}

func (h *CharacterInterventionHandler) GetByAgeGroup(c *fiber.Ctx) error {
	ageGroup := c.Params("ageGroup")
	if ageGroup == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Age group tidak valid", nil)
	}

	result, err := h.service.GetByAgeGroup(c.Context(), ageGroup)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil interventions", err)
	}

	return common.Success(c, "Interventions berhasil diambil", fiber.Map{
		"interventions": result,
		"total":         len(result),
	})
}

func (h *CharacterInterventionHandler) GetActive(c *fiber.Ctx) error {
	result, err := h.service.GetActive(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil active interventions", err)
	}

	return common.Success(c, "Active interventions berhasil diambil", fiber.Map{
		"interventions": result,
		"total":         len(result),
	})
}

func (h *CharacterInterventionHandler) Create(c *fiber.Ctx) error {
	var req CreateCharacterInterventionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.Create(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat intervention", err)
	}

	return common.Success(c, "Intervention berhasil dibuat", result)
}

func (h *CharacterInterventionHandler) Update(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateCharacterInterventionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.Update(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate intervention", err)
	}

	return common.Success(c, "Intervention berhasil diupdate", result)
}

func (h *CharacterInterventionHandler) Delete(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.Delete(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus intervention", err)
	}

	return common.Success(c, "Intervention berhasil dihapus", nil)
}

// StudentCharacterIntervention Handlers

func (h *CharacterInterventionHandler) GetAllStudentInterventions(c *fiber.Ctx) error {
	result, err := h.service.GetAllStudentInterventions(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student interventions", err)
	}

	return common.Success(c, "Student interventions berhasil diambil", fiber.Map{
		"student_interventions": result,
		"total":                 len(result),
	})
}

func (h *CharacterInterventionHandler) GetStudentInterventionByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetStudentInterventionByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Student intervention tidak ditemukan", err)
	}

	return common.Success(c, "Student intervention berhasil diambil", result)
}

func (h *CharacterInterventionHandler) GetStudentInterventionsByStudent(c *fiber.Ctx) error {
	studentID := c.Params("studentId")
	if studentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", nil)
	}

	result, err := h.service.GetStudentInterventionsByStudent(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student interventions", err)
	}

	return common.Success(c, "Student interventions berhasil diambil", fiber.Map{
		"student_interventions": result,
		"total":                 len(result),
	})
}

func (h *CharacterInterventionHandler) GetStudentInterventionsByTeacher(c *fiber.Ctx) error {
	teacherID := c.Params("teacherId")
	if teacherID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Teacher ID tidak valid", nil)
	}

	result, err := h.service.GetStudentInterventionsByTeacher(c.Context(), teacherID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student interventions", err)
	}

	return common.Success(c, "Student interventions berhasil diambil", fiber.Map{
		"student_interventions": result,
		"total":                 len(result),
	})
}

func (h *CharacterInterventionHandler) GetActiveStudentInterventions(c *fiber.Ctx) error {
	result, err := h.service.GetActiveStudentInterventions(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil active student interventions", err)
	}

	return common.Success(c, "Active student interventions berhasil diambil", fiber.Map{
		"student_interventions": result,
		"total":                 len(result),
	})
}

func (h *CharacterInterventionHandler) GetStudentInterventionsByStatus(c *fiber.Ctx) error {
	status := c.Params("status")
	if status == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Status tidak valid", nil)
	}

	result, err := h.service.GetStudentInterventionsByStatus(c.Context(), status)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil student interventions", err)
	}

	return common.Success(c, "Student interventions berhasil diambil", fiber.Map{
		"student_interventions": result,
		"total":                 len(result),
	})
}

func (h *CharacterInterventionHandler) CreateStudentIntervention(c *fiber.Ctx) error {
	var req CreateStudentInterventionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateStudentIntervention(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat student intervention", err)
	}

	return common.Success(c, "Student intervention berhasil dibuat", result)
}

func (h *CharacterInterventionHandler) UpdateStudentIntervention(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateStudentInterventionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateStudentIntervention(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate student intervention", err)
	}

	return common.Success(c, "Student intervention berhasil diupdate", result)
}

func (h *CharacterInterventionHandler) DeleteStudentIntervention(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteStudentIntervention(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus student intervention", err)
	}

	return common.Success(c, "Student intervention berhasil dihapus", nil)
}

// CharacterInterventionProgress Handlers

func (h *CharacterInterventionHandler) GetAllProgress(c *fiber.Ctx) error {
	result, err := h.service.GetAllProgress(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil progress records", err)
	}

	return common.Success(c, "Progress records berhasil diambil", fiber.Map{
		"progress": result,
		"total":    len(result),
	})
}

func (h *CharacterInterventionHandler) GetProgressByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetProgressByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Progress tidak ditemukan", err)
	}

	return common.Success(c, "Progress berhasil diambil", result)
}

func (h *CharacterInterventionHandler) GetProgressByAssignment(c *fiber.Ctx) error {
	assignmentID := c.Params("assignmentId")
	if assignmentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Assignment ID tidak valid", nil)
	}

	result, err := h.service.GetProgressByAssignment(c.Context(), assignmentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil progress records", err)
	}

	return common.Success(c, "Progress records berhasil diambil", fiber.Map{
		"progress": result,
		"total":    len(result),
	})
}

func (h *CharacterInterventionHandler) GetProgressByObserver(c *fiber.Ctx) error {
	observerID := c.Params("observerId")
	if observerID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Observer ID tidak valid", nil)
	}

	result, err := h.service.GetProgressByObserver(c.Context(), observerID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil progress records", err)
	}

	return common.Success(c, "Progress records berhasil diambil", fiber.Map{
		"progress": result,
		"total":    len(result),
	})
}

func (h *CharacterInterventionHandler) CreateProgress(c *fiber.Ctx) error {
	var req CreateInterventionProgressRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateProgress(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat progress", err)
	}

	return common.Success(c, "Progress berhasil dibuat", result)
}

func (h *CharacterInterventionHandler) UpdateProgress(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateInterventionProgressRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateProgress(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate progress", err)
	}

	return common.Success(c, "Progress berhasil diupdate", result)
}

func (h *CharacterInterventionHandler) DeleteProgress(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteProgress(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus progress", err)
	}

	return common.Success(c, "Progress berhasil dihapus", nil)
}

// InterventionRecommendation Handlers

func (h *CharacterInterventionHandler) GetAllRecommendations(c *fiber.Ctx) error {
	result, err := h.service.GetAllRecommendations(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil recommendations", err)
	}

	return common.Success(c, "Recommendations berhasil diambil", fiber.Map{
		"recommendations": result,
		"total":           len(result),
	})
}

func (h *CharacterInterventionHandler) GetRecommendationByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetRecommendationByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Recommendation tidak ditemukan", err)
	}

	return common.Success(c, "Recommendation berhasil diambil", result)
}

func (h *CharacterInterventionHandler) GetRecommendationsByStudent(c *fiber.Ctx) error {
	studentID := c.Params("studentId")
	if studentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", nil)
	}

	result, err := h.service.GetRecommendationsByStudent(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil recommendations", err)
	}

	return common.Success(c, "Recommendations berhasil diambil", fiber.Map{
		"recommendations": result,
		"total":           len(result),
	})
}

func (h *CharacterInterventionHandler) GetPendingRecommendations(c *fiber.Ctx) error {
	result, err := h.service.GetPendingRecommendations(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil pending recommendations", err)
	}

	return common.Success(c, "Pending recommendations berhasil diambil", fiber.Map{
		"recommendations": result,
		"total":           len(result),
	})
}

func (h *CharacterInterventionHandler) CreateRecommendation(c *fiber.Ctx) error {
	var req CreateInterventionRecommendationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateRecommendation(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat recommendation", err)
	}

	return common.Success(c, "Recommendation berhasil dibuat", result)
}

func (h *CharacterInterventionHandler) UpdateRecommendation(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateInterventionRecommendationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateRecommendation(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate recommendation", err)
	}

	return common.Success(c, "Recommendation berhasil diupdate", result)
}

func (h *CharacterInterventionHandler) DeleteRecommendation(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteRecommendation(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus recommendation", err)
	}

	return common.Success(c, "Recommendation berhasil dihapus", nil)
}

// CharacterMilestone Handlers

func (h *CharacterInterventionHandler) GetAllMilestones(c *fiber.Ctx) error {
	result, err := h.service.GetAllMilestones(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil milestones", err)
	}

	return common.Success(c, "Milestones berhasil diambil", fiber.Map{
		"milestones": result,
		"total":      len(result),
	})
}

func (h *CharacterInterventionHandler) GetMilestoneByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetMilestoneByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Milestone tidak ditemukan", err)
	}

	return common.Success(c, "Milestone berhasil diambil", result)
}

func (h *CharacterInterventionHandler) GetMilestonesByStudent(c *fiber.Ctx) error {
	studentID := c.Params("studentId")
	if studentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", nil)
	}

	result, err := h.service.GetMilestonesByStudent(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil milestones", err)
	}

	return common.Success(c, "Milestones berhasil diambil", fiber.Map{
		"milestones": result,
		"total":      len(result),
	})
}

func (h *CharacterInterventionHandler) GetMilestonesByDimension(c *fiber.Ctx) error {
	dimension := c.Params("dimension")
	if dimension == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Dimension tidak valid", nil)
	}

	result, err := h.service.GetMilestonesByDimension(c.Context(), dimension)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil milestones", err)
	}

	return common.Success(c, "Milestones berhasil diambil", fiber.Map{
		"milestones": result,
		"total":      len(result),
	})
}

func (h *CharacterInterventionHandler) GetMilestonesByObserver(c *fiber.Ctx) error {
	observerID := c.Params("observerId")
	if observerID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Observer ID tidak valid", nil)
	}

	result, err := h.service.GetMilestonesByObserver(c.Context(), observerID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil milestones", err)
	}

	return common.Success(c, "Milestones berhasil diambil", fiber.Map{
		"milestones": result,
		"total":      len(result),
	})
}

func (h *CharacterInterventionHandler) CreateMilestone(c *fiber.Ctx) error {
	var req CreateCharacterMilestoneRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateMilestone(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat milestone", err)
	}

	return common.Success(c, "Milestone berhasil dibuat", result)
}

func (h *CharacterInterventionHandler) UpdateMilestone(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateCharacterMilestoneRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateMilestone(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate milestone", err)
	}

	return common.Success(c, "Milestone berhasil diupdate", result)
}

func (h *CharacterInterventionHandler) DeleteMilestone(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteMilestone(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus milestone", err)
	}

	return common.Success(c, "Milestone berhasil dihapus", nil)
}

// Summary Handler

func (h *CharacterInterventionHandler) GetInterventionSummary(c *fiber.Ctx) error {
	result, err := h.service.GetInterventionSummary(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil intervention summary", err)
	}

	return common.Success(c, "Intervention summary berhasil diambil", result)
}
