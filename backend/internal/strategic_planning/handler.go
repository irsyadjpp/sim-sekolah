package strategic_planning

import (
	"fmt"
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type Handler struct {
	svc Service
}

func NewHandler(svc Service) *Handler {
	return &Handler{svc: svc}
}

// Rapor Pendidikan Handlers
func (h *Handler) CreateRaporPendidikan(c *fiber.Ctx) error {
	var req CreateRaporPendidikanRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateRaporPendidikan(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat data rapor pendidikan", err)
	}
	return common.Created(c, "Data rapor pendidikan berhasil dibuat", data)
}

func (h *Handler) GetRaporPendidikanByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetRaporPendidikanByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Data rapor pendidikan tidak ditemukan", err)
	}
	return common.Success(c, "Detail data rapor pendidikan berhasil diambil", data)
}

func (h *Handler) GetRaporPendidikanBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	year := c.Query("year")
	data, err := h.svc.GetRaporPendidikanBySchool(c.UserContext(), schoolID, year)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data rapor pendidikan", err)
	}
	return common.Success(c, "Data rapor pendidikan berhasil diambil", data)
}

func (h *Handler) UpdateRaporPendidikan(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateRaporPendidikanRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateRaporPendidikan(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui data rapor pendidikan", err)
	}
	return common.Success(c, "Data rapor pendidikan berhasil diperbarui", data)
}

func (h *Handler) DeleteRaporPendidikan(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteRaporPendidikan(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus data rapor pendidikan", err)
	}
	return common.Success(c, "Data rapor pendidikan berhasil dihapus", nil)
}

func (h *Handler) SyncRaporPendidikan(c *fiber.Ctx) error {
	var req SyncRaporPendidikanRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.SyncRaporPendidikan(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal sinkronisasi data rapor pendidikan", err)
	}
	return common.Success(c, "Sinkronisasi data rapor pendidikan berhasil", data)
}

// Survey Handlers
func (h *Handler) CreateSurvey(c *fiber.Ctx) error {
	var req CreateSurveyRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateSurvey(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat survei", err)
	}
	return common.Created(c, "Survei berhasil dibuat", data)
}

func (h *Handler) GetSurveyByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetSurveyByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Survei tidak ditemukan", err)
	}
	return common.Success(c, "Detail survei berhasil diambil", data)
}

func (h *Handler) GetSurveysBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	pagination := common.GetPagination(c)
	data, total, err := h.svc.GetSurveysBySchool(c.UserContext(), schoolID, pagination)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data survei", err)
	}
	return common.Paginated(c, "Data survei berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

func (h *Handler) UpdateSurvey(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateSurveyRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateSurvey(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui survei", err)
	}
	return common.Success(c, "Survei berhasil diperbarui", data)
}

func (h *Handler) DeleteSurvey(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteSurvey(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus survei", err)
	}
	return common.Success(c, "Survei berhasil dihapus", nil)
}

func (h *Handler) GetSurveyTemplates(c *fiber.Ctx) error {
	category := c.Query("category")
	data, err := h.svc.GetSurveyTemplates(c.UserContext(), category)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil template survei", err)
	}
	return common.Success(c, "Template survei berhasil diambil", data)
}

func (h *Handler) GetActiveSurveys(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetActiveSurveys(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil survei aktif", err)
	}
	return common.Success(c, "Survei aktif berhasil diambil", data)
}

func (h *Handler) SubmitSurveyResponse(c *fiber.Ctx) error {
	var req CreateSurveyResponseRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.SubmitSurveyResponse(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengirim respon survei", err)
	}
	return common.Created(c, "Respon survei berhasil dikirim", data)
}

func (h *Handler) GetSurveyResponses(c *fiber.Ctx) error {
	surveyID := c.Params("surveyId")
	pagination := common.GetPagination(c)
	data, total, err := h.svc.GetSurveyResponses(c.UserContext(), surveyID, pagination)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil respon survei", err)
	}
	return common.Paginated(c, "Respon survei berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

func (h *Handler) GetSurveyAnalytics(c *fiber.Ctx) error {
	surveyID := c.Params("surveyId")
	data, err := h.svc.GetSurveyAnalytics(c.UserContext(), surveyID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil analitik survei", err)
	}
	return common.Success(c, "Analitik survei berhasil diambil", data)
}

// FGD Session Handlers
func (h *Handler) CreateFGDSession(c *fiber.Ctx) error {
	var req CreateFGDSessionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateFGDSession(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat sesi FGD", err)
	}
	return common.Created(c, "Sesi FGD berhasil dibuat", data)
}

func (h *Handler) GetFGDSessionByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetFGDSessionByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Sesi FGD tidak ditemukan", err)
	}
	return common.Success(c, "Detail sesi FGD berhasil diambil", data)
}

