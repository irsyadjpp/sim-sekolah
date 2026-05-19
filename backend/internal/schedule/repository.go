package schedule

import (
	"context"

	"gorm.io/gorm"
)

type ScheduleRepository interface {
	GetByClassroom(ctx context.Context, classroomID string) ([]ClassSchedule, error)
	GetByTeacher(ctx context.Context, teacherID string) ([]ClassSchedule, error)
	Create(ctx context.Context, schedule *ClassSchedule) error
	Delete(ctx context.Context, id string) error
}

type scheduleRepository struct {
	db *gorm.DB
}

func NewScheduleRepository(db *gorm.DB) ScheduleRepository {
	return &scheduleRepository{db: db}
}

func (r *scheduleRepository) GetByClassroom(ctx context.Context, classroomID string) ([]ClassSchedule, error) {
	var schedules []ClassSchedule
	err := r.db.WithContext(ctx).
		Preload("TeachingAssignment").
		Preload("TeachingAssignment.Subject").
		Preload("TeachingAssignment.Teacher").
		Where("classroom_id = ?", classroomID).
		Order("day_of_week ASC, start_time ASC").
		Find(&schedules).Error
	return schedules, err
}

func (r *scheduleRepository) GetByTeacher(ctx context.Context, teacherID string) ([]ClassSchedule, error) {
	var schedules []ClassSchedule
	err := r.db.WithContext(ctx).
		Joins("JOIN trx_teaching_assignment ta ON ta.id = trx_class_schedule.teaching_assignment_id").
		Preload("Classroom").
		Preload("TeachingAssignment").
		Preload("TeachingAssignment.Subject").
		Where("ta.teacher_id = ?", teacherID).
		Order("day_of_week ASC, start_time ASC").
		Find(&schedules).Error
	return schedules, err
}

func (r *scheduleRepository) Create(ctx context.Context, schedule *ClassSchedule) error {
	return r.db.WithContext(ctx).Create(schedule).Error
}

func (r *scheduleRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&ClassSchedule{}, "id = ?", id).Error
}
