package document_repository

import (
	"context"
	"fmt"
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// Service handles business logic for document repository
type Service struct {
	repo *Repository
}

// NewService creates a new document repository service
func NewService(repo *Repository) *Service {
	return &Service{repo: repo}
}

// CreateDocument creates a new document with validation and business logic
func (s *Service) CreateDocument(ctx context.Context, req *DocumentRequest, authorID, schoolID uuid.UUID) (*Document, error) {
	// Validate request
	if !IsValidDocumentCategory(req.Category) {
		return nil, fmt.Errorf("invalid document category: %s", req.Category)
	}
	if !IsValidDocumentType(req.DocumentType) {
		return nil, fmt.Errorf("invalid document type: %s", req.DocumentType)
	}
	if !IsValidAccessLevel(req.AccessLevel) {
		return nil, fmt.Errorf("invalid access level: %s", req.AccessLevel)
	}

	// Set default values
	if req.Status == "" {
		req.Status = DocumentStatusDraft
	}

	// Create document
	doc := &Document{
		ID:                uuid.New(),
		Title:             req.Title,
		Description:       req.Description,
		DocumentNumber:    req.DocumentNumber,
		Category:          req.Category,
		DocumentType:      req.DocumentType,
		Status:            req.Status,
		AccessLevel:       req.AccessLevel,
		FileURL:           req.FileURL,
		FileName:          req.FileName,
		FileSize:          req.FileSize,
		FileHash:          req.FileHash,
		MimeType:          req.MimeType,
		AuthorID:          authorID,
		SchoolID:          schoolID,
		Version:           1,
		IsCurrentVersion:  true,
		PublishedDate:     req.PublishedDate,
		ExpiryDate:        req.ExpiryDate,
		EffectiveDate:     req.EffectiveDate,
		ReviewDate:        req.ReviewDate,
		IsConfidential:    req.IsConfidential,
		RequiresSignature: req.RequiresSignature,
		StorageLocation:   req.StorageLocation,
	}

	if req.DepartmentID != nil {
		deptID, err := uuid.Parse(*req.DepartmentID)
		if err != nil {
			return nil, fmt.Errorf("invalid department ID: %w", err)
		}
		doc.DepartmentID = &deptID
	}

	// Create document
	if err := s.repo.CreateDocument(ctx, doc); err != nil {
		return nil, fmt.Errorf("failed to create document: %w", err)
	}

	// Associate tags if provided
	if len(req.Tags) > 0 {
		for _, tagName := range req.Tags {
			tag, err := s.getOrCreateTag(ctx, tagName)
			if err != nil {
				continue // Log error but continue with other tags
			}
			_ = s.repo.AssociateDocumentWithTag(ctx, doc.ID, tag.ID)
			_ = s.repo.IncrementDocumentTagUsage(ctx, tag.ID)
		}
	}

	return doc, nil
}

// GetDocumentByID retrieves a document by ID
func (s *Service) GetDocumentByID(ctx context.Context, id uuid.UUID) (*Document, error) {
	doc, err := s.repo.GetDocumentByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("failed to get document: %w", err)
	}

	// Increment view count
	_ = s.repo.IncrementDocumentViewCount(ctx, id)

	return doc, nil
}

// GetDocumentsBySchoolID retrieves documents by school ID with filters
func (s *Service) GetDocumentsBySchoolID(ctx context.Context, schoolID uuid.UUID, req DocumentListRequest) ([]Document, int64, error) {
	return s.repo.GetDocumentsBySchoolID(ctx, schoolID, req)
}

