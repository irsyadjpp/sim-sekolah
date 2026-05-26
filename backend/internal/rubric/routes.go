package rubric

import (
	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")

	repo := NewRepository(db)
	service := NewService(repo)
	handler := NewHandler(service)

	handler.RegisterRoutes(group)
}
