package individual_learning_plan

import (
	"context"
	"errors"
	"time"

	"github.com/google/uuid"
)

type ILPService interface {
	// Individual Learning Plan CRUD
	CreateILP(ctx context.Context, req *CreateILPRequest) (*ILPResponse, error)
	GetILPByID(ctx context.Context, id uuid.UUID) (*ILPDetailResponse, error)
	GetILPByStudentID(ctx context.Context, studentID uuid.UUID) ([]ILPResponse, error)
	GetILPByStudentAndAcademicYear(ctx context.Context, studentID, academicYearID uuid.UUID) (*ILPDetailResponse, error)
	GetAllILPs(ctx context.Context) ([]ILPResponse, error)
	UpdateILP(ctx context.Context, id uuid.UUID, req *UpdateILPRequest) (*ILPResponse, error)
	DeleteILP(ctx context.Context, id uuid.UUID) error

	// ILP Milestone CRUD
	CreateMilestone(ctx context.Context, req *CreateMilestoneRequest) (*MilestoneResponse, error)
	GetMilestoneByID(ctx context.Context, id uuid.UUID) (*MilestoneResponse, error)
	GetMilestonesByILPID(ctx context.Context, ilpID uuid.UUID) ([]MilestoneResponse, error)
	UpdateMilestone(ctx context.Context, id uuid.UUID, req *UpdateMilestoneRequest) (*MilestoneResponse, error)
	DeleteMilestone(ctx context.Context, id uuid.UUID) error

	// ILP Template CRUD
	CreateTemplate(ctx context.Context, req *CreateTemplateRequest) (*ILPTemplateResponse, error)
	GetTemplateByID(ctx context.Context, id uuid.UUID) (*ILPTemplateResponse, error)
	GetAllTemplates(ctx context.Context) ([]ILPTemplateResponse, error)
	GetActiveTemplates(ctx context.Context) ([]ILPTemplateResponse, error)
	GetTemplatesByPhase(ctx context.Context, phaseID uuid.UUID) ([]ILPTemplateResponse, error)
	UpdateTemplate(ctx context.Context, id uuid.UUID, req *UpdateTemplateRequest) (*ILPTemplateResponse, error)
	DeleteTemplate(ctx context.Context, id uuid.UUID) error

	// Summary
	GetILPSummary(ctx context.Context) (*ILPSummaryResponse, error)
}

type ilpService struct {
	repo ILPRepository
}

func NewILPService(repo ILPRepository) ILPService {
	return &ilpService{repo: repo}
}

// Helper functions to convert models to response DTOs

func ilpToResponse(ilp *IndividualLearningPlan) *ILPResponse {
	return &ILPResponse{
		ID:             ilp.ID,
		StudentID:      ilp.StudentID,
		AcademicYearID: ilp.AcademicYearID,
		Title:          ilp.Title,
		Goals:          ilp.Goals,
		Strategies:     ilp.Strategies,
		Accommodations: ilp.Accommodations,
		ParentNotes:    ilp.ParentNotes,
		TeacherNotes:   ilp.TeacherNotes,
		Status:         ilp.Status,
		CreatedAt:      ilp.CreatedAt,
		UpdatedAt:      ilp.UpdatedAt,
	}
}

func milestoneToResponse(milestone *ILPMilestone) *MilestoneResponse {
	return &MilestoneResponse{
		ID:            milestone.ID,
		ILPID:         milestone.ILPID,
		MilestoneName: milestone.MilestoneName,
		TargetDate:    milestone.TargetDate,
		Achieved:      milestone.Achieved,
		AchievedDate:  milestone.AchievedDate,
		Notes:         milestone.Notes,
		CreatedAt:     milestone.CreatedAt,
		UpdatedAt:     milestone.UpdatedAt,
	}
}

func templateToResponse(template *ILPTemplate) *ILPTemplateResponse {
	return &ILPTemplateResponse{
		ID:                template.ID,
		TemplateCode:      template.TemplateCode,
		TemplateName:      template.TemplateName,
		PhaseID:           template.PhaseID,
		Description:       template.Description,
		DefaultGoals:      template.DefaultGoals,
		DefaultStrategies: template.DefaultStrategies,
		IsActive:          template.IsActive,
		CreatedAt:         template.CreatedAt,
		UpdatedAt:         template.UpdatedAt,
	}
}

// Individual Learning Plan CRUD

