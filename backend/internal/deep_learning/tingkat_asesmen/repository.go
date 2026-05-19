package tingkat_asesmen

import (
	"context"
	"gorm.io/gorm"
)

type Repository interface {
	GetAll() ([]AssessmentLevel, error)
	Seed(ctx context.Context) error
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

func (r *repository) GetAll() ([]AssessmentLevel, error) {
	var results []AssessmentLevel
	err := r.db.Order("level_code ASC").Find(&results).Error
	return results, err
}

func (r *repository) Seed(ctx context.Context) error {
	seeds := []struct {
		Code        string
		Description string
		PISA        string
	}{
		{"LOTS", "Lower Order Thinking Skills", "Level 1-3"},
		{"HOTS", "Higher Order Thinking Skills", "Level 4-6"},
	}
	for _, s := range seeds {
		var count int64
		r.db.Model(&AssessmentLevel{}).Where("level_code = ?", s.Code).Count(&count)
		if count == 0 {
			r.db.Create(&AssessmentLevel{
				LevelCode:   s.Code,
				Description: s.Description,
				PISALevel:   s.PISA,
			})
		}
	}
	return nil
}
