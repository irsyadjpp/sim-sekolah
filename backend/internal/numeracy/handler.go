package numeracy

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

// Indicator handlers
func (h *Handler) CreateIndicator(c *fiber.Ctx) error {
	var request NumeracyIndicatorRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.CreateIndicator(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *Handler) GetIndicatorByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	response, err := h.service.GetIndicatorByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Indicator not found",
		})
	}

	return c.JSON(response)
}

func (h *Handler) GetIndicators(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if phaseID := c.Query("phase_id"); phaseID != "" {
		id, err := uuid.Parse(phaseID)
		if err == nil {
			filter["phase_id"] = id
		}
	}

	if numeracyType := c.Query("numeracy_type"); numeracyType != "" {
		filter["numeracy_type"] = numeracyType
	}

	if gradeLevel := c.Query("grade_level"); gradeLevel != "" {
		filter["grade_level"] = gradeLevel
	}

	if isActive := c.Query("is_active"); isActive != "" {
		if isActive == "true" {
			filter["is_active"] = true
		} else if isActive == "false" {
			filter["is_active"] = false
		}
	}

	responses, err := h.service.GetIndicators(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

func (h *Handler) UpdateIndicator(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	var request NumeracyIndicatorRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.UpdateIndicator(id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

func (h *Handler) DeleteIndicator(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	err = h.service.DeleteIndicator(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

// Assessment handlers
func (h *Handler) CreateAssessment(c *fiber.Ctx) error {
	var request NumeracyAssessmentRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.CreateAssessment(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *Handler) GetAssessmentByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	response, err := h.service.GetAssessmentByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Assessment not found",
		})
	}

	return c.JSON(response)
}

func (h *Handler) GetAssessments(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if studentID := c.Query("student_id"); studentID != "" {
		id, err := uuid.Parse(studentID)
		if err == nil {
			filter["student_id"] = id
		}
	}

	if indicatorID := c.Query("indicator_id"); indicatorID != "" {
		id, err := uuid.Parse(indicatorID)
		if err == nil {
			filter["indicator_id"] = id
		}
	}

	if assessmentType := c.Query("assessment_type"); assessmentType != "" {
		filter["assessment_type"] = assessmentType
	}

	if masteryLevel := c.Query("mastery_level"); masteryLevel != "" {
		filter["mastery_level"] = masteryLevel
	}

	responses, err := h.service.GetAssessments(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

func (h *Handler) UpdateAssessment(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	var request NumeracyAssessmentRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.UpdateAssessment(id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

func (h *Handler) DeleteAssessment(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	err = h.service.DeleteAssessment(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

// Growth handlers
func (h *Handler) CreateGrowth(c *fiber.Ctx) error {
	var request NumeracyGrowthRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.CreateGrowth(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *Handler) GetGrowthByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	response, err := h.service.GetGrowthByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Growth record not found",
		})
	}

	return c.JSON(response)
}

func (h *Handler) GetGrowthByStudentAndPeriod(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("student_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid student ID format",
		})
	}

	period := c.Params("period")
	if period == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Period is required",
		})
	}

	response, err := h.service.GetGrowthByStudentAndPeriod(studentID, period)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Growth record not found",
		})
	}

	return c.JSON(response)
}

func (h *Handler) GetGrowths(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if studentID := c.Query("student_id"); studentID != "" {
		id, err := uuid.Parse(studentID)
		if err == nil {
			filter["student_id"] = id
		}
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

	responses, err := h.service.GetGrowths(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

func (h *Handler) UpdateGrowth(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	var request NumeracyGrowthRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.UpdateGrowth(id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

func (h *Handler) DeleteGrowth(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	err = h.service.DeleteGrowth(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

func (h *Handler) CalculateStudentGrowth(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("student_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid student ID format",
		})
	}

	period := c.Query("period")
	if period == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Period is required",
		})
	}

	academicYearIDStr := c.Query("academic_year_id")
	if academicYearIDStr == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Academic year ID is required",
		})
	}

	academicYearID, err := uuid.Parse(academicYearIDStr)
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid academic year ID format",
		})
	}

	response, err := h.service.CalculateStudentGrowth(studentID, period, academicYearID)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

// Intervention handlers
func (h *Handler) CreateIntervention(c *fiber.Ctx) error {
	var request NumeracyInterventionRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.CreateIntervention(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusCreated).JSON(response)
}

