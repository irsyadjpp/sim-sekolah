package reading_literacy

import (
	"gorm.io/gorm"
)

type Repository interface {
	// Reading Level Operations
	GetAllReadingLevels() ([]ReadingLevel, error)
	GetReadingLevelByID(id string) (*ReadingLevel, error)
	GetReadingLevelByCode(levelCode string) (*ReadingLevel, error)
	CreateReadingLevel(level *ReadingLevel) error
	UpdateReadingLevel(level *ReadingLevel) error
	DeleteReadingLevel(id string) error
	SeedReadingLevels() error

	// Assessment Operations
	GetAllAssessments() ([]ReadingLiteracyAssessment, error)
	GetAssessmentByID(id string) (*ReadingLiteracyAssessment, error)
	GetAssessmentsByStudent(studentID string) ([]ReadingLiteracyAssessment, error)
	GetAssessmentsByLevel(levelID string) ([]ReadingLiteracyAssessment, error)
	GetLatestAssessmentByStudent(studentID string) (*ReadingLiteracyAssessment, error)
	CreateAssessment(assessment *ReadingLiteracyAssessment) error
	UpdateAssessment(assessment *ReadingLiteracyAssessment) error
	DeleteAssessment(id string) error
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

// Reading Level Operations
func (r *repository) GetAllReadingLevels() ([]ReadingLevel, error) {
	var levels []ReadingLevel
	err := r.db.Where("deleted_at IS NULL").Order("level_code ASC").Find(&levels).Error
	return levels, err
}

func (r *repository) GetReadingLevelByID(id string) (*ReadingLevel, error) {
	var level ReadingLevel
	err := r.db.Where("id = ? AND deleted_at IS NULL", id).First(&level).Error
	if err != nil {
		return nil, err
	}
	return &level, nil
}

func (r *repository) GetReadingLevelByCode(levelCode string) (*ReadingLevel, error) {
	var level ReadingLevel
	err := r.db.Where("level_code = ? AND deleted_at IS NULL", levelCode).First(&level).Error
	if err != nil {
		return nil, err
	}
	return &level, nil
}

func (r *repository) CreateReadingLevel(level *ReadingLevel) error {
	return r.db.Create(level).Error
}

func (r *repository) UpdateReadingLevel(level *ReadingLevel) error {
	return r.db.Save(level).Error
}

func (r *repository) DeleteReadingLevel(id string) error {
	return r.db.Where("id = ?", id).Delete(&ReadingLevel{}).Error
}

func (r *repository) SeedReadingLevels() error {
	levels := GetStandardReadingLevels()
	for _, level := range levels {
		var count int64
		r.db.Model(&ReadingLevel{}).
			Where("level_code = ?", level.LevelCode).
			Count(&count)
		if count == 0 {
			r.db.Create(&level)
		}
	}
	return nil
}

// Assessment Operations
func (r *repository) GetAllAssessments() ([]ReadingLiteracyAssessment, error) {
	var assessments []ReadingLiteracyAssessment
	err := r.db.Where("deleted_at IS NULL").Order("assessment_date DESC").Find(&assessments).Error
	return assessments, err
}

func (r *repository) GetAssessmentByID(id string) (*ReadingLiteracyAssessment, error) {
	var assessment ReadingLiteracyAssessment
	err := r.db.Where("id = ? AND deleted_at IS NULL", id).First(&assessment).Error
	if err != nil {
		return nil, err
	}
	return &assessment, nil
}

func (r *repository) GetAssessmentsByStudent(studentID string) ([]ReadingLiteracyAssessment, error) {
	var assessments []ReadingLiteracyAssessment
	err := r.db.Where("deleted_at IS NULL AND student_id = ?", studentID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *repository) GetAssessmentsByLevel(levelID string) ([]ReadingLiteracyAssessment, error) {
	var assessments []ReadingLiteracyAssessment
	err := r.db.Where("deleted_at IS NULL AND reading_level_id = ?", levelID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *repository) GetLatestAssessmentByStudent(studentID string) (*ReadingLiteracyAssessment, error) {
	var assessment ReadingLiteracyAssessment
	err := r.db.Where("deleted_at IS NULL AND student_id = ?", studentID).
		Order("assessment_date DESC").
		First(&assessment).Error
	if err != nil {
		return nil, err
	}
	return &assessment, nil
}

func (r *repository) CreateAssessment(assessment *ReadingLiteracyAssessment) error {
	return r.db.Create(assessment).Error
}

func (r *repository) UpdateAssessment(assessment *ReadingLiteracyAssessment) error {
	return r.db.Save(assessment).Error
}

func (r *repository) DeleteAssessment(id string) error {
	return r.db.Where("id = ?", id).Delete(&ReadingLiteracyAssessment{}).Error
}
