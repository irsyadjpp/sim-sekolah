package schedule

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	repo := NewScheduleRepository(db)
	svc := NewScheduleService(repo)
	h := NewScheduleHandler(svc)

	// Routes
	router.Get("/kelas/:id/jadwal", middleware.Protected(), h.GetByClassroom)
	router.Get("/guru/:id/jadwal", middleware.Protected(), h.GetByTeacher)

	schedules := router.Group("/jadwal")
	schedules.Use(middleware.Protected())
	schedules.Post("/", h.Create)
	schedules.Delete("/:id", h.Delete)
}
