package document_repository

import (
	"context"
	"fmt"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// Repository handles data access for document repository
type Repository struct {
	db *gorm.DB
}

// NewRepository creates a new document repository
func NewRepository(db *gorm.DB) *Repository {
	return &Repository{db: db}
}

// CreateDocument creates a new document
func (r *Repository) CreateDocument(ctx context.Context, doc *Document) error {
	return r.db.WithContext(ctx).Create(doc).Error
}

// GetDocumentByID retrieves a document by ID
func (r *Repository) GetDocumentByID(ctx context.Context, id uuid.UUID) (*Document, error) {
	var doc Document
	err := r.db.WithContext(ctx).
		Preload("Author").
		Preload("Department").
		Where("id = ?", id).
		First(&doc).Error
	if err != nil {
		return nil, err
	}
	return &doc, nil
}

// GetDocumentsBySchoolID retrieves documents by school ID
func (r *Repository) GetDocumentsBySchoolID(ctx context.Context, schoolID uuid.UUID, req DocumentListRequest) ([]Document, int64, error) {
	var documents []Document
	var total int64

	query := r.db.WithContext(ctx).Model(&Document{}).Where("school_id = ?", schoolID)

	// Apply filters
	if req.Category != "" {
		query = query.Where("category = ?", req.Category)
	}
	if req.DocumentType != "" {
		query = query.Where("document_type = ?", req.DocumentType)
	}
	if req.Status != "" {
		query = query.Where("status = ?", req.Status)
	}
	if req.AccessLevel != "" {
		query = query.Where("access_level = ?", req.AccessLevel)
	}
	if req.AuthorID != "" {
		authorUUID, err := uuid.Parse(req.AuthorID)
		if err == nil {
			query = query.Where("author_id = ?", authorUUID)
		}
	}
	if req.DepartmentID != "" {
		departmentUUID, err := uuid.Parse(req.DepartmentID)
		if err == nil {
			query = query.Where("department_id = ?", departmentUUID)
		}
	}
	if req.IsCurrentVersion != nil {
		query = query.Where("is_current_version = ?", *req.IsCurrentVersion)
	}

	// Search filter
	if req.Search != "" {
		searchPattern := "%" + req.Search + "%"
		query = query.Where("title ILIKE ? OR description ILIKE ? OR document_number ILIKE ?",
			searchPattern, searchPattern, searchPattern)
	}

	// Get total count
	if err := query.Count(&total).Error; err != nil {
		return nil, 0, err
	}

	// Apply sorting
	sortBy := "created_at"
	if req.SortBy != "" {
		sortBy = req.SortBy
	}
	sortOrder := "desc"
	if req.SortOrder != "" {
		sortOrder = req.SortOrder
	}
	query = query.Order(fmt.Sprintf("%s %s", sortBy, sortOrder))

	// Apply pagination
	if req.Page <= 0 {
		req.Page = 1
	}
	if req.Limit <= 0 || req.Limit > 100 {
		req.Limit = 20
	}
	offset := (req.Page - 1) * req.Limit
	query = query.Offset(offset).Limit(req.Limit)

	// Execute query
	if err := query.
		Preload("Author").
		Preload("Department").
		Find(&documents).Error; err != nil {
		return nil, 0, err
	}

	return documents, total, nil
}

// UpdateDocument updates an existing document
func (r *Repository) UpdateDocument(ctx context.Context, doc *Document) error {
	return r.db.WithContext(ctx).Save(doc).Error
}

// DeleteDocument soft deletes a document
func (r *Repository) DeleteDocument(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&Document{}, id).Error
}

// CreateDocumentVersion creates a new document version
func (r *Repository) CreateDocumentVersion(ctx context.Context, version *DocumentVersion) error {
	return r.db.WithContext(ctx).Create(version).Error
}

// GetDocumentVersions retrieves all versions of a document
func (r *Repository) GetDocumentVersions(ctx context.Context, documentID uuid.UUID) ([]DocumentVersion, error) {
	var versions []DocumentVersion
	err := r.db.WithContext(ctx).
		Where("document_id = ?", documentID).
		Order("version_number DESC").
		Find(&versions).Error
	return versions, err
}

