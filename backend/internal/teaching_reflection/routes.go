package teaching_reflection

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewTeachingReflectionRepository(db)
	service := NewTeachingReflectionService(repo)
	handler := NewTeachingReflectionHandler(service)

	registerTeachingReflectionRoutes(group, handler)
}

func registerTeachingReflectionRoutes(router fiber.Router, handler *TeachingReflectionHandler) {
	// TeachingReflection routes
	reflections := router.Group("/teaching-reflection")
	{
		reflections.Get("", handler.GetReflectionsByTeacher) // Default to current teacher from JWT
		reflections.Get("/:id", handler.GetReflectionByID)
		reflections.Get("/teacher/:teacherId", handler.GetReflectionsByTeacher)
		reflections.Get("/teacher/:teacherId/summary", handler.GetReflectionSummary)
		reflections.Post("", handler.CreateReflection)
		reflections.Put("/:id", handler.UpdateReflection)
		reflections.Delete("/:id", handler.DeleteReflection)
	}
}
