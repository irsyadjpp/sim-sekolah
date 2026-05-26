package numeracy

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewRepository(db)
	service := NewService(repo)
	handler := NewHandler(service)

	handler.RegisterRoutes(group)
}

func (h *Handler) RegisterRoutes(group fiber.Router) {
	// Indicator routes
	indicators := group.Group("/numeracy/indicators")
	indicators.Post("/", h.CreateIndicator)
	indicators.Get("/:id", h.GetIndicatorByID)
	indicators.Get("/", h.GetIndicators)
	indicators.Put("/:id", h.UpdateIndicator)
	indicators.Delete("/:id", h.DeleteIndicator)

	// Assessment routes
	assessments := group.Group("/numeracy/assessments")
	assessments.Post("/", h.CreateAssessment)
	assessments.Post("/bulk", h.BulkCreateAssessments)
	assessments.Get("/:id", h.GetAssessmentByID)
	assessments.Get("/", h.GetAssessments)
	assessments.Put("/:id", h.UpdateAssessment)
	assessments.Put("/bulk", h.BulkUpdateAssessments)
	assessments.Delete("/:id", h.DeleteAssessment)

	// Growth routes
	growths := group.Group("/numeracy/growths")
	growths.Post("/", h.CreateGrowth)
	growths.Get("/:id", h.GetGrowthByID)
	growths.Get("/student/:student_id/period/:period", h.GetGrowthByStudentAndPeriod)
	growths.Get("/", h.GetGrowths)
	growths.Put("/:id", h.UpdateGrowth)
	growths.Delete("/:id", h.DeleteGrowth)
	growths.Post("/student/:student_id/calculate", h.CalculateStudentGrowth)

	// Intervention routes
	interventions := group.Group("/numeracy/interventions")
	interventions.Post("/", h.CreateIntervention)
	interventions.Get("/:id", h.GetInterventionByID)
	interventions.Get("/", h.GetInterventions)
	interventions.Put("/:id", h.UpdateIntervention)
	interventions.Delete("/:id", h.DeleteIntervention)

	// Analytics routes
	analytics := group.Group("/numeracy/analytics")
	analytics.Get("/", h.GetNumeracyAnalytics)

	// Report routes
	reports := group.Group("/numeracy/reports")
	reports.Get("/student/:student_id", h.ExportStudentNumeracyReport)
}
