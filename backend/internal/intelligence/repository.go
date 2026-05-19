package intelligence

import (
	"context"
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
	"gorm.io/gorm/clause"
)

type IntelligenceRepository interface {
	// Profile Ext
	GetProfileExt(ctx context.Context, studentID uuid.UUID) (*StudentProfileExt, error)
	UpsertProfileExt(ctx context.Context, data *StudentProfileExt) error

	// Anecdotal Observational Journal
	GetAnecdotalsByStudent(ctx context.Context, studentID uuid.UUID) ([]AnecdotalObservation, error)
	CreateAnecdotal(ctx context.Context, obs *AnecdotalObservation, tagIDs []string) error
	GetObservationTags(ctx context.Context) ([]ObservationTag, error)

	// Agile Assessment Engine
	CreateInstrument(ctx context.Context, data *AssessmentInstrument) error
	GetInstrumentByID(ctx context.Context, id uuid.UUID) (*AssessmentInstrument, error)
	SubmitResultsBatch(ctx context.Context, results []StudentAssessmentResult) error
	GetResultsByInstrument(ctx context.Context, instrumentID uuid.UUID) ([]StudentAssessmentResult, error)
	GetAcademicProgressByStudent(ctx context.Context, studentID uuid.UUID) (map[string]interface{}, error)

	// Actionable Analytics (EWS)
	GetAlertsByClassroom(ctx context.Context, classroomID uuid.UUID) ([]EarlyWarningAlert, error)
	GetAlertsByStudent(ctx context.Context, studentID uuid.UUID) ([]EarlyWarningAlert, error)
	UpdateAlert(ctx context.Context, alertID uuid.UUID, status, notes string, resolvedAt *time.Time) error
	CreateAlert(ctx context.Context, alert *EarlyWarningAlert) error
	CheckAlertExists(ctx context.Context, studentID uuid.UUID, alertType string) (bool, error)
}

type intelligenceRepository struct {
	db *gorm.DB
}

func NewIntelligenceRepository(db *gorm.DB) IntelligenceRepository {
	return &intelligenceRepository{db: db}
}

func (r *intelligenceRepository) GetProfileExt(ctx context.Context, studentID uuid.UUID) (*StudentProfileExt, error) {
	var profile StudentProfileExt
	err := r.db.WithContext(ctx).First(&profile, "student_id = ?", studentID).Error
	if err != nil {
		if err == gorm.ErrRecordNotFound {
			return nil, nil
		}
		return nil, err
	}
	return &profile, nil
}

func (r *intelligenceRepository) UpsertProfileExt(ctx context.Context, data *StudentProfileExt) error {
	return r.db.WithContext(ctx).Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "student_id"}},
		DoUpdates: clause.AssignmentColumns([]string{"learning_style", "dominant_interests", "special_needs_notes", "baseline_literacy", "baseline_numeracy", "updated_at"}),
	}).Create(data).Error
}

func (r *intelligenceRepository) GetAnecdotalsByStudent(ctx context.Context, studentID uuid.UUID) ([]AnecdotalObservation, error) {
	var observations []AnecdotalObservation
	err := r.db.WithContext(ctx).
		Preload("Tags").
		Where("student_id = ?", studentID).
		Order("observation_date DESC, created_at DESC").
		Find(&observations).Error
	return observations, err
}

func (r *intelligenceRepository) CreateAnecdotal(ctx context.Context, obs *AnecdotalObservation, tagIDs []string) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		if err := tx.Create(obs).Error; err != nil {
			return err
		}

		for _, tagID := range tagIDs {
			mapping := ObservationTagMapping{
				ObservationID: obs.ID,
				TagID:         tagID,
			}
			if err := tx.Create(&mapping).Error; err != nil {
				return err
			}
		}
		return nil
	})
}

func (r *intelligenceRepository) GetObservationTags(ctx context.Context) ([]ObservationTag, error) {
	var tags []ObservationTag
	err := r.db.WithContext(ctx).Find(&tags).Error
	return tags, err
}

