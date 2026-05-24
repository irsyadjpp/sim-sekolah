package parent_partnership

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type ParentPartnershipHandler struct {
	service ParentPartnershipService
}

func NewParentPartnershipHandler(service ParentPartnershipService) *ParentPartnershipHandler {
	return &ParentPartnershipHandler{service: service}
}

// ParentPartnership Handlers

func (h *ParentPartnershipHandler) GetAll(c *fiber.Ctx) error {
	result, err := h.service.GetAll(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil partnerships", err)
	}

	return common.Success(c, "Partnerships berhasil diambil", fiber.Map{
		"partnerships": result,
		"total":        len(result),
	})
}

func (h *ParentPartnershipHandler) GetByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Partnership tidak ditemukan", err)
	}

	return common.Success(c, "Partnership berhasil diambil", result)
}

func (h *ParentPartnershipHandler) GetByStudentID(c *fiber.Ctx) error {
	studentID := c.Params("studentId")
	if studentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", nil)
	}

	result, err := h.service.GetByStudentID(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil partnerships siswa", err)
	}

	return common.Success(c, "Partnerships siswa berhasil diambil", fiber.Map{
		"partnerships": result,
		"total":        len(result),
	})
}

func (h *ParentPartnershipHandler) GetActiveByStudentID(c *fiber.Ctx) error {
	studentID := c.Params("studentId")
	if studentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", nil)
	}

	result, err := h.service.GetActiveByStudentID(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil active partnerships siswa", err)
	}

	return common.Success(c, "Active partnerships siswa berhasil diambil", fiber.Map{
		"partnerships": result,
		"total":        len(result),
	})
}

func (h *ParentPartnershipHandler) Create(c *fiber.Ctx) error {
	var req CreateParentPartnershipRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.Create(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat partnership", err)
	}

	return common.Success(c, "Partnership berhasil dibuat", result)
}

func (h *ParentPartnershipHandler) Update(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateParentPartnershipRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.Update(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate partnership", err)
	}

	return common.Success(c, "Partnership berhasil diupdate", result)
}

func (h *ParentPartnershipHandler) Delete(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.Delete(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus partnership", err)
	}

	return common.Success(c, "Partnership berhasil dihapus", nil)
}

// ParentCommunication Handlers

func (h *ParentPartnershipHandler) GetAllCommunications(c *fiber.Ctx) error {
	result, err := h.service.GetAllCommunications(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil communications", err)
	}

	return common.Success(c, "Communications berhasil diambil", fiber.Map{
		"communications": result,
		"total":          len(result),
	})
}

func (h *ParentPartnershipHandler) GetCommunicationByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetCommunicationByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Communication tidak ditemukan", err)
	}

	return common.Success(c, "Communication berhasil diambil", result)
}

func (h *ParentPartnershipHandler) GetCommunicationsByPartnership(c *fiber.Ctx) error {
	partnershipID := c.Params("partnershipId")
	if partnershipID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Partnership ID tidak valid", nil)
	}

	result, err := h.service.GetCommunicationsByPartnership(c.Context(), partnershipID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil communications", err)
	}

	return common.Success(c, "Communications berhasil diambil", fiber.Map{
		"communications": result,
		"total":          len(result),
	})
}

func (h *ParentPartnershipHandler) GetPendingFollowUps(c *fiber.Ctx) error {
	result, err := h.service.GetPendingFollowUps(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil pending follow-ups", err)
	}

	return common.Success(c, "Pending follow-ups berhasil diambil", fiber.Map{
		"communications": result,
		"total":          len(result),
	})
}

func (h *ParentPartnershipHandler) CreateCommunication(c *fiber.Ctx) error {
	var req CreateParentCommunicationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateCommunication(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat communication", err)
	}

	return common.Success(c, "Communication berhasil dibuat", result)
}

func (h *ParentPartnershipHandler) UpdateCommunication(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateParentCommunicationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateCommunication(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate communication", err)
	}

	return common.Success(c, "Communication berhasil diupdate", result)
}

func (h *ParentPartnershipHandler) DeleteCommunication(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteCommunication(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus communication", err)
	}

	return common.Success(c, "Communication berhasil dihapus", nil)
}

// ParentMeeting Handlers

func (h *ParentPartnershipHandler) GetAllMeetings(c *fiber.Ctx) error {
	result, err := h.service.GetAllMeetings(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil meetings", err)
	}

	return common.Success(c, "Meetings berhasil diambil", fiber.Map{
		"meetings": result,
		"total":    len(result),
	})
}

