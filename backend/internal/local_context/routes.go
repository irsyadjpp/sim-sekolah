package local_context

import (
	"sim-sekolah/internal/auth"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewLocalContextRepository(db)
	svc := NewLocalContextService(repo)
	h := NewLocalContextHandler(svc)

	group := router.Group("/konteks-lokal")

	// Semua butuh login
	group.Use(middleware.Protected())

	// Categories
	group.Get("/kategori", h.GetAllCategories)

	// Contexts
	group.Get("/", h.GetAllContexts)
	group.Post("/", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH", "GURU"), h.CreateContext)
	group.Put("/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH", "GURU"), h.UpdateContext)
	group.Delete("/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH", "GURU"), h.DeleteContext)
}
