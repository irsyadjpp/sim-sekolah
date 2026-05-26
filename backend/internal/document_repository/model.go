package document_repository

import (
	"time"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// Document Categories
const (
	DocumentCategoryGeneral        = "GENERAL"
	DocumentCategoryAccreditation  = "ACCREDITATION"
	DocumentCategoryCurriculum     = "CURRICULUM"
	DocumentCategoryAssessment     = "ASSESSMENT"
	DocumentCategoryAdministration = "ADMINISTRATION"
	DocumentCategoryFinance        = "FINANCE"
	DocumentCategoryHR             = "HR"
	DocumentCategoryLegal          = "LEGAL"
	DocumentCategoryStudent        = "STUDENT"
	DocumentCategoryTeacher        = "TEACHER"
	DocumentCategoryPolicy         = "POLICY"
	DocumentCategoryReport         = "REPORT"
)

// Document Types
const (
	DocumentTypePDF     = "PDF"
	DocumentTypeDOC     = "DOC"
	DocumentTypeDOCX    = "DOCX"
	DocumentTypeXLS     = "XLS"
	DocumentTypeXLSX    = "XLSX"
	DocumentTypePPT     = "PPT"
	DocumentTypePPTX    = "PPTX"
	DocumentTypeImage   = "IMAGE"
	DocumentTypeVideo   = "VIDEO"
	DocumentTypeAudio   = "AUDIO"
	DocumentTypeArchive = "ARCHIVE"
	DocumentTypeOther   = "OTHER"
)

// Document Status
const (
	DocumentStatusDraft     = "DRAFT"
	DocumentStatusPending   = "PENDING"
	DocumentStatusApproved  = "APPROVED"
	DocumentStatusRejected  = "REJECTED"
	DocumentStatusArchived  = "ARCHIVED"
	DocumentStatusPublished = "PUBLISHED"
)

// Access Levels
const (
	AccessLevelPublic     = "PUBLIC"
	AccessLevelInternal   = "INTERNAL"
	AccessLevelPrivate    = "PRIVATE"
	AccessLevelRestricted = "RESTRICTED"
)

// Document represents a document in the repository
type Document struct {
	ID                uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Title             string     `gorm:"type:varchar(255);not null" json:"title"`
	Description       string     `gorm:"type:text" json:"description"`
	DocumentNumber    string     `gorm:"type:varchar(100);uniqueIndex" json:"document_number"`
	Category          string     `gorm:"type:varchar(50);not null;index" json:"category"`
	DocumentType      string     `gorm:"type:varchar(20);not null" json:"document_type"`
	Status            string     `gorm:"type:varchar(20);not null;default:DRAFT" json:"status"`
	AccessLevel       string     `gorm:"type:varchar(20);not null;default:INTERNAL" json:"access_level"`
	FileURL           string     `gorm:"type:varchar(500);not null" json:"file_url"`
	FileName          string     `gorm:"type:varchar(255);not null" json:"file_name"`
	FileSize          int64      `gorm:"type:bigint" json:"file_size"`
	FileHash          string     `gorm:"type:varchar(64)" json:"file_hash"`
	MimeType          string     `gorm:"type:varchar(100)" json:"mime_type"`
	AuthorID          uuid.UUID  `gorm:"type:uuid;not null;index" json:"author_id"`
	DepartmentID      *uuid.UUID `gorm:"type:uuid;index" json:"department_id"`
	SchoolID          uuid.UUID  `gorm:"type:uuid;not null;index" json:"school_id"`
	Tags              string     `gorm:"type:text" json:"tags"` // JSON array of tags
	Version           int        `gorm:"default:1" json:"version"`
	IsCurrentVersion  bool       `gorm:"default:true" json:"is_current_version"`
	ParentDocumentID  *uuid.UUID `gorm:"type:uuid;index" json:"parent_document_id"` // For versioning
	PublishedDate     *time.Time `gorm:"type:timestamp" json:"published_date"`
	ExpiryDate        *time.Time `gorm:"type:timestamp" json:"expiry_date"`
	EffectiveDate     *time.Time `gorm:"type:timestamp" json:"effective_date"`
	ReviewDate        *time.Time `gorm:"type:timestamp" json:"review_date"`
	ArchivedDate      *time.Time `gorm:"type:timestamp" json:"archived_date"`
	DownloadCount     int        `gorm:"default:0" json:"download_count"`
	ViewCount         int        `gorm:"default:0" json:"view_count"`
	IsConfidential    bool       `gorm:"default:false" json:"is_confidential"`
	RequiresSignature bool       `gorm:"default:false" json:"requires_signature"`
	StorageLocation   string     `gorm:"type:varchar(255)" json:"storage_location"` // S3, local, etc.

	common.Auditable
}

func (Document) TableName() string {
	return "documents"
}

// DocumentVersion represents version history of documents
type DocumentVersion struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	DocumentID     uuid.UUID `gorm:"type:uuid;not null;index" json:"document_id"`
	VersionNumber  int       `gorm:"not null" json:"version_number"`
	Title          string    `gorm:"type:varchar(255);not null" json:"title"`
	Description    string    `gorm:"type:text" json:"description"`
	FileURL        string    `gorm:"type:varchar(500);not null" json:"file_url"`
	FileName       string    `gorm:"type:varchar(255);not null" json:"file_name"`
	FileSize       int64     `gorm:"type:bigint" json:"file_size"`
	FileHash       string    `gorm:"type:varchar(64)" json:"file_hash"`
	ChangeSummary  string    `gorm:"type:text" json:"change_summary"`
	ChangedBy      uuid.UUID `gorm:"type:uuid;not null" json:"changed_by"`
	ChangeReason   string    `gorm:"type:text" json:"change_reason"`
	IsMajorVersion bool      `gorm:"default:false" json:"is_major_version"`

	common.Auditable
}