// UpdateDocument updates an existing document
func (s *Service) UpdateDocument(ctx context.Context, id uuid.UUID, req *DocumentRequest, userID uuid.UUID) (*Document, error) {
	doc, err := s.repo.GetDocumentByID(ctx, id)
	if err != nil {
		return nil, fmt.Errorf("document not found: %w", err)
	}

	// Validate request
	if req.Category != "" && !IsValidDocumentCategory(req.Category) {
		return nil, fmt.Errorf("invalid document category: %s", req.Category)
	}
	if req.DocumentType != "" && !IsValidDocumentType(req.DocumentType) {
		return nil, fmt.Errorf("invalid document type: %s", req.DocumentType)
	}
	if req.AccessLevel != "" && !IsValidAccessLevel(req.AccessLevel) {
		return nil, fmt.Errorf("invalid access level: %s", req.AccessLevel)
	}

	// Update fields
	if req.Title != "" {
		doc.Title = req.Title
	}
	if req.Description != "" {
		doc.Description = req.Description
	}
	if req.DocumentNumber != "" {
		doc.DocumentNumber = req.DocumentNumber
	}
	if req.Category != "" {
		doc.Category = req.Category
	}
	if req.DocumentType != "" {
		doc.DocumentType = req.DocumentType
	}
	if req.Status != "" {
		doc.Status = req.Status
	}
	if req.AccessLevel != "" {
		doc.AccessLevel = req.AccessLevel
	}
	if req.FileURL != "" {
		doc.FileURL = req.FileURL
	}
	if req.FileName != "" {
		doc.FileName = req.FileName
	}
	if req.FileSize > 0 {
		doc.FileSize = req.FileSize
	}
	if req.FileHash != "" {
		doc.FileHash = req.FileHash
	}
	if req.MimeType != "" {
		doc.MimeType = req.MimeType
	}
	if req.DepartmentID != nil {
		deptID, err := uuid.Parse(*req.DepartmentID)
		if err != nil {
			return nil, fmt.Errorf("invalid department ID: %w", err)
		}
		doc.DepartmentID = &deptID
	}
	if req.PublishedDate != nil {
		doc.PublishedDate = req.PublishedDate
	}
	if req.ExpiryDate != nil {
		doc.ExpiryDate = req.ExpiryDate
	}
	if req.EffectiveDate != nil {
		doc.EffectiveDate = req.EffectiveDate
	}
	if req.ReviewDate != nil {
		doc.ReviewDate = req.ReviewDate
	}
	doc.IsConfidential = req.IsConfidential
	doc.RequiresSignature = req.RequiresSignature
	if req.StorageLocation != "" {
		doc.StorageLocation = req.StorageLocation
	}

	// Update document
	if err := s.repo.UpdateDocument(ctx, doc); err != nil {
		return nil, fmt.Errorf("failed to update document: %w", err)
	}

	// Update tags if provided
	if len(req.Tags) > 0 {
		// Remove existing tag associations
		_ = s.repo.DissociateDocumentWithTag(ctx, id, uuid.Nil) // This needs to be fixed to remove all associations

		// Add new tag associations
		for _, tagName := range req.Tags {
			tag, err := s.getOrCreateTag(ctx, tagName)
			if err != nil {
				continue
			}
			_ = s.repo.AssociateDocumentWithTag(ctx, id, tag.ID)
			_ = s.repo.IncrementDocumentTagUsage(ctx, tag.ID)
		}
	}

	return doc, nil
}

// DeleteDocument deletes a document
func (s *Service) DeleteDocument(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteDocument(ctx, id)
}

// CreateDocumentVersion creates a new version of a document
func (s *Service) CreateDocumentVersion(ctx context.Context, req *DocumentVersionRequest, changedBy uuid.UUID) (*DocumentVersion, error) {
	// Get current version to determine new version number
	latestVersion, err := s.repo.GetLatestDocumentVersion(ctx, uuid.MustParse(req.DocumentID))
	var newVersionNumber int
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			newVersionNumber = 1
		} else {
			return nil, fmt.Errorf("failed to get latest version: %w", err)
		}
	} else {
		if req.IsMajorVersion {
			newVersionNumber = (latestVersion.VersionNumber/10)*10 + 10
		} else {
			newVersionNumber = latestVersion.VersionNumber + 1
		}
	}

	// Create version
	version := &DocumentVersion{
		ID:             uuid.New(),
		DocumentID:     uuid.MustParse(req.DocumentID),
		VersionNumber:  newVersionNumber,
		Title:          req.Title,
		Description:    req.Description,
		FileURL:        req.FileURL,
		FileName:       req.FileName,
		FileSize:       req.FileSize,
		FileHash:       req.FileHash,
		ChangeSummary:  req.ChangeSummary,
		ChangedBy:      changedBy,
		ChangeReason:   req.ChangeReason,
		IsMajorVersion: req.IsMajorVersion,
	}

	if err := s.repo.CreateDocumentVersion(ctx, version); err != nil {
		return nil, fmt.Errorf("failed to create document version: %w", err)
	}

	// Update main document version
	doc, err := s.repo.GetDocumentByID(ctx, uuid.MustParse(req.DocumentID))
	if err == nil {
		doc.Version = newVersionNumber
		_ = s.repo.UpdateDocument(ctx, doc)
	}

	return version, nil
}

// GetDocumentVersions retrieves all versions of a document
func (s *Service) GetDocumentVersions(ctx context.Context, documentID uuid.UUID) ([]DocumentVersion, error) {
	return s.repo.GetDocumentVersions(ctx, documentID)
}

