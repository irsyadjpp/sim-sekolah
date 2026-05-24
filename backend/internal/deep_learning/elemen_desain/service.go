package elemen_desain

import (
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"
)

type Service interface {
	GetAll() ([]DesignElementResponse, error)
	GetByFrameworkType(frameworkType string) ([]DesignElementResponse, error)
	GetByID(id string) (*DesignElementResponse, error)
	Create(req CreateDesignElementRequest) (*DesignElementResponse, error)
	Update(id string, req UpdateDesignElementRequest) (*DesignElementResponse, error)
	Delete(id string) error
	GetFrameworkGroups() ([]FrameworkGroupResponse, error)
}

type service struct {
	repo Repository
}

func NewService(repo Repository) Service {
	return &service{repo: repo}
}

func (s *service) GetAll() ([]DesignElementResponse, error) {
	elements, err := s.repo.GetAll()
	if err != nil {
		return nil, fmt.Errorf("failed to get design elements: %w", err)
	}

	responses := make([]DesignElementResponse, len(elements))
	for i, element := range elements {
		responses[i] = s.toResponse(&element)
	}
	return responses, nil
}

func (s *service) GetByFrameworkType(frameworkType string) ([]DesignElementResponse, error) {
	if !IsValidFrameworkElementType(frameworkType) {
		return nil, errors.New("invalid framework element type")
	}

	elements, err := s.repo.GetByFrameworkType(frameworkType)
	if err != nil {
		return nil, fmt.Errorf("failed to get design elements by framework type: %w", err)
	}

	responses := make([]DesignElementResponse, len(elements))
	for i, element := range elements {
		responses[i] = s.toResponse(&element)
	}
	return responses, nil
}

func (s *service) GetByID(id string) (*DesignElementResponse, error) {
	element, err := s.repo.GetByID(id)
	if err != nil {
		return nil, fmt.Errorf("failed to get design element: %w", err)
	}
	res := s.toResponse(element)
	return &res, nil
}

func (s *service) Create(req CreateDesignElementRequest) (*DesignElementResponse, error) {
	// Validate framework type
	if !IsValidFrameworkElementType(req.FrameworkElementType) {
		return nil, errors.New("invalid framework element type")
	}

	// Set default values
	isActive := true
	if req.IsActive != nil {
		isActive = *req.IsActive
	}

	element := &DesignElement{
		ID:                   uuid.New(),
		Name:                 req.Name,
		Description:          req.Description,
		FrameworkElementType: req.FrameworkElementType,
		IsActive:             isActive,
	}

	element.CreatedAt = time.Now()
	element.UpdatedAt = time.Now()

	if err := s.repo.Create(element); err != nil {
		return nil, fmt.Errorf("failed to create design element: %w", err)
	}

	res := s.toResponse(element)
	return &res, nil
}

func (s *service) Update(id string, req UpdateDesignElementRequest) (*DesignElementResponse, error) {
	element, err := s.repo.GetByID(id)
	if err != nil {
		return nil, fmt.Errorf("design element not found: %w", err)
	}

	// Update fields if provided
	if req.Name != "" {
		element.Name = req.Name
	}
	if req.Description != "" {
		element.Description = req.Description
	}
	if req.FrameworkElementType != "" {
		if !IsValidFrameworkElementType(req.FrameworkElementType) {
			return nil, errors.New("invalid framework element type")
		}
		element.FrameworkElementType = req.FrameworkElementType
	}
	if req.IsActive != nil {
		element.IsActive = *req.IsActive
	}

	element.UpdatedAt = time.Now()

	if err := s.repo.Update(element); err != nil {
		return nil, fmt.Errorf("failed to update design element: %w", err)
	}

	res := s.toResponse(element)
	return &res, nil
}

func (s *service) Delete(id string) error {
	if err := s.repo.Delete(id); err != nil {
		return fmt.Errorf("failed to delete design element: %w", err)
	}
	return nil
}

func (s *service) GetFrameworkGroups() ([]FrameworkGroupResponse, error) {
	allElements, err := s.repo.GetAll()
	if err != nil {
		return nil, fmt.Errorf("failed to get design elements: %w", err)
	}

	// Group by framework type
	groups := make(map[string][]DesignElement)
	for _, element := range allElements {
		groups[element.FrameworkElementType] = append(groups[element.FrameworkElementType], element)
	}

	// Build response groups
	frameworkTypes := []string{
		FrameworkElementPraktikPedagogis,
		FrameworkElementKemitraanPembelajaran,
		FrameworkElementLingkunganPembelajaran,
		FrameworkElementPemanfaatanDigital,
	}

	responseGroups := make([]FrameworkGroupResponse, 0, len(frameworkTypes))
	for _, fwType := range frameworkTypes {
		elements, exists := groups[fwType]
		if !exists {
			continue
		}

		elementResponses := make([]DesignElementResponse, len(elements))
		for i, element := range elements {
			elementResponses[i] = s.toResponse(&element)
		}

		responseGroups = append(responseGroups, FrameworkGroupResponse{
			FrameworkType: fwType,
			FrameworkName: GetFrameworkElementDescription(fwType),
			Elements:      elementResponses,
			ElementCount:  len(elements),
		})
	}

	return responseGroups, nil
}

func (s *service) toResponse(element *DesignElement) DesignElementResponse {
	return DesignElementResponse{
		ID:                   element.ID.String(),
		Name:                 element.Name,
		Description:          element.Description,
		FrameworkElementType: element.FrameworkElementType,
		IsActive:             element.IsActive,
		CreatedAt:            element.CreatedAt.Format(time.RFC3339),
		UpdatedAt:            element.UpdatedAt.Format(time.RFC3339),
	}
}
