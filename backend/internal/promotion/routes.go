package promotion

import (
	"sim-sekolah/internal/auth"

	"github.com/gofiber/fiber/v2"
)

func RegisterRoutes(router fiber.Router, h *PromotionHandler) {
	group := router.Group("/academic", auth.Protected(), auth.RoleMiddleware("SUPER_ADMIN", "ADMIN"))

	group.Post("/promotion", h.Promote)
	group.Post("/graduation", h.Graduate)
}
