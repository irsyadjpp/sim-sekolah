package reading_literacy

import (
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"
)

type Service interface {
	// Reading Level Operations
	GetAllReadingLevels() ([]ReadingLevelResponse, error)
	GetReadingLevelByID(id string) (*ReadingLevelResponse, error)
	GetReadingLevelByCode(levelCode string) (*ReadingLevelResponse, error)
	CreateReadingLevel(req CreateReadingLevelRequest) (*ReadingLevelResponse, error)
	UpdateReadingLevel(id string, req UpdateReadingLevelRequest) (*ReadingLevelResponse, error)
	DeleteReadingLevel(id string) error

	// Assessment Operations
	GetAllAssessments() ([]AssessmentResponse, error)
	GetAssessmentByID(id string) (*AssessmentResponse, error)
	GetAssessmentsByStudent(studentID string) ([]AssessmentResponse, error)
	GetAssessmentsByLevel(levelID string) ([]AssessmentResponse, error)
	CreateAssessment(req CreateAssessmentRequest) (*AssessmentResponse, error)
	UpdateAssessment(id string, req UpdateAssessmentRequest) (*AssessmentResponse, error)
	DeleteAssessment(id string) error
	GetStudentProgression(studentID string) (*StudentProgressionResponse, error)
}

type service struct {
	repo Repository
}

func NewService(repo Repository) Service {
	return &service{repo: repo}
}

// Reading Level Operations
func (s *service) GetAllReadingLevels() ([]ReadingLevelResponse, error) {
	levels, err := s.repo.GetAllReadingLevels()
	if err != nil {
		return nil, fmt.Errorf("failed to get reading levels: %w", err)
	}

	responses := make([]ReadingLevelResponse, len(levels))
	for i, level := range levels {
		responses[i] = s.readingLevelToResponse(&level)
	}
	return responses, nil
}

func (s *service) GetReadingLevelByID(id string) (*ReadingLevelResponse, error) {
	level, err := s.repo.GetReadingLevelByID(id)
	if err != nil {
		return nil, fmt.Errorf("failed to get reading level: %w", err)
	}
	res := s.readingLevelToResponse(level)
	return &res, nil
}

func (s *service) GetReadingLevelByCode(levelCode string) (*ReadingLevelResponse, error) {
	level, err := s.repo.GetReadingLevelByCode(levelCode)
	if err != nil {
		return nil, fmt.Errorf("failed to get reading level: %w", err)
	}
	res := s.readingLevelToResponse(level)
	return &res, nil
}

func (s *service) CreateReadingLevel(req CreateReadingLevelRequest) (*ReadingLevelResponse, error) {
	if !IsValidReadingLevel(req.LevelCode) {
		return nil, errors.New("invalid reading level code")
	}

	isActive := true
	if req.IsActive != nil {
		isActive = *req.IsActive
	}

	level := &ReadingLevel{
		ID:          uuid.New(),
		LevelCode:   req.LevelCode,
		LevelName:   req.LevelName,
		Description: req.Description,
		Indicators:  req.Indicators,
		WPMRange:    req.WPMRange,
		IsActive:    isActive,
	}

	if req.PhaseID != "" {
		level.PhaseID = uuid.MustParse(req.PhaseID)
	}

	level.CreatedAt = time.Now()
	level.UpdatedAt = time.Now()

	if err := s.repo.CreateReadingLevel(level); err != nil {
		return nil, fmt.Errorf("failed to create reading level: %w", err)
	}

	res := s.readingLevelToResponse(level)
	return &res, nil
}

func (s *service) UpdateReadingLevel(id string, req UpdateReadingLevelRequest) (*ReadingLevelResponse, error) {
	level, err := s.repo.GetReadingLevelByID(id)
	if err != nil {
		return nil, fmt.Errorf("reading level not found: %w", err)
	}

	if req.LevelCode != "" {
		if !IsValidReadingLevel(req.LevelCode) {
			return nil, errors.New("invalid reading level code")
		}
		level.LevelCode = req.LevelCode
	}
	if req.LevelName != "" {
		level.LevelName = req.LevelName
	}
	if req.Description != "" {
		level.Description = req.Description
	}
	if req.Indicators != "" {
		level.Indicators = req.Indicators
	}
	if req.WPMRange != "" {
		level.WPMRange = req.WPMRange
	}
	if req.PhaseID != "" {
		level.PhaseID = uuid.MustParse(req.PhaseID)
	}
	if req.IsActive != nil {
		level.IsActive = *req.IsActive
	}

	level.UpdatedAt = time.Now()

	if err := s.repo.UpdateReadingLevel(level); err != nil {
		return nil, fmt.Errorf("failed to update reading level: %w", err)
	}

	res := s.readingLevelToResponse(level)
	return &res, nil
}

func (s *service) DeleteReadingLevel(id string) error {
	if err := s.repo.DeleteReadingLevel(id); err != nil {
		return fmt.Errorf("failed to delete reading level: %w", err)
	}
	return nil
}

