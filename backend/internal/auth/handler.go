package auth

import (
	"context"
	"strings"
	"time"

	"sim-sekolah/internal/common"
	"sim-sekolah/internal/system"

	"github.com/gofiber/fiber/v2"
)

type AuthHandler struct {
	svc AuthService
}

func NewAuthHandler(svc AuthService) *AuthHandler {
	return &AuthHandler{svc: svc}
}

// RegisterHandler godoc
// @Summary Register
// @Description Endpoint untuk registrasi guru/staf secara mandiri. Default role: GURU
// @Tags Auth
// @Accept json
// @Produce json
// @Param request body RegisterRequest true "Register Request"
// @Success 201 {object} common.Response
// @Router /auth/register [post]
func (h *AuthHandler) Register(c *fiber.Ctx) error {
	var req RegisterRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	if err := h.svc.Register(c.UserContext(), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Pendaftaran gagal", err)
	}

	return common.Created(c, "Pendaftaran berhasil", nil)
}

// LoginHandler godoc
// @Summary Login
// @Tags Auth
// @Accept json
// @Produce json
// @Param request body LoginRequest true "Login Request"
// @Success 200 {object} common.Response
// @Router /auth/login [post]
func (h *AuthHandler) Login(c *fiber.Ctx) error {
	var req LoginRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	data, refreshToken, err := h.svc.Login(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusUnauthorized, "Gagal masuk", err)
	}

	if mfaReq, ok := data["mfa_required"].(bool); ok && mfaReq {
		return common.Success(c, "Verifikasi MFA diperlukan", data)
	}

	// Trigger Audit Log for successful login
	if system.GlobalAuditService != nil {
		if userResp, ok := data["user"].(MeResponse); ok {
			system.GlobalAuditService.LogEvent(c.UserContext(), userResp.ID, "LOGIN", "auth", userResp.ID, c.IP())
		}
	}

	c.Cookie(&fiber.Cookie{
		Name:     "refresh_token",
		Value:    refreshToken,
		Expires:  time.Now().Add(time.Hour * 24 * 30),
		HTTPOnly: true,
		Secure:   true,
		SameSite: "Lax",
	})

	return common.Success(c, "Berhasil masuk", data)
}

// RefreshHandler godoc
// @Summary Refresh Token
// @Description Memperbarui Access Token menggunakan Refresh Token dari HttpOnly Cookie
// @Tags Auth
// @Produce json
// @Success 200 {object} common.Response
// @Router /auth/refresh [post]
func (h *AuthHandler) Refresh(c *fiber.Ctx) error {
	refreshToken := c.Cookies("refresh_token")
	if refreshToken == "" {
		return common.Error(c, fiber.StatusUnauthorized, "Token penyegar tidak ditemukan", "")
	}

	data, newRefreshToken, err := h.svc.Refresh(c.UserContext(), refreshToken)
	if err != nil {
		c.Cookie(&fiber.Cookie{
			Name:     "refresh_token",
			Value:    "",
			Expires:  time.Now().Add(-1 * time.Hour),
			HTTPOnly: true,
		})
		return common.ErrorFromService(c, fiber.StatusUnauthorized, "Gagal menyegarkan token", err)
	}

	c.Cookie(&fiber.Cookie{
		Name:     "refresh_token",
		Value:    newRefreshToken,
		Expires:  time.Now().Add(time.Hour * 24 * 30),
		HTTPOnly: true,
		Secure:   true,
		SameSite: "Lax",
	})

	return common.Success(c, "Token berhasil disegarkan", data)
}

// Note: Refresh method in service needs context update too

// LogoutHandler godoc
// @Summary Logout
// @Description Menghapus Refresh Token dari database dan Cookie
// @Tags Auth
// @Produce json
// @Success 200 {object} common.Response
// @Router /auth/logout [post]
func (h *AuthHandler) Logout(c *fiber.Ctx) error {
	refreshToken := c.Cookies("refresh_token")

	// Pass access token into context so the service can blacklist it in Redis
	rawAccessToken := strings.TrimPrefix(c.Get("Authorization"), "Bearer ")
	//nolint:staticcheck // SA1029: using built-in string type as key for backward compatibility across modules
	ctx := context.WithValue(c.UserContext(), "access_token", rawAccessToken)

	if refreshToken != "" {
		_ = h.svc.Logout(ctx, refreshToken)
	}

	c.Cookie(&fiber.Cookie{
		Name:     "refresh_token",
		Value:    "",
		Expires:  time.Now().Add(-1 * time.Hour),
		HTTPOnly: true,
		Secure:   true,
		SameSite: "Lax",
	})

	return common.Success(c, "Berhasil keluar", nil)
}

