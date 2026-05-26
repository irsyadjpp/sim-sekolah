package document_repository

import "time"

// DocumentRequest represents request for creating/updating documents
type DocumentRequest struct {
	Title             string     `json:"title" validate:"required,max=255"`
	Description       string     `json:"description"`
	DocumentNumber    string     `json:"document_number" validate:"max=100"`
	Category          string     `json:"category" validate:"required"`
	DocumentType      string     `json:"document_type" validate:"required"`
	Status            string     `json:"status"`
	AccessLevel       string     `json:"access_level"`
	FileURL           string     `json:"file_url" validate:"required,url,max=500"`
	FileName          string     `json:"file_name" validate:"required,max=255"`
	FileSize          int64      `json:"file_size"`
	FileHash          string     `json:"file_hash"`
	MimeType          string     `json:"mime_type"`
	DepartmentID      *string    `json:"department_id"`
	Tags              []string   `json:"tags"`
	PublishedDate     *time.Time `json:"published_date"`
	ExpiryDate        *time.Time `json:"expiry_date"`
	EffectiveDate     *time.Time `json:"effective_date"`
	ReviewDate        *time.Time `json:"review_date"`
	IsConfidential    bool       `json:"is_confidential"`
	RequiresSignature bool       `json:"requires_signature"`
	StorageLocation   string     `json:"storage_location"`
}

// DocumentResponse represents response for document data
type DocumentResponse struct {
	ID                string     `json:"id"`
	Title             string     `json:"title"`
	Description       string     `json:"description"`
	DocumentNumber    string     `json:"document_number"`
	Category          string     `json:"category"`
	DocumentType      string     `json:"document_type"`
	Status            string     `json:"status"`
	AccessLevel       string     `json:"access_level"`
	FileURL           string     `json:"file_url"`
	FileName          string     `json:"file_name"`
	FileSize          int64      `json:"file_size"`
	FileHash          string     `json:"file_hash"`
	MimeType          string     `json:"mime_type"`
	AuthorID          string     `json:"author_id"`
	AuthorName        string     `json:"author_name"`
	DepartmentID      *string    `json:"department_id"`
	DepartmentName    *string    `json:"department_name"`
	SchoolID          string     `json:"school_id"`
	Tags              []string   `json:"tags"`
	Version           int        `json:"version"`
	IsCurrentVersion  bool       `json:"is_current_version"`
	ParentDocumentID  *string    `json:"parent_document_id"`
	PublishedDate     *time.Time `json:"published_date"`
	ExpiryDate        *time.Time `json:"expiry_date"`
	EffectiveDate     *time.Time `json:"effective_date"`
	ReviewDate        *time.Time `json:"review_date"`
	ArchivedDate      *time.Time `json:"archived_date"`
	DownloadCount     int        `json:"download_count"`
	ViewCount         int        `json:"view_count"`
	IsConfidential    bool       `json:"is_confidential"`
	RequiresSignature bool       `json:"requires_signature"`
	StorageLocation   string     `json:"storage_location"`
	CreatedAt         time.Time  `json:"created_at"`
	UpdatedAt         time.Time  `json:"updated_at"`
	CreatedBy         string     `json:"created_by"`
	UpdatedBy         string     `json:"updated_by"`
}

// DocumentListRequest represents request for listing documents
type DocumentListRequest struct {
	Category         string   `json:"category" form:"category"`
	DocumentType     string   `json:"document_type" form:"document_type"`
	Status           string   `json:"status" form:"status"`
	AccessLevel      string   `json:"access_level" form:"access_level"`
	AuthorID         string   `json:"author_id" form:"author_id"`
	DepartmentID     string   `json:"department_id" form:"department_id"`
	Tags             []string `json:"tags" form:"tags"`
	Search           string   `json:"search" form:"search"`
	SortBy           string   `json:"sort_by" form:"sort_by"`       // created_at, title, download_count, etc.
	SortOrder        string   `json:"sort_order" form:"sort_order"` // asc, desc
	Page             int      `json:"page" form:"page"`
	Limit            int      `json:"limit" form:"limit"`
	IsCurrentVersion *bool    `json:"is_current_version" form:"is_current_version"`
}

// DocumentListResponse represents response for document list
type DocumentListResponse struct {
	Documents  []DocumentResponse `json:"documents"`
	Total      int64              `json:"total"`
	Page       int                `json:"page"`
	Limit      int                `json:"limit"`
	TotalPages int                `json:"total_pages"`
}

