package character_intervention

import (
	"context"

	"gorm.io/gorm"
)

type CharacterInterventionRepository interface {
	// CharacterIntervention
	GetAll(ctx context.Context) ([]CharacterIntervention, error)
	GetByID(ctx context.Context, id string) (*CharacterIntervention, error)
	GetByDimension(ctx context.Context, dimension string) ([]CharacterIntervention, error)
	GetByAgeGroup(ctx context.Context, ageGroup string) ([]CharacterIntervention, error)
	GetActive(ctx context.Context) ([]CharacterIntervention, error)
	Create(ctx context.Context, data *CharacterIntervention) error
	Update(ctx context.Context, data *CharacterIntervention) error
	Delete(ctx context.Context, id string) error

	// StudentCharacterIntervention
	GetAllStudentInterventions(ctx context.Context) ([]StudentCharacterIntervention, error)
	GetStudentInterventionByID(ctx context.Context, id string) (*StudentCharacterIntervention, error)
	GetStudentInterventionsByStudent(ctx context.Context, studentID string) ([]StudentCharacterIntervention, error)
	GetStudentInterventionsByTeacher(ctx context.Context, teacherID string) ([]StudentCharacterIntervention, error)
	GetActiveStudentInterventions(ctx context.Context) ([]StudentCharacterIntervention, error)
	GetStudentInterventionsByStatus(ctx context.Context, status string) ([]StudentCharacterIntervention, error)
	CreateStudentIntervention(ctx context.Context, data *StudentCharacterIntervention) error
	UpdateStudentIntervention(ctx context.Context, data *StudentCharacterIntervention) error
	DeleteStudentIntervention(ctx context.Context, id string) error

	// CharacterInterventionProgress
	GetAllProgress(ctx context.Context) ([]CharacterInterventionProgress, error)
	GetProgressByID(ctx context.Context, id string) (*CharacterInterventionProgress, error)
	GetProgressByAssignment(ctx context.Context, assignmentID string) ([]CharacterInterventionProgress, error)
	GetProgressByObserver(ctx context.Context, observerID string) ([]CharacterInterventionProgress, error)
	CreateProgress(ctx context.Context, data *CharacterInterventionProgress) error
	UpdateProgress(ctx context.Context, data *CharacterInterventionProgress) error
	DeleteProgress(ctx context.Context, id string) error

	// InterventionRecommendation
	GetAllRecommendations(ctx context.Context) ([]InterventionRecommendation, error)
	GetRecommendationByID(ctx context.Context, id string) (*InterventionRecommendation, error)
	GetRecommendationsByStudent(ctx context.Context, studentID string) ([]InterventionRecommendation, error)
	GetPendingRecommendations(ctx context.Context) ([]InterventionRecommendation, error)
	CreateRecommendation(ctx context.Context, data *InterventionRecommendation) error
	UpdateRecommendation(ctx context.Context, data *InterventionRecommendation) error
	DeleteRecommendation(ctx context.Context, id string) error

	// CharacterMilestone
	GetAllMilestones(ctx context.Context) ([]CharacterMilestone, error)
	GetMilestoneByID(ctx context.Context, id string) (*CharacterMilestone, error)
	GetMilestonesByStudent(ctx context.Context, studentID string) ([]CharacterMilestone, error)
	GetMilestonesByDimension(ctx context.Context, dimension string) ([]CharacterMilestone, error)
	GetMilestonesByObserver(ctx context.Context, observerID string) ([]CharacterMilestone, error)
	CreateMilestone(ctx context.Context, data *CharacterMilestone) error
	UpdateMilestone(ctx context.Context, data *CharacterMilestone) error
	DeleteMilestone(ctx context.Context, id string) error

	// Summary
	GetInterventionSummary(ctx context.Context) (*InterventionSummaryResponse, error)
}

type characterInterventionRepository struct {
	db *gorm.DB
}

func NewCharacterInterventionRepository(db *gorm.DB) CharacterInterventionRepository {
	return &characterInterventionRepository{db: db}
}

