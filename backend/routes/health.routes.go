package routes

import "github.com/gofiber/fiber/v2"

func SetupHealthRoutes(api fiber.Router) {
	api.Get("/health", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"success": true,
			"message": "API Running",
		})
	})
}