// SubmitDocumentForApproval submits a document for approval
func (s *Service) SubmitDocumentForApproval(ctx context.Context, documentID uuid.UUID, approvers []uuid.UUID) error {
	// Update document status to pending
	doc, err := s.repo.GetDocumentByID(ctx, documentID)
	if err != nil {
		return fmt.Errorf("document not found: %w", err)
	}
	doc.Status = DocumentStatusPending
	if err := s.repo.UpdateDocument(ctx, doc); err != nil {
		return fmt.Errorf("failed to update document status: %w", err)
	}

	// Create approval requests
	for i, approverID := range approvers {
		approval := &DocumentApproval{
			ID:            uuid.New(),
			DocumentID:    documentID,
			ApproverID:    approverID,
			Status:        "PENDING",
			ApprovalLevel: i + 1,
			IsRequired:    true,
		}
		if err := s.repo.CreateDocumentApproval(ctx, approval); err != nil {
			return fmt.Errorf("failed to create approval request: %w", err)
		}
	}

	return nil
}

// ApproveDocument approves a document
func (s *Service) ApproveDocument(ctx context.Context, approvalID uuid.UUID, approverID uuid.UUID, comments string) error {
	approval, err := s.repo.GetDocumentApprovalByID(ctx, approvalID)
	if err != nil {
		return fmt.Errorf("approval not found: %w", err)
	}

	if approval.ApproverID != approverID {
		return fmt.Errorf("unauthorized: you are not the assigned approver")
	}

	// Update approval
	approval.Status = "APPROVED"
	approval.Comments = comments
	now := time.Now()
	approval.ApprovedAt = &now

	if err := s.repo.UpdateDocumentApproval(ctx, approval); err != nil {
		return fmt.Errorf("failed to update approval: %w", err)
	}

	// Check if all required approvals are completed
	allApprovals, err := s.repo.GetDocumentApprovals(ctx, approval.DocumentID)
	if err != nil {
		return fmt.Errorf("failed to get approvals: %w", err)
	}

	allApproved := true
	for _, a := range allApprovals {
		if a.IsRequired && a.Status != "APPROVED" {
			allApproved = false
			break
		}
	}

	// Update document status if all approvals completed
	if allApproved {
		doc, err := s.repo.GetDocumentByID(ctx, approval.DocumentID)
		if err == nil {
			doc.Status = DocumentStatusApproved
			_ = s.repo.UpdateDocument(ctx, doc)
		}
	}

	return nil
}

// RejectDocument rejects a document
func (s *Service) RejectDocument(ctx context.Context, approvalID uuid.UUID, approverID uuid.UUID, comments string) error {
	approval, err := s.repo.GetDocumentApprovalByID(ctx, approvalID)
	if err != nil {
		return fmt.Errorf("approval not found: %w", err)
	}

	if approval.ApproverID != approverID {
		return fmt.Errorf("unauthorized: you are not the assigned approver")
	}

	// Update approval
	approval.Status = "REJECTED"
	approval.Comments = comments

	if err := s.repo.UpdateDocumentApproval(ctx, approval); err != nil {
		return fmt.Errorf("failed to update approval: %w", err)
	}

	// Update document status
	doc, err := s.repo.GetDocumentByID(ctx, approval.DocumentID)
	if err == nil {
		doc.Status = DocumentStatusRejected
		_ = s.repo.UpdateDocument(ctx, doc)
	}

	return nil
}

// GetDocumentApprovalByID retrieves an approval by ID
func (s *Service) GetDocumentApprovalByID(ctx context.Context, id uuid.UUID) (*DocumentApproval, error) {
	return s.repo.GetDocumentApprovalByID(ctx, id)
}

// CreateDocumentCategory creates a new document category
func (s *Service) CreateDocumentCategory(ctx context.Context, req *DocumentCategoryRequest) (*DocumentCategory, error) {
	category := &DocumentCategory{
		ID:          uuid.New(),
		Name:        req.Name,
		Description: req.Description,
		Color:       req.Color,
		Icon:        req.Icon,
		SortOrder:   req.SortOrder,
		IsActive:    req.IsActive,
	}

	if req.ParentID != nil {
		parentID, err := uuid.Parse(*req.ParentID)
		if err != nil {
			return nil, fmt.Errorf("invalid parent ID: %w", err)
		}
		category.ParentID = &parentID
	}

	if err := s.repo.CreateDocumentCategory(ctx, category); err != nil {
		return nil, fmt.Errorf("failed to create category: %w", err)
	}

	return category, nil
}

