package learning_principle

import (
	"context"
	"errors"
	"strings"

	"sim-sekolah/internal/common"
)

// LearningPrincipleService defines the business logic for LearningPrinciple entities
type LearningPrincipleService interface {
	GetAll(pagination common.Pagination, search string) ([]LearningPrinciple, int64, error)
	GetByID(id string) (*LearningPrinciple, error)
	GetByCode(code string) (*LearningPrinciple, error)
	Create(ctx context.Context, req CreateLearningPrincipleRequest) (*LearningPrinciple, error)
	Update(ctx context.Context, id string, req UpdateLearningPrincipleRequest) (*LearningPrinciple, error)
	Delete(ctx context.Context, id string) error
	ValidateStandardPrincipleCode(code string) error
}

type learningPrincipleService struct {
	repo LearningPrincipleRepository
}

// NewLearningPrincipleService creates a new LearningPrincipleService with injected LearningPrincipleRepository
func NewLearningPrincipleService(repo LearningPrincipleRepository) LearningPrincipleService {
	return &learningPrincipleService{repo: repo}
}

func (s *learningPrincipleService) GetAll(pagination common.Pagination, search string) ([]LearningPrinciple, int64, error) {
	return s.repo.GetAll(pagination.Limit, pagination.Offset, search)
}

func (s *learningPrincipleService) GetByID(id string) (*LearningPrinciple, error) {
	return s.repo.GetByID(id)
}

func (s *learningPrincipleService) GetByCode(code string) (*LearningPrinciple, error) {
	return s.repo.GetByCode(code)
}

func (s *learningPrincipleService) Create(ctx context.Context, req CreateLearningPrincipleRequest) (*LearningPrinciple, error) {
	// Validate that the principle code is one of the standard 3 learning principles
	if err := s.ValidateStandardPrincipleCode(req.PrincipleCode); err != nil {
		return nil, err
	}

	principle := &LearningPrinciple{
		PrincipleCode:          req.PrincipleCode,
		PrincipleName:          req.PrincipleName,
		Description:            req.Description,
		KeyCharacteristics:     req.KeyCharacteristics,
		ImplementationExamples: req.ImplementationExamples,
		IsActive:               true,
	}

	if err := s.repo.Create(ctx, principle); err != nil {
		return nil, err
	}

	return principle, nil
}

func (s *learningPrincipleService) Update(ctx context.Context, id string, req UpdateLearningPrincipleRequest) (*LearningPrinciple, error) {
	principle, err := s.repo.GetByID(id)
	if err != nil {
		return nil, err
	}

	if err := common.CheckOwnership(ctx, principle.CreatedBy); err != nil {
		return nil, err
	}

	if req.PrincipleCode != "" {
		// Validate that the new principle code is one of the standard 3 learning principles
		if err := s.ValidateStandardPrincipleCode(req.PrincipleCode); err != nil {
			return nil, err
		}
		principle.PrincipleCode = req.PrincipleCode
	}
	if req.PrincipleName != "" {
		principle.PrincipleName = req.PrincipleName
	}
	if req.Description != "" {
		principle.Description = req.Description
	}
	if req.KeyCharacteristics != "" {
		principle.KeyCharacteristics = req.KeyCharacteristics
	}
	if req.ImplementationExamples != "" {
		principle.ImplementationExamples = req.ImplementationExamples
	}
	if req.IsActive != nil {
		principle.IsActive = *req.IsActive
	}

	if err := s.repo.Update(ctx, principle); err != nil {
		return nil, err
	}

	return principle, nil
}

func (s *learningPrincipleService) Delete(ctx context.Context, id string) error {
	principle, err := s.repo.GetByID(id)
	if err != nil {
		return err
	}

	if err := common.CheckOwnership(ctx, principle.CreatedBy); err != nil {
		return err
	}

	return s.repo.Delete(ctx, id)
}

// ValidateStandardPrincipleCode validates that the principle code is one of the 3 standard learning principles
// from the Deep Learning framework
func (s *learningPrincipleService) ValidateStandardPrincipleCode(code string) error {
	// Normalize code to uppercase for comparison
	normalizedCode := strings.ToUpper(strings.TrimSpace(code))

	// Define valid learning principle codes
	validPrincipleCodes := map[string]bool{
		PrincipleCodeBerkesadaran:   true,
		PrincipleCodeBermakna:       true,
		PrincipleCodeMenggembirakan: true,
	}

	if !validPrincipleCodes[normalizedCode] {
		return errors.New("kode prinsip pembelajaran tidak valid. Hanya 3 prinsip pembelajaran yang diperbolehkan: BERKESADARAN, BERMAKNA, MENGENGIRAKAN")
	}

	return nil
}