// GetLatestDocumentVersion retrieves the latest version of a document
func (r *Repository) GetLatestDocumentVersion(ctx context.Context, documentID uuid.UUID) (*DocumentVersion, error) {
	var version DocumentVersion
	err := r.db.WithContext(ctx).
		Where("document_id = ?", documentID).
		Order("version_number DESC").
		First(&version).Error
	if err != nil {
		return nil, err
	}
	return &version, nil
}

// CreateDocumentApproval creates a new document approval
func (r *Repository) CreateDocumentApproval(ctx context.Context, approval *DocumentApproval) error {
	return r.db.WithContext(ctx).Create(approval).Error
}

// GetDocumentApprovals retrieves approvals for a document
func (r *Repository) GetDocumentApprovals(ctx context.Context, documentID uuid.UUID) ([]DocumentApproval, error) {
	var approvals []DocumentApproval
	err := r.db.WithContext(ctx).
		Preload("Approver").
		Where("document_id = ?", documentID).
		Order("approval_level ASC").
		Find(&approvals).Error
	return approvals, err
}

// UpdateDocumentApproval updates a document approval
func (r *Repository) UpdateDocumentApproval(ctx context.Context, approval *DocumentApproval) error {
	return r.db.WithContext(ctx).Save(approval).Error
}

// CreateDocumentCategory creates a new document category
func (r *Repository) CreateDocumentCategory(ctx context.Context, category *DocumentCategory) error {
	return r.db.WithContext(ctx).Create(category).Error
}

// GetDocumentCategories retrieves all document categories
func (r *Repository) GetDocumentCategories(ctx context.Context) ([]DocumentCategory, error) {
	var categories []DocumentCategory
	err := r.db.WithContext(ctx).
		Where("is_active = ?", true).
		Order("sort_order ASC, name ASC").
		Find(&categories).Error
	return categories, err
}

// GetDocumentCategoryByID retrieves a category by ID
func (r *Repository) GetDocumentCategoryByID(ctx context.Context, id uuid.UUID) (*DocumentCategory, error) {
	var category DocumentCategory
	err := r.db.WithContext(ctx).Where("id = ?", id).First(&category).Error
	if err != nil {
		return nil, err
	}
	return &category, nil
}

// UpdateDocumentCategory updates a document category
func (r *Repository) UpdateDocumentCategory(ctx context.Context, category *DocumentCategory) error {
	return r.db.WithContext(ctx).Save(category).Error
}

// DeleteDocumentCategory deletes a document category
func (r *Repository) DeleteDocumentCategory(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&DocumentCategory{}, id).Error
}

// CreateDocumentTag creates a new document tag
func (r *Repository) CreateDocumentTag(ctx context.Context, tag *DocumentTag) error {
	return r.db.WithContext(ctx).Create(tag).Error
}

// GetDocumentTags retrieves all document tags
func (r *Repository) GetDocumentTags(ctx context.Context) ([]DocumentTag, error) {
	var tags []DocumentTag
	err := r.db.WithContext(ctx).
		Order("usage_count DESC, name ASC").
		Find(&tags).Error
	return tags, err
}

// GetDocumentTagsByDocumentID retrieves tags for a specific document
func (r *Repository) GetDocumentTagsByDocumentID(ctx context.Context, documentID uuid.UUID) ([]DocumentTag, error) {
	var tags []DocumentTag
	err := r.db.WithContext(ctx).
		Joins("JOIN document_tag_associations ON document_tags.id = document_tag_associations.tag_id").
		Where("document_tag_associations.document_id = ?", documentID).
		Find(&tags).Error
	return tags, err
}

// AssociateDocumentWithTag associates a document with a tag
func (r *Repository) AssociateDocumentWithTag(ctx context.Context, documentID, tagID uuid.UUID) error {
	association := &DocumentTagAssociation{
		DocumentID: documentID,
		TagID:      tagID,
	}
	return r.db.WithContext(ctx).Create(association).Error
}