func (s *ilpService) CreateILP(ctx context.Context, req *CreateILPRequest) (*ILPResponse, error) {
	ilp := &IndividualLearningPlan{
		ID:             uuid.New(),
		StudentID:      req.StudentID,
		AcademicYearID: req.AcademicYearID,
		Title:          req.Title,
		Goals:          req.Goals,
		Strategies:     req.Strategies,
		Accommodations: req.Accommodations,
		ParentNotes:    req.ParentNotes,
		TeacherNotes:   req.TeacherNotes,
		Status:         ILPStatusActive,
	}

	err := s.repo.CreateILP(ctx, ilp)
	if err != nil {
		return nil, err
	}

	return ilpToResponse(ilp), nil
}

func (s *ilpService) GetILPByID(ctx context.Context, id uuid.UUID) (*ILPDetailResponse, error) {
	ilp, err := s.repo.GetILPByID(ctx, id)
	if err != nil {
		return nil, err
	}

	milestones, _ := s.repo.GetMilestonesByILPID(ctx, id)
	milestoneResponses := make([]MilestoneResponse, len(milestones))
	for i, m := range milestones {
		milestoneResponses[i] = *milestoneToResponse(&m)
	}

	return &ILPDetailResponse{
		ID:             ilp.ID,
		StudentID:      ilp.StudentID,
		AcademicYearID: ilp.AcademicYearID,
		Title:          ilp.Title,
		Goals:          ilp.Goals,
		Strategies:     ilp.Strategies,
		Accommodations: ilp.Accommodations,
		ParentNotes:    ilp.ParentNotes,
		TeacherNotes:   ilp.TeacherNotes,
		Status:         ilp.Status,
		CreatedAt:      ilp.CreatedAt,
		UpdatedAt:      ilp.UpdatedAt,
		Milestones:     milestoneResponses,
	}, nil
}

func (s *ilpService) GetILPByStudentID(ctx context.Context, studentID uuid.UUID) ([]ILPResponse, error) {
	ilps, err := s.repo.GetILPByStudentID(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]ILPResponse, len(ilps))
	for i, ilp := range ilps {
		responses[i] = *ilpToResponse(&ilp)
	}
	return responses, nil
}

func (s *ilpService) GetILPByStudentAndAcademicYear(ctx context.Context, studentID, academicYearID uuid.UUID) (*ILPDetailResponse, error) {
	ilp, err := s.repo.GetILPByStudentAndAcademicYear(ctx, studentID, academicYearID)
	if err != nil {
		return nil, err
	}

	milestones, _ := s.repo.GetMilestonesByILPID(ctx, ilp.ID)
	milestoneResponses := make([]MilestoneResponse, len(milestones))
	for i, m := range milestones {
		milestoneResponses[i] = *milestoneToResponse(&m)
	}

	return &ILPDetailResponse{
		ID:             ilp.ID,
		StudentID:      ilp.StudentID,
		AcademicYearID: ilp.AcademicYearID,
		Title:          ilp.Title,
		Goals:          ilp.Goals,
		Strategies:     ilp.Strategies,
		Accommodations: ilp.Accommodations,
		ParentNotes:    ilp.ParentNotes,
		TeacherNotes:   ilp.TeacherNotes,
		Status:         ilp.Status,
		CreatedAt:      ilp.CreatedAt,
		UpdatedAt:      ilp.UpdatedAt,
		Milestones:     milestoneResponses,
	}, nil
}

func (s *ilpService) GetAllILPs(ctx context.Context) ([]ILPResponse, error) {
	ilps, err := s.repo.GetAllILPs(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]ILPResponse, len(ilps))
	for i, ilp := range ilps {
		responses[i] = *ilpToResponse(&ilp)
	}
	return responses, nil
}

func (s *ilpService) UpdateILP(ctx context.Context, id uuid.UUID, req *UpdateILPRequest) (*ILPResponse, error) {
	ilp, err := s.repo.GetILPByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.Title != nil {
		ilp.Title = *req.Title
	}
	if req.Goals != nil {
		ilp.Goals = *req.Goals
	}
	if req.Strategies != nil {
		ilp.Strategies = *req.Strategies
	}
	if req.Accommodations != nil {
		ilp.Accommodations = *req.Accommodations
	}
	if req.ParentNotes != nil {
		ilp.ParentNotes = *req.ParentNotes
	}
	if req.TeacherNotes != nil {
		ilp.TeacherNotes = *req.TeacherNotes
	}
	if req.Status != nil {
		if !IsValidILPStatus(*req.Status) {
			return nil, errors.New("invalid status")
		}
		ilp.Status = *req.Status
	}

	err = s.repo.UpdateILP(ctx, ilp)
	if err != nil {
		return nil, err
	}

	return ilpToResponse(ilp), nil
}

