package teaching_assignment

import (
	"context"

	"gorm.io/gorm"
)

type TeachingAssignmentRepository interface {
	GetByClassroom(ctx context.Context, classroomID string) ([]TeachingAssignment, error)
	GetByID(ctx context.Context, id string) (*TeachingAssignment, error)
	Create(ctx context.Context, data *TeachingAssignment) error
	Update(ctx context.Context, data *TeachingAssignment) error
	Delete(ctx context.Context, id string) error
	IsTeacherAssigned(ctx context.Context, classroomID, subjectID, teacherID string) (bool, error)
}

type teachingAssignmentRepository struct {
	db *gorm.DB
}

func NewTeachingAssignmentRepository(db *gorm.DB) TeachingAssignmentRepository {
	return &teachingAssignmentRepository{db: db}
}

func (r *teachingAssignmentRepository) GetByClassroom(ctx context.Context, classroomID string) ([]TeachingAssignment, error) {
	var assignments []TeachingAssignment
	err := r.db.WithContext(ctx).
		Preload("Teacher").
		Preload("Subject").
		Where("classroom_id = ?", classroomID).
		Find(&assignments).Error
	return assignments, err
}

func (r *teachingAssignmentRepository) GetByID(ctx context.Context, id string) (*TeachingAssignment, error) {
	var a TeachingAssignment
	err := r.db.WithContext(ctx).
		Preload("Teacher").
		Preload("Subject").
		First(&a, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return &a, nil
}

func (r *teachingAssignmentRepository) Create(ctx context.Context, data *TeachingAssignment) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *teachingAssignmentRepository) Update(ctx context.Context, data *TeachingAssignment) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *teachingAssignmentRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&TeachingAssignment{}, "id = ?", id).Error
}

func (r *teachingAssignmentRepository) IsTeacherAssigned(ctx context.Context, classroomID, subjectID, teacherID string) (bool, error) {
	var count int64
	err := r.db.WithContext(ctx).Table("teaching_assignments").
		Where("classroom_id = ? AND subject_id = ? AND teacher_id = ?", classroomID, subjectID, teacherID).
		Count(&count).Error
	return count > 0, err
}