func (h *Handler) GetFGDSessionsBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	pagination := common.GetPagination(c)
	data, total, err := h.svc.GetFGDSessionsBySchool(c.UserContext(), schoolID, pagination)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil sesi FGD", err)
	}
	return common.Paginated(c, "Sesi FGD berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

func (h *Handler) UpdateFGDSession(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateFGDSessionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateFGDSession(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui sesi FGD", err)
	}
	return common.Success(c, "Sesi FGD berhasil diperbarui", data)
}

func (h *Handler) DeleteFGDSession(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteFGDSession(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus sesi FGD", err)
	}
	return common.Success(c, "Sesi FGD berhasil dihapus", nil)
}

func (h *Handler) GetUpcomingFGDSessions(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetUpcomingFGDSessions(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil sesi FGD yang akan datang", err)
	}
	return common.Success(c, "Sesi FGD yang akan datang berhasil diambil", data)
}

func (h *Handler) AddFGDParticipant(c *fiber.Ctx) error {
	var req AddFGDParticipantRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.AddFGDParticipant(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menambahkan peserta FGD", err)
	}
	return common.Created(c, "Peserta FGD berhasil ditambahkan", data)
}

func (h *Handler) GetFGDParticipants(c *fiber.Ctx) error {
	sessionID := c.Params("sessionId")
	data, err := h.svc.GetFGDParticipants(c.UserContext(), sessionID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil peserta FGD", err)
	}
	return common.Success(c, "Peserta FGD berhasil diambil", data)
}

func (h *Handler) UpdateFGDParticipant(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateFGDParticipantRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateFGDParticipant(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui peserta FGD", err)
	}
	return common.Success(c, "Peserta FGD berhasil diperbarui", data)
}

func (h *Handler) DeleteFGDParticipant(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteFGDParticipant(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus peserta FGD", err)
	}
	return common.Success(c, "Peserta FGD berhasil dihapus", nil)
}

// Student Needs Enhanced Handlers
func (h *Handler) CreateStudentNeedsEnhanced(c *fiber.Ctx) error {
	var req CreateStudentNeedsEnhancedRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateStudentNeedsEnhanced(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat data kebutuhan siswa", err)
	}
	return common.Created(c, "Data kebutuhan siswa berhasil dibuat", data)
}

func (h *Handler) GetStudentNeedsEnhancedByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetStudentNeedsEnhancedByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Data kebutuhan siswa tidak ditemukan", err)
	}
	return common.Success(c, "Detail data kebutuhan siswa berhasil diambil", data)
}

func (h *Handler) GetStudentNeedsEnhancedBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	pagination := common.GetPagination(c)
	data, total, err := h.svc.GetStudentNeedsEnhancedBySchool(c.UserContext(), schoolID, pagination)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data kebutuhan siswa", err)
	}
	return common.Paginated(c, "Data kebutuhan siswa berhasil diambil", data, pagination.Page, pagination.Limit, total)
}

func (h *Handler) GetStudentNeedsEnhancedByProfile(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	profilDimensi := c.Query("profil_dimensi")
	data, err := h.svc.GetStudentNeedsEnhancedByProfile(c.UserContext(), schoolID, profilDimensi)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data kebutuhan siswa", err)
	}
	return common.Success(c, "Data kebutuhan siswa berhasil diambil", data)
}

func (h *Handler) UpdateStudentNeedsEnhanced(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateStudentNeedsEnhancedRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateStudentNeedsEnhanced(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui data kebutuhan siswa", err)
	}
	return common.Success(c, "Data kebutuhan siswa berhasil diperbarui", data)
}

func (h *Handler) DeleteStudentNeedsEnhanced(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteStudentNeedsEnhanced(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus data kebutuhan siswa", err)
	}
	return common.Success(c, "Data kebutuhan siswa berhasil dihapus", nil)
}

// SWOT Handlers
func (h *Handler) CreateSWOTItem(c *fiber.Ctx) error {
	var req CreateSWOTItemRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateSWOTItem(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat item SWOT", err)
	}
	return common.Created(c, "Item SWOT berhasil dibuat", data)
}

func (h *Handler) GetSWOTItemByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetSWOTItemByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Item SWOT tidak ditemukan", err)
	}
	return common.Success(c, "Detail item SWOT berhasil diambil", data)
}

func (h *Handler) GetSWOTItemsBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	quadrant := c.Query("quadrant")
	data, err := h.svc.GetSWOTItemsBySchool(c.UserContext(), schoolID, quadrant)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil item SWOT", err)
	}
	return common.Success(c, "Item SWOT berhasil diambil", data)
}

func (h *Handler) UpdateSWOTItem(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateSWOTItemRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateSWOTItem(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui item SWOT", err)
	}
	return common.Success(c, "Item SWOT berhasil diperbarui", data)
}

func (h *Handler) DeleteSWOTItem(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteSWOTItem(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus item SWOT", err)
	}
	return common.Success(c, "Item SWOT berhasil dihapus", nil)
}

func (h *Handler) CreateSWOTAnalysisSession(c *fiber.Ctx) error {
	var req CreateSWOTAnalysisSessionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateSWOTAnalysisSession(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat sesi analisis SWOT", err)
	}
	return common.Created(c, "Sesi analisis SWOT berhasil dibuat", data)
}

func (h *Handler) GetSWOTAnalysisSessionByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetSWOTAnalysisSessionByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Sesi analisis SWOT tidak ditemukan", err)
	}
	return common.Success(c, "Detail sesi analisis SWOT berhasil diambil", data)
}

func (h *Handler) GetSWOTAnalysisSessionsBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetSWOTAnalysisSessionsBySchool(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil sesi analisis SWOT", err)
	}
	return common.Success(c, "Sesi analisis SWOT berhasil diambil", data)
}

func (h *Handler) UpdateSWOTAnalysisSession(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateSWOTAnalysisSessionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateSWOTAnalysisSession(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui sesi analisis SWOT", err)
	}
	return common.Success(c, "Sesi analisis SWOT berhasil diperbarui", data)
}

