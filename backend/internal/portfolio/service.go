package portfolio

import (
	"errors"
	"time"

	"github.com/google/uuid"
)

type Service interface {
	// Portfolio operations
	CreatePortfolio(request PortfolioRequest) (*PortfolioResponse, error)
	GetPortfolioByID(id uuid.UUID) (*PortfolioResponse, error)
	GetPortfolios(filter map[string]interface{}) ([]PortfolioResponse, error)
	UpdatePortfolio(id uuid.UUID, request PortfolioRequest) (*PortfolioResponse, error)
	DeletePortfolio(id uuid.UUID) error
	GetStudentPortfolios(studentID uuid.UUID) ([]PortfolioResponse, error)
	PublishPortfolio(id uuid.UUID) (*PortfolioResponse, error)

	// PortfolioArtifact operations
	CreateArtifact(request PortfolioArtifactRequest) (*PortfolioArtifactResponse, error)
	GetArtifactByID(id uuid.UUID) (*PortfolioArtifactResponse, error)
	GetArtifacts(filter map[string]interface{}) ([]PortfolioArtifactResponse, error)
	UpdateArtifact(id uuid.UUID, request PortfolioArtifactRequest) (*PortfolioArtifactResponse, error)
	DeleteArtifact(id uuid.UUID) error
	GetPortfolioArtifacts(portfolioID uuid.UUID) ([]PortfolioArtifactResponse, error)

	// LearningEvidence operations
	CreateLearningEvidence(request LearningEvidenceRequest) (*LearningEvidenceResponse, error)
	GetLearningEvidenceByID(id uuid.UUID) (*LearningEvidenceResponse, error)
	GetLearningEvidence(filter map[string]interface{}) ([]LearningEvidenceResponse, error)
	UpdateLearningEvidence(id uuid.UUID, request LearningEvidenceRequest) (*LearningEvidenceResponse, error)
	DeleteLearningEvidence(id uuid.UUID) error
	GetStudentLearningEvidence(studentID uuid.UUID) ([]LearningEvidenceResponse, error)
	ValidateEvidence(id uuid.UUID, validationStatus string, notes string, validatedBy uuid.UUID) (*LearningEvidenceResponse, error)

	// PortfolioReview operations
	CreateReview(request PortfolioReviewRequest) (*PortfolioReviewResponse, error)
	GetReviewByID(id uuid.UUID) (*PortfolioReviewResponse, error)
	GetReviews(filter map[string]interface{}) ([]PortfolioReviewResponse, error)
	UpdateReview(id uuid.UUID, request PortfolioReviewRequest) (*PortfolioReviewResponse, error)
	DeleteReview(id uuid.UUID) error
	GetPortfolioReviews(portfolioID uuid.UUID) ([]PortfolioReviewResponse, error)

	// Analytics operations
	GetPortfolioAnalytics(request PortfolioAnalyticsRequest) (*PortfolioAnalyticsResponse, error)
}

type service struct {
	repo Repository
}

func NewService(repo Repository) Service {
	return &service{repo: repo}
}

// Portfolio operations
func (s *service) CreatePortfolio(request PortfolioRequest) (*PortfolioResponse, error) {
	// Validate portfolio type
	if !IsValidPortfolioType(request.PortfolioType) {
		return nil, errors.New("invalid portfolio type")
	}

	portfolio := &Portfolio{
		ID:             uuid.New(),
		StudentID:      request.StudentID,
		PortfolioType:  request.PortfolioType,
		Title:          request.Title,
		Description:    request.Description,
		SubjectID:      request.SubjectID,
		ProjectID:      request.ProjectID,
		Period:         request.Period,
		AcademicYearID: request.AcademicYearID,
		TeacherID:      request.TeacherID,
	}

	if request.IsPublished != nil {
		portfolio.IsPublished = *request.IsPublished
		if portfolio.IsPublished {
			now := time.Now()
			portfolio.PublishedAt = &now
		}
	}

	err := s.repo.CreatePortfolio(portfolio)
	if err != nil {
		return nil, err
	}

	return s.modelToPortfolioResponse(portfolio), nil
}

func (s *service) GetPortfolioByID(id uuid.UUID) (*PortfolioResponse, error) {
	portfolio, err := s.repo.GetPortfolioByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToPortfolioResponse(portfolio), nil
}

