package character_intervention

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewCharacterInterventionRepository(db)
	service := NewCharacterInterventionService(repo)
	handler := NewCharacterInterventionHandler(service)

	registerCharacterInterventionRoutes(group, handler)
}

func registerCharacterInterventionRoutes(router fiber.Router, handler *CharacterInterventionHandler) {
	// CharacterIntervention routes
	interventions := router.Group("/character-interventions")
	{
		interventions.Get("", handler.GetAll)
		interventions.Get("/active", handler.GetActive)
		interventions.Get("/summary", handler.GetInterventionSummary)
		interventions.Get("/:id", handler.GetByID)
		interventions.Get("/dimension/:dimension", handler.GetByDimension)
		interventions.Get("/age-group/:ageGroup", handler.GetByAgeGroup)
		interventions.Post("", handler.Create)
		interventions.Put("/:id", handler.Update)
		interventions.Delete("/:id", handler.Delete)
	}

	// StudentCharacterIntervention routes
	studentInterventions := router.Group("/student-interventions")
	{
		studentInterventions.Get("", handler.GetAllStudentInterventions)
		studentInterventions.Get("/active", handler.GetActiveStudentInterventions)
		studentInterventions.Get("/status/:status", handler.GetStudentInterventionsByStatus)
		studentInterventions.Get("/:id", handler.GetStudentInterventionByID)
		studentInterventions.Post("", handler.CreateStudentIntervention)
		studentInterventions.Put("/:id", handler.UpdateStudentIntervention)
		studentInterventions.Delete("/:id", handler.DeleteStudentIntervention)
	}

	// Student-specific intervention routes
	students := router.Group("/students/:studentId")
	{
		students.Get("/interventions", handler.GetStudentInterventionsByStudent)
		students.Get("/recommendations", handler.GetRecommendationsByStudent)
		students.Get("/milestones", handler.GetMilestonesByStudent)
	}

	// Teacher-specific intervention routes
	teachers := router.Group("/teachers/:teacherId")
	{
		teachers.Get("/student-interventions", handler.GetStudentInterventionsByTeacher)
	}

	// CharacterInterventionProgress routes
	progress := router.Group("/intervention-progress")
	{
		progress.Get("", handler.GetAllProgress)
		progress.Get("/:id", handler.GetProgressByID)
		progress.Post("", handler.CreateProgress)
		progress.Put("/:id", handler.UpdateProgress)
		progress.Delete("/:id", handler.DeleteProgress)
	}

	// Assignment-specific progress routes
	assignments := router.Group("/student-interventions/:assignmentId")
	{
		assignments.Get("/progress", handler.GetProgressByAssignment)
	}

	// Observer-specific progress routes
	observers := router.Group("/observers/:observerId")
	{
		observers.Get("/progress", handler.GetProgressByObserver)
	}

	// InterventionRecommendation routes
	recommendations := router.Group("/intervention-recommendations")
	{
		recommendations.Get("", handler.GetAllRecommendations)
		recommendations.Get("/pending", handler.GetPendingRecommendations)
		recommendations.Get("/:id", handler.GetRecommendationByID)
		recommendations.Post("", handler.CreateRecommendation)
		recommendations.Put("/:id", handler.UpdateRecommendation)
		recommendations.Delete("/:id", handler.DeleteRecommendation)
	}

	// CharacterMilestone routes
	milestones := router.Group("/character-milestones")
	{
		milestones.Get("", handler.GetAllMilestones)
		milestones.Get("/:id", handler.GetMilestoneByID)
		milestones.Post("", handler.CreateMilestone)
		milestones.Put("/:id", handler.UpdateMilestone)
		milestones.Delete("/:id", handler.DeleteMilestone)
	}

	// Dimension-specific milestone routes
	dimensions := router.Group("/character-milestones/dimension/:dimension")
	{
		dimensions.Get("", handler.GetMilestonesByDimension)
	}

	// Observer-specific milestone routes
	observerMilestones := router.Group("/observers/:observerId")
	{
		observerMilestones.Get("/milestones", handler.GetMilestonesByObserver)
	}
}