// DocumentVersionRequest represents request for creating document version
type DocumentVersionRequest struct {
	DocumentID     string `json:"document_id" validate:"required"`
	Title          string `json:"title" validate:"required,max=255"`
	Description    string `json:"description"`
	FileURL        string `json:"file_url" validate:"required,url,max=500"`
	FileName       string `json:"file_name" validate:"required,max=255"`
	FileSize       int64  `json:"file_size"`
	FileHash       string `json:"file_hash"`
	ChangeSummary  string `json:"change_summary"`
	ChangeReason   string `json:"change_reason"`
	IsMajorVersion bool   `json:"is_major_version"`
}

// DocumentVersionResponse represents response for document version
type DocumentVersionResponse struct {
	ID             string    `json:"id"`
	DocumentID     string    `json:"document_id"`
	VersionNumber  int       `json:"version_number"`
	Title          string    `json:"title"`
	Description    string    `json:"description"`
	FileURL        string    `json:"file_url"`
	FileName       string    `json:"file_name"`
	FileSize       int64     `json:"file_size"`
	FileHash       string    `json:"file_hash"`
	ChangeSummary  string    `json:"change_summary"`
	ChangedBy      string    `json:"changed_by"`
	ChangedByName  string    `json:"changed_by_name"`
	ChangeReason   string    `json:"change_reason"`
	IsMajorVersion bool      `json:"is_major_version"`
	CreatedAt      time.Time `json:"created_at"`
}

// DocumentApprovalRequest represents request for document approval
type DocumentApprovalRequest struct {
	DocumentID    string `json:"document_id" validate:"required"`
	ApproverID    string `json:"approver_id" validate:"required"`
	Status        string `json:"status" validate:"required"`
	Comments      string `json:"comments"`
	ApprovalLevel int    `json:"approval_level" validate:"required,min=1"`
	IsRequired    bool   `json:"is_required"`
}

// DocumentApprovalResponse represents response for document approval
type DocumentApprovalResponse struct {
	ID            string     `json:"id"`
	DocumentID    string     `json:"document_id"`
	ApproverID    string     `json:"approver_id"`
	ApproverName  string     `json:"approver_name"`
	Status        string     `json:"status"`
	Comments      string     `json:"comments"`
	ApprovedAt    *time.Time `json:"approved_at"`
	ApprovalLevel int        `json:"approval_level"`
	IsRequired    bool       `json:"is_required"`
	CreatedAt     time.Time  `json:"created_at"`
}

// DocumentCategoryRequest represents request for creating/updating categories
type DocumentCategoryRequest struct {
	Name        string  `json:"name" validate:"required,max=100"`
	Description string  `json:"description"`
	Color       string  `json:"color" validate:"omitempty,len=7"`
	Icon        string  `json:"icon" validate:"max=50"`
	ParentID    *string `json:"parent_id"`
	SortOrder   int     `json:"sort_order"`
	IsActive    bool    `json:"is_active"`
}

// DocumentCategoryResponse represents response for document category
type DocumentCategoryResponse struct {
	ID            string    `json:"id"`
	Name          string    `json:"name"`
	Description   string    `json:"description"`
	Color         string    `json:"color"`
	Icon          string    `json:"icon"`
	ParentID      *string   `json:"parent_id"`
	SortOrder     int       `json:"sort_order"`
	IsActive      bool      `json:"is_active"`
	DocumentCount int       `json:"document_count"`
	CreatedAt     time.Time `json:"created_at"`
	UpdatedAt     time.Time `json:"updated_at"`
}

// DocumentTagRequest represents request for creating/updating tags
type DocumentTagRequest struct {
	Name  string `json:"name" validate:"required,max=50"`
	Color string `json:"color" validate:"omitempty,len=7"`
}

// DocumentTagResponse represents response for document tag
type DocumentTagResponse struct {
	ID         string    `json:"id"`
	Name       string    `json:"name"`
	Color      string    `json:"color"`
	UsageCount int       `json:"usage_count"`
	CreatedAt  time.Time `json:"created_at"`
	UpdatedAt  time.Time `json:"updated_at"`
}

// DocumentShareRequest represents request for sharing documents
type DocumentShareRequest struct {
	DocumentID string     `json:"document_id" validate:"required"`
	SharedWith string     `json:"shared_with" validate:"required"`
	ShareType  string     `json:"share_type" validate:"required"`
	Permission string     `json:"permission" validate:"required"`
	ExpiresAt  *time.Time `json:"expires_at"`
}

// DocumentShareResponse represents response for document share
type DocumentShareResponse struct {
	ID             string     `json:"id"`
	DocumentID     string     `json:"document_id"`
	SharedWith     string     `json:"shared_with"`
	SharedWithName string     `json:"shared_with_name"`
	SharedBy       string     `json:"shared_by"`
	SharedByName   string     `json:"shared_by_name"`
	ShareType      string     `json:"share_type"`
	Permission     string     `json:"permission"`
	ExpiresAt      *time.Time `json:"expires_at"`
	AccessCount    int        `json:"access_count"`
	IsActive       bool       `json:"is_active"`
	CreatedAt      time.Time  `json:"created_at"`
}