func (h *Handler) DeleteSWOTAnalysisSession(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteSWOTAnalysisSession(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus sesi analisis SWOT", err)
	}
	return common.Success(c, "Sesi analisis SWOT berhasil dihapus", nil)
}

func (h *Handler) AddSWOTItemToSession(c *fiber.Ctx) error {
	var req AddSWOTSessionItemRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.AddSWOTItemToSession(c.UserContext(), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menambahkan item ke sesi SWOT", err)
	}
	return common.Success(c, "Item SWOT berhasil ditambahkan ke sesi", nil)
}

func (h *Handler) GetSWOTSessionItems(c *fiber.Ctx) error {
	sessionID := c.Params("sessionId")
	data, err := h.svc.GetSWOTSessionItems(c.UserContext(), sessionID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil item sesi SWOT", err)
	}
	return common.Success(c, "Item sesi SWOT berhasil diambil", data)
}

// Root Cause Handlers
func (h *Handler) CreateRootCause(c *fiber.Ctx) error {
	var req CreateRootCauseRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateRootCause(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat analisis root cause", err)
	}
	return common.Created(c, "Analisis root cause berhasil dibuat", data)
}

func (h *Handler) GetRootCauseByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetRootCauseByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Analisis root cause tidak ditemukan", err)
	}
	return common.Success(c, "Detail analisis root cause berhasil diambil", data)
}

func (h *Handler) GetRootCausesBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	status := c.Query("status")
	data, err := h.svc.GetRootCausesBySchool(c.UserContext(), schoolID, status)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil analisis root cause", err)
	}
	return common.Success(c, "Analisis root cause berhasil diambil", data)
}

func (h *Handler) UpdateRootCause(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateRootCauseRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateRootCause(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui analisis root cause", err)
	}
	return common.Success(c, "Analisis root cause berhasil diperbarui", data)
}

func (h *Handler) DeleteRootCause(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteRootCause(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus analisis root cause", err)
	}
	return common.Success(c, "Analisis root cause berhasil dihapus", nil)
}

func (h *Handler) ValidateRootCause(c *fiber.Ctx) error {
	id := c.Params("id")
	var req ValidateRootCauseRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.ValidateRootCause(c.UserContext(), id, req); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memvalidasi analisis root cause", err)
	}
	return common.Success(c, "Analisis root cause berhasil divalidasi", nil)
}

func (h *Handler) GetRootCauseHistory(c *fiber.Ctx) error {
	rootCauseID := c.Params("rootCauseId")
	data, err := h.svc.GetRootCauseHistory(c.UserContext(), rootCauseID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil riwayat analisis root cause", err)
	}
	return common.Success(c, "Riwayat analisis root cause berhasil diambil", data)
}

// Fishbone Handlers
func (h *Handler) CreateFishboneDiagram(c *fiber.Ctx) error {
	var req CreateFishboneDiagramRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateFishboneDiagram(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat diagram fishbone", err)
	}
	return common.Created(c, "Diagram fishbone berhasil dibuat", data)
}

func (h *Handler) GetFishboneDiagramByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetFishboneDiagramByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Diagram fishbone tidak ditemukan", err)
	}
	return common.Success(c, "Detail diagram fishbone berhasil diambil", data)
}

func (h *Handler) GetFishboneDiagramsBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetFishboneDiagramsBySchool(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil diagram fishbone", err)
	}
	return common.Success(c, "Diagram fishbone berhasil diambil", data)
}

func (h *Handler) UpdateFishboneDiagram(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateFishboneDiagramRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateFishboneDiagram(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui diagram fishbone", err)
	}
	return common.Success(c, "Diagram fishbone berhasil diperbarui", data)
}

func (h *Handler) DeleteFishboneDiagram(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteFishboneDiagram(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus diagram fishbone", err)
	}
	return common.Success(c, "Diagram fishbone berhasil dihapus", nil)
}

func (h *Handler) CreateFishboneNode(c *fiber.Ctx) error {
	var req CreateFishboneNodeRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateFishboneNode(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat node fishbone", err)
	}
	return common.Created(c, "Node fishbone berhasil dibuat", data)
}

func (h *Handler) GetFishboneNodesByDiagram(c *fiber.Ctx) error {
	diagramID := c.Params("diagramId")
	data, err := h.svc.GetFishboneNodesByDiagram(c.UserContext(), diagramID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil node fishbone", err)
	}
	return common.Success(c, "Node fishbone berhasil diambil", data)
}

func (h *Handler) UpdateFishboneNode(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateFishboneNodeRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateFishboneNode(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui node fishbone", err)
	}
	return common.Success(c, "Node fishbone berhasil diperbarui", data)
}

func (h *Handler) DeleteFishboneNode(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteFishboneNode(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus node fishbone", err)
	}
	return common.Success(c, "Node fishbone berhasil dihapus", nil)
}

func (h *Handler) CreateFishboneConnection(c *fiber.Ctx) error {
	var req CreateFishboneConnectionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateFishboneConnection(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat koneksi fishbone", err)
	}
	return common.Created(c, "Koneksi fishbone berhasil dibuat", data)
}

