package portfolio

import (
	"time"

	"sim-sekolah/internal/common"
	"sim-sekolah/internal/student"

	"github.com/google/uuid"
)

// Portfolio Types
const (
	PortfolioTypeStudent   = "STUDENT"   // Individual student portfolio
	PortfolioTypeProject   = "PROJECT"   // Project-based portfolio
	PortfolioTypeSubject   = "SUBJECT"   // Subject-specific portfolio
	PortfolioTypeCharacter = "CHARACTER" // Character development portfolio
)

// Artifact Types
const (
	ArtifactTypeDocument    = "DOCUMENT"    // Documents, worksheets
	ArtifactTypeImage       = "IMAGE"       // Photos, drawings
	ArtifactTypeVideo       = "VIDEO"       // Video recordings
	ArtifactTypeAudio       = "AUDIO"       // Audio recordings
	ArtifactTypeProject     = "PROJECT"     // Project outputs
	ArtifactTypeAssessment  = "ASSESSMENT"  // Assessment results
	ArtifactTypeReflection  = "REFLECTION"  // Student reflections
	ArtifactTypeCertificate = "CERTIFICATE" // Certificates, awards
)

// Portfolio represents student learning portfolio
type Portfolio struct {
	ID             uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID      uuid.UUID  `gorm:"type:uuid;not null;index" json:"student_id"`
	PortfolioType  string     `gorm:"type:varchar(20);not null" json:"portfolio_type"`
	Title          string     `gorm:"type:varchar(200);not null" json:"title"`
	Description    string     `gorm:"type:text" json:"description"`
	SubjectID      *uuid.UUID `gorm:"type:uuid;index" json:"subject_id,omitempty"`
	ProjectID      *uuid.UUID `gorm:"type:uuid;index" json:"project_id,omitempty"`
	Period         string     `gorm:"type:varchar(20)" json:"period"` // SEMESTER_1, SEMESTER_2
	AcademicYearID uuid.UUID  `gorm:"type:uuid;not null;index" json:"academic_year_id"`
	TeacherID      uuid.UUID  `gorm:"type:uuid" json:"teacher_id"`
	IsPublished    bool       `gorm:"default:false" json:"is_published"`
	PublishedAt    *time.Time `gorm:"type:timestamp" json:"published_at,omitempty"`

	common.Auditable

	Student   *student.MasterStudent `gorm:"foreignKey:StudentID" json:"student,omitempty"`
	Artifacts []PortfolioArtifact    `gorm:"foreignKey:PortfolioID" json:"artifacts,omitempty"`
}

func (Portfolio) TableName() string {
	return "portfolios"
}

// PortfolioArtifact represents individual artifacts within a portfolio
type PortfolioArtifact struct {
	ID              uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	PortfolioID     uuid.UUID `gorm:"type:uuid;not null;index" json:"portfolio_id"`
	ArtifactType    string    `gorm:"type:varchar(20);not null" json:"artifact_type"`
	Title           string    `gorm:"type:varchar(200);not null" json:"title"`
	Description     string    `gorm:"type:text" json:"description"`
	FileURL         string    `gorm:"type:varchar(500)" json:"file_url"`
	FileName        string    `gorm:"type:varchar(255)" json:"file_name"`
	FileSize        int64     `gorm:"type:bigint" json:"file_size"`
	FileType        string    `gorm:"type:varchar(50)" json:"file_type"`
	ThumbnailURL    string    `gorm:"type:varchar(500)" json:"thumbnail_url"`
	CompetencyIDs   string    `gorm:"type:text" json:"competency_ids"` // JSON array of competency IDs
	Skills          string    `gorm:"type:text" json:"skills"`         // JSON array of skills demonstrated
	Reflection      string    `gorm:"type:text" json:"reflection"`
	TeacherFeedback string    `gorm:"type:text" json:"teacher_feedback"`
	TeacherID       uuid.UUID `gorm:"type:uuid" json:"teacher_id"`
	IsFeatured      bool      `gorm:"default:false" json:"is_featured"`
	DisplayOrder    int       `gorm:"default:0" json:"display_order"`

	common.Auditable

	Portfolio *Portfolio `gorm:"foreignKey:PortfolioID" json:"portfolio,omitempty"`
}

func (PortfolioArtifact) TableName() string {
	return "portfolio_artifacts"
}