func (s *ilpService) DeleteILP(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteILP(ctx, id)
}

// ILP Milestone CRUD

func (s *ilpService) CreateMilestone(ctx context.Context, req *CreateMilestoneRequest) (*MilestoneResponse, error) {
	// Validate ILP exists
	_, err := s.repo.GetILPByID(ctx, req.ILPID)
	if err != nil {
		return nil, errors.New("ILP not found")
	}

	// Parse target date
	targetDate, err := time.Parse("2006-01-02", req.TargetDate)
	if err != nil {
		return nil, errors.New("invalid target date format")
	}

	milestone := &ILPMilestone{
		ID:            uuid.New(),
		ILPID:         req.ILPID,
		MilestoneName: req.MilestoneName,
		TargetDate:    targetDate,
		Achieved:      false,
		Notes:         req.Notes,
	}

	err = s.repo.CreateMilestone(ctx, milestone)
	if err != nil {
		return nil, err
	}

	return milestoneToResponse(milestone), nil
}

func (s *ilpService) GetMilestoneByID(ctx context.Context, id uuid.UUID) (*MilestoneResponse, error) {
	milestone, err := s.repo.GetMilestoneByID(ctx, id)
	if err != nil {
		return nil, err
	}
	return milestoneToResponse(milestone), nil
}

func (s *ilpService) GetMilestonesByILPID(ctx context.Context, ilpID uuid.UUID) ([]MilestoneResponse, error) {
	milestones, err := s.repo.GetMilestonesByILPID(ctx, ilpID)
	if err != nil {
		return nil, err
	}

	responses := make([]MilestoneResponse, len(milestones))
	for i, m := range milestones {
		responses[i] = *milestoneToResponse(&m)
	}
	return responses, nil
}

func (s *ilpService) UpdateMilestone(ctx context.Context, id uuid.UUID, req *UpdateMilestoneRequest) (*MilestoneResponse, error) {
	milestone, err := s.repo.GetMilestoneByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.MilestoneName != nil {
		milestone.MilestoneName = *req.MilestoneName
	}
	if req.TargetDate != nil {
		targetDate, err := time.Parse("2006-01-02", *req.TargetDate)
		if err != nil {
			return nil, errors.New("invalid target date format")
		}
		milestone.TargetDate = targetDate
	}
	if req.Achieved != nil {
		milestone.Achieved = *req.Achieved
		if *req.Achieved {
			now := time.Now()
			milestone.AchievedDate = &now
		}
	}
	if req.Notes != nil {
		milestone.Notes = *req.Notes
	}

	err = s.repo.UpdateMilestone(ctx, milestone)
	if err != nil {
		return nil, err
	}

	return milestoneToResponse(milestone), nil
}

func (s *ilpService) DeleteMilestone(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteMilestone(ctx, id)
}

// ILP Template CRUD

type CreateTemplateRequest struct {
	TemplateCode      string    `json:"template_code" binding:"required"`
	TemplateName      string    `json:"template_name" binding:"required"`
	PhaseID           uuid.UUID `json:"phase_id"`
	Description       string    `json:"description"`
	DefaultGoals      string    `json:"default_goals"`
	DefaultStrategies string    `json:"default_strategies"`
}

type UpdateTemplateRequest struct {
	TemplateName      *string    `json:"template_name"`
	PhaseID           *uuid.UUID `json:"phase_id"`
	Description       *string    `json:"description"`
	DefaultGoals      *string    `json:"default_goals"`
	DefaultStrategies *string    `json:"default_strategies"`
	IsActive          *bool      `json:"is_active"`
}