// DissociateDocumentWithTag removes association between document and tag
func (r *Repository) DissociateDocumentWithTag(ctx context.Context, documentID, tagID uuid.UUID) error {
	return r.db.WithContext(ctx).
		Where("document_id = ? AND tag_id = ?", documentID, tagID).
		Delete(&DocumentTagAssociation{}).Error
}

// IncrementDocumentTagUsage increments usage count for a tag
func (r *Repository) IncrementDocumentTagUsage(ctx context.Context, tagID uuid.UUID) error {
	return r.db.WithContext(ctx).
		Model(&DocumentTag{}).
		Where("id = ?", tagID).
		UpdateColumn("usage_count", gorm.Expr("usage_count + 1")).Error
}

// CreateDocumentShare creates a new document share
func (r *Repository) CreateDocumentShare(ctx context.Context, share *DocumentShare) error {
	return r.db.WithContext(ctx).Create(share).Error
}

// GetDocumentShares retrieves shares for a document
func (r *Repository) GetDocumentShares(ctx context.Context, documentID uuid.UUID) ([]DocumentShare, error) {
	var shares []DocumentShare
	err := r.db.WithContext(ctx).
		Preload("SharedWith").
		Preload("SharedBy").
		Where("document_id = ? AND is_active = ?", documentID, true).
		Find(&shares).Error
	return shares, err
}

// GetSharedDocuments retrieves documents shared with a user
func (r *Repository) GetSharedDocuments(ctx context.Context, userID uuid.UUID) ([]Document, error) {
	var documents []Document
	err := r.db.WithContext(ctx).
		Joins("JOIN document_shares ON documents.id = document_shares.document_id").
		Where("document_shares.shared_with = ? AND document_shares.is_active = ?", userID, true).
		Preload("Author").
		Find(&documents).Error
	return documents, err
}

// UpdateDocumentShare updates a document share
func (r *Repository) UpdateDocumentShare(ctx context.Context, share *DocumentShare) error {
	return r.db.WithContext(ctx).Save(share).Error
}

// DeleteDocumentShare deletes a document share
func (r *Repository) DeleteDocumentShare(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&DocumentShare{}, id).Error
}

// LogDocumentAccess logs document access
func (r *Repository) LogDocumentAccess(ctx context.Context, log *DocumentAccessLog) error {
	return r.db.WithContext(ctx).Create(log).Error
}

// GetDocumentAccessLogs retrieves access logs for a document
func (r *Repository) GetDocumentAccessLogs(ctx context.Context, documentID uuid.UUID, limit int) ([]DocumentAccessLog, error) {
	var logs []DocumentAccessLog
	query := r.db.WithContext(ctx).
		Preload("User").
		Where("document_id = ?", documentID).
		Order("access_time DESC")

	if limit > 0 {
		query = query.Limit(limit)
	}

	err := query.Find(&logs).Error
	return logs, err
}

// GetUserAccessLogs retrieves access logs for a user
func (r *Repository) GetUserAccessLogs(ctx context.Context, userID uuid.UUID, limit int) ([]DocumentAccessLog, error) {
	var logs []DocumentAccessLog
	query := r.db.WithContext(ctx).
		Preload("Document").
		Where("user_id = ?", userID).
		Order("access_time DESC")

	if limit > 0 {
		query = query.Limit(limit)
	}

	err := query.Find(&logs).Error
	return logs, err
}

// IncrementDocumentDownloadCount increments download count for a document
func (r *Repository) IncrementDocumentDownloadCount(ctx context.Context, documentID uuid.UUID) error {
	return r.db.WithContext(ctx).
		Model(&Document{}).
		Where("id = ?", documentID).
		UpdateColumn("download_count", gorm.Expr("download_count + 1")).Error
}