// DocumentAccessLogResponse represents response for access log
type DocumentAccessLogResponse struct {
	ID             string    `json:"id"`
	DocumentID     string    `json:"document_id"`
	DocumentTitle  string    `json:"document_title"`
	UserID         string    `json:"user_id"`
	UserName       string    `json:"user_name"`
	Action         string    `json:"action"`
	IPAddress      string    `json:"ip_address"`
	UserAgent      string    `json:"user_agent"`
	AccessTime     time.Time `json:"access_time"`
	AdditionalInfo string    `json:"additional_info"`
}

// AccreditationDocumentRequest represents request for accreditation document
type AccreditationDocumentRequest struct {
	DocumentID        string     `json:"document_id" validate:"required"`
	AccreditationType string     `json:"accreditation_type" validate:"required"`
	StandardNumber    string     `json:"standard_number" validate:"required,max=50"`
	StandardComponent string     `json:"standard_component" validate:"required,max=100"`
	EvidenceType      string     `json:"evidence_type" validate:"required,max=50"`
	ComplianceStatus  string     `json:"compliance_status" validate:"required"`
	AssessorNotes     string     `json:"assessor_notes"`
	VerificationDate  *time.Time `json:"verification_date"`
	NextReviewDate    *time.Time `json:"next_review_date"`
	IsMandatory       bool       `json:"is_mandatory"`
}

// AccreditationDocumentResponse represents response for accreditation document
type AccreditationDocumentResponse struct {
	ID                string     `json:"id"`
	DocumentID        string     `json:"document_id"`
	DocumentTitle     string     `json:"document_title"`
	AccreditationType string     `json:"accreditation_type"`
	StandardNumber    string     `json:"standard_number"`
	StandardComponent string     `json:"standard_component"`
	EvidenceType      string     `json:"evidence_type"`
	ComplianceStatus  string     `json:"compliance_status"`
	AssessorNotes     string     `json:"assessor_notes"`
	VerificationDate  *time.Time `json:"verification_date"`
	NextReviewDate    *time.Time `json:"next_review_date"`
	IsMandatory       bool       `json:"is_mandatory"`
	CreatedAt         time.Time  `json:"created_at"`
	UpdatedAt         time.Time  `json:"updated_at"`
}

// DocumentStatistics represents document statistics
type DocumentStatistics struct {
	TotalDocuments       int64            `json:"total_documents"`
	ByCategory           map[string]int64 `json:"by_category"`
	ByStatus             map[string]int64 `json:"by_status"`
	ByType               map[string]int64 `json:"by_type"`
	TotalDownloads       int64            `json:"total_downloads"`
	TotalViews           int64            `json:"total_views"`
	RecentUploads        int64            `json:"recent_uploads"` // Last 30 days
	PendingApprovals     int64            `json:"pending_approvals"`
	ExpiringDocuments    int64            `json:"expiring_documents"` // Expiring in next 30 days
	StorageUsed          int64            `json:"storage_used"`
	StorageUsedFormatted string           `json:"storage_used_formatted"`
}

// DocumentSearchRequest represents advanced search request
type DocumentSearchRequest struct {
	Query          string     `json:"query" validate:"required"`
	Categories     []string   `json:"categories"`
	DocumentTypes  []string   `json:"document_types"`
	DateFrom       *time.Time `json:"date_from"`
	DateTo         *time.Time `json:"date_to"`
	AuthorID       string     `json:"author_id"`
	Tags           []string   `json:"tags"`
	IncludeContent bool       `json:"include_content"` // Search in document content
	Page           int        `json:"page"`
	Limit          int        `json:"limit"`
}

// BulkDocumentActionRequest represents bulk action on documents
type BulkDocumentActionRequest struct {
	DocumentIDs []string               `json:"document_ids" validate:"required,min=1"`
	Action      string                 `json:"action" validate:"required"` // DELETE, ARCHIVE, PUBLISH, UNPUBLISH, CHANGE_CATEGORY, CHANGE_ACCESS
	Parameters  map[string]interface{} `json:"parameters"`                 // Action-specific parameters
}

// BulkDocumentActionResponse represents response for bulk action
type BulkDocumentActionResponse struct {
	SuccessCount int      `json:"success_count"`
	FailedCount  int      `json:"failed_count"`
	FailedIDs    []string `json:"failed_ids"`
	Message      string   `json:"message"`
}
