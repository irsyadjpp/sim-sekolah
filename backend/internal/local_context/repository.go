package local_context

import (
	"context"

	"gorm.io/gorm"
)

type LocalContextRepository interface {
	// Categories
	GetAllCategories() ([]LocalContextCategory, error)
	GetCategoryByID(id string) (*LocalContextCategory, error)
	CreateCategory(ctx context.Context, category *LocalContextCategory) error

	// Contexts
	GetAll(limit, offset int, search, categoryID, scopeType string) ([]LocalContext, int64, error)
	GetByID(id string) (*LocalContext, error)
	Create(ctx context.Context, context *LocalContext) error
	Update(ctx context.Context, context *LocalContext) error
	Delete(ctx context.Context, id string) error
}

type localContextRepository struct {
	db *gorm.DB
}

func NewLocalContextRepository(db *gorm.DB) LocalContextRepository {
	return &localContextRepository{db: db}
}

func (r *localContextRepository) GetAllCategories() ([]LocalContextCategory, error) {
	var categories []LocalContextCategory
	err := r.db.Find(&categories).Error
	return categories, err
}

func (r *localContextRepository) GetCategoryByID(id string) (*LocalContextCategory, error) {
	var category LocalContextCategory
	err := r.db.First(&category, "id = ?", id).Error
	return &category, err
}

func (r *localContextRepository) CreateCategory(ctx context.Context, category *LocalContextCategory) error {
	return r.db.WithContext(ctx).Create(category).Error
}

func (r *localContextRepository) GetAll(limit, offset int, search, categoryID, scopeType string) ([]LocalContext, int64, error) {
	var contexts []LocalContext
	var total int64

	query := r.db.Model(&LocalContext{}).Preload("Category")

	if search != "" {
		query = query.Where("title ILIKE ? OR description ILIKE ?", "%"+search+"%", "%"+search+"%")
	}
	if categoryID != "" {
		query = query.Where("category_id = ?", categoryID)
	}
	if scopeType != "" {
		query = query.Where("scope_type = ?", scopeType)
	}

	err := query.Count(&total).Limit(limit).Offset(offset).Find(&contexts).Error
	return contexts, total, err
}

func (r *localContextRepository) GetByID(id string) (*LocalContext, error) {
	var context LocalContext
	err := r.db.Preload("Category").First(&context, "id = ?", id).Error
	return &context, err
}

func (r *localContextRepository) Create(ctx context.Context, context *LocalContext) error {
	return r.db.WithContext(ctx).Create(context).Error
}

func (r *localContextRepository) Update(ctx context.Context, context *LocalContext) error {
	return r.db.WithContext(ctx).Save(context).Error
}

func (r *localContextRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&LocalContext{}, "id = ?", id).Error
}
