package portfolio

import (
	"fmt"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Repository interface {
	// Portfolio operations
	CreatePortfolio(portfolio *Portfolio) error
	GetPortfolioByID(id uuid.UUID) (*Portfolio, error)
	GetPortfolios(filter map[string]interface{}) ([]Portfolio, error)
	UpdatePortfolio(portfolio *Portfolio) error
	DeletePortfolio(id uuid.UUID) error
	GetStudentPortfolios(studentID uuid.UUID) ([]Portfolio, error)

	// PortfolioArtifact operations
	CreateArtifact(artifact *PortfolioArtifact) error
	GetArtifactByID(id uuid.UUID) (*PortfolioArtifact, error)
	GetArtifacts(filter map[string]interface{}) ([]PortfolioArtifact, error)
	UpdateArtifact(artifact *PortfolioArtifact) error
	DeleteArtifact(id uuid.UUID) error
	GetPortfolioArtifacts(portfolioID uuid.UUID) ([]PortfolioArtifact, error)

	// LearningEvidence operations
	CreateLearningEvidence(evidence *LearningEvidence) error
	GetLearningEvidenceByID(id uuid.UUID) (*LearningEvidence, error)
	GetLearningEvidence(filter map[string]interface{}) ([]LearningEvidence, error)
	UpdateLearningEvidence(evidence *LearningEvidence) error
	DeleteLearningEvidence(id uuid.UUID) error
	GetStudentLearningEvidence(studentID uuid.UUID) ([]LearningEvidence, error)

	// PortfolioReview operations
	CreateReview(review *PortfolioReview) error
	GetReviewByID(id uuid.UUID) (*PortfolioReview, error)
	GetReviews(filter map[string]interface{}) ([]PortfolioReview, error)
	UpdateReview(review *PortfolioReview) error
	DeleteReview(id uuid.UUID) error
	GetPortfolioReviews(portfolioID uuid.UUID) ([]PortfolioReview, error)

	// Analytics operations
	GetPortfolioAnalytics(request PortfolioAnalyticsRequest) (*PortfolioAnalyticsResponse, error)
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

// Portfolio operations
func (r *repository) CreatePortfolio(portfolio *Portfolio) error {
	return r.db.Create(portfolio).Error
}

func (r *repository) GetPortfolioByID(id uuid.UUID) (*Portfolio, error) {
	var portfolio Portfolio
	err := r.db.Preload("Student").Preload("Artifacts").Where("id = ? AND deleted_at IS NULL", id).First(&portfolio).Error
	if err != nil {
		return nil, err
	}
	return &portfolio, nil
}

func (r *repository) GetPortfolios(filter map[string]interface{}) ([]Portfolio, error) {
	var portfolios []Portfolio
	query := r.db.Preload("Student").Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Order("created_at DESC").Find(&portfolios).Error
	return portfolios, err
}

func (r *repository) UpdatePortfolio(portfolio *Portfolio) error {
	return r.db.Save(portfolio).Error
}

func (r *repository) DeletePortfolio(id uuid.UUID) error {
	return r.db.Model(&Portfolio{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *repository) GetStudentPortfolios(studentID uuid.UUID) ([]Portfolio, error) {
	var portfolios []Portfolio
	err := r.db.Preload("Student").Preload("Artifacts").Where("student_id = ? AND deleted_at IS NULL", studentID).Order("created_at DESC").Find(&portfolios).Error
	return portfolios, err
}

// PortfolioArtifact operations
func (r *repository) CreateArtifact(artifact *PortfolioArtifact) error {
	return r.db.Create(artifact).Error
}

func (r *repository) GetArtifactByID(id uuid.UUID) (*PortfolioArtifact, error) {
	var artifact PortfolioArtifact
	err := r.db.Preload("Portfolio").Where("id = ? AND deleted_at IS NULL", id).First(&artifact).Error
	if err != nil {
		return nil, err
	}
	return &artifact, nil
}

func (r *repository) GetArtifacts(filter map[string]interface{}) ([]PortfolioArtifact, error) {
	var artifacts []PortfolioArtifact
	query := r.db.Preload("Portfolio").Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Order("display_order ASC, created_at DESC").Find(&artifacts).Error
	return artifacts, err
}

func (r *repository) UpdateArtifact(artifact *PortfolioArtifact) error {
	return r.db.Save(artifact).Error
}

func (r *repository) DeleteArtifact(id uuid.UUID) error {
	return r.db.Model(&PortfolioArtifact{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *repository) GetPortfolioArtifacts(portfolioID uuid.UUID) ([]PortfolioArtifact, error) {
	var artifacts []PortfolioArtifact
	err := r.db.Where("portfolio_id = ? AND deleted_at IS NULL", portfolioID).Order("display_order ASC, created_at DESC").Find(&artifacts).Error
	return artifacts, err
}

// LearningEvidence operations
func (r *repository) CreateLearningEvidence(evidence *LearningEvidence) error {
	return r.db.Create(evidence).Error
}

func (r *repository) GetLearningEvidenceByID(id uuid.UUID) (*LearningEvidence, error) {
	var evidence LearningEvidence
	err := r.db.Preload("Student").Where("id = ? AND deleted_at IS NULL", id).First(&evidence).Error
	if err != nil {
		return nil, err
	}
	return &evidence, nil
}

func (r *repository) GetLearningEvidence(filter map[string]interface{}) ([]LearningEvidence, error) {
	var evidence []LearningEvidence
	query := r.db.Preload("Student").Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Order("evidence_date DESC, created_at DESC").Find(&evidence).Error
	return evidence, err
}

func (r *repository) UpdateLearningEvidence(evidence *LearningEvidence) error {
	return r.db.Save(evidence).Error
}

func (r *repository) DeleteLearningEvidence(id uuid.UUID) error {
	return r.db.Model(&LearningEvidence{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *repository) GetStudentLearningEvidence(studentID uuid.UUID) ([]LearningEvidence, error) {
	var evidence []LearningEvidence
	err := r.db.Preload("Student").Where("student_id = ? AND deleted_at IS NULL", studentID).Order("evidence_date DESC, created_at DESC").Find(&evidence).Error
	return evidence, err
}

// PortfolioReview operations
func (r *repository) CreateReview(review *PortfolioReview) error {
	return r.db.Create(review).Error
}

func (r *repository) GetReviewByID(id uuid.UUID) (*PortfolioReview, error) {
	var review PortfolioReview
	err := r.db.Where("id = ? AND deleted_at IS NULL", id).First(&review).Error
	if err != nil {
		return nil, err
	}
	return &review, nil
}

func (r *repository) GetReviews(filter map[string]interface{}) ([]PortfolioReview, error) {
	var reviews []PortfolioReview
	query := r.db.Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Order("review_date DESC, created_at DESC").Find(&reviews).Error
	return reviews, err
}

func (r *repository) UpdateReview(review *PortfolioReview) error {
	return r.db.Save(review).Error
}

func (r *repository) DeleteReview(id uuid.UUID) error {
	return r.db.Model(&PortfolioReview{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *repository) GetPortfolioReviews(portfolioID uuid.UUID) ([]PortfolioReview, error) {
	var reviews []PortfolioReview
	err := r.db.Where("portfolio_id = ? AND deleted_at IS NULL", portfolioID).Order("review_date DESC, created_at DESC").Find(&reviews).Error
	return reviews, err
}

// Analytics operations
func (r *repository) GetPortfolioAnalytics(request PortfolioAnalyticsRequest) (*PortfolioAnalyticsResponse, error) {
	response := &PortfolioAnalyticsResponse{}

	// Base query for portfolios
	baseQuery := r.db.Model(&Portfolio{}).Where("deleted_at IS NULL")

	// Apply filters
	if request.StudentID != nil {
		baseQuery = baseQuery.Where("student_id = ?", *request.StudentID)
	}
	if request.Period != nil {
		baseQuery = baseQuery.Where("period = ?", *request.Period)
	}
	if request.AcademicYearID != nil {
		baseQuery = baseQuery.Where("academic_year_id = ?", *request.AcademicYearID)
	}
	if request.PortfolioType != nil {
		baseQuery = baseQuery.Where("portfolio_type = ?", *request.PortfolioType)
	}

	// Get total portfolios
	baseQuery.Count(&response.TotalPortfolios)

	// Get published portfolios
	var publishedCount int64
	publishedQuery := r.db.Model(&Portfolio{}).Where("is_published = true AND deleted_at IS NULL")
	if request.StudentID != nil {
		publishedQuery = publishedQuery.Where("student_id = ?", *request.StudentID)
	}
	if request.AcademicYearID != nil {
		publishedQuery = publishedQuery.Where("academic_year_id = ?", *request.AcademicYearID)
	}
	publishedQuery.Count(&publishedCount)
	response.PublishedPortfolios = publishedCount

	// Get total artifacts
	artifactQuery := r.db.Model(&PortfolioArtifact{}).Where("deleted_at IS NULL")
	if request.StudentID != nil {
		artifactQuery = artifactQuery.Where("portfolio_id IN (SELECT id FROM portfolios WHERE student_id = ? AND deleted_at IS NULL)", *request.StudentID)
	}
	artifactQuery.Count(&response.TotalArtifacts)

	// Calculate average artifacts per portfolio
	if response.TotalPortfolios > 0 {
		response.AverageArtifacts = float64(response.TotalArtifacts) / float64(response.TotalPortfolios)
	}

	// Get statistics by portfolio type
	typeStatsQuery := r.db.Model(&Portfolio{}).
		Select("portfolio_type, COUNT(*) as count").
		Where("deleted_at IS NULL")

	if request.StudentID != nil {
		typeStatsQuery = typeStatsQuery.Where("student_id = ?", *request.StudentID)
	}
	if request.AcademicYearID != nil {
		typeStatsQuery = typeStatsQuery.Where("academic_year_id = ?", *request.AcademicYearID)
	}

	typeStatsQuery.Group("portfolio_type")

	typeStats := []struct {
		PortfolioType string
		Count         int64
	}{}

	typeStatsQuery.Scan(&typeStats)

	totalCount := response.TotalPortfolios
	for _, stat := range typeStats {
		percentage := float64(0)
		if totalCount > 0 {
			percentage = float64(stat.Count) / float64(totalCount) * 100
		}
		response.ByPortfolioType = append(response.ByPortfolioType, PortfolioTypeStats{
			PortfolioType: stat.PortfolioType,
			TypeName:      GetPortfolioTypeDescription(stat.PortfolioType),
			Count:         stat.Count,
			Percentage:    percentage,
		})
	}

	// Get statistics by artifact type
	artifactTypeStatsQuery := r.db.Model(&PortfolioArtifact{}).
		Select("artifact_type, COUNT(*) as count").
		Where("deleted_at IS NULL")

	if request.StudentID != nil {
		artifactTypeStatsQuery = artifactTypeStatsQuery.Where("portfolio_id IN (SELECT id FROM portfolios WHERE student_id = ? AND deleted_at IS NULL)", *request.StudentID)
	}

	artifactTypeStatsQuery.Group("artifact_type")

	artifactTypeStats := []struct {
		ArtifactType string
		Count        int64
	}{}

	artifactTypeStatsQuery.Scan(&artifactTypeStats)

	totalArtifacts := response.TotalArtifacts
	for _, stat := range artifactTypeStats {
		percentage := float64(0)
		if totalArtifacts > 0 {
			percentage = float64(stat.Count) / float64(totalArtifacts) * 100
		}
		response.ByArtifactType = append(response.ByArtifactType, ArtifactTypeStats{
			ArtifactType: stat.ArtifactType,
			TypeName:     GetArtifactTypeDescription(stat.ArtifactType),
			Count:        stat.Count,
			Percentage:   percentage,
		})
	}

	return response, nil
}