func (s *ilpService) CreateTemplate(ctx context.Context, req *CreateTemplateRequest) (*ILPTemplateResponse, error) {
	// Check if template code already exists
	existing, _ := s.repo.GetTemplateByCode(ctx, req.TemplateCode)
	if existing != nil {
		return nil, errors.New("template code already exists")
	}

	template := &ILPTemplate{
		ID:                uuid.New(),
		TemplateCode:      req.TemplateCode,
		TemplateName:      req.TemplateName,
		PhaseID:           req.PhaseID,
		Description:       req.Description,
		DefaultGoals:      req.DefaultGoals,
		DefaultStrategies: req.DefaultStrategies,
		IsActive:          true,
	}

	err := s.repo.CreateTemplate(ctx, template)
	if err != nil {
		return nil, err
	}

	return templateToResponse(template), nil
}

func (s *ilpService) GetTemplateByID(ctx context.Context, id uuid.UUID) (*ILPTemplateResponse, error) {
	template, err := s.repo.GetTemplateByID(ctx, id)
	if err != nil {
		return nil, err
	}
	return templateToResponse(template), nil
}

func (s *ilpService) GetAllTemplates(ctx context.Context) ([]ILPTemplateResponse, error) {
	templates, err := s.repo.GetAllTemplates(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]ILPTemplateResponse, len(templates))
	for i, t := range templates {
		responses[i] = *templateToResponse(&t)
	}
	return responses, nil
}

func (s *ilpService) GetActiveTemplates(ctx context.Context) ([]ILPTemplateResponse, error) {
	templates, err := s.repo.GetActiveTemplates(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]ILPTemplateResponse, len(templates))
	for i, t := range templates {
		responses[i] = *templateToResponse(&t)
	}
	return responses, nil
}

func (s *ilpService) GetTemplatesByPhase(ctx context.Context, phaseID uuid.UUID) ([]ILPTemplateResponse, error) {
	templates, err := s.repo.GetTemplatesByPhase(ctx, phaseID)
	if err != nil {
		return nil, err
	}

	responses := make([]ILPTemplateResponse, len(templates))
	for i, t := range templates {
		responses[i] = *templateToResponse(&t)
	}
	return responses, nil
}

func (s *ilpService) UpdateTemplate(ctx context.Context, id uuid.UUID, req *UpdateTemplateRequest) (*ILPTemplateResponse, error) {
	template, err := s.repo.GetTemplateByID(ctx, id)
	if err != nil {
		return nil, err
	}

	// Update fields if provided
	if req.TemplateName != nil {
		template.TemplateName = *req.TemplateName
	}
	if req.PhaseID != nil {
		template.PhaseID = *req.PhaseID
	}
	if req.Description != nil {
		template.Description = *req.Description
	}
	if req.DefaultGoals != nil {
		template.DefaultGoals = *req.DefaultGoals
	}
	if req.DefaultStrategies != nil {
		template.DefaultStrategies = *req.DefaultStrategies
	}
	if req.IsActive != nil {
		template.IsActive = *req.IsActive
	}

	err = s.repo.UpdateTemplate(ctx, template)
	if err != nil {
		return nil, err
	}

	return templateToResponse(template), nil
}

func (s *ilpService) DeleteTemplate(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteTemplate(ctx, id)
}

// Summary

func (s *ilpService) GetILPSummary(ctx context.Context) (*ILPSummaryResponse, error) {
	ilps, err := s.repo.GetAllILPs(ctx)
	if err != nil {
		return nil, err
	}

	totalILPs := len(ilps)
	activeILPs := 0
	completedILPs := 0

	for _, ilp := range ilps {
		if ilp.Status == ILPStatusActive {
			activeILPs++
		} else if ilp.Status == ILPStatusCompleted {
			completedILPs++
		}
	}

	// Get recent ILPs (last 5)
	recentCount := 5
	if totalILPs < recentCount {
		recentCount = totalILPs
	}
	recentILPs := make([]ILPResponse, recentCount)
	for i := 0; i < recentCount; i++ {
		recentILPs[i] = *ilpToResponse(&ilps[i])
	}

	// Calculate milestone stats
	milestoneStats := make(map[string]int)
	for _, ilp := range ilps {
		milestones, _ := s.repo.GetMilestonesByILPID(ctx, ilp.ID)
		total := len(milestones)
		achieved := 0
		for _, m := range milestones {
			if m.Achieved {
				achieved++
			}
		}
		milestoneStats["total"] += total
		milestoneStats["achieved"] += achieved
	}

	return &ILPSummaryResponse{
		TotalILPs:      totalILPs,
		ActiveILPs:     activeILPs,
		CompletedILPs:  completedILPs,
		RecentILPs:     recentILPs,
		MilestoneStats: milestoneStats,
	}, nil
}
