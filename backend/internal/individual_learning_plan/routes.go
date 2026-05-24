package individual_learning_plan

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewILPRepository(db)
	service := NewILPService(repo)
	handler := NewILPHandler(service)

	registerILPRoutes(group, handler)
}

func registerILPRoutes(router fiber.Router, handler *ILPHandler) {
	// ILP Template routes
	templates := router.Group("/ilp/templates")
	{
		templates.Post("", handler.CreateTemplate)
		templates.Get("", handler.GetAllTemplates)
		templates.Get("/active", handler.GetActiveTemplates)
		templates.Get("/phase/:phaseId", handler.GetTemplatesByPhase)
		templates.Get("/:id", handler.GetTemplateByID)
		templates.Put("/:id", handler.UpdateTemplate)
		templates.Delete("/:id", handler.DeleteTemplate)
	}

	// Student-specific ILP routes
	students := router.Group("/students/:studentId")
	{
		students.Get("/ilp", handler.GetILPByStudentID)
		students.Get("/ilp/academic-year/:academicYearId", handler.GetILPByStudentAndAcademicYear)
		students.Post("/ilp", handler.CreateILP)
		students.Put("/ilp/:id", handler.UpdateILP)
		students.Delete("/ilp/:id", handler.DeleteILP)
	}

	// ILP routes (general)
	ilp := router.Group("/ilp")
	{
		ilp.Get("", handler.GetAllILPs)
		ilp.Get("/:id", handler.GetILPByID)
		ilp.Get("/summary", handler.GetILPSummary)
		ilp.Put("/:id", handler.UpdateILP)
		ilp.Delete("/:id", handler.DeleteILP)

		// Milestone routes
		ilp.Post("/milestones", handler.CreateMilestone)
		ilp.Get("/milestones/:id", handler.GetMilestoneByID)
		ilp.Get("/:ilpId/milestones", handler.GetMilestonesByILPID)
		ilp.Put("/milestones/:id", handler.UpdateMilestone)
		ilp.Delete("/milestones/:id", handler.DeleteMilestone)
	}
}