// GetDocumentCategories retrieves all document categories
func (s *Service) GetDocumentCategories(ctx context.Context) ([]DocumentCategory, error) {
	return s.repo.GetDocumentCategories(ctx)
}

// CreateDocumentTag creates a new document tag
func (s *Service) CreateDocumentTag(ctx context.Context, req *DocumentTagRequest) (*DocumentTag, error) {
	tag := &DocumentTag{
		ID:    uuid.New(),
		Name:  req.Name,
		Color: req.Color,
	}

	if err := s.repo.CreateDocumentTag(ctx, tag); err != nil {
		return nil, fmt.Errorf("failed to create tag: %w", err)
	}

	return tag, nil
}

// GetDocumentTags retrieves all document tags
func (s *Service) GetDocumentTags(ctx context.Context) ([]DocumentTag, error) {
	return s.repo.GetDocumentTags(ctx)
}

// ShareDocument shares a document with a user or group
func (s *Service) ShareDocument(ctx context.Context, req *DocumentShareRequest, sharedBy uuid.UUID) (*DocumentShare, error) {
	share := &DocumentShare{
		ID:         uuid.New(),
		DocumentID: uuid.MustParse(req.DocumentID),
		SharedWith: uuid.MustParse(req.SharedWith),
		SharedBy:   sharedBy,
		ShareType:  req.ShareType,
		Permission: req.Permission,
		ExpiresAt:  req.ExpiresAt,
		IsActive:   true,
	}

	if err := s.repo.CreateDocumentShare(ctx, share); err != nil {
		return nil, fmt.Errorf("failed to create share: %w", err)
	}

	return share, nil
}

// GetDocumentShares retrieves shares for a document
func (s *Service) GetDocumentShares(ctx context.Context, documentID uuid.UUID) ([]DocumentShare, error) {
	return s.repo.GetDocumentShares(ctx, documentID)
}

// GetDocumentStatistics retrieves document statistics
func (s *Service) GetDocumentStatistics(ctx context.Context, schoolID uuid.UUID) (*DocumentStatistics, error) {
	return s.repo.GetDocumentStatistics(ctx, schoolID)
}

// SearchDocuments performs advanced search
func (s *Service) SearchDocuments(ctx context.Context, schoolID uuid.UUID, req *DocumentSearchRequest) ([]Document, int64, error) {
	return s.repo.SearchDocuments(ctx, schoolID, *req)
}

// Helper function to get or create a tag
func (s *Service) getOrCreateTag(ctx context.Context, tagName string) (*DocumentTag, error) {
	// Try to find existing tag
	tags, err := s.repo.GetDocumentTags(ctx)
	if err != nil {
		return nil, err
	}

	for _, tag := range tags {
		if tag.Name == tagName {
			return &tag, nil
		}
	}

	// Create new tag
	newTag := &DocumentTag{
		ID:    uuid.New(),
		Name:  tagName,
		Color: "#3B82F6", // Default blue color
	}

	if err := s.repo.CreateDocumentTag(ctx, newTag); err != nil {
		return nil, err
	}

	return newTag, nil
}

// DownloadDocument handles document download with logging
func (s *Service) DownloadDocument(ctx context.Context, documentID, userID uuid.UUID, ipAddress, userAgent string) (*Document, error) {
	doc, err := s.repo.GetDocumentByID(ctx, documentID)
	if err != nil {
		return nil, fmt.Errorf("document not found: %w", err)
	}

	// Log access
	log := &DocumentAccessLog{
		ID:         uuid.New(),
		DocumentID: documentID,
		UserID:     userID,
		Action:     "DOWNLOAD",
		IPAddress:  ipAddress,
		UserAgent:  userAgent,
		AccessTime: time.Now(),
	}

	_ = s.repo.LogDocumentAccess(ctx, log)

	// Increment download count
	_ = s.repo.IncrementDocumentDownloadCount(ctx, documentID)

	return doc, nil
}

// GetExpiringDocuments retrieves documents expiring soon
func (s *Service) GetExpiringDocuments(ctx context.Context, schoolID uuid.UUID, days int) ([]Document, error) {
	var documents []Document
	err := s.repo.GetExpiringDocuments(ctx, schoolID, days, &documents)
	return documents, err
}

// GetPendingApprovalDocuments retrieves documents pending approval
func (s *Service) GetPendingApprovalDocuments(ctx context.Context, schoolID uuid.UUID) ([]Document, error) {
	var documents []Document
	err := s.repo.GetPendingApprovalDocuments(ctx, schoolID, &documents)
	return documents, err
}
