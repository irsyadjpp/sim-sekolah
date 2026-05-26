package rubric

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Repository interface {
	// Rubric operations
	CreateRubric(ctx context.Context, rubric *Rubric) error
	GetRubricByID(id uuid.UUID) (*Rubric, error)
	GetRubrics(filter map[string]interface{}) ([]Rubric, error)
	UpdateRubric(ctx context.Context, rubric *Rubric) error
	DeleteRubric(ctx context.Context, id uuid.UUID) error
	GetRubricTemplates(assessmentType string) ([]Rubric, error)
	CopyRubric(ctx context.Context, originalID uuid.UUID, newTitle string) (*Rubric, error)

	// RubricCriteria operations
	CreateCriteria(ctx context.Context, criteria *RubricCriteria) error
	GetCriteriaByID(id uuid.UUID) (*RubricCriteria, error)
	GetCriteriaByRubric(rubricID uuid.UUID) ([]RubricCriteria, error)
	UpdateCriteria(ctx context.Context, criteria *RubricCriteria) error
	DeleteCriteria(ctx context.Context, id uuid.UUID) error

	// RubricLevel operations
	CreateLevel(ctx context.Context, level *RubricLevel) error
	GetLevelByID(id uuid.UUID) (*RubricLevel, error)
	GetLevelsByRubric(rubricID uuid.UUID) ([]RubricLevel, error)
	UpdateLevel(ctx context.Context, level *RubricLevel) error
	DeleteLevel(ctx context.Context, id uuid.UUID) error

	// RubricCriteriaLevel operations
	CreateCriteriaLevel(ctx context.Context, criteriaLevel *RubricCriteriaLevel) error
	GetCriteriaLevels(criteriaID uuid.UUID) ([]RubricCriteriaLevel, error)
	UpdateCriteriaLevel(ctx context.Context, criteriaLevel *RubricCriteriaLevel) error
	DeleteCriteriaLevel(ctx context.Context, id uuid.UUID) error
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

// Rubric operations
func (r *repository) CreateRubric(ctx context.Context, rubric *Rubric) error {
	return r.db.WithContext(ctx).Create(rubric).Error
}

func (r *repository) GetRubricByID(id uuid.UUID) (*Rubric, error) {
	var rubric Rubric
	err := r.db.Preload("Criteria.Levels").Preload("Levels").Where("id = ? AND deleted_at IS NULL", id).First(&rubric).Error
	if err != nil {
		return nil, err
	}
	return &rubric, nil
}

func (r *repository) GetRubrics(filter map[string]interface{}) ([]Rubric, error) {
	var rubrics []Rubric
	query := r.db.Where("deleted_at IS NULL")

	if assessmentType, ok := filter["assessment_type"].(string); ok && assessmentType != "" {
		query = query.Where("assessment_type = ?", assessmentType)
	}
	if subjectID, ok := filter["subject_id"].(string); ok && subjectID != "" {
		query = query.Where("subject_id = ?", subjectID)
	}
	if gradeLevel, ok := filter["grade_level"].(string); ok && gradeLevel != "" {
		query = query.Where("grade_level = ? OR grade_level = ?", gradeLevel, GradeAll)
	}
	if isTemplate, ok := filter["is_template"].(bool); ok {
		query = query.Where("is_template = ?", isTemplate)
	}
	if isActive, ok := filter["is_active"].(bool); ok {
		query = query.Where("is_active = ?", isActive)
	}

	err := query.Preload("Criteria").Preload("Levels").Order("created_at DESC").Find(&rubrics).Error
	return rubrics, err
}

func (r *repository) UpdateRubric(ctx context.Context, rubric *Rubric) error {
	return r.db.WithContext(ctx).Save(rubric).Error
}

func (r *repository) DeleteRubric(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&Rubric{}).Error
}

func (r *repository) GetRubricTemplates(assessmentType string) ([]Rubric, error) {
	var rubrics []Rubric
	query := r.db.Where("is_template = ? AND is_active = ? AND deleted_at IS NULL", true, true)

	if assessmentType != "" {
		query = query.Where("assessment_type = ?", assessmentType)
	}

	err := query.Preload("Criteria").Preload("Levels").Order("created_at DESC").Find(&rubrics).Error
	return rubrics, err
}

