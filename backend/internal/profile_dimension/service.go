package profile_dimension

import (
	"context"
	"sim-sekolah/internal/common"
)

type ProfileDimensionService interface {
	GetAll(pagination common.Pagination, search string) ([]ProfileDimension, int64, error)
	GetByID(id string) (*ProfileDimension, error)
	Create(ctx context.Context, req CreateProfileDimensionRequest) (*ProfileDimension, error)
	Update(ctx context.Context, id string, req UpdateProfileDimensionRequest) (*ProfileDimension, error)
	Delete(ctx context.Context, id string) error
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