func (s *service) GetPortfolios(filter map[string]interface{}) ([]PortfolioResponse, error) {
	portfolios, err := s.repo.GetPortfolios(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]PortfolioResponse, len(portfolios))
	for i, portfolio := range portfolios {
		responses[i] = *s.modelToPortfolioResponse(&portfolio)
	}
	return responses, nil
}

func (s *service) UpdatePortfolio(id uuid.UUID, request PortfolioRequest) (*PortfolioResponse, error) {
	// Validate portfolio type
	if !IsValidPortfolioType(request.PortfolioType) {
		return nil, errors.New("invalid portfolio type")
	}

	portfolio, err := s.repo.GetPortfolioByID(id)
	if err != nil {
		return nil, err
	}

	portfolio.StudentID = request.StudentID
	portfolio.PortfolioType = request.PortfolioType
	portfolio.Title = request.Title
	portfolio.Description = request.Description
	portfolio.SubjectID = request.SubjectID
	portfolio.ProjectID = request.ProjectID
	portfolio.Period = request.Period
	portfolio.AcademicYearID = request.AcademicYearID
	portfolio.TeacherID = request.TeacherID

	// Handle publish status change
	if request.IsPublished != nil {
		if !portfolio.IsPublished && *request.IsPublished {
			// Publishing for the first time
			now := time.Now()
			portfolio.PublishedAt = &now
		}
		portfolio.IsPublished = *request.IsPublished
	}

	err = s.repo.UpdatePortfolio(portfolio)
	if err != nil {
		return nil, err
	}

	return s.modelToPortfolioResponse(portfolio), nil
}

func (s *service) DeletePortfolio(id uuid.UUID) error {
	return s.repo.DeletePortfolio(id)
}

func (s *service) GetStudentPortfolios(studentID uuid.UUID) ([]PortfolioResponse, error) {
	portfolios, err := s.repo.GetStudentPortfolios(studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]PortfolioResponse, len(portfolios))
	for i, portfolio := range portfolios {
		responses[i] = *s.modelToPortfolioResponse(&portfolio)
	}
	return responses, nil
}

func (s *service) PublishPortfolio(id uuid.UUID) (*PortfolioResponse, error) {
	portfolio, err := s.repo.GetPortfolioByID(id)
	if err != nil {
		return nil, err
	}

	portfolio.IsPublished = true
	now := time.Now()
	portfolio.PublishedAt = &now

	err = s.repo.UpdatePortfolio(portfolio)
	if err != nil {
		return nil, err
	}

	return s.modelToPortfolioResponse(portfolio), nil
}

// PortfolioArtifact operations
func (s *service) CreateArtifact(request PortfolioArtifactRequest) (*PortfolioArtifactResponse, error) {
	// Validate artifact type
	if !IsValidArtifactType(request.ArtifactType) {
		return nil, errors.New("invalid artifact type")
	}

	artifact := &PortfolioArtifact{
		ID:              uuid.New(),
		PortfolioID:     request.PortfolioID,
		ArtifactType:    request.ArtifactType,
		Title:           request.Title,
		Description:     request.Description,
		FileURL:         request.FileURL,
		FileName:        request.FileName,
		FileSize:        request.FileSize,
		FileType:        request.FileType,
		ThumbnailURL:    request.ThumbnailURL,
		CompetencyIDs:   request.CompetencyIDs,
		Skills:          request.Skills,
		Reflection:      request.Reflection,
		TeacherFeedback: request.TeacherFeedback,
		TeacherID:       request.TeacherID,
	}

	if request.IsFeatured != nil {
		artifact.IsFeatured = *request.IsFeatured
	}

	if request.DisplayOrder != nil {
		artifact.DisplayOrder = *request.DisplayOrder
	}

	err := s.repo.CreateArtifact(artifact)
	if err != nil {
		return nil, err
	}

	return s.modelToArtifactResponse(artifact), nil
}

func (s *service) GetArtifactByID(id uuid.UUID) (*PortfolioArtifactResponse, error) {
	artifact, err := s.repo.GetArtifactByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToArtifactResponse(artifact), nil
}

func (s *service) GetArtifacts(filter map[string]interface{}) ([]PortfolioArtifactResponse, error) {
	artifacts, err := s.repo.GetArtifacts(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]PortfolioArtifactResponse, len(artifacts))
	for i, artifact := range artifacts {
		responses[i] = *s.modelToArtifactResponse(&artifact)
	}
	return responses, nil
}

