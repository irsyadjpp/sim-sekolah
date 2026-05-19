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
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data asesmen", err.Error())
	}
	return common.Success(c, "Data asesmen berhasil diambil", data)
}

// GetAssessmentByIDHandler godoc
func (h *AssessmentHandler) GetAssessmentByID(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Asesmen tidak ditemukan", err.Error())
	}
	return common.Success(c, "Detail asesmen berhasil diambil", data)
}

// CreateAssessmentHandler godoc
func (h *AssessmentHandler) CreateAssessment(c *fiber.Ctx) error {
	var req CreateAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	data, err := h.svc.Create(c.UserContext(), c.Params("assignmentId"), req)
	if err != nil {
		status := fiber.StatusInternalServerError
		if err.Error() == "forbidden: you don't have permission to modify this resource" {
			status = fiber.StatusForbidden
		}
		return common.Error(c, status, "Gagal membuat asesmen", err.Error())
	}
	return common.Created(c, "Asesmen berhasil dibuat", data)
}

// UpdateAssessmentHandler godoc
func (h *AssessmentHandler) UpdateAssessment(c *fiber.Ctx) error {
	var req UpdateAssessmentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}

	data, err := h.svc.Update(c.UserContext(), c.Params("id"), req)
	if err != nil {
		status := fiber.StatusInternalServerError
		if err.Error() == "forbidden: you don't have permission to modify this resource" {
			status = fiber.StatusForbidden
		}
		return common.Error(c, status, "Gagal memperbarui asesmen", err.Error())
	}
	return common.Success(c, "Asesmen berhasil diperbarui", data)
}

// DeleteAssessmentHandler godoc
func (h *AssessmentHandler) DeleteAssessment(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		status := fiber.StatusInternalServerError
		if err.Error() == "forbidden: you don't have permission to modify this resource" {
			status = fiber.StatusForbidden
		}
		return common.Error(c, status, "Gagal menghapus asesmen", err.Error())
	}
	return common.Success(c, "Asesmen berhasil dihapus", nil)
}

// GetScoresHandler godoc
func (h *AssessmentHandler) GetScores(c *fiber.Ctx) error {
	data, err := h.svc.GetScores(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil nilai", err.Error())
	}
	return common.Success(c, "Data nilai berhasil diambil", data)
}

// UpsertScoresHandler godoc
func (h *AssessmentHandler) UpsertScores(c *fiber.Ctx) error {
	var req UpsertScoresRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	if err := h.svc.UpsertScores(c.UserContext(), c.Params("id"), req); err != nil {
		status := fiber.StatusInternalServerError
		if err.Error() == "forbidden: you don't have permission to modify this resource" {
			status = fiber.StatusForbidden
		}
		return common.Error(c, status, "Gagal menyimpan nilai", err.Error())
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
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data kehadiran", err.Error())
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
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	if err := h.svc.UpsertAttendances(c.UserContext(), classroomID, date, req); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal menyimpan data kehadiran", err.Error())
	}
	return common.Success(c, "Data kehadiran berhasil disimpan", nil)
}
