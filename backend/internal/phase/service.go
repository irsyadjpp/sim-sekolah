package phase

import (
	"context"
	"errors"
	"strings"

	"sim-sekolah/internal/common"
)

// PhaseService mendefinisikan business logic untuk entitas Phase.
type PhaseService interface {
	GetAll(pagination common.Pagination, search string) ([]Phase, int64, error)
	GetByID(id string) (*Phase, error)
	Create(ctx context.Context, req CreatePhaseRequest) (*Phase, error)
	Update(ctx context.Context, id string, req UpdatePhaseRequest) (*Phase, error)
	Delete(ctx context.Context, id string) error
	ValidateSDPhase(phaseCode string) error
}

type phaseService struct {
	repo PhaseRepository
}

// NewPhaseService membuat instance PhaseService baru dengan injected PhaseRepository.
func NewPhaseService(repo PhaseRepository) PhaseService {
	return &phaseService{repo: repo}
}

func (s *phaseService) GetAll(pagination common.Pagination, search string) ([]Phase, int64, error) {
	return s.repo.GetAll(pagination.Limit, pagination.Offset, search)
}

func (s *phaseService) GetByID(id string) (*Phase, error) {
	return s.repo.GetByID(id)
}

func (s *phaseService) Create(ctx context.Context, req CreatePhaseRequest) (*Phase, error) {
	// Validate that the phase is SD-only
	if err := s.ValidateSDPhase(req.Code); err != nil {
		return nil, err
	}

	p := &Phase{
		Code:        req.Code,
		Name:        req.Name,
		Description: req.Description,
	}

	if err := s.repo.Create(ctx, p); err != nil {
		return nil, err
	}

	return p, nil
}

func (s *phaseService) Update(ctx context.Context, id string, req UpdatePhaseRequest) (*Phase, error) {
	p, err := s.repo.GetByID(id)
	if err != nil {
		return nil, err
	}

	if err := common.CheckOwnership(ctx, p.CreatedBy); err != nil {
		return nil, err
	}

	if req.Code != "" {
		// Validate that the new phase code is SD-only
		if err := s.ValidateSDPhase(req.Code); err != nil {
			return nil, err
		}
		p.Code = req.Code
	}
	if req.Name != "" {
		p.Name = req.Name
	}
	p.Description = req.Description

	if err := s.repo.Update(ctx, p); err != nil {
		return nil, err
	}

	return p, nil
}

func (s *phaseService) Delete(ctx context.Context, id string) error {
	p, err := s.repo.GetByID(id)
	if err != nil {
		return err
	}

	if err := common.CheckOwnership(ctx, p.CreatedBy); err != nil {
		return err
	}

	return s.repo.Delete(ctx, id)
}

// ValidateSDPhase validates that a phase code is valid for Sekolah Dasar (SD)
// Only Fase A, B, C are valid for SD (Kelas 1-6)
func (s *phaseService) ValidateSDPhase(phaseCode string) error {
	// Normalize phase code to uppercase for comparison
	normalizedCode := strings.ToUpper(strings.TrimSpace(phaseCode))

	// Define valid SD phases
	validSDPhases := map[string]bool{
		"FAS-A": true,
		"FAS-B": true,
		"FAS-C": true,
		"A":     true, // Alternative short codes
		"B":     true,
		"C":     true,
	}

	if !validSDPhases[normalizedCode] {
		return errors.New("fase ini tidak relevan untuk Sekolah Dasar. Hanya Fase A (Kelas 1-2), Fase B (Kelas 3-4), dan Fase C (Kelas 5-6) yang diperbolehkan")
	}

	return nil
}