// ForgotPasswordHandler godoc
// @Summary Forgot Password
// @Tags Auth
// @Accept json
// @Produce json
// @Param request body ForgotPasswordRequest true "Forgot Password Request"
// @Success 200 {object} common.Response
// @Router /auth/forgot-password [post]
func (h *AuthHandler) ForgotPassword(c *fiber.Ctx) error {
	var req ForgotPasswordRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	if err := h.svc.ForgotPassword(c.UserContext(), req); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memproses permintaan", err)
	}

	return common.Success(c, "Jika email Anda terdaftar, Anda akan menerima tautan pemulihan", nil)
}

// ResetPasswordHandler godoc
// @Summary Reset Password
// @Tags Auth
// @Accept json
// @Produce json
// @Param request body ResetPasswordRequest true "Reset Password Request"
// @Success 200 {object} common.Response
// @Router /auth/reset-password [post]
func (h *AuthHandler) ResetPassword(c *fiber.Ctx) error {
	var req ResetPasswordRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	if err := h.svc.ResetPassword(c.UserContext(), "", req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Gagal mengatur ulang kata sandi", err)
	}

	return common.Success(c, "Kata sandi berhasil diatur ulang", nil)
}

// GetMeHandler godoc
// @Summary Get Current User Profile
// @Tags Auth
// @Produce json
// @Security BearerAuth
// @Success 200 {object} common.Response
// @Router /auth/me [get]
func (h *AuthHandler) GetMe(c *fiber.Ctx) error {
	userID, ok := c.Locals("user_id").(string)
	if !ok {
		return common.Error(c, fiber.StatusUnauthorized, "Konteks pengguna hilang", "")
	}

	resp, err := h.svc.GetMe(c.UserContext(), userID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusNotFound, "Pengguna tidak ditemukan", err)
	}

	return common.Success(c, "Profil berhasil diambil", resp)
}

// UpdateMeHandler godoc
// @Summary Update Current User Profile
// @Tags Auth
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body UpdateMeRequest true "Update Request"
// @Success 200 {object} common.Response
// @Router /auth/me [put]
func (h *AuthHandler) UpdateMe(c *fiber.Ctx) error {
	userID, ok := c.Locals("user_id").(string)
	if !ok {
		return common.Error(c, fiber.StatusUnauthorized, "Konteks pengguna hilang", "")
	}

	var req UpdateMeRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	if err := h.svc.UpdateMe(c.UserContext(), userID, req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Gagal memperbarui profil", err)
	}

	return common.Success(c, "Profil berhasil diperbarui", nil)
}

// ChangePasswordHandler godoc
// @Summary Change Password
// @Tags Auth
// @Accept json
// @Produce json
// @Security BearerAuth
// @Param request body ChangePasswordRequest true "Change Password Request"
// @Success 200 {object} common.Response
// @Router /auth/change-password [post]
func (h *AuthHandler) ChangePassword(c *fiber.Ctx) error {
	userID, ok := c.Locals("user_id").(string)
	if !ok {
		return common.Error(c, fiber.StatusUnauthorized, "Konteks pengguna hilang", "")
	}

	var req ChangePasswordRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	if err := common.Validate.Struct(req); err != nil {
		return common.Error(c, fiber.StatusBadRequest, "Validasi gagal", common.MapValidatorError(err))
	}

	if err := h.svc.ChangePassword(c.UserContext(), userID, req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Gagal memperbarui kata sandi", err)
	}

	return common.Success(c, "Kata sandi berhasil diperbarui", nil)
}

// UploadPhotoHandler godoc
// @Summary Upload Profile Photo
// @Tags Auth
// @Accept multipart/form-data
// @Produce json
// @Security BearerAuth
// @Param file formData file true "Profile Photo"
// @Success 200 {object} common.Response
// @Router /auth/me/photo [post]
func (h *AuthHandler) UploadPhoto(c *fiber.Ctx) error {
	userID, ok := c.Locals("user_id").(string)
	if !ok {
		return common.Error(c, fiber.StatusUnauthorized, "Konteks pengguna hilang", "")
	}

	file, err := c.FormFile("file")
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "File tidak ditemukan", err)
	}

	photoURL, err := h.svc.UploadPhoto(c.UserContext(), userID, file)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal mengunggah foto", err)
	}

	return common.Success(c, "Foto berhasil diunggah", fiber.Map{"photo_url": photoURL})
}

func (h *AuthHandler) Verify2FA(c *fiber.Ctx) error {
	var req Verify2FARequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	data, refreshToken, err := h.svc.Verify2FA(c.UserContext(), req)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusUnauthorized, "Verifikasi 2FA gagal", err)
	}

	// Trigger Audit Log for successful MFA login
	if system.GlobalAuditService != nil {
		if userResp, ok := data["user"].(MeResponse); ok {
			system.GlobalAuditService.LogEvent(c.UserContext(), userResp.ID, "LOGIN", "auth", userResp.ID, c.IP())
		}
	}

	c.Cookie(&fiber.Cookie{
		Name:     "refresh_token",
		Value:    refreshToken,
		Expires:  time.Now().Add(time.Hour * 24 * 30),
		HTTPOnly: true,
		Secure:   true,
		SameSite: "Lax",
	})

	return common.Success(c, "Berhasil masuk", data)
}

