package profile_dimension

import (
	"context"
	"errors"
	"strings"

	"sim-sekolah/internal/common"
)

type ProfileDimensionService interface {
	GetAll(pagination common.Pagination, search string) ([]ProfileDimension, int64, error)
	GetByID(id string) (*ProfileDimension, error)
	Create(ctx context.Context, req CreateProfileDimensionRequest) (*ProfileDimension, error)
	Update(ctx context.Context, id string, req UpdateProfileDimensionRequest) (*ProfileDimension, error)
	Delete(ctx context.Context, id string) error
	ValidateStandardDimensionCode(code string) error
}

type profileDimensionService struct {
	repo ProfileDimensionRepository
}

func NewProfileDimensionService(repo ProfileDimensionRepository) ProfileDimensionService {
	return &profileDimensionService{repo: repo}
}

func (s *profileDimensionService) GetAll(pagination common.Pagination, search string) ([]ProfileDimension, int64, error) {
	return s.repo.GetAll(pagination.Limit, pagination.Offset, search)
}

func (s *profileDimensionService) GetByID(id string) (*ProfileDimension, error) {
	return s.repo.GetByID(id)
}

func (s *profileDimensionService) Create(ctx context.Context, req CreateProfileDimensionRequest) (*ProfileDimension, error) {
	// Validate that the dimension code is one of the 8 standard dimensions
	if err := s.ValidateStandardDimensionCode(req.DimensionCode); err != nil {
		return nil, err
	}

	d := &ProfileDimension{
		DimensionCode: req.DimensionCode,
		DimensionName: req.DimensionName,
		Description:   req.Description,
	}
	if req.IsActive != nil {
		d.IsActive = *req.IsActive
	} else {
		d.IsActive = true
	}

	if err := s.repo.Create(ctx, d); err != nil {
		return nil, err
	}
	return d, nil
}

func (s *profileDimensionService) Update(ctx context.Context, id string, req UpdateProfileDimensionRequest) (*ProfileDimension, error) {
	d, err := s.repo.GetByID(id)
	if err != nil {
		return nil, err
	}

	if err := common.CheckOwnership(ctx, d.CreatedBy); err != nil {
		return nil, err
	}

	if req.DimensionCode != "" {
		// Validate that the new dimension code is one of the 8 standard dimensions
		if err := s.ValidateStandardDimensionCode(req.DimensionCode); err != nil {
			return nil, err
		}
		d.DimensionCode = req.DimensionCode
	}
	if req.DimensionName != "" {
		d.DimensionName = req.DimensionName
	}
	if req.Description != "" {
		d.Description = req.Description
	}
	if req.IsActive != nil {
		d.IsActive = *req.IsActive
	}

	if err := s.repo.Update(ctx, d); err != nil {
		return nil, err
	}
	return d, nil
}

func (s *profileDimensionService) Delete(ctx context.Context, id string) error {
	d, err := s.repo.GetByID(id)
	if err != nil {
		return err
	}

	if err := common.CheckOwnership(ctx, d.CreatedBy); err != nil {
		return err
	}

	return s.repo.Delete(ctx, id)
}

// ValidateStandardDimensionCode validates that the dimension code is one of the 8 standard profile dimensions
// from the Deep Learning framework
func (s *profileDimensionService) ValidateStandardDimensionCode(code string) error {
	// Normalize code to uppercase for comparison
	normalizedCode := strings.ToUpper(strings.TrimSpace(code))

	// Define valid dimension codes according to Deep Learning framework
	validDimensionCodes := map[string]bool{
		DimensionCodeKeimanan:    true,
		DimensionCodeKewargaan:   true,
		DimensionCodePenalaran:   true,
		DimensionCodeKreativitas: true,
		DimensionCodeKolaborasi:  true,
		DimensionCodeKemandirian: true,
		DimensionCodeKesehatan:   true,
		DimensionCodeKomunikasi:  true,
	}

	if !validDimensionCodes[normalizedCode] {
		return errors.New("kode dimensi profil tidak valid. Hanya 8 dimensi profil lulusan Deep Learning yang diperbolehkan: DIM_KEIMANAN, DIM_KEWARGAAN, DIM_PENALARAN, DIM_KREATIVITAS, DIM_KOLABORASI, DIM_KEMANDIRIAN, DIM_KESEHATAN, DIM_KOMUNIKASI")
	}

	return nil
}
