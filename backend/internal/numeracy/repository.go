package numeracy

import (
	"fmt"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Repository interface {
	CreateIndicator(indicator *NumeracyIndicator) error
	GetIndicatorByID(id uuid.UUID) (*NumeracyIndicator, error)
	GetIndicators(filter map[string]interface{}) ([]NumeracyIndicator, error)
	UpdateIndicator(indicator *NumeracyIndicator) error
	DeleteIndicator(id uuid.UUID) error

	CreateAssessment(assessment *NumeracyAssessment) error
	GetAssessmentByID(id uuid.UUID) (*NumeracyAssessment, error)
	GetAssessments(filter map[string]interface{}) ([]NumeracyAssessment, error)
	UpdateAssessment(assessment *NumeracyAssessment) error
	DeleteAssessment(id uuid.UUID) error

	CreateGrowth(growth *NumeracyGrowth) error
	GetGrowthByID(id uuid.UUID) (*NumeracyGrowth, error)
	GetGrowthByStudentAndPeriod(studentID uuid.UUID, period string) (*NumeracyGrowth, error)
	GetGrowths(filter map[string]interface{}) ([]NumeracyGrowth, error)
	UpdateGrowth(growth *NumeracyGrowth) error
	DeleteGrowth(id uuid.UUID) error

	CreateIntervention(intervention *NumeracyIntervention) error
	GetInterventionByID(id uuid.UUID) (*NumeracyIntervention, error)
	GetInterventions(filter map[string]interface{}) ([]NumeracyIntervention, error)
	UpdateIntervention(intervention *NumeracyIntervention) error
	DeleteIntervention(id uuid.UUID) error

	GetNumeracyAnalytics(request NumeracyAnalyticsRequest) (*NumeracyAnalyticsResponse, error)
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

// Indicator operations
func (r *repository) CreateIndicator(indicator *NumeracyIndicator) error {
	return r.db.Create(indicator).Error
}

func (r *repository) GetIndicatorByID(id uuid.UUID) (*NumeracyIndicator, error) {
	var indicator NumeracyIndicator
	err := r.db.Preload("Phase").Where("id = ? AND deleted_at IS NULL", id).First(&indicator).Error
	if err != nil {
		return nil, err
	}
	return &indicator, nil
}

func (r *repository) GetIndicators(filter map[string]interface{}) ([]NumeracyIndicator, error) {
	var indicators []NumeracyIndicator
	query := r.db.Preload("Phase").Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Find(&indicators).Error
	return indicators, err
}

func (r *repository) UpdateIndicator(indicator *NumeracyIndicator) error {
	return r.db.Save(indicator).Error
}

func (r *repository) DeleteIndicator(id uuid.UUID) error {
	return r.db.Model(&NumeracyIndicator{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

// Assessment operations
func (r *repository) CreateAssessment(assessment *NumeracyAssessment) error {
	return r.db.Create(assessment).Error
}

func (r *repository) GetAssessmentByID(id uuid.UUID) (*NumeracyAssessment, error) {
	var assessment NumeracyAssessment
	err := r.db.Preload("Student").Preload("Indicator").Where("id = ? AND deleted_at IS NULL", id).First(&assessment).Error
	if err != nil {
		return nil, err
	}
	return &assessment, nil
}

func (r *repository) GetAssessments(filter map[string]interface{}) ([]NumeracyAssessment, error) {
	var assessments []NumeracyAssessment
	query := r.db.Preload("Student").Preload("Indicator").Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Order("assessment_date DESC, created_at DESC").Find(&assessments).Error
	return assessments, err
}

func (r *repository) UpdateAssessment(assessment *NumeracyAssessment) error {
	return r.db.Save(assessment).Error
}

func (r *repository) DeleteAssessment(id uuid.UUID) error {
	return r.db.Model(&NumeracyAssessment{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

// Growth operations
func (r *repository) CreateGrowth(growth *NumeracyGrowth) error {
	return r.db.Create(growth).Error
}

func (r *repository) GetGrowthByID(id uuid.UUID) (*NumeracyGrowth, error) {
	var growth NumeracyGrowth
	err := r.db.Preload("Student").Where("id = ? AND deleted_at IS NULL", id).First(&growth).Error
	if err != nil {
		return nil, err
	}
	return &growth, nil
}

func (r *repository) GetGrowthByStudentAndPeriod(studentID uuid.UUID, period string) (*NumeracyGrowth, error) {
	var growth NumeracyGrowth
	err := r.db.Preload("Student").Where("student_id = ? AND period = ? AND deleted_at IS NULL", studentID, period).First(&growth).Error
	if err != nil {
		return nil, err
	}
	return &growth, nil
}

func (r *repository) GetGrowths(filter map[string]interface{}) ([]NumeracyGrowth, error) {
	var growths []NumeracyGrowth
	query := r.db.Preload("Student").Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Order("created_at DESC").Find(&growths).Error
	return growths, err
}

func (r *repository) UpdateGrowth(growth *NumeracyGrowth) error {
	return r.db.Save(growth).Error
}

func (r *repository) DeleteGrowth(id uuid.UUID) error {
	return r.db.Model(&NumeracyGrowth{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

// Intervention operations
func (r *repository) CreateIntervention(intervention *NumeracyIntervention) error {
	return r.db.Create(intervention).Error
}

func (r *repository) GetInterventionByID(id uuid.UUID) (*NumeracyIntervention, error) {
	var intervention NumeracyIntervention
	err := r.db.Preload("Student").Preload("Indicator").Where("id = ? AND deleted_at IS NULL", id).First(&intervention).Error
	if err != nil {
		return nil, err
	}
	return &intervention, nil
}

func (r *repository) GetInterventions(filter map[string]interface{}) ([]NumeracyIntervention, error) {
	var interventions []NumeracyIntervention
	query := r.db.Preload("Student").Preload("Indicator").Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Order("created_at DESC").Find(&interventions).Error
	return interventions, err
}

func (r *repository) UpdateIntervention(intervention *NumeracyIntervention) error {
	return r.db.Save(intervention).Error
}

func (r *repository) DeleteIntervention(id uuid.UUID) error {
	return r.db.Model(&NumeracyIntervention{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

// Analytics operations
func (r *repository) GetNumeracyAnalytics(request NumeracyAnalyticsRequest) (*NumeracyAnalyticsResponse, error) {
	response := &NumeracyAnalyticsResponse{}

	// Base query for assessments
	baseQuery := r.db.Model(&NumeracyAssessment{}).Where("deleted_at IS NULL")

	// Apply filters
	if request.StudentID != nil {
		baseQuery = baseQuery.Where("student_id = ?", *request.StudentID)
	}
	if request.StartDate != nil {
		baseQuery = baseQuery.Where("assessment_date >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		baseQuery = baseQuery.Where("assessment_date <= ?", *request.EndDate)
	}

	// Get total assessments
	baseQuery.Count(&response.TotalAssessments)

	// Get average score
	var avgScore float64
	baseQuery.Select("AVG(score)").Scan(&avgScore)
	response.AverageScore = avgScore

	// Get mastery rate (percentage of assessments with mastery level MENGUASAI)
	var masteryCount int64
	var totalMasteryCheck int64
	baseQuery.Count(&totalMasteryCheck)
	baseQuery.Where("mastery_level = ?", "MENGUASAI").Count(&masteryCount)
	if totalMasteryCheck > 0 {
		response.MasteryRate = float64(masteryCount) / float64(totalMasteryCheck) * 100
	}

	// Get statistics by numeracy type
	typeStatsQuery := r.db.Table("numeracy_assessments").
		Select("ni.numeracy_type, COUNT(*) as count, AVG(na.score) as average_score").
		Joins("JOIN numeracy_indicators ni ON numeracy_assessments.indicator_id = ni.id").
		Where("numeracy_assessments.deleted_at IS NULL")

	if request.StudentID != nil {
		typeStatsQuery = typeStatsQuery.Where("numeracy_assessments.student_id = ?", *request.StudentID)
	}
	if request.StartDate != nil {
		typeStatsQuery = typeStatsQuery.Where("numeracy_assessments.assessment_date >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		typeStatsQuery = typeStatsQuery.Where("numeracy_assessments.assessment_date <= ?", *request.EndDate)
	}

	typeStatsQuery.Group("ni.numeracy_type")

	typeStats := []struct {
		NumeracyType string
		Count        int64
		AverageScore float64
	}{}

	typeStatsQuery.Scan(&typeStats)

	for _, stat := range typeStats {
		response.ByNumeracyType = append(response.ByNumeracyType, NumeracyTypeStats{
			NumeracyType: stat.NumeracyType,
			TypeName:     GetNumeracyTypeDescription(stat.NumeracyType),
			Count:        stat.Count,
			AverageScore: stat.AverageScore,
		})
	}

	// Get statistics by mastery level
	masteryStatsQuery := r.db.Model(&NumeracyAssessment{}).
		Select("mastery_level, COUNT(*) as count").
		Where("deleted_at IS NULL")

	if request.StudentID != nil {
		masteryStatsQuery = masteryStatsQuery.Where("student_id = ?", *request.StudentID)
	}
	if request.StartDate != nil {
		masteryStatsQuery = masteryStatsQuery.Where("assessment_date >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		masteryStatsQuery = masteryStatsQuery.Where("assessment_date <= ?", *request.EndDate)
	}

	masteryStatsQuery.Group("mastery_level")

	masteryStats := []struct {
		MasteryLevel string
		Count        int64
	}{}

	masteryStatsQuery.Scan(&masteryStats)

	totalCount := int64(0)
	for _, stat := range masteryStats {
		totalCount += stat.Count
	}

	for _, stat := range masteryStats {
		percentage := float64(0)
		if totalCount > 0 {
			percentage = float64(stat.Count) / float64(totalCount) * 100
		}
		response.ByMasteryLevel = append(response.ByMasteryLevel, MasteryLevelStats{
			MasteryLevel: stat.MasteryLevel,
			LevelName:    GetMasteryLevelDescription(stat.MasteryLevel),
			Count:        stat.Count,
			Percentage:   percentage,
		})
	}

	return response, nil
}