func (h *ParentPartnershipHandler) GetMeetingByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetMeetingByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Meeting tidak ditemukan", err)
	}

	return common.Success(c, "Meeting berhasil diambil", result)
}

func (h *ParentPartnershipHandler) GetMeetingsByPartnership(c *fiber.Ctx) error {
	partnershipID := c.Params("partnershipId")
	if partnershipID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Partnership ID tidak valid", nil)
	}

	result, err := h.service.GetMeetingsByPartnership(c.Context(), partnershipID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil meetings", err)
	}

	return common.Success(c, "Meetings berhasil diambil", fiber.Map{
		"meetings": result,
		"total":    len(result),
	})
}

func (h *ParentPartnershipHandler) GetMeetingsByTeacher(c *fiber.Ctx) error {
	teacherID := c.Params("teacherId")
	if teacherID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Teacher ID tidak valid", nil)
	}

	result, err := h.service.GetMeetingsByTeacher(c.Context(), teacherID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil meetings", err)
	}

	return common.Success(c, "Meetings berhasil diambil", fiber.Map{
		"meetings": result,
		"total":    len(result),
	})
}

func (h *ParentPartnershipHandler) GetScheduledMeetings(c *fiber.Ctx) error {
	result, err := h.service.GetScheduledMeetings(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil scheduled meetings", err)
	}

	return common.Success(c, "Scheduled meetings berhasil diambil", fiber.Map{
		"meetings": result,
		"total":    len(result),
	})
}

func (h *ParentPartnershipHandler) CreateMeeting(c *fiber.Ctx) error {
	var req CreateParentMeetingRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateMeeting(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat meeting", err)
	}

	return common.Success(c, "Meeting berhasil dibuat", result)
}

func (h *ParentPartnershipHandler) UpdateMeeting(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateParentMeetingRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateMeeting(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate meeting", err)
	}

	return common.Success(c, "Meeting berhasil diupdate", result)
}

func (h *ParentPartnershipHandler) DeleteMeeting(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteMeeting(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus meeting", err)
	}

	return common.Success(c, "Meeting berhasil dihapus", nil)
}

// PartnershipActivity Handlers

func (h *ParentPartnershipHandler) GetAllActivities(c *fiber.Ctx) error {
	result, err := h.service.GetAllActivities(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil activities", err)
	}

	return common.Success(c, "Activities berhasil diambil", fiber.Map{
		"activities": result,
		"total":      len(result),
	})
}

func (h *ParentPartnershipHandler) GetActivityByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetActivityByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Activity tidak ditemukan", err)
	}

	return common.Success(c, "Activity berhasil diambil", result)
}

func (h *ParentPartnershipHandler) GetActivitiesByPartnership(c *fiber.Ctx) error {
	partnershipID := c.Params("partnershipId")
	if partnershipID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Partnership ID tidak valid", nil)
	}

	result, err := h.service.GetActivitiesByPartnership(c.Context(), partnershipID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil activities", err)
	}

	return common.Success(c, "Activities berhasil diambil", fiber.Map{
		"activities": result,
		"total":      len(result),
	})
}

func (h *ParentPartnershipHandler) GetActivitiesByDateRange(c *fiber.Ctx) error {
	startDate := c.Query("start_date")
	endDate := c.Query("end_date")

	if startDate == "" || endDate == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Start date dan end date diperlukan", nil)
	}

	result, err := h.service.GetActivitiesByDateRange(c.Context(), startDate, endDate)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil activities", err)
	}

	return common.Success(c, "Activities berhasil diambil", fiber.Map{
		"activities": result,
		"total":      len(result),
	})
}

func (h *ParentPartnershipHandler) CreateActivity(c *fiber.Ctx) error {
	var req CreatePartnershipActivityRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateActivity(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat activity", err)
	}

	return common.Success(c, "Activity berhasil dibuat", result)
}

func (h *ParentPartnershipHandler) UpdateActivity(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdatePartnershipActivityRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateActivity(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate activity", err)
	}

	return common.Success(c, "Activity berhasil diupdate", result)
}

func (h *ParentPartnershipHandler) DeleteActivity(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteActivity(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus activity", err)
	}

	return common.Success(c, "Activity berhasil dihapus", nil)
}

// Summary Handler

func (h *ParentPartnershipHandler) GetPartnershipSummary(c *fiber.Ctx) error {
	result, err := h.service.GetPartnershipSummary(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil partnership summary", err)
	}

	return common.Success(c, "Partnership summary berhasil diambil", result)
}
