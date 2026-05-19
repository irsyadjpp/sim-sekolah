package school

import (
	"context"
	"errors"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type SchoolService interface {
	GetAll(ctx context.Context, pagination common.Pagination, search string) ([]School, int64, error)
	GetByID(ctx context.Context, id string) (*School, error)
	Create(ctx context.Context, req CreateSchoolRequest) (*School, error)
	Update(ctx context.Context, id string, req UpdateSchoolRequest) (*School, error)
	Delete(ctx context.Context, id string) error
}

type schoolService struct {
	repo SchoolRepository
}

// NewSchoolService creates a new SchoolService with an injected SchoolRepository.
func NewSchoolService(repo SchoolRepository) SchoolService {
	return &schoolService{repo: repo}
}

func (s *schoolService) GetAll(ctx context.Context, pagination common.Pagination, search string) ([]School, int64, error) {
	return s.repo.GetAll(ctx, pagination.Limit, pagination.Offset, search)
}

func (s *schoolService) GetByID(ctx context.Context, id string) (*School, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *schoolService) Create(ctx context.Context, req CreateSchoolRequest) (*School, error) {
	school := &School{
		ID:                  uuid.New(),
		NPSN:                req.NPSN,
		SchoolName:          req.SchoolName,
		Address:             req.Address,
		Phone:               req.Phone,
		Email:               req.Email,
		ElectricityCapacity: req.ElectricityCapacity,
		SignalStatus:        req.SignalStatus,
		Vision:              req.Vision,
		Mission:             req.Mission,
		EducationForm:       req.EducationForm,
		Country:             req.Country,
		TotalStaff:          req.TotalStaff,
		LabCount:            req.LabCount,
		RombelCount:         req.RombelCount,
		SyncSystem:          req.SyncSystem,
		SyncCompliance:      req.SyncCompliance,
	}
	if err := s.repo.Create(ctx, school); err != nil {
		return nil, err
	}

	// Trigger RAG embedding
	TriggerContextEmbedding(school)

	return school, nil
}

func (s *schoolService) Update(ctx context.Context, id string, req UpdateSchoolRequest) (*School, error) {
	school, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("sekolah tidak ditemukan")
	}

	if req.NPSN != "" {
		school.NPSN = req.NPSN
	}
	if req.SchoolName != "" {
		school.SchoolName = req.SchoolName
	}
	if req.Address != "" {
		school.Address = req.Address
	}
	if req.Phone != "" {
		school.Phone = req.Phone
	}
	if req.Email != "" {
		school.Email = req.Email
	}
	if req.ElectricityCapacity != 0 {
		school.ElectricityCapacity = req.ElectricityCapacity
	}
	if req.SignalStatus != "" {
		school.SignalStatus = req.SignalStatus
	}
	if req.Vision != "" {
		school.Vision = req.Vision
	}
	if req.Mission != "" {
		school.Mission = req.Mission
	}
	if req.EducationForm != "" {
		school.EducationForm = req.EducationForm
	}
	if req.Country != "" {
		school.Country = req.Country
	}
	if req.TotalStaff != 0 {
		school.TotalStaff = req.TotalStaff
	}
	if req.LabCount != 0 {
		school.LabCount = req.LabCount
	}
	if req.RombelCount != 0 {
		school.RombelCount = req.RombelCount
	}
	if req.SyncSystem != "" {
		school.SyncSystem = req.SyncSystem
	}
	if req.SyncCompliance != "" {
		school.SyncCompliance = req.SyncCompliance
	}

	if err := s.repo.Update(ctx, school); err != nil {
		return nil, err
	}

	// Trigger RAG embedding
	TriggerContextEmbedding(school)

	return school, nil
}

func (s *schoolService) Delete(ctx context.Context, id string) error {
	if _, err := s.repo.GetByID(ctx, id); err != nil {
		return errors.New("sekolah tidak ditemukan")
	}
	return s.repo.Delete(ctx, id)
}