func (DocumentVersion) TableName() string {
	return "document_versions"
}

// DocumentApproval represents approval workflow for documents
type DocumentApproval struct {
	ID            uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	DocumentID    uuid.UUID  `gorm:"type:uuid;not null;index" json:"document_id"`
	ApproverID    uuid.UUID  `gorm:"type:uuid;not null;index" json:"approver_id"`
	Status        string     `gorm:"type:varchar(20);not null" json:"status"` // PENDING, APPROVED, REJECTED
	Comments      string     `gorm:"type:text" json:"comments"`
	ApprovedAt    *time.Time `gorm:"type:timestamp" json:"approved_at"`
	ApprovalLevel int        `gorm:"not null" json:"approval_level"` // 1, 2, 3 for multi-level approval
	IsRequired    bool       `gorm:"default:true" json:"is_required"`

	common.Auditable
}

func (DocumentApproval) TableName() string {
	return "document_approvals"
}

// DocumentCategory represents document categories
type DocumentCategory struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Name        string     `gorm:"type:varchar(100);not null;uniqueIndex" json:"name"`
	Description string     `gorm:"type:text" json:"description"`
	Color       string     `gorm:"type:varchar(7)" json:"color"` // Hex color code
	Icon        string     `gorm:"type:varchar(50)" json:"icon"`
	ParentID    *uuid.UUID `gorm:"type:uuid;index" json:"parent_id"` // For hierarchical categories
	SortOrder   int        `gorm:"default:0" json:"sort_order"`
	IsActive    bool       `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (DocumentCategory) TableName() string {
	return "document_categories"
}

// DocumentTag represents tags for documents
type DocumentTag struct {
	ID         uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Name       string    `gorm:"type:varchar(50);not null;uniqueIndex" json:"name"`
	Color      string    `gorm:"type:varchar(7)" json:"color"`
	UsageCount int       `gorm:"default:0" json:"usage_count"`

	common.Auditable
}

func (DocumentTag) TableName() string {
	return "document_tags"
}

// DocumentTagAssociation represents many-to-many relationship between documents and tags
type DocumentTagAssociation struct {
	DocumentID uuid.UUID `gorm:"type:uuid;primaryKey;autoIncrement:false" json:"document_id"`
	TagID      uuid.UUID `gorm:"type:uuid;primaryKey;autoIncrement:false" json:"tag_id"`

	common.Auditable
}

func (DocumentTagAssociation) TableName() string {
	return "document_tag_associations"
}

// DocumentAccessLog represents access logs for documents
type DocumentAccessLog struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	DocumentID     uuid.UUID `gorm:"type:uuid;not null;index" json:"document_id"`
	UserID         uuid.UUID `gorm:"type:uuid;not null;index" json:"user_id"`
	Action         string    `gorm:"type:varchar(20);not null" json:"action"` // VIEW, DOWNLOAD, EDIT, DELETE, SHARE
	IPAddress      string    `gorm:"type:varchar(45)" json:"ip_address"`
	UserAgent      string    `gorm:"type:varchar(500)" json:"user_agent"`
	AccessTime     time.Time `gorm:"type:timestamp;not null;default:CURRENT_TIMESTAMP" json:"access_time"`
	AdditionalInfo string    `gorm:"type:jsonb" json:"additional_info"`
}

func (DocumentAccessLog) TableName() string {
	return "document_access_logs"
}

// DocumentShare represents document sharing information
type DocumentShare struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	DocumentID  uuid.UUID  `gorm:"type:uuid;not null;index" json:"document_id"`
	SharedWith  uuid.UUID  `gorm:"type:uuid;not null;index" json:"shared_with"` // User or group ID
	SharedBy    uuid.UUID  `gorm:"type:uuid;not null" json:"shared_by"`
	ShareType   string     `gorm:"type:varchar(20);not null" json:"share_type"` // USER, GROUP, DEPARTMENT
	Permission  string     `gorm:"type:varchar(20);not null" json:"permission"` // VIEW, EDIT, DOWNLOAD
	ExpiresAt   *time.Time `gorm:"type:timestamp" json:"expires_at"`
	AccessCount int        `gorm:"default:0" json:"access_count"`
	IsActive    bool       `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (DocumentShare) TableName() string {
	return "document_shares"
}