func (s *service) UpdateArtifact(id uuid.UUID, request PortfolioArtifactRequest) (*PortfolioArtifactResponse, error) {
	// Validate artifact type
	if !IsValidArtifactType(request.ArtifactType) {
		return nil, errors.New("invalid artifact type")
	}

	artifact, err := s.repo.GetArtifactByID(id)
	if err != nil {
		return nil, err
	}

	artifact.PortfolioID = request.PortfolioID
	artifact.ArtifactType = request.ArtifactType
	artifact.Title = request.Title
	artifact.Description = request.Description
	artifact.FileURL = request.FileURL
	artifact.FileName = request.FileName
	artifact.FileSize = request.FileSize
	artifact.FileType = request.FileType
	artifact.ThumbnailURL = request.ThumbnailURL
	artifact.CompetencyIDs = request.CompetencyIDs
	artifact.Skills = request.Skills
	artifact.Reflection = request.Reflection
	artifact.TeacherFeedback = request.TeacherFeedback
	artifact.TeacherID = request.TeacherID

	if request.IsFeatured != nil {
		artifact.IsFeatured = *request.IsFeatured
	}

	if request.DisplayOrder != nil {
		artifact.DisplayOrder = *request.DisplayOrder
	}

	err = s.repo.UpdateArtifact(artifact)
	if err != nil {
		return nil, err
	}

	return s.modelToArtifactResponse(artifact), nil
}

func (s *service) DeleteArtifact(id uuid.UUID) error {
	return s.repo.DeleteArtifact(id)
}

func (s *service) GetPortfolioArtifacts(portfolioID uuid.UUID) ([]PortfolioArtifactResponse, error) {
	artifacts, err := s.repo.GetPortfolioArtifacts(portfolioID)
	if err != nil {
		return nil, err
	}

	responses := make([]PortfolioArtifactResponse, len(artifacts))
	for i, artifact := range artifacts {
		responses[i] = *s.modelToArtifactResponse(&artifact)
	}
	return responses, nil
}

// LearningEvidence operations
func (s *service) CreateLearningEvidence(request LearningEvidenceRequest) (*LearningEvidenceResponse, error) {
	evidence := &LearningEvidence{
		ID:               uuid.New(),
		StudentID:        request.StudentID,
		ArtifactID:       request.ArtifactID,
		CompetencyID:     request.CompetencyID,
		CompetencyType:   request.CompetencyType,
		EvidenceDate:     request.EvidenceDate,
		MasteryLevel:     request.MasteryLevel,
		TeacherID:        request.TeacherID,
		ValidationStatus: request.ValidationStatus,
		ValidationNotes:  request.ValidationNotes,
		ValidatedBy:      request.ValidatedBy,
	}

	if evidence.ValidationStatus == "" {
		evidence.ValidationStatus = "PENDING"
	}

	err := s.repo.CreateLearningEvidence(evidence)
	if err != nil {
		return nil, err
	}

	return s.modelToEvidenceResponse(evidence), nil
}

func (s *service) GetLearningEvidenceByID(id uuid.UUID) (*LearningEvidenceResponse, error) {
	evidence, err := s.repo.GetLearningEvidenceByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToEvidenceResponse(evidence), nil
}

func (s *service) GetLearningEvidence(filter map[string]interface{}) ([]LearningEvidenceResponse, error) {
	evidenceList, err := s.repo.GetLearningEvidence(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]LearningEvidenceResponse, len(evidenceList))
	for i, evidence := range evidenceList {
		responses[i] = *s.modelToEvidenceResponse(&evidence)
	}
	return responses, nil
}

func (s *service) UpdateLearningEvidence(id uuid.UUID, request LearningEvidenceRequest) (*LearningEvidenceResponse, error) {
	evidence, err := s.repo.GetLearningEvidenceByID(id)
	if err != nil {
		return nil, err
	}

	evidence.StudentID = request.StudentID
	evidence.ArtifactID = request.ArtifactID
	evidence.CompetencyID = request.CompetencyID
	evidence.CompetencyType = request.CompetencyType
	evidence.EvidenceDate = request.EvidenceDate
	evidence.MasteryLevel = request.MasteryLevel
	evidence.TeacherID = request.TeacherID
	evidence.ValidationStatus = request.ValidationStatus
	evidence.ValidationNotes = request.ValidationNotes
	evidence.ValidatedBy = request.ValidatedBy

	err = s.repo.UpdateLearningEvidence(evidence)
	if err != nil {
		return nil, err
	}

	return s.modelToEvidenceResponse(evidence), nil
}

