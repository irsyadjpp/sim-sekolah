package document_repository

import (
	"strconv"

	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

// Handler handles HTTP requests for document repository
type Handler struct {
	service       *Service
	uploadService *UploadService
}

// NewHandler creates a new document repository handler
func NewHandler(service *Service) *Handler {
	uploadService, err := NewUploadService(service.repo)
	if err != nil {
		// Log error but continue without upload service
		uploadService = nil
	}
	return &Handler{
		service:       service,
		uploadService: uploadService,
	}
}

// CreateDocument handles POST /api/documents
func (h *Handler) CreateDocument(c *fiber.Ctx) error {
	var req DocumentRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
			"error":   err.Error(),
		})
	}

	// Get user ID from context (assuming middleware sets this)
	userID := c.Locals("user_id").(uuid.UUID)
	schoolID := c.Locals("school_id").(uuid.UUID)

	doc, err := h.service.CreateDocument(c.Context(), &req, userID, schoolID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to create document",
			"error":   err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Document created successfully",
		"data":    doc,
	})
}

// GetDocumentByID handles GET /api/documents/:id
func (h *Handler) GetDocumentByID(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid document ID",
		})
	}

	doc, err := h.service.GetDocumentByID(c.Context(), id)
	if err != nil {
		return c.Status(404).JSON(fiber.Map{
			"status":  "error",
			"message": "Document not found",
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Document retrieved successfully",
		"data":    doc,
	})
}

// GetDocuments handles GET /api/documents
func (h *Handler) GetDocuments(c *fiber.Ctx) error {
	var req DocumentListRequest
	if err := c.QueryParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request parameters",
		})
	}

	schoolID := c.Locals("school_id").(uuid.UUID)

	documents, total, err := h.service.GetDocumentsBySchoolID(c.Context(), schoolID, req)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to retrieve documents",
			"error":   err.Error(),
		})
	}

	totalPages := int(total) / req.Limit
	if int(total)%req.Limit > 0 {
		totalPages++
	}

	return c.Status(200).JSON(fiber.Map{
		"status":      "success",
		"message":     "Documents retrieved successfully",
		"data":        documents,
		"total":       total,
		"page":        req.Page,
		"limit":       req.Limit,
		"total_pages": totalPages,
	})
}

// UpdateDocument handles PUT /api/documents/:id
func (h *Handler) UpdateDocument(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid document ID",
		})
	}

	var req DocumentRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	userID := c.Locals("user_id").(uuid.UUID)

	doc, err := h.service.UpdateDocument(c.Context(), id, &req, userID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to update document",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Document updated successfully",
		"data":    doc,
	})
}

// DeleteDocument handles DELETE /api/documents/:id
func (h *Handler) DeleteDocument(c *fiber.Ctx) error {
	id, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid document ID",
		})
	}

	if err := h.service.DeleteDocument(c.Context(), id); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to delete document",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Document deleted successfully",
	})
}

// CreateDocumentVersion handles POST /api/documents/:id/versions
func (h *Handler) CreateDocumentVersion(c *fiber.Ctx) error {
	documentID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid document ID",
		})
	}

	var req DocumentVersionRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	req.DocumentID = documentID.String()
	userID := c.Locals("user_id").(uuid.UUID)

	version, err := h.service.CreateDocumentVersion(c.Context(), &req, userID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to create document version",
			"error":   err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Document version created successfully",
		"data":    version,
	})
}

// GetDocumentVersions handles GET /api/documents/:id/versions
func (h *Handler) GetDocumentVersions(c *fiber.Ctx) error {
	documentID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid document ID",
		})
	}

	versions, err := h.service.GetDocumentVersions(c.Context(), documentID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to retrieve document versions",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Document versions retrieved successfully",
		"data":    versions,
	})
}

