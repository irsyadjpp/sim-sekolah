package learning_principle

import (
	"sim-sekolah/internal/auth"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

// SetupRoutes sets up the routes for learning principle endpoints
func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewLearningPrincipleRepository(db)
	svc := NewLearningPrincipleService(repo)
	h := NewLearningPrincipleHandler(svc)

	// Learning Principle routes
	router.Get("/learning-principles", middleware.Protected(), h.GetAll)
	router.Get("/learning-principles/:id", middleware.Protected(), h.GetByID)
	router.Get("/learning-principles/code/:code", middleware.Protected(), h.GetByCode)
	router.Post("/learning-principles", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), middleware.Protected(), h.Create)
	router.Put("/learning-principles/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), middleware.Protected(), h.Update)
	router.Delete("/learning-principles/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), middleware.Protected(), h.Delete)
}
