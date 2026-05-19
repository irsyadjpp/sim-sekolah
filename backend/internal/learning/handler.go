package learning

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

type LearningHandler struct {
	svc LearningService
}

func NewLearningHandler(svc LearningService) *LearningHandler {
	return &LearningHandler{svc: svc}
}

func (h *LearningHandler) GenerateModule(c *fiber.Ctx) error {
	atpID, err := uuid.Parse(c.Params("atpId"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "ID ATP tidak valid", err)
	}

	schoolContext := c.Query("school_context", "Pesisir, kepulauan, akses internet terbatas.")

	res, err := h.svc.GenerateTeachingModuleAI(c.Context(), atpID, schoolContext)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal membuat modul", err)
	}

	return common.Success(c, "Modul berhasil dibuat", res)
}

func (h *LearningHandler) SaveModule(c *fiber.Ctx) error {
	var module TeachingModule
	if err := c.BodyParser(&module); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	if err := h.svc.SaveTeachingModule(c.Context(), &module); err != nil {
		return common.ErrorFromService(c, fiber.StatusUnprocessableEntity, "Gagal menyimpan modul", err)
	}

	return common.Success(c, "Modul berhasil disimpan", module)
}

func (h *LearningHandler) GetAllATP(c *fiber.Ctx) error {
	classroomID := c.Query("classroom_id")
	res, err := h.svc.GetAllATP(classroomID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengambil ATP", err)
	}
	return common.Success(c, "ATP berhasil diambil", res)
}

func (h *LearningHandler) GetATPByID(c *fiber.Ctx) error {
	res, err := h.svc.GetATPByID(c.Params("id"))
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "ATP tidak ditemukan", err)
	}
	return common.Success(c, "ATP berhasil diambil", res)
}

func (h *LearningHandler) SaveATP(c *fiber.Ctx) error {
	var atp ATP
	if err := c.BodyParser(&atp); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}
	if err := h.svc.SaveATP(c.Context(), &atp); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menyimpan ATP", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "SAVE", "atp", atp.ID.String(), c.IP())
	}

	return common.Success(c, "ATP berhasil disimpan", atp)
}

func (h *LearningHandler) DeleteATP(c *fiber.Ctx) error {
	id := c.Params("id")
	if err := h.svc.DeleteATP(c.UserContext(), id); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghapus ATP", err)
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "DELETE", "atp", id, c.IP())
	}

	return common.Success(c, "ATP berhasil dihapus", nil)
}
