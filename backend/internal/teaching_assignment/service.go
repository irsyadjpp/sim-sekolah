package teaching_assignment

import (
	"context"
	"errors"

	"github.com/google/uuid"
)

type TeachingAssignmentService interface {
	GetByClassroom(ctx context.Context, classroomID string) ([]TeachingAssignment, error)
	GetByID(ctx context.Context, id string) (*TeachingAssignment, error)
	Create(ctx context.Context, req CreateTeachingAssignmentRequest) (*TeachingAssignment, error)
	Update(ctx context.Context, id string, req UpdateTeachingAssignmentRequest) (*TeachingAssignment, error)
	Delete(ctx context.Context, id string) error
}

type teachingAssignmentService struct {
	repo TeachingAssignmentRepository
}

func NewTeachingAssignmentService(repo TeachingAssignmentRepository) TeachingAssignmentService {
	return &teachingAssignmentService{repo: repo}
}

func (s *teachingAssignmentService) GetByClassroom(ctx context.Context, classroomID string) ([]TeachingAssignment, error) {
	return s.repo.GetByClassroom(ctx, classroomID)
}

func (s *teachingAssignmentService) GetByID(ctx context.Context, id string) (*TeachingAssignment, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *teachingAssignmentService) Create(ctx context.Context, req CreateTeachingAssignmentRequest) (*TeachingAssignment, error) {
	classUUID, _ := uuid.Parse(req.ClassroomID)
	teacherUUID, _ := uuid.Parse(req.TeacherID)
	subjectUUID, _ := uuid.Parse(req.SubjectID)

	a := &TeachingAssignment{
		ID:          uuid.New(),
		ClassroomID: classUUID,
		TeacherID:   teacherUUID,
		SubjectID:   subjectUUID,
	}

	if err := s.repo.Create(ctx, a); err != nil {
		return nil, err
	}
	return a, nil
}

func (s *teachingAssignmentService) Update(ctx context.Context, id string, req UpdateTeachingAssignmentRequest) (*TeachingAssignment, error) {
	a, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("penugasan tidak ditemukan")
	}

	if req.TeacherID != "" {
		tid, _ := uuid.Parse(req.TeacherID)
		a.TeacherID = tid
	}
	if req.SubjectID != "" {
		sid, _ := uuid.Parse(req.SubjectID)
		a.SubjectID = sid
	}

	if err := s.repo.Update(ctx, a); err != nil {
		return nil, err
	}
	return a, nil
}

func (s *teachingAssignmentService) Delete(ctx context.Context, id string) error {
	if _, err := s.repo.GetByID(ctx, id); err != nil {
		return errors.New("penugasan tidak ditemukan")
	}
	return s.repo.Delete(ctx, id)
}
