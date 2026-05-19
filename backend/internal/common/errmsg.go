package common

import (
	"strings"

	"github.com/gofiber/fiber/v2"
)

// serviceErrorMessages maps stable English service error strings to Indonesian user-facing text.
// Service layers should keep emitting the English keys; handlers translate via UserMessage.
var serviceErrorMessages = map[string]string{
	// auth
	"all fields are required":             "Semua field wajib diisi",
	"username already exists":             "Username sudah digunakan",
	"role GURU not found":                 "Role GURU tidak ditemukan di sistem",
	"email and password are required":     "Email dan kata sandi wajib diisi",
	"invalid email or password":           "Email atau kata sandi tidak valid",
	"account is disabled":                 "Akun dinonaktifkan",
	"account is locked":                   "Akun terkunci",
	"account is expired":                  "Akun kedaluwarsa",
	"credentials have expired":            "Kredensial kedaluwarsa",
	"invalid refresh token":               "Token penyegar tidak valid",
	"refresh token expired":               "Token penyegar kedaluwarsa",
	"user not found":                      "Pengguna tidak ditemukan",
	"account is disabled or locked":       "Akun dinonaktifkan atau terkunci",
	"failed to create new refresh token":  "Gagal membuat token penyegar baru",
	"failed to create reset token":        "Gagal membuat token reset sandi",
	"invalid or expired token":            "Token tidak valid atau kedaluwarsa",
	"failed to hash new password":         "Gagal mengenkripsi sandi baru",
	"failed to update password":           "Gagal memperbarui sandi",
	"failed to connect to storage server": "Gagal terhubung ke server penyimpanan",
	"failed to create refresh token":      "Gagal membuat token penyegar",

	// common/security
	"unauthorized: no roles found in context":                      "Tidak terautentikasi: peran pengguna tidak ditemukan",
	"unauthorized: no user ID found in context":                    "Tidak terautentikasi: ID pengguna tidak ditemukan",
	"forbidden: you cannot modify a system-created resource":       "Akses ditolak: resource sistem tidak dapat diubah",
	"forbidden: you are not the owner of this resource":            "Akses ditolak: Anda bukan pemilik resource ini",
	"forbidden: user is not associated with any teacher profile":   "Akses ditolak: akun tidak terhubung ke profil guru",
	"forbidden: you don't have permission to modify this resource": "Akses ditolak: Anda tidak memiliki izin mengubah resource ini",

	// generic
	"unauthorized": "Tidak terautentikasi",

	// intelligence
	"invalid student ID":              "ID murid tidak valid",
	"student basic info not found":    "Data dasar murid tidak ditemukan",
	"invalid teacher ID":              "ID guru tidak valid",
	"invalid learning objective ID":   "ID tujuan pembelajaran tidak valid",
	"invalid teaching module ID":      "ID modul ajar tidak valid",
	"invalid instrument ID":           "ID instrumen penilaian tidak valid",
	"assessment instrument not found": "Instrumen penilaian tidak ditemukan",
	"invalid classroom ID":            "ID kelas tidak valid",
	"invalid alert ID":                "ID peringatan tidak valid",

	// curriculum
	"academic year not found":                                   "Tahun ajaran tidak ditemukan",
	"academic year is not active":                               "Tahun ajaran tidak aktif",
	"curriculum document already exists for this academic year": "Dokumen kurikulum sudah ada untuk tahun ajaran ini",
	"school readiness data not found":                           "Data kesiapan sekolah tidak ditemukan",
	"curriculum document not found":                             "Dokumen kurikulum tidak ditemukan",
	"cannot formulate chapters for a final document":            "Tidak dapat merumuskan bab untuk dokumen yang sudah final",
	"queue service is not initialized":                          "Layanan antrean belum diinisialisasi",
	"all 5 chapters must be completed before finalizing":        "Kelima bab harus selesai sebelum finalisasi",

	// spmb
	"invalid school_year_id":    "Tahun ajaran tidak valid",
	"invalid admission_path_id": "Jalur masuk tidak valid",
	"invalid birth_date format": "Format tanggal lahir tidak valid",

	// promotion
	"invalid operator ID": "ID operator tidak valid",

	// assessment
	"assessment tidak ditemukan":              "Asesmen tidak ditemukan",
	"classroom_id and date are required":      "ID kelas dan tanggal wajib diisi",
	"invalid classroom ID format":             "Format ID kelas tidak valid",
	"invalid date format, must be YYYY-MM-DD": "Format tanggal tidak valid, gunakan YYYY-MM-DD",

	// schedule
	"classroom ID is required": "ID kelas wajib diisi",
	"teacher ID is required":   "ID guru wajib diisi",

	// cp / subject
	"element not belongs to this subject":         "Elemen tidak termasuk mata pelajaran ini",
	"detail not belongs to this learning outcome": "Detail tidak termasuk capaian pembelajaran ini",

	// report (forbidden prefix handled below)
	"forbidden: hanya wali kelas atau admin yang berhak":             "Hanya wali kelas atau admin yang berhak",
	"forbidden: anda tidak mengajar mata pelajaran ini di kelas ini": "Anda tidak mengajar mata pelajaran ini di kelas ini",

	// enrollment
	"enrollment ini bukan milik kelas tersebut": "Data enrollment bukan milik kelas tersebut",

	// ai
	"GEMINI_API_KEY tidak dikonfigurasi": "Kunci API Gemini belum dikonfigurasi",

	// assessment (english keys)
	"format tanggal tidak valid, gunakan YYYY-MM-DD": "Format tanggal tidak valid, gunakan YYYY-MM-DD",

	// user
	"satu atau lebih role tidak valid": "Satu atau lebih peran tidak valid",

	// cp (english)
	"terdapat duplikasi elemen pada detail capaian pembelajaran": "Terdapat duplikasi elemen pada detail capaian pembelajaran",
	"mata pelajaran tidak valid atau tidak ditemukan":            "Mata pelajaran tidak valid atau tidak ditemukan",
	"fase pembelajaran tidak valid atau tidak ditemukan":         "Fase pembelajaran tidak valid atau tidak ditemukan",
}

