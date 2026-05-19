package ai

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewAIRepository()
	svc := NewAIService(repo)
	h := NewAIHandler(svc)

	group := router.Group("/ai")
	group.Use(middleware.Protected())

	group.Post("/generate-narrative", h.GenerateNarrative)
}
