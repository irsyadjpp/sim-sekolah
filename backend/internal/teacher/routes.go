package teacher

import (
	"sim-sekolah/internal/auth"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

// SetupRoutes wires teacher dependencies and registers routes.
func SetupRoutes(api fiber.Router, db *gorm.DB) {
	repo := NewTeacherRepository(db)
	svc := NewTeacherService(repo, db)
	h := NewTeacherHandler(svc)

	group := api.Group("/guru")
	group.Use(middleware.Protected())

	group.Get("/", h.GetAll)
	group.Get("/sekolah/:schoolId", h.GetBySchool)
	group.Get("/:id", h.GetByID)

	group.Post("/", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.Create)
	group.Put("/:id", auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"), h.Update)
	group.Delete("/:id", auth.RoleMiddleware("SUPER_ADMIN"), h.Delete)
}
