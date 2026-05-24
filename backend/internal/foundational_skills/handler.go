package foundational_skills

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type Handler struct {
	service Service
}

func NewHandler(service Service) *Handler {
	return &Handler{service: service}
}

// RegisterRoutes registers the foundational skills routes
func (h *Handler) RegisterRoutes(group fiber.Router) {
	foundationalSkills := group.Group("/foundational-skills")
	{
		// Skill Standard Endpoints
		foundationalSkills.Get("/standards", h.GetAllSkillStandards)
		foundationalSkills.Get("/standards/:id", h.GetSkillStandardByID)
		foundationalSkills.Get("/standards/type/:type", h.GetSkillStandardsByType)
		foundationalSkills.Post("/standards", h.CreateSkillStandard)
		foundationalSkills.Put("/standards/:id", h.UpdateSkillStandard)
		foundationalSkills.Delete("/standards/:id", h.DeleteSkillStandard)

		// Assessment Endpoints
		foundationalSkills.Get("/assessments", h.GetAllAssessments)
		foundationalSkills.Get("/assessments/:id", h.GetAssessmentByID)
		foundationalSkills.Get("/students/:studentId", h.GetStudentProgress)
		foundationalSkills.Get("/standards/:standardId/assessments", h.GetAssessmentsByStandard)
		foundationalSkills.Post("/assessments", h.CreateAssessment)
		foundationalSkills.Put("/assessments/:id", h.UpdateAssessment)
		foundationalSkills.Delete("/assessments/:id", h.DeleteAssessment)
	}
}

// Skill Standard Handlers
func (h *Handler) GetAllSkillStandards(c *fiber.Ctx) error {
	standards, err := h.service.GetAllSkillStandards()
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil standar keterampilan dasar", err)
	}

	return common.Success(c, "Standar keterampilan dasar berhasil diambil", fiber.Map{
		"standards": standards,
		"total":     len(standards),
	})
}

func (h *Handler) GetSkillStandardByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	standard, err := h.service.GetSkillStandardByID(id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Standar keterampilan dasar tidak ditemukan", err)
	}

	return common.Success(c, "Standar keterampilan dasar berhasil diambil", standard)
}

func (h *Handler) GetSkillStandardsByType(c *fiber.Ctx) error {
	skillType := c.Params("type")
	if skillType == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Tipe keterampilan diperlukan", nil)
	}

	standards, err := h.service.GetSkillStandardsByType(skillType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, err.Error(), err)
	}

	return common.Success(c, "Standar keterampilan dasar berhasil diambil", fiber.Map{
		"standards": standards,
		"total":     len(standards),
	})
}

func (h *Handler) CreateSkillStandard(c *fiber.Ctx) error {
	var req CreateSkillStandardRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	standard, err := h.service.CreateSkillStandard(req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat standar keterampilan dasar", err)
	}

	return common.Success(c, "Standar keterampilan dasar berhasil dibuat", standard)
}

func (h *Handler) UpdateSkillStandard(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	var req UpdateSkillStandardRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	standard, err := h.service.UpdateSkillStandard(id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate standar keterampilan dasar", err)
	}

	return common.Success(c, "Standar keterampilan dasar berhasil diupdate", standard)
}

func (h *Handler) DeleteSkillStandard(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	if err := h.service.DeleteSkillStandard(id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus standar keterampilan dasar", err)
	}

	return common.Success(c, "Standar keterampilan dasar berhasil dihapus", nil)
}

// Assessment Handlers
func (h *Handler) GetAllAssessments(c *fiber.Ctx) error {
	assessments, err := h.service.GetAllAssessments()
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil asesmen keterampilan dasar", err)
	}

	return common.Success(c, "Asesmen keterampilan dasar berhasil diambil", fiber.Map{
		"assessments": assessments,
		"total":       len(assessments),
	})
}

func (h *Handler) GetAssessmentByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	assessment, err := h.service.GetAssessmentByID(id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Asesmen keterampilan dasar tidak ditemukan", err)
	}

	return common.Success(c, "Asesmen keterampilan dasar berhasil diambil", assessment)
}

func (h *Handler) GetStudentProgress(c *fiber.Ctx) error {
	studentID := c.Params("studentId")
	if studentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID siswa diperlukan", nil)
	}

	progress, err := h.service.GetStudentProgress(studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil progres siswa", err)
	}

	return common.Success(c, "Progres siswa berhasil diambil", progress)
}

func (h *Handler) GetAssessmentsByStandard(c *fiber.Ctx) error {
	standardID := c.Params("standardId")
	if standardID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID standar diperlukan", nil)
	}

	assessments, err := h.service.GetAssessmentsByStandard(standardID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil asesmen berdasarkan standar", err)
	}

	return common.Success(c, "Asesmen keterampilan dasar berhasil diambil", fiber.Map{
		"assessments": assessments,
		"total":       len(assessments),
	})
}

func (h *Handler) CreateAssessment(c *fiber.Ctx) error {
	var req CreateAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	assessment, err := h.service.CreateAssessment(req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat asesmen keterampilan dasar", err)
	}

	return common.Success(c, "Asesmen keterampilan dasar berhasil dibuat", assessment)
}

func (h *Handler) UpdateAssessment(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	var req UpdateAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	assessment, err := h.service.UpdateAssessment(id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate asesmen keterampilan dasar", err)
	}

	return common.Success(c, "Asesmen keterampilan dasar berhasil diupdate", assessment)
}

func (h *Handler) DeleteAssessment(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	if err := h.service.DeleteAssessment(id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus asesmen keterampilan dasar", err)
	}

	return common.Success(c, "Asesmen keterampilan dasar berhasil dihapus", nil)
}
