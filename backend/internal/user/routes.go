package user

import (
	"sim-sekolah/internal/auth"
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	repo := NewUserRepository(db)
	svc := NewUserService(repo)
	h := NewUserHandler(svc)

	// Fitur ini murni untuk ADMIN
	group := api.Group("/pengguna")
	group.Use(middleware.Protected())
	group.Use(auth.RoleMiddleware("SUPER_ADMIN", "ADMIN_SEKOLAH"))

	group.Get("/", h.GetAll)
	group.Get("/peran", h.GetAllRoles)
	group.Get("/:id", h.GetByID)
	group.Patch("/:id/status", h.UpdateStatus)
	group.Put("/:id/peran", h.AssignRoles)
	group.Post("/:id/atur-ulang-kata-sandi", h.ResetPassword)
}
