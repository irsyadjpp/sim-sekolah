package foundational_skills

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewRepository(db)
	service := NewService(repo)
	handler := NewHandler(service)

	handler.RegisterRoutes(group)
}
