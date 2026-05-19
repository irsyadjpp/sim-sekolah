package classroom

import (
	"context"
	"errors"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type ClassroomService interface {
	GetAll(ctx context.Context, pagination common.Pagination, schoolID string) ([]Classroom, int64, error)
	GetByID(ctx context.Context, id string) (*Classroom, error)
	Create(ctx context.Context, req CreateClassroomRequest) (*Classroom, error)
	Update(ctx context.Context, id string, req UpdateClassroomRequest) (*Classroom, error)
	Delete(ctx context.Context, id string) error
}

type classroomService struct {
	repo ClassroomRepository
}

func NewClassroomService(repo ClassroomRepository) ClassroomService {
	return &classroomService{repo: repo}
}

func (s *classroomService) GetAll(ctx context.Context, pagination common.Pagination, schoolID string) ([]Classroom, int64, error) {
	return s.repo.GetAll(ctx, pagination.Limit, pagination.Offset, schoolID)
}

func (s *classroomService) GetByID(ctx context.Context, id string) (*Classroom, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *classroomService) Create(ctx context.Context, req CreateClassroomRequest) (*Classroom, error) {
	schoolID, _ := uuid.Parse(req.SchoolID)
	ayID, _ := uuid.Parse(req.AcademicYearID)
	gradeID, _ := uuid.Parse(req.GradeID)
	phaseID, _ := uuid.Parse(req.PhaseID)

	classroom := &Classroom{
		ID:                   uuid.New(),
		SchoolID:             schoolID,
		AcademicYearID:       ayID,
		GradeID:              gradeID,
		PhaseID:              phaseID,
		ClassroomName:        req.ClassroomName,
		MaxQuota:             req.MaxQuota,
		ClassCharacteristics: req.ClassCharacteristics,
	}

	if req.MaxQuota == 0 {
		classroom.MaxQuota = 28 // Default
	}

	if req.HomeroomTeacherID != "" {
		htID, _ := uuid.Parse(req.HomeroomTeacherID)
		classroom.HomeroomTeacherID = &htID
	}

	if err := s.repo.Create(ctx, classroom); err != nil {
		return nil, err
	}
	return classroom, nil
}

func (s *classroomService) Update(ctx context.Context, id string, req UpdateClassroomRequest) (*Classroom, error) {
	classroom, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("kelas tidak ditemukan")
	}

	if req.GradeID != "" {
		classroom.GradeID, _ = uuid.Parse(req.GradeID)
	}
	if req.PhaseID != "" {
		classroom.PhaseID, _ = uuid.Parse(req.PhaseID)
	}
	if req.ClassroomName != "" {
		classroom.ClassroomName = req.ClassroomName
	}
	if req.HomeroomTeacherID != "" {
		htID, _ := uuid.Parse(req.HomeroomTeacherID)
		classroom.HomeroomTeacherID = &htID
	}
	if req.MaxQuota != 0 {
		classroom.MaxQuota = req.MaxQuota
	}
	if req.ClassCharacteristics != "" {
		classroom.ClassCharacteristics = req.ClassCharacteristics
	}

	if err := s.repo.Update(ctx, classroom); err != nil {
		return nil, err
	}
	return classroom, nil
}

func (s *classroomService) Delete(ctx context.Context, id string) error {
	if _, err := s.repo.GetByID(ctx, id); err != nil {
		return errors.New("kelas/rombel tidak ditemukan")
	}
	return s.repo.Delete(ctx, id)
}
