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

	group := router.Group("/kecerdasan-buatan")
	group.Use(middleware.Protected())

	group.Post("/buat-narasi", h.GenerateNarrative)
}