// CharacterIntervention Methods
func (r *characterInterventionRepository) GetAll(ctx context.Context) ([]CharacterIntervention, error) {
	var interventions []CharacterIntervention
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("character_dimension, intervention_name ASC").
		Find(&interventions).Error
	return interventions, err
}

func (r *characterInterventionRepository) GetByID(ctx context.Context, id string) (*CharacterIntervention, error) {
	var intervention CharacterIntervention
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&intervention).Error
	if err != nil {
		return nil, err
	}
	return &intervention, nil
}

func (r *characterInterventionRepository) GetByDimension(ctx context.Context, dimension string) ([]CharacterIntervention, error) {
	var interventions []CharacterIntervention
	err := r.db.WithContext(ctx).
		Where("character_dimension = ? AND is_active = true AND deleted_at IS NULL", dimension).
		Order("intervention_name ASC").
		Find(&interventions).Error
	return interventions, err
}

func (r *characterInterventionRepository) GetByAgeGroup(ctx context.Context, ageGroup string) ([]CharacterIntervention, error) {
	var interventions []CharacterIntervention
	err := r.db.WithContext(ctx).
		Where("target_age_group = ? AND is_active = true AND deleted_at IS NULL", ageGroup).
		Order("character_dimension, intervention_name ASC").
		Find(&interventions).Error
	return interventions, err
}

func (r *characterInterventionRepository) GetActive(ctx context.Context) ([]CharacterIntervention, error) {
	var interventions []CharacterIntervention
	err := r.db.WithContext(ctx).
		Where("is_active = true AND deleted_at IS NULL").
		Order("character_dimension, intervention_name ASC").
		Find(&interventions).Error
	return interventions, err
}

func (r *characterInterventionRepository) Create(ctx context.Context, data *CharacterIntervention) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *characterInterventionRepository) Update(ctx context.Context, data *CharacterIntervention) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *characterInterventionRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&CharacterIntervention{}).Error
}

// StudentCharacterIntervention Methods
func (r *characterInterventionRepository) GetAllStudentInterventions(ctx context.Context) ([]StudentCharacterIntervention, error) {
	var assignments []StudentCharacterIntervention
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("assignment_date DESC").
		Find(&assignments).Error
	return assignments, err
}

func (r *characterInterventionRepository) GetStudentInterventionByID(ctx context.Context, id string) (*StudentCharacterIntervention, error) {
	var assignment StudentCharacterIntervention
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&assignment).Error
	if err != nil {
		return nil, err
	}
	return &assignment, nil
}

func (r *characterInterventionRepository) GetStudentInterventionsByStudent(ctx context.Context, studentID string) ([]StudentCharacterIntervention, error) {
	var assignments []StudentCharacterIntervention
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND deleted_at IS NULL", studentID).
		Order("assignment_date DESC").
		Find(&assignments).Error
	return assignments, err
}

func (r *characterInterventionRepository) GetStudentInterventionsByTeacher(ctx context.Context, teacherID string) ([]StudentCharacterIntervention, error) {
	var assignments []StudentCharacterIntervention
	err := r.db.WithContext(ctx).
		Where("teacher_id = ? AND deleted_at IS NULL", teacherID).
		Order("assignment_date DESC").
		Find(&assignments).Error
	return assignments, err
}

func (r *characterInterventionRepository) GetActiveStudentInterventions(ctx context.Context) ([]StudentCharacterIntervention, error) {
	var assignments []StudentCharacterIntervention
	err := r.db.WithContext(ctx).
		Where("current_status = ? AND deleted_at IS NULL", AssignmentStatusActive).
		Order("priority_level DESC, assignment_date ASC").
		Find(&assignments).Error
	return assignments, err
}

