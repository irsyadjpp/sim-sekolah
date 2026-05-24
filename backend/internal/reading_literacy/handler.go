package reading_literacy

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

// RegisterRoutes registers the reading literacy routes
func (h *Handler) RegisterRoutes(group fiber.Router) {
	readingLiteracy := group.Group("/reading-literacy")
	{
		// Reading Level Endpoints
		readingLiteracy.Get("/levels", h.GetAllReadingLevels)
		readingLiteracy.Get("/levels/:id", h.GetReadingLevelByID)
		readingLiteracy.Get("/levels/code/:code", h.GetReadingLevelByCode)
		readingLiteracy.Post("/levels", h.CreateReadingLevel)
		readingLiteracy.Put("/levels/:id", h.UpdateReadingLevel)
		readingLiteracy.Delete("/levels/:id", h.DeleteReadingLevel)

		// Assessment Endpoints
		readingLiteracy.Get("/assessments", h.GetAllAssessments)
		readingLiteracy.Get("/assessments/:id", h.GetAssessmentByID)
		readingLiteracy.Get("/students/:studentId", h.GetStudentProgression)
		readingLiteracy.Get("/levels/:levelId/assessments", h.GetAssessmentsByLevel)
		readingLiteracy.Post("/assessments", h.CreateAssessment)
		readingLiteracy.Put("/assessments/:id", h.UpdateAssessment)
		readingLiteracy.Delete("/assessments/:id", h.DeleteAssessment)
	}
}

// Reading Level Handlers
func (h *Handler) GetAllReadingLevels(c *fiber.Ctx) error {
	levels, err := h.service.GetAllReadingLevels()
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil level membaca", err)
	}

	return common.Success(c, "Level membaca berhasil diambil", fiber.Map{
		"levels": levels,
		"total":  len(levels),
	})
}

func (h *Handler) GetReadingLevelByID(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	level, err := h.service.GetReadingLevelByID(id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Level membaca tidak ditemukan", err)
	}

	return common.Success(c, "Level membaca berhasil diambil", level)
}

func (h *Handler) GetReadingLevelByCode(c *fiber.Ctx) error {
	levelCode := c.Params("code")
	if levelCode == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Kode level diperlukan", nil)
	}

	level, err := h.service.GetReadingLevelByCode(levelCode)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Level membaca tidak ditemukan", err)
	}

	return common.Success(c, "Level membaca berhasil diambil", level)
}

func (h *Handler) CreateReadingLevel(c *fiber.Ctx) error {
	var req CreateReadingLevelRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	level, err := h.service.CreateReadingLevel(req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat level membaca", err)
	}

	return common.Success(c, "Level membaca berhasil dibuat", level)
}

func (h *Handler) UpdateReadingLevel(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	var req UpdateReadingLevelRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format request tidak valid", err)
	}

	level, err := h.service.UpdateReadingLevel(id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate level membaca", err)
	}

	return common.Success(c, "Level membaca berhasil diupdate", level)
}

func (h *Handler) DeleteReadingLevel(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	if err := h.service.DeleteReadingLevel(id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus level membaca", err)
	}

	return common.Success(c, "Level membaca berhasil dihapus", nil)
}

// Assessment Handlers
func (h *Handler) GetAllAssessments(c *fiber.Ctx) error {
	assessments, err := h.service.GetAllAssessments()
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil asesmen literasi membaca", err)
	}

	return common.Success(c, "Asesmen literasi membaca berhasil diambil", fiber.Map{
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
		return common.ErrorFromService(c, fiber.StatusNotFound, "Asesmen literasi membaca tidak ditemukan", err)
	}

	return common.Success(c, "Asesmen literasi membaca berhasil diambil", assessment)
}

func (h *Handler) GetStudentProgression(c *fiber.Ctx) error {
	studentID := c.Params("studentId")
	if studentID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID siswa diperlukan", nil)
	}

	progression, err := h.service.GetStudentProgression(studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil progres siswa", err)
	}

	return common.Success(c, "Progres siswa berhasil diambil", progression)
}

func (h *Handler) GetAssessmentsByLevel(c *fiber.Ctx) error {
	levelID := c.Params("levelId")
	if levelID == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID level diperlukan", nil)
	}

	assessments, err := h.service.GetAssessmentsByLevel(levelID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil asesmen berdasarkan level", err)
	}

	return common.Success(c, "Asesmen literasi membaca berhasil diambil", fiber.Map{
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
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat asesmen literasi membaca", err)
	}

	return common.Success(c, "Asesmen literasi membaca berhasil dibuat", assessment)
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
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate asesmen literasi membaca", err)
	}

	return common.Success(c, "Asesmen literasi membaca berhasil diupdate", assessment)
}

func (h *Handler) DeleteAssessment(c *fiber.Ctx) error {
	id := c.Params("id")
	if id == "" {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID diperlukan", nil)
	}

	if err := h.service.DeleteAssessment(id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus asesmen literasi membaca", err)
	}

	return common.Success(c, "Asesmen literasi membaca berhasil dihapus", nil)
}
