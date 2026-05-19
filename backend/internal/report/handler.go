package report

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type ReportHandler struct {
	svc ReportService
}

func NewReportHandler(svc ReportService) *ReportHandler {
	return &ReportHandler{svc: svc}
}

// GenerateReportsHandler godoc
func (h *ReportHandler) GenerateReports(c *fiber.Ctx) error {
	var req GenerateReportRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.GenerateReportsForClassroom(c.UserContext(), c.Params("classroomId"), req.Semester); err != nil {
		return common.ErrorFromService(c, fiber.StatusForbidden, "Gagal membuat draft rapor", err)
	}
	return common.Created(c, "Draft rapor berhasil dibuat", nil)
}

// GetReportsByClassroomHandler godoc
func (h *ReportHandler) GetReportsByClassroom(c *fiber.Ctx) error {
	semester := c.Query("semester")
	if semester == "" {
		return common.Error(c, fiber.StatusBadRequest, "Parameter semester wajib diisi", "")
	}

	data, err := h.svc.GetByClassroom(c.UserContext(), c.Params("classroomId"), semester)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data rapor", err)
	}
	return common.Success(c, "Data rapor berhasil diambil", data)
}

// GetReportDetailHandler godoc
func (h *ReportHandler) GetReportDetail(c *fiber.Ctx) error {
	data, err := h.svc.GetByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Rapor tidak ditemukan", err)
	}
	return common.Success(c, "Detail rapor berhasil diambil", data)
}

// UpsertReportNotesHandler godoc
func (h *ReportHandler) UpsertReportNotes(c *fiber.Ctx) error {
	var req UpsertReportNotesRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := h.svc.UpsertNotes(c.UserContext(), c.Params("id"), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusForbidden, "Gagal menyimpan catatan", err)
	}
	return common.Success(c, "Catatan berhasil disimpan", nil)
}

// UpsertReportScoreHandler godoc
func (h *ReportHandler) UpsertReportScore(c *fiber.Ctx) error {
	var req UpsertReportScoreRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	if err := h.svc.UpsertScore(c.UserContext(), c.Params("id"), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusForbidden, "Gagal menyimpan nilai", err)
	}
	return common.Success(c, "Nilai mapel berhasil disimpan", nil)
}

func (h *ReportHandler) UpsertP5(c *fiber.Ctx) error {
	var req UpsertReportP5Request
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	if err := h.svc.UpsertP5(c.UserContext(), c.Params("id"), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusForbidden, "Gagal menyimpan P5", err)
	}
	return common.Success(c, "Data P5 berhasil disimpan", nil)
}

func (h *ReportHandler) UpsertDeepLearning(c *fiber.Ctx) error {
	var req UpsertReportDeepLearningRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	if err := h.svc.UpsertDeepLearning(c.UserContext(), c.Params("id"), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusForbidden, "Gagal menyimpan data deep learning", err)
	}
	return common.Success(c, "Data Deep Learning disimpan", nil)
}

func (h *ReportHandler) UpsertExtracurricular(c *fiber.Ctx) error {
	var req UpsertReportExtracurricularRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	if err := h.svc.UpsertExtracurricular(c.UserContext(), c.Params("id"), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusForbidden, "Gagal menyimpan data ekstrakurikuler", err)
	}
	return common.Success(c, "Data Ekstrakurikuler disimpan", nil)
}

func (h *ReportHandler) UpsertAttendance(c *fiber.Ctx) error {
	var req UpsertReportAttendanceRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}
	if err := h.svc.UpsertAttendance(c.UserContext(), c.Params("id"), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusForbidden, "Gagal menyimpan data absensi", err)
	}
	return common.Success(c, "Data Absensi disimpan", nil)
}

func (h *ReportHandler) FinalizeReport(c *fiber.Ctx) error {
	if err := h.svc.FinalizeReport(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusForbidden, "Gagal finalisasi rapor", err)
	}
	return common.Success(c, "Rapor berhasil difinalisasi", nil)
}

func (h *ReportHandler) GenerateAIDescription(c *fiber.Ctx) error {
	if err := h.svc.GenerateReportNarrativeAI(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menyusun narasi AI", err)
	}
	return common.Success(c, "Narasi rapor berhasil disusun oleh AI", nil)
}
