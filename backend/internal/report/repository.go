package report

import (
	"context"

	"gorm.io/gorm"
	"gorm.io/gorm/clause"
)

type ReportRepository interface {
	GetByClassroomAndSemester(ctx context.Context, classroomID, semester string) ([]Report, error)
	GetByID(ctx context.Context, id string) (*Report, error)
	Create(ctx context.Context, report *Report) error
	Update(ctx context.Context, report *Report) error

	// Upserts for nested data
	UpsertScore(ctx context.Context, score *ReportScore) error
	UpsertP5(ctx context.Context, p5 *ReportP5) error
	UpsertDeepLearning(ctx context.Context, dl *ReportDeepLearning) error
	UpsertExtracurricular(ctx context.Context, extra *ReportExtracurricular) error
	UpsertAttendance(ctx context.Context, attendance *ReportAttendance) error

	// Deletes for nested data
	DeleteP5(ctx context.Context, id string) error
	DeleteDeepLearning(ctx context.Context, id string) error
	DeleteExtracurricular(ctx context.Context, id string) error
}

type reportRepository struct {
	db *gorm.DB
}

func NewReportRepository(db *gorm.DB) ReportRepository {
	return &reportRepository{db: db}
}

func (r *reportRepository) GetByClassroomAndSemester(ctx context.Context, classroomID, semester string) ([]Report, error) {
	var reports []Report
	err := r.db.WithContext(ctx).
		Preload("Student").
		Where("classroom_id = ? AND semester = ?", classroomID, semester).
		Find(&reports).Error
	return reports, err
}

func (r *reportRepository) GetByID(ctx context.Context, id string) (*Report, error) {
	var rep Report
	err := r.db.WithContext(ctx).
		Preload("Student").
		Preload("Classroom").
		Preload("Scores.Subject"). // Preload mapel di dalam scores
		Preload("P5").
		Preload("DeepLearning").
		Preload("Extracurricular").
		Preload("Attendance").
		First(&rep, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return &rep, nil
}

func (r *reportRepository) Create(ctx context.Context, report *Report) error {
	// Gunakan ON CONFLICT DO NOTHING agar jika admin panggil generate berulang kali tidak error
	return r.db.WithContext(ctx).Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "classroom_id"}, {Name: "student_id"}, {Name: "semester"}},
		DoNothing: true,
	}).Create(report).Error
}

func (r *reportRepository) Update(ctx context.Context, report *Report) error {
	return r.db.WithContext(ctx).Save(report).Error
}

func (r *reportRepository) UpsertScore(ctx context.Context, score *ReportScore) error {
	return r.db.WithContext(ctx).Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "report_id"}, {Name: "subject_id"}},
		DoUpdates: clause.AssignmentColumns([]string{"final_score", "competency_achieved", "competency_needs_improvement"}),
	}).Create(score).Error
}

func (r *reportRepository) UpsertP5(ctx context.Context, p5 *ReportP5) error {
	return r.db.WithContext(ctx).Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "report_id"}, {Name: "theme"}},
		DoUpdates: clause.AssignmentColumns([]string{"description", "predicate"}),
	}).Create(p5).Error
}

func (r *reportRepository) UpsertDeepLearning(ctx context.Context, dl *ReportDeepLearning) error {
	return r.db.WithContext(ctx).Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "report_id"}, {Name: "aspect"}},
		DoUpdates: clause.AssignmentColumns([]string{"observation_notes"}),
	}).Create(dl).Error
}

func (r *reportRepository) UpsertExtracurricular(ctx context.Context, extra *ReportExtracurricular) error {
	return r.db.WithContext(ctx).Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "report_id"}, {Name: "activity_name"}},
		DoUpdates: clause.AssignmentColumns([]string{"predicate", "description"}),
	}).Create(extra).Error
}

func (r *reportRepository) UpsertAttendance(ctx context.Context, att *ReportAttendance) error {
	return r.db.WithContext(ctx).Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "report_id"}},
		DoUpdates: clause.AssignmentColumns([]string{"sick", "permission", "unexcused"}),
	}).Create(att).Error
}

func (r *reportRepository) DeleteP5(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&ReportP5{}, "id = ?", id).Error
}
func (r *reportRepository) DeleteDeepLearning(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&ReportDeepLearning{}, "id = ?", id).Error
}
func (r *reportRepository) DeleteExtracurricular(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&ReportExtracurricular{}, "id = ?", id).Error
}