// IncrementDocumentViewCount increments view count for a document
func (r *Repository) IncrementDocumentViewCount(ctx context.Context, documentID uuid.UUID) error {
	return r.db.WithContext(ctx).
		Model(&Document{}).
		Where("id = ?", documentID).
		UpdateColumn("view_count", gorm.Expr("view_count + 1")).Error
}

// CreateAccreditationDocument creates an accreditation document
func (r *Repository) CreateAccreditationDocument(ctx context.Context, accDoc *AccreditationDocument) error {
	return r.db.WithContext(ctx).Create(accDoc).Error
}

// GetAccreditationDocuments retrieves accreditation documents
func (r *Repository) GetAccreditationDocuments(ctx context.Context, accreditationType string) ([]AccreditationDocument, error) {
	var accDocs []AccreditationDocument
	query := r.db.WithContext(ctx).Preload("Document")

	if accreditationType != "" {
		query = query.Where("accreditation_type = ?", accreditationType)
	}

	err := query.Find(&accDocs).Error
	return accDocs, err
}

// GetAccreditationDocumentByDocumentID retrieves accreditation document by document ID
func (r *Repository) GetAccreditationDocumentByDocumentID(ctx context.Context, documentID uuid.UUID) (*AccreditationDocument, error) {
	var accDoc AccreditationDocument
	err := r.db.WithContext(ctx).
		Preload("Document").
		Where("document_id = ?", documentID).
		First(&accDoc).Error
	if err != nil {
		return nil, err
	}
	return &accDoc, nil
}

// UpdateAccreditationDocument updates an accreditation document
func (r *Repository) UpdateAccreditationDocument(ctx context.Context, accDoc *AccreditationDocument) error {
	return r.db.WithContext(ctx).Save(accDoc).Error
}

// DeleteAccreditationDocument deletes an accreditation document
func (r *Repository) DeleteAccreditationDocument(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&AccreditationDocument{}, id).Error
}

// GetDocumentStatistics retrieves document statistics
func (r *Repository) GetDocumentStatistics(ctx context.Context, schoolID uuid.UUID) (*DocumentStatistics, error) {
	stats := &DocumentStatistics{}

	// Total documents
	r.db.WithContext(ctx).Model(&Document{}).Where("school_id = ?", schoolID).Count(&stats.TotalDocuments)

	// By category
	var categoryStats []struct {
		Category string
		Count    int64
	}
	r.db.WithContext(ctx).
		Model(&Document{}).
		Select("category, count(*) as count").
		Where("school_id = ?", schoolID).
		Group("category").
		Scan(&categoryStats)

	stats.ByCategory = make(map[string]int64)
	for _, stat := range categoryStats {
		stats.ByCategory[stat.Category] = stat.Count
	}

	// By status
	var statusStats []struct {
		Status string
		Count  int64
	}
	r.db.WithContext(ctx).
		Model(&Document{}).
		Select("status, count(*) as count").
		Where("school_id = ?", schoolID).
		Group("status").
		Scan(&statusStats)

	stats.ByStatus = make(map[string]int64)
	for _, stat := range statusStats {
		stats.ByStatus[stat.Status] = stat.Count
	}

	// By type
	var typeStats []struct {
		DocumentType string
		Count        int64
	}
	r.db.WithContext(ctx).
		Model(&Document{}).
		Select("document_type, count(*) as count").
		Where("school_id = ?", schoolID).
		Group("document_type").
		Scan(&typeStats)

	stats.ByType = make(map[string]int64)
	for _, stat := range typeStats {
		stats.ByType[stat.DocumentType] = stat.Count
	}

	// Total downloads and views
	r.db.WithContext(ctx).Model(&Document{}).Where("school_id = ?", schoolID).Select("COALESCE(SUM(download_count), 0)").Scan(&stats.TotalDownloads)
	r.db.WithContext(ctx).Model(&Document{}).Where("school_id = ?", schoolID).Select("COALESCE(SUM(view_count), 0)").Scan(&stats.TotalViews)

	// Recent uploads (last 30 days)
	r.db.WithContext(ctx).Model(&Document{}).Where("school_id = ? AND created_at >= CURRENT_DATE - INTERVAL '30 days'", schoolID).Count(&stats.RecentUploads)

	// Pending approvals
	r.db.WithContext(ctx).Model(&Document{}).Where("school_id = ? AND status = ?", schoolID, "PENDING").Count(&stats.PendingApprovals)

	// Expiring documents (next 30 days)
	r.db.WithContext(ctx).Model(&Document{}).Where("school_id = ? AND expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'", schoolID).Count(&stats.ExpiringDocuments)

	// Storage used
	r.db.WithContext(ctx).Model(&Document{}).Where("school_id = ?", schoolID).Select("COALESCE(SUM(file_size), 0)").Scan(&stats.StorageUsed)

	return stats, nil
}

