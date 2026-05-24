package peer_assessment

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type PeerAssessmentHandler struct {
	service PeerAssessmentService
}

func NewPeerAssessmentHandler(service PeerAssessmentService) *PeerAssessmentHandler {
	return &PeerAssessmentHandler{service: service}
}

// PeerAssessmentTemplate Handlers

func (h *PeerAssessmentHandler) GetAllTemplates(c *fiber.Ctx) error {
	result, err := h.service.GetAllTemplates(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil templates", err)
	}

	return common.Success(c, "Templates berhasil diambil", fiber.Map{
		"templates": result,
		"total":     len(result),
	})
}

func (h *PeerAssessmentHandler) GetTemplateByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetTemplateByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Template tidak ditemukan", err)
	}

	return common.Success(c, "Template berhasil diambil", result)
}

func (h *PeerAssessmentHandler) GetTemplatesByType(c *fiber.Ctx) error {
	assessmentType := c.Params("type")
	if assessmentType == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Assessment type tidak valid", nil)
	}

	result, err := h.service.GetTemplatesByType(c.Context(), assessmentType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil templates", err)
	}

	return common.Success(c, "Templates berhasil diambil", fiber.Map{
		"templates": result,
		"total":     len(result),
	})
}

func (h *PeerAssessmentHandler) GetTemplatesByPhase(c *fiber.Ctx) error {
	phase := c.Params("phase")
	if phase == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Phase tidak valid", nil)
	}

	result, err := h.service.GetTemplatesByPhase(c.Context(), phase)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil templates", err)
	}

	return common.Success(c, "Templates berhasil diambil", fiber.Map{
		"templates": result,
		"total":     len(result),
	})
}

func (h *PeerAssessmentHandler) GetTemplatesBySubject(c *fiber.Ctx) error {
	subjectID := c.Params("subjectId")
	if subjectID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Subject ID tidak valid", nil)
	}

	result, err := h.service.GetTemplatesBySubject(c.Context(), subjectID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil templates", err)
	}

	return common.Success(c, "Templates berhasil diambil", fiber.Map{
		"templates": result,
		"total":     len(result),
	})
}

func (h *PeerAssessmentHandler) GetActiveTemplates(c *fiber.Ctx) error {
	result, err := h.service.GetActiveTemplates(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil active templates", err)
	}

	return common.Success(c, "Active templates berhasil diambil", fiber.Map{
		"templates": result,
		"total":     len(result),
	})
}

func (h *PeerAssessmentHandler) CreateTemplate(c *fiber.Ctx) error {
	var req CreatePeerAssessmentTemplateRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateTemplate(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat template", err)
	}

	return common.Success(c, "Template berhasil dibuat", result)
}

func (h *PeerAssessmentHandler) UpdateTemplate(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdatePeerAssessmentTemplateRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateTemplate(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate template", err)
	}

	return common.Success(c, "Template berhasil diupdate", result)
}

func (h *PeerAssessmentHandler) DeleteTemplate(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteTemplate(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus template", err)
	}

	return common.Success(c, "Template berhasil dihapus", nil)
}

// SelfAssessment Handlers

func (h *PeerAssessmentHandler) GetAllSelfAssessments(c *fiber.Ctx) error {
	result, err := h.service.GetAllSelfAssessments(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil self assessments", err)
	}

	return common.Success(c, "Self assessments berhasil diambil", fiber.Map{
		"self_assessments": result,
		"total":            len(result),
	})
}

func (h *PeerAssessmentHandler) GetSelfAssessmentByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetSelfAssessmentByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Self assessment tidak ditemukan", err)
	}

	return common.Success(c, "Self assessment berhasil diambil", result)
}

func (h *PeerAssessmentHandler) GetSelfAssessmentsByStudent(c *fiber.Ctx) error {
	studentID := c.Params("studentId")
	if studentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", nil)
	}

	result, err := h.service.GetSelfAssessmentsByStudent(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil self assessments", err)
	}

	return common.Success(c, "Self assessments berhasil diambil", fiber.Map{
		"self_assessments": result,
		"total":            len(result),
	})
}

