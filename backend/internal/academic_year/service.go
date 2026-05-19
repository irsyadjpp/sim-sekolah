package academic_year

import (
	"context"
	"errors"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type AcademicYearService interface {
	GetAll(ctx context.Context, pagination common.Pagination) ([]AcademicYear, int64, error)
	GetByID(ctx context.Context, id string) (*AcademicYear, error)
	Create(ctx context.Context, req CreateAcademicYearRequest) (*AcademicYear, error)
	Update(ctx context.Context, id string, req UpdateAcademicYearRequest) (*AcademicYear, error)
	Delete(ctx context.Context, id string) error
	SetActive(ctx context.Context, id string) error
}

type academicYearService struct {
	repo AcademicYearRepository
}

func NewAcademicYearService(repo AcademicYearRepository) AcademicYearService {
	return &academicYearService{repo: repo}
}

func (s *academicYearService) GetAll(ctx context.Context, pagination common.Pagination) ([]AcademicYear, int64, error) {
	return s.repo.GetAll(ctx, pagination.Limit, pagination.Offset)
}

func (s *academicYearService) GetByID(ctx context.Context, id string) (*AcademicYear, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *academicYearService) Create(ctx context.Context, req CreateAcademicYearRequest) (*AcademicYear, error) {
	year := &AcademicYear{
		ID:       uuid.New(),
		YearName: req.YearName,
		Semester: req.Semester,
		IsActive: req.IsActive,
	}

	// Jika new year diset active, nonaktifkan yang lain dulu
	if req.IsActive {
		if err := s.repo.DeactivateAll(ctx); err != nil {
			return nil, err
		}
	}

	if err := s.repo.Create(ctx, year); err != nil {
		return nil, err
	}
	return year, nil
}

func (s *academicYearService) Update(ctx context.Context, id string, req UpdateAcademicYearRequest) (*AcademicYear, error) {
	year, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("tahun ajaran tidak ditemukan")
	}

	if req.YearName != "" {
		year.YearName = req.YearName
	}
	if req.Semester != "" {
		year.Semester = req.Semester
	}
	if req.IsActive != nil {
		// Jika diset active, nonaktifkan semua yang lain
		if *req.IsActive {
			if err := s.repo.DeactivateAll(ctx); err != nil {
				return nil, err
			}
		}
		year.IsActive = *req.IsActive
	}

	if err := s.repo.Update(ctx, year); err != nil {
		return nil, err
	}
	return year, nil
}

func (s *academicYearService) Delete(ctx context.Context, id string) error {
	if _, err := s.repo.GetByID(ctx, id); err != nil {
		return errors.New("tahun ajaran tidak ditemukan")
	}
	return s.repo.Delete(ctx, id)
}

// SetActive adalah shortcut untuk mengaktifkan satu tahun ajaran sekaligus menonaktifkan semua lainnya
func (s *academicYearService) SetActive(ctx context.Context, id string) error {
	return s.repo.SetActiveTransaction(ctx, id)
}