func (h *Handler) GetFishboneConnections(c *fiber.Ctx) error {
	diagramID := c.Params("diagramId")
	data, err := h.svc.GetFishboneConnections(c.UserContext(), diagramID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil koneksi fishbone", err)
	}
	return common.Success(c, "Koneksi fishbone berhasil diambil", data)
}

func (h *Handler) DeleteFishboneConnection(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteFishboneConnection(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus koneksi fishbone", err)
	}
	return common.Success(c, "Koneksi fishbone berhasil dihapus", nil)
}

// KSP Integration Handlers
func (h *Handler) CreateKSPAnalysisIntegration(c *fiber.Ctx) error {
	var req CreateKSPAnalysisIntegrationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateKSPAnalysisIntegration(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat integrasi analisis KSP", err)
	}
	return common.Created(c, "Integrasi analisis KSP berhasil dibuat", data)
}

func (h *Handler) GetKSPAnalysisIntegrationByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetKSPAnalysisIntegrationByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Integrasi analisis KSP tidak ditemukan", err)
	}
	return common.Success(c, "Detail integrasi analisis KSP berhasil diambil", data)
}

func (h *Handler) GetKSPAnalysisIntegrationsByDocument(c *fiber.Ctx) error {
	documentID := c.Params("documentId")
	data, err := h.svc.GetKSPAnalysisIntegrationsByDocument(c.UserContext(), documentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil integrasi analisis KSP", err)
	}
	return common.Success(c, "Integrasi analisis KSP berhasil diambil", data)
}

func (h *Handler) UpdateKSPAnalysisIntegration(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateKSPAnalysisIntegrationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateKSPAnalysisIntegration(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui integrasi analisis KSP", err)
	}
	return common.Success(c, "Integrasi analisis KSP berhasil diperbarui", data)
}

func (h *Handler) DeleteKSPAnalysisIntegration(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteKSPAnalysisIntegration(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus integrasi analisis KSP", err)
	}
	return common.Success(c, "Integrasi analisis KSP berhasil dihapus", nil)
}

func (h *Handler) ApproveKSPAnalysisIntegration(c *fiber.Ctx) error {
	id := c.Params("id")
	var req ApproveKSPAnalysisIntegrationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.ApproveKSPAnalysisIntegration(c.UserContext(), id, req); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menyetujui integrasi analisis KSP", err)
	}
	return common.Success(c, "Integrasi analisis KSP berhasil disetujui", nil)
}

func (h *Handler) CreateKSPAnalysisRecommendation(c *fiber.Ctx) error {
	var req CreateKSPAnalysisRecommendationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateKSPAnalysisRecommendation(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat rekomendasi analisis KSP", err)
	}
	return common.Created(c, "Rekomendasi analisis KSP berhasil dibuat", data)
}

func (h *Handler) GetKSPAnalysisRecommendations(c *fiber.Ctx) error {
	integrationID := c.Params("integrationId")
	data, err := h.svc.GetKSPAnalysisRecommendations(c.UserContext(), integrationID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil rekomendasi analisis KSP", err)
	}
	return common.Success(c, "Rekomendasi analisis KSP berhasil diambil", data)
}

func (h *Handler) UpdateKSPAnalysisRecommendation(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateKSPAnalysisRecommendationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateKSPAnalysisRecommendation(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui rekomendasi analisis KSP", err)
	}
	return common.Success(c, "Rekomendasi analisis KSP berhasil diperbarui", data)
}

func (h *Handler) DeleteKSPAnalysisRecommendation(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteKSPAnalysisRecommendation(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus rekomendasi analisis KSP", err)
	}
	return common.Success(c, "Rekomendasi analisis KSP berhasil dihapus", nil)
}

func (h *Handler) CreateKSPAnalysisTemplate(c *fiber.Ctx) error {
	var req CreateKSPAnalysisTemplateRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CreateKSPAnalysisTemplate(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat template analisis KSP", err)
	}
	return common.Created(c, "Template analisis KSP berhasil dibuat", data)
}

func (h *Handler) GetKSPAnalysisTemplateByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetKSPAnalysisTemplateByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Template analisis KSP tidak ditemukan", err)
	}
	return common.Success(c, "Detail template analisis KSP berhasil diambil", data)
}

func (h *Handler) GetPublicKSPAnalysisTemplates(c *fiber.Ctx) error {
	category := c.Query("category")
	data, err := h.svc.GetPublicKSPAnalysisTemplates(c.UserContext(), category)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil template analisis KSP publik", err)
	}
	return common.Success(c, "Template analisis KSP publik berhasil diambil", data)
}

func (h *Handler) GetKSPAnalysisTemplatesBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetKSPAnalysisTemplatesBySchool(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil template analisis KSP sekolah", err)
	}
	return common.Success(c, "Template analisis KSP sekolah berhasil diambil", data)
}

func (h *Handler) UpdateKSPAnalysisTemplate(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateKSPAnalysisTemplateRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateKSPAnalysisTemplate(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui template analisis KSP", err)
	}
	return common.Success(c, "Template analisis KSP berhasil diperbarui", data)
}

func (h *Handler) DeleteKSPAnalysisTemplate(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteKSPAnalysisTemplate(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus template analisis KSP", err)
	}
	return common.Success(c, "Template analisis KSP berhasil dihapus", nil)
}

func (h *Handler) IncrementTemplateUsage(c *fiber.Ctx) error {
	templateID := c.Params("templateId")
	if err := h.svc.IncrementTemplateUsage(c.UserContext(), templateID); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menambah penggunaan template", err)
	}
	return common.Success(c, "Penggunaan template berhasil ditambah", nil)
}

