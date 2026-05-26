package document_repository

import (
	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

// SetupRoutes sets up document repository routes
func SetupRoutes(app fiber.Router, db *gorm.DB) {
	repo := NewRepository(db)
	service := NewService(repo)
	handler := NewHandler(service)

	documents := app.Group("/api/documents")
	{
		// Document CRUD operations
		documents.Post("/", handler.CreateDocument)
		documents.Get("/", handler.GetDocuments)
		documents.Get("/:id", handler.GetDocumentByID)
		documents.Put("/:id", handler.UpdateDocument)
		documents.Delete("/:id", handler.DeleteDocument)

		// Document versions
		documents.Post("/:id/versions", handler.CreateDocumentVersion)
		documents.Get("/:id/versions", handler.GetDocumentVersions)

		// Document approval workflow
		documents.Post("/:id/submit-approval", handler.SubmitForApproval)
		documents.Post("/approvals/:id/approve", handler.ApproveDocument)
		documents.Post("/approvals/:id/reject", handler.RejectDocument)

		// Document sharing
		documents.Post("/:id/share", handler.ShareDocument)
		documents.Get("/:id/shares", handler.GetDocumentShares)

		// Document operations
		documents.Get("/:id/download", handler.DownloadDocument)
		documents.Post("/search", handler.SearchDocuments)
		documents.Get("/statistics", handler.GetStatistics)
		documents.Get("/expiring", handler.GetExpiringDocuments)
		documents.Get("/pending-approvals", handler.GetPendingApprovals)
	}

	// Categories and tags
	categories := app.Group("/api/documents/categories")
	{
		categories.Post("/", handler.CreateCategory)
		categories.Get("/", handler.GetCategories)
	}

	tags := app.Group("/api/documents/tags")
	{
		tags.Post("/", handler.CreateTag)
		tags.Get("/", handler.GetTags)
	}
}
