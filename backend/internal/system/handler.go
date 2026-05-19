package system

import (
	"sim-sekolah/internal/common"

	"github.com/gofiber/fiber/v2"
)

type Handler struct {
	service SystemService
	audit   AuditService
}

func NewHandler(service SystemService, audit AuditService) *Handler {
	return &Handler{service: service, audit: audit}
}

// GetPimpinan godoc
// @Summary      Get Pimpinan Dashboard Data
// @Description  Mengambil data statistik makro sekolah untuk kebutuhan dasbor Pimpinan (Kepala Sekolah), termasuk tingkat kelulusan siswa, kepatuhan pengerjaan KSP, dan ringkasan diagram nilai kognitif siswa secara real-time.
// @Tags         System & Dashboard
// @Produce      json
// @Success      200  {object}  common.Response  "Data dasbor pimpinan berhasil diambil"
// @Failure      500  {object}  common.Response  "Gagal mengambil data dasbor pimpinan"
// @Router       /system/dashboard/pimpinan [get]
func (h *Handler) GetPimpinan(c *fiber.Ctx) error {
	data, err := h.service.GetPimpinanDashboard(c.UserContext())
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data dasbor pimpinan", err.Error())
	}
	return common.Success(c, "Data dasbor pimpinan berhasil diambil", data)
}

// GetGuru godoc
// @Summary      Get Guru Dashboard Data
// @Description  Mengambil data aktivitas operasional harian untuk dasbor Guru, termasuk tingkat kepatuhan pengerjaan Modul Ajar mandiri dan pemantauan perkembangan kognitif/sosial siswa di kelas yang diajarnya.
// @Tags         System & Dashboard
// @Produce      json
// @Success      200  {object}  common.Response  "Data dasbor guru berhasil diambil"
// @Failure      500  {object}  common.Response  "Gagal mengambil data dasbor guru"
// @Router       /system/dashboard/guru [get]
func (h *Handler) GetGuru(c *fiber.Ctx) error {
	data, err := h.service.GetGuruDashboard(c.UserContext())
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data dasbor guru", err.Error())
	}
	return common.Success(c, "Data dasbor guru berhasil diambil", data)
}

// GetOperator godoc
// @Summary      Get Operator Dashboard Data
// @Description  Mengambil statistik telemetri kesehatan perangkat keras (*hardware* server), utilisasi memori cache Redis, pool database PostgreSQL, dan ringkasan persentase sinkronisasi Dapodik untuk dasbor Operator Sistem.
// @Tags         System & Dashboard
// @Produce      json
// @Success      200  {object}  common.Response  "Data dasbor operator berhasil diambil"
// @Failure      500  {object}  common.Response  "Gagal mengambil data dasbor operator"
// @Router       /system/dashboard/operator [get]
func (h *Handler) GetOperator(c *fiber.Ctx) error {
	data, err := h.service.GetOperatorDashboard(c.UserContext())
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data dasbor operator", err.Error())
	}
	return common.Success(c, "Data dasbor operator berhasil diambil", data)
}

// GetAuditLogs godoc
// @Summary      Get System Audit Logs
// @Description  Mengambil daftar catatan log audit aktivitas operasional sistem secara paginasi. Mendukung pencarian kueri berdasarkan nama/email pengguna dan penyaringan berdasarkan tipe aksi keamanan.
// @Tags         System & Dashboard
// @Produce      json
// @Param        page    query     int     false  "Nomor halaman aktif (default: 1)"
// @Param        limit   query     int     false  "Jumlah entri log per halaman (default: 10)"
// @Param        search  query     string  false  "Kata kunci pencarian nama atau email aktor pengguna"
// @Param        action  query     string  false  "Penyaringan berdasarkan tipe aksi keamanan (e.g. LOGIN, UPDATE, DELETE)"
// @Success      200  {object}  common.PaginationResponse{data=[]AuditLog}  "Data audit log berhasil diambil secara terpaginasi"
// @Failure      500  {object}  common.Response  "Gagal mengambil data audit log"
// @Router       /system/audit-logs [get]
func (h *Handler) GetAuditLogs(c *fiber.Ctx) error {
	pagination := common.GetPagination(c)
	search := c.Query("search", "")
	actionFilter := c.Query("action", "")

	data, total, err := h.audit.GetAuditLogs(c.UserContext(), pagination.Page, pagination.Limit, search, actionFilter)
	if err != nil {
		return common.Error(c, fiber.StatusInternalServerError, "Gagal mengambil data audit log", err.Error())
	}
	return common.Paginated(c, "Data audit log berhasil diambil", data, pagination.Page, pagination.Limit, total)
}