// FASE 4: Integration Handlers

// Local Context Integration (FR 2.1)
func (h *Handler) GetLocalContextForSWOT(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetLocalContextForSWOT(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data konteks lokal untuk SWOT", err)
	}
	return common.Success(c, "Data konteks lokal untuk SWOT berhasil diambil", data)
}

func (h *Handler) AnalyzeLearningPotential(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.AnalyzeLearningPotential(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menganalisis potensi pembelajaran", err)
	}
	return common.Success(c, "Analisis potensi pembelajaran berhasil dilakukan", data)
}

func (h *Handler) GetEnhancedLocalCategories(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetEnhancedLocalCategories(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil kategori lokal yang di-enhance", err)
	}
	return common.Success(c, "Kategori lokal yang di-enhance berhasil diambil", data)
}

// Student Context Analytics (FR 2.2)
func (h *Handler) GetSurveyAnalyticsAggregated(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	surveyID := c.Params("surveyId")
	data, err := h.svc.GetSurveyAnalyticsAggregated(c.UserContext(), schoolID, surveyID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil analitik survei teragregasi", err)
	}
	return common.Success(c, "Analitik survei teragregasi berhasil diambil", data)
}

func (h *Handler) GetStudentProfileAnalysis(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	profileDimension := c.Query("profile_dimension")
	if profileDimension == "" {
		profileDimension = "BERIMAN" // default
	}
	data, err := h.svc.GetStudentProfileAnalysis(c.UserContext(), schoolID, profileDimension)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil analisis profil siswa", err)
	}
	return common.Success(c, "Analisis profil siswa berhasil diambil", data)
}

func (h *Handler) GetStatisticalAnalysis(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	analysisType := c.Query("analysis_type")
	if analysisType == "" {
		analysisType = "correlation" // default
	}
	data, err := h.svc.GetStatisticalAnalysis(c.UserContext(), schoolID, analysisType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil analisis statistik", err)
	}
	return common.Success(c, "Analisis statistik berhasil diambil", data)
}

func (h *Handler) GenerateActionPlanRecommendations(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GenerateActionPlanRecommendations(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat rekomendasi rencana aksi", err)
	}
	return common.Success(c, "Rekomendasi rencana aksi berhasil dibuat", data)
}

// School Data Integration (FR 2.3)
func (h *Handler) GetSchoolDataForSWOT(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetSchoolDataForSWOT(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil data sekolah untuk SWOT", err)
	}
	return common.Success(c, "Data sekolah untuk SWOT berhasil diambil", data)
}

func (h *Handler) GetDigitalReadinessAssessment(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetDigitalReadinessAssessment(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil penilaian kesiapan digital", err)
	}
	return common.Success(c, "Penilaian kesiapan digital berhasil diambil", data)
}

func (h *Handler) GetSarprasPrioritization(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetSarprasPrioritization(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil prioritas sarpras", err)
	}
	return common.Success(c, "Prioritas sarpras berhasil diambil", data)
}

// FASE 5: Analysis Tool Enhancements

// SWOT Builder Enhancements (FR 3.1)

func (h *Handler) GetSWOTAnalyticsAggregation(c *fiber.Ctx) error {
	sessionID := c.Params("sessionId")
	data, err := h.svc.GetSWOTAnalyticsAggregation(c.UserContext(), sessionID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil analitik SWOT teragregasi", err)
	}
	return common.Success(c, "Analitik SWOT teragregasi berhasil diambil", data)
}

func (h *Handler) MapDataToSWOTItem(c *fiber.Ctx) error {
	var req SWOTDataMappingRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.MapDataToSWOTItem(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memetakan data ke item SWOT", err)
	}
	return common.Success(c, "Data berhasil dipetakan ke item SWOT", data)
}

func (h *Handler) GetAvailableDataSourceTypes(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetAvailableDataSourceTypes(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil tipe sumber data yang tersedia", err)
	}
	return common.Success(c, "Tipe sumber data yang tersedia berhasil diambil", data)
}

func (h *Handler) ExportSWOTAnalysis(c *fiber.Ctx) error {
	sessionID := c.Params("sessionId")
	format := c.Query("format", "json")

	data, err := h.svc.ExportSWOTAnalysis(c.UserContext(), sessionID, format)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengekspor analisis SWOT", err)
	}

	contentType := "application/json"
	filename := "swot_analysis.json"
	if format == "csv" {
		contentType = "text/csv"
		filename = "swot_analysis.csv"
	}

	c.Set("Content-Type", contentType)
	c.Set("Content-Disposition", fmt.Sprintf("attachment; filename=%s", filename))
	return c.Send(data)
}

// Root Cause Analyzer Enhancements (FR 3.2)

func (h *Handler) Perform5WhysAnalysis(c *fiber.Ctx) error {
	var req FiveWhysRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.Perform5WhysAnalysis(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal melakukan analisis 5-Whys", err)
	}
	return common.Success(c, "Analisis 5-Whys berhasil dilakukan", data)
}

func (h *Handler) LinkRaporMetricToRootCause(c *fiber.Ctx) error {
	var req RaporMetricLinkRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.LinkRaporMetricToRootCause(c.UserContext(), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghubungkan metrik Rapor ke akar masalah", err)
	}
	return common.Success(c, "Metrik Rapor berhasil dihubungkan ke akar masalah", nil)
}