func (r *repository) CopyRubric(ctx context.Context, originalID uuid.UUID, newTitle string) (*Rubric, error) {
	var original Rubric
	err := r.db.Preload("Criteria.Levels").Preload("Levels").Where("id = ?", originalID).First(&original).Error
	if err != nil {
		return nil, err
	}

	// Create new rubric
	newRubric := &Rubric{
		ID:             uuid.New(),
		Title:          newTitle,
		Description:    original.Description,
		SubjectID:      original.SubjectID,
		AssessmentType: original.AssessmentType,
		GradeLevel:     original.GradeLevel,
		MaxScore:       original.MaxScore,
		IsTemplate:     false, // Copy is not a template
		IsActive:       true,
	}

	err = r.db.WithContext(ctx).Create(newRubric).Error
	if err != nil {
		return nil, err
	}

	// Copy levels
	levelMapping := make(map[uuid.UUID]uuid.UUID)
	for _, level := range original.Levels {
		newLevel := &RubricLevel{
			ID:            uuid.New(),
			RubricID:      newRubric.ID,
			LevelCode:     level.LevelCode,
			LevelName:     level.LevelName,
			PointValue:    level.PointValue,
			MinPercentage: level.MinPercentage,
			MaxPercentage: level.MaxPercentage,
			Sequence:      level.Sequence,
			Color:         level.Color,
		}
		err = r.db.WithContext(ctx).Create(newLevel).Error
		if err != nil {
			return nil, err
		}
		levelMapping[level.ID] = newLevel.ID
	}

	// Copy criteria with their level descriptions
	for _, criteria := range original.Criteria {
		newCriteria := &RubricCriteria{
			ID:          uuid.New(),
			RubricID:    newRubric.ID,
			Title:       criteria.Title,
			Description: criteria.Description,
			Weight:      criteria.Weight,
			Sequence:    criteria.Sequence,
			IsRequired:  criteria.IsRequired,
		}
		err = r.db.WithContext(ctx).Create(newCriteria).Error
		if err != nil {
			return nil, err
		}

		// Copy criteria levels
		for _, criteriaLevel := range criteria.Levels {
			newCriteriaLevel := &RubricCriteriaLevel{
				ID:          uuid.New(),
				CriteriaID:  newCriteria.ID,
				LevelID:     levelMapping[criteriaLevel.LevelID], // Map to new level ID
				Description: criteriaLevel.Description,
				Examples:    criteriaLevel.Examples,
			}
			err = r.db.WithContext(ctx).Create(newCriteriaLevel).Error
			if err != nil {
				return nil, err
			}
		}
	}

	return r.GetRubricByID(newRubric.ID)
}

// RubricCriteria operations
func (r *repository) CreateCriteria(ctx context.Context, criteria *RubricCriteria) error {
	return r.db.WithContext(ctx).Create(criteria).Error
}

func (r *repository) GetCriteriaByID(id uuid.UUID) (*RubricCriteria, error) {
	var criteria RubricCriteria
	err := r.db.Preload("Levels").Where("id = ?", id).First(&criteria).Error
	if err != nil {
		return nil, err
	}
	return &criteria, nil
}

func (r *repository) GetCriteriaByRubric(rubricID uuid.UUID) ([]RubricCriteria, error) {
	var criteria []RubricCriteria
	err := r.db.Preload("Levels").Where("rubric_id = ?", rubricID).Order("sequence ASC").Find(&criteria).Error
	return criteria, err
}

func (r *repository) UpdateCriteria(ctx context.Context, criteria *RubricCriteria) error {
	return r.db.WithContext(ctx).Save(criteria).Error
}

func (r *repository) DeleteCriteria(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&RubricCriteria{}).Error
}

// RubricLevel operations
func (r *repository) CreateLevel(ctx context.Context, level *RubricLevel) error {
	return r.db.WithContext(ctx).Create(level).Error
}

func (r *repository) GetLevelByID(id uuid.UUID) (*RubricLevel, error) {
	var level RubricLevel
	err := r.db.Where("id = ?", id).First(&level).Error
	if err != nil {
		return nil, err
	}
	return &level, nil
}

func (r *repository) GetLevelsByRubric(rubricID uuid.UUID) ([]RubricLevel, error) {
	var levels []RubricLevel
	err := r.db.Where("rubric_id = ?", rubricID).Order("sequence ASC").Find(&levels).Error
	return levels, err
}

func (r *repository) UpdateLevel(ctx context.Context, level *RubricLevel) error {
	return r.db.WithContext(ctx).Save(level).Error
}

func (r *repository) DeleteLevel(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&RubricLevel{}).Error
}

// RubricCriteriaLevel operations
func (r *repository) CreateCriteriaLevel(ctx context.Context, criteriaLevel *RubricCriteriaLevel) error {
	return r.db.WithContext(ctx).Create(criteriaLevel).Error
}

func (r *repository) GetCriteriaLevels(criteriaID uuid.UUID) ([]RubricCriteriaLevel, error) {
	var criteriaLevels []RubricCriteriaLevel
	err := r.db.Preload("Level").Where("criteria_id = ?", criteriaID).Find(&criteriaLevels).Error
	return criteriaLevels, err
}

func (r *repository) UpdateCriteriaLevel(ctx context.Context, criteriaLevel *RubricCriteriaLevel) error {
	return r.db.WithContext(ctx).Save(criteriaLevel).Error
}

func (r *repository) DeleteCriteriaLevel(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&RubricCriteriaLevel{}).Error
}
