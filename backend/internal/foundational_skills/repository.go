package foundational_skills

import (
	"gorm.io/gorm"
)

type Repository interface {
	// Skill Standard Operations
	GetAllSkillStandards() ([]FoundationalSkillStandard, error)
	GetSkillStandardByID(id string) (*FoundationalSkillStandard, error)
	GetSkillStandardsByType(skillType string) ([]FoundationalSkillStandard, error)
	CreateSkillStandard(standard *FoundationalSkillStandard) error
	UpdateSkillStandard(standard *FoundationalSkillStandard) error
	DeleteSkillStandard(id string) error
	SeedSkillStandards() error

	// Assessment Operations
	GetAllAssessments() ([]FoundationalSkillAssessment, error)
	GetAssessmentByID(id string) (*FoundationalSkillAssessment, error)
	GetAssessmentsByStudent(studentID string) ([]FoundationalSkillAssessment, error)
	GetAssessmentsByStandard(standardID string) ([]FoundationalSkillAssessment, error)
	CreateAssessment(assessment *FoundationalSkillAssessment) error
	UpdateAssessment(assessment *FoundationalSkillAssessment) error
	DeleteAssessment(id string) error
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

// Skill Standard Operations
func (r *repository) GetAllSkillStandards() ([]FoundationalSkillStandard, error) {
	var standards []FoundationalSkillStandard
	err := r.db.Where("deleted_at IS NULL").Order("skill_type ASC, skill_code ASC").Find(&standards).Error
	return standards, err
}

func (r *repository) GetSkillStandardByID(id string) (*FoundationalSkillStandard, error) {
	var standard FoundationalSkillStandard
	err := r.db.Where("id = ? AND deleted_at IS NULL", id).First(&standard).Error
	if err != nil {
		return nil, err
	}
	return &standard, nil
}

func (r *repository) GetSkillStandardsByType(skillType string) ([]FoundationalSkillStandard, error) {
	var standards []FoundationalSkillStandard
	err := r.db.Where("deleted_at IS NULL AND skill_type = ?", skillType).
		Order("skill_code ASC").
		Find(&standards).Error
	return standards, err
}

func (r *repository) CreateSkillStandard(standard *FoundationalSkillStandard) error {
	return r.db.Create(standard).Error
}

func (r *repository) UpdateSkillStandard(standard *FoundationalSkillStandard) error {
	return r.db.Save(standard).Error
}

func (r *repository) DeleteSkillStandard(id string) error {
	return r.db.Where("id = ?", id).Delete(&FoundationalSkillStandard{}).Error
}

func (r *repository) SeedSkillStandards() error {
	standards := GetStandardFoundationalSkillStandards()
	for _, standard := range standards {
		var count int64
		r.db.Model(&FoundationalSkillStandard{}).
			Where("skill_code = ?", standard.SkillCode).
			Count(&count)
		if count == 0 {
			r.db.Create(&standard)
		}
	}
	return nil
}

// Assessment Operations
func (r *repository) GetAllAssessments() ([]FoundationalSkillAssessment, error) {
	var assessments []FoundationalSkillAssessment
	err := r.db.Where("deleted_at IS NULL").Order("assessment_date DESC").Find(&assessments).Error
	return assessments, err
}

func (r *repository) GetAssessmentByID(id string) (*FoundationalSkillAssessment, error) {
	var assessment FoundationalSkillAssessment
	err := r.db.Where("id = ? AND deleted_at IS NULL", id).First(&assessment).Error
	if err != nil {
		return nil, err
	}
	return &assessment, nil
}

func (r *repository) GetAssessmentsByStudent(studentID string) ([]FoundationalSkillAssessment, error) {
	var assessments []FoundationalSkillAssessment
	err := r.db.Where("deleted_at IS NULL AND student_id = ?", studentID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *repository) GetAssessmentsByStandard(standardID string) ([]FoundationalSkillAssessment, error) {
	var assessments []FoundationalSkillAssessment
	err := r.db.Where("deleted_at IS NULL AND skill_standard_id = ?", standardID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *repository) CreateAssessment(assessment *FoundationalSkillAssessment) error {
	return r.db.Create(assessment).Error
}

func (r *repository) UpdateAssessment(assessment *FoundationalSkillAssessment) error {
	return r.db.Save(assessment).Error
}

func (r *repository) DeleteAssessment(id string) error {
	return r.db.Where("id = ?", id).Delete(&FoundationalSkillAssessment{}).Error
}
