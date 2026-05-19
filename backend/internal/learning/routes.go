package learning

import (
	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
	"sim-sekolah/internal/ai"
	"sim-sekolah/pkg/middleware"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	aiRepo := ai.NewAIRepository()
	aiSvc := ai.NewAIService(aiRepo)
	svc := NewLearningService(db, aiSvc)
	h := NewLearningHandler(svc)

	learning := router.Group("/pembelajaran")
	learning.Use(middleware.Protected())

	learning.Get("/atp", h.GetAllATP)
	learning.Get("/atp/:id", h.GetATPByID)
	learning.Post("/atp", h.SaveATP)
	learning.Delete("/atp/:id", h.DeleteATP)

	learning.Post("/atp/:atpId/buat-modul", h.GenerateModule)
	learning.Post("/modul", h.SaveModule)
}
