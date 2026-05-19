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

	auth := router.Group("/auth")

	auth.Post("/register", h.Register)
	auth.Post("/login", h.Login)
	auth.Post("/refresh", h.Refresh)
	auth.Post("/logout", h.Logout)
	auth.Post("/forgot-password", h.ForgotPassword)
	auth.Post("/reset-password", h.ResetPassword)
	auth.Post("/verify-2fa", h.Verify2FA)

	// Protected routes
	protected := auth.Group("/")
	protected.Use(middleware.Protected())
	protected.Get("/me", h.GetMe)
	protected.Put("/me", h.UpdateMe)
	protected.Post("/me/photo", h.UploadPhoto)
	protected.Post("/change-password", h.ChangePassword)
	protected.Post("/2fa/setup", h.Setup2FA)
	protected.Post("/2fa/enable", h.Enable2FA)
	protected.Post("/2fa/disable", h.Disable2FA)
	protected.Post("/impersonate", h.Impersonate)
	protected.Post("/stop-impersonation", h.StopImpersonation)
}
