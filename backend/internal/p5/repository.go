package p5

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Repository interface {
	// Project operations
	CreateProject(ctx context.Context, project *Project) error
	GetProjectByID(id uuid.UUID) (*Project, error)
	GetProjects(filter map[string]interface{}) ([]Project, error)
	UpdateProject(ctx context.Context, project *Project) error
	DeleteProject(ctx context.Context, id uuid.UUID) error

	// Team operations
	CreateTeam(ctx context.Context, team *ProjectTeam) error
	GetTeamByID(id uuid.UUID) (*ProjectTeam, error)
	GetTeamsByProject(projectID uuid.UUID) ([]ProjectTeam, error)
	UpdateTeam(ctx context.Context, team *ProjectTeam) error
	DeleteTeam(ctx context.Context, id uuid.UUID) error

	// Team Member operations
	CreateTeamMember(ctx context.Context, member *TeamMember) error
	GetTeamMemberByID(id uuid.UUID) (*TeamMember, error)
	GetTeamMembers(teamID uuid.UUID) ([]TeamMember, error)
	UpdateTeamMember(ctx context.Context, member *TeamMember) error
	DeleteTeamMember(ctx context.Context, id uuid.UUID) error

	// Milestone operations
	CreateMilestone(ctx context.Context, milestone *ProjectMilestone) error
	GetMilestoneByID(id uuid.UUID) (*ProjectMilestone, error)
	GetMilestonesByProject(projectID uuid.UUID) ([]ProjectMilestone, error)
	UpdateMilestone(ctx context.Context, milestone *ProjectMilestone) error
	DeleteMilestone(ctx context.Context, id uuid.UUID) error

	// Participation operations
	CreateParticipation(ctx context.Context, participation *StudentParticipation) error
	GetParticipationByID(id uuid.UUID) (*StudentParticipation, error)
	GetParticipationsByProject(projectID uuid.UUID) ([]StudentParticipation, error)
	GetParticipationsByStudent(studentID uuid.UUID) ([]StudentParticipation, error)
	UpdateParticipation(ctx context.Context, participation *StudentParticipation) error
	DeleteParticipation(ctx context.Context, id uuid.UUID) error
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

// Project operations
func (r *repository) CreateProject(ctx context.Context, project *Project) error {
	return r.db.WithContext(ctx).Create(project).Error
}

func (r *repository) GetProjectByID(id uuid.UUID) (*Project, error) {
	var project Project
	err := r.db.Preload("Subject").Preload("Teams.Members").Preload("Milestones").Preload("Participations").
		Where("id = ? AND deleted_at IS NULL", id).First(&project).Error
	if err != nil {
		return nil, err
	}
	return &project, nil
}

func (r *repository) GetProjects(filter map[string]interface{}) ([]Project, error) {
	var projects []Project
	query := r.db.Where("deleted_at IS NULL")

	if subjectID, ok := filter["subject_id"].(string); ok && subjectID != "" {
		query = query.Where("subject_id = ?", subjectID)
	}
	if classroomID, ok := filter["classroom_id"].(string); ok && classroomID != "" {
		query = query.Where("classroom_id = ?", classroomID)
	}
	if status, ok := filter["status"].(string); ok && status != "" {
		query = query.Where("status = ?", status)
	}
	if academicYearID, ok := filter["academic_year_id"].(string); ok && academicYearID != "" {
		query = query.Where("academic_year_id = ?", academicYearID)
	}
	if semester, ok := filter["semester"].(int); ok && semester > 0 {
		query = query.Where("semester = ?", semester)
	}

	err := query.Preload("Subject").Preload("Teams").Preload("Milestones").Preload("Participations").
		Order("created_at DESC").Find(&projects).Error
	return projects, err
}

func (r *repository) UpdateProject(ctx context.Context, project *Project) error {
	return r.db.WithContext(ctx).Save(project).Error
}

func (r *repository) DeleteProject(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&Project{}).Error
}

// Team operations
func (r *repository) CreateTeam(ctx context.Context, team *ProjectTeam) error {
	return r.db.WithContext(ctx).Create(team).Error
}

