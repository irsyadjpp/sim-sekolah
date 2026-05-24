package learning_experience

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type LearningExperienceRepository interface {
	// Learning Experience CRUD
	CreateLearningExperience(ctx context.Context, exp *LearningExperience) error
	GetLearningExperienceByID(ctx context.Context, id uuid.UUID) (*LearningExperience, error)
	GetAllLearningExperiences(ctx context.Context) ([]LearningExperience, error)
	GetActiveLearningExperiences(ctx context.Context) ([]LearningExperience, error)
	UpdateLearningExperience(ctx context.Context, exp *LearningExperience) error
	DeleteLearningExperience(ctx context.Context, id uuid.UUID) error
	GetLearningExperienceByCode(ctx context.Context, code string) (*LearningExperience, error)

	// Activity Experience Mapping
	CreateActivityExperienceMapping(ctx context.Context, mapping *ActivityExperienceMapping) error
	DeleteActivityExperienceMapping(ctx context.Context, activityID uuid.UUID) error
	GetExperienceByActivityID(ctx context.Context, activityID uuid.UUID) (*LearningExperience, error)
	GetActivitiesByExperienceID(ctx context.Context, experienceID uuid.UUID) ([]uuid.UUID, error)

	// Student Experience Progression
	CreateStudentProgression(ctx context.Context, progression *StudentExperienceProgression) error
	GetStudentProgressionByID(ctx context.Context, id uuid.UUID) (*StudentExperienceProgression, error)
	UpdateStudentProgression(ctx context.Context, progression *StudentExperienceProgression) error
	DeleteStudentProgression(ctx context.Context, id uuid.UUID) error
	GetStudentProgressions(ctx context.Context, studentID uuid.UUID, subjectID uuid.UUID) ([]StudentExperienceProgression, error)
	GetStudentProgressionsBySubject(ctx context.Context, studentID uuid.UUID, subjectID uuid.UUID) ([]StudentExperienceProgression, error)
	GetAllStudentProgressions(ctx context.Context) ([]StudentExperienceProgression, error)
}

type learningExperienceRepository struct {
	db *gorm.DB
}

func NewLearningExperienceRepository(db *gorm.DB) LearningExperienceRepository {
	return &learningExperienceRepository{db: db}
}

// Learning Experience CRUD

func (r *learningExperienceRepository) CreateLearningExperience(ctx context.Context, exp *LearningExperience) error {
	return r.db.WithContext(ctx).Create(exp).Error
}

func (r *learningExperienceRepository) GetLearningExperienceByID(ctx context.Context, id uuid.UUID) (*LearningExperience, error) {
	var exp LearningExperience
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&exp).Error
	if err != nil {
		return nil, err
	}
	return &exp, nil
}

func (r *learningExperienceRepository) GetAllLearningExperiences(ctx context.Context) ([]LearningExperience, error) {
	var experiences []LearningExperience
	err := r.db.WithContext(ctx).Where("deleted_at IS NULL").Order("sequence_order").Find(&experiences).Error
	return experiences, err
}

func (r *learningExperienceRepository) GetActiveLearningExperiences(ctx context.Context) ([]LearningExperience, error) {
	var experiences []LearningExperience
	err := r.db.WithContext(ctx).Where("is_active = ? AND deleted_at IS NULL", true).Order("sequence_order").Find(&experiences).Error
	return experiences, err
}

func (r *learningExperienceRepository) UpdateLearningExperience(ctx context.Context, exp *LearningExperience) error {
	return r.db.WithContext(ctx).Model(&LearningExperience{}).Where("id = ?", exp.ID).Updates(exp).Error
}

