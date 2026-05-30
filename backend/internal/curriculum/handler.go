package curriculum

import (
	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"

	"sim-sekolah/internal/common"
)

type CurriculumHandler struct {
	svc CurriculumService
}

func NewCurriculumHandler(svc CurriculumService) *CurriculumHandler {
	return &CurriculumHandler{svc: svc}
}

// InitializeDocument godoc
// @Summary      Create a new curriculum document
// @Description  Creates a new curriculum document for the given academic year and school.
// @Tags         Curriculum
// @Accept       json
// @Produce      json
// @Param        request body InitializeCurriculumRequest true "Initialize Request"
// @Success      201  {object}  common.Response
// @Failure      400  {object}  common.Response
// @Failure      409  {object}  common.Response
// @Router       /curriculum-documents [post]
// @Security     BearerAuth
func (h *CurriculumHandler) InitializeDocument(c *fiber.Ctx) error {
	var req InitializeCurriculumRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	doc, err := h.svc.InitializeDocument(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat dokumen kurikulum", err)
	}

	return common.Created(c, "Dokumen kurikulum berhasil diinisialisasi", doc)
}

// GetDocuments godoc
// @Summary      Get all curriculum documents
// @Description  Get a list of all curriculum documents
// @Tags         Curriculum
// @Accept       json
// @Produce      json
// @Success      200  {object}  common.Response
// @Failure      500  {object}  common.Response
// @Router       /curriculum-documents [get]
// @Security     BearerAuth
func (h *CurriculumHandler) GetDocuments(c *fiber.Ctx) error {
	docs, err := h.svc.GetDocuments(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil dokumen kurikulum", err)
	}
	return common.Success(c, "Dokumen kurikulum berhasil diambil", docs)
}

// GetDocumentByID godoc
// @Summary      Get curriculum document by ID
// @Description  Get a curriculum document with all its chapters
// @Tags         Curriculum
// @Accept       json
// @Produce      json
// @Param        id path string true "Curriculum Document ID"
// @Success      200  {object}  common.Response
// @Failure      400  {object}  common.Response
// @Failure      404  {object}  common.Response
// @Router       /curriculum-documents/{id} [get]
// @Security     BearerAuth
func (h *CurriculumHandler) GetDocumentByID(c *fiber.Ctx) error {
	docID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "ID dokumen tidak valid", "invalid document id")
	}

	doc, err := h.svc.GetDocumentByID(c.Context(), docID)
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Dokumen tidak ditemukan", "document not found")
	}

	return common.Success(c, "Dokumen kurikulum berhasil diambil", doc)
}

// CheckReadiness godoc
// @Summary      Check school data readiness
// @Description  Check if the school data is 90% ready for curriculum formulation
// @Tags         Curriculum
// @Accept       json
// @Produce      json
// @Param        school_id query string true "School ID"
// @Success      200  {object}  common.Response
// @Failure      400  {object}  common.Response
// @Router       /curriculum-documents/readiness [get]
// @Security     BearerAuth
func (h *CurriculumHandler) CheckReadiness(c *fiber.Ctx) error {
	schoolIDStr := c.Query("school_id")
	schoolID, err := uuid.Parse(schoolIDStr)
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "ID sekolah tidak valid", "invalid school id")
	}

	res, err := h.svc.CheckReadiness(c.Context(), schoolID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memeriksa kesiapan data", err)
	}

	return common.Success(c, "Kesiapan data berhasil diperiksa", res)
}

// TriggerChapterFormulation godoc
// @Summary      Trigger Chapter Formulation
// @Description  Queues a background job to formulate a curriculum chapter using AI
// @Tags         Curriculum
// @Accept       json
// @Produce      json
// @Param        request body TriggerChapterRequest true "Trigger Request"
// @Success      200  {object}  common.Response
// @Failure      400  {object}  common.Response
// @Router       /curriculum-documents/chapters/trigger [post]
// @Security     BearerAuth
func (h *CurriculumHandler) TriggerChapterFormulation(c *fiber.Ctx) error {
	var req TriggerChapterRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	userIDStr, _ := c.Locals("user_id").(string)
	userID, err := uuid.Parse(userIDStr)
	if err != nil {
		return common.Error(c, fiber.StatusUnauthorized, "Tidak terautentikasi", "Token pengguna tidak valid")
	}

	res, err := h.svc.TriggerChapterFormulation(c.Context(), userID, req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengantrean perumusan bab", err)
	}

	return common.Success(c, "Perumusan bab berhasil diantrean", res)
}