// SearchDocuments performs advanced search on documents
func (r *Repository) SearchDocuments(ctx context.Context, schoolID uuid.UUID, req DocumentSearchRequest) ([]Document, int64, error) {
	var documents []Document
	var total int64

	query := r.db.WithContext(ctx).Model(&Document{}).Where("school_id = ?", schoolID)

	// Search query
	searchPattern := "%" + req.Query + "%"
	query = query.Where("title ILIKE ? OR description ILIKE ? OR document_number ILIKE ?",
		searchPattern, searchPattern, searchPattern)

	// Additional filters
	if len(req.Categories) > 0 {
		query = query.Where("category IN ?", req.Categories)
	}
	if len(req.DocumentTypes) > 0 {
		query = query.Where("document_type IN ?", req.DocumentTypes)
	}
	if req.AuthorID != "" {
		authorUUID, err := uuid.Parse(req.AuthorID)
		if err == nil {
			query = query.Where("author_id = ?", authorUUID)
		}
	}
	if req.DateFrom != nil {
		query = query.Where("created_at >= ?", *req.DateFrom)
	}
	if req.DateTo != nil {
		query = query.Where("created_at <= ?", *req.DateTo)
	}
	if len(req.Tags) > 0 {
		query = query.Joins("JOIN document_tag_associations ON documents.id = document_tag_associations.document_id").
			Joins("JOIN document_tags ON document_tag_associations.tag_id = document_tags.id").
			Where("document_tags.name IN ?", req.Tags)
	}

	// Get total count
	if err := query.Count(&total).Error; err != nil {
		return nil, 0, err
	}

	// Apply pagination
	if req.Page <= 0 {
		req.Page = 1
	}
	if req.Limit <= 0 || req.Limit > 100 {
		req.Limit = 20
	}
	offset := (req.Page - 1) * req.Limit
	query = query.Offset(offset).Limit(req.Limit)

	// Execute query
	if err := query.
		Preload("Author").
		Preload("Department").
		Find(&documents).Error; err != nil {
		return nil, 0, err
	}

	return documents, total, nil
}

// GetDocumentApprovalByID retrieves an approval by ID
func (r *Repository) GetDocumentApprovalByID(ctx context.Context, id uuid.UUID) (*DocumentApproval, error) {
	var approval DocumentApproval
	err := r.db.WithContext(ctx).
		Preload("Approver").
		Where("id = ?", id).
		First(&approval).Error
	if err != nil {
		return nil, err
	}
	return &approval, nil
}

// GetExpiringDocuments retrieves documents expiring within specified days
func (r *Repository) GetExpiringDocuments(ctx context.Context, schoolID uuid.UUID, days int, documents *[]Document) error {
	return r.db.WithContext(ctx).
		Where("school_id = ? AND expiry_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '? days'", schoolID, days).
		Preload("Author").
		Find(documents).Error
}

// GetPendingApprovalDocuments retrieves documents pending approval
func (r *Repository) GetPendingApprovalDocuments(ctx context.Context, schoolID uuid.UUID, documents *[]Document) error {
	return r.db.WithContext(ctx).
		Where("school_id = ? AND status = ?", schoolID, "PENDING").
		Preload("Author").
		Find(documents).Error
}