func (r *learningExperienceRepository) DeleteLearningExperience(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Model(&LearningExperience{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *learningExperienceRepository) GetLearningExperienceByCode(ctx context.Context, code string) (*LearningExperience, error) {
	var exp LearningExperience
	err := r.db.WithContext(ctx).Where("experience_code = ? AND deleted_at IS NULL", code).First(&exp).Error
	if err != nil {
		return nil, err
	}
	return &exp, nil
}

// Activity Experience Mapping

func (r *learningExperienceRepository) CreateActivityExperienceMapping(ctx context.Context, mapping *ActivityExperienceMapping) error {
	return r.db.WithContext(ctx).Create(mapping).Error
}

func (r *learningExperienceRepository) DeleteActivityExperienceMapping(ctx context.Context, activityID uuid.UUID) error {
	return r.db.WithContext(ctx).Where("activity_id = ?", activityID).Delete(&ActivityExperienceMapping{}).Error
}

func (r *learningExperienceRepository) GetExperienceByActivityID(ctx context.Context, activityID uuid.UUID) (*LearningExperience, error) {
	var mapping ActivityExperienceMapping
	err := r.db.WithContext(ctx).Where("activity_id = ?", activityID).First(&mapping).Error
	if err != nil {
		return nil, err
	}

	var exp LearningExperience
	err = r.db.WithContext(ctx).Where("id = ?", mapping.ExperienceID).First(&exp).Error
	if err != nil {
		return nil, err
	}
	return &exp, nil
}

func (r *learningExperienceRepository) GetActivitiesByExperienceID(ctx context.Context, experienceID uuid.UUID) ([]uuid.UUID, error) {
	var mappings []ActivityExperienceMapping
	err := r.db.WithContext(ctx).Where("experience_id = ?", experienceID).Find(&mappings).Error
	if err != nil {
		return nil, err
	}

	activityIDs := make([]uuid.UUID, len(mappings))
	for i, mapping := range mappings {
		activityIDs[i] = mapping.ActivityID
	}
	return activityIDs, nil
}

// Student Experience Progression

func (r *learningExperienceRepository) CreateStudentProgression(ctx context.Context, progression *StudentExperienceProgression) error {
	return r.db.WithContext(ctx).Create(progression).Error
}

func (r *learningExperienceRepository) GetStudentProgressionByID(ctx context.Context, id uuid.UUID) (*StudentExperienceProgression, error) {
	var progression StudentExperienceProgression
	err := r.db.WithContext(ctx).Where("id = ?", id).First(&progression).Error
	if err != nil {
		return nil, err
	}
	return &progression, nil
}

func (r *learningExperienceRepository) UpdateStudentProgression(ctx context.Context, progression *StudentExperienceProgression) error {
	return r.db.WithContext(ctx).Model(&StudentExperienceProgression{}).Where("id = ?", progression.ID).Updates(progression).Error
}

func (r *learningExperienceRepository) DeleteStudentProgression(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&StudentExperienceProgression{}, "id = ?", id).Error
}

func (r *learningExperienceRepository) GetStudentProgressions(ctx context.Context, studentID uuid.UUID, subjectID uuid.UUID) ([]StudentExperienceProgression, error) {
	var progressions []StudentExperienceProgression
	query := r.db.WithContext(ctx).Where("student_id = ?", studentID)

	if subjectID != uuid.Nil {
		query = query.Where("subject_id = ?", subjectID)
	}

	err := query.Order("created_at").Find(&progressions).Error
	return progressions, err
}

func (r *learningExperienceRepository) GetStudentProgressionsBySubject(ctx context.Context, studentID uuid.UUID, subjectID uuid.UUID) ([]StudentExperienceProgression, error) {
	var progressions []StudentExperienceProgression
	err := r.db.WithContext(ctx).Where("student_id = ? AND subject_id = ?", studentID, subjectID).Order("created_at").Find(&progressions).Error
	return progressions, err
}

func (r *learningExperienceRepository) GetAllStudentProgressions(ctx context.Context) ([]StudentExperienceProgression, error) {
	var progressions []StudentExperienceProgression
	err := r.db.WithContext(ctx).Find(&progressions).Error
	return progressions, err
}