func (h *PeerAssessmentHandler) GetSelfAssessmentsByTemplate(c *fiber.Ctx) error {
	templateID := c.Params("templateId")
	if templateID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Template ID tidak valid", nil)
	}

	result, err := h.service.GetSelfAssessmentsByTemplate(c.Context(), templateID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil self assessments", err)
	}

	return common.Success(c, "Self assessments berhasil diambil", fiber.Map{
		"self_assessments": result,
		"total":            len(result),
	})
}

func (h *PeerAssessmentHandler) CreateSelfAssessment(c *fiber.Ctx) error {
	var req CreateSelfAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateSelfAssessment(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat self assessment", err)
	}

	return common.Success(c, "Self assessment berhasil dibuat", result)
}

func (h *PeerAssessmentHandler) UpdateSelfAssessment(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateSelfAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateSelfAssessment(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate self assessment", err)
	}

	return common.Success(c, "Self assessment berhasil diupdate", result)
}

func (h *PeerAssessmentHandler) DeleteSelfAssessment(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteSelfAssessment(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus self assessment", err)
	}

	return common.Success(c, "Self assessment berhasil dihapus", nil)
}

// PeerAssessment Handlers

func (h *PeerAssessmentHandler) GetAllPeerAssessments(c *fiber.Ctx) error {
	result, err := h.service.GetAllPeerAssessments(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil peer assessments", err)
	}

	return common.Success(c, "Peer assessments berhasil diambil", fiber.Map{
		"peer_assessments": result,
		"total":            len(result),
	})
}

func (h *PeerAssessmentHandler) GetPeerAssessmentByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetPeerAssessmentByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Peer assessment tidak ditemukan", err)
	}

	return common.Success(c, "Peer assessment berhasil diambil", result)
}

func (h *PeerAssessmentHandler) GetPeerAssessmentsByAssessor(c *fiber.Ctx) error {
	assessorID := c.Params("assessorId")
	if assessorID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Assessor ID tidak valid", nil)
	}

	result, err := h.service.GetPeerAssessmentsByAssessor(c.Context(), assessorID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil peer assessments", err)
	}

	return common.Success(c, "Peer assessments berhasil diambil", fiber.Map{
		"peer_assessments": result,
		"total":            len(result),
	})
}

func (h *PeerAssessmentHandler) GetPeerAssessmentsByAssessed(c *fiber.Ctx) error {
	assessedID := c.Params("assessedId")
	if assessedID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Assessed ID tidak valid", nil)
	}

	result, err := h.service.GetPeerAssessmentsByAssessed(c.Context(), assessedID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil peer assessments", err)
	}

	return common.Success(c, "Peer assessments berhasil diambil", fiber.Map{
		"peer_assessments": result,
		"total":            len(result),
	})
}

func (h *PeerAssessmentHandler) GetPeerAssessmentsByTemplate(c *fiber.Ctx) error {
	templateID := c.Params("templateId")
	if templateID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Template ID tidak valid", nil)
	}

	result, err := h.service.GetPeerAssessmentsByTemplate(c.Context(), templateID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil peer assessments", err)
	}

	return common.Success(c, "Peer assessments berhasil diambil", fiber.Map{
		"peer_assessments": result,
		"total":            len(result),
	})
}

func (h *PeerAssessmentHandler) GetPendingPeerReviews(c *fiber.Ctx) error {
	result, err := h.service.GetPendingPeerReviews(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil pending peer reviews", err)
	}

	return common.Success(c, "Pending peer reviews berhasil diambil", fiber.Map{
		"peer_assessments": result,
		"total":            len(result),
	})
}

func (h *PeerAssessmentHandler) CreatePeerAssessment(c *fiber.Ctx) error {
	var req CreatePeerAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreatePeerAssessment(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat peer assessment", err)
	}

	return common.Success(c, "Peer assessment berhasil dibuat", result)
}

