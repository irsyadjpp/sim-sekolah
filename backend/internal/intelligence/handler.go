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
		return common.Error(c, fiber.StatusBadRequest, "Student ID is required", nil)
	}

	profile, err := h.svc.GetStudent360Profile(c.UserContext(), studentID)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to get student 360 profile", err.Error())
	}
	return common.Success(c, "Student 360 profile successfully retrieved", profile)
}

func (h *IntelligenceHandler) UpsertProfileExt(c *fiber.Ctx) error {
	studentID := c.Params("student_id")
	if studentID == "" {
		return common.Error(c, fiber.StatusBadRequest, "Student ID is required", nil)
	}

	var req UpsertProfileExtRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}

	err := h.svc.UpsertProfileExt(c.UserContext(), studentID, req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to update student profile extension", err.Error())
	}
	return common.Success(c, "Student profile extension successfully updated", nil)
}

func (h *IntelligenceHandler) CreateAnecdotal(c *fiber.Ctx) error {
	var req CreateAnecdotalRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}

	teacherID, ok := c.Locals("user_id").(string)
	if !ok || teacherID == "" {
		return common.Error(c, fiber.StatusUnauthorized, "Unauthorized", "Teacher ID missing")
	}

	obs, err := h.svc.CreateAnecdotal(c.UserContext(), req, teacherID)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to record anecdotal observation", err.Error())
	}
	return common.Success(c, "Anecdotal observation notes successfully saved", obs)
}

func (h *IntelligenceHandler) GetObservationTags(c *fiber.Ctx) error {
	tags, err := h.svc.GetObservationTags(c.UserContext())
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to get observation tags", err.Error())
	}
	return common.Success(c, "Observation tags list successfully retrieved", tags)
}

func (h *IntelligenceHandler) CreateInstrument(c *fiber.Ctx) error {
	var req CreateInstrumentRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}

	inst, err := h.svc.CreateInstrument(c.UserContext(), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to create assessment instrument", err.Error())
	}
	return common.Success(c, "Assessment instrument successfully created", inst)
}

func (h *IntelligenceHandler) SubmitResults(c *fiber.Ctx) error {
	instrumentID := c.Params("instrument_id")
	if instrumentID == "" {
		return common.Error(c, fiber.StatusBadRequest, "Instrument ID is required", nil)
	}

	var req SubmitResultsBatchRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}

	err := h.svc.SubmitResultsBatch(c.UserContext(), instrumentID, req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to submit student assessment scores", err.Error())
	}
	return common.Success(c, "Mass student assessment scores successfully submitted", nil)
}

func (h *IntelligenceHandler) GetResults(c *fiber.Ctx) error {
	instrumentID := c.Params("instrument_id")
	if instrumentID == "" {
		return common.Error(c, fiber.StatusBadRequest, "Instrument ID is required", nil)
	}

	results, err := h.svc.GetResultsByInstrument(c.UserContext(), instrumentID)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to get student assessment scores", err.Error())
	}
	return common.Success(c, "Student assessment scores successfully retrieved", results)
}

func (h *IntelligenceHandler) GetAlerts(c *fiber.Ctx) error {
	classroomID := c.Query("classroom_id")
	if classroomID == "" {
		return common.Error(c, fiber.StatusBadRequest, "Classroom ID query parameter is required", nil)
	}

	alerts, err := h.svc.GetAlertsByClassroom(c.UserContext(), classroomID)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to get early warning system (EWS) alerts", err.Error())
	}
	return common.Success(c, "Classroom early warning system (EWS) alerts successfully retrieved", alerts)
}

func (h *IntelligenceHandler) UpdateAlert(c *fiber.Ctx) error {
	alertID := c.Params("alert_id")
	if alertID == "" {
		return common.Error(c, fiber.StatusBadRequest, "Alert ID is required", nil)
	}

	var req EarlyWarningInterventionRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request body", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validation failed", err.Error())
	}

	err := h.svc.UpdateAlert(c.UserContext(), alertID, req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to update counseling warning status", err.Error())
	}
	return common.Success(c, "Counseling early warning intervention successfully recorded", nil)
}

func (h *IntelligenceHandler) TriggerCron(c *fiber.Ctx) error {
	err := h.svc.CalculateEarlyWarningAlerts(c.UserContext())
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Failed to run risk analytics assistant EWS", err.Error())
	}
	return common.Success(c, "Risk analytics assistant EWS triggered successfully", nil)
}