// GetChapter godoc
// @Summary      Get Chapter Content
// @Description  Retrieve HTML content for a specific chapter
// @Tags         Curriculum
// @Accept       json
// @Produce      json
// @Param        id path string true "Curriculum Document ID"
// @Param        chapter_number path int true "Chapter Number"
// @Success      200  {object}  common.Response
// @Failure      404  {object}  common.Response
// @Router       /curriculum-documents/{id}/chapters/{chapter_number} [get]
// @Security     BearerAuth
func (h *CurriculumHandler) GetChapter(c *fiber.Ctx) error {
	docID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "ID dokumen tidak valid", "invalid document id")
	}

	chapterNum, err := c.ParamsInt("chapter_number")
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Nomor bab tidak valid", "invalid chapter number")
	}

	chapter, err := h.svc.GetChapter(c.Context(), docID, chapterNum)
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Bab tidak ditemukan", "chapter not found")
	}

	return common.Success(c, "Bab berhasil diambil", chapter)
}

// UpdateChapterContent godoc
// @Summary      Update Chapter Content
// @Description  Save manual corrections to a chapter
// @Tags         Curriculum
// @Accept       json
// @Produce      json
// @Param        chapter_id path string true "Chapter ID"
// @Param        request body UpdateChapterRequest true "Update Request"
// @Success      200  {object}  common.Response
// @Failure      400  {object}  common.Response
// @Router       /curriculum-documents/chapters/{chapter_id} [put]
// @Security     BearerAuth
func (h *CurriculumHandler) UpdateChapterContent(c *fiber.Ctx) error {
	chapterID, err := uuid.Parse(c.Params("chapter_id"))
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "ID bab tidak valid", "invalid chapter id")
	}

	var req UpdateChapterRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.UpdateChapterContent(c.Context(), chapterID, req); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memperbarui bab", err)
	}

	return common.Success(c, "Bab berhasil diperbarui", nil)
}

// FinalizeDocument godoc
// @Summary      Finalize Curriculum Document
// @Description  Locks the document and marks it as FINAL
// @Tags         Curriculum
// @Accept       json
// @Produce      json
// @Param        id path string true "Curriculum Document ID"
// @Success      200  {object}  common.Response
// @Failure      400  {object}  common.Response
// @Router       /curriculum-documents/{id}/finalize [post]
// @Security     BearerAuth
func (h *CurriculumHandler) FinalizeDocument(c *fiber.Ctx) error {
	docID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "ID dokumen tidak valid", "invalid document id")
	}

	if err := h.svc.FinalizeDocument(c.Context(), docID); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Gagal memfinalisasi dokumen", err)
	}

	return common.Success(c, "Dokumen berhasil difinalisasi", nil)
}

// ExportDocument godoc
// @Summary      Export Document to PDF
// @Description  Mock export of the FINAL curriculum document
// @Tags         Curriculum
// @Accept       json
// @Produce      json
// @Param        id path string true "Curriculum Document ID"
// @Success      200  {object}  common.Response
// @Failure      403  {object}  common.Response
// @Router       /curriculum-documents/{id}/export [get]
// @Security     BearerAuth
func (h *CurriculumHandler) ExportDocument(c *fiber.Ctx) error {
	docID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "ID dokumen tidak valid", "invalid document id")
	}

	// Mock PDF Export Logic
	_ = docID
	return common.Success(c, "PDF berhasil diekspor", map[string]string{
		"download_url": "https://storage.sim-sekolah.com/exports/curriculum.pdf",
	})
}

// UpdateCurriculumType godoc
// @Summary      Update Curriculum Type
// @Description  Updates the curriculum type of a document (INTRAKURIKULER, KOKURIKULER, EKSTRAKURIKULER)
// @Tags         Curriculum
// @Accept       json
// @Produce      json
// @Param        id path string true "Curriculum Document ID"
// @Param        request body UpdateCurriculumTypeRequest true "Update Request"
// @Success      200  {object}  common.Response
// @Failure      400  {object}  common.Response
// @Router       /curriculum-documents/{id}/type [put]
// @Security     BearerAuth
func (h *CurriculumHandler) UpdateCurriculumType(c *fiber.Ctx) error {
	docID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "ID dokumen tidak valid", "invalid document id")
	}

	var req UpdateCurriculumTypeRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.UpdateCurriculumType(c.Context(), docID, req); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate tipe kurikulum", err)
	}

	return common.Success(c, "Tipe kurikulum berhasil diupdate", nil)
}

// Co-curricular Activities Handlers

// GetAllKokurikulerActivities godoc
func (h *CurriculumHandler) GetAllKokurikulerActivities(c *fiber.Ctx) error {
	activities, err := h.svc.GetAllKokurikulerActivities(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil aktivitas kokurikuler", err)
	}
	return common.Success(c, "Aktivitas kokurikuler berhasil diambil", activities)
}