func (h *AuthHandler) Setup2FA(c *fiber.Ctx) error {
	userID, ok := c.Locals("user_id").(string)
	if !ok {
		return common.Error(c, fiber.StatusUnauthorized, "Konteks pengguna hilang", "")
	}

	data, err := h.svc.Setup2FA(c.UserContext(), userID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal memulai pengaturan 2FA", err)
	}

	return common.Success(c, "Pengaturan 2FA dimulai", data)
}

func (h *AuthHandler) Enable2FA(c *fiber.Ctx) error {
	userID, ok := c.Locals("user_id").(string)
	if !ok {
		return common.Error(c, fiber.StatusUnauthorized, "Konteks pengguna hilang", "")
	}

	var req OTPVerificationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	if err := h.svc.Enable2FA(c.UserContext(), userID, req.Code); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Gagal mengaktifkan 2FA", err)
	}

	// Trigger Audit Log
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "MFA_ENABLE", "security", userID, c.IP())
	}

	return common.Success(c, "2FA berhasil diaktifkan", nil)
}

func (h *AuthHandler) Disable2FA(c *fiber.Ctx) error {
	userID, ok := c.Locals("user_id").(string)
	if !ok {
		return common.Error(c, fiber.StatusUnauthorized, "Konteks pengguna hilang", "")
	}

	var req OTPVerificationRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	if err := h.svc.Disable2FA(c.UserContext(), userID, req.Code); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Gagal menonaktifkan 2FA", err)
	}

	// Trigger Audit Log
	if system.GlobalAuditService != nil {
		system.GlobalAuditService.LogEvent(c.UserContext(), userID, "MFA_DISABLE", "security", userID, c.IP())
	}

	return common.Success(c, "2FA berhasil dinonaktifkan", nil)
}

func (h *AuthHandler) Impersonate(c *fiber.Ctx) error {
	actorID, ok := c.Locals("user_id").(string)
	if !ok {
		return common.Error(c, fiber.StatusUnauthorized, "Konteks pengguna hilang", "")
	}

	var req ImpersonateRequest
	if err := c.BodyParser(&req); err != nil {
		return common.ErrorFromService(c, fiber.StatusBadRequest, "Format permintaan tidak valid", err)
	}

	if req.TargetUserID == "" {
		return common.Error(c, fiber.StatusBadRequest, "ID pengguna target wajib diisi", "")
	}

	token, err := h.svc.Impersonate(c.UserContext(), actorID, req.TargetUserID)
	if err != nil {
		return common.ErrorFromService(c, fiber.StatusForbidden, "Penyamaran ditolak", err)
	}

	// Trigger Audit Log
	if system.GlobalAuditService != nil {
		// Prepare a temporary context with impersonator_id to audit log correctly
		//nolint:staticcheck // SA1029: using built-in string type as key for backward compatibility across modules
		auditCtx := context.WithValue(c.UserContext(), "impersonator_id", actorID)
		system.GlobalAuditService.LogEvent(auditCtx, req.TargetUserID, "IMPERSONATE_START", "auth", req.TargetUserID, c.IP())
	}

	return common.Success(c, "Penyamaran berhasil dimulai", fiber.Map{
		"token": token,
	})
}

func (h *AuthHandler) StopImpersonation(c *fiber.Ctx) error {
	// Extract the actual token from the request Authorization header
	authHeader := c.Get("Authorization")
	tokenString := strings.Replace(authHeader, "Bearer ", "", 1)

	// Verify we are actually impersonating
	impersonatorID, isImpersonating := c.Locals("impersonator_id").(string)
	targetUserID, ok := c.Locals("user_id").(string)

	if !isImpersonating || !ok {
		return common.Error(c, fiber.StatusBadRequest, "Tidak ada sesi penyamaran aktif yang ditemukan", "")
	}

	if err := h.svc.StopImpersonation(c.UserContext(), tokenString); err != nil {
		return common.ErrorFromService(c, fiber.StatusInternalServerError, "Gagal menghentikan penyamaran", err)
	}

	// Trigger Audit Log
	if system.GlobalAuditService != nil {
		//nolint:staticcheck // SA1029: using built-in string type as key for backward compatibility across modules
		auditCtx := context.WithValue(c.UserContext(), "impersonator_id", impersonatorID)
		system.GlobalAuditService.LogEvent(auditCtx, targetUserID, "IMPERSONATE_STOP", "auth", targetUserID, c.IP())
	}

	return common.Success(c, "Penyamaran berhasil dihentikan", nil)
}
