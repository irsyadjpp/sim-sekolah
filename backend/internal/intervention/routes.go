package intervention

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewInterventionRepository(db)
	service := NewInterventionService(repo)
	handler := NewInterventionHandler(service)

	registerInterventionRoutes(group, handler)
}

func registerInterventionRoutes(router fiber.Router, handler *InterventionHandler) {
	// RemedialProgram routes
	remedial := router.Group("/intervention/remedial")
	{
		remedial.Get("", handler.GetAllRemedialPrograms)
		remedial.Get("/:id", handler.GetRemedialProgramByID)
		remedial.Post("", handler.CreateRemedialProgram)
		remedial.Put("/:id", handler.UpdateRemedialProgram)
		remedial.Delete("/:id", handler.DeleteRemedialProgram)
	}

	// EnrichmentProgram routes
	enrichment := router.Group("/intervention/enrichment")
	{
		enrichment.Get("", handler.GetAllEnrichmentPrograms)
		enrichment.Get("/:id", handler.GetEnrichmentProgramByID)
		enrichment.Post("", handler.CreateEnrichmentProgram)
		enrichment.Put("/:id", handler.UpdateEnrichmentProgram)
		enrichment.Delete("/:id", handler.DeleteEnrichmentProgram)
	}

	// StudentAssignment routes
	assignments := router.Group("/intervention/assignments")
	{
		assignments.Get("", handler.GetAssignmentsByStudent) // Default to current student from JWT
		assignments.Get("/:id", handler.GetStudentAssignmentByID)
		assignments.Get("/student/:studentId", handler.GetAssignmentsByStudent)
		assignments.Post("", handler.CreateStudentAssignment)
		assignments.Put("/:id", handler.UpdateStudentAssignment)
		assignments.Delete("/:id", handler.DeleteStudentAssignment)
	}

	// Summary routes
	assignments.Get("/summary", handler.GetInterventionSummary)
}
