package enrollment

import (
	"context"

	"gorm.io/gorm"
)

type EnrollmentRepository interface {
	GetByClassroom(ctx context.Context, classroomID string) ([]Enrollment, error)
	GetByID(ctx context.Context, id string) (*Enrollment, error)
	IsEnrolled(ctx context.Context, classroomID, studentID string) (bool, error)
	Create(ctx context.Context, data *Enrollment) error
	Delete(ctx context.Context, id string) error
	CountByClassroom(ctx context.Context, classroomID string) (int64, error)
}

type enrollmentRepository struct {
	db *gorm.DB
}

func NewEnrollmentRepository(db *gorm.DB) EnrollmentRepository {
	return &enrollmentRepository{db: db}
}

func (r *enrollmentRepository) GetByClassroom(ctx context.Context, classroomID string) ([]Enrollment, error) {
	var enrollments []Enrollment
	err := r.db.WithContext(ctx).
		Preload("Student").
		Where("classroom_id = ?", classroomID).
		Order("enrollment_date ASC").
		Find(&enrollments).Error
	return enrollments, err
}

func (r *enrollmentRepository) GetByID(ctx context.Context, id string) (*Enrollment, error) {
	var e Enrollment
	err := r.db.WithContext(ctx).Preload("Student").First(&e, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return &e, nil
}

func (r *enrollmentRepository) IsEnrolled(ctx context.Context, classroomID, studentID string) (bool, error) {
	var count int64
	err := r.db.WithContext(ctx).Model(&Enrollment{}).
		Where("classroom_id = ? AND student_id = ?", classroomID, studentID).
		Count(&count).Error
	return count > 0, err
}

func (r *enrollmentRepository) Create(ctx context.Context, data *Enrollment) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *enrollmentRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&Enrollment{}, "id = ?", id).Error
}

func (r *enrollmentRepository) CountByClassroom(ctx context.Context, classroomID string) (int64, error) {
	var count int64
	err := r.db.WithContext(ctx).Model(&Enrollment{}).Where("classroom_id = ?", classroomID).Count(&count).Error
	return count, err
}
