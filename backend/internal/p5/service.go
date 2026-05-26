package p5

import (
	"context"
	"fmt"
	"strings"

	"github.com/google/uuid"
)

type Service interface {
	// Project operations
	CreateProject(ctx context.Context, req CreateProjectRequest) (*Project, error)
	GetProjectByID(id uuid.UUID) (*Project, error)
	GetProjects(filter map[string]interface{}) ([]Project, error)
	UpdateProject(ctx context.Context, id uuid.UUID, req UpdateProjectRequest) (*Project, error)
	DeleteProject(ctx context.Context, id uuid.UUID) error
	UpdateProjectProgress(ctx context.Context, projectID uuid.UUID) error

	// Team operations
	CreateTeam(ctx context.Context, req CreateTeamRequest) (*ProjectTeam, error)
	GetTeamByID(id uuid.UUID) (*ProjectTeam, error)
	GetTeamsByProject(projectID uuid.UUID) ([]ProjectTeam, error)
	UpdateTeam(ctx context.Context, id uuid.UUID, req UpdateTeamRequest) (*ProjectTeam, error)
	DeleteTeam(ctx context.Context, id uuid.UUID) error
	AutoGenerateTeams(ctx context.Context, req AutoGenerateTeamsRequest) ([]ProjectTeam, error)

	// Team Member operations
	AddTeamMember(ctx context.Context, teamID uuid.UUID, req CreateTeamMemberRequest) (*TeamMember, error)
	GetTeamMembers(teamID uuid.UUID) ([]TeamMember, error)
	UpdateTeamMember(ctx context.Context, id uuid.UUID, req UpdateTeamMemberRequest) (*TeamMember, error)
	RemoveTeamMember(ctx context.Context, id uuid.UUID) error

	// Milestone operations
	CreateMilestone(ctx context.Context, projectID uuid.UUID, req CreateMilestoneRequest) (*ProjectMilestone, error)
	GetMilestoneByID(id uuid.UUID) (*ProjectMilestone, error)
	GetMilestonesByProject(projectID uuid.UUID) ([]ProjectMilestone, error)
	UpdateMilestone(ctx context.Context, id uuid.UUID, req UpdateMilestoneRequest) (*ProjectMilestone, error)
	DeleteMilestone(ctx context.Context, id uuid.UUID) error
	UpdateMilestoneProgress(ctx context.Context, projectID uuid.UUID) error

	// Participation operations
	CreateParticipation(ctx context.Context, req CreateParticipationRequest) (*StudentParticipation, error)
	GetParticipationByID(id uuid.UUID) (*StudentParticipation, error)
	GetParticipationsByProject(projectID uuid.UUID) ([]StudentParticipation, error)
	UpdateParticipation(ctx context.Context, id uuid.UUID, req UpdateParticipationRequest) (*StudentParticipation, error)
	DeleteParticipation(ctx context.Context, id uuid.UUID) error
	RecordFinalAssessment(ctx context.Context, id uuid.UUID, finalScore float64, grade, teacherFeedback string) error
}

type service struct {
	repo Repository
}

func NewService(repo Repository) Service {
	return &service{repo: repo}
}

