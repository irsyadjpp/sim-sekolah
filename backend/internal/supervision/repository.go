package supervision

import (
	"database/sql"
	"fmt"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type SupervisionRepository interface {
	// SupervisionCycle operations
	CreateCycle(cycle *SupervisionCycle) error
	GetCycleByID(id uuid.UUID) (*SupervisionCycle, error)
	GetAllCycles() ([]SupervisionCycle, error)
	GetCyclesBySchool(schoolID uuid.UUID) ([]SupervisionCycle, error)
	GetCyclesByAcademicYear(academicYearID uuid.UUID) ([]SupervisionCycle, error)
	GetActiveCycles() ([]SupervisionCycle, error)
	UpdateCycle(cycle *SupervisionCycle) error
	DeleteCycle(id uuid.UUID) error

	// TeacherObservation operations
	CreateObservation(observation *TeacherObservation) error
	GetObservationByID(id uuid.UUID) (*TeacherObservation, error)
	GetAllObservations() ([]TeacherObservation, error)
	GetObservationsByTeacher(teacherID uuid.UUID) ([]TeacherObservation, error)
	GetObservationsByObserver(observerID uuid.UUID) ([]TeacherObservation, error)
	GetObservationsByCycle(cycleID uuid.UUID) ([]TeacherObservation, error)
	GetObservationsByStatus(status string) ([]TeacherObservation, error)
	UpdateObservation(observation *TeacherObservation) error
	DeleteObservation(id uuid.UUID) error

	// SupervisionFeedback operations
	CreateFeedback(feedback *SupervisionFeedback) error
	GetFeedbackByID(id uuid.UUID) (*SupervisionFeedback, error)
	GetAllFeedback() ([]SupervisionFeedback, error)
	GetFeedbackByTeacher(teacherID uuid.UUID) ([]SupervisionFeedback, error)
	GetFeedbackByObservation(observationID uuid.UUID) ([]SupervisionFeedback, error)
	UpdateFeedback(feedback *SupervisionFeedback) error
	DeleteFeedback(id uuid.UUID) error

	// SupervisionAnalytics operations
	CreateAnalytics(analytics *SupervisionAnalytics) error
	GetAnalyticsByID(id uuid.UUID) (*SupervisionAnalytics, error)
	GetAnalyticsBySchool(schoolID uuid.UUID) ([]SupervisionAnalytics, error)
	GetAnalyticsByAcademicYear(academicYearID uuid.UUID) ([]SupervisionAnalytics, error)
	GetLatestAnalytics(schoolID uuid.UUID) (*SupervisionAnalytics, error)
	UpdateAnalytics(analytics *SupervisionAnalytics) error

	// Summary operations
	GetSupervisionSummary(schoolID uuid.UUID) (*SupervisionSummaryResponse, error)
}

type supervisionRepository struct {
	db *gorm.DB
}

func NewSupervisionRepository(db *gorm.DB) SupervisionRepository {
	return &supervisionRepository{db: db}
}

// SupervisionCycle operations
func (r *supervisionRepository) CreateCycle(cycle *SupervisionCycle) error {
	return r.db.Create(cycle).Error
}

func (r *supervisionRepository) GetCycleByID(id uuid.UUID) (*SupervisionCycle, error) {
	var cycle SupervisionCycle
	err := r.db.Where("id = ?", id).First(&cycle).Error
	if err != nil {
		return nil, err
	}
	return &cycle, nil
}

func (r *supervisionRepository) GetAllCycles() ([]SupervisionCycle, error) {
	var cycles []SupervisionCycle
	err := r.db.Find(&cycles).Error
	return cycles, err
}

func (r *supervisionRepository) GetCyclesBySchool(schoolID uuid.UUID) ([]SupervisionCycle, error) {
	var cycles []SupervisionCycle
	err := r.db.Where("school_id = ?", schoolID).Find(&cycles).Error
	return cycles, err
}

func (r *supervisionRepository) GetCyclesByAcademicYear(academicYearID uuid.UUID) ([]SupervisionCycle, error) {
	var cycles []SupervisionCycle
	err := r.db.Where("academic_year_id = ?", academicYearID).Find(&cycles).Error
	return cycles, err
}

func (r *supervisionRepository) GetActiveCycles() ([]SupervisionCycle, error) {
	var cycles []SupervisionCycle
	err := r.db.Where("status = ? AND is_active = ?", SupervisionCycleStatusActive, true).Find(&cycles).Error
	return cycles, err
}

func (r *supervisionRepository) UpdateCycle(cycle *SupervisionCycle) error {
	return r.db.Save(cycle).Error
}

func (r *supervisionRepository) DeleteCycle(id uuid.UUID) error {
	return r.db.Delete(&SupervisionCycle{}, "id = ?", id).Error
}

// TeacherObservation operations
func (r *supervisionRepository) CreateObservation(observation *TeacherObservation) error {
	return r.db.Create(observation).Error
}

func (r *supervisionRepository) GetObservationByID(id uuid.UUID) (*TeacherObservation, error) {
	var observation TeacherObservation
	err := r.db.Where("id = ?", id).First(&observation).Error
	if err != nil {
		return nil, err
	}
	return &observation, nil
}

func (r *supervisionRepository) GetAllObservations() ([]TeacherObservation, error) {
	var observations []TeacherObservation
	err := r.db.Find(&observations).Error
	return observations, err
}

func (r *supervisionRepository) GetObservationsByTeacher(teacherID uuid.UUID) ([]TeacherObservation, error) {
	var observations []TeacherObservation
	err := r.db.Where("teacher_id = ?", teacherID).Find(&observations).Error
	return observations, err
}

func (r *supervisionRepository) GetObservationsByObserver(observerID uuid.UUID) ([]TeacherObservation, error) {
	var observations []TeacherObservation
	err := r.db.Where("observer_id = ?", observerID).Find(&observations).Error
	return observations, err
}

func (r *supervisionRepository) GetObservationsByCycle(cycleID uuid.UUID) ([]TeacherObservation, error) {
	var observations []TeacherObservation
	err := r.db.Where("supervision_cycle_id = ?", cycleID).Find(&observations).Error
	return observations, err
}

func (r *supervisionRepository) GetObservationsByStatus(status string) ([]TeacherObservation, error) {
	var observations []TeacherObservation
	err := r.db.Where("status = ?", status).Find(&observations).Error
	return observations, err
}

func (r *supervisionRepository) UpdateObservation(observation *TeacherObservation) error {
	return r.db.Save(observation).Error
}

func (r *supervisionRepository) DeleteObservation(id uuid.UUID) error {
	return r.db.Delete(&TeacherObservation{}, "id = ?", id).Error
}

// SupervisionFeedback operations
func (r *supervisionRepository) CreateFeedback(feedback *SupervisionFeedback) error {
	return r.db.Create(feedback).Error
}

func (r *supervisionRepository) GetFeedbackByID(id uuid.UUID) (*SupervisionFeedback, error) {
	var feedback SupervisionFeedback
	err := r.db.Where("id = ?", id).First(&feedback).Error
	if err != nil {
		return nil, err
	}
	return &feedback, nil
}

func (r *supervisionRepository) GetAllFeedback() ([]SupervisionFeedback, error) {
	var feedbacks []SupervisionFeedback
	err := r.db.Find(&feedbacks).Error
	return feedbacks, err
}

func (r *supervisionRepository) GetFeedbackByTeacher(teacherID uuid.UUID) ([]SupervisionFeedback, error) {
	var feedbacks []SupervisionFeedback
	err := r.db.Where("teacher_id = ?", teacherID).Find(&feedbacks).Error
	return feedbacks, err
}

func (r *supervisionRepository) GetFeedbackByObservation(observationID uuid.UUID) ([]SupervisionFeedback, error) {
	var feedbacks []SupervisionFeedback
	err := r.db.Where("observation_id = ?", observationID).Find(&feedbacks).Error
	return feedbacks, err
}

func (r *supervisionRepository) UpdateFeedback(feedback *SupervisionFeedback) error {
	return r.db.Save(feedback).Error
}

func (r *supervisionRepository) DeleteFeedback(id uuid.UUID) error {
	return r.db.Delete(&SupervisionFeedback{}, "id = ?", id).Error
}

// SupervisionAnalytics operations
func (r *supervisionRepository) CreateAnalytics(analytics *SupervisionAnalytics) error {
	return r.db.Create(analytics).Error
}

func (r *supervisionRepository) GetAnalyticsByID(id uuid.UUID) (*SupervisionAnalytics, error) {
	var analytics SupervisionAnalytics
	err := r.db.Where("id = ?", id).First(&analytics).Error
	if err != nil {
		return nil, err
	}
	return &analytics, nil
}

func (r *supervisionRepository) GetAnalyticsBySchool(schoolID uuid.UUID) ([]SupervisionAnalytics, error) {
	var analytics []SupervisionAnalytics
	err := r.db.Where("school_id = ?", schoolID).Order("analytics_date DESC").Find(&analytics).Error
	return analytics, err
}

func (r *supervisionRepository) GetAnalyticsByAcademicYear(academicYearID uuid.UUID) ([]SupervisionAnalytics, error) {
	var analytics []SupervisionAnalytics
	err := r.db.Where("academic_year_id = ?", academicYearID).Order("analytics_date DESC").Find(&analytics).Error
	return analytics, err
}

func (r *supervisionRepository) GetLatestAnalytics(schoolID uuid.UUID) (*SupervisionAnalytics, error) {
	var analytics SupervisionAnalytics
	err := r.db.Where("school_id = ?", schoolID).Order("analytics_date DESC").First(&analytics).Error
	if err != nil {
		return nil, err
	}
	return &analytics, nil
}

func (r *supervisionRepository) UpdateAnalytics(analytics *SupervisionAnalytics) error {
	return r.db.Save(analytics).Error
}

// Summary operations
func (r *supervisionRepository) GetSupervisionSummary(schoolID uuid.UUID) (*SupervisionSummaryResponse, error) {
	var summary SupervisionSummaryResponse

	// Count total cycles
	if err := r.db.Model(&SupervisionCycle{}).Where("school_id = ?", schoolID).Count(&summary.TotalCycles).Error; err != nil {
		return nil, fmt.Errorf("error counting total cycles: %w", err)
	}

	// Count active cycles
	if err := r.db.Model(&SupervisionCycle{}).Where("school_id = ? AND status = ?", schoolID, SupervisionCycleStatusActive).Count(&summary.ActiveCycles).Error; err != nil {
		return nil, fmt.Errorf("error counting active cycles: %w", err)
	}

	// Count total observations
	if err := r.db.Model(&TeacherObservation{}).
		Joins("JOIN supervision_cycles ON teacher_observations.supervision_cycle_id = supervision_cycles.id").
		Where("supervision_cycles.school_id = ?", schoolID).
		Count(&summary.TotalObservations).Error; err != nil {
		return nil, fmt.Errorf("error counting total observations: %w", err)
	}

	// Count pending observations
	if err := r.db.Model(&TeacherObservation{}).
		Joins("JOIN supervision_cycles ON teacher_observations.supervision_cycle_id = supervision_cycles.id").
		Where("supervision_cycles.school_id = ? AND teacher_observations.status = ?", schoolID, ObservationStatusScheduled).
		Count(&summary.PendingObservations).Error; err != nil {
		return nil, fmt.Errorf("error counting pending observations: %w", err)
	}

	// Count completed observations
	if err := r.db.Model(&TeacherObservation{}).
		Joins("JOIN supervision_cycles ON teacher_observations.supervision_cycle_id = supervision_cycles.id").
		Where("supervision_cycles.school_id = ? AND teacher_observations.status = ?", schoolID, ObservationStatusCompleted).
		Count(&summary.CompletedObservations).Error; err != nil {
		return nil, fmt.Errorf("error counting completed observations: %w", err)
	}

	// Calculate average score
	var avgScore sql.NullFloat64
	if err := r.db.Model(&TeacherObservation{}).
		Select("AVG(score)").
		Joins("JOIN supervision_cycles ON teacher_observations.supervision_cycle_id = supervision_cycles.id").
		Where("supervision_cycles.school_id = ? AND teacher_observations.score IS NOT NULL", schoolID).
		Scan(&avgScore).Error; err != nil {
		return nil, fmt.Errorf("error calculating average score: %w", err)
	}
	if avgScore.Valid {
		summary.AverageScore = avgScore.Float64
	}

	// Count unique teachers supervised
	if err := r.db.Model(&TeacherObservation{}).
		Select("COUNT(DISTINCT teacher_id)").
		Joins("JOIN supervision_cycles ON teacher_observations.supervision_cycle_id = supervision_cycles.id").
		Where("supervision_cycles.school_id = ?", schoolID).
		Scan(&summary.TeachersSupervised).Error; err != nil {
		return nil, fmt.Errorf("error counting teachers supervised: %w", err)
	}

	return &summary, nil
}
