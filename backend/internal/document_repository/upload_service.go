package document_repository

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io"
	"mime/multipart"
	"path/filepath"
	"strings"
	"time"

	"sim-sekolah/config"

	"github.com/aws/aws-sdk-go-v2/aws"
	awsconfig "github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

// UploadService handles file uploads and storage operations
type UploadService struct {
	repo       *Repository
	s3Client   *s3.Client
	bucketName string
}

// NewUploadService creates a new upload service
func NewUploadService(repo *Repository) (*UploadService, error) {
	// Initialize AWS SDK for SeaweedFS S3
	cfg, err := awsconfig.LoadDefaultConfig(context.Background(),
		awsconfig.WithEndpointResolverWithOptions(aws.EndpointResolverWithOptionsFunc(
			func(service, region string, options ...interface{}) (aws.Endpoint, error) {
				return aws.Endpoint{
					URL:               config.Cfg.Storage.SeaweedFSS3Endpoint,
					SigningRegion:     config.Cfg.Storage.SeaweedFSRegion,
					HostnameImmutable: true,
				}, nil
			},
		)),
		awsconfig.WithCredentialsProvider(aws.CredentialsProviderFunc(
			func(ctx context.Context) (aws.Credentials, error) {
				return aws.Credentials{
					AccessKeyID:     config.Cfg.Storage.SeaweedFSAccessKey,
					SecretAccessKey: config.Cfg.Storage.SeaweedFSSecretKey,
				}, nil
			},
		)),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to configure AWS SDK: %w", err)
	}

	s3Client := s3.NewFromConfig(cfg)

	return &UploadService{
		repo:       repo,
		s3Client:   s3Client,
		bucketName: config.Cfg.Storage.SeaweedFSBucket,
	}, nil
}

// CalculateFileHash calculates SHA-256 hash of file content
func CalculateFileHash(file io.Reader) (string, error) {
	hash := sha256.New()
	if _, err := io.Copy(hash, file); err != nil {
		return "", err
	}
	return hex.EncodeToString(hash.Sum(nil)), nil
}

// GetStorageFolderPath returns the folder path based on document category
func GetStorageFolderPath(category string) string {
	switch category {
	case DocumentCategoryCurriculum:
		return "curriculum/buku-pelajaran"
	case DocumentCategoryAssessment:
		return "assessment/ujian-dan-tugas"
	case DocumentCategoryGeneral:
		return "general/dokumen-umum"
	case DocumentCategoryAccreditation:
		return "accreditation/dokumen-akreditasi"
	case DocumentCategoryAdministration:
		return "administration/administrasi"
	case DocumentCategoryFinance:
		return "finance/keuangan"
	case DocumentCategoryHR:
		return "hr/sdm"
	case DocumentCategoryLegal:
		return "legal/dokumen-hukum"
	case DocumentCategoryStudent:
		return "student/siswa"
	case DocumentCategoryTeacher:
		return "teacher/guru"
	case DocumentCategoryPolicy:
		return "policy/kebijakan"
	case DocumentCategoryReport:
		return "report/laporan"
	default:
		return "general/other"
	}
}

// CheckDuplicateDocument checks if a document with the same hash or metadata already exists
func (s *UploadService) CheckDuplicateDocument(ctx context.Context, schoolID uuid.UUID, fileHash, title, documentNumber string) (*Document, error) {
	// Check by file hash (most reliable duplicate detection)
	if fileHash != "" {
		var existingDoc Document
		err := s.repo.db.WithContext(ctx).
			Where("school_id = ? AND file_hash = ?", schoolID, fileHash).
			First(&existingDoc).Error
		if err == nil {
			return &existingDoc, nil
		}
		if err != gorm.ErrRecordNotFound {
			return nil, fmt.Errorf("error checking for duplicate by hash: %w", err)
		}
	}

	// Check by document number (business identifier)
	if documentNumber != "" {
		var existingDoc Document
		err := s.repo.db.WithContext(ctx).
			Where("school_id = ? AND document_number = ?", schoolID, documentNumber).
			First(&existingDoc).Error
		if err == nil {
			return &existingDoc, nil
		}
		if err != gorm.ErrRecordNotFound {
			return nil, fmt.Errorf("error checking for duplicate by document number: %w", err)
		}
	}

	// Check by title within the same category and type (less strict)
	if title != "" {
		var existingDoc Document
		err := s.repo.db.WithContext(ctx).
			Where("school_id = ? AND title = ? AND status != ?", schoolID, title, "ARCHIVED").
			First(&existingDoc).Error
		if err == nil {
			return &existingDoc, nil
		}
		// Ignore if not found, this is just a warning level check
	}

	return nil, nil
}