// Project operations
func (s *service) CreateProject(ctx context.Context, req CreateProjectRequest) (*Project, error) {
	project := &Project{
		ID:                 uuid.New(),
		Title:              req.Title,
		Description:        req.Description,
		ProjectTheme:       req.ProjectTheme,
		Semester:           req.Semester,
		StartDate:          req.StartDate,
		EndDate:            req.EndDate,
		TotalWeeks:         req.TotalWeeks,
		ProjectType:        req.ProjectType,
		MaxTeamSize:        req.MaxTeamSize,
		RequiredDimensions: req.RequiredDimensions,
		Status:             ProjectStatusPlanning,
		Progress:           0,
	}

	if req.SubjectID != "" {
		subjectID, err := uuid.Parse(req.SubjectID)
		if err != nil {
			return nil, fmt.Errorf("invalid subject_id: %w", err)
		}
		project.SubjectID = &subjectID
	}

	if req.ClassroomID != "" {
		classroomID, err := uuid.Parse(req.ClassroomID)
		if err != nil {
			return nil, fmt.Errorf("invalid classroom_id: %w", err)
		}
		project.ClassroomID = &classroomID
	}

	if req.AcademicYearID != "" {
		academicYearID, err := uuid.Parse(req.AcademicYearID)
		if err != nil {
			return nil, fmt.Errorf("invalid academic_year_id: %w", err)
		}
		project.AcademicYearID = &academicYearID
	}

	if req.TeachingModuleID != "" {
		teachingModuleID, err := uuid.Parse(req.TeachingModuleID)
		if err != nil {
			return nil, fmt.Errorf("invalid teaching_module_id: %w", err)
		}
		project.TeachingModuleID = &teachingModuleID
	}

	if req.RubricID != "" {
		rubricID, err := uuid.Parse(req.RubricID)
		if err != nil {
			return nil, fmt.Errorf("invalid rubric_id: %w", err)
		}
		project.RubricID = &rubricID
	}

	err := s.repo.CreateProject(ctx, project)
	if err != nil {
		return nil, err
	}

	// Create milestones if provided
	if len(req.Milestones) > 0 {
		for i, milestoneReq := range req.Milestones {
			if milestoneReq.Sequence == 0 {
				milestoneReq.Sequence = i + 1
			}
			milestone := &ProjectMilestone{
				ID:             uuid.New(),
				ProjectID:      project.ID,
				Title:          milestoneReq.Title,
				Description:    milestoneReq.Description,
				Sequence:       milestoneReq.Sequence,
				StartDate:      milestoneReq.StartDate,
				EndDate:        milestoneReq.EndDate,
				RequiredHours:  milestoneReq.RequiredHours,
				Deliverables:   milestoneReq.Deliverables,
				AssessmentType: milestoneReq.AssessmentType,
				Status:         MilestoneStatusNotStarted,
			}
			err := s.repo.CreateMilestone(ctx, milestone)
			if err != nil {
				return nil, fmt.Errorf("failed to create milestone: %w", err)
			}
		}
	}

	return s.repo.GetProjectByID(project.ID)
}

func (s *service) GetProjectByID(id uuid.UUID) (*Project, error) {
	return s.repo.GetProjectByID(id)
}

func (s *service) GetProjects(filter map[string]interface{}) ([]Project, error) {
	return s.repo.GetProjects(filter)
}

func (s *service) UpdateProject(ctx context.Context, id uuid.UUID, req UpdateProjectRequest) (*Project, error) {
	project, err := s.repo.GetProjectByID(id)
	if err != nil {
		return nil, err
	}

	if req.Title != "" {
		project.Title = req.Title
	}
	if req.Description != "" {
		project.Description = req.Description
	}
	if req.ProjectTheme != "" {
		project.ProjectTheme = req.ProjectTheme
	}
	if req.Semester > 0 {
		project.Semester = req.Semester
	}
	if req.StartDate != "" {
		project.StartDate = req.StartDate
	}
	if req.EndDate != "" {
		project.EndDate = req.EndDate
	}
	if req.TotalWeeks > 0 {
		project.TotalWeeks = req.TotalWeeks
	}
	if req.ProjectType != "" {
		project.ProjectType = req.ProjectType
	}
	if req.MaxTeamSize > 0 {
		project.MaxTeamSize = req.MaxTeamSize
	}
	if req.RequiredDimensions != "" {
		project.RequiredDimensions = req.RequiredDimensions
	}
	if req.Status != "" {
		project.Status = req.Status
	}
	if req.Progress >= 0 {
		project.Progress = req.Progress
	}

	if req.SubjectID != "" {
		subjectID, err := uuid.Parse(req.SubjectID)
		if err != nil {
			return nil, fmt.Errorf("invalid subject_id: %w", err)
		}
		project.SubjectID = &subjectID
	}

	if req.ClassroomID != "" {
		classroomID, err := uuid.Parse(req.ClassroomID)
		if err != nil {
			return nil, fmt.Errorf("invalid classroom_id: %w", err)
		}
		project.ClassroomID = &classroomID
	}

	if req.AcademicYearID != "" {
		academicYearID, err := uuid.Parse(req.AcademicYearID)
		if err != nil {
			return nil, fmt.Errorf("invalid academic_year_id: %w", err)
		}
		project.AcademicYearID = &academicYearID
	}

	if req.TeachingModuleID != "" {
		teachingModuleID, err := uuid.Parse(req.TeachingModuleID)
		if err != nil {
			return nil, fmt.Errorf("invalid teaching_module_id: %w", err)
		}
		project.TeachingModuleID = &teachingModuleID
	}

	if req.RubricID != "" {
		rubricID, err := uuid.Parse(req.RubricID)
		if err != nil {
			return nil, fmt.Errorf("invalid rubric_id: %w", err)
		}
		project.RubricID = &rubricID
	}

	err = s.repo.UpdateProject(ctx, project)
	if err != nil {
		return nil, err
	}

	// Update milestones if provided
	if len(req.Milestones) > 0 {
		// Delete existing milestones and recreate
		milestones, _ := s.repo.GetMilestonesByProject(id)
		for _, m := range milestones {
			_ = s.repo.DeleteMilestone(ctx, m.ID)
		}

		for i, milestoneReq := range req.Milestones {
			if milestoneReq.Sequence == 0 {
				milestoneReq.Sequence = i + 1
			}
			milestone := &ProjectMilestone{
				ID:             uuid.New(),
				ProjectID:      project.ID,
				Title:          milestoneReq.Title,
				Description:    milestoneReq.Description,
				Sequence:       milestoneReq.Sequence,
				StartDate:      milestoneReq.StartDate,
				EndDate:        milestoneReq.EndDate,
				RequiredHours:  milestoneReq.RequiredHours,
				Deliverables:   milestoneReq.Deliverables,
				AssessmentType: milestoneReq.AssessmentType,
				Status:         MilestoneStatusNotStarted,
			}
			err := s.repo.CreateMilestone(ctx, milestone)
			if err != nil {
				return nil, fmt.Errorf("failed to create milestone: %w", err)
			}
		}
	}

	return s.repo.GetProjectByID(id)
}

