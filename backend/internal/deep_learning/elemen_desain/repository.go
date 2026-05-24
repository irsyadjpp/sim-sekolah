package elemen_desain

import (
	"gorm.io/gorm"
)

type Repository interface {
	GetAll() ([]DesignElement, error)
	GetByFrameworkType(frameworkType string) ([]DesignElement, error)
	GetByID(id string) (*DesignElement, error)
	Create(element *DesignElement) error
	Update(element *DesignElement) error
	Delete(id string) error
	Seed() error
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

func (r *repository) GetAll() ([]DesignElement, error) {
	var results []DesignElement
	err := r.db.Where("deleted_at IS NULL").Order("framework_element_type ASC, design_element_name ASC").Find(&results).Error
	return results, err
}

func (r *repository) GetByFrameworkType(frameworkType string) ([]DesignElement, error) {
	var results []DesignElement
	err := r.db.Where("deleted_at IS NULL AND framework_element_type = ?", frameworkType).
		Order("design_element_name ASC").
		Find(&results).Error
	return results, err
}

func (r *repository) GetByID(id string) (*DesignElement, error) {
	var element DesignElement
	err := r.db.Where("id = ? AND deleted_at IS NULL", id).First(&element).Error
	if err != nil {
		return nil, err
	}
	return &element, nil
}

func (r *repository) Create(element *DesignElement) error {
	return r.db.Create(element).Error
}

func (r *repository) Update(element *DesignElement) error {
	return r.db.Save(element).Error
}

func (r *repository) Delete(id string) error {
	return r.db.Where("id = ?", id).Delete(&DesignElement{}).Error
}

func (r *repository) Seed() error {
	elements := GetStandardFrameworkElements()
	for _, element := range elements {
		var count int64
		r.db.Model(&DesignElement{}).
			Where("design_element_name = ?", element.Name).
			Count(&count)
		if count == 0 {
			r.db.Create(&element)
		}
	}
	return nil
}
