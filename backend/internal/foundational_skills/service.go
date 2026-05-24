package foundational_skills

import (
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"
)

type Service interface {
	// Skill Standard Operations
	GetAllSkillStandards() ([]SkillStandardResponse, error)
	GetSkillStandardByID(id string) (*SkillStandardResponse, error)
	GetSkillStandardsByType(skillType string) ([]SkillStandardResponse, error)
	CreateSkillStandard(req CreateSkillStandardRequest) (*SkillStandardResponse, error)
	UpdateSkillStandard(id string, req UpdateSkillStandardRequest) (*SkillStandardResponse, error)
	DeleteSkillStandard(id string) error

	// Assessment Operations
	GetAllAssessments() ([]AssessmentResponse, error)
	GetAssessmentByID(id string) (*AssessmentResponse, error)
	GetAssessmentsByStudent(studentID string) ([]AssessmentResponse, error)
	GetAssessmentsByStandard(standardID string) ([]AssessmentResponse, error)
	CreateAssessment(req CreateAssessmentRequest) (*AssessmentResponse, error)
	UpdateAssessment(id string, req UpdateAssessmentRequest) (*AssessmentResponse, error)
	DeleteAssessment(id string) error
	GetStudentProgress(studentID string) (*StudentProgressResponse, error)
}

type service struct {
	repo Repository
}

func NewService(repo Repository) Service {
	return &service{repo: repo}
}

// Skill Standard Operations
func (s *service) GetAllSkillStandards() ([]SkillStandardResponse, error) {
	standards, err := s.repo.GetAllSkillStandards()
	if err != nil {
		return nil, fmt.Errorf("failed to get skill standards: %w", err)
	}

	responses := make([]SkillStandardResponse, len(standards))
	for i, standard := range standards {
		responses[i] = s.skillStandardToResponse(&standard)
	}
	return responses, nil
}

func (s *service) GetSkillStandardByID(id string) (*SkillStandardResponse, error) {
	standard, err := s.repo.GetSkillStandardByID(id)
	if err != nil {
		return nil, fmt.Errorf("failed to get skill standard: %w", err)
	}
	res := s.skillStandardToResponse(standard)
	return &res, nil
}

func (s *service) GetSkillStandardsByType(skillType string) ([]SkillStandardResponse, error) {
	if !IsValidSkillType(skillType) {
		return nil, errors.New("invalid skill type")
	}

	standards, err := s.repo.GetSkillStandardsByType(skillType)
	if err != nil {
		return nil, fmt.Errorf("failed to get skill standards by type: %w", err)
	}

	responses := make([]SkillStandardResponse, len(standards))
	for i, standard := range standards {
		responses[i] = s.skillStandardToResponse(&standard)
	}
	return responses, nil
}

func (s *service) CreateSkillStandard(req CreateSkillStandardRequest) (*SkillStandardResponse, error) {
	if !IsValidSkillType(req.SkillType) {
		return nil, errors.New("invalid skill type")
	}

	isActive := true
	if req.IsActive != nil {
		isActive = *req.IsActive
	}

	standard := &FoundationalSkillStandard{
		ID:          uuid.New(),
		SkillType:   req.SkillType,
		SkillCode:   req.SkillCode,
		SkillName:   req.SkillName,
		Description: req.Description,
		Indicators:  req.Indicators,
		IsActive:    isActive,
	}

	if req.PhaseID != "" {
		standard.PhaseID = uuid.MustParse(req.PhaseID)
	}

	standard.CreatedAt = time.Now()
	standard.UpdatedAt = time.Now()

	if err := s.repo.CreateSkillStandard(standard); err != nil {
		return nil, fmt.Errorf("failed to create skill standard: %w", err)
	}

	res := s.skillStandardToResponse(standard)
	return &res, nil
}

func (s *service) UpdateSkillStandard(id string, req UpdateSkillStandardRequest) (*SkillStandardResponse, error) {
	standard, err := s.repo.GetSkillStandardByID(id)
	if err != nil {
		return nil, fmt.Errorf("skill standard not found: %w", err)
	}

	if req.SkillType != "" {
		if !IsValidSkillType(req.SkillType) {
			return nil, errors.New("invalid skill type")
		}
		standard.SkillType = req.SkillType
	}
	if req.SkillCode != "" {
		standard.SkillCode = req.SkillCode
	}
	if req.SkillName != "" {
		standard.SkillName = req.SkillName
	}
	if req.Description != "" {
		standard.Description = req.Description
	}
	if req.Indicators != "" {
		standard.Indicators = req.Indicators
	}
	if req.PhaseID != "" {
		standard.PhaseID = uuid.MustParse(req.PhaseID)
	}
	if req.IsActive != nil {
		standard.IsActive = *req.IsActive
	}

	standard.UpdatedAt = time.Now()

	if err := s.repo.UpdateSkillStandard(standard); err != nil {
		return nil, fmt.Errorf("failed to update skill standard: %w", err)
	}

	res := s.skillStandardToResponse(standard)
	return &res, nil
}