func (s *service) DeleteProject(ctx context.Context, id uuid.UUID) error {
	project, err := s.repo.GetProjectByID(id)
	if err != nil {
		return err
	}

	// Delete associated milestones
	milestones, err := s.repo.GetMilestonesByProject(id)
	if err == nil {
		for _, m := range milestones {
			_ = s.repo.DeleteMilestone(ctx, m.ID)
		}
	}

	// Delete associated teams
	teams, err := s.repo.GetTeamsByProject(id)
	if err == nil {
		for _, t := range teams {
			members, _ := s.repo.GetTeamMembers(t.ID)
			for _, m := range members {
				_ = s.repo.DeleteTeamMember(ctx, m.ID)
			}
			_ = s.repo.DeleteTeam(ctx, t.ID)
		}
	}

	// Delete associated participations
	participations, err := s.repo.GetParticipationsByProject(id)
	if err == nil {
		for _, p := range participations {
			_ = s.repo.DeleteParticipation(ctx, p.ID)
		}
	}

	return s.repo.DeleteProject(ctx, project.ID)
}

func (s *service) UpdateProjectProgress(ctx context.Context, projectID uuid.UUID) error {
	project, err := s.repo.GetProjectByID(projectID)
	if err != nil {
		return err
	}

	milestones, err := s.repo.GetMilestonesByProject(projectID)
	if err != nil {
		return err
	}

	if len(milestones) == 0 {
		return nil
	}

	completedCount := 0
	for _, m := range milestones {
		if m.Status == MilestoneStatusCompleted {
			completedCount++
		}
	}

	progress := int(float64(completedCount) / float64(len(milestones)) * 100)
	project.Progress = progress

	// Update project status based on progress
	if progress == 100 {
		project.Status = ProjectStatusCompleted
	} else if progress > 0 && project.Status == ProjectStatusPlanning {
		project.Status = ProjectStatusOngoing
	}

	return s.repo.UpdateProject(ctx, project)
}

// Team operations
func (s *service) CreateTeam(ctx context.Context, req CreateTeamRequest) (*ProjectTeam, error) {
	project, err := s.repo.GetProjectByID(uuid.MustParse(req.ProjectID))
	if err != nil {
		return nil, fmt.Errorf("project not found: %w", err)
	}

	team := &ProjectTeam{
		ID:          uuid.New(),
		ProjectID:   project.ID,
		TeamName:    req.TeamName,
		TeamCode:    generateTeamCode(),
		MaxMembers:  req.MaxMembers,
		CurrentSize: 0,
		IsActive:    true,
	}

	if req.TeamLeaderID != "" {
		leaderID, err := uuid.Parse(req.TeamLeaderID)
		if err != nil {
			return nil, fmt.Errorf("invalid team_leader_id: %w", err)
		}
		team.TeamLeaderID = &leaderID
	}

	err = s.repo.CreateTeam(ctx, team)
	if err != nil {
		return nil, err
	}

	return s.repo.GetTeamByID(team.ID)
}