// SubmitForApproval handles POST /api/documents/:id/submit-approval
func (h *Handler) SubmitForApproval(c *fiber.Ctx) error {
	documentID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid document ID",
		})
	}

	var req struct {
		ApproverIDs []string `json:"approver_ids" validate:"required"`
	}
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	approverUUIDs := make([]uuid.UUID, len(req.ApproverIDs))
	for i, id := range req.ApproverIDs {
		approverUUIDs[i], err = uuid.Parse(id)
		if err != nil {
			return c.Status(400).JSON(fiber.Map{
				"status":  "error",
				"message": "Invalid approver ID",
			})
		}
	}

	if err := h.service.SubmitDocumentForApproval(c.Context(), documentID, approverUUIDs); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to submit for approval",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Document submitted for approval successfully",
	})
}

// ApproveDocument handles POST /api/documents/approvals/:id/approve
func (h *Handler) ApproveDocument(c *fiber.Ctx) error {
	approvalID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid approval ID",
		})
	}

	var req struct {
		Comments string `json:"comments"`
	}
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	userID := c.Locals("user_id").(uuid.UUID)

	if err := h.service.ApproveDocument(c.Context(), approvalID, userID, req.Comments); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to approve document",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Document approved successfully",
	})
}

// RejectDocument handles POST /api/documents/approvals/:id/reject
func (h *Handler) RejectDocument(c *fiber.Ctx) error {
	approvalID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid approval ID",
		})
	}

	var req struct {
		Comments string `json:"comments"`
	}
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	userID := c.Locals("user_id").(uuid.UUID)

	if err := h.service.RejectDocument(c.Context(), approvalID, userID, req.Comments); err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to reject document",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Document rejected successfully",
	})
}

// CreateCategory handles POST /api/documents/categories
func (h *Handler) CreateCategory(c *fiber.Ctx) error {
	var req DocumentCategoryRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	category, err := h.service.CreateDocumentCategory(c.Context(), &req)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to create category",
			"error":   err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Category created successfully",
		"data":    category,
	})
}

// GetCategories handles GET /api/documents/categories
func (h *Handler) GetCategories(c *fiber.Ctx) error {
	categories, err := h.service.GetDocumentCategories(c.Context())
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to retrieve categories",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Categories retrieved successfully",
		"data":    categories,
	})
}

// CreateTag handles POST /api/documents/tags
func (h *Handler) CreateTag(c *fiber.Ctx) error {
	var req DocumentTagRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	tag, err := h.service.CreateDocumentTag(c.Context(), &req)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to create tag",
			"error":   err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Tag created successfully",
		"data":    tag,
	})
}

// GetTags handles GET /api/documents/tags
func (h *Handler) GetTags(c *fiber.Ctx) error {
	tags, err := h.service.GetDocumentTags(c.Context())
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to retrieve tags",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Tags retrieved successfully",
		"data":    tags,
	})
}

// ShareDocument handles POST /api/documents/:id/share
func (h *Handler) ShareDocument(c *fiber.Ctx) error {
	documentID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid document ID",
		})
	}

	var req DocumentShareRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	req.DocumentID = documentID.String()
	userID := c.Locals("user_id").(uuid.UUID)

	share, err := h.service.ShareDocument(c.Context(), &req, userID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to share document",
			"error":   err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Document shared successfully",
		"data":    share,
	})
}

// GetDocumentShares handles GET /api/documents/:id/shares
func (h *Handler) GetDocumentShares(c *fiber.Ctx) error {
	documentID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid document ID",
		})
	}

	shares, err := h.service.GetDocumentShares(c.Context(), documentID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to retrieve document shares",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Document shares retrieved successfully",
		"data":    shares,
	})
}

// GetStatistics handles GET /api/documents/statistics
func (h *Handler) GetStatistics(c *fiber.Ctx) error {
	schoolID := c.Locals("school_id").(uuid.UUID)

	stats, err := h.service.GetDocumentStatistics(c.Context(), schoolID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to retrieve statistics",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Statistics retrieved successfully",
		"data":    stats,
	})
}

// SearchDocuments handles POST /api/documents/search
func (h *Handler) SearchDocuments(c *fiber.Ctx) error {
	var req DocumentSearchRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
		})
	}

	schoolID := c.Locals("school_id").(uuid.UUID)

	documents, total, err := h.service.SearchDocuments(c.Context(), schoolID, &req)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to search documents",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Documents retrieved successfully",
		"data":    documents,
		"total":   total,
	})
}