// Assessment Operations
func (s *service) GetAllAssessments() ([]AssessmentResponse, error) {
	assessments, err := s.repo.GetAllAssessments()
	if err != nil {
		return nil, fmt.Errorf("failed to get assessments: %w", err)
	}

	responses := make([]AssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = s.assessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *service) GetAssessmentByID(id string) (*AssessmentResponse, error) {
	assessment, err := s.repo.GetAssessmentByID(id)
	if err != nil {
		return nil, fmt.Errorf("failed to get assessment: %w", err)
	}
	res := s.assessmentToResponse(assessment)
	return &res, nil
}

func (s *service) GetAssessmentsByStudent(studentID string) ([]AssessmentResponse, error) {
	assessments, err := s.repo.GetAssessmentsByStudent(studentID)
	if err != nil {
		return nil, fmt.Errorf("failed to get student assessments: %w", err)
	}

	responses := make([]AssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = s.assessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *service) GetAssessmentsByLevel(levelID string) ([]AssessmentResponse, error) {
	assessments, err := s.repo.GetAssessmentsByLevel(levelID)
	if err != nil {
		return nil, fmt.Errorf("failed to get assessments by level: %w", err)
	}

	responses := make([]AssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = s.assessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *service) CreateAssessment(req CreateAssessmentRequest) (*AssessmentResponse, error) {
	if req.WordsPerMinute < 0 {
		return nil, errors.New("words per minute cannot be negative")
	}
	if req.ComprehensionScore < 0 || req.ComprehensionScore > 100 {
		return nil, errors.New("comprehension score must be between 0 and 100")
	}
	if req.AccuracyScore < 0 || req.AccuracyScore > 100 {
		return nil, errors.New("accuracy score must be between 0 and 100")
	}
	if req.FluencyRating != "" && !IsValidFluencyRating(req.FluencyRating) {
		return nil, errors.New("invalid fluency rating")
	}

	assessment := &ReadingLiteracyAssessment{
		ID:                 uuid.New(),
		StudentID:          uuid.MustParse(req.StudentID),
		ReadingLevelID:     uuid.MustParse(req.ReadingLevelID),
		AssessmentDate:     req.AssessmentDate,
		WordsPerMinute:     req.WordsPerMinute,
		ComprehensionScore: req.ComprehensionScore,
		FluencyRating:      req.FluencyRating,
		AccuracyScore:      req.AccuracyScore,
		Notes:              req.Notes,
	}

	if req.TeacherID != "" {
		assessment.TeacherID = uuid.MustParse(req.TeacherID)
	}

	assessment.CreatedAt = time.Now()
	assessment.UpdatedAt = time.Now()

	if err := s.repo.CreateAssessment(assessment); err != nil {
		return nil, fmt.Errorf("failed to create assessment: %w", err)
	}

	res := s.assessmentToResponse(assessment)
	return &res, nil
}

func (s *service) UpdateAssessment(id string, req UpdateAssessmentRequest) (*AssessmentResponse, error) {
	assessment, err := s.repo.GetAssessmentByID(id)
	if err != nil {
		return nil, fmt.Errorf("assessment not found: %w", err)
	}

	if req.ReadingLevelID != "" {
		assessment.ReadingLevelID = uuid.MustParse(req.ReadingLevelID)
	}
	if req.AssessmentDate != "" {
		assessment.AssessmentDate = req.AssessmentDate
	}
	if req.WordsPerMinute != nil {
		if *req.WordsPerMinute < 0 {
			return nil, errors.New("words per minute cannot be negative")
		}
		assessment.WordsPerMinute = *req.WordsPerMinute
	}
	if req.ComprehensionScore != nil {
		if *req.ComprehensionScore < 0 || *req.ComprehensionScore > 100 {
			return nil, errors.New("comprehension score must be between 0 and 100")
		}
		assessment.ComprehensionScore = *req.ComprehensionScore
	}
	if req.FluencyRating != "" {
		if !IsValidFluencyRating(req.FluencyRating) {
			return nil, errors.New("invalid fluency rating")
		}
		assessment.FluencyRating = req.FluencyRating
	}
	if req.AccuracyScore != nil {
		if *req.AccuracyScore < 0 || *req.AccuracyScore > 100 {
			return nil, errors.New("accuracy score must be between 0 and 100")
		}
		assessment.AccuracyScore = *req.AccuracyScore
	}
	if req.Notes != "" {
		assessment.Notes = req.Notes
	}

	assessment.UpdatedAt = time.Now()

	if err := s.repo.UpdateAssessment(assessment); err != nil {
		return nil, fmt.Errorf("failed to update assessment: %w", err)
	}

	res := s.assessmentToResponse(assessment)
	return &res, nil
}

func (s *service) DeleteAssessment(id string) error {
	if err := s.repo.DeleteAssessment(id); err != nil {
		return fmt.Errorf("failed to delete assessment: %w", err)
	}
	return nil
}

func (s *service) GetStudentProgression(studentID string) (*StudentProgressionResponse, error) {
	assessments, err := s.repo.GetAssessmentsByStudent(studentID)
	if err != nil {
		return nil, fmt.Errorf("failed to get student progression: %w", err)
	}

	// Convert assessments to responses
	assessmentResponses := make([]AssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		assessmentResponses[i] = s.assessmentToResponse(&assessment)
	}

	// Get latest assessment and current level
	latestAssessment, err := s.repo.GetLatestAssessmentByStudent(studentID)
	var currentLevel ReadingLevelResponse
	if err == nil {
		level, err := s.repo.GetReadingLevelByID(latestAssessment.ReadingLevelID.String())
		if err == nil {
			currentLevel = s.readingLevelToResponse(level)
		}
	}

	// Calculate averages and distribution
	totalWPM := 0
	totalComprehension := 0.0
	totalAccuracy := 0.0
	fluencyDistribution := make(map[string]int)

	for _, assessment := range assessments {
		totalWPM += assessment.WordsPerMinute
		totalComprehension += assessment.ComprehensionScore
		totalAccuracy += assessment.AccuracyScore

		if assessment.FluencyRating != "" {
			fluencyDistribution[assessment.FluencyRating]++
		}
	}

	averageWPM := 0
	averageComprehension := 0.0
	averageAccuracy := 0.0

	if len(assessments) > 0 {
		averageWPM = totalWPM / len(assessments)
		averageComprehension = totalComprehension / float64(len(assessments))
		averageAccuracy = totalAccuracy / float64(len(assessments))
	}

	// Build progression history
	progressionHistory := s.buildProgressionHistory(assessments)

	return &StudentProgressionResponse{
		StudentID:            studentID,
		StudentName:          "", // Will be populated from user service if needed
		Assessments:          assessmentResponses,
		CurrentLevel:         currentLevel,
		ProgressionHistory:   progressionHistory,
		AverageWPM:           averageWPM,
		AverageComprehension: averageComprehension,
		AverageAccuracy:      averageAccuracy,
		FluencyDistribution:  fluencyDistribution,
	}, nil
}

func (s *service) buildProgressionHistory(assessments []ReadingLiteracyAssessment) []LevelProgress {
	if len(assessments) == 0 {
		return []LevelProgress{}
	}

	history := make([]LevelProgress, 0)
	uniqueLevels := make(map[string]bool)

	// Sort by assessment date ascending for progression
	sortedAssessments := make([]ReadingLiteracyAssessment, len(assessments))
	copy(sortedAssessments, assessments)

	// Simple sort by date (in production, use proper date comparison)
	for i := 0; i < len(sortedAssessments); i++ {
		for j := i + 1; j < len(sortedAssessments); j++ {
			if sortedAssessments[i].AssessmentDate > sortedAssessments[j].AssessmentDate {
				sortedAssessments[i], sortedAssessments[j] = sortedAssessments[j], sortedAssessments[i]
			}
		}
	}

	for _, assessment := range sortedAssessments {
		levelID := assessment.ReadingLevelID.String()
		if !uniqueLevels[levelID] {
			level, err := s.repo.GetReadingLevelByID(levelID)
			if err == nil {
				achievedDate := assessment.AssessmentDate
				durationDays := 0

				if len(history) > 0 {
					prevDate := history[len(history)-1].AchievedDate
					durationDays = s.calculateDaysBetween(prevDate, achievedDate)
				}

				history = append(history, LevelProgress{
					ReadingLevelID: levelID,
					LevelName:      level.LevelName,
					LevelCode:      level.LevelCode,
					AchievedDate:   achievedDate,
					DurationDays:   durationDays,
				})
				uniqueLevels[levelID] = true
			}
		}
	}

	return history
}

func (s *service) calculateDaysBetween(date1, date2 string) int {
	// Simple implementation - in production use proper date parsing
	// This is a placeholder for proper date calculation
	return 0
}

func (s *service) readingLevelToResponse(level *ReadingLevel) ReadingLevelResponse {
	var phaseID string
	if level.PhaseID != uuid.Nil {
		phaseID = level.PhaseID.String()
	}

	return ReadingLevelResponse{
		ID:          level.ID.String(),
		LevelCode:   level.LevelCode,
		LevelName:   level.LevelName,
		Description: level.Description,
		PhaseID:     phaseID,
		Indicators:  level.Indicators,
		WPMRange:    level.WPMRange,
		IsActive:    level.IsActive,
		CreatedAt:   level.CreatedAt.Format(time.RFC3339),
		UpdatedAt:   level.UpdatedAt.Format(time.RFC3339),
	}
}

func (s *service) assessmentToResponse(assessment *ReadingLiteracyAssessment) AssessmentResponse {
	return AssessmentResponse{
		ID:                 assessment.ID.String(),
		StudentID:          assessment.StudentID.String(),
		ReadingLevelID:     assessment.ReadingLevelID.String(),
		AssessmentDate:     assessment.AssessmentDate,
		WordsPerMinute:     assessment.WordsPerMinute,
		ComprehensionScore: assessment.ComprehensionScore,
		FluencyRating:      assessment.FluencyRating,
		AccuracyScore:      assessment.AccuracyScore,
		Notes:              assessment.Notes,
		TeacherID:          assessment.TeacherID.String(),
		CreatedAt:          assessment.CreatedAt.Format(time.RFC3339),
		UpdatedAt:          assessment.UpdatedAt.Format(time.RFC3339),
	}
}