func (s *service) GetTeamByID(id uuid.UUID) (*ProjectTeam, error) {
	return s.repo.GetTeamByID(id)
}

func (s *service) GetTeamsByProject(projectID uuid.UUID) ([]ProjectTeam, error) {
	return s.repo.GetTeamsByProject(projectID)
}

func (s *service) UpdateTeam(ctx context.Context, id uuid.UUID, req UpdateTeamRequest) (*ProjectTeam, error) {
	team, err := s.repo.GetTeamByID(id)
	if err != nil {
		return nil, err
	}

	if req.TeamName != "" {
		team.TeamName = req.TeamName
	}
	if req.MaxMembers > 0 {
		team.MaxMembers = req.MaxMembers
	}
	if req.TeamLeaderID != "" {
		leaderID, err := uuid.Parse(req.TeamLeaderID)
		if err != nil {
			return nil, fmt.Errorf("invalid team_leader_id: %w", err)
		}
		team.TeamLeaderID = &leaderID
	}

	team.IsActive = req.IsActive

	err = s.repo.UpdateTeam(ctx, team)
	if err != nil {
		return nil, err
	}

	return s.repo.GetTeamByID(id)
}

func (s *service) DeleteTeam(ctx context.Context, id uuid.UUID) error {
	team, err := s.repo.GetTeamByID(id)
	if err != nil {
		return err
	}

	// Delete team members
	members, err := s.repo.GetTeamMembers(team.ID)
	if err == nil {
		for _, m := range members {
			_ = s.repo.DeleteTeamMember(ctx, m.ID)
		}
	}

	return s.repo.DeleteTeam(ctx, team.ID)
}

func (s *service) AutoGenerateTeams(ctx context.Context, req AutoGenerateTeamsRequest) ([]ProjectTeam, error) {
	project, err := s.repo.GetProjectByID(uuid.MustParse(req.ProjectID))
	if err != nil {
		return nil, fmt.Errorf("project not found: %w", err)
	}

	// For now, create a simple implementation that creates empty teams
	// In a real implementation, this would involve fetching students and balancing them
	teamCount := project.MaxTeamSize / req.TeamSize
	if teamCount == 0 {
		teamCount = 1
	}

	var teams []ProjectTeam
	for i := 0; i < teamCount; i++ {
		team := &ProjectTeam{
			ID:          uuid.New(),
			ProjectID:   project.ID,
			TeamName:    fmt.Sprintf("Tim %d", i+1),
			TeamCode:    generateTeamCode(),
			MaxMembers:  req.TeamSize,
			CurrentSize: 0,
			IsActive:    true,
		}
		err := s.repo.CreateTeam(ctx, team)
		if err != nil {
			return nil, err
		}
		teams = append(teams, *team)
	}

	return teams, nil
}

// Team Member operations
func (s *service) AddTeamMember(ctx context.Context, teamID uuid.UUID, req CreateTeamMemberRequest) (*TeamMember, error) {
	team, err := s.repo.GetTeamByID(teamID)
	if err != nil {
		return nil, fmt.Errorf("team not found: %w", err)
	}

	if team.CurrentSize >= team.MaxMembers {
		return nil, fmt.Errorf("team is at full capacity")
	}

	member := &TeamMember{
		ID:        uuid.New(),
		TeamID:    team.ID,
		StudentID: uuid.MustParse(req.StudentID),
		Role:      req.Role,
		JoinedAt:  req.JoinedAt,
		IsActive:  true,
	}

	if member.Role == "" {
		member.Role = RoleMember
	}

	err = s.repo.CreateTeamMember(ctx, member)
	if err != nil {
		return nil, err
	}

	// Update team current size
	team.CurrentSize++
	err = s.repo.UpdateTeam(ctx, team)
	if err != nil {
		return nil, err
	}

	return member, nil
}

func (s *service) GetTeamMembers(teamID uuid.UUID) ([]TeamMember, error) {
	return s.repo.GetTeamMembers(teamID)
}

