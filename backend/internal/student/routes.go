package student

import (
	"sim-sekolah/internal/auth"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

// SetupRoutes wires student dependencies and registers routes.
func SetupRoutes(api fiber.Router, db *gorm.DB) {
	repo := NewStudentRepository(db)
	svc := NewStudentService(repo)
	h := NewStudentHandler(svc)

	group := api.Group("/students")
	group.Use(middleware.Protected())

	group.Get("/", h.GetAll)
	group.Get("/school/:schoolId", h.GetBySchool)
	group.Get("/:id", h.GetByID)

	group.Post("/", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.Create)
	group.Put("/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.Update)
	group.Delete("/:id", auth.RoleMiddleware("SUPER_ADMIN"), h.Delete)

	// Nested: Data Orang Tua
	group.Post("/:id/parents", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.UpsertParent)
	group.Delete("/:id/parents/:parentId", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.DeleteParent)
}
