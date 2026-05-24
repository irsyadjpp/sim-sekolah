package play_based_learning

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewPlayBasedLearningRepository(db)
	service := NewPlayBasedLearningService(repo)
	handler := NewPlayBasedLearningHandler(service)

	registerPlayBasedLearningRoutes(group, handler)
}

func registerPlayBasedLearningRoutes(router fiber.Router, handler *PlayBasedLearningHandler) {
	// Play Activity Type routes
	activityTypes := router.Group("/play-based-activity-types")
	{
		activityTypes.Post("", handler.CreatePlayActivityType)
		activityTypes.Get("", handler.GetAllPlayActivityTypes)
		activityTypes.Get("/active", handler.GetActivePlayActivityTypes)
		activityTypes.Get("/phase/:phaseId", handler.GetPlayActivityTypesByPhase)
		activityTypes.Get("/domain/:domain", handler.GetPlayActivityTypesByDomain)
		activityTypes.Get("/:id", handler.GetPlayActivityTypeByID)
		activityTypes.Put("/:id", handler.UpdatePlayActivityType)
		activityTypes.Delete("/:id", handler.DeletePlayActivityType)
	}

	// Play Based Activity routes
	modules := router.Group("/teaching-modules/:moduleId")
	{
		modules.Post("/play-based-activities", handler.CreatePlayBasedActivity)
		modules.Get("/play-based-activities", handler.GetPlayBasedActivitiesByModuleID)
		modules.Get("/play-based-activities/summary", handler.GetPlayBasedLearningSummary)
		modules.Delete("/play-based-activities", handler.DeletePlayBasedActivitiesByModuleID)
	}

	// Play Based Activity individual routes
	activities := router.Group("/play-based-activities")
	{
		activities.Get("/:id", handler.GetPlayBasedActivityByID)
		activities.Put("/:id", handler.UpdatePlayBasedActivity)
		activities.Delete("/:id", handler.DeletePlayBasedActivity)
	}

	// Play Observation routes
	students := router.Group("/students/:studentId")
	{
		students.Get("/play-observations", handler.GetPlayObservationsByStudentID)
		students.Get("/play-observations/summary", handler.GetStudentPlaySummary)
		students.Get("/play-based-activities/:activityId/observations", handler.GetPlayObservationsByStudentAndActivity)
		students.Post("/play-observations", handler.CreatePlayObservation)
	}

	// Play Observation individual routes
	observations := router.Group("/play-observations")
	{
		observations.Get("/:id", handler.GetPlayObservationByID)
		observations.Put("/:id", handler.UpdatePlayObservation)
		observations.Delete("/:id", handler.DeletePlayObservation)
	}

	// Play Observation by activity
	activityObs := router.Group("/play-based-activities/:activityId")
	{
		activityObs.Get("/observations", handler.GetPlayObservationsByActivityID)
	}
}
