package profile_dimension

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewProfileDimensionRepository(db)
	svc := NewProfileDimensionService(repo)
	h := NewProfileDimensionHandler(svc)

	group := router.Group("/dimensi-profil")
	group.Use(middleware.Protected())

	group.Get("/", h.GetAll)
	group.Get("/:id", h.GetByID)
	group.Post("/", h.Create)
	group.Put("/:id", h.Update)
	group.Delete("/:id", h.Delete)
}