func (h *Handler) GetRootCauseSuggestions(c *fiber.Ctx) error {
	rootCauseID := c.Params("rootCauseId")
	data, err := h.svc.GetRootCauseSuggestions(c.UserContext(), rootCauseID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil saran akar masalah", err)
	}
	return common.Success(c, "Saran akar masalah berhasil diambil", data)
}

func (h *Handler) ExportRootCauseAnalysis(c *fiber.Ctx) error {
	rootCauseID := c.Params("rootCauseId")
	format := c.Query("format", "json")

	data, err := h.svc.ExportRootCauseAnalysis(c.UserContext(), rootCauseID, format)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengekspor analisis akar masalah", err)
	}

	contentType := "application/json"
	filename := "root_cause_analysis.json"
	if format == "csv" {
		contentType = "text/csv"
		filename = "root_cause_analysis.csv"
	}

	c.Set("Content-Type", contentType)
	c.Set("Content-Disposition", fmt.Sprintf("attachment; filename=%s", filename))
	return c.Send(data)
}

// Fishbone Diagram Enhancements (FR 3.3)

func (h *Handler) GetFishboneAnalytics(c *fiber.Ctx) error {
	diagramID := c.Params("diagramId")
	data, err := h.svc.GetFishboneAnalytics(c.UserContext(), diagramID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil analitik diagram fishbone", err)
	}
	return common.Success(c, "Analitik diagram fishbone berhasil diambil", data)
}

func (h *Handler) ValidateFishboneStructure(c *fiber.Ctx) error {
	diagramID := c.Params("diagramId")
	data, err := h.svc.ValidateFishboneStructure(c.UserContext(), diagramID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memvalidasi struktur diagram fishbone", err)
	}
	return common.Success(c, "Struktur diagram fishbone berhasil divalidasi", data)
}

func (h *Handler) GetFishboneCategories(c *fiber.Ctx) error {
	data, err := h.svc.GetFishboneCategories(c.UserContext())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil kategori fishbone", err)
	}
	return common.Success(c, "Kategori fishbone berhasil diambil", data)
}

func (h *Handler) ExportFishboneDiagram(c *fiber.Ctx) error {
	diagramID := c.Params("diagramId")
	format := c.Query("format", "json")

	data, err := h.svc.ExportFishboneDiagram(c.UserContext(), diagramID, format)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengekspor diagram fishbone", err)
	}

	contentType := "application/json"
	filename := "fishbone_diagram.json"
	if format == "csv" {
		contentType = "text/csv"
		filename = "fishbone_diagram.csv"
	}

	c.Set("Content-Type", contentType)
	c.Set("Content-Disposition", fmt.Sprintf("attachment; filename=%s", filename))
	return c.Send(data)
}

// Fishbone Template Handlers (T-5.3.14)

func (h *Handler) CreateFishboneTemplate(c *fiber.Ctx) error {
	var req CreateFishboneTemplateRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	// Get user ID from context (assuming middleware sets it)
	userID := c.Locals("user_id").(string)

	data, err := h.svc.CreateFishboneTemplate(c.UserContext(), req, userID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat template fishbone", err)
	}
	return common.Created(c, "Template fishbone berhasil dibuat", data)
}

func (h *Handler) GetFishboneTemplateByID(c *fiber.Ctx) error {
	id := c.Params("id")
	data, err := h.svc.GetFishboneTemplateByID(c.UserContext(), id)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Template fishbone tidak ditemukan", err)
	}
	return common.Success(c, "Detail template fishbone berhasil diambil", data)
}

func (h *Handler) GetPublicFishboneTemplates(c *fiber.Ctx) error {
	category := c.Query("category")
	data, err := h.svc.GetPublicFishboneTemplates(c.UserContext(), category)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil template fishbone publik", err)
	}
	return common.Success(c, "Template fishbone publik berhasil diambil", data)
}

func (h *Handler) GetFishboneTemplatesBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	data, err := h.svc.GetFishboneTemplatesBySchool(c.UserContext(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil template fishbone sekolah", err)
	}
	return common.Success(c, "Template fishbone sekolah berhasil diambil", data)
}

func (h *Handler) UpdateFishboneTemplate(c *fiber.Ctx) error {
	id := c.Params("id")
	var req UpdateFishboneTemplateRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateFishboneTemplate(c.UserContext(), id, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui template fishbone", err)
	}
	return common.Success(c, "Template fishbone berhasil diperbarui", data)
}

func (h *Handler) DeleteFishboneTemplate(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteFishboneTemplate(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus template fishbone", err)
	}
	return common.Success(c, "Template fishbone berhasil dihapus", nil)
}

func (h *Handler) IncrementFishboneTemplateUsage(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.IncrementTemplateUsage(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal increment usage template", err)
	}
	return common.Success(c, "Template usage berhasil diincrement", nil)
}

func (h *Handler) ApplyFishboneTemplate(c *fiber.Ctx) error {
	templateID := c.Params("templateId")
	diagramID := c.Params("diagramId")

	if err := h.svc.ApplyTemplateToDiagram(c.UserContext(), templateID, diagramID); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menerapkan template ke diagram", err)
	}
	return common.Success(c, "Template berhasil diterapkan ke diagram", nil)
}

// FASE 6: KSP Enhanced Generation Handlers