func (s *service) UpdateTeamMember(ctx context.Context, id uuid.UUID, req UpdateTeamMemberRequest) (*TeamMember, error) {
	member, err := s.repo.GetTeamMemberByID(id)
	if err != nil {
		return nil, err
	}

	if req.Role != "" {
		member.Role = req.Role
	}

	member.IsActive = req.IsActive

	err = s.repo.UpdateTeamMember(ctx, member)
	if err != nil {
		return nil, err
	}

	return s.repo.GetTeamMemberByID(id)
}

func (s *service) RemoveTeamMember(ctx context.Context, id uuid.UUID) error {
	member, err := s.repo.GetTeamMemberByID(id)
	if err != nil {
		return err
	}

	team, err := s.repo.GetTeamByID(member.TeamID)
	if err != nil {
		return err
	}

	team.CurrentSize--
	_ = s.repo.UpdateTeam(ctx, team)

	return s.repo.DeleteTeamMember(ctx, member.ID)
}

// Milestone operations
func (s *service) CreateMilestone(ctx context.Context, projectID uuid.UUID, req CreateMilestoneRequest) (*ProjectMilestone, error) {
	_, err := s.repo.GetProjectByID(projectID)
	if err != nil {
		return nil, fmt.Errorf("project not found: %w", err)
	}

	milestone := &ProjectMilestone{
		ID:             uuid.New(),
		ProjectID:      projectID,
		Title:          req.Title,
		Description:    req.Description,
		Sequence:       req.Sequence,
		StartDate:      req.StartDate,
		EndDate:        req.EndDate,
		RequiredHours:  req.RequiredHours,
		Deliverables:   req.Deliverables,
		AssessmentType: req.AssessmentType,
		Status:         MilestoneStatusNotStarted,
	}

	if milestone.Sequence == 0 {
		// Get current max sequence
		milestones, _ := s.repo.GetMilestonesByProject(projectID)
		maxSeq := 0
		for _, m := range milestones {
			if m.Sequence > maxSeq {
				maxSeq = m.Sequence
			}
		}
		milestone.Sequence = maxSeq + 1
	}

	err = s.repo.CreateMilestone(ctx, milestone)
	if err != nil {
		return nil, err
	}

	return s.repo.GetMilestoneByID(milestone.ID)
}

func (s *service) GetMilestoneByID(id uuid.UUID) (*ProjectMilestone, error) {
	return s.repo.GetMilestoneByID(id)
}

func (s *service) GetMilestonesByProject(projectID uuid.UUID) ([]ProjectMilestone, error) {
	return s.repo.GetMilestonesByProject(projectID)
}

func (s *service) UpdateMilestone(ctx context.Context, id uuid.UUID, req UpdateMilestoneRequest) (*ProjectMilestone, error) {
	milestone, err := s.repo.GetMilestoneByID(id)
	if err != nil {
		return nil, err
	}

	if req.Title != "" {
		milestone.Title = req.Title
	}
	if req.Description != "" {
		milestone.Description = req.Description
	}
	if req.Sequence > 0 {
		milestone.Sequence = req.Sequence
	}
	if req.StartDate != "" {
		milestone.StartDate = req.StartDate
	}
	if req.EndDate != "" {
		milestone.EndDate = req.EndDate
	}
	if req.RequiredHours > 0 {
		milestone.RequiredHours = req.RequiredHours
	}
	if req.Deliverables != "" {
		milestone.Deliverables = req.Deliverables
	}
	if req.AssessmentType != "" {
		milestone.AssessmentType = req.AssessmentType
	}
	if req.Status != "" {
		milestone.Status = req.Status
	}
	if req.CompletionDate != nil {
		milestone.CompletionDate = req.CompletionDate
	}

	err = s.repo.UpdateMilestone(ctx, milestone)
	if err != nil {
		return nil, err
	}

	// Update project progress after milestone change
	_ = s.UpdateProjectProgress(ctx, milestone.ProjectID)

	return s.repo.GetMilestoneByID(id)
}

func (s *service) DeleteMilestone(ctx context.Context, id uuid.UUID) error {
	milestone, err := s.repo.GetMilestoneByID(id)
	if err != nil {
		return err
	}

	projectID := milestone.ProjectID
	err = s.repo.DeleteMilestone(ctx, milestone.ID)
	if err != nil {
		return err
	}

	// Update project progress
	return s.UpdateProjectProgress(ctx, projectID)
}