// GetKokurikulerActivityByID godoc
func (h *CurriculumHandler) GetKokurikulerActivityByID(c *fiber.Ctx) error {
	activity, err := h.svc.GetKokurikulerActivityByID(c.Context(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Aktivitas kokurikuler tidak ditemukan", err)
	}
	return common.Success(c, "Aktivitas kokurikuler berhasil diambil", activity)
}

// CreateKokurikulerActivity godoc
func (h *CurriculumHandler) CreateKokurikulerActivity(c *fiber.Ctx) error {
	var req CreateKokurikulerActivityRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	activity, err := h.svc.CreateKokurikulerActivity(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat aktivitas kokurikuler", err)
	}
	return common.Created(c, "Aktivitas kokurikuler berhasil dibuat", activity)
}

// UpdateKokurikulerActivity godoc
func (h *CurriculumHandler) UpdateKokurikulerActivity(c *fiber.Ctx) error {
	var req UpdateKokurikulerActivityRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	activity, err := h.svc.UpdateKokurikulerActivity(c.Context(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate aktivitas kokurikuler", err)
	}
	return common.Success(c, "Aktivitas kokurikuler berhasil diupdate", activity)
}

// DeleteKokurikulerActivity godoc
func (h *CurriculumHandler) DeleteKokurikulerActivity(c *fiber.Ctx) error {
	if err := h.svc.DeleteKokurikulerActivity(c.Context(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus aktivitas kokurikuler", err)
	}
	return common.Success(c, "Aktivitas kokurikuler berhasil dihapus", nil)
}

// Extra-curricular Activities Handlers

// GetAllEkstrakurikulerActivities godoc
func (h *CurriculumHandler) GetAllEkstrakurikulerActivities(c *fiber.Ctx) error {
	activities, err := h.svc.GetAllEkstrakurikulerActivities(c.Context())
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil aktivitas ekstrakurikuler", err)
	}
	return common.Success(c, "Aktivitas ekstrakurikuler berhasil diambil", activities)
}

// GetEkstrakurikulerActivityByID godoc
func (h *CurriculumHandler) GetEkstrakurikulerActivityByID(c *fiber.Ctx) error {
	activity, err := h.svc.GetEkstrakurikulerActivityByID(c.Context(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Aktivitas ekstrakurikuler tidak ditemukan", err)
	}
	return common.Success(c, "Aktivitas ekstrakurikuler berhasil diambil", activity)
}

// CreateEkstrakurikulerActivity godoc
func (h *CurriculumHandler) CreateEkstrakurikulerActivity(c *fiber.Ctx) error {
	var req CreateEkstrakurikulerActivityRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	activity, err := h.svc.CreateEkstrakurikulerActivity(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat aktivitas ekstrakurikuler", err)
	}
	return common.Created(c, "Aktivitas ekstrakurikuler berhasil dibuat", activity)
}

// UpdateEkstrakurikulerActivity godoc
func (h *CurriculumHandler) UpdateEkstrakurikulerActivity(c *fiber.Ctx) error {
	var req UpdateEkstrakurikulerActivityRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	activity, err := h.svc.UpdateEkstrakurikulerActivity(c.Context(), c.Params("id"), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengupdate aktivitas ekstrakurikuler", err)
	}
	return common.Success(c, "Aktivitas ekstrakurikuler berhasil diupdate", activity)
}

// DeleteEkstrakurikulerActivity godoc
func (h *CurriculumHandler) DeleteEkstrakurikulerActivity(c *fiber.Ctx) error {
	if err := h.svc.DeleteEkstrakurikulerActivity(c.Context(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus aktivitas ekstrakurikuler", err)
	}
	return common.Success(c, "Aktivitas ekstrakurikuler berhasil dihapus", nil)
}

// Analysis Data Integration Handlers (FR 4.2.1-4.2.5)

func (h *CurriculumHandler) IntegrateSWOTData(c *fiber.Ctx) error {
	var req AnalysisDataIntegrationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	response, err := h.svc.IntegrateSWOTData(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengintegrasikan SWOT data", err)
	}
	return common.Success(c, "SWOT data berhasil diintegrasikan", response)
}

func (h *CurriculumHandler) IntegrateRootCauseData(c *fiber.Ctx) error {
	var req AnalysisDataIntegrationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	response, err := h.svc.IntegrateRootCauseData(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengintegrasikan Root Cause data", err)
	}
	return common.Success(c, "Root Cause data berhasil diintegrasikan", response)
}

func (h *CurriculumHandler) IntegrateFishboneData(c *fiber.Ctx) error {
	var req AnalysisDataIntegrationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	response, err := h.svc.IntegrateFishboneData(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengintegrasikan Fishbone data", err)
	}
	return common.Success(c, "Fishbone data berhasil diintegrasikan", response)
}

func (h *CurriculumHandler) IntegrateStudentNeedsData(c *fiber.Ctx) error {
	var req AnalysisDataIntegrationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	response, err := h.svc.IntegrateStudentNeedsData(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengintegrasikan Student Needs data", err)
	}
	return common.Success(c, "Student Needs data berhasil diintegrasikan", response)
}

func (h *CurriculumHandler) GenerateKSPWithAnalysis(c *fiber.Ctx) error {
	var req KSPExportWithAnalysisRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	response, err := h.svc.GenerateKSPWithAnalysis(c.Context(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal generate KSP dengan analysis data", err)
	}
	return common.Success(c, "KSP dengan analysis data berhasil di-generate", response)
}
