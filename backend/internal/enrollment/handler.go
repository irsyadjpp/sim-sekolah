package enrollment

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type EnrollmentHandler struct {
	svc EnrollmentService
}

func NewEnrollmentHandler(svc EnrollmentService) *EnrollmentHandler {
	return &EnrollmentHandler{svc: svc}
}

// GetEnrollmentsHandler godoc
func (h *EnrollmentHandler) GetEnrollments(c *fiber.Ctx) error {
	data, err := h.svc.GetByClassroom(c.UserContext(), c.Params("classroomId"))
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data enrollment", err.Error())
	}
	return common.Success(c, "Data enrollment berhasil diambil", data)
}

// EnrollStudentHandler godoc
func (h *EnrollmentHandler) EnrollStudent(c *fiber.Ctx) error {
	classroomID := c.Params("classroomId")
	var req CreateEnrollmentRequest

	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	data, err := h.svc.Enroll(c.UserContext(), classroomID, req)
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Gagal mendaftarkan siswa", err.Error())
	}
	return common.Created(c, "Siswa berhasil didaftarkan", data)
}

// BulkEnrollHandler godoc
func (h *EnrollmentHandler) BulkEnroll(c *fiber.Ctx) error {
	classroomID := c.Params("classroomId")
	var req BulkEnrollRequest

	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Request body tidak valid", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	created, skipped, err := h.svc.BulkEnroll(c.UserContext(), classroomID, req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mendaftarkan siswa", err.Error())
	}

	return common.Created(c, "Bulk enrollment selesai", fiber.Map{
		"enrolled": created,
		"skipped":  skipped,
	})
}

// UnenrollStudentHandler godoc
func (h *EnrollmentHandler) UnenrollStudent(c *fiber.Ctx) error {
	if err := h.svc.Unenroll(c.UserContext(), c.Params("classroomId"), c.Params("enrollmentId")); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Gagal menghapus enrollment", err.Error())
	}
	return common.Success(c, "Siswa berhasil dikeluarkan dari kelas", nil)
}