func (r *characterInterventionRepository) GetStudentInterventionsByStatus(ctx context.Context, status string) ([]StudentCharacterIntervention, error) {
	var assignments []StudentCharacterIntervention
	err := r.db.WithContext(ctx).
		Where("current_status = ? AND deleted_at IS NULL", status).
		Order("assignment_date DESC").
		Find(&assignments).Error
	return assignments, err
}

func (r *characterInterventionRepository) CreateStudentIntervention(ctx context.Context, data *StudentCharacterIntervention) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *characterInterventionRepository) UpdateStudentIntervention(ctx context.Context, data *StudentCharacterIntervention) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *characterInterventionRepository) DeleteStudentIntervention(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&StudentCharacterIntervention{}).Error
}

// CharacterInterventionProgress Methods
func (r *characterInterventionRepository) GetAllProgress(ctx context.Context) ([]CharacterInterventionProgress, error) {
	var progress []CharacterInterventionProgress
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("observation_date DESC").
		Find(&progress).Error
	return progress, err
}

func (r *characterInterventionRepository) GetProgressByID(ctx context.Context, id string) (*CharacterInterventionProgress, error) {
	var p CharacterInterventionProgress
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&p).Error
	if err != nil {
		return nil, err
	}
	return &p, nil
}

func (r *characterInterventionRepository) GetProgressByAssignment(ctx context.Context, assignmentID string) ([]CharacterInterventionProgress, error) {
	var progress []CharacterInterventionProgress
	err := r.db.WithContext(ctx).
		Where("assignment_id = ? AND deleted_at IS NULL", assignmentID).
		Order("observation_date ASC").
		Find(&progress).Error
	return progress, err
}

func (r *characterInterventionRepository) GetProgressByObserver(ctx context.Context, observerID string) ([]CharacterInterventionProgress, error) {
	var progress []CharacterInterventionProgress
	err := r.db.WithContext(ctx).
		Where("observer_id = ? AND deleted_at IS NULL", observerID).
		Order("observation_date DESC").
		Find(&progress).Error
	return progress, err
}

func (r *characterInterventionRepository) CreateProgress(ctx context.Context, data *CharacterInterventionProgress) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *characterInterventionRepository) UpdateProgress(ctx context.Context, data *CharacterInterventionProgress) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *characterInterventionRepository) DeleteProgress(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&CharacterInterventionProgress{}).Error
}

// InterventionRecommendation Methods
func (r *characterInterventionRepository) GetAllRecommendations(ctx context.Context) ([]InterventionRecommendation, error) {
	var recommendations []InterventionRecommendation
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("recommendation_date DESC").
		Find(&recommendations).Error
	return recommendations, err
}

func (r *characterInterventionRepository) GetRecommendationByID(ctx context.Context, id string) (*InterventionRecommendation, error) {
	var recommendation InterventionRecommendation
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&recommendation).Error
	if err != nil {
		return nil, err
	}
	return &recommendation, nil
}

func (r *characterInterventionRepository) GetRecommendationsByStudent(ctx context.Context, studentID string) ([]InterventionRecommendation, error) {
	var recommendations []InterventionRecommendation
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND deleted_at IS NULL", studentID).
		Order("recommendation_date DESC").
		Find(&recommendations).Error
	return recommendations, err
}

func (r *characterInterventionRepository) GetPendingRecommendations(ctx context.Context) ([]InterventionRecommendation, error) {
	var recommendations []InterventionRecommendation
	err := r.db.WithContext(ctx).
		Where("is_accepted IS NULL AND deleted_at IS NULL").
		Order("recommendation_date ASC").
		Find(&recommendations).Error
	return recommendations, err
}

func (r *characterInterventionRepository) CreateRecommendation(ctx context.Context, data *InterventionRecommendation) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *characterInterventionRepository) UpdateRecommendation(ctx context.Context, data *InterventionRecommendation) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *characterInterventionRepository) DeleteRecommendation(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&InterventionRecommendation{}).Error
}

