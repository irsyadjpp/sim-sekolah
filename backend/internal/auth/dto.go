package auth

type RegisterRequest struct {
	FullName string `json:"full_name" validate:"required" example:"Budi Santoso"`     // Nama lengkap guru atau staf sekolah
	Username string `json:"username" validate:"required" example:"budis"`             // Username unik untuk login ke sistem
	Email    string `json:"email" validate:"required,email" example:"budi@sd.sch.id"` // Alamat email resmi pendaftar
	Password string `json:"password" validate:"required,min=6" example:"budi1234"`    // Kata sandi keamanan minimal 6 karakter
}

type LoginRequest struct {
	Email    string `json:"email" validate:"required,email" example:"admin@simsekolah.com"` // Alamat email resmi terdaftar
	Password string `json:"password" validate:"required" example:"password123"`             // Kata sandi keamanan pengguna
}

type ForgotPasswordRequest struct {
	Email string `json:"email" validate:"required,email" example:"budi@sd.sch.id"` // Alamat email terdaftar untuk pemulihan sandi
}

type ResetPasswordRequest struct {
	Token    string `json:"token" validate:"required" example:"abcdef123456"`          // Token unik pemulihan sandi yang dikirim lewat email
	Password string `json:"password" validate:"required,min=8" example:"sandiBaru999"` // Kata sandi baru minimal 8 karakter
}

type MeResponse struct {
	ID       string      `json:"id" example:"a425fa98-4362-4f74-9a33-8dcfbaeecc45"` // UUID identifikasi unik pengguna
	FullName string      `json:"full_name" example:"Budi Santoso"`                  // Nama lengkap pengguna
	Username string      `json:"username" example:"budis"`                          // Username login aktif
	Email    string      `json:"email" example:"budi@sd.sch.id"`                    // Alamat email aktif
	Roles    []string    `json:"roles" example:"GURU,WALIKELAS"`                    // Peran hak akses dalam sistem (RBAC)
	Teacher  interface{} `json:"teacher,omitempty"`                                 // Detail profil guru jika perannya adalah GURU
	Student  interface{} `json:"student,omitempty"`                                 // Detail profil siswa jika perannya adalah SISWA

	// Appearance Settings
	ThemeColor   string `json:"theme_color" example:"theme-purple"` // Pilihan warna utama UI (default: theme-purple)
	ThemeMode    string `json:"theme_mode" example:"dark"`          // Pilihan mode visual: 'light', 'dark', atau 'system'
	ContentType  string `json:"content_type" example:"boxed"`       // Tipe lebar tata letak: 'boxed' atau 'fluid'
	LeftMenuType string `json:"left_menu_type" example:"comfort"`   // Jenis kenyamanan menu kiri: 'comfort' atau 'compact'

	// Security & Notifications
	TwoFactorEnabled   bool `json:"two_factor_enabled" example:"true"`  // Status aktivasi Multi-Factor Authentication (MFA)
	EmailNotifications bool `json:"email_notifications" example:"true"` // Pengaturan persetujuan notifikasi via email
	PushNotifications  bool `json:"push_notifications" example:"true"`  // Pengaturan persetujuan notifikasi via web push
}

type UpdateMeRequest struct {
	FullName     string `json:"full_name" example:"Budi Santoso, S.Pd"` // Nama lengkap terbaru beserta gelar pendidikan
	Username     string `json:"username" example:"budi_santoso"`        // Username baru jika ingin diubah
	ThemeColor   string `json:"theme_color" example:"theme-purple"`     // Warna tema kustomisasi antarmuka
	ThemeMode    string `json:"theme_mode" example:"light"`             // Mode visual kustomisasi antarmuka
	ContentType  string `json:"content_type" example:"fluid"`           // Lebar halaman kustomisasi antarmuka
	LeftMenuType string `json:"left_menu_type" example:"compact"`       // Model menu kiri kustomisasi antarmuka

	// Pointer so we can differentiate false and nil (not sent)
	TwoFactorEnabled   *bool `json:"two_factor_enabled" example:"true"`   // Pengaktifan / penonaktifan Two-Factor Authentication (TOTP)
	EmailNotifications *bool `json:"email_notifications" example:"false"` // Pengaturan persetujuan notifikasi email
	PushNotifications  *bool `json:"push_notifications" example:"true"`   // Pengaturan persetujuan push notifikasi
}

type ChangePasswordRequest struct {
	CurrentPassword string `json:"current_password" validate:"required" example:"sandiLama123"`  // Kata sandi aktif saat ini
	NewPassword     string `json:"new_password" validate:"required,min=8" example:"sandiBaru99"` // Kata sandi baru minimal 8 karakter
}

type Verify2FARequest struct {
	TempToken string `json:"temp_token" validate:"required" example:"temp_token_abcdef"` // Token login sementara sebelum verifikasi MFA
	Code      string `json:"code" validate:"required,len=6" example:"123456"`            // Kode OTP 6-digit dari Google Authenticator
}

type OTPVerificationRequest struct {
	Code string `json:"code" validate:"required,len=6" example:"654321"` // Kode verifikasi 6-digit untuk konfirmasi perubahan penting
}
