package schedule

import (
	"context"
	"errors"

	"github.com/google/uuid"
)

type CreateScheduleRequest struct {
	ClassroomID          uuid.UUID `json:"classroom_id" validate:"required"`
	TeachingAssignmentID uuid.UUID `json:"teaching_assignment_id" validate:"required"`
	DayOfWeek            int       `json:"day_of_week" validate:"required,min=1,max=7"`
	StartTime            string    `json:"start_time" validate:"required"`
	EndTime              string    `json:"end_time" validate:"required"`
}

type ScheduleService interface {
	GetByClassroom(ctx context.Context, classroomID string) ([]ClassSchedule, error)
	GetByTeacher(ctx context.Context, teacherID string) ([]ClassSchedule, error)
	Create(ctx context.Context, req CreateScheduleRequest) (*ClassSchedule, error)
	Delete(ctx context.Context, id string) error
}

type scheduleService struct {
	repo ScheduleRepository
}

func NewScheduleService(repo ScheduleRepository) ScheduleService {
	return &scheduleService{repo: repo}
}

func (s *scheduleService) GetByClassroom(ctx context.Context, classroomID string) ([]ClassSchedule, error) {
	if classroomID == "" {
		return nil, errors.New("classroom ID is required")
	}
	return s.repo.GetByClassroom(ctx, classroomID)
}

func (s *scheduleService) GetByTeacher(ctx context.Context, teacherID string) ([]ClassSchedule, error) {
	if teacherID == "" {
		return nil, errors.New("teacher ID is required")
	}
	return s.repo.GetByTeacher(ctx, teacherID)
}

func (s *scheduleService) Create(ctx context.Context, req CreateScheduleRequest) (*ClassSchedule, error) {
	schedule := &ClassSchedule{
		ClassroomID:          req.ClassroomID,
		TeachingAssignmentID: req.TeachingAssignmentID,
		DayOfWeek:            req.DayOfWeek,
		StartTime:            req.StartTime,
		EndTime:              req.EndTime,
	}

	if err := s.repo.Create(ctx, schedule); err != nil {
		return nil, err
	}
	return schedule, nil
}

func (s *scheduleService) Delete(ctx context.Context, id string) error {
	return s.repo.Delete(ctx, id)
}
