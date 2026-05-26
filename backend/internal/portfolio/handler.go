package portfolio

import (
	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type Handler struct {
	service Service
}

func NewHandler(service Service) *Handler {
	return &Handler{service: service}
}

// Portfolio handlers
func (h *Handler) CreatePortfolio(c *fiber.Ctx) error {
	var request PortfolioRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.CreatePortfolio(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *Handler) GetPortfolioByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	response, err := h.service.GetPortfolioByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Portfolio not found",
		})
	}

	return c.JSON(response)
}

func (h *Handler) GetPortfolios(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if studentID := c.Query("student_id"); studentID != "" {
		id, err := uuid.Parse(studentID)
		if err == nil {
			filter["student_id"] = id
		}
	}

	if portfolioType := c.Query("portfolio_type"); portfolioType != "" {
		filter["portfolio_type"] = portfolioType
	}

	if period := c.Query("period"); period != "" {
		filter["period"] = period
	}

	if academicYearID := c.Query("academic_year_id"); academicYearID != "" {
		id, err := uuid.Parse(academicYearID)
		if err == nil {
			filter["academic_year_id"] = id
		}
	}

	if isPublished := c.Query("is_published"); isPublished != "" {
		if isPublished == "true" {
			filter["is_published"] = true
		} else if isPublished == "false" {
			filter["is_published"] = false
		}
	}

	responses, err := h.service.GetPortfolios(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

func (h *Handler) UpdatePortfolio(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	var request PortfolioRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.UpdatePortfolio(id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

func (h *Handler) DeletePortfolio(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	err = h.service.DeletePortfolio(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

func (h *Handler) GetStudentPortfolios(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("student_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid student ID format",
		})
	}

	responses, err := h.service.GetStudentPortfolios(studentID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

func (h *Handler) PublishPortfolio(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	response, err := h.service.PublishPortfolio(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

// Artifact handlers
func (h *Handler) CreateArtifact(c *fiber.Ctx) error {
	var request PortfolioArtifactRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.CreateArtifact(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *Handler) GetArtifactByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	response, err := h.service.GetArtifactByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Artifact not found",
		})
	}

	return c.JSON(response)
}

func (h *Handler) GetArtifacts(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if portfolioID := c.Query("portfolio_id"); portfolioID != "" {
		id, err := uuid.Parse(portfolioID)
		if err == nil {
			filter["portfolio_id"] = id
		}
	}

	if artifactType := c.Query("artifact_type"); artifactType != "" {
		filter["artifact_type"] = artifactType
	}

	if isFeatured := c.Query("is_featured"); isFeatured != "" {
		if isFeatured == "true" {
			filter["is_featured"] = true
		} else if isFeatured == "false" {
			filter["is_featured"] = false
		}
	}

	responses, err := h.service.GetArtifacts(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

func (h *Handler) UpdateArtifact(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	var request PortfolioArtifactRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.UpdateArtifact(id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

func (h *Handler) DeleteArtifact(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	err = h.service.DeleteArtifact(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

func (h *Handler) GetPortfolioArtifacts(c *fiber.Ctx) error {
	portfolioID, err := uuid.Parse(c.Params("portfolio_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid portfolio ID format",
		})
	}

	responses, err := h.service.GetPortfolioArtifacts(portfolioID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

// LearningEvidence handlers
func (h *Handler) CreateLearningEvidence(c *fiber.Ctx) error {
	var request LearningEvidenceRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.CreateLearningEvidence(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *Handler) GetLearningEvidenceByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	response, err := h.service.GetLearningEvidenceByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Learning evidence not found",
		})
	}

	return c.JSON(response)
}

func (h *Handler) GetLearningEvidence(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if studentID := c.Query("student_id"); studentID != "" {
		id, err := uuid.Parse(studentID)
		if err == nil {
			filter["student_id"] = id
		}
	}

	if artifactID := c.Query("artifact_id"); artifactID != "" {
		id, err := uuid.Parse(artifactID)
		if err == nil {
			filter["artifact_id"] = id
		}
	}

	if competencyType := c.Query("competency_type"); competencyType != "" {
		filter["competency_type"] = competencyType
	}

	if validationStatus := c.Query("validation_status"); validationStatus != "" {
		filter["validation_status"] = validationStatus
	}

	responses, err := h.service.GetLearningEvidence(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

func (h *Handler) UpdateLearningEvidence(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	var request LearningEvidenceRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.UpdateLearningEvidence(id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

func (h *Handler) DeleteLearningEvidence(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	err = h.service.DeleteLearningEvidence(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

func (h *Handler) GetStudentLearningEvidence(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("student_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid student ID format",
		})
	}

	responses, err := h.service.GetStudentLearningEvidence(studentID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

func (h *Handler) ValidateEvidence(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	var request struct {
		ValidationStatus string    `json:"validation_status" validate:"required"`
		Notes            string    `json:"notes"`
		ValidatedBy      uuid.UUID `json:"validated_by" validate:"required"`
	}

	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.ValidateEvidence(id, request.ValidationStatus, request.Notes, request.ValidatedBy)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

// PortfolioReview handlers
func (h *Handler) CreateReview(c *fiber.Ctx) error {
	var request PortfolioReviewRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.CreateReview(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *Handler) GetReviewByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	response, err := h.service.GetReviewByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Review not found",
		})
	}

	return c.JSON(response)
}

func (h *Handler) GetReviews(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if portfolioID := c.Query("portfolio_id"); portfolioID != "" {
		id, err := uuid.Parse(portfolioID)
		if err == nil {
			filter["portfolio_id"] = id
		}
	}

	if reviewerID := c.Query("reviewer_id"); reviewerID != "" {
		id, err := uuid.Parse(reviewerID)
		if err == nil {
			filter["reviewer_id"] = id
		}
	}

	if isFormal := c.Query("is_formal"); isFormal != "" {
		if isFormal == "true" {
			filter["is_formal"] = true
		} else if isFormal == "false" {
			filter["is_formal"] = false
		}
	}

	responses, err := h.service.GetReviews(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

func (h *Handler) UpdateReview(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	var request PortfolioReviewRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.UpdateReview(id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

func (h *Handler) DeleteReview(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	err = h.service.DeleteReview(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

func (h *Handler) GetPortfolioReviews(c *fiber.Ctx) error {
	portfolioID, err := uuid.Parse(c.Params("portfolio_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid portfolio ID format",
		})
	}

	responses, err := h.service.GetPortfolioReviews(portfolioID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

// Analytics handlers
func (h *Handler) GetPortfolioAnalytics(c *fiber.Ctx) error {
	var request PortfolioAnalyticsRequest

	if studentID := c.Query("student_id"); studentID != "" {
		id, err := uuid.Parse(studentID)
		if err == nil {
			request.StudentID = &id
		}
	}

	if period := c.Query("period"); period != "" {
		request.Period = &period
	}

	if academicYearID := c.Query("academic_year_id"); academicYearID != "" {
		id, err := uuid.Parse(academicYearID)
		if err == nil {
			request.AcademicYearID = &id
		}
	}

	if portfolioType := c.Query("portfolio_type"); portfolioType != "" {
		request.PortfolioType = &portfolioType
	}

	response, err := h.service.GetPortfolioAnalytics(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

// Export handlers
func (h *Handler) ExportStudentPortfolioReport(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("student_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid student ID format",
		})
	}

	// Get all student portfolios
	portfolios, err := h.service.GetStudentPortfolios(studentID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	// Get all student learning evidence
	evidence, err := h.service.GetStudentLearningEvidence(studentID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	report := fiber.Map{
		"portfolios": portfolios,
		"evidence":   evidence,
	}

	return c.JSON(report)
}