// Document Compilation Handlers (FR 4.1.1)

func (h *Handler) CompileDocumentWithAnalysis(c *fiber.Ctx) error {
	var req DocumentCompilationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.CompileDocumentWithAnalysis(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengompilasi dokumen", err)
	}
	return common.Success(c, "Dokumen berhasil dikompilasi", data)
}

func (h *Handler) GenerateAnalysisSnapshot(c *fiber.Ctx) error {
	integrationID := c.Params("integrationId")
	data, err := h.svc.GenerateAnalysisSnapshot(c.UserContext(), integrationID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal generate analysis snapshot", err)
	}
	return common.Success(c, "Analysis snapshot berhasil dibuat", data)
}
// Chart Generation Handlers (FR 4.1.3)

func (h *Handler) GenerateChartsFromAnalysis(c *fiber.Ctx) error {
	var req ChartGenerationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.GenerateChartsFromAnalysis(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal generate charts", err)
	}
	return common.Success(c, "Charts berhasil dibuat", data)
}

func (h *Handler) GenerateSWOTChart(c *fiber.Ctx) error {
	var data SWOTChartData
	if err := c.BodyParser(&data); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(data); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	chartType := c.Query("type", "bar")

	response, err := h.svc.GenerateSWOTChart(c.UserContext(), data, chartType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal generate SWOT chart", err)
	}
	return common.Success(c, "SWOT chart berhasil dibuat", response)
}

func (h *Handler) GenerateRootCauseChart(c *fiber.Ctx) error {
	var data RootCauseChartData
	if err := c.BodyParser(&data); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(data); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	chartType := c.Query("type", "pie")

	response, err := h.svc.GenerateRootCauseChart(c.UserContext(), data, chartType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal generate root cause chart", err)
	}
	return common.Success(c, "Root cause chart berhasil dibuat", response)
}

func (h *Handler) GenerateFishboneChart(c *fiber.Ctx) error {
	var data FishboneChartData
	if err := c.BodyParser(&data); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(data); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	chartType := c.Query("type", "bar")

	response, err := h.svc.GenerateFishboneChart(c.UserContext(), data, chartType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal generate fishbone chart", err)
	}
	return common.Success(c, "Fishbone chart berhasil dibuat", response)
}

func (h *Handler) GenerateStudentNeedsChart(c *fiber.Ctx) error {
	var data StudentNeedsChartData
	if err := c.BodyParser(&data); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(data); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	chartType := c.Query("type", "radar")

	response, err := h.svc.GenerateStudentNeedsChart(c.UserContext(), data, chartType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal generate student needs chart", err)
	}
	return common.Success(c, "Student needs chart berhasil dibuat", response)
}

// AI Platform Integration Handlers (FR 4.1.4)

func (h *Handler) GenerateContentWithAI(c *fiber.Ctx) error {
	var req AIContentGenerationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	response, err := h.svc.GenerateContentWithAI(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal generate content dengan AI", err)
	}
	return common.Success(c, "Content berhasil di-generate dengan AI", response)
}

func (h *Handler) GenerateRecommendationsWithAI(c *fiber.Ctx) error {
	var req AIRecommendationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	response, err := h.svc.GenerateRecommendationsWithAI(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal generate recommendations dengan AI", err)
	}
	return common.Success(c, "Recommendations berhasil di-generate dengan AI", response)
}

func (h *Handler) GetAIIntegrationConfig(c *fiber.Ctx) error {
	config, err := h.svc.GetAIIntegrationConfig(c.UserContext())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil AI integration config", err)
	}
	return common.Success(c, "AI integration config berhasil diambil", config)
}

func (h *Handler) UpdateAIIntegrationConfig(c *fiber.Ctx) error {
	var config AIIntegrationConfig
	if err := c.BodyParser(&config); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(config); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	err := h.svc.UpdateAIIntegrationConfig(c.UserContext(), config)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal update AI integration config", err)
	}
	return common.Success(c, "AI integration config berhasil di-update", nil)
}

// Version History Handlers (FR 4.1.5)

func (h *Handler) CreateAnalysisVersionHistory(c *fiber.Ctx) error {
	var req AnalysisVersionHistoryRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	// Get user ID from context (assuming it's set by middleware)
	changedBy := c.Locals("user_id").(string)

	data, err := h.svc.CreateAnalysisVersionHistory(c.UserContext(), req, changedBy)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal create version history", err)
	}
	return common.Created(c, "Version history berhasil dibuat", data)
}

func (h *Handler) GetAnalysisVersionHistory(c *fiber.Ctx) error {
	analysisID := c.Params("analysisId")
	analysisType := c.Query("type")

	data, err := h.svc.GetAnalysisVersionHistory(c.UserContext(), analysisID, analysisType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil version history", err)
	}
	return common.Success(c, "Version history berhasil diambil", data)
}

func (h *Handler) GetAnalysisVersionByID(c *fiber.Ctx) error {
	versionID := c.Params("versionId")

	data, err := h.svc.GetAnalysisVersionByID(c.UserContext(), versionID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Version tidak ditemukan", err)
	}
	return common.Success(c, "Version detail berhasil diambil", data)
}

