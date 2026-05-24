package profile_dimension

import (
	"context"

	"gorm.io/gorm"
)

type ProfileDimensionRepository interface {
	GetAll(limit, offset int, search string) ([]ProfileDimension, int64, error)
	GetByID(id string) (*ProfileDimension, error)
	Create(ctx context.Context, d *ProfileDimension) error
	Update(ctx context.Context, d *ProfileDimension) error
	Delete(ctx context.Context, id string) error
	Seed(ctx context.Context) error
}

type profileDimensionRepository struct {
	db *gorm.DB
}

func NewProfileDimensionRepository(db *gorm.DB) ProfileDimensionRepository {
	return &profileDimensionRepository{db: db}
}

func (r *profileDimensionRepository) GetAll(limit, offset int, search string) ([]ProfileDimension, int64, error) {
	var dimensions []ProfileDimension
	var total int64

	query := r.db.Model(&ProfileDimension{})
	if search != "" {
		query = query.Where("dimension_name ILIKE ?", "%"+search+"%")
	}

	query.Count(&total)
	err := query.Limit(limit).Offset(offset).Order("dimension_name ASC").Find(&dimensions).Error
	return dimensions, total, err
}

func (r *profileDimensionRepository) GetByID(id string) (*ProfileDimension, error) {
	var d ProfileDimension
	err := r.db.First(&d, "id = ?", id).Error
	return &d, err
}

func (r *profileDimensionRepository) Create(ctx context.Context, d *ProfileDimension) error {
	return r.db.WithContext(ctx).Create(d).Error
}

func (r *profileDimensionRepository) Update(ctx context.Context, d *ProfileDimension) error {
	return r.db.WithContext(ctx).Save(d).Error
}

func (r *profileDimensionRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&ProfileDimension{}, "id = ?", id).Error
}

func (r *profileDimensionRepository) Seed(ctx context.Context) error {
	// Use the 8 standard dimensions from Deep Learning framework
	standardDimensions := GetStandardDimensions()

	for _, dimension := range standardDimensions {
		var count int64
		r.db.Model(&ProfileDimension{}).Where("dimension_code = ?", dimension.DimensionCode).Count(&count)
		if count == 0 {
			r.db.Create(&dimension)
		}
	}

	// Delete any non-standard dimensions that might exist (cleanup)
	// This removes old Pancasila-based dimensions if they exist
	r.db.Where("dimension_code NOT IN (?)", []string{
		DimensionCodeKeimanan,
		DimensionCodeKewargaan,
		DimensionCodePenalaran,
		DimensionCodeKreativitas,
		DimensionCodeKolaborasi,
		DimensionCodeKemandirian,
		DimensionCodeKesehatan,
		DimensionCodeKomunikasi,
	}).Delete(&ProfileDimension{})

	return nil
}
