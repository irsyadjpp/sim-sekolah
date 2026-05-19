package intelligence

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type IntelligenceHandler struct {
	svc IntelligenceService
}

func NewIntelligenceHandler(svc IntelligenceService) *IntelligenceHandler {
	return &IntelligenceHandler{svc: svc}
}

func (h *IntelligenceHandler) GetStudent360(c *fiber.Ctx) error {
	studentID := c.Params("student_id")
	if studentID == "" {
		return common.Error(c, fiber.StatusBadRequest, "ID murid wajib diisi", nil)
	}

	profile, err := h.svc.GetStudent360Profile(c.UserContext(), studentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil profil murid", err)
	}
	return common.Success(c, "Profil 360 murid berhasil diambil", profile)
}

func (h *IntelligenceHandler) UpsertProfileExt(c *fiber.Ctx) error {
	studentID := c.Params("student_id")
	if studentID == "" {
		return common.Error(c, fiber.StatusBadRequest, "ID murid wajib diisi", nil)
	}

	var req UpsertProfileExtRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	err := h.svc.UpsertProfileExt(c.UserContext(), studentID, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui ekstensi profil murid", err)
	}
	return common.Success(c, "Ekstensi profil murid berhasil diperbarui", nil)
}

func (h *IntelligenceHandler) CreateAnecdotal(c *fiber.Ctx) error {
	var req CreateAnecdotalRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	teacherID, ok := c.Locals("user_id").(string)
	if !ok || teacherID == "" {
		return common.Error(c, fiber.StatusUnauthorized, "Tidak terautentikasi", "ID guru tidak ditemukan")
	}

	obs, err := h.svc.CreateAnecdotal(c.UserContext(), req, teacherID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mencatat observasi", err)
	}
	return common.Success(c, "Catatan observasi anekdotal berhasil disimpan", obs)
}

func (h *IntelligenceHandler) GetObservationTags(c *fiber.Ctx) error {
	tags, err := h.svc.GetObservationTags(c.UserContext())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil tag observasi", err)
	}
	return common.Success(c, "Daftar tag observasi berhasil diambil", tags)
}

func (h *IntelligenceHandler) CreateInstrument(c *fiber.Ctx) error {
	var req CreateInstrumentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	inst, err := h.svc.CreateInstrument(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat instrumen penilaian", err)
	}
	return common.Success(c, "Instrumen penilaian berhasil dibuat", inst)
}

func (h *IntelligenceHandler) SubmitResults(c *fiber.Ctx) error {
	instrumentID := c.Params("instrument_id")
	if instrumentID == "" {
		return common.Error(c, fiber.StatusBadRequest, "ID instrumen penilaian wajib diisi", nil)
	}

	var req SubmitResultsBatchRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	err := h.svc.SubmitResultsBatch(c.UserContext(), instrumentID, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengirim nilai", err)
	}
	return common.Success(c, "Nilai penilaian massal murid berhasil dikirim", nil)
}

func (h *IntelligenceHandler) GetResults(c *fiber.Ctx) error {
	instrumentID := c.Params("instrument_id")
	if instrumentID == "" {
		return common.Error(c, fiber.StatusBadRequest, "ID instrumen penilaian wajib diisi", nil)
	}

	results, err := h.svc.GetResultsByInstrument(c.UserContext(), instrumentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil nilai", err)
	}
	return common.Success(c, "Nilai penilaian murid berhasil diambil", results)
}

func (h *IntelligenceHandler) GetAlerts(c *fiber.Ctx) error {
	classroomID := c.Query("classroom_id")
	if classroomID == "" {
		return common.Error(c, fiber.StatusBadRequest, "Parameter query classroom_id wajib diisi", nil)
	}

	alerts, err := h.svc.GetAlertsByClassroom(c.UserContext(), classroomID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil peringatan EWS", err)
	}
	return common.Success(c, "Peringatan EWS kelas berhasil diambil", alerts)
}

func (h *IntelligenceHandler) UpdateAlert(c *fiber.Ctx) error {
	alertID := c.Params("alert_id")
	if alertID == "" {
		return common.Error(c, fiber.StatusBadRequest, "ID peringatan wajib diisi", nil)
	}

	var req EarlyWarningInterventionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	err := h.svc.UpdateAlert(c.UserContext(), alertID, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui status peringatan bimbingan", err)
	}
	return common.Success(c, "Intervensi bimbingan EWS berhasil dicatat", nil)
}

func (h *IntelligenceHandler) TriggerCron(c *fiber.Ctx) error {
	err := h.svc.CalculateEarlyWarningAlerts(c.UserContext())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menjalankan analitik EWS", err)
	}
	return common.Success(c, "Asisten analitik risiko EWS berhasil dipicu", nil)
}
