package schedule

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type ScheduleHandler struct {
	svc ScheduleService
}

func NewScheduleHandler(svc ScheduleService) *ScheduleHandler {
	return &ScheduleHandler{svc: svc}
}

// GetByClassroom godoc
// @Summary Get Schedules By Classroom
// @Tags Academic Schedule
// @Produce json
// @Security BearerAuth
// @Param id path string true "Classroom ID"
// @Success 200 {object} common.Response
// @Router /classrooms/{id}/schedules [get]
func (h *ScheduleHandler) GetByClassroom(c *fiber.Ctx) error {
	data, err := h.svc.GetByClassroom(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil jadwal kelas", err)
	}
	return common.Success(c, "Jadwal berhasil diambil", data)
}

// GetByTeacher godoc
// @Summary Get Schedules By Teacher
// @Tags Academic Schedule
// @Produce json
// @Security BearerAuth
// @Param id path string true "Teacher ID"
// @Success 200 {object} common.Response
// @Router /teachers/{id}/schedules [get]
func (h *ScheduleHandler) GetByTeacher(c *fiber.Ctx) error {
	data, err := h.svc.GetByTeacher(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil jadwal guru", err)
	}
	return common.Success(c, "Jadwal berhasil diambil", data)
}

// Create godoc
// @Summary Create Schedule
// @Tags Academic Schedule
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body CreateScheduleRequest true "Schedule Request"
// @Success 201 {object} common.Response
// @Router /schedules [post]
func (h *ScheduleHandler) Create(c *fiber.Ctx) error {
	var req CreateScheduleRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	data, err := h.svc.Create(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat jadwal", err)
	}
	return common.Success(c, "Jadwal berhasil dibuat", data)
}

// Delete godoc
// @Summary Delete Schedule
// @Tags Academic Schedule
// @Produce json
// @Security BearerAuth
// @Param id path string true "Schedule ID"
// @Success 200 {object} common.Response
// @Router /schedules/{id} [delete]
func (h *ScheduleHandler) Delete(c *fiber.Ctx) error {
	if err := h.svc.Delete(c.UserContext(), c.Params("id")); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus jadwal", err)
	}
	return common.Success(c, "Jadwal berhasil dihapus", nil)
}