func (h *Handler) CompareAnalysisVersions(c *fiber.Ctx) error {
	analysisID := c.Params("analysisId")
	version1 := c.QueryInt("version1")
	version2 := c.QueryInt("version2")

	if version1 == 0 || version2 == 0 {
		return common.Error(c, fiber.StatusBadRequest, "Version1 and Version2 are required", nil)
	}

	data, err := h.svc.CompareAnalysisVersions(c.UserContext(), analysisID, version1, version2)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal compare versions", err)
	}
	return common.Success(c, "Version comparison berhasil", data)
}

func (h *Handler) RestoreAnalysisVersion(c *fiber.Ctx) error {
	var req VersionRestoreRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	// Get user ID from context
	changedBy := c.Locals("user_id").(string)

	err := h.svc.RestoreAnalysisVersion(c.UserContext(), req, changedBy)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal restore version", err)
	}
	return common.Success(c, "Version berhasil di-restore", nil)
}

// Extended Review and Approval Workflow Handlers (FR 4.1.13)

func (h *Handler) CreateApprovalWorkflow(c *fiber.Ctx) error {
	var req ApprovalWorkflowRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	createdBy := c.Locals("user_id").(string)

	data, err := h.svc.CreateApprovalWorkflow(c.UserContext(), req, createdBy)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal create approval workflow", err)
	}
	return common.Created(c, "Approval workflow berhasil dibuat", data)
}

func (h *Handler) GetApprovalWorkflowByID(c *fiber.Ctx) error {
	workflowID := c.Params("workflowId")

	data, err := h.svc.GetApprovalWorkflowByID(c.UserContext(), workflowID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Approval workflow tidak ditemukan", err)
	}
	return common.Success(c, "Approval workflow berhasil diambil", data)
}

func (h *Handler) GetApprovalWorkflowsBySchool(c *fiber.Ctx) error {
	schoolID := c.Params("schoolId")
	workflowType := c.Query("type")

	data, err := h.svc.GetApprovalWorkflowsBySchool(c.UserContext(), schoolID, workflowType)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil approval workflows", err)
	}
	return common.Success(c, "Approval workflows berhasil diambil", data)
}

func (h *Handler) UpdateApprovalWorkflow(c *fiber.Ctx) error {
	workflowID := c.Params("workflowId")
	var req ApprovalWorkflowRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.UpdateApprovalWorkflow(c.UserContext(), workflowID, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal update approval workflow", err)
	}
	return common.Success(c, "Approval workflow berhasil di-update", data)
}

func (h *Handler) DeleteApprovalWorkflow(c *fiber.Ctx) error {
	workflowID := c.Params("workflowId")

	err := h.svc.DeleteApprovalWorkflow(c.UserContext(), workflowID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal delete approval workflow", err)
	}
	return common.Success(c, "Approval workflow berhasil di-delete", nil)
}

func (h *Handler) SubmitForApproval(c *fiber.Ctx) error {
	documentID := c.Params("documentId")
	workflowID := c.Query("workflowId")

	submittedBy := c.Locals("user_id").(string)

	data, err := h.svc.SubmitForApproval(c.UserContext(), documentID, workflowID, submittedBy)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal submit untuk approval", err)
	}
	return common.Created(c, "Document berhasil disubmit untuk approval", data)
}

func (h *Handler) ProcessApproval(c *fiber.Ctx) error {
	var req ApprovalRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	approverID := c.Locals("user_id").(string)

	data, err := h.svc.ProcessApproval(c.UserContext(), req, approverID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal process approval", err)
	}
	return common.Success(c, "Approval berhasil diproses", data)
}

func (h *Handler) GetDocumentApprovalStatus(c *fiber.Ctx) error {
	documentID := c.Params("documentId")

	data, err := h.svc.GetDocumentApprovalStatus(c.UserContext(), documentID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil approval status", err)
	}
	return common.Success(c, "Approval status berhasil diambil", data)
}

func (h *Handler) AssignWorkflowStep(c *fiber.Ctx) error {
	var req struct {
		WorkflowID string `json:"workflow_id" binding:"required"`
		StepID     string `json:"step_id" binding:"required"`
		DocumentID string `json:"document_id" binding:"required"`
		AssignedTo string `json:"assigned_to" binding:"required"`
	}
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	assignedBy := c.Locals("user_id").(string)

	data, err := h.svc.AssignWorkflowStep(c.UserContext(), req.WorkflowID, req.StepID, req.DocumentID, req.AssignedTo, assignedBy)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal assign workflow step", err)
	}
	return common.Created(c, "Workflow step berhasil di-assign", data)
}

func (h *Handler) GetPendingApprovals(c *fiber.Ctx) error {
	approverID := c.Locals("user_id").(string)

	data, err := h.svc.GetPendingApprovals(c.UserContext(), approverID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil pending approvals", err)
	}
	return common.Success(c, "Pending approvals berhasil diambil", data)
}

func (h *Handler) SendApprovalNotification(c *fiber.Ctx) error {
	var notification ApprovalNotification
	if err := c.BodyParser(&notification); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Request body tidak valid", err)
	}
	if err := common.Validate.Struct(notification); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	err := h.svc.SendApprovalNotification(c.UserContext(), notification)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal send approval notification", err)
	}
	return common.Success(c, "Approval notification berhasil dikirim", nil)
}

func (h *Handler) GetApprovalNotifications(c *fiber.Ctx) error {
	recipientID := c.Locals("user_id").(string)

	data, err := h.svc.GetApprovalNotifications(c.UserContext(), recipientID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil approval notifications", err)
	}
	return common.Success(c, "Approval notifications berhasil diambil", data)
}
