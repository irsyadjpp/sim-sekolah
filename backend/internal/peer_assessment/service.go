package peer_assessment

import (
	"context"
	"errors"
	"time"

	"github.com/google/uuid"
)

type PeerAssessmentService interface {
	// PeerAssessmentTemplate
	GetAllTemplates(ctx context.Context) ([]PeerAssessmentTemplateResponse, error)
	GetTemplateByID(ctx context.Context, id string) (*PeerAssessmentTemplateResponse, error)
	GetTemplatesByType(ctx context.Context, assessmentType string) ([]PeerAssessmentTemplateResponse, error)
	GetTemplatesByPhase(ctx context.Context, phase string) ([]PeerAssessmentTemplateResponse, error)
	GetTemplatesBySubject(ctx context.Context, subjectID string) ([]PeerAssessmentTemplateResponse, error)
	GetActiveTemplates(ctx context.Context) ([]PeerAssessmentTemplateResponse, error)
	CreateTemplate(ctx context.Context, req CreatePeerAssessmentTemplateRequest) (*PeerAssessmentTemplateResponse, error)
	UpdateTemplate(ctx context.Context, id string, req UpdatePeerAssessmentTemplateRequest) (*PeerAssessmentTemplateResponse, error)
	DeleteTemplate(ctx context.Context, id string) error

	// SelfAssessment
	GetAllSelfAssessments(ctx context.Context) ([]SelfAssessmentResponse, error)
	GetSelfAssessmentByID(ctx context.Context, id string) (*SelfAssessmentResponse, error)
	GetSelfAssessmentsByStudent(ctx context.Context, studentID string) ([]SelfAssessmentResponse, error)
	GetSelfAssessmentsByTemplate(ctx context.Context, templateID string) ([]SelfAssessmentResponse, error)
	CreateSelfAssessment(ctx context.Context, req CreateSelfAssessmentRequest) (*SelfAssessmentResponse, error)
	UpdateSelfAssessment(ctx context.Context, id string, req UpdateSelfAssessmentRequest) (*SelfAssessmentResponse, error)
	DeleteSelfAssessment(ctx context.Context, id string) error

	// PeerAssessment
	GetAllPeerAssessments(ctx context.Context) ([]PeerAssessmentResponse, error)
	GetPeerAssessmentByID(ctx context.Context, id string) (*PeerAssessmentResponse, error)
	GetPeerAssessmentsByAssessor(ctx context.Context, assessorID string) ([]PeerAssessmentResponse, error)
	GetPeerAssessmentsByAssessed(ctx context.Context, assessedID string) ([]PeerAssessmentResponse, error)
	GetPeerAssessmentsByTemplate(ctx context.Context, templateID string) ([]PeerAssessmentResponse, error)
	GetPendingPeerReviews(ctx context.Context) ([]PeerAssessmentResponse, error)
	CreatePeerAssessment(ctx context.Context, req CreatePeerAssessmentRequest) (*PeerAssessmentResponse, error)
	UpdatePeerAssessment(ctx context.Context, id string, req UpdatePeerAssessmentRequest) (*PeerAssessmentResponse, error)
	DeletePeerAssessment(ctx context.Context, id string) error

	// GroupAssessment
	GetAllGroupAssessments(ctx context.Context) ([]GroupAssessmentResponse, error)
	GetGroupAssessmentByID(ctx context.Context, id string) (*GroupAssessmentResponse, error)
	GetGroupAssessmentsByGroup(ctx context.Context, groupID string) ([]GroupAssessmentResponse, error)
	GetGroupAssessmentsByTemplate(ctx context.Context, templateID string) ([]GroupAssessmentResponse, error)
	CreateGroupAssessment(ctx context.Context, req CreateGroupAssessmentRequest) (*GroupAssessmentResponse, error)
	UpdateGroupAssessment(ctx context.Context, id string, req UpdateGroupAssessmentRequest) (*GroupAssessmentResponse, error)
	DeleteGroupAssessment(ctx context.Context, id string) error

	// GroupAssessmentMember
	GetAllGroupAssessmentMembers(ctx context.Context) ([]GroupAssessmentMemberResponse, error)
	GetGroupAssessmentMemberByID(ctx context.Context, id string) (*GroupAssessmentMemberResponse, error)
	GetGroupAssessmentMembersByGroupAssessment(ctx context.Context, groupAssessmentID string) ([]GroupAssessmentMemberResponse, error)
	GetGroupAssessmentMembersByStudent(ctx context.Context, studentID string) ([]GroupAssessmentMemberResponse, error)
	CreateGroupAssessmentMember(ctx context.Context, req CreateGroupAssessmentMemberRequest) (*GroupAssessmentMemberResponse, error)
	UpdateGroupAssessmentMember(ctx context.Context, id string, req UpdateGroupAssessmentMemberRequest) (*GroupAssessmentMemberResponse, error)
	DeleteGroupAssessmentMember(ctx context.Context, id string) error

	// PeerAssessmentGuideline
	GetAllGuidelines(ctx context.Context) ([]PeerAssessmentGuidelineResponse, error)
	GetGuidelineByID(ctx context.Context, id string) (*PeerAssessmentGuidelineResponse, error)
	GetGuidelinesByPhase(ctx context.Context, phase string) ([]PeerAssessmentGuidelineResponse, error)
	GetGuidelinesByCategory(ctx context.Context, category string) ([]PeerAssessmentGuidelineResponse, error)
	GetActiveGuidelines(ctx context.Context) ([]PeerAssessmentGuidelineResponse, error)
	CreateGuideline(ctx context.Context, req CreatePeerAssessmentGuidelineRequest) (*PeerAssessmentGuidelineResponse, error)
	UpdateGuideline(ctx context.Context, id string, req UpdatePeerAssessmentGuidelineRequest) (*PeerAssessmentGuidelineResponse, error)
	DeleteGuideline(ctx context.Context, id string) error

	// Summary
	GetPeerAssessmentSummary(ctx context.Context) (*PeerAssessmentSummaryResponse, error)
}