func (s *service) DeleteLearningEvidence(id uuid.UUID) error {
	return s.repo.DeleteLearningEvidence(id)
}

func (s *service) GetStudentLearningEvidence(studentID uuid.UUID) ([]LearningEvidenceResponse, error) {
	evidenceList, err := s.repo.GetStudentLearningEvidence(studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]LearningEvidenceResponse, len(evidenceList))
	for i, evidence := range evidenceList {
		responses[i] = *s.modelToEvidenceResponse(&evidence)
	}
	return responses, nil
}

func (s *service) ValidateEvidence(id uuid.UUID, validationStatus string, notes string, validatedBy uuid.UUID) (*LearningEvidenceResponse, error) {
	evidence, err := s.repo.GetLearningEvidenceByID(id)
	if err != nil {
		return nil, err
	}

	evidence.ValidationStatus = validationStatus
	evidence.ValidationNotes = notes
	evidence.ValidatedBy = validatedBy

	now := time.Now()
	evidence.ValidatedAt = &now

	err = s.repo.UpdateLearningEvidence(evidence)
	if err != nil {
		return nil, err
	}

	return s.modelToEvidenceResponse(evidence), nil
}

// PortfolioReview operations
func (s *service) CreateReview(request PortfolioReviewRequest) (*PortfolioReviewResponse, error) {
	review := &PortfolioReview{
		ID:                  uuid.New(),
		PortfolioID:         request.PortfolioID,
		ReviewerID:          request.ReviewerID,
		ReviewDate:          request.ReviewDate,
		OverallRating:       request.OverallRating,
		Strengths:           request.Strengths,
		AreasForImprovement: request.AreasForImprovement,
		Recommendations:     request.Recommendations,
		IsFormal:            request.IsFormal,
	}

	err := s.repo.CreateReview(review)
	if err != nil {
		return nil, err
	}

	return s.modelToReviewResponse(review), nil
}

func (s *service) GetReviewByID(id uuid.UUID) (*PortfolioReviewResponse, error) {
	review, err := s.repo.GetReviewByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToReviewResponse(review), nil
}

func (s *service) GetReviews(filter map[string]interface{}) ([]PortfolioReviewResponse, error) {
	reviews, err := s.repo.GetReviews(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]PortfolioReviewResponse, len(reviews))
	for i, review := range reviews {
		responses[i] = *s.modelToReviewResponse(&review)
	}
	return responses, nil
}

func (s *service) UpdateReview(id uuid.UUID, request PortfolioReviewRequest) (*PortfolioReviewResponse, error) {
	review, err := s.repo.GetReviewByID(id)
	if err != nil {
		return nil, err
	}

	review.PortfolioID = request.PortfolioID
	review.ReviewerID = request.ReviewerID
	review.ReviewDate = request.ReviewDate
	review.OverallRating = request.OverallRating
	review.Strengths = request.Strengths
	review.AreasForImprovement = request.AreasForImprovement
	review.Recommendations = request.Recommendations
	review.IsFormal = request.IsFormal

	err = s.repo.UpdateReview(review)
	if err != nil {
		return nil, err
	}

	return s.modelToReviewResponse(review), nil
}

func (s *service) DeleteReview(id uuid.UUID) error {
	return s.repo.DeleteReview(id)
}

func (s *service) GetPortfolioReviews(portfolioID uuid.UUID) ([]PortfolioReviewResponse, error) {
	reviews, err := s.repo.GetPortfolioReviews(portfolioID)
	if err != nil {
		return nil, err
	}

	responses := make([]PortfolioReviewResponse, len(reviews))
	for i, review := range reviews {
		responses[i] = *s.modelToReviewResponse(&review)
	}
	return responses, nil
}

// Analytics operations
func (s *service) GetPortfolioAnalytics(request PortfolioAnalyticsRequest) (*PortfolioAnalyticsResponse, error) {
	return s.repo.GetPortfolioAnalytics(request)
}

