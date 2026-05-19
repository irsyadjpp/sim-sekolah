package grade

import (
	"context"
	"errors"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type GradeService interface {
	GetAll(ctx context.Context, pagination common.Pagination) ([]Grade, int64, error)
	GetByPhaseID(ctx context.Context, phaseID string) ([]Grade, error)
	GetByID(ctx context.Context, id string) (*Grade, error)
	Create(ctx context.Context, req CreateGradeRequest) (*Grade, error)
	Update(ctx context.Context, id string, req UpdateGradeRequest) (*Grade, error)
	Delete(ctx context.Context, id string) error
}

type gradeService struct {
	repo GradeRepository
}

func NewGradeService(repo GradeRepository) GradeService {
	return &gradeService{repo: repo}
}

func (s *gradeService) GetAll(ctx context.Context, pagination common.Pagination) ([]Grade, int64, error) {
	return s.repo.GetAll(ctx, pagination.Limit, pagination.Offset)
}

func (s *gradeService) GetByPhaseID(ctx context.Context, phaseID string) ([]Grade, error) {
	return s.repo.GetByPhaseID(ctx, phaseID)
}

func (s *gradeService) GetByID(ctx context.Context, id string) (*Grade, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *gradeService) Create(ctx context.Context, req CreateGradeRequest) (*Grade, error) {
	phaseUUID, _ := uuid.Parse(req.PhaseID)
	grade := &Grade{
		ID:         uuid.New(),
		PhaseID:    phaseUUID,
		GradeLevel: req.GradeLevel,
		GradeName:  req.GradeName,
	}
	if err := s.repo.Create(ctx, grade); err != nil {
		return nil, err
	}
	return grade, nil
}

func (s *gradeService) Update(ctx context.Context, id string, req UpdateGradeRequest) (*Grade, error) {
	grade, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("kelas tidak ditemukan")
	}

	if req.PhaseID != "" {
		phaseUUID, _ := uuid.Parse(req.PhaseID)
		grade.PhaseID = phaseUUID
	}
	if req.GradeLevel != 0 {
		grade.GradeLevel = req.GradeLevel
	}
	if req.GradeName != "" {
		grade.GradeName = req.GradeName
	}

	if err := s.repo.Update(ctx, grade); err != nil {
		return nil, err
	}
	return grade, nil
}

func (s *gradeService) Delete(ctx context.Context, id string) error {
	if _, err := s.repo.GetByID(ctx, id); err != nil {
		return errors.New("kelas tidak ditemukan")
	}
	return s.repo.Delete(ctx, id)
}
