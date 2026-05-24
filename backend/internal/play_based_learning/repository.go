package play_based_learning

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type PlayBasedLearningRepository interface {
	// Play Activity Type CRUD
	CreatePlayActivityType(ctx context.Context, activityType *PlayActivityType) error
	GetPlayActivityTypeByID(ctx context.Context, id uuid.UUID) (*PlayActivityType, error)
	GetAllPlayActivityTypes(ctx context.Context) ([]PlayActivityType, error)
	GetActivePlayActivityTypes(ctx context.Context) ([]PlayActivityType, error)
	GetPlayActivityTypesByPhase(ctx context.Context, phaseID uuid.UUID) ([]PlayActivityType, error)
	GetPlayActivityTypesByDomain(ctx context.Context, domain string) ([]PlayActivityType, error)
	UpdatePlayActivityType(ctx context.Context, activityType *PlayActivityType) error
	DeletePlayActivityType(ctx context.Context, id uuid.UUID) error
	GetPlayActivityTypeByCode(ctx context.Context, code string) (*PlayActivityType, error)

	// Play Based Activity CRUD
	CreatePlayBasedActivity(ctx context.Context, activity *PlayBasedActivity) error
	GetPlayBasedActivityByID(ctx context.Context, id uuid.UUID) (*PlayBasedActivity, error)
	GetPlayBasedActivitiesByModuleID(ctx context.Context, moduleID uuid.UUID) ([]PlayBasedActivity, error)
	UpdatePlayBasedActivity(ctx context.Context, activity *PlayBasedActivity) error
	DeletePlayBasedActivity(ctx context.Context, id uuid.UUID) error
	DeletePlayBasedActivitiesByModuleID(ctx context.Context, moduleID uuid.UUID) error

	// Play Observation CRUD
	CreatePlayObservation(ctx context.Context, observation *PlayObservation) error
	GetPlayObservationByID(ctx context.Context, id uuid.UUID) (*PlayObservation, error)
	GetPlayObservationsByActivityID(ctx context.Context, activityID uuid.UUID) ([]PlayObservation, error)
	GetPlayObservationsByStudentID(ctx context.Context, studentID uuid.UUID) ([]PlayObservation, error)
	GetPlayObservationsByStudentAndActivity(ctx context.Context, studentID, activityID uuid.UUID) ([]PlayObservation, error)
	UpdatePlayObservation(ctx context.Context, observation *PlayObservation) error
	DeletePlayObservation(ctx context.Context, id uuid.UUID) error
	GetAllPlayObservations(ctx context.Context) ([]PlayObservation, error)
}

type playBasedLearningRepository struct {
	db *gorm.DB
}

func NewPlayBasedLearningRepository(db *gorm.DB) PlayBasedLearningRepository {
	return &playBasedLearningRepository{db: db}
}

// Play Activity Type CRUD

func (r *playBasedLearningRepository) CreatePlayActivityType(ctx context.Context, activityType *PlayActivityType) error {
	return r.db.WithContext(ctx).Create(activityType).Error
}

func (r *playBasedLearningRepository) GetPlayActivityTypeByID(ctx context.Context, id uuid.UUID) (*PlayActivityType, error) {
	var activityType PlayActivityType
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&activityType).Error
	if err != nil {
		return nil, err
	}
	return &activityType, nil
}

func (r *playBasedLearningRepository) GetAllPlayActivityTypes(ctx context.Context) ([]PlayActivityType, error) {
	var activityTypes []PlayActivityType
	err := r.db.WithContext(ctx).Where("deleted_at IS NULL").Order("activity_code").Find(&activityTypes).Error
	return activityTypes, err
}

func (r *playBasedLearningRepository) GetActivePlayActivityTypes(ctx context.Context) ([]PlayActivityType, error) {
	var activityTypes []PlayActivityType
	err := r.db.WithContext(ctx).Where("is_active = ? AND deleted_at IS NULL", true).Order("activity_code").Find(&activityTypes).Error
	return activityTypes, err
}

func (r *playBasedLearningRepository) GetPlayActivityTypesByPhase(ctx context.Context, phaseID uuid.UUID) ([]PlayActivityType, error) {
	var activityTypes []PlayActivityType
	err := r.db.WithContext(ctx).Where("phase_id = ? AND is_active = ? AND deleted_at IS NULL", phaseID, true).Order("activity_code").Find(&activityTypes).Error
	return activityTypes, err
}

func (r *playBasedLearningRepository) GetPlayActivityTypesByDomain(ctx context.Context, domain string) ([]PlayActivityType, error) {
	var activityTypes []PlayActivityType
	err := r.db.WithContext(ctx).Where("play_domain = ? AND is_active = ? AND deleted_at IS NULL", domain, true).Order("activity_code").Find(&activityTypes).Error
	return activityTypes, err
}