// Helper functions to convert models to DTOs
func (s *service) modelToPortfolioResponse(portfolio *Portfolio) *PortfolioResponse {
	response := &PortfolioResponse{
		ID:             portfolio.ID,
		StudentID:      portfolio.StudentID,
		PortfolioType:  portfolio.PortfolioType,
		TypeName:       GetPortfolioTypeDescription(portfolio.PortfolioType),
		Title:          portfolio.Title,
		Description:    portfolio.Description,
		SubjectID:      portfolio.SubjectID,
		ProjectID:      portfolio.ProjectID,
		Period:         portfolio.Period,
		AcademicYearID: portfolio.AcademicYearID,
		TeacherID:      portfolio.TeacherID,
		IsPublished:    portfolio.IsPublished,
		PublishedAt:    portfolio.PublishedAt,
		CreatedAt:      portfolio.CreatedAt,
		UpdatedAt:      portfolio.UpdatedAt,
		ArtifactCount:  len(portfolio.Artifacts),
	}

	if portfolio.Student != nil {
		response.StudentName = portfolio.Student.FullName
	}

	periodNames := map[string]string{
		"SEMESTER_1": "Semester 1",
		"SEMESTER_2": "Semester 2",
	}
	response.PeriodName = periodNames[portfolio.Period]

	return response
}

func (s *service) modelToArtifactResponse(artifact *PortfolioArtifact) *PortfolioArtifactResponse {
	response := &PortfolioArtifactResponse{
		ID:              artifact.ID,
		PortfolioID:     artifact.PortfolioID,
		ArtifactType:    artifact.ArtifactType,
		TypeName:        GetArtifactTypeDescription(artifact.ArtifactType),
		Title:           artifact.Title,
		Description:     artifact.Description,
		FileURL:         artifact.FileURL,
		FileName:        artifact.FileName,
		FileSize:        artifact.FileSize,
		FileType:        artifact.FileType,
		ThumbnailURL:    artifact.ThumbnailURL,
		CompetencyIDs:   artifact.CompetencyIDs,
		Skills:          artifact.Skills,
		Reflection:      artifact.Reflection,
		TeacherFeedback: artifact.TeacherFeedback,
		TeacherID:       artifact.TeacherID,
		IsFeatured:      artifact.IsFeatured,
		DisplayOrder:    artifact.DisplayOrder,
		CreatedAt:       artifact.CreatedAt,
		UpdatedAt:       artifact.UpdatedAt,
	}

	if artifact.Portfolio != nil {
		response.PortfolioTitle = artifact.Portfolio.Title
	}

	return response
}

func (s *service) modelToEvidenceResponse(evidence *LearningEvidence) *LearningEvidenceResponse {
	response := &LearningEvidenceResponse{
		ID:               evidence.ID,
		StudentID:        evidence.StudentID,
		ArtifactID:       evidence.ArtifactID,
		CompetencyID:     evidence.CompetencyID,
		CompetencyType:   evidence.CompetencyType,
		EvidenceDate:     evidence.EvidenceDate,
		MasteryLevel:     evidence.MasteryLevel,
		TeacherID:        evidence.TeacherID,
		ValidationStatus: evidence.ValidationStatus,
		ValidationNotes:  evidence.ValidationNotes,
		ValidatedBy:      evidence.ValidatedBy,
		ValidatedAt:      evidence.ValidatedAt,
		CreatedAt:        evidence.CreatedAt,
		UpdatedAt:        evidence.UpdatedAt,
	}

	if evidence.Student != nil {
		response.StudentName = evidence.Student.FullName
	}

	masteryLevelNames := map[string]string{
		"BELUM":     "Belum Menguasai",
		"SEDANG":    "Sedang Mengembangkan",
		"MENGUASAI": "Menguasai",
	}
	response.LevelName = masteryLevelNames[evidence.MasteryLevel]

	statusNames := map[string]string{
		"PENDING":  "Menunggu Validasi",
		"APPROVED": "Disetujui",
		"REJECTED": "Ditolak",
	}
	response.StatusName = statusNames[evidence.ValidationStatus]

	return response
}

func (s *service) modelToReviewResponse(review *PortfolioReview) *PortfolioReviewResponse {
	response := &PortfolioReviewResponse{
		ID:                  review.ID,
		PortfolioID:         review.PortfolioID,
		ReviewerID:          review.ReviewerID,
		ReviewDate:          review.ReviewDate,
		OverallRating:       review.OverallRating,
		Strengths:           review.Strengths,
		AreasForImprovement: review.AreasForImprovement,
		Recommendations:     review.Recommendations,
		IsFormal:            review.IsFormal,
		CreatedAt:           review.CreatedAt,
		UpdatedAt:           review.UpdatedAt,
	}

	return response
}