// UploadFile uploads a file to SeaweedFS with folder organization
func (s *UploadService) UploadFile(ctx context.Context, fileHeader *multipart.FileHeader, category string) (string, int64, string, error) {
	// Open the file
	file, err := fileHeader.Open()
	if err != nil {
		return "", 0, "", fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	// Calculate file hash for duplicate detection
	fileSeeker, err := fileHeader.Open()
	if err != nil {
		return "", 0, "", fmt.Errorf("failed to open file for hashing: %w", err)
	}
	fileHash, err := CalculateFileHash(fileSeeker)
	fileSeeker.Close()
	if err != nil {
		return "", 0, "", fmt.Errorf("failed to calculate file hash: %w", err)
	}

	// Get file size and content type
	fileSize := fileHeader.Size
	mimeType := fileHeader.Header.Get("Content-Type")
	if mimeType == "" {
		mimeType = "application/octet-stream"
	}

	// Generate unique filename
	ext := filepath.Ext(fileHeader.Filename)
	uniqueFileName := fmt.Sprintf("%s_%s%s", fileHash[:8], time.Now().Format("20060102-150405"), ext)

	// Get folder path based on category
	folderPath := GetStorageFolderPath(category)

	// Create S3 object key
	objectKey := fmt.Sprintf("%s/%s/%s", folderPath, category, uniqueFileName)

	// Reset file reader to beginning
	file, err = fileHeader.Open()
	if err != nil {
		return "", 0, "", fmt.Errorf("failed to reopen file: %w", err)
	}
	defer file.Close()

	// Upload to SeaweedFS via S3 API
	_, err = s.s3Client.PutObject(ctx, &s3.PutObjectInput{
		Bucket:      aws.String(s.bucketName),
		Key:         aws.String(objectKey),
		Body:        file,
		ContentType: aws.String(mimeType),
		Metadata: map[string]string{
			"original-name": fileHeader.Filename,
			"file-hash":     fileHash,
			"upload-time":   time.Now().Format(time.RFC3339),
		},
	})
	if err != nil {
		return "", 0, "", fmt.Errorf("failed to upload file to SeaweedFS: %w", err)
	}

	// Generate file URL
	fileURL := fmt.Sprintf("s3://%s/%s", s.bucketName, objectKey)

	return fileURL, fileSize, fileHash, nil
}

// ValidateMetadata validates document metadata before upload
func (s *UploadService) ValidateMetadata(title, documentNumber, category, documentType string) error {
	if title == "" {
		return fmt.Errorf("document title is required")
	}

	if !IsValidDocumentCategory(category) {
		return fmt.Errorf("invalid document category: %s", category)
	}

	if !IsValidDocumentType(documentType) {
		return fmt.Errorf("invalid document type: %s", documentType)
	}

	// Additional validation for document number format if provided
	if documentNumber != "" {
		if len(documentNumber) < 3 || len(documentNumber) > 50 {
			return fmt.Errorf("document number must be between 3 and 50 characters")
		}
	}

	return nil
}

// UploadDocumentWithMetadata handles the complete upload process with metadata validation
func (s *UploadService) UploadDocumentWithMetadata(
	ctx context.Context,
	fileHeader *multipart.FileHeader,
	title, description, documentNumber, category, documentType, accessLevel string,
	authorID, schoolID uuid.UUID,
) (*Document, error) {
	// Validate metadata
	if err := s.ValidateMetadata(title, documentNumber, category, documentType); err != nil {
		return nil, fmt.Errorf("metadata validation failed: %w", err)
	}

	// Upload file to SeaweedFS
	fileURL, fileSize, fileHash, err := s.UploadFile(ctx, fileHeader, category)
	if err != nil {
		return nil, fmt.Errorf("file upload failed: %w", err)
	}

	// Check for duplicates
	duplicate, err := s.CheckDuplicateDocument(ctx, schoolID, fileHash, title, documentNumber)
	if err != nil {
		return nil, fmt.Errorf("duplicate check failed: %w", err)
	}
	if duplicate != nil {
		return nil, fmt.Errorf("duplicate document found: %s (ID: %s)", duplicate.Title, duplicate.ID)
	}

	// Get MIME type from file header
	mimeType := fileHeader.Header.Get("Content-Type")
	if mimeType == "" {
		mimeType = "application/octet-stream"
	}

	// Determine file type from MIME type
	fileType := s.determineFileTypeFromMime(mimeType)

	// Create document record
	doc := &Document{
		ID:               uuid.New(),
		Title:            title,
		Description:      description,
		DocumentNumber:   documentNumber,
		Category:         category,
		DocumentType:     fileType,
		Status:           DocumentStatusDraft,
		AccessLevel:      accessLevel,
		FileURL:          fileURL,
		FileName:         fileHeader.Filename,
		FileSize:         fileSize,
		FileHash:         fileHash,
		MimeType:         mimeType,
		AuthorID:         authorID,
		SchoolID:         schoolID,
		Version:          1,
		IsCurrentVersion: true,
		StorageLocation:  "seaweedfs",
	}

	// Set default access level if not provided
	if accessLevel == "" {
		doc.AccessLevel = AccessLevelInternal
	}

	// Save to database
	if err := s.repo.CreateDocument(ctx, doc); err != nil {
		return nil, fmt.Errorf("failed to create document record: %w", err)
	}

	return doc, nil
}

// determineFileTypeFromMime determines document type from MIME type
func (s *UploadService) determineFileTypeFromMime(mimeType string) string {
	switch {
	case strings.Contains(mimeType, "pdf"):
		return DocumentTypePDF
	case strings.Contains(mimeType, "word") || strings.Contains(mimeType, "doc"):
		if strings.Contains(mimeType, "docx") || strings.HasSuffix(mimeType, "docx") {
			return DocumentTypeDOCX
		}
		return DocumentTypeDOC
	case strings.Contains(mimeType, "excel") || strings.Contains(mimeType, "sheet"):
		if strings.Contains(mimeType, "xlsx") || strings.HasSuffix(mimeType, "xlsx") {
			return DocumentTypeXLSX
		}
		return DocumentTypeXLS
	case strings.Contains(mimeType, "powerpoint") || strings.Contains(mimeType, "presentation"):
		if strings.Contains(mimeType, "pptx") || strings.HasSuffix(mimeType, "pptx") {
			return DocumentTypePPTX
		}
		return DocumentTypePPT
	case strings.Contains(mimeType, "image"):
		return DocumentTypeImage
	case strings.Contains(mimeType, "video"):
		return DocumentTypeVideo
	case strings.Contains(mimeType, "audio"):
		return DocumentTypeAudio
	default:
		return DocumentTypeOther
	}
}