func (h *PeerAssessmentHandler) UpdatePeerAssessment(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdatePeerAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdatePeerAssessment(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate peer assessment", err)
	}

	return common.Success(c, "Peer assessment berhasil diupdate", result)
}

func (h *PeerAssessmentHandler) DeletePeerAssessment(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeletePeerAssessment(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus peer assessment", err)
	}

	return common.Success(c, "Peer assessment berhasil dihapus", nil)
}

// GroupAssessment Handlers

func (h *PeerAssessmentHandler) GetAllGroupAssessments(c *fiber.Ctx) error {
	result, err := h.service.GetAllGroupAssessments(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil group assessments", err)
	}

	return common.Success(c, "Group assessments berhasil diambil", fiber.Map{
		"group_assessments": result,
		"total":             len(result),
	})
}

func (h *PeerAssessmentHandler) GetGroupAssessmentByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetGroupAssessmentByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Group assessment tidak ditemukan", err)
	}

	return common.Success(c, "Group assessment berhasil diambil", result)
}

func (h *PeerAssessmentHandler) GetGroupAssessmentsByGroup(c *fiber.Ctx) error {
	groupID := c.Params("groupId")
	if groupID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Group ID tidak valid", nil)
	}

	result, err := h.service.GetGroupAssessmentsByGroup(c.Context(), groupID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil group assessments", err)
	}

	return common.Success(c, "Group assessments berhasil diambil", fiber.Map{
		"group_assessments": result,
		"total":             len(result),
	})
}

func (h *PeerAssessmentHandler) GetGroupAssessmentsByTemplate(c *fiber.Ctx) error {
	templateID := c.Params("templateId")
	if templateID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Template ID tidak valid", nil)
	}

	result, err := h.service.GetGroupAssessmentsByTemplate(c.Context(), templateID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil group assessments", err)
	}

	return common.Success(c, "Group assessments berhasil diambil", fiber.Map{
		"group_assessments": result,
		"total":             len(result),
	})
}

func (h *PeerAssessmentHandler) CreateGroupAssessment(c *fiber.Ctx) error {
	var req CreateGroupAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateGroupAssessment(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat group assessment", err)
	}

	return common.Success(c, "Group assessment berhasil dibuat", result)
}

func (h *PeerAssessmentHandler) UpdateGroupAssessment(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateGroupAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateGroupAssessment(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate group assessment", err)
	}

	return common.Success(c, "Group assessment berhasil diupdate", result)
}

func (h *PeerAssessmentHandler) DeleteGroupAssessment(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteGroupAssessment(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus group assessment", err)
	}

	return common.Success(c, "Group assessment berhasil dihapus", nil)
}

// GroupAssessmentMember Handlers

func (h *PeerAssessmentHandler) GetAllGroupAssessmentMembers(c *fiber.Ctx) error {
	result, err := h.service.GetAllGroupAssessmentMembers(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil group assessment members", err)
	}

	return common.Success(c, "Group assessment members berhasil diambil", fiber.Map{
		"group_assessment_members": result,
		"total":                    len(result),
	})
}

func (h *PeerAssessmentHandler) GetGroupAssessmentMemberByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetGroupAssessmentMemberByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Group assessment member tidak ditemukan", err)
	}

	return common.Success(c, "Group assessment member berhasil diambil", result)
}

func (h *PeerAssessmentHandler) GetGroupAssessmentMembersByGroupAssessment(c *fiber.Ctx) error {
	groupAssessmentID := c.Params("groupAssessmentId")
	if groupAssessmentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Group Assessment ID tidak valid", nil)
	}

	result, err := h.service.GetGroupAssessmentMembersByGroupAssessment(c.Context(), groupAssessmentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil group assessment members", err)
	}

	return common.Success(c, "Group assessment members berhasil diambil", fiber.Map{
		"group_assessment_members": result,
		"total":                    len(result),
	})
}

