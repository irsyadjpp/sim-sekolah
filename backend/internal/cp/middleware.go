package cp

import (
	"github.com/gofiber/fiber/v2"

	"sim-sekolah/internal/auth"
)

func AdminOrTeacherOnly() fiber.Handler {

	return auth.RoleMiddleware(
		"SUPER_ADMIN",
		"ADMIN_SEKOLAH",
		"GURU",
	)
}