// DownloadDocument handles GET /api/documents/:id/download
func (h *Handler) DownloadDocument(c *fiber.Ctx) error {
	documentID, err := uuid.Parse(c.Params("id"))
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid document ID",
		})
	}

	userID := c.Locals("user_id").(uuid.UUID)
	ipAddress := c.IP()
	userAgent := c.Get("User-Agent")

	doc, err := h.service.DownloadDocument(c.Context(), documentID, userID, ipAddress, userAgent)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to download document",
			"error":   err.Error(),
		})
	}

	// In a real implementation, you would stream the file from the storage location
	// For now, return the document URL
	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Document download initiated",
		"data": fiber.Map{
			"file_url":  doc.FileURL,
			"file_name": doc.FileName,
			"mime_type": doc.MimeType,
		},
	})
}

// GetExpiringDocuments handles GET /api/documents/expiring
func (h *Handler) GetExpiringDocuments(c *fiber.Ctx) error {
	schoolID := c.Locals("school_id").(uuid.UUID)
	daysStr := c.Query("days", "30")
	days, err := strconv.Atoi(daysStr)
	if err != nil {
		days = 30
	}

	documents, err := h.service.GetExpiringDocuments(c.Context(), schoolID, days)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to retrieve expiring documents",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Expiring documents retrieved successfully",
		"data":    documents,
	})
}

// GetPendingApprovals handles GET /api/documents/pending-approvals
func (h *Handler) GetPendingApprovals(c *fiber.Ctx) error {
	schoolID := c.Locals("school_id").(uuid.UUID)

	documents, err := h.service.GetPendingApprovalDocuments(c.Context(), schoolID)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to retrieve pending approvals",
			"error":   err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":  "success",
		"message": "Pending approvals retrieved successfully",
		"data":    documents,
	})
}

// UploadDocument handles POST /api/documents/upload
func (h *Handler) UploadDocument(c *fiber.Ctx) error {
	if h.uploadService == nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Upload service not available",
		})
	}

	// Get form data
	title := c.FormValue("title")
	description := c.FormValue("description")
	documentNumber := c.FormValue("document_number")
	category := c.FormValue("category")
	documentType := c.FormValue("document_type")
	accessLevel := c.FormValue("access_level")

	// Get file from form
	fileHeader, err := c.FormFile("file")
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "File is required",
			"error":   err.Error(),
		})
	}

	// Get user and school ID from context
	userID := c.Locals("user_id").(uuid.UUID)
	schoolID := c.Locals("school_id").(uuid.UUID)

	// Upload document with metadata
	doc, err := h.uploadService.UploadDocumentWithMetadata(
		c.Context(),
		fileHeader,
		title,
		description,
		documentNumber,
		category,
		documentType,
		accessLevel,
		userID,
		schoolID,
	)
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to upload document",
			"error":   err.Error(),
		})
	}

	return c.Status(201).JSON(fiber.Map{
		"status":  "success",
		"message": "Document uploaded successfully",
		"data":    doc,
	})
}

// CheckDuplicate handles POST /api/documents/check-duplicate
func (h *Handler) CheckDuplicate(c *fiber.Ctx) error {
	if h.uploadService == nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Upload service not available",
		})
	}

	var req struct {
		Title          string `json:"title"`
		DocumentNumber string `json:"document_number"`
		FileHash       string `json:"file_hash"`
	}

	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{
			"status":  "error",
			"message": "Invalid request body",
			"error":   err.Error(),
		})
	}

	schoolID := c.Locals("school_id").(uuid.UUID)

	duplicate, err := h.uploadService.CheckDuplicateDocument(c.Context(), schoolID, req.FileHash, req.Title, req.DocumentNumber)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status":  "error",
			"message": "Failed to check for duplicates",
			"error":   err.Error(),
		})
	}

	if duplicate != nil {
		return c.Status(200).JSON(fiber.Map{
			"status":      "warning",
			"message":     "Duplicate document found",
			"data":        duplicate,
			"isDuplicate": true,
		})
	}

	return c.Status(200).JSON(fiber.Map{
		"status":      "success",
		"message":     "No duplicate found",
		"isDuplicate": false,
	})
}
