package assessment

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"gorm.io/gorm"
	"gorm.io/gorm/clause"
)

type AssessmentRepository interface {
	GetByTeachingAssignment(ctx context.Context, assignmentID string) ([]Assessment, error)
	GetByID(ctx context.Context, id string) (*Assessment, error)
	Create(ctx context.Context, data *Assessment) error
	Update(ctx context.Context, data *Assessment) error
	Delete(ctx context.Context, id string) error

	// Scores
	GetScoresByAssessment(ctx context.Context, assessmentID string) ([]AssessmentScore, error)
	UpsertScores(ctx context.Context, assessmentID string, scores []AssessmentScore) error

	// Attendance
	GetAttendancesByClassroomAndDate(ctx context.Context, classroomID string, date string) ([]DailyAttendance, error)
	UpsertAttendances(ctx context.Context, attendances []DailyAttendance) error

	// SD Assessment Criteria
	GetAllSDAssessmentCriteria(ctx context.Context) ([]SDAssessmentCriteria, error)
	GetSDAssessmentCriteriaByID(ctx context.Context, id string) (*SDAssessmentCriteria, error)
	GetSDAssessmentCriteriaByType(ctx context.Context, assessmentType string) ([]SDAssessmentCriteria, error)
	GetSDAssessmentCriteriaByPhase(ctx context.Context, phaseID string) ([]SDAssessmentCriteria, error)
	CreateSDAssessmentCriteria(ctx context.Context, data *SDAssessmentCriteria) error
	UpdateSDAssessmentCriteria(ctx context.Context, data *SDAssessmentCriteria) error
	DeleteSDAssessmentCriteria(ctx context.Context, id string) error
}

type assessmentRepository struct {
	db *gorm.DB
}

func NewAssessmentRepository(db *gorm.DB) AssessmentRepository {
	return &assessmentRepository{db: db}
}

func (r *assessmentRepository) GetByTeachingAssignment(ctx context.Context, assignmentID string) ([]Assessment, error) {
	var assessments []Assessment
	err := r.db.WithContext(ctx).
		Where("teaching_assignment_id = ?", assignmentID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *assessmentRepository) GetByID(ctx context.Context, id string) (*Assessment, error) {
	var a Assessment
	err := r.db.WithContext(ctx).
		Preload("TeachingAssignment").
		First(&a, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return &a, nil
}

func (r *assessmentRepository) Create(ctx context.Context, data *Assessment) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *assessmentRepository) Update(ctx context.Context, data *Assessment) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *assessmentRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&Assessment{}, "id = ?", id).Error
}

func (r *assessmentRepository) GetScoresByAssessment(ctx context.Context, assessmentID string) ([]AssessmentScore, error) {
	var scores []AssessmentScore
	err := r.db.WithContext(ctx).
		Preload("Student").
		Where("assessment_id = ?", assessmentID).
		Find(&scores).Error
	return scores, err
}

func (r *assessmentRepository) UpsertScores(ctx context.Context, assessmentID string, scores []AssessmentScore) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		for _, score := range scores {
			var studentStatus string
			err := tx.Table("master_student").
				Select("student_status").
				Where("id = ?", score.StudentID).
				Row().Scan(&studentStatus)
			if err != nil {
				return err
			}
			if studentStatus != "active" {
				return errors.New("siswa dengan ID " + score.StudentID.String() + " tidak aktif (status: " + studentStatus + "), pencatatan nilai ditolak")
			}

			if score.ID == uuid.Nil {
				score.ID = uuid.New()
			}
			err = tx.Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "assessment_id"}, {Name: "student_id"}},
				DoUpdates: clause.AssignmentColumns([]string{"score", "notes"}),
			}).Create(&score).Error
			if err != nil {
				return err
			}
		}
		return nil
	})
}

func (r *assessmentRepository) GetAttendancesByClassroomAndDate(ctx context.Context, classroomID string, date string) ([]DailyAttendance, error) {
	var attendances []DailyAttendance
	err := r.db.WithContext(ctx).
		Preload("Student").
		Where("classroom_id = ? AND date = ?", classroomID, date).
		Find(&attendances).Error
	return attendances, err
}

func (r *assessmentRepository) UpsertAttendances(ctx context.Context, attendances []DailyAttendance) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		for _, att := range attendances {
			var studentStatus string
			err := tx.Table("master_student").
				Select("student_status").
				Where("id = ?", att.StudentID).
				Row().Scan(&studentStatus)
			if err != nil {
				return err
			}
			if studentStatus != "active" {
				return errors.New("siswa dengan ID " + att.StudentID.String() + " tidak aktif (status: " + studentStatus + "), pencatatan kehadiran ditolak")
			}

			if att.ID == uuid.Nil {
				att.ID = uuid.New()
			}
			err = tx.Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "classroom_id"}, {Name: "student_id"}, {Name: "date"}},
				DoUpdates: clause.AssignmentColumns([]string{"status", "notes"}),
			}).Create(&att).Error
			if err != nil {
				return err
			}
		}
		return nil
	})
}

// SD Assessment Criteria Methods
func (r *assessmentRepository) GetAllSDAssessmentCriteria(ctx context.Context) ([]SDAssessmentCriteria, error) {
	var criteria []SDAssessmentCriteria
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("assessment_type ASC, criteria_name ASC").
		Find(&criteria).Error
	return criteria, err
}

func (r *assessmentRepository) GetSDAssessmentCriteriaByID(ctx context.Context, id string) (*SDAssessmentCriteria, error) {
	var criterion SDAssessmentCriteria
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&criterion).Error
	if err != nil {
		return nil, err
	}
	return &criterion, nil
}

func (r *assessmentRepository) GetSDAssessmentCriteriaByType(ctx context.Context, assessmentType string) ([]SDAssessmentCriteria, error) {
	var criteria []SDAssessmentCriteria
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL AND assessment_type = ?", assessmentType).
		Order("criteria_name ASC").
		Find(&criteria).Error
	return criteria, err
}

func (r *assessmentRepository) GetSDAssessmentCriteriaByPhase(ctx context.Context, phaseID string) ([]SDAssessmentCriteria, error) {
	var criteria []SDAssessmentCriteria
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL AND phase_id = ?", phaseID).
		Order("assessment_type ASC, criteria_name ASC").
		Find(&criteria).Error
	return criteria, err
}

func (r *assessmentRepository) CreateSDAssessmentCriteria(ctx context.Context, data *SDAssessmentCriteria) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *assessmentRepository) UpdateSDAssessmentCriteria(ctx context.Context, data *SDAssessmentCriteria) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *assessmentRepository) DeleteSDAssessmentCriteria(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&SDAssessmentCriteria{}, "id = ?", id).Error
}
