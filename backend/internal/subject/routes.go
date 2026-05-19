package subject

import (
	"sim-sekolah/internal/auth"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

// SetupRoutes wires subject dependencies and registers routes.
func SetupRoutes(api fiber.Router, db *gorm.DB) {
	subRepo := NewSubjectRepository(db)
	elemRepo := NewSubjectElementRepository(db)
	svc := NewSubjectService(subRepo, elemRepo)
	h := NewSubjectHandler(svc)

	group := api.Group("/mata-pelajaran")
	group.Use(middleware.Protected())

	group.Get("/", h.GetAll)
	group.Get("/:id", h.GetByID)

	group.Post("/", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.Create)
	group.Put("/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.Update)
	group.Delete("/:id", auth.RoleMiddleware("SUPER_ADMIN"), h.Delete)

	// Nested routes for Elements
	group.Get("/:subjectId/elemen", h.GetAllElements)
	group.Post("/:subjectId/elemen", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.CreateElement)
	group.Put("/:subjectId/elemen/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.UpdateElement)
	group.Delete("/:subjectId/elemen/:id", auth.RoleMiddleware("SUPER_ADMIN"), h.DeleteElement)
}