func (r *intelligenceRepository) CreateInstrument(ctx context.Context, data *AssessmentInstrument) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *intelligenceRepository) GetInstrumentByID(ctx context.Context, id uuid.UUID) (*AssessmentInstrument, error) {
	var inst AssessmentInstrument
	err := r.db.WithContext(ctx).First(&inst, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return &inst, nil
}

func (r *intelligenceRepository) SubmitResultsBatch(ctx context.Context, results []StudentAssessmentResult) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		for _, res := range results {
			if res.ID == uuid.Nil {
				res.ID = uuid.New()
			}
			err := tx.Clauses(clause.OnConflict{
				Columns:   []clause.Column{{Name: "instrument_id"}, {Name: "student_id"}},
				DoUpdates: clause.AssignmentColumns([]string{"numeric_score", "rubric_achievement", "narrative_feedback", "assessed_at"}),
			}).Create(&res).Error
			if err != nil {
				return err
			}
		}
		return nil
	})
}

func (r *intelligenceRepository) GetResultsByInstrument(ctx context.Context, instrumentID uuid.UUID) ([]StudentAssessmentResult, error) {
	var results []StudentAssessmentResult
	err := r.db.WithContext(ctx).Where("instrument_id = ?", instrumentID).Find(&results).Error
	return results, err
}

func (r *intelligenceRepository) GetAcademicProgressByStudent(ctx context.Context, studentID uuid.UUID) (map[string]interface{}, error) {
	// Menghitung progress akademik berdasarkan Tujuan Pembelajaran (TP) yang sudah di-assess
	type Progress struct {
		LearningObjectiveTitle string   `json:"learning_objective_title"`
		AverageScore           *float64 `json:"average_score"`
		LastRubric             string   `json:"last_rubric"`
	}

	var rawProgress []Progress
	err := r.db.WithContext(ctx).Raw(`
		SELECT 
			co.title as learning_objective_title,
			AVG(ar.numeric_score) as average_score,
			(SELECT ar2.rubric_achievement 
			 FROM trx_student_assessment_result ar2
			 JOIN trx_assessment_instrument ai2 ON ar2.instrument_id = ai2.id
			 WHERE ar2.student_id = ar.student_id AND ai2.learning_objective_id = ai.learning_objective_id
			 ORDER BY ar2.assessed_at DESC LIMIT 1) as last_rubric
		FROM trx_student_assessment_result ar
		JOIN trx_assessment_instrument ai ON ar.instrument_id = ai.id
		JOIN cur_learning_objective co ON ai.learning_objective_id = co.id
		WHERE ar.student_id = ?
		GROUP BY co.title, ai.learning_objective_id, ar.student_id
	`, studentID).Scan(&rawProgress).Error

	if err != nil {
		return nil, err
	}

	res := make(map[string]interface{})
	res["objectives_evaluated"] = len(rawProgress)
	res["details"] = rawProgress

	return res, nil
}

func (r *intelligenceRepository) GetAlertsByClassroom(ctx context.Context, classroomID uuid.UUID) ([]EarlyWarningAlert, error) {
	var alerts []EarlyWarningAlert
	err := r.db.WithContext(ctx).
		Where("classroom_id = ?", classroomID).
		Order("severity_level DESC, detected_at DESC").
		Find(&alerts).Error
	return alerts, err
}

func (r *intelligenceRepository) GetAlertsByStudent(ctx context.Context, studentID uuid.UUID) ([]EarlyWarningAlert, error) {
	var alerts []EarlyWarningAlert
	err := r.db.WithContext(ctx).
		Where("student_id = ?", studentID).
		Order("detected_at DESC").
		Find(&alerts).Error
	return alerts, err
}

func (r *intelligenceRepository) UpdateAlert(ctx context.Context, alertID uuid.UUID, status, notes string, resolvedAt *time.Time) error {
	return r.db.WithContext(ctx).
		Table("anl_early_warning_alert").
		Where("id = ?", alertID).
		Updates(map[string]interface{}{
			"status":             status,
			"intervention_notes": notes,
			"resolved_at":        resolvedAt,
		}).Error
}

func (r *intelligenceRepository) CreateAlert(ctx context.Context, alert *EarlyWarningAlert) error {
	return r.db.WithContext(ctx).Create(alert).Error
}

func (r *intelligenceRepository) CheckAlertExists(ctx context.Context, studentID uuid.UUID, alertType string) (bool, error) {
	var count int64
	err := r.db.WithContext(ctx).
		Table("anl_early_warning_alert").
		Where("student_id = ? AND alert_type = ? AND status = 'OPEN'", studentID, alertType).
		Count(&count).Error
	return count > 0, err
}
