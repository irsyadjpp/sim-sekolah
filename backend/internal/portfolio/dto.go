package portfolio

import (
	"time"

	"github.com/google/uuid"
)

// PortfolioRequest represents request body for creating/updating portfolio
type PortfolioRequest struct {
	StudentID      uuid.UUID  `json:"student_id" validate:"required"`
	PortfolioType  string     `json:"portfolio_type" validate:"required"`
	Title          string     `json:"title" validate:"required"`
	Description    string     `json:"description"`
	SubjectID      *uuid.UUID `json:"subject_id"`
	ProjectID      *uuid.UUID `json:"project_id"`
	Period         string     `json:"period"`
	AcademicYearID uuid.UUID  `json:"academic_year_id" validate:"required"`
	TeacherID      uuid.UUID  `json:"teacher_id"`
	IsPublished    *bool      `json:"is_published"`
}

// PortfolioResponse represents response body for portfolio
type PortfolioResponse struct {
	ID             uuid.UUID                   `json:"id"`
	StudentID      uuid.UUID                   `json:"student_id"`
	StudentName    string                      `json:"student_name,omitempty"`
	PortfolioType  string                      `json:"portfolio_type"`
	TypeName       string                      `json:"type_name,omitempty"`
	Title          string                      `json:"title"`
	Description    string                      `json:"description"`
	SubjectID      *uuid.UUID                  `json:"subject_id"`
	ProjectID      *uuid.UUID                  `json:"project_id"`
	Period         string                      `json:"period"`
	PeriodName     string                      `json:"period_name,omitempty"`
	AcademicYearID uuid.UUID                   `json:"academic_year_id"`
	TeacherID      uuid.UUID                   `json:"teacher_id"`
	TeacherName    string                      `json:"teacher_name,omitempty"`
	IsPublished    bool                        `json:"is_published"`
	PublishedAt    *time.Time                  `json:"published_at"`
	CreatedAt      time.Time                   `json:"created_at"`
	UpdatedAt      time.Time                   `json:"updated_at"`
	ArtifactCount  int                         `json:"artifact_count,omitempty"`
	Artifacts      []PortfolioArtifactResponse `json:"artifacts,omitempty"`
}

// PortfolioArtifactRequest represents request body for creating/updating portfolio artifact
type PortfolioArtifactRequest struct {
	PortfolioID     uuid.UUID `json:"portfolio_id" validate:"required"`
	ArtifactType    string    `json:"artifact_type" validate:"required"`
	Title           string    `json:"title" validate:"required"`
	Description     string    `json:"description"`
	FileURL         string    `json:"file_url"`
	FileName        string    `json:"file_name"`
	FileSize        int64     `json:"file_size"`
	FileType        string    `json:"file_type"`
	ThumbnailURL    string    `json:"thumbnail_url"`
	CompetencyIDs   string    `json:"competency_ids"`
	Skills          string    `json:"skills"`
	Reflection      string    `json:"reflection"`
	TeacherFeedback string    `json:"teacher_feedback"`
	TeacherID       uuid.UUID `json:"teacher_id"`
	IsFeatured      *bool     `json:"is_featured"`
	DisplayOrder    *int      `json:"display_order"`
}