// AccreditationDocument represents documents specifically for accreditation
type AccreditationDocument struct {
	ID                uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	DocumentID        uuid.UUID  `gorm:"type:uuid;not null;uniqueIndex" json:"document_id"`
	AccreditationType string     `gorm:"type:varchar(50);not null" json:"accreditation_type"` // A, B, C
	StandardNumber    string     `gorm:"type:varchar(50);not null" json:"standard_number"`
	StandardComponent string     `gorm:"type:varchar(100);not null" json:"standard_component"`
	EvidenceType      string     `gorm:"type:varchar(50);not null" json:"evidence_type"`
	ComplianceStatus  string     `gorm:"type:varchar(20);not null" json:"compliance_status"` // COMPLIANT, PARTIALLY_COMPLIANT, NON_COMPLIANT
	AssessorNotes     string     `gorm:"type:text" json:"assessor_notes"`
	VerificationDate  *time.Time `gorm:"type:timestamp" json:"verification_date"`
	NextReviewDate    *time.Time `gorm:"type:timestamp" json:"next_review_date"`
	IsMandatory       bool       `gorm:"default:false" json:"is_mandatory"`

	common.Auditable
}

func (AccreditationDocument) TableName() string {
	return "accreditation_documents"
}

// Helper functions

func IsValidDocumentCategory(category string) bool {
	validCategories := map[string]bool{
		DocumentCategoryGeneral:        true,
		DocumentCategoryAccreditation:  true,
		DocumentCategoryCurriculum:     true,
		DocumentCategoryAssessment:     true,
		DocumentCategoryAdministration: true,
		DocumentCategoryFinance:        true,
		DocumentCategoryHR:             true,
		DocumentCategoryLegal:          true,
		DocumentCategoryStudent:        true,
		DocumentCategoryTeacher:        true,
		DocumentCategoryPolicy:         true,
		DocumentCategoryReport:         true,
	}
	return validCategories[category]
}

func IsValidDocumentType(docType string) bool {
	validTypes := map[string]bool{
		DocumentTypePDF:     true,
		DocumentTypeDOC:     true,
		DocumentTypeDOCX:    true,
		DocumentTypeXLS:     true,
		DocumentTypeXLSX:    true,
		DocumentTypePPT:     true,
		DocumentTypePPTX:    true,
		DocumentTypeImage:   true,
		DocumentTypeVideo:   true,
		DocumentTypeAudio:   true,
		DocumentTypeArchive: true,
		DocumentTypeOther:   true,
	}
	return validTypes[docType]
}

func IsValidDocumentStatus(status string) bool {
	validStatuses := map[string]bool{
		DocumentStatusDraft:     true,
		DocumentStatusPending:   true,
		DocumentStatusApproved:  true,
		DocumentStatusRejected:  true,
		DocumentStatusArchived:  true,
		DocumentStatusPublished: true,
	}
	return validStatuses[status]
}

func IsValidAccessLevel(level string) bool {
	validLevels := map[string]bool{
		AccessLevelPublic:     true,
		AccessLevelInternal:   true,
		AccessLevelPrivate:    true,
		AccessLevelRestricted: true,
	}
	return validLevels[level]
}
