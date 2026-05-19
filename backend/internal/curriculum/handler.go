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
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}

	doc, err := h.svc.InitializeDocument(c.Context(), req)
	if err != nil {
		if err.Error() == "curriculum document already exists for this academic year" {
			return common.Error(c, fiber.StatusConflict, "Conflict", err.Error())
		}
		return common.Error(c, fiber.StatusInternalServerError, "Internal Server Error", err.Error())
	}

	return common.Created(c, "Curriculum document initialized", doc)
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
		return common.Error(c, fiber.StatusInternalServerError, "Internal Server Error", err.Error())
	}
	return common.Success(c, "Curriculum documents retrieved", docs)
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
		return common.Error(c, fiber.StatusBadRequest, "Invalid input", "invalid document id")
	}

	doc, err := h.svc.GetDocumentByID(c.Context(), docID)
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Not Found", "document not found")
	}

	return common.Success(c, "Curriculum document retrieved", doc)
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
		return common.Error(c, fiber.StatusBadRequest, "Invalid input", "invalid school id")
	}

	res, err := h.svc.CheckReadiness(c.Context(), schoolID)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Internal Server Error", err.Error())
	}

	return common.Success(c, "Readiness checked", res)
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
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}

	userIDStr, _ := c.Locals("user_id").(string)
	userID, err := uuid.Parse(userIDStr)
	if err != nil {
		return common.Error(c, fiber.StatusUnauthorized, "Unauthorized", "Invalid user token")
	}

	res, err := h.svc.TriggerChapterFormulation(c.Context(), userID, req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Internal Server Error", err.Error())
	}

	return common.Success(c, "Chapter formulation queued", res)
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
		return common.Error(c, fiber.StatusBadRequest, "Invalid input", "invalid document id")
	}

	chapterNum, err := c.ParamsInt("chapter_number")
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid input", "invalid chapter number")
	}

	chapter, err := h.svc.GetChapter(c.Context(), docID, chapterNum)
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Not Found", "chapter not found")
	}

	return common.Success(c, "Chapter retrieved", chapter)
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
		return common.Error(c, fiber.StatusBadRequest, "Invalid input", "invalid chapter id")
	}

	var req UpdateChapterRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}

	if err := h.svc.UpdateChapterContent(c.Context(), chapterID, req); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Internal Server Error", err.Error())
	}

	return common.Success(c, "Chapter updated", nil)
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
		return common.Error(c, fiber.StatusBadRequest, "Invalid input", "invalid document id")
	}

	if err := h.svc.FinalizeDocument(c.Context(), docID); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Bad Request", err.Error())
	}

	return common.Success(c, "Document finalized", nil)
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
		return common.Error(c, fiber.StatusBadRequest, "Invalid input", "invalid document id")
	}

	// Mock PDF Export Logic
	_ = docID
	return common.Success(c, "PDF exported successfully", map[string]string{
		"download_url": "https://storage.sim-sekolah.com/exports/curriculum.pdf",
	})
}