func (r *repository) GetTeamByID(id uuid.UUID) (*ProjectTeam, error) {
	var team ProjectTeam
	err := r.db.Preload("Project").Preload("Members").Where("id = ?", id).First(&team).Error
	if err != nil {
		return nil, err
	}
	return &team, nil
}

func (r *repository) GetTeamsByProject(projectID uuid.UUID) ([]ProjectTeam, error) {
	var teams []ProjectTeam
	err := r.db.Preload("Members").Where("project_id = ?", projectID).Order("created_at ASC").Find(&teams).Error
	return teams, err
}

func (r *repository) UpdateTeam(ctx context.Context, team *ProjectTeam) error {
	return r.db.WithContext(ctx).Save(team).Error
}

func (r *repository) DeleteTeam(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&ProjectTeam{}).Error
}

// Team Member operations
func (r *repository) CreateTeamMember(ctx context.Context, member *TeamMember) error {
	return r.db.WithContext(ctx).Create(member).Error
}

func (r *repository) GetTeamMemberByID(id uuid.UUID) (*TeamMember, error) {
	var member TeamMember
	err := r.db.Where("id = ?", id).First(&member).Error
	if err != nil {
		return nil, err
	}
	return &member, nil
}

func (r *repository) GetTeamMembers(teamID uuid.UUID) ([]TeamMember, error) {
	var members []TeamMember
	err := r.db.Where("team_id = ?", teamID).Find(&members).Error
	return members, err
}

func (r *repository) UpdateTeamMember(ctx context.Context, member *TeamMember) error {
	return r.db.WithContext(ctx).Save(member).Error
}

func (r *repository) DeleteTeamMember(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&TeamMember{}).Error
}

// Milestone operations
func (r *repository) CreateMilestone(ctx context.Context, milestone *ProjectMilestone) error {
	return r.db.WithContext(ctx).Create(milestone).Error
}

func (r *repository) GetMilestoneByID(id uuid.UUID) (*ProjectMilestone, error) {
	var milestone ProjectMilestone
	err := r.db.Preload("Project").Where("id = ?", id).First(&milestone).Error
	if err != nil {
		return nil, err
	}
	return &milestone, nil
}

func (r *repository) GetMilestonesByProject(projectID uuid.UUID) ([]ProjectMilestone, error) {
	var milestones []ProjectMilestone
	err := r.db.Where("project_id = ?", projectID).Order("sequence ASC").Find(&milestones).Error
	return milestones, err
}

func (r *repository) UpdateMilestone(ctx context.Context, milestone *ProjectMilestone) error {
	return r.db.WithContext(ctx).Save(milestone).Error
}

func (r *repository) DeleteMilestone(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&ProjectMilestone{}).Error
}

// Participation operations
func (r *repository) CreateParticipation(ctx context.Context, participation *StudentParticipation) error {
	return r.db.WithContext(ctx).Create(participation).Error
}

func (r *repository) GetParticipationByID(id uuid.UUID) (*StudentParticipation, error) {
	var participation StudentParticipation
	err := r.db.Preload("Project").Where("id = ?", id).First(&participation).Error
	if err != nil {
		return nil, err
	}
	return &participation, nil
}

func (r *repository) GetParticipationsByProject(projectID uuid.UUID) ([]StudentParticipation, error) {
	var participations []StudentParticipation
	err := r.db.Preload("Project").Where("project_id = ?", projectID).Find(&participations).Error
	return participations, err
}

func (r *repository) GetParticipationsByStudent(studentID uuid.UUID) ([]StudentParticipation, error) {
	var participations []StudentParticipation
	err := r.db.Preload("Project").Where("student_id = ?", studentID).Find(&participations).Error
	return participations, err
}

func (r *repository) UpdateParticipation(ctx context.Context, participation *StudentParticipation) error {
	return r.db.WithContext(ctx).Save(participation).Error
}

func (r *repository) DeleteParticipation(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&StudentParticipation{}).Error
}