func (h *PeerAssessmentHandler) GetGroupAssessmentMembersByStudent(c *fiber.Ctx) error {
	studentID := c.Params("studentId")
	if studentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Student ID tidak valid", nil)
	}

	result, err := h.service.GetGroupAssessmentMembersByStudent(c.Context(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil group assessment members", err)
	}

	return common.Success(c, "Group assessment members berhasil diambil", fiber.Map{
		"group_assessment_members": result,
		"total":                    len(result),
	})
}

func (h *PeerAssessmentHandler) CreateGroupAssessmentMember(c *fiber.Ctx) error {
	var req CreateGroupAssessmentMemberRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateGroupAssessmentMember(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat group assessment member", err)
	}

	return common.Success(c, "Group assessment member berhasil dibuat", result)
}

func (h *PeerAssessmentHandler) UpdateGroupAssessmentMember(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdateGroupAssessmentMemberRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateGroupAssessmentMember(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate group assessment member", err)
	}

	return common.Success(c, "Group assessment member berhasil diupdate", result)
}

func (h *PeerAssessmentHandler) DeleteGroupAssessmentMember(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteGroupAssessmentMember(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus group assessment member", err)
	}

	return common.Success(c, "Group assessment member berhasil dihapus", nil)
}

// PeerAssessmentGuideline Handlers

func (h *PeerAssessmentHandler) GetAllGuidelines(c *fiber.Ctx) error {
	result, err := h.service.GetAllGuidelines(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil guidelines", err)
	}

	return common.Success(c, "Guidelines berhasil diambil", fiber.Map{
		"guidelines": result,
		"total":      len(result),
	})
}

func (h *PeerAssessmentHandler) GetGuidelineByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	result, err := h.service.GetGuidelineByID(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Guideline tidak ditemukan", err)
	}

	return common.Success(c, "Guideline berhasil diambil", result)
}

func (h *PeerAssessmentHandler) GetGuidelinesByPhase(c *fiber.Ctx) error {
	phase := c.Params("phase")
	if phase == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Phase tidak valid", nil)
	}

	result, err := h.service.GetGuidelinesByPhase(c.Context(), phase)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil guidelines", err)
	}

	return common.Success(c, "Guidelines berhasil diambil", fiber.Map{
		"guidelines": result,
		"total":      len(result),
	})
}

func (h *PeerAssessmentHandler) GetGuidelinesByCategory(c *fiber.Ctx) error {
	category := c.Params("category")
	if category == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Category tidak valid", nil)
	}

	result, err := h.service.GetGuidelinesByCategory(c.Context(), category)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil guidelines", err)
	}

	return common.Success(c, "Guidelines berhasil diambil", fiber.Map{
		"guidelines": result,
		"total":      len(result),
	})
}

func (h *PeerAssessmentHandler) GetActiveGuidelines(c *fiber.Ctx) error {
	result, err := h.service.GetActiveGuidelines(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil active guidelines", err)
	}

	return common.Success(c, "Active guidelines berhasil diambil", fiber.Map{
		"guidelines": result,
		"total":      len(result),
	})
}

func (h *PeerAssessmentHandler) CreateGuideline(c *fiber.Ctx) error {
	var req CreatePeerAssessmentGuidelineRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.CreateGuideline(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat guideline", err)
	}

	return common.Success(c, "Guideline berhasil dibuat", result)
}

func (h *PeerAssessmentHandler) UpdateGuideline(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	var req UpdatePeerAssessmentGuidelineRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	result, err := h.service.UpdateGuideline(c.Context(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate guideline", err)
	}

	return common.Success(c, "Guideline berhasil diupdate", result)
}

func (h *PeerAssessmentHandler) DeleteGuideline(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID tidak valid", nil)
	}

	err := h.service.DeleteGuideline(c.Context(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus guideline", err)
	}

	return common.Success(c, "Guideline berhasil dihapus", nil)
}

// Summary Handler

func (h *PeerAssessmentHandler) GetPeerAssessmentSummary(c *fiber.Ctx) error {
	result, err := h.service.GetPeerAssessmentSummary(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil peer assessment summary", err)
	}

	return common.Success(c, "Peer assessment summary berhasil diambil", result)
}
