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
	router.Get("/classrooms/:id/schedules", middleware.Protected(), h.GetByClassroom)
	router.Get("/teachers/:id/schedules", middleware.Protected(), h.GetByTeacher)

	schedules := router.Group("/schedules")
	schedules.Use(middleware.Protected())
	schedules.Post("/", h.Create)
	schedules.Delete("/:id", h.Delete)
}
