package elemen_desain

import (
	"context"
	"gorm.io/gorm"
)

type Repository interface {
	GetAll() ([]DesignElement, error)
	Seed(ctx context.Context) error
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

func (r *repository) GetAll() ([]DesignElement, error) {
	var results []DesignElement
	err := r.db.Order("design_element_name ASC").Find(&results).Error
	return results, err
}

func (r *repository) Seed(ctx context.Context) error {
	seeds := []string{"Praktik Pedagogis", "Lingkungan Pembelajaran", "Pemanfaatan Digital", "Kemitraan Pembelajaran"}
	for _, name := range seeds {
		var count int64
		r.db.Model(&DesignElement{}).Where("design_element_name = ?", name).Count(&count)
		if count == 0 {
			r.db.Create(&DesignElement{Name: name})
		}
	}
	return nil
}
