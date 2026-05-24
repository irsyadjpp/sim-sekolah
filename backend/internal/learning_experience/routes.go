package learning_experience

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewLearningExperienceRepository(db)
	service := NewLearningExperienceService(repo)
	handler := NewLearningExperienceHandler(service)

	registerLearningExperienceRoutes(group, handler)
}

func registerLearningExperienceRoutes(router fiber.Router, handler *LearningExperienceHandler) {
	// Learning Experience CRUD routes
	experiences := router.Group("/learning-experiences")
	{
		experiences.Post("", handler.CreateLearningExperience)
		experiences.Get("", handler.GetAllLearningExperiences)
		experiences.Get("/active", handler.GetActiveLearningExperiences)
		experiences.Get("/:id", handler.GetLearningExperienceByID)
		experiences.Put("/:id", handler.UpdateLearningExperience)
		experiences.Delete("/:id", handler.DeleteLearningExperience)

		// Activity Experience Mapping routes
		experiences.Post("/link-activity", handler.LinkActivityToExperience)
		experiences.Delete("/link-activity/:activityId", handler.UnlinkActivityFromExperience)
		experiences.Get("/by-activity/:activityId", handler.GetExperienceByActivityID)

		// Student Progression routes
		experiences.Post("/student-progression", handler.CreateStudentProgression)
		experiences.Get("/student-progression/:id", handler.GetStudentProgressionByID)
		experiences.Put("/student-progression/:id", handler.UpdateStudentProgression)
		experiences.Delete("/student-progression/:id", handler.DeleteStudentProgression)
	}

	// Student-specific progression routes
	students := router.Group("/students")
	{
		students.Get("/:studentId/experience-progression", handler.GetStudentProgressions)
		students.Get("/:studentId/subjects/:subjectId/progression-summary", handler.GetStudentProgressionSummary)
	}
}