// LearningEvidence represents evidence of learning linked to competencies
type LearningEvidence struct {
	ID               uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID        uuid.UUID  `gorm:"type:uuid;not null;index" json:"student_id"`
	ArtifactID       uuid.UUID  `gorm:"type:uuid;not null;index" json:"artifact_id"`
	CompetencyID     uuid.UUID  `gorm:"type:uuid;not null;index" json:"competency_id"`
	CompetencyType   string     `gorm:"type:varchar(20);not null" json:"competency_type"` // CP, TP, PROJECT
	EvidenceDate     time.Time  `gorm:"type:date;not null" json:"evidence_date"`
	MasteryLevel     string     `gorm:"type:varchar(20);not null" json:"mastery_level"` // BELUM, SEDANG, MENGUASAI
	TeacherID        uuid.UUID  `gorm:"type:uuid" json:"teacher_id"`
	ValidationStatus string     `gorm:"type:varchar(20);not null;default:PENDING" json:"validation_status"` // PENDING, APPROVED, REJECTED
	ValidationNotes  string     `gorm:"type:text" json:"validation_notes"`
	ValidatedBy      uuid.UUID  `gorm:"type:uuid" json:"validated_by"`
	ValidatedAt      *time.Time `gorm:"type:timestamp" json:"validated_at"`

	common.Auditable

	Student *student.MasterStudent `gorm:"foreignKey:StudentID" json:"student,omitempty"`
}

func (LearningEvidence) TableName() string {
	return "learning_evidence"
}

// PortfolioReview represents teacher review of student portfolio
type PortfolioReview struct {
	ID                  uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	PortfolioID         uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_portfolio_reviewer" json:"portfolio_id"`
	ReviewerID          uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_portfolio_reviewer" json:"reviewer_id"`
	ReviewDate          time.Time `gorm:"type:date;not null" json:"review_date"`
	OverallRating       int       `gorm:"type:int;check:overall_rating >= 1 AND overall_rating <= 5" json:"overall_rating"`
	Strengths           string    `gorm:"type:text" json:"strengths"`
	AreasForImprovement string    `gorm:"type:text" json:"areas_for_improvement"`
	Recommendations     string    `gorm:"type:text" json:"recommendations"`
	IsFormal            bool      `gorm:"default:false" json:"is_formal"`

	common.Auditable
}

func (PortfolioReview) TableName() string {
	return "portfolio_reviews"
}

// GetPortfolioTypeDescription returns Indonesian description of portfolio type
func GetPortfolioTypeDescription(portfolioType string) string {
	descriptions := map[string]string{
		PortfolioTypeStudent:   "Portofolio Siswa",
		PortfolioTypeProject:   "Portofolio Proyek",
		PortfolioTypeSubject:   "Portofolio Mata Pelajaran",
		PortfolioTypeCharacter: "Portofolio Karakter",
	}
	return descriptions[portfolioType]
}

// GetArtifactTypeDescription returns Indonesian description of artifact type
func GetArtifactTypeDescription(artifactType string) string {
	descriptions := map[string]string{
		ArtifactTypeDocument:    "Dokumen",
		ArtifactTypeImage:       "Gambar",
		ArtifactTypeVideo:       "Video",
		ArtifactTypeAudio:       "Audio",
		ArtifactTypeProject:     "Proyek",
		ArtifactTypeAssessment:  "Asesmen",
		ArtifactTypeReflection:  "Refleksi",
		ArtifactTypeCertificate: "Sertifikat/Penghargaan",
	}
	return descriptions[artifactType]
}

// IsValidPortfolioType validates portfolio type
func IsValidPortfolioType(portfolioType string) bool {
	validTypes := map[string]bool{
		PortfolioTypeStudent:   true,
		PortfolioTypeProject:   true,
		PortfolioTypeSubject:   true,
		PortfolioTypeCharacter: true,
	}
	return validTypes[portfolioType]
}

// IsValidArtifactType validates artifact type
func IsValidArtifactType(artifactType string) bool {
	validTypes := map[string]bool{
		ArtifactTypeDocument:    true,
		ArtifactTypeImage:       true,
		ArtifactTypeVideo:       true,
		ArtifactTypeAudio:       true,
		ArtifactTypeProject:     true,
		ArtifactTypeAssessment:  true,
		ArtifactTypeReflection:  true,
		ArtifactTypeCertificate: true,
	}
	return validTypes[artifactType]
}