func (s *service) DeleteSkillStandard(id string) error {
	if err := s.repo.DeleteSkillStandard(id); err != nil {
		return fmt.Errorf("failed to delete skill standard: %w", err)
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

func (s *service) GetAssessmentsByStandard(standardID string) ([]AssessmentResponse, error) {
	assessments, err := s.repo.GetAssessmentsByStandard(standardID)
	if err != nil {
		return nil, fmt.Errorf("failed to get assessments by standard: %w", err)
	}

	responses := make([]AssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = s.assessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *service) CreateAssessment(req CreateAssessmentRequest) (*AssessmentResponse, error) {
	if !IsValidMasteryLevel(req.MasteryLevel) {
		return nil, errors.New("invalid mastery level")
	}

	assessment := &FoundationalSkillAssessment{
		ID:              uuid.New(),
		StudentID:       uuid.MustParse(req.StudentID),
		SkillStandardID: uuid.MustParse(req.SkillStandardID),
		AssessmentDate:  req.AssessmentDate,
		MasteryLevel:    req.MasteryLevel,
		Notes:           req.Notes,
	}

	if req.Score != nil {
		assessment.Score = *req.Score
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

	if req.SkillStandardID != "" {
		assessment.SkillStandardID = uuid.MustParse(req.SkillStandardID)
	}
	if req.AssessmentDate != "" {
		assessment.AssessmentDate = req.AssessmentDate
	}
	if req.MasteryLevel != "" {
		if !IsValidMasteryLevel(req.MasteryLevel) {
			return nil, errors.New("invalid mastery level")
		}
		assessment.MasteryLevel = req.MasteryLevel
	}
	if req.Score != nil {
		assessment.Score = *req.Score
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

func (s *service) GetStudentProgress(studentID string) (*StudentProgressResponse, error) {
	assessments, err := s.repo.GetAssessmentsByStudent(studentID)
	if err != nil {
		return nil, fmt.Errorf("failed to get student progress: %w", err)
	}

	// Convert assessments to responses
	assessmentResponses := make([]AssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		assessmentResponses[i] = s.assessmentToResponse(&assessment)
	}

	// Calculate skill breakdown
	skillBreakdown := make(map[string]SkillProgress)
	overallMastery := make(map[string]int)
	latestAssessment := make(map[string]AssessmentResponse)

	for _, assessment := range assessments {
		standard, err := s.repo.GetSkillStandardByID(assessment.SkillStandardID.String())
		if err == nil {
			skillType := standard.SkillType

			if skillBreakdown[skillType].SkillType == "" {
				skillBreakdown[skillType] = SkillProgress{
					SkillType:    skillType,
					MasteryCount: make(map[string]int),
				}
			}

			progress := skillBreakdown[skillType]
			progress.TotalAssessments++
			progress.MasteryCount[assessment.MasteryLevel]++
			if assessment.Score > 0 {
				progress.AverageScore = (progress.AverageScore*float64(progress.TotalAssessments-1) + assessment.Score) / float64(progress.TotalAssessments)
			}
			skillBreakdown[skillType] = progress

			if overallMastery[assessment.MasteryLevel] == 0 {
				overallMastery[assessment.MasteryLevel] = 1
			} else {
				overallMastery[assessment.MasteryLevel]++
			}

			// Track latest assessment per skill type
			if _, exists := latestAssessment[skillType]; !exists {
				latestAssessment[skillType] = s.assessmentToResponse(&assessment)
			}
		}
	}

	return &StudentProgressResponse{
		StudentID:        studentID,
		StudentName:      "", // Will be populated from user service if needed
		Assessments:      assessmentResponses,
		SkillBreakdown:   skillBreakdown,
		OverallMastery:   overallMastery,
		LatestAssessment: latestAssessment,
	}, nil
}

func (s *service) skillStandardToResponse(standard *FoundationalSkillStandard) SkillStandardResponse {
	var phaseID string
	if standard.PhaseID != uuid.Nil {
		phaseID = standard.PhaseID.String()
	}

	return SkillStandardResponse{
		ID:          standard.ID.String(),
		SkillType:   standard.SkillType,
		SkillCode:   standard.SkillCode,
		SkillName:   standard.SkillName,
		Description: standard.Description,
		PhaseID:     phaseID,
		Indicators:  standard.Indicators,
		IsActive:    standard.IsActive,
		CreatedAt:   standard.CreatedAt.Format(time.RFC3339),
		UpdatedAt:   standard.UpdatedAt.Format(time.RFC3339),
	}
}

func (s *service) assessmentToResponse(assessment *FoundationalSkillAssessment) AssessmentResponse {
	return AssessmentResponse{
		ID:              assessment.ID.String(),
		StudentID:       assessment.StudentID.String(),
		SkillStandardID: assessment.SkillStandardID.String(),
		AssessmentDate:  assessment.AssessmentDate,
		MasteryLevel:    assessment.MasteryLevel,
		Score:           &assessment.Score,
		Notes:           assessment.Notes,
		TeacherID:       assessment.TeacherID.String(),
		CreatedAt:       assessment.CreatedAt.Format(time.RFC3339),
		UpdatedAt:       assessment.UpdatedAt.Format(time.RFC3339),
	}
}