func (h *Handler) GetInterventionByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	response, err := h.service.GetInterventionByID(id)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Intervention not found",
		})
	}

	return c.JSON(response)
}

func (h *Handler) GetInterventions(c *fiber.Ctx) error {
	filter := make(map[string]interface{})

	if studentID := c.Query("student_id"); studentID != "" {
		id, err := uuid.Parse(studentID)
		if err == nil {
			filter["student_id"] = id
		}
	}

	if indicatorID := c.Query("indicator_id"); indicatorID != "" {
		id, err := uuid.Parse(indicatorID)
		if err == nil {
			filter["indicator_id"] = id
		}
	}

	if interventionType := c.Query("intervention_type"); interventionType != "" {
		filter["intervention_type"] = interventionType
	}

	if status := c.Query("status"); status != "" {
		filter["status"] = status
	}

	responses, err := h.service.GetInterventions(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(responses)
}

func (h *Handler) UpdateIntervention(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	var request NumeracyInterventionRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	response, err := h.service.UpdateIntervention(id, request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

func (h *Handler) DeleteIntervention(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid ID format",
		})
	}

	err = h.service.DeleteIntervention(id)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(fiber.StatusNoContent).Send(nil)
}

// Analytics handlers
func (h *Handler) GetNumeracyAnalytics(c *fiber.Ctx) error {
	var request NumeracyAnalyticsRequest

	if studentID := c.Query("student_id"); studentID != "" {
		id, err := uuid.Parse(studentID)
		if err == nil {
			request.StudentID = &id
		}
	}

	if classroomID := c.Query("classroom_id"); classroomID != "" {
		id, err := uuid.Parse(classroomID)
		if err == nil {
			request.ClassroomID = &id
		}
	}

	if phaseID := c.Query("phase_id"); phaseID != "" {
		id, err := uuid.Parse(phaseID)
		if err == nil {
			request.PhaseID = &id
		}
	}

	if numeracyType := c.Query("numeracy_type"); numeracyType != "" {
		request.NumeracyType = &numeracyType
	}

	response, err := h.service.GetNumeracyAnalytics(request)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.JSON(response)
}

// Bulk operations handlers
func (h *Handler) BulkCreateAssessments(c *fiber.Ctx) error {
	var requests []NumeracyAssessmentRequest
	if err := c.BodyParser(&requests); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	responses := make([]NumeracyAssessmentResponse, len(requests))
	for i, request := range requests {
		response, err := h.service.CreateAssessment(request)
		if err != nil {
			return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
				"error": err.Error(),
				"index": i,
			})
		}
		responses[i] = *response
	}

	return c.Status(fiber.StatusCreated).JSON(responses)
}

func (h *Handler) BulkUpdateAssessments(c *fiber.Ctx) error {
	var requests []struct {
		ID      uuid.UUID                 `json:"id"`
		Request NumeracyAssessmentRequest `json:"request"`
	}
	if err := c.BodyParser(&requests); err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid request body",
		})
	}

	responses := make([]NumeracyAssessmentResponse, len(requests))
	for i, req := range requests {
		response, err := h.service.UpdateAssessment(req.ID, req.Request)
		if err != nil {
			return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
				"error": err.Error(),
				"index": i,
			})
		}
		responses[i] = *response
	}

	return c.JSON(responses)
}

// Export handlers
func (h *Handler) ExportStudentNumeracyReport(c *fiber.Ctx) error {
	studentID, err := uuid.Parse(c.Params("student_id"))
	if err != nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid student ID format",
		})
	}

	period := c.Query("period")
	if period == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Period is required",
		})
	}

	// Get growth data
	growth, err := h.service.GetGrowthByStudentAndPeriod(studentID, period)
	if err != nil {
		return c.Status(fiber.StatusNotFound).JSON(fiber.Map{
			"error": "Growth data not found",
		})
	}

	// Get assessments
	filter := map[string]interface{}{
		"student_id": studentID,
	}
	assessments, err := h.service.GetAssessments(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	// Get interventions
	interventions, err := h.service.GetInterventions(filter)
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	report := fiber.Map{
		"growth":        growth,
		"assessments":   assessments,
		"interventions": interventions,
	}

	return c.JSON(report)
}