var serviceErrorPrefixes = []struct {
	prefix string
	msg    string
}{
	{"invalid student ID in batch: ", "ID murid tidak valid dalam batch: "},
	{"invalid student ID: ", "ID murid tidak valid: "},
	{"invalid operator ID: ", "ID operator tidak valid: "},
	{"numeric_score is required for numeric scoring method for student ", "Skor numerik wajib diisi untuk metode penilaian numerik, murid "},
	{"siswa dengan ID ", "Siswa dengan ID "},
	{"forbidden: ", ""}, // exact keys preferred; prefix fallback uses remainder
}

// UserMessage returns an Indonesian user-facing message for a service error.
// If the error is already in Indonesian or unmapped, the original text is returned.
func UserMessage(err error) string {
	if err == nil {
		return ""
	}
	raw := err.Error()
	if msg, ok := serviceErrorMessages[raw]; ok {
		return msg
	}
	for _, p := range serviceErrorPrefixes {
		if strings.HasPrefix(raw, p.prefix) {
			if p.msg == "" {
				if strings.HasPrefix(raw, "forbidden: ") {
					return "Akses ditolak: " + strings.TrimPrefix(raw, "forbidden: ")
				}
				continue
			}
			return p.msg + strings.TrimPrefix(raw, p.prefix)
		}
	}
	if isLikelyIndonesian(raw) {
		return raw
	}
	return raw
}

// DevDetail returns the original error string for the JSON "error" field (developer/debug).
func DevDetail(err error) interface{} {
	if err == nil {
		return nil
	}
	return err.Error()
}

// IsForbidden reports whether err represents a forbidden access service error.
func IsForbidden(err error) bool {
	if err == nil {
		return false
	}
	raw := err.Error()
	return strings.HasPrefix(raw, "forbidden:") ||
		raw == "forbidden: you don't have permission to modify this resource" ||
		raw == "forbidden: hanya wali kelas atau admin yang berhak" ||
		raw == "forbidden: anda tidak mengajar mata pelajaran ini di kelas ini"
}

