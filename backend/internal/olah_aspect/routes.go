package olah_aspect

import (
	"sim-sekolah/internal/auth"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

// SetupRoutes sets up the routes for olah aspect endpoints
func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewOlahAspectRepository(db)
	svc := NewOlahAspectService(repo)
	h := NewOlahAspectHandler(svc)

	// Olah Aspect routes
	router.Get("/olah-aspects", middleware.Protected(), h.GetAll)
	router.Get("/olah-aspects/:id", middleware.Protected(), h.GetByID)
	router.Get("/olah-aspects/code/:code", middleware.Protected(), h.GetByCode)
	router.Post("/olah-aspects", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), middleware.Protected(), h.Create)
	router.Put("/olah-aspects/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), middleware.Protected(), h.Update)
	router.Delete("/olah-aspects/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), middleware.Protected(), h.Delete)
}
