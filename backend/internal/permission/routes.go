package permission

import (
	"sim-sekolah/internal/auth"

	"github.com/gofiber/fiber/v2"
)

func RegisterRoutes(router fiber.Router, h *PermissionHandler) {
	// Membatasi akses eksklusif hanya untuk admin sekolah / operator utama
	group := router.Group("/permissions", auth.Protected(), auth.RoleMiddleware("SUPER_ADMIN", "ADMIN"))

	group.Get("/", h.GetAll)
	group.Get("/:id", h.GetByID)
	group.Post("/", h.Create)
	group.Delete("/:id", h.Delete)

	group.Get("/roles/:role_id", h.GetPermissionsByRoleID)
	group.Post("/roles/:role_id", h.AssignPermissionsToRole)
}