// IsUnauthorized reports whether err represents an unauthorized service error.
func IsUnauthorized(err error) bool {
	if err == nil {
		return false
	}
	raw := err.Error()
	return raw == "unauthorized" || strings.HasPrefix(raw, "unauthorized:")
}

// IsNotFound reports whether err represents a not-found style service error.
func IsNotFound(err error) bool {
	if err == nil {
		return false
	}
	raw := err.Error()
	return strings.Contains(raw, "not found") ||
		strings.Contains(raw, "tidak ditemukan") ||
		raw == "assessment instrument not found"
}

// HTTPStatusFromError picks an HTTP status from the service error, or returns fallback.
func HTTPStatusFromError(err error, fallback int) int {
	if err == nil {
		return fallback
	}
	if IsForbidden(err) {
		return fiber.StatusForbidden
	}
	if IsUnauthorized(err) {
		return fiber.StatusUnauthorized
	}
	if IsNotFound(err) {
		return fiber.StatusNotFound
	}
	raw := err.Error()
	if strings.Contains(raw, "already exists") || strings.Contains(raw, "sudah ada") || strings.Contains(raw, "sudah terdaftar") {
		return fiber.StatusConflict
	}
	if strings.HasPrefix(raw, "invalid ") || strings.Contains(raw, "tidak valid") || strings.Contains(raw, "wajib diisi") {
		return fiber.StatusBadRequest
	}
	return fallback
}

// ErrorFromService writes a standard API error: Indonesian message, original detail in "error".
func ErrorFromService(c *fiber.Ctx, fallbackStatus int, fallbackMessage string, err error) error {
	if err == nil {
		return Error(c, fallbackStatus, fallbackMessage, nil)
	}
	raw := err.Error()
	userMsg := UserMessage(err)
	if userMsg == raw && !isLikelyIndonesian(raw) {
		userMsg = fallbackMessage
	}
	status := HTTPStatusFromError(err, fallbackStatus)
	return Error(c, status, userMsg, raw)
}

// ErrorFromServiceMessage uses an explicit user message but still maps HTTP status from err.
func ErrorFromServiceMessage(c *fiber.Ctx, fallbackStatus int, userMessage string, err error) error {
	if err == nil {
		return Error(c, fallbackStatus, userMessage, nil)
	}
	status := HTTPStatusFromError(err, fallbackStatus)
	return Error(c, status, userMessage, DevDetail(err))
}

func isLikelyIndonesian(s string) bool {
	lower := strings.ToLower(s)
	indicators := []string{
		"tidak", "gagal", "berhasil", "wajib", "invalid", "sudah", "murid", "guru",
		"sekolah", "kelas", "rapor", "pendaftar", "akun", "sandi", "izin", "akses",
	}
	for _, w := range indicators {
		if strings.Contains(lower, w) {
			// exclude pure English "invalid" only when no Indonesian companion
			if w == "invalid" && !strings.Contains(lower, "tidak") && !strings.Contains(lower, "format") {
				continue
			}
			if w != "invalid" || strings.Contains(lower, "tidak") || strings.Contains(lower, "format") {
				return true
			}
		}
	}
	return false
}

// MapValidatorError translates common go-playground validator messages to Indonesian.
func MapValidatorError(err error) string {
	if err == nil {
		return ""
	}
	raw := err.Error()
	replacements := []struct{ from, to string }{
		{"is required", "wajib diisi"},
		{"must be a valid email", "harus berupa email yang valid"},
		{"must be at least", "minimal"},
		{"characters long", "karakter"},
		{"failed on the", "gagal pada"},
		{"validation for", "validasi untuk"},
	}
	out := raw
	for _, r := range replacements {
		out = strings.ReplaceAll(out, r.from, r.to)
	}
	return out
}
