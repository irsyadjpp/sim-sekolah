package portfolio

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
	// Portfolio routes
	portfolios := group.Group("/portfolios")
	portfolios.Post("/", h.CreatePortfolio)
	portfolios.Get("/:id", h.GetPortfolioByID)
	portfolios.Get("/", h.GetPortfolios)
	portfolios.Put("/:id", h.UpdatePortfolio)
	portfolios.Delete("/:id", h.DeletePortfolio)
	portfolios.Get("/student/:student_id", h.GetStudentPortfolios)
	portfolios.Put("/:id/publish", h.PublishPortfolio)

	// Artifact routes
	artifacts := group.Group("/portfolio-artifacts")
	artifacts.Post("/", h.CreateArtifact)
	artifacts.Get("/:id", h.GetArtifactByID)
	artifacts.Get("/", h.GetArtifacts)
	artifacts.Put("/:id", h.UpdateArtifact)
	artifacts.Delete("/:id", h.DeleteArtifact)
	artifacts.Get("/portfolio/:portfolio_id", h.GetPortfolioArtifacts)

	// LearningEvidence routes
	evidence := group.Group("/learning-evidence")
	evidence.Post("/", h.CreateLearningEvidence)
	evidence.Get("/:id", h.GetLearningEvidenceByID)
	evidence.Get("/", h.GetLearningEvidence)
	evidence.Put("/:id", h.UpdateLearningEvidence)
	evidence.Delete("/:id", h.DeleteLearningEvidence)
	evidence.Get("/student/:student_id", h.GetStudentLearningEvidence)
	evidence.Put("/:id/validate", h.ValidateEvidence)

	// PortfolioReview routes
	reviews := group.Group("/portfolio-reviews")
	reviews.Post("/", h.CreateReview)
	reviews.Get("/:id", h.GetReviewByID)
	reviews.Get("/", h.GetReviews)
	reviews.Put("/:id", h.UpdateReview)
	reviews.Delete("/:id", h.DeleteReview)
	reviews.Get("/portfolio/:portfolio_id", h.GetPortfolioReviews)

	// Analytics routes
	analytics := group.Group("/portfolio-analytics")
	analytics.Get("/", h.GetPortfolioAnalytics)

	// Report routes
	reports := group.Group("/portfolio-reports")
	reports.Get("/student/:student_id", h.ExportStudentPortfolioReport)
}
