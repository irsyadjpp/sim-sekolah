package promotion

import (
	"sim-sekolah/internal/auth"

	"github.com/gofiber/fiber/v2"
)

func RegisterRoutes(router fiber.Router, h *PromotionHandler) {
	group := router.Group("/akademik", auth.Protected(), auth.RoleMiddleware("SUPER_ADMIN", "ADMIN"))

	group.Post("/kenaikan-kelas", h.Promote)
	group.Post("/kelulusan", h.Graduate)
}
