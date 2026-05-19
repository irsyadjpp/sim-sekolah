package local_context

import (
	"context"
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type LocalContextService interface {
	// Categories
	GetAllCategories() ([]LocalContextCategory, error)
	CreateCategory(ctx context.Context, req CreateCategoryRequest) (*LocalContextCategory, error)

	// Contexts
	GetAll(pagination common.Pagination, search, categoryID, scopeType string) ([]LocalContext, int64, error)
	GetByID(id string) (*LocalContext, error)
	Create(ctx context.Context, req CreateContextRequest) (*LocalContext, error)
	Update(ctx context.Context, id string, req UpdateContextRequest) (*LocalContext, error)
	Delete(ctx context.Context, id string) error
}

type localContextService struct {
	repo LocalContextRepository
}

func NewLocalContextService(repo LocalContextRepository) LocalContextService {
	return &localContextService{repo: repo}
}

func (s *localContextService) GetAllCategories() ([]LocalContextCategory, error) {
	return s.repo.GetAllCategories()
}

func (s *localContextService) CreateCategory(ctx context.Context, req CreateCategoryRequest) (*LocalContextCategory, error) {
	category := &LocalContextCategory{
		CategoryCode: req.CategoryCode,
		CategoryName: req.CategoryName,
		Description:  req.Description,
	}
	if err := s.repo.CreateCategory(ctx, category); err != nil {
		return nil, err
	}
	return category, nil
}

func (s *localContextService) GetAll(pagination common.Pagination, search, categoryID, scopeType string) ([]LocalContext, int64, error) {
	return s.repo.GetAll(pagination.Limit, pagination.Offset, search, categoryID, scopeType)
}

func (s *localContextService) GetByID(id string) (*LocalContext, error) {
	return s.repo.GetByID(id)
}

func (s *localContextService) Create(ctx context.Context, req CreateContextRequest) (*LocalContext, error) {
	categoryUUID, _ := uuid.Parse(req.CategoryID)

	contextEntry := &LocalContext{
		CategoryID:  categoryUUID,
		Title:       req.Title,
		Description: req.Description,
		Location:    req.Location,
		ScopeType:   req.ScopeType,
	}

	if req.IsActive != nil {
		contextEntry.IsActive = *req.IsActive
	} else {
		contextEntry.IsActive = true
	}

	if err := s.repo.Create(ctx, contextEntry); err != nil {
		return nil, err
	}
	return contextEntry, nil
}

func (s *localContextService) Update(ctx context.Context, id string, req UpdateContextRequest) (*LocalContext, error) {
	contextEntry, err := s.repo.GetByID(id)
	if err != nil {
		return nil, err
	}

	if err := common.CheckOwnership(ctx, contextEntry.CreatedBy); err != nil {
		return nil, err
	}

	if req.CategoryID != "" {
		categoryUUID, _ := uuid.Parse(req.CategoryID)
		contextEntry.CategoryID = categoryUUID
	}
	if req.Title != "" {
		contextEntry.Title = req.Title
	}
	contextEntry.Description = req.Description
	if req.Location != "" {
		contextEntry.Location = req.Location
	}
	if req.ScopeType != "" {
		contextEntry.ScopeType = req.ScopeType
	}
	if req.IsActive != nil {
		contextEntry.IsActive = *req.IsActive
	}

	if err := s.repo.Update(ctx, contextEntry); err != nil {
		return nil, err
	}
	return contextEntry, nil
}

func (s *localContextService) Delete(ctx context.Context, id string) error {
	contextEntry, err := s.repo.GetByID(id)
	if err != nil {
		return err
	}

	if err := common.CheckOwnership(ctx, contextEntry.CreatedBy); err != nil {
		return err
	}

	return s.repo.Delete(ctx, id)
}