// PortfolioArtifactResponse represents response body for portfolio artifact
type PortfolioArtifactResponse struct {
	ID              uuid.UUID `json:"id"`
	PortfolioID     uuid.UUID `json:"portfolio_id"`
	PortfolioTitle  string    `json:"portfolio_title,omitempty"`
	ArtifactType    string    `json:"artifact_type"`
	TypeName        string    `json:"type_name,omitempty"`
	Title           string    `json:"title"`
	Description     string    `json:"description"`
	FileURL         string    `json:"file_url"`
	FileName        string    `json:"file_name"`
	FileSize        int64     `json:"file_size"`
	FileType        string    `json:"file_type"`
	ThumbnailURL    string    `json:"thumbnail_url"`
	CompetencyIDs   string    `json:"competency_ids"`
	Skills          string    `json:"skills"`
	Reflection      string    `json:"reflection"`
	TeacherFeedback string    `json:"teacher_feedback"`
	TeacherID       uuid.UUID `json:"teacher_id"`
	TeacherName     string    `json:"teacher_name,omitempty"`
	IsFeatured      bool      `json:"is_featured"`
	DisplayOrder    int       `json:"display_order"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
}

// LearningEvidenceRequest represents request body for creating/updating learning evidence
type LearningEvidenceRequest struct {
	StudentID        uuid.UUID `json:"student_id" validate:"required"`
	ArtifactID       uuid.UUID `json:"artifact_id" validate:"required"`
	CompetencyID     uuid.UUID `json:"competency_id" validate:"required"`
	CompetencyType   string    `json:"competency_type" validate:"required"`
	EvidenceDate     time.Time `json:"evidence_date" validate:"required"`
	MasteryLevel     string    `json:"mastery_level" validate:"required"`
	TeacherID        uuid.UUID `json:"teacher_id"`
	ValidationStatus string    `json:"validation_status"`
	ValidationNotes  string    `json:"validation_notes"`
	ValidatedBy      uuid.UUID `json:"validated_by"`
}

// LearningEvidenceResponse represents response body for learning evidence
type LearningEvidenceResponse struct {
	ID               uuid.UUID  `json:"id"`
	StudentID        uuid.UUID  `json:"student_id"`
	StudentName      string     `json:"student_name,omitempty"`
	ArtifactID       uuid.UUID  `json:"artifact_id"`
	ArtifactTitle    string     `json:"artifact_title,omitempty"`
	CompetencyID     uuid.UUID  `json:"competency_id"`
	CompetencyName   string     `json:"competency_name,omitempty"`
	CompetencyType   string     `json:"competency_type"`
	EvidenceDate     time.Time  `json:"evidence_date"`
	MasteryLevel     string     `json:"mastery_level"`
	LevelName        string     `json:"level_name,omitempty"`
	TeacherID        uuid.UUID  `json:"teacher_id"`
	TeacherName      string     `json:"teacher_name,omitempty"`
	ValidationStatus string     `json:"validation_status"`
	StatusName       string     `json:"status_name,omitempty"`
	ValidationNotes  string     `json:"validation_notes"`
	ValidatedBy      uuid.UUID  `json:"validated_by"`
	ValidatorName    string     `json:"validator_name,omitempty"`
	ValidatedAt      *time.Time `json:"validated_at"`
	CreatedAt        time.Time  `json:"created_at"`
	UpdatedAt        time.Time  `json:"updated_at"`
}

// PortfolioReviewRequest represents request body for creating/updating portfolio review
type PortfolioReviewRequest struct {
	PortfolioID         uuid.UUID `json:"portfolio_id" validate:"required"`
	ReviewerID          uuid.UUID `json:"reviewer_id" validate:"required"`
	ReviewDate          time.Time `json:"review_date" validate:"required"`
	OverallRating       int       `json:"overall_rating" validate:"min=1,max=5"`
	Strengths           string    `json:"strengths"`
	AreasForImprovement string    `json:"areas_for_improvement"`
	Recommendations     string    `json:"recommendations"`
	IsFormal            bool      `json:"is_formal"`
}

// PortfolioReviewResponse represents response body for portfolio review
type PortfolioReviewResponse struct {
	ID                  uuid.UUID `json:"id"`
	PortfolioID         uuid.UUID `json:"portfolio_id"`
	PortfolioTitle      string    `json:"portfolio_title,omitempty"`
	ReviewerID          uuid.UUID `json:"reviewer_id"`
	ReviewerName        string    `json:"reviewer_name,omitempty"`
	ReviewDate          time.Time `json:"review_date"`
	OverallRating       int       `json:"overall_rating"`
	Strengths           string    `json:"strengths"`
	AreasForImprovement string    `json:"areas_for_improvement"`
	Recommendations     string    `json:"recommendations"`
	IsFormal            bool      `json:"is_formal"`
	CreatedAt           time.Time `json:"created_at"`
	UpdatedAt           time.Time `json:"updated_at"`
}

// PortfolioAnalyticsRequest represents request for portfolio analytics
type PortfolioAnalyticsRequest struct {
	StudentID      *uuid.UUID `json:"student_id,omitempty"`
	ClassroomID    *uuid.UUID `json:"classroom_id,omitempty"`
	Period         *string    `json:"period,omitempty"`
	AcademicYearID *uuid.UUID `json:"academic_year_id,omitempty"`
	PortfolioType  *string    `json:"portfolio_type,omitempty"`
}

// PortfolioAnalyticsResponse represents portfolio analytics data
type PortfolioAnalyticsResponse struct {
	TotalPortfolios     int64                     `json:"total_portfolios"`
	TotalArtifacts      int64                     `json:"total_artifacts"`
	PublishedPortfolios int64                     `json:"total_published"`
	AverageArtifacts    float64                   `json:"average_artifacts_per_portfolio"`
	ByPortfolioType     []PortfolioTypeStats      `json:"by_portfolio_type"`
	ByArtifactType      []ArtifactTypeStats       `json:"by_artifact_type"`
	RecentActivity      []RecentPortfolioActivity `json:"recent_activity,omitempty"`
	TopPortfolios       []PortfolioStats          `json:"top_portfolios,omitempty"`
}

// PortfolioTypeStats represents statistics by portfolio type
type PortfolioTypeStats struct {
	PortfolioType string  `json:"portfolio_type"`
	TypeName      string  `json:"type_name"`
	Count         int64   `json:"count"`
	Percentage    float64 `json:"percentage"`
}

// ArtifactTypeStats represents statistics by artifact type
type ArtifactTypeStats struct {
	ArtifactType string  `json:"artifact_type"`
	TypeName     string  `json:"type_name"`
	Count        int64   `json:"count"`
	Percentage   float64 `json:"percentage"`
}

// RecentPortfolioActivity represents recent portfolio activity
type RecentPortfolioActivity struct {
	ActivityID   uuid.UUID `json:"activity_id"`
	ActivityType string    `json:"activity_type"` // CREATED, UPDATED, PUBLISHED
	PortfolioID  uuid.UUID `json:"portfolio_id"`
	Title        string    `json:"title"`
	StudentName  string    `json:"student_name"`
	Timestamp    time.Time `json:"timestamp"`
}

// PortfolioStats represents portfolio statistics
type PortfolioStats struct {
	PortfolioID   uuid.UUID `json:"portfolio_id"`
	Title         string    `json:"title"`
	StudentName   string    `json:"student_name"`
	ArtifactCount int       `json:"artifact_count"`
	ViewCount     int       `json:"view_count"`
	AverageRating float64   `json:"average_rating"`
}
