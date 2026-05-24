package olah_aspect

import (
	"context"
	"errors"
	"strings"

	"sim-sekolah/internal/common"
)

// OlahAspectService defines the business logic for OlahAspect entities
type OlahAspectService interface {
	GetAll(pagination common.Pagination, search string) ([]OlahAspect, int64, error)
	GetByID(id string) (*OlahAspect, error)
	GetByCode(code string) (*OlahAspect, error)
	Create(ctx context.Context, req CreateOlahAspectRequest) (*OlahAspect, error)
	Update(ctx context.Context, id string, req UpdateOlahAspectRequest) (*OlahAspect, error)
	Delete(ctx context.Context, id string) error
	ValidateStandardAspectCode(code string) error
}

type olahAspectService struct {
	repo OlahAspectRepository
}

// NewOlahAspectService creates a new OlahAspectService with injected OlahAspectRepository
func NewOlahAspectService(repo OlahAspectRepository) OlahAspectService {
	return &olahAspectService{repo: repo}
}

func (s *olahAspectService) GetAll(pagination common.Pagination, search string) ([]OlahAspect, int64, error) {
	return s.repo.GetAll(pagination.Limit, pagination.Offset, search)
}

func (s *olahAspectService) GetByID(id string) (*OlahAspect, error) {
	return s.repo.GetByID(id)
}

func (s *olahAspectService) GetByCode(code string) (*OlahAspect, error) {
	return s.repo.GetByCode(code)
}

func (s *olahAspectService) Create(ctx context.Context, req CreateOlahAspectRequest) (*OlahAspect, error) {
	// Validate that the aspect code is one of the standard 4 olah aspects
	if err := s.ValidateStandardAspectCode(req.AspectCode); err != nil {
		return nil, err
	}

	aspect := &OlahAspect{
		AspectCode: req.AspectCode,
		AspectName: req.AspectName,
		Definition: req.Definition,
		Indicators: req.Indicators,
		IsActive:   true,
	}

	if err := s.repo.Create(ctx, aspect); err != nil {
		return nil, err
	}

	return aspect, nil
}

func (s *olahAspectService) Update(ctx context.Context, id string, req UpdateOlahAspectRequest) (*OlahAspect, error) {
	aspect, err := s.repo.GetByID(id)
	if err != nil {
		return nil, err
	}

	if err := common.CheckOwnership(ctx, aspect.CreatedBy); err != nil {
		return nil, err
	}

	if req.AspectCode != "" {
		// Validate that the new aspect code is one of the standard 4 olah aspects
		if err := s.ValidateStandardAspectCode(req.AspectCode); err != nil {
			return nil, err
		}
		aspect.AspectCode = req.AspectCode
	}
	if req.AspectName != "" {
		aspect.AspectName = req.AspectName
	}
	if req.Definition != "" {
		aspect.Definition = req.Definition
	}
	if req.Indicators != "" {
		aspect.Indicators = req.Indicators
	}
	if req.IsActive != nil {
		aspect.IsActive = *req.IsActive
	}

	if err := s.repo.Update(ctx, aspect); err != nil {
		return nil, err
	}

	return aspect, nil
}

func (s *olahAspectService) Delete(ctx context.Context, id string) error {
	aspect, err := s.repo.GetByID(id)
	if err != nil {
		return err
	}

	if err := common.CheckOwnership(ctx, aspect.CreatedBy); err != nil {
		return err
	}

	return s.repo.Delete(ctx, id)
}

// ValidateStandardAspectCode validates that the aspect code is one of the 4 standard olah aspects
// from the Deep Learning framework
func (s *olahAspectService) ValidateStandardAspectCode(code string) error {
	// Normalize code to uppercase for comparison
	normalizedCode := strings.ToUpper(strings.TrimSpace(code))

	// Define valid olah aspect codes
	validAspectCodes := map[string]bool{
		AspectCodeOlahPikir: true,
		AspectCodeOlahHati:  true,
		AspectCodeOlahRasa:  true,
		AspectCodeOlahRaga:  true,
	}

	if !validAspectCodes[normalizedCode] {
		return errors.New("kode aspek olah tidak valid. Hanya 4 aspek olah yang diperbolehkan: OLAH_PIKIR, OLAH_HATI, OLAH_RASA, OLAH_RAGA")
	}

	return nil
}
