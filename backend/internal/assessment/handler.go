package assessment

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type AssessmentHandler struct {
	svc AssessmentService
}

func NewAssessmentHandler(svc AssessmentService) *AssessmentHandler {
	return &AssessmentHandler{svc: svc}
}

// GetAssessmentsHandler godoc
func (h *AssessmentHandler) GetAssessments(c *fiber.Ctx) error {
	data, err := h.svc.GetByTeachingAssignment(c.UserContext(), c.Params("assignmentId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data asesmen", err)
	}
	return common.Success(c, "Data asesmen berhasil diambil", data)
}

// GetAssessmentByIDHandler godoc
func (h *AssessmentHandler) GetAssessmentByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Asesmen tidak ditemukan", err)
	}
	return common.Success(c, "Detail asesmen berhasil diambil", data)
}

// CreateAssessmentHandler godoc
func (h *AssessmentHandler) CreateAssessment(c *fiber.Ctx) error {
	var req CreateAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.Create(c.UserContext(), c.Params("assignmentId"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat asesmen", err)
	}
	return common.Created(c, "Asesmen berhasil dibuat", data)
}

// UpdateAssessmentHandler godoc
func (h *AssessmentHandler) UpdateAssessment(c *fiber.Ctx) error {
	var req UpdateAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}

	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui asesmen", err)
	}
	return common.Success(c, "Asesmen berhasil diperbarui", data)
}

// DeleteAssessmentHandler godoc
func (h *AssessmentHandler) DeleteAssessment(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus asesmen", err)
	}
	return common.Success(c, "Asesmen berhasil dihapus", nil)
}

// GetScoresHandler godoc
func (h *AssessmentHandler) GetScores(c *fiber.Ctx) error {
	data, err := h.svc.GetScores(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil nilai", err)
	}
	return common.Success(c, "Data nilai berhasil diambil", data)
}

// UpsertScoresHandler godoc
func (h *AssessmentHandler) UpsertScores(c *fiber.Ctx) error {
	var req UpsertScoresRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.UpsertScores(c.UserContext(), c.Params("id"), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menyimpan nilai", err)
	}
	return common.Success(c, "Nilai berhasil disimpan", nil)
}

// GetAttendances godoc
func (h *AssessmentHandler) GetAttendances(c *fiber.Ctx) error {
	classroomID := c.Params("classroomId")
	date := c.Query("date", "")
	if date == "" {
		return common.Error(c, fiber.StatusBadRequest, "Tanggal wajib diisi (?date=YYYY-MM-DD)", nil)
	}

	data, err := h.svc.GetAttendances(c.UserContext(), classroomID, date)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data kehadiran", err)
	}
	return common.Success(c, "Data kehadiran berhasil diambil", data)
}

// UpsertAttendances godoc
func (h *AssessmentHandler) UpsertAttendances(c *fiber.Ctx) error {
	classroomID := c.Params("classroomId")
	date := c.Query("date", "")
	if date == "" {
		return common.Error(c, fiber.StatusBadRequest, "Tanggal wajib diisi (?date=YYYY-MM-DD)", nil)
	}

	var req UpsertAttendancesRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.UpsertAttendances(c.UserContext(), classroomID, date, req); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menyimpan data kehadiran", err)
	}
	return common.Success(c, "Data kehadiran berhasil disimpan", nil)
}

// GetAgeAppropriateTypes godoc
func (h *AssessmentHandler) GetAgeAppropriateTypes(c *fiber.Ctx) error {
	data := h.svc.GetAgeAppropriateTypes()
	return common.Success(c, "Tipe asesmen SD berhasil diambil", data)
}

// SD Assessment Criteria Handlers

// GetAllSDAssessmentCriteria godoc
func (h *AssessmentHandler) GetAllSDAssessmentCriteria(c *fiber.Ctx) error {
	data, err := h.svc.GetAllSDAssessmentCriteria(c.UserContext())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil kriteria asesmen SD", err)
	}
	return common.Success(c, "Kriteria asesmen SD berhasil diambil", data)
}

// GetSDAssessmentCriteriaByType godoc
func (h *AssessmentHandler) GetSDAssessmentCriteriaByType(c *fiber.Ctx) error {
	assessmentType := c.Params("type")
	data, err := h.svc.GetSDAssessmentCriteriaByType(c.UserContext(), assessmentType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil kriteria asesmen SD berdasarkan tipe", err)
	}
	return common.Success(c, "Kriteria asesmen SD berhasil diambil", data)
}

// GetSDAssessmentCriteriaByPhase godoc
func (h *AssessmentHandler) GetSDAssessmentCriteriaByPhase(c *fiber.Ctx) error {
	phaseID := c.Params("phaseId")
	data, err := h.svc.GetSDAssessmentCriteriaByPhase(c.UserContext(), phaseID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil kriteria asesmen SD berdasarkan fase", err)
	}
	return common.Success(c, "Kriteria asesmen SD berhasil diambil", data)
}

// CreateSDAssessmentCriteria godoc
func (h *AssessmentHandler) CreateSDAssessmentCriteria(c *fiber.Ctx) error {
	var req CreateSDAssessmentCriteriaRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}

	data, err := h.svc.CreateSDAssessmentCriteria(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat kriteria asesmen SD", err)
	}
	return common.Created(c, "Kriteria asesmen SD berhasil dibuat", data)
}

// UpdateSDAssessmentCriteria godoc
func (h *AssessmentHandler) UpdateSDAssessmentCriteria(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateSDAssessmentCriteriaRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}

	data, err := h.svc.UpdateSDAssessmentCriteria(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate kriteria asesmen SD", err)
	}
	return common.Success(c, "Kriteria asesmen SD berhasil diupdate", data)
}

// DeleteSDAssessmentCriteria godoc
func (h *AssessmentHandler) DeleteSDAssessmentCriteria(c *fiber.Ctx) error {
	if err := h.svc.DeleteSDAssessmentCriteria(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus kriteria asesmen SD", err)
	}
	return common.Success(c, "Kriteria asesmen SD berhasil dihapus", nil)
}
