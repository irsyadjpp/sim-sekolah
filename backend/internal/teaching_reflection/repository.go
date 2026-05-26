package teaching_reflection

import (
	"database/sql"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type TeachingReflectionRepository interface {
	// TeachingReflection operations
	CreateReflection(reflection *TeachingReflection) error
	GetReflectionByID(id uuid.UUID) (*TeachingReflection, error)
	GetAllReflections() ([]TeachingReflection, error)
	GetReflectionsByTeacher(teacherID uuid.UUID) ([]TeachingReflection, error)
	GetReflectionsByType(reflectionType string) ([]TeachingReflection, error)
	GetReflectionsByStatus(status string) ([]TeachingReflection, error)
	UpdateReflection(reflection *TeachingReflection) error
	DeleteReflection(id uuid.UUID) error

	// EffectivenessMetrics operations
	CreateEffectivenessMetrics(metrics *EffectivenessMetrics) error
	GetEffectivenessMetricsByID(id uuid.UUID) (*EffectivenessMetrics, error)
	GetEffectivenessMetricsByTeacher(teacherID uuid.UUID) ([]EffectivenessMetrics, error)
	UpdateEffectivenessMetrics(metrics *EffectivenessMetrics) error
	DeleteEffectivenessMetrics(id uuid.UUID) error

	// QualityIndicators operations
	CreateQualityIndicator(indicator *QualityIndicators) error
	GetQualityIndicatorByID(id uuid.UUID) (*QualityIndicators, error)
	GetQualityIndicatorsByTeacher(teacherID uuid.UUID) ([]QualityIndicators, error)
	UpdateQualityIndicator(indicator *QualityIndicators) error
	DeleteQualityIndicator(id uuid.UUID) error

	// Summary operations
	GetReflectionSummary(teacherID uuid.UUID) (*ReflectionSummaryResponse, error)
}

type teachingReflectionRepository struct {
	db *gorm.DB
}

func NewTeachingReflectionRepository(db *gorm.DB) TeachingReflectionRepository {
	return &teachingReflectionRepository{db: db}
}

// TeachingReflection operations
func (r *teachingReflectionRepository) CreateReflection(reflection *TeachingReflection) error {
	return r.db.Create(reflection).Error
}

func (r *teachingReflectionRepository) GetReflectionByID(id uuid.UUID) (*TeachingReflection, error) {
	var reflection TeachingReflection
	err := r.db.Where("id = ?", id).First(&reflection).Error
	if err != nil {
		return nil, err
	}
	return &reflection, nil
}

func (r *teachingReflectionRepository) GetAllReflections() ([]TeachingReflection, error) {
	var reflections []TeachingReflection
	err := r.db.Find(&reflections).Error
	return reflections, err
}

func (r *teachingReflectionRepository) GetReflectionsByTeacher(teacherID uuid.UUID) ([]TeachingReflection, error) {
	var reflections []TeachingReflection
	err := r.db.Where("teacher_id = ?", teacherID).Order("reflection_date DESC").Find(&reflections).Error
	return reflections, err
}

func (r *teachingReflectionRepository) GetReflectionsByType(reflectionType string) ([]TeachingReflection, error) {
	var reflections []TeachingReflection
	err := r.db.Where("reflection_type = ?", reflectionType).Find(&reflections).Error
	return reflections, err
}

func (r *teachingReflectionRepository) GetReflectionsByStatus(status string) ([]TeachingReflection, error) {
	var reflections []TeachingReflection
	err := r.db.Where("status = ?", status).Find(&reflections).Error
	return reflections, err
}

func (r *teachingReflectionRepository) UpdateReflection(reflection *TeachingReflection) error {
	return r.db.Save(reflection).Error
}

func (r *teachingReflectionRepository) DeleteReflection(id uuid.UUID) error {
	return r.db.Delete(&TeachingReflection{}, "id = ?", id).Error
}

// EffectivenessMetrics operations
func (r *teachingReflectionRepository) CreateEffectivenessMetrics(metrics *EffectivenessMetrics) error {
	return r.db.Create(metrics).Error
}

func (r *teachingReflectionRepository) GetEffectivenessMetricsByID(id uuid.UUID) (*EffectivenessMetrics, error) {
	var metrics EffectivenessMetrics
	err := r.db.Where("id = ?", id).First(&metrics).Error
	if err != nil {
		return nil, err
	}
	return &metrics, nil
}

func (r *teachingReflectionRepository) GetEffectivenessMetricsByTeacher(teacherID uuid.UUID) ([]EffectivenessMetrics, error) {
	var metrics []EffectivenessMetrics
	err := r.db.Where("teacher_id = ?", teacherID).Order("measurement_date DESC").Find(&metrics).Error
	return metrics, err
}

func (r *teachingReflectionRepository) UpdateEffectivenessMetrics(metrics *EffectivenessMetrics) error {
	return r.db.Save(metrics).Error
}

func (r *teachingReflectionRepository) DeleteEffectivenessMetrics(id uuid.UUID) error {
	return r.db.Delete(&EffectivenessMetrics{}, "id = ?", id).Error
}

// QualityIndicators operations
func (r *teachingReflectionRepository) CreateQualityIndicator(indicator *QualityIndicators) error {
	return r.db.Create(indicator).Error
}

func (r *teachingReflectionRepository) GetQualityIndicatorByID(id uuid.UUID) (*QualityIndicators, error) {
	var indicator QualityIndicators
	err := r.db.Where("id = ?", id).First(&indicator).Error
	if err != nil {
		return nil, err
	}
	return &indicator, nil
}

func (r *teachingReflectionRepository) GetQualityIndicatorsByTeacher(teacherID uuid.UUID) ([]QualityIndicators, error) {
	var indicators []QualityIndicators
	err := r.db.Where("teacher_id = ?", teacherID).Order("assessment_date DESC").Find(&indicators).Error
	return indicators, err
}

func (r *teachingReflectionRepository) UpdateQualityIndicator(indicator *QualityIndicators) error {
	return r.db.Save(indicator).Error
}

func (r *teachingReflectionRepository) DeleteQualityIndicator(id uuid.UUID) error {
	return r.db.Delete(&QualityIndicators{}, "id = ?", id).Error
}

// Summary operations
func (r *teachingReflectionRepository) GetReflectionSummary(teacherID uuid.UUID) (*ReflectionSummaryResponse, error) {
	var summary ReflectionSummaryResponse

	// Count total reflections
	if err := r.db.Model(&TeachingReflection{}).Where("teacher_id = ?", teacherID).Count(&summary.TotalReflections).Error; err != nil {
		return nil, err
	}

	// Count submitted reflections
	if err := r.db.Model(&TeachingReflection{}).Where("teacher_id = ? AND status = ?", teacherID, ReflectionStatusSubmitted).Count(&summary.SubmittedReflections).Error; err != nil {
		return nil, err
	}

	// Calculate average self rating
	var avgRating sql.NullFloat64
	if err := r.db.Model(&TeachingReflection{}).
		Select("AVG(self_rating)").
		Where("teacher_id = ? AND self_rating IS NOT NULL", teacherID).
		Scan(&avgRating).Error; err != nil {
		return nil, err
	}
	if avgRating.Valid {
		summary.AverageSelfRating = avgRating.Float64
	}

	// Find most used reflection type
	var mostUsedType struct {
		ReflectionType string
		Count          int64
	}
	if err := r.db.Model(&TeachingReflection{}).
		Select("reflection_type, COUNT(*) as count").
		Where("teacher_id = ?", teacherID).
		Group("reflection_type").
		Order("count DESC").
		Limit(1).
		Scan(&mostUsedType).Error; err != nil {
		return nil, err
	}
	summary.MostUsedType = mostUsedType.ReflectionType

	// Count recent activity (last 30 days)
	if err := r.db.Model(&TeachingReflection{}).
		Where("teacher_id = ? AND reflection_date >= CURRENT_DATE - INTERVAL '30 days'", teacherID).
		Count(&summary.RecentActivity).Error; err != nil {
		return nil, err
	}

	return &summary, nil
}