func (s *service) UpdateMilestoneProgress(ctx context.Context, projectID uuid.UUID) error {
	milestones, err := s.repo.GetMilestonesByProject(projectID)
	if err != nil {
		return err
	}

	for _, m := range milestones {
		// TODO: Check if end date has passed for in-progress milestones
		// This is a placeholder - in real implementation, check actual dates
		_ = m.Status
	}

	return s.UpdateProjectProgress(ctx, projectID)
}

// Participation operations
func (s *service) CreateParticipation(ctx context.Context, req CreateParticipationRequest) (*StudentParticipation, error) {
	_, err := s.repo.GetProjectByID(uuid.MustParse(req.ProjectID))
	if err != nil {
		return nil, fmt.Errorf("project not found: %w", err)
	}

	participation := &StudentParticipation{
		ID:              uuid.New(),
		ProjectID:       uuid.MustParse(req.ProjectID),
		StudentID:       uuid.MustParse(req.StudentID),
		Role:            req.Role,
		OverallProgress: req.OverallProgress,
		EngagementLevel: req.EngagementLevel,
		AttendanceRate:  req.AttendanceRate,
	}

	if req.TeamID != "" {
		teamID, err := uuid.Parse(req.TeamID)
		if err != nil {
			return nil, fmt.Errorf("invalid team_id: %w", err)
		}
		participation.TeamID = &teamID
	}

	if participation.Role == "" {
		participation.Role = RoleMember
	}

	if participation.EngagementLevel == "" {
		participation.EngagementLevel = "SEDANG"
	}

	err = s.repo.CreateParticipation(ctx, participation)
	if err != nil {
		return nil, err
	}

	return s.repo.GetParticipationByID(participation.ID)
}

func (s *service) GetParticipationByID(id uuid.UUID) (*StudentParticipation, error) {
	return s.repo.GetParticipationByID(id)
}

func (s *service) GetParticipationsByProject(projectID uuid.UUID) ([]StudentParticipation, error) {
	return s.repo.GetParticipationsByProject(projectID)
}

func (s *service) UpdateParticipation(ctx context.Context, id uuid.UUID, req UpdateParticipationRequest) (*StudentParticipation, error) {
	participation, err := s.repo.GetParticipationByID(id)
	if err != nil {
		return nil, err
	}

	if req.OverallProgress >= 0 {
		participation.OverallProgress = req.OverallProgress
	}
	if req.EngagementLevel != "" {
		participation.EngagementLevel = req.EngagementLevel
	}
	if req.AttendanceRate >= 0 {
		participation.AttendanceRate = req.AttendanceRate
	}
	if req.DimensionGrowth != "" {
		participation.DimensionGrowth = req.DimensionGrowth
	}
	if req.ChallengesFaced != "" {
		participation.ChallengesFaced = req.ChallengesFaced
	}
	if req.SupportNeeded != "" {
		participation.SupportNeeded = req.SupportNeeded
	}
	if req.FinalScore != nil {
		participation.FinalScore = req.FinalScore
	}
	if req.Grade != nil {
		participation.Grade = req.Grade
	}
	if req.TeacherFeedback != "" {
		participation.TeacherFeedback = req.TeacherFeedback
	}

	err = s.repo.UpdateParticipation(ctx, participation)
	if err != nil {
		return nil, err
	}

	return s.repo.GetParticipationByID(id)
}

func (s *service) DeleteParticipation(ctx context.Context, id uuid.UUID) error {
	return s.repo.DeleteParticipation(ctx, id)
}

func (s *service) RecordFinalAssessment(ctx context.Context, id uuid.UUID, finalScore float64, grade, teacherFeedback string) error {
	participation, err := s.repo.GetParticipationByID(id)
	if err != nil {
		return err
	}

	participation.FinalScore = &finalScore
	participation.Grade = &grade
	participation.TeacherFeedback = teacherFeedback
	participation.OverallProgress = 100

	return s.repo.UpdateParticipation(ctx, participation)
}

// Helper functions
func generateTeamCode() string {
	return fmt.Sprintf("TM%s", strings.ToUpper(uuid.New().String()[:8]))
}
