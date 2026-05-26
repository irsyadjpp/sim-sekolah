package supervision

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewSupervisionRepository(db)
	service := NewSupervisionService(repo)
	handler := NewSupervisionHandler(service)

	registerSupervisionRoutes(group, handler)
}

func registerSupervisionRoutes(router fiber.Router, handler *SupervisionHandler) {
	// SupervisionCycle routes
	cycles := router.Group("/supervision/cycles")
	{
		cycles.Get("", handler.GetAllCycles)
		cycles.Get("/active", handler.GetActiveCycles)
		cycles.Get("/summary", handler.GetSupervisionSummary)
		cycles.Get("/:id", handler.GetCycleByID)
		cycles.Get("/school/:schoolId", handler.GetCyclesBySchool)
		cycles.Get("/academic-year/:academicYearId", handler.GetCyclesByAcademicYear)
		cycles.Post("", handler.CreateCycle)
		cycles.Put("/:id", handler.UpdateCycle)
		cycles.Delete("/:id", handler.DeleteCycle)
	}

	// TeacherObservation routes
	observations := router.Group("/supervision/observations")
	{
		observations.Get("", handler.GetAllObservations)
		observations.Get("/:id", handler.GetObservationByID)
		observations.Get("/teacher/:teacherId", handler.GetObservationsByTeacher)
		observations.Get("/observer/:observerId", handler.GetObservationsByObserver)
		observations.Get("/cycle/:cycleId", handler.GetObservationsByCycle)
		observations.Get("/status/:status", handler.GetObservationsByStatus)
		observations.Post("", handler.CreateObservation)
		observations.Put("/:id", handler.UpdateObservation)
		observations.Delete("/:id", handler.DeleteObservation)
	}

	// SupervisionFeedback routes
	feedbacks := router.Group("/supervision/feedbacks")
	{
		feedbacks.Get("", handler.GetAllFeedback)
		feedbacks.Get("/:id", handler.GetFeedbackByID)
		feedbacks.Get("/teacher/:teacherId", handler.GetFeedbackByTeacher)
		feedbacks.Get("/observation/:observationId", handler.GetFeedbackByObservation)
		feedbacks.Post("", handler.CreateFeedback)
		feedbacks.Put("/:id", handler.UpdateFeedback)
		feedbacks.Delete("/:id", handler.DeleteFeedback)
	}

	// SupervisionAnalytics routes
	analytics := router.Group("/supervision/analytics")
	{
		analytics.Get("/school/:schoolId", handler.GetAnalyticsBySchool)
		analytics.Get("/academic-year/:academicYearId", handler.GetAnalyticsByAcademicYear)
		analytics.Get("/school/:schoolId/latest", handler.GetLatestAnalytics)
		analytics.Post("/generate/:schoolId/:academicYearId", handler.GenerateAnalytics)
	}
}
