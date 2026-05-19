package ppdb

import (
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"

	"github.com/gofiber/fiber/v2"
)

type PPDBHandler struct {
	svc PPDBService
}

func NewPPDBHandler(svc PPDBService) *PPDBHandler {
	return &PPDBHandler{svc: svc}
}

// RegisterHandler godoc
func (h *PPDBHandler) Register(c *fiber.Ctx) error {
	var req RegisterPPDBRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	data, err := h.svc.Register(c.UserContext(), req)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mendaftar", err.Error())
	}
	return common.Created(c, "Pendaftaran berhasil, simpan nomor registrasi Anda", data)
}

// CheckStatusHandler godoc
func (h *PPDBHandler) CheckStatus(c *fiber.Ctx) error {
	nik := c.Query("nik")
	if nik == "" {
		return common.Error(c, fiber.StatusBadRequest, "NIK wajib diisi", "")
	}

	data, err := h.svc.CheckStatusByNIK(c.UserContext(), nik)
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Data pendaftar tidak ditemukan", err.Error())
	}

	res := fiber.Map{
		"registration_no": data.RegistrationNo,
		"full_name":       data.FullName,
		"status":          data.Status,
	}

	return common.Success(c, "Status berhasil dicek", res)
}

// UploadDocumentHandler godoc
func (h *PPDBHandler) UploadDocument(c *fiber.Ctx) error {
	docType := c.FormValue("document_type")
	if docType == "" {
		return common.Error(c, fiber.StatusBadRequest, "Tipe dokumen wajib diisi", "")
	}

	file, err := c.FormFile("file")
	if err != nil {
		return common.Error(c, fiber.StatusBadRequest, "File tidak ditemukan dalam request", err.Error())
	}

	if err := h.svc.UploadDocument(c.UserContext(), c.Params("id"), docType, file); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengupload dokumen", err.Error())
	}

	return common.Success(c, "Dokumen berhasil diupload", nil)
}

// GetApplicantsHandler godoc
func (h *PPDBHandler) GetApplicants(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	status := c.Query("status", "")

	data, total, err := h.svc.GetApplicants(c.UserContext(), pagination, status)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data", err.Error())
	}
	return common.Paginated(c, "Data pendaftar", data, pagination.Page, pagination.Limit, total)
}

// GetApplicantDetailHandler godoc
func (h *PPDBHandler) GetApplicantDetail(c *fiber.Ctx) error {
	data, err := h.svc.GetApplicantByID(c.UserContext(), c.Params("id"))
	if err != nil {
		return common.Error(c, fiber.StatusNotFound, "Data tidak ditemukan", err.Error())
	}
	return common.Success(c, "Detail pendaftar", data)
}

// VerifyApplicantHandler godoc
func (h *PPDBHandler) VerifyApplicant(c *fiber.Ctx) error {
	var req VerifyPPDBRequest
	if err := c.BodyParser(&req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Invalid request", err.Error())
	}
	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", err.Error())
	}

	if err := h.svc.VerifyApplication(c.UserContext(), c.Params("id"), req); err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal memverifikasi", err.Error())
	}

	msg := "Pendaftar berhasil diverifikasi"
	if req.Status == "Accepted" {
		msg = "Pendaftar berhasil diterima dan data siswa telah dibuat secara otomatis"
	}

	// Trigger Audit Log
	userID, _ := c.Locals("user_id").(string)
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "VERIFY_PPDB", "applicant", c.Params("id"), c.IP())
	}

	return common.Success(c, msg, nil)
}

// GetAdmissionPathsHandler godoc
func (h *PPDBHandler) GetAdmissionPaths(c *fiber.Ctx) error {
	data, err := h.svc.GetAdmissionPaths(c.UserContext())
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil jalur masuk", err.Error())
	}
	return common.Success(c, "Daftar jalur masuk seleksi", data)
}

// GetActiveAcademicYearsHandler godoc
func (h *PPDBHandler) GetActiveAcademicYears(c *fiber.Ctx) error {
	data, err := h.svc.GetActiveAcademicYears(c.UserContext())
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil tahun ajaran aktif", err.Error())
	}
	return common.Success(c, "Daftar tahun ajaran aktif", data)
}
