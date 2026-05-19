package tahapan_kognitif

import (
	"context"
	"gorm.io/gorm"
)

type Repository interface {
	GetAll() ([]CognitiveStage, error)
	Seed(ctx context.Context) error
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

func (r *repository) GetAll() ([]CognitiveStage, error) {
	var results []CognitiveStage
	err := r.db.Order("stage_order ASC").Find(&results).Error
	return results, err
}

func (r *repository) Seed(ctx context.Context) error {
	seeds := []struct {
		Order int
		Name  string
	}{
		{1, "Understand"},
		{2, "Apply"},
		{3, "Reflect"},
	}
	for _, s := range seeds {
		var count int64
		r.db.Model(&CognitiveStage{}).Where("stage_name = ?", s.Name).Count(&count)
		if count == 0 {
			r.db.Create(&CognitiveStage{Order: s.Order, Name: s.Name})
		}
	}
	return nil
}