// CharacterMilestone Methods
func (r *characterInterventionRepository) GetAllMilestones(ctx context.Context) ([]CharacterMilestone, error) {
	var milestones []CharacterMilestone
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("milestone_date DESC").
		Find(&milestones).Error
	return milestones, err
}

func (r *characterInterventionRepository) GetMilestoneByID(ctx context.Context, id string) (*CharacterMilestone, error) {
	var milestone CharacterMilestone
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&milestone).Error
	if err != nil {
		return nil, err
	}
	return &milestone, nil
}

func (r *characterInterventionRepository) GetMilestonesByStudent(ctx context.Context, studentID string) ([]CharacterMilestone, error) {
	var milestones []CharacterMilestone
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND deleted_at IS NULL", studentID).
		Order("milestone_date DESC").
		Find(&milestones).Error
	return milestones, err
}

func (r *characterInterventionRepository) GetMilestonesByDimension(ctx context.Context, dimension string) ([]CharacterMilestone, error) {
	var milestones []CharacterMilestone
	err := r.db.WithContext(ctx).
		Where("character_dimension = ? AND deleted_at IS NULL", dimension).
		Order("milestone_date DESC").
		Find(&milestones).Error
	return milestones, err
}

func (r *characterInterventionRepository) GetMilestonesByObserver(ctx context.Context, observerID string) ([]CharacterMilestone, error) {
	var milestones []CharacterMilestone
	err := r.db.WithContext(ctx).
		Where("observer_id = ? AND deleted_at IS NULL", observerID).
		Order("milestone_date DESC").
		Find(&milestones).Error
	return milestones, err
}

func (r *characterInterventionRepository) CreateMilestone(ctx context.Context, data *CharacterMilestone) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *characterInterventionRepository) UpdateMilestone(ctx context.Context, data *CharacterMilestone) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *characterInterventionRepository) DeleteMilestone(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&CharacterMilestone{}).Error
}

// Summary Method
func (r *characterInterventionRepository) GetInterventionSummary(ctx context.Context) (*InterventionSummaryResponse, error) {
	var totalInterventions int64
	r.db.WithContext(ctx).Model(&CharacterIntervention{}).Count(&totalInterventions)

	var activeInterventions int64
	r.db.WithContext(ctx).Model(&CharacterIntervention{}).Where("is_active = true").Count(&activeInterventions)

	var completedInterventions int64
	r.db.WithContext(ctx).Model(&StudentCharacterIntervention{}).Where("current_status = ?", AssignmentStatusCompleted).Count(&completedInterventions)

	var totalStudentAssignments int64
	r.db.WithContext(ctx).Model(&StudentCharacterIntervention{}).Count(&totalStudentAssignments)

	var activeStudentAssignments int64
	r.db.WithContext(ctx).Model(&StudentCharacterIntervention{}).Where("current_status = ?", AssignmentStatusActive).Count(&activeStudentAssignments)

	var totalProgressRecords int64
	r.db.WithContext(ctx).Model(&CharacterInterventionProgress{}).Count(&totalProgressRecords)

	var totalMilestones int64
	r.db.WithContext(ctx).Model(&CharacterMilestone{}).Count(&totalMilestones)

	var totalRecommendations int64
	r.db.WithContext(ctx).Model(&InterventionRecommendation{}).Count(&totalRecommendations)

	var pendingRecommendations int64
	r.db.WithContext(ctx).Model(&InterventionRecommendation{}).Where("is_accepted IS NULL").Count(&pendingRecommendations)

	return &InterventionSummaryResponse{
		TotalInterventions:       int(totalInterventions),
		ActiveInterventions:      int(activeInterventions),
		CompletedInterventions:   int(completedInterventions),
		TotalStudentAssignments:  int(totalStudentAssignments),
		ActiveStudentAssignments: int(activeStudentAssignments),
		TotalProgressRecords:     int(totalProgressRecords),
		TotalMilestones:          int(totalMilestones),
		TotalRecommendations:     int(totalRecommendations),
		PendingRecommendations:   int(pendingRecommendations),
	}, nil
}
