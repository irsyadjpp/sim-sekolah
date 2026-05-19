package auth

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB, rdb *redis.Client) {
	repo := NewAuthRepository(db, rdb)
	svc := NewAuthService(repo)
	h := NewAuthHandler(svc)

	auth := router.Group("/otentikasi")

	auth.Post("/daftar", h.Register)
	auth.Post("/masuk", h.Login)
	auth.Post("/segarkan", h.Refresh)
	auth.Post("/keluar", h.Logout)
	auth.Post("/lupa-kata-sandi", h.ForgotPassword)
	auth.Post("/atur-ulang-kata-sandi", h.ResetPassword)
	auth.Post("/verifikasi-2fa", h.Verify2FA)

	// Protected routes
	protected := auth.Group("/")
	protected.Use(middleware.Protected())
	protected.Get("/saya", h.GetMe)
	protected.Put("/saya", h.UpdateMe)
	protected.Post("/saya/foto", h.UploadPhoto)
	protected.Post("/ubah-kata-sandi", h.ChangePassword)
	protected.Post("/2fa/atur", h.Setup2FA)
	protected.Post("/2fa/aktifkan", h.Enable2FA)
	protected.Post("/2fa/nonaktifkan", h.Disable2FA)
	protected.Post("/penyamaran", h.Impersonate)
	protected.Post("/berhenti-penyamaran", h.StopImpersonation)
}