type peerAssessmentService struct {
	repo PeerAssessmentRepository
}

func NewPeerAssessmentService(repo PeerAssessmentRepository) PeerAssessmentService {
	return &peerAssessmentService{repo: repo}
}

// PeerAssessmentTemplate Methods
func (s *peerAssessmentService) GetAllTemplates(ctx context.Context) ([]PeerAssessmentTemplateResponse, error) {
	templates, err := s.repo.GetAllTemplates(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentTemplateResponse, len(templates))
	for i, template := range templates {
		responses[i] = *s.templateToResponse(&template)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetTemplateByID(ctx context.Context, id string) (*PeerAssessmentTemplateResponse, error) {
	template, err := s.repo.GetTemplateByID(ctx, id)
	if err != nil {
		return nil, errors.New("template tidak ditemukan")
	}
	return s.templateToResponse(template), nil
}

func (s *peerAssessmentService) GetTemplatesByType(ctx context.Context, assessmentType string) ([]PeerAssessmentTemplateResponse, error) {
	templates, err := s.repo.GetTemplatesByType(ctx, assessmentType)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentTemplateResponse, len(templates))
	for i, template := range templates {
		responses[i] = *s.templateToResponse(&template)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetTemplatesByPhase(ctx context.Context, phase string) ([]PeerAssessmentTemplateResponse, error) {
	templates, err := s.repo.GetTemplatesByPhase(ctx, phase)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentTemplateResponse, len(templates))
	for i, template := range templates {
		responses[i] = *s.templateToResponse(&template)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetTemplatesBySubject(ctx context.Context, subjectID string) ([]PeerAssessmentTemplateResponse, error) {
	templates, err := s.repo.GetTemplatesBySubject(ctx, subjectID)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentTemplateResponse, len(templates))
	for i, template := range templates {
		responses[i] = *s.templateToResponse(&template)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetActiveTemplates(ctx context.Context) ([]PeerAssessmentTemplateResponse, error) {
	templates, err := s.repo.GetActiveTemplates(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentTemplateResponse, len(templates))
	for i, template := range templates {
		responses[i] = *s.templateToResponse(&template)
	}
	return responses, nil
}

func (s *peerAssessmentService) CreateTemplate(ctx context.Context, req CreatePeerAssessmentTemplateRequest) (*PeerAssessmentTemplateResponse, error) {
	var subjectUUID *uuid.UUID
	if req.SubjectID != nil && *req.SubjectID != "" {
		parsed, err := uuid.Parse(*req.SubjectID)
		if err != nil {
			return nil, errors.New("invalid subject ID format")
		}
		subjectUUID = &parsed
	}

	template := &PeerAssessmentTemplate{
		ID:              uuid.New(),
		TemplateName:    req.TemplateName,
		AssessmentType:  req.AssessmentType,
		SubjectID:       subjectUUID,
		Phase:           req.Phase,
		AssessmentFocus: req.AssessmentFocus,
		Description:     req.Description,
		Criteria:        req.Criteria,
		RatingScale:     req.RatingScale,
		Instructions:    req.Instructions,
		IsActive:        true,
	}

	if req.IsActive != nil {
		template.IsActive = *req.IsActive
	}

	if err := s.repo.CreateTemplate(ctx, template); err != nil {
		return nil, err
	}
	return s.templateToResponse(template), nil
}

func (s *peerAssessmentService) UpdateTemplate(ctx context.Context, id string, req UpdatePeerAssessmentTemplateRequest) (*PeerAssessmentTemplateResponse, error) {
	template, err := s.repo.GetTemplateByID(ctx, id)
	if err != nil {
		return nil, errors.New("template tidak ditemukan")
	}

	if req.SubjectID != nil {
		if *req.SubjectID != "" {
			parsed, err := uuid.Parse(*req.SubjectID)
			if err != nil {
				return nil, errors.New("invalid subject ID format")
			}
			template.SubjectID = &parsed
		} else {
			template.SubjectID = nil
		}
	}

	if req.TemplateName != "" {
		template.TemplateName = req.TemplateName
	}
	if req.AssessmentType != "" {
		template.AssessmentType = req.AssessmentType
	}
	if req.Phase != "" {
		template.Phase = req.Phase
	}
	if req.AssessmentFocus != "" {
		template.AssessmentFocus = req.AssessmentFocus
	}
	if req.Description != "" {
		template.Description = req.Description
	}
	if req.Criteria != "" {
		template.Criteria = req.Criteria
	}
	if req.RatingScale != "" {
		template.RatingScale = req.RatingScale
	}
	if req.Instructions != "" {
		template.Instructions = req.Instructions
	}
	if req.IsActive != nil {
		template.IsActive = *req.IsActive
	}

	if err := s.repo.UpdateTemplate(ctx, template); err != nil {
		return nil, err
	}
	return s.templateToResponse(template), nil
}

func (s *peerAssessmentService) DeleteTemplate(ctx context.Context, id string) error {
	_, err := s.repo.GetTemplateByID(ctx, id)
	if err != nil {
		return errors.New("template tidak ditemukan")
	}
	return s.repo.DeleteTemplate(ctx, id)
}

// SelfAssessment Methods
func (s *peerAssessmentService) GetAllSelfAssessments(ctx context.Context) ([]SelfAssessmentResponse, error) {
	assessments, err := s.repo.GetAllSelfAssessments(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]SelfAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.selfAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetSelfAssessmentByID(ctx context.Context, id string) (*SelfAssessmentResponse, error) {
	assessment, err := s.repo.GetSelfAssessmentByID(ctx, id)
	if err != nil {
		return nil, errors.New("self assessment tidak ditemukan")
	}
	return s.selfAssessmentToResponse(assessment), nil
}

func (s *peerAssessmentService) GetSelfAssessmentsByStudent(ctx context.Context, studentID string) ([]SelfAssessmentResponse, error) {
	assessments, err := s.repo.GetSelfAssessmentsByStudent(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]SelfAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.selfAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetSelfAssessmentsByTemplate(ctx context.Context, templateID string) ([]SelfAssessmentResponse, error) {
	assessments, err := s.repo.GetSelfAssessmentsByTemplate(ctx, templateID)
	if err != nil {
		return nil, err
	}

	responses := make([]SelfAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.selfAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) CreateSelfAssessment(ctx context.Context, req CreateSelfAssessmentRequest) (*SelfAssessmentResponse, error) {
	studentUUID, err := uuid.Parse(req.StudentID)
	if err != nil {
		return nil, errors.New("invalid student ID format")
	}

	templateUUID, err := uuid.Parse(req.TemplateID)
	if err != nil {
		return nil, errors.New("invalid template ID format")
	}

	var teacherUUID *uuid.UUID
	if req.TeacherID != nil && *req.TeacherID != "" {
		parsed, err := uuid.Parse(*req.TeacherID)
		if err != nil {
			return nil, errors.New("invalid teacher ID format")
		}
		teacherUUID = &parsed
	}

	assessmentDate := time.Now()
	if req.AssessmentDate != "" {
		parsed, err := time.Parse(time.RFC3339, req.AssessmentDate)
		if err != nil {
			return nil, errors.New("invalid assessment date format")
		}
		assessmentDate = parsed
	}

	assessment := &SelfAssessment{
		ID:              uuid.New(),
		StudentID:       studentUUID,
		TemplateID:      templateUUID,
		TeacherID:       teacherUUID,
		AssessmentDate:  assessmentDate,
		Context:         req.Context,
		Responses:       req.Responses,
		SelfReflection:  req.SelfReflection,
		GoalsSet:        req.GoalsSet,
		ConfidenceLevel: req.ConfidenceLevel,
		TeacherFeedback: req.TeacherFeedback,
	}

	if err := s.repo.CreateSelfAssessment(ctx, assessment); err != nil {
		return nil, err
	}
	return s.selfAssessmentToResponse(assessment), nil
}

func (s *peerAssessmentService) UpdateSelfAssessment(ctx context.Context, id string, req UpdateSelfAssessmentRequest) (*SelfAssessmentResponse, error) {
	assessment, err := s.repo.GetSelfAssessmentByID(ctx, id)
	if err != nil {
		return nil, errors.New("self assessment tidak ditemukan")
	}

	if req.TeacherID != nil {
		if *req.TeacherID != "" {
			parsed, err := uuid.Parse(*req.TeacherID)
			if err != nil {
				return nil, errors.New("invalid teacher ID format")
			}
			assessment.TeacherID = &parsed
		} else {
			assessment.TeacherID = nil
		}
	}

	if req.AssessmentDate != "" {
		parsed, err := time.Parse(time.RFC3339, req.AssessmentDate)
		if err != nil {
			return nil, errors.New("invalid assessment date format")
		}
		assessment.AssessmentDate = parsed
	}

	if req.Context != "" {
		assessment.Context = req.Context
	}
	if req.Responses != "" {
		assessment.Responses = req.Responses
	}
	if req.SelfReflection != "" {
		assessment.SelfReflection = req.SelfReflection
	}
	if req.GoalsSet != nil {
		assessment.GoalsSet = req.GoalsSet
	}
	if req.ConfidenceLevel != "" {
		assessment.ConfidenceLevel = req.ConfidenceLevel
	}
	if req.TeacherFeedback != "" {
		assessment.TeacherFeedback = req.TeacherFeedback
	}

	if err := s.repo.UpdateSelfAssessment(ctx, assessment); err != nil {
		return nil, err
	}
	return s.selfAssessmentToResponse(assessment), nil
}

func (s *peerAssessmentService) DeleteSelfAssessment(ctx context.Context, id string) error {
	_, err := s.repo.GetSelfAssessmentByID(ctx, id)
	if err != nil {
		return errors.New("self assessment tidak ditemukan")
	}
	return s.repo.DeleteSelfAssessment(ctx, id)
}

// PeerAssessment Methods
func (s *peerAssessmentService) GetAllPeerAssessments(ctx context.Context) ([]PeerAssessmentResponse, error) {
	assessments, err := s.repo.GetAllPeerAssessments(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.peerAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetPeerAssessmentByID(ctx context.Context, id string) (*PeerAssessmentResponse, error) {
	assessment, err := s.repo.GetPeerAssessmentByID(ctx, id)
	if err != nil {
		return nil, errors.New("peer assessment tidak ditemukan")
	}
	return s.peerAssessmentToResponse(assessment), nil
}

func (s *peerAssessmentService) GetPeerAssessmentsByAssessor(ctx context.Context, assessorID string) ([]PeerAssessmentResponse, error) {
	assessments, err := s.repo.GetPeerAssessmentsByAssessor(ctx, assessorID)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.peerAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetPeerAssessmentsByAssessed(ctx context.Context, assessedID string) ([]PeerAssessmentResponse, error) {
	assessments, err := s.repo.GetPeerAssessmentsByAssessed(ctx, assessedID)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.peerAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetPeerAssessmentsByTemplate(ctx context.Context, templateID string) ([]PeerAssessmentResponse, error) {
	assessments, err := s.repo.GetPeerAssessmentsByTemplate(ctx, templateID)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.peerAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetPendingPeerReviews(ctx context.Context) ([]PeerAssessmentResponse, error) {
	assessments, err := s.repo.GetPendingPeerReviews(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.peerAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) CreatePeerAssessment(ctx context.Context, req CreatePeerAssessmentRequest) (*PeerAssessmentResponse, error) {
	assessorUUID, err := uuid.Parse(req.AssessorStudentID)
	if err != nil {
		return nil, errors.New("invalid assessor student ID format")
	}

	assessedUUID, err := uuid.Parse(req.AssessedStudentID)
	if err != nil {
		return nil, errors.New("invalid assessed student ID format")
	}

	if assessorUUID == assessedUUID {
		return nil, errors.New("assessor dan assessed tidak boleh sama")
	}

	templateUUID, err := uuid.Parse(req.TemplateID)
	if err != nil {
		return nil, errors.New("invalid template ID format")
	}

	var teacherUUID *uuid.UUID
	if req.TeacherID != nil && *req.TeacherID != "" {
		parsed, err := uuid.Parse(*req.TeacherID)
		if err != nil {
			return nil, errors.New("invalid teacher ID format")
		}
		teacherUUID = &parsed
	}

	assessmentDate := time.Now()
	if req.AssessmentDate != "" {
		parsed, err := time.Parse(time.RFC3339, req.AssessmentDate)
		if err != nil {
			return nil, errors.New("invalid assessment date format")
		}
		assessmentDate = parsed
	}

	assessment := &PeerAssessment{
		ID:                   uuid.New(),
		AssessorStudentID:    assessorUUID,
		AssessedStudentID:    assessedUUID,
		TemplateID:           templateUUID,
		TeacherID:            teacherUUID,
		AssessmentDate:       assessmentDate,
		Context:              req.Context,
		Responses:            req.Responses,
		PositiveFeedback:     req.PositiveFeedback,
		ConstructiveFeedback: req.ConstructiveFeedback,
		Suggestions:          req.Suggestions,
		RelationshipContext:  req.RelationshipContext,
		TeacherReviewStatus:  ReviewStatusPending,
		TeacherNotes:         req.TeacherNotes,
	}

	if err := s.repo.CreatePeerAssessment(ctx, assessment); err != nil {
		return nil, err
	}
	return s.peerAssessmentToResponse(assessment), nil
}

func (s *peerAssessmentService) UpdatePeerAssessment(ctx context.Context, id string, req UpdatePeerAssessmentRequest) (*PeerAssessmentResponse, error) {
	assessment, err := s.repo.GetPeerAssessmentByID(ctx, id)
	if err != nil {
		return nil, errors.New("peer assessment tidak ditemukan")
	}

	if req.TeacherID != nil {
		if *req.TeacherID != "" {
			parsed, err := uuid.Parse(*req.TeacherID)
			if err != nil {
				return nil, errors.New("invalid teacher ID format")
			}
			assessment.TeacherID = &parsed
		} else {
			assessment.TeacherID = nil
		}
	}

	if req.AssessmentDate != "" {
		parsed, err := time.Parse(time.RFC3339, req.AssessmentDate)
		if err != nil {
			return nil, errors.New("invalid assessment date format")
		}
		assessment.AssessmentDate = parsed
	}

	if req.Context != "" {
		assessment.Context = req.Context
	}
	if req.Responses != "" {
		assessment.Responses = req.Responses
	}
	if req.PositiveFeedback != "" {
		assessment.PositiveFeedback = req.PositiveFeedback
	}
	if req.ConstructiveFeedback != "" {
		assessment.ConstructiveFeedback = req.ConstructiveFeedback
	}
	if req.Suggestions != nil {
		assessment.Suggestions = req.Suggestions
	}
	if req.RelationshipContext != "" {
		assessment.RelationshipContext = req.RelationshipContext
	}
	if req.TeacherReviewStatus != "" {
		assessment.TeacherReviewStatus = req.TeacherReviewStatus
	}
	if req.TeacherNotes != "" {
		assessment.TeacherNotes = req.TeacherNotes
	}

	if err := s.repo.UpdatePeerAssessment(ctx, assessment); err != nil {
		return nil, err
	}
	return s.peerAssessmentToResponse(assessment), nil
}

func (s *peerAssessmentService) DeletePeerAssessment(ctx context.Context, id string) error {
	_, err := s.repo.GetPeerAssessmentByID(ctx, id)
	if err != nil {
		return errors.New("peer assessment tidak ditemukan")
	}
	return s.repo.DeletePeerAssessment(ctx, id)
}

// GroupAssessment Methods
func (s *peerAssessmentService) GetAllGroupAssessments(ctx context.Context) ([]GroupAssessmentResponse, error) {
	assessments, err := s.repo.GetAllGroupAssessments(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]GroupAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.groupAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetGroupAssessmentByID(ctx context.Context, id string) (*GroupAssessmentResponse, error) {
	assessment, err := s.repo.GetGroupAssessmentByID(ctx, id)
	if err != nil {
		return nil, errors.New("group assessment tidak ditemukan")
	}
	return s.groupAssessmentToResponse(assessment), nil
}

func (s *peerAssessmentService) GetGroupAssessmentsByGroup(ctx context.Context, groupID string) ([]GroupAssessmentResponse, error) {
	assessments, err := s.repo.GetGroupAssessmentsByGroup(ctx, groupID)
	if err != nil {
		return nil, err
	}

	responses := make([]GroupAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.groupAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetGroupAssessmentsByTemplate(ctx context.Context, templateID string) ([]GroupAssessmentResponse, error) {
	assessments, err := s.repo.GetGroupAssessmentsByTemplate(ctx, templateID)
	if err != nil {
		return nil, err
	}

	responses := make([]GroupAssessmentResponse, len(assessments))
	for i, assessment := range assessments {
		responses[i] = *s.groupAssessmentToResponse(&assessment)
	}
	return responses, nil
}

func (s *peerAssessmentService) CreateGroupAssessment(ctx context.Context, req CreateGroupAssessmentRequest) (*GroupAssessmentResponse, error) {
	templateUUID, err := uuid.Parse(req.TemplateID)
	if err != nil {
		return nil, errors.New("invalid template ID format")
	}

	var teacherUUID *uuid.UUID
	if req.TeacherID != nil && *req.TeacherID != "" {
		parsed, err := uuid.Parse(*req.TeacherID)
		if err != nil {
			return nil, errors.New("invalid teacher ID format")
		}
		teacherUUID = &parsed
	}

	assessmentDate := time.Now()
	if req.AssessmentDate != "" {
		parsed, err := time.Parse(time.RFC3339, req.AssessmentDate)
		if err != nil {
			return nil, errors.New("invalid assessment date format")
		}
		assessmentDate = parsed
	}

	assessment := &GroupAssessment{
		ID:                      uuid.New(),
		GroupID:                 req.GroupID,
		GroupName:               req.GroupName,
		TemplateID:              templateUUID,
		TeacherID:               teacherUUID,
		AssessmentDate:          assessmentDate,
		Context:                 req.Context,
		ProjectDescription:      req.ProjectDescription,
		GroupResponses:          req.GroupResponses,
		IndividualContributions: req.IndividualContributions,
		CollaborationRating:     req.CollaborationRating,
		GroupGoals:              req.GroupGoals,
		GroupReflection:         req.GroupReflection,
		TeacherFeedback:         req.TeacherFeedback,
	}

	if err := s.repo.CreateGroupAssessment(ctx, assessment); err != nil {
		return nil, err
	}
	return s.groupAssessmentToResponse(assessment), nil
}

func (s *peerAssessmentService) UpdateGroupAssessment(ctx context.Context, id string, req UpdateGroupAssessmentRequest) (*GroupAssessmentResponse, error) {
	assessment, err := s.repo.GetGroupAssessmentByID(ctx, id)
	if err != nil {
		return nil, errors.New("group assessment tidak ditemukan")
	}

	if req.TeacherID != nil {
		if *req.TeacherID != "" {
			parsed, err := uuid.Parse(*req.TeacherID)
			if err != nil {
				return nil, errors.New("invalid teacher ID format")
			}
			assessment.TeacherID = &parsed
		} else {
			assessment.TeacherID = nil
		}
	}

	if req.AssessmentDate != "" {
		parsed, err := time.Parse(time.RFC3339, req.AssessmentDate)
		if err != nil {
			return nil, errors.New("invalid assessment date format")
		}
		assessment.AssessmentDate = parsed
	}

	if req.GroupName != "" {
		assessment.GroupName = req.GroupName
	}
	if req.Context != "" {
		assessment.Context = req.Context
	}
	if req.ProjectDescription != "" {
		assessment.ProjectDescription = req.ProjectDescription
	}
	if req.GroupResponses != "" {
		assessment.GroupResponses = req.GroupResponses
	}
	if req.IndividualContributions != "" {
		assessment.IndividualContributions = req.IndividualContributions
	}
	if req.CollaborationRating != "" {
		assessment.CollaborationRating = req.CollaborationRating
	}
	if req.GroupGoals != nil {
		assessment.GroupGoals = req.GroupGoals
	}
	if req.GroupReflection != "" {
		assessment.GroupReflection = req.GroupReflection
	}
	if req.TeacherFeedback != "" {
		assessment.TeacherFeedback = req.TeacherFeedback
	}

	if err := s.repo.UpdateGroupAssessment(ctx, assessment); err != nil {
		return nil, err
	}
	return s.groupAssessmentToResponse(assessment), nil
}

func (s *peerAssessmentService) DeleteGroupAssessment(ctx context.Context, id string) error {
	_, err := s.repo.GetGroupAssessmentByID(ctx, id)
	if err != nil {
		return errors.New("group assessment tidak ditemukan")
	}
	return s.repo.DeleteGroupAssessment(ctx, id)
}

// GroupAssessmentMember Methods
func (s *peerAssessmentService) GetAllGroupAssessmentMembers(ctx context.Context) ([]GroupAssessmentMemberResponse, error) {
	members, err := s.repo.GetAllGroupAssessmentMembers(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]GroupAssessmentMemberResponse, len(members))
	for i, member := range members {
		responses[i] = *s.groupAssessmentMemberToResponse(&member)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetGroupAssessmentMemberByID(ctx context.Context, id string) (*GroupAssessmentMemberResponse, error) {
	member, err := s.repo.GetGroupAssessmentMemberByID(ctx, id)
	if err != nil {
		return nil, errors.New("group assessment member tidak ditemukan")
	}
	return s.groupAssessmentMemberToResponse(member), nil
}

func (s *peerAssessmentService) GetGroupAssessmentMembersByGroupAssessment(ctx context.Context, groupAssessmentID string) ([]GroupAssessmentMemberResponse, error) {
	members, err := s.repo.GetGroupAssessmentMembersByGroupAssessment(ctx, groupAssessmentID)
	if err != nil {
		return nil, err
	}

	responses := make([]GroupAssessmentMemberResponse, len(members))
	for i, member := range members {
		responses[i] = *s.groupAssessmentMemberToResponse(&member)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetGroupAssessmentMembersByStudent(ctx context.Context, studentID string) ([]GroupAssessmentMemberResponse, error) {
	members, err := s.repo.GetGroupAssessmentMembersByStudent(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]GroupAssessmentMemberResponse, len(members))
	for i, member := range members {
		responses[i] = *s.groupAssessmentMemberToResponse(&member)
	}
	return responses, nil
}

func (s *peerAssessmentService) CreateGroupAssessmentMember(ctx context.Context, req CreateGroupAssessmentMemberRequest) (*GroupAssessmentMemberResponse, error) {
	groupAssessmentUUID, err := uuid.Parse(req.GroupAssessmentID)
	if err != nil {
		return nil, errors.New("invalid group assessment ID format")
	}

	studentUUID, err := uuid.Parse(req.StudentID)
	if err != nil {
		return nil, errors.New("invalid student ID format")
	}

	member := &GroupAssessmentMember{
		ID:                     uuid.New(),
		GroupAssessmentID:      groupAssessmentUUID,
		StudentID:              studentUUID,
		Role:                   req.Role,
		ParticipationRating:    req.ParticipationRating,
		PeerFeedbackReceived:   req.PeerFeedbackReceived,
		SelfContributionRating: req.SelfContributionRating,
		ContributionNotes:      req.ContributionNotes,
	}

	if err := s.repo.CreateGroupAssessmentMember(ctx, member); err != nil {
		return nil, err
	}
	return s.groupAssessmentMemberToResponse(member), nil
}

func (s *peerAssessmentService) UpdateGroupAssessmentMember(ctx context.Context, id string, req UpdateGroupAssessmentMemberRequest) (*GroupAssessmentMemberResponse, error) {
	member, err := s.repo.GetGroupAssessmentMemberByID(ctx, id)
	if err != nil {
		return nil, errors.New("group assessment member tidak ditemukan")
	}

	if req.Role != "" {
		member.Role = req.Role
	}
	if req.ParticipationRating != "" {
		member.ParticipationRating = req.ParticipationRating
	}
	if req.PeerFeedbackReceived != nil {
		member.PeerFeedbackReceived = req.PeerFeedbackReceived
	}
	if req.SelfContributionRating != "" {
		member.SelfContributionRating = req.SelfContributionRating
	}
	if req.ContributionNotes != "" {
		member.ContributionNotes = req.ContributionNotes
	}

	if err := s.repo.UpdateGroupAssessmentMember(ctx, member); err != nil {
		return nil, err
	}
	return s.groupAssessmentMemberToResponse(member), nil
}

func (s *peerAssessmentService) DeleteGroupAssessmentMember(ctx context.Context, id string) error {
	_, err := s.repo.GetGroupAssessmentMemberByID(ctx, id)
	if err != nil {
		return errors.New("group assessment member tidak ditemukan")
	}
	return s.repo.DeleteGroupAssessmentMember(ctx, id)
}

// PeerAssessmentGuideline Methods
func (s *peerAssessmentService) GetAllGuidelines(ctx context.Context) ([]PeerAssessmentGuidelineResponse, error) {
	guidelines, err := s.repo.GetAllGuidelines(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentGuidelineResponse, len(guidelines))
	for i, guideline := range guidelines {
		responses[i] = *s.guidelineToResponse(&guideline)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetGuidelineByID(ctx context.Context, id string) (*PeerAssessmentGuidelineResponse, error) {
	guideline, err := s.repo.GetGuidelineByID(ctx, id)
	if err != nil {
		return nil, errors.New("guideline tidak ditemukan")
	}
	return s.guidelineToResponse(guideline), nil
}

func (s *peerAssessmentService) GetGuidelinesByPhase(ctx context.Context, phase string) ([]PeerAssessmentGuidelineResponse, error) {
	guidelines, err := s.repo.GetGuidelinesByPhase(ctx, phase)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentGuidelineResponse, len(guidelines))
	for i, guideline := range guidelines {
		responses[i] = *s.guidelineToResponse(&guideline)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetGuidelinesByCategory(ctx context.Context, category string) ([]PeerAssessmentGuidelineResponse, error) {
	guidelines, err := s.repo.GetGuidelinesByCategory(ctx, category)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentGuidelineResponse, len(guidelines))
	for i, guideline := range guidelines {
		responses[i] = *s.guidelineToResponse(&guideline)
	}
	return responses, nil
}

func (s *peerAssessmentService) GetActiveGuidelines(ctx context.Context) ([]PeerAssessmentGuidelineResponse, error) {
	guidelines, err := s.repo.GetActiveGuidelines(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]PeerAssessmentGuidelineResponse, len(guidelines))
	for i, guideline := range guidelines {
		responses[i] = *s.guidelineToResponse(&guideline)
	}
	return responses, nil
}

func (s *peerAssessmentService) CreateGuideline(ctx context.Context, req CreatePeerAssessmentGuidelineRequest) (*PeerAssessmentGuidelineResponse, error) {
	guideline := &PeerAssessmentGuideline{
		ID:                uuid.New(),
		Phase:             req.Phase,
		GuidelineCategory: req.GuidelineCategory,
		Title:             req.Title,
		Content:           req.Content,
		Examples:          req.Examples,
		DoS:               req.DoS,
		DontS:             req.DontS,
		DisplayOrder:      req.DisplayOrder,
		IsActive:          true,
	}

	if req.IsActive != nil {
		guideline.IsActive = *req.IsActive
	}

	if err := s.repo.CreateGuideline(ctx, guideline); err != nil {
		return nil, err
	}
	return s.guidelineToResponse(guideline), nil
}

func (s *peerAssessmentService) UpdateGuideline(ctx context.Context, id string, req UpdatePeerAssessmentGuidelineRequest) (*PeerAssessmentGuidelineResponse, error) {
	guideline, err := s.repo.GetGuidelineByID(ctx, id)
	if err != nil {
		return nil, errors.New("guideline tidak ditemukan")
	}

	if req.Phase != "" {
		guideline.Phase = req.Phase
	}
	if req.GuidelineCategory != "" {
		guideline.GuidelineCategory = req.GuidelineCategory
	}
	if req.Title != "" {
		guideline.Title = req.Title
	}
	if req.Content != "" {
		guideline.Content = req.Content
	}
	if req.Examples != nil {
		guideline.Examples = req.Examples
	}
	if req.DoS != nil {
		guideline.DoS = req.DoS
	}
	if req.DontS != nil {
		guideline.DontS = req.DontS
	}
	if req.DisplayOrder != 0 {
		guideline.DisplayOrder = req.DisplayOrder
	}
	if req.IsActive != nil {
		guideline.IsActive = *req.IsActive
	}

	if err := s.repo.UpdateGuideline(ctx, guideline); err != nil {
		return nil, err
	}
	return s.guidelineToResponse(guideline), nil
}

func (s *peerAssessmentService) DeleteGuideline(ctx context.Context, id string) error {
	_, err := s.repo.GetGuidelineByID(ctx, id)
	if err != nil {
		return errors.New("guideline tidak ditemukan")
	}
	return s.repo.DeleteGuideline(ctx, id)
}

// Summary Method
func (s *peerAssessmentService) GetPeerAssessmentSummary(ctx context.Context) (*PeerAssessmentSummaryResponse, error) {
	return s.repo.GetPeerAssessmentSummary(ctx)
}

// Helper methods for converting models to responses
func (s *peerAssessmentService) templateToResponse(template *PeerAssessmentTemplate) *PeerAssessmentTemplateResponse {
	var subjectID *string
	if template.SubjectID != nil {
		id := template.SubjectID.String()
		subjectID = &id
	}

	var createdBy *string
	if template.CreatedBy != nil {
		id := template.CreatedBy.String()
		createdBy = &id
	}

	var updatedBy *string
	if template.UpdatedBy != nil {
		id := template.UpdatedBy.String()
		updatedBy = &id
	}

	return &PeerAssessmentTemplateResponse{
		ID:              template.ID.String(),
		TemplateName:    template.TemplateName,
		AssessmentType:  template.AssessmentType,
		SubjectID:       subjectID,
		Phase:           template.Phase,
		AssessmentFocus: template.AssessmentFocus,
		Description:     template.Description,
		Criteria:        template.Criteria,
		RatingScale:     template.RatingScale,
		Instructions:    template.Instructions,
		IsActive:        template.IsActive,
		CreatedAt:       template.CreatedAt,
		UpdatedAt:       template.UpdatedAt,
		CreatedBy:       createdBy,
		UpdatedBy:       updatedBy,
	}
}

func (s *peerAssessmentService) selfAssessmentToResponse(assessment *SelfAssessment) *SelfAssessmentResponse {
	var teacherID *string
	if assessment.TeacherID != nil {
		id := assessment.TeacherID.String()
		teacherID = &id
	}

	return &SelfAssessmentResponse{
		ID:              assessment.ID.String(),
		StudentID:       assessment.StudentID.String(),
		TemplateID:      assessment.TemplateID.String(),
		TeacherID:       teacherID,
		AssessmentDate:  assessment.AssessmentDate,
		Context:         assessment.Context,
		Responses:       assessment.Responses,
		SelfReflection:  assessment.SelfReflection,
		GoalsSet:        assessment.GoalsSet,
		ConfidenceLevel: assessment.ConfidenceLevel,
		TeacherFeedback: assessment.TeacherFeedback,
		CreatedAt:       assessment.CreatedAt,
		UpdatedAt:       assessment.UpdatedAt,
	}
}

func (s *peerAssessmentService) peerAssessmentToResponse(assessment *PeerAssessment) *PeerAssessmentResponse {
	var teacherID *string
	if assessment.TeacherID != nil {
		id := assessment.TeacherID.String()
		teacherID = &id
	}

	return &PeerAssessmentResponse{
		ID:                   assessment.ID.String(),
		AssessorStudentID:    assessment.AssessorStudentID.String(),
		AssessedStudentID:    assessment.AssessedStudentID.String(),
		TemplateID:           assessment.TemplateID.String(),
		TeacherID:            teacherID,
		AssessmentDate:       assessment.AssessmentDate,
		Context:              assessment.Context,
		Responses:            assessment.Responses,
		PositiveFeedback:     assessment.PositiveFeedback,
		ConstructiveFeedback: assessment.ConstructiveFeedback,
		Suggestions:          assessment.Suggestions,
		RelationshipContext:  assessment.RelationshipContext,
		TeacherReviewStatus:  assessment.TeacherReviewStatus,
		TeacherNotes:         assessment.TeacherNotes,
		CreatedAt:            assessment.CreatedAt,
		UpdatedAt:            assessment.UpdatedAt,
	}
}

func (s *peerAssessmentService) groupAssessmentToResponse(assessment *GroupAssessment) *GroupAssessmentResponse {
	var teacherID *string
	if assessment.TeacherID != nil {
		id := assessment.TeacherID.String()
		teacherID = &id
	}

	return &GroupAssessmentResponse{
		ID:                      assessment.ID.String(),
		GroupID:                 assessment.GroupID.String(),
		GroupName:               assessment.GroupName,
		TemplateID:              assessment.TemplateID.String(),
		TeacherID:               teacherID,
		AssessmentDate:          assessment.AssessmentDate,
		Context:                 assessment.Context,
		ProjectDescription:      assessment.ProjectDescription,
		GroupResponses:          assessment.GroupResponses,
		IndividualContributions: assessment.IndividualContributions,
		CollaborationRating:     assessment.CollaborationRating,
		GroupGoals:              assessment.GroupGoals,
		GroupReflection:         assessment.GroupReflection,
		TeacherFeedback:         assessment.TeacherFeedback,
		CreatedAt:               assessment.CreatedAt,
		UpdatedAt:               assessment.UpdatedAt,
	}
}

func (s *peerAssessmentService) groupAssessmentMemberToResponse(member *GroupAssessmentMember) *GroupAssessmentMemberResponse {
	return &GroupAssessmentMemberResponse{
		ID:                     member.ID.String(),
		GroupAssessmentID:      member.GroupAssessmentID.String(),
		StudentID:              member.StudentID.String(),
		Role:                   member.Role,
		ParticipationRating:    member.ParticipationRating,
		PeerFeedbackReceived:   member.PeerFeedbackReceived,
		SelfContributionRating: member.SelfContributionRating,
		ContributionNotes:      member.ContributionNotes,
		CreatedAt:              member.CreatedAt,
		UpdatedAt:              member.UpdatedAt,
	}
}

func (s *peerAssessmentService) guidelineToResponse(guideline *PeerAssessmentGuideline) *PeerAssessmentGuidelineResponse {
	var createdBy *string
	if guideline.CreatedBy != nil {
		id := guideline.CreatedBy.String()
		createdBy = &id
	}

	var updatedBy *string
	if guideline.UpdatedBy != nil {
		id := guideline.UpdatedBy.String()
		updatedBy = &id
	}

	return &PeerAssessmentGuidelineResponse{
		ID:                guideline.ID.String(),
		Phase:             guideline.Phase,
		GuidelineCategory: guideline.GuidelineCategory,
		Title:             guideline.Title,
		Content:           guideline.Content,
		Examples:          guideline.Examples,
		DoS:               guideline.DoS,
		DontS:             guideline.DontS,
		DisplayOrder:      guideline.DisplayOrder,
		IsActive:          guideline.IsActive,
		CreatedAt:         guideline.CreatedAt,
		UpdatedAt:         guideline.UpdatedAt,
		CreatedBy:         createdBy,
		UpdatedBy:         updatedBy,
	}
}