func (r *playBasedLearningRepository) UpdatePlayActivityType(ctx context.Context, activityType *PlayActivityType) error {
	return r.db.WithContext(ctx).Model(&PlayActivityType{}).Where("id = ?", activityType.ID).Updates(activityType).Error
}

func (r *playBasedLearningRepository) DeletePlayActivityType(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Model(&PlayActivityType{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *playBasedLearningRepository) GetPlayActivityTypeByCode(ctx context.Context, code string) (*PlayActivityType, error) {
	var activityType PlayActivityType
	err := r.db.WithContext(ctx).Where("activity_code = ? AND deleted_at IS NULL", code).First(&activityType).Error
	if err != nil {
		return nil, err
	}
	return &activityType, nil
}

// Play Based Activity CRUD

func (r *playBasedLearningRepository) CreatePlayBasedActivity(ctx context.Context, activity *PlayBasedActivity) error {
	return r.db.WithContext(ctx).Preload("ActivityType").Create(activity).Error
}

func (r *playBasedLearningRepository) GetPlayBasedActivityByID(ctx context.Context, id uuid.UUID) (*PlayBasedActivity, error) {
	var activity PlayBasedActivity
	err := r.db.WithContext(ctx).Preload("ActivityType").Where("id = ?", id).First(&activity).Error
	if err != nil {
		return nil, err
	}
	return &activity, nil
}

func (r *playBasedLearningRepository) GetPlayBasedActivitiesByModuleID(ctx context.Context, moduleID uuid.UUID) ([]PlayBasedActivity, error) {
	var activities []PlayBasedActivity
	err := r.db.WithContext(ctx).Preload("ActivityType").Where("module_id = ?", moduleID).Order("created_at").Find(&activities).Error
	return activities, err
}

func (r *playBasedLearningRepository) UpdatePlayBasedActivity(ctx context.Context, activity *PlayBasedActivity) error {
	return r.db.WithContext(ctx).Model(&PlayBasedActivity{}).Where("id = ?", activity.ID).Updates(activity).Error
}

func (r *playBasedLearningRepository) DeletePlayBasedActivity(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&PlayBasedActivity{}, "id = ?", id).Error
}

func (r *playBasedLearningRepository) DeletePlayBasedActivitiesByModuleID(ctx context.Context, moduleID uuid.UUID) error {
	return r.db.WithContext(ctx).Where("module_id = ?", moduleID).Delete(&PlayBasedActivity{}).Error
}

// Play Observation CRUD

func (r *playBasedLearningRepository) CreatePlayObservation(ctx context.Context, observation *PlayObservation) error {
	return r.db.WithContext(ctx).Create(observation).Error
}

func (r *playBasedLearningRepository) GetPlayObservationByID(ctx context.Context, id uuid.UUID) (*PlayObservation, error) {
	var observation PlayObservation
	err := r.db.WithContext(ctx).Where("id = ?", id).First(&observation).Error
	if err != nil {
		return nil, err
	}
	return &observation, nil
}

func (r *playBasedLearningRepository) GetPlayObservationsByActivityID(ctx context.Context, activityID uuid.UUID) ([]PlayObservation, error) {
	var observations []PlayObservation
	err := r.db.WithContext(ctx).Where("activity_id = ?", activityID).Order("observation_date DESC").Find(&observations).Error
	return observations, err
}

func (r *playBasedLearningRepository) GetPlayObservationsByStudentID(ctx context.Context, studentID uuid.UUID) ([]PlayObservation, error) {
	var observations []PlayObservation
	err := r.db.WithContext(ctx).Where("student_id = ?", studentID).Order("observation_date DESC").Find(&observations).Error
	return observations, err
}

func (r *playBasedLearningRepository) GetPlayObservationsByStudentAndActivity(ctx context.Context, studentID, activityID uuid.UUID) ([]PlayObservation, error) {
	var observations []PlayObservation
	err := r.db.WithContext(ctx).Where("student_id = ? AND activity_id = ?", studentID, activityID).Order("observation_date DESC").Find(&observations).Error
	return observations, err
}

func (r *playBasedLearningRepository) UpdatePlayObservation(ctx context.Context, observation *PlayObservation) error {
	return r.db.WithContext(ctx).Model(&PlayObservation{}).Where("id = ?", observation.ID).Updates(observation).Error
}

func (r *playBasedLearningRepository) DeletePlayObservation(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&PlayObservation{}, "id = ?", id).Error
}

func (r *playBasedLearningRepository) GetAllPlayObservations(ctx context.Context) ([]PlayObservation, error) {
	var observations []PlayObservation
	err := r.db.WithContext(ctx).Find(&observations).Error
	return observations, err
}
