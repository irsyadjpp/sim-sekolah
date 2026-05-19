package academic_year

import (
	"context"
	"time"

	"sim-sekolah/pkg/cache"

	"gorm.io/gorm"
)

type AcademicYearRepository interface {
	GetAll(ctx context.Context, limit int, offset int) ([]AcademicYear, int64, error)
	GetByID(ctx context.Context, id string) (*AcademicYear, error)
	Create(ctx context.Context, data *AcademicYear) error
	Update(ctx context.Context, data *AcademicYear) error
	Delete(ctx context.Context, id string) error
	DeactivateAll(ctx context.Context) error
	SetActiveTransaction(ctx context.Context, id string) error
}

type academicYearRepository struct {
	db *gorm.DB
}

func NewAcademicYearRepository(db *gorm.DB) AcademicYearRepository {
	return &academicYearRepository{db: db}
}

func (r *academicYearRepository) GetAll(ctx context.Context, limit int, offset int) ([]AcademicYear, int64, error) {
	var years []AcademicYear
	var total int64

	query := r.db.WithContext(ctx).Model(&AcademicYear{})
	query.Count(&total)

	err := query.Limit(limit).Offset(offset).Order("year_name DESC, semester DESC").Find(&years).Error
	return years, total, err
}

func (r *academicYearRepository) GetByID(ctx context.Context, id string) (*AcademicYear, error) {
	var year AcademicYear
	// Coba ambil dari Redis cache terlebih dahulu
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, "academic_year:id:"+id, &year); err == nil {
			return &year, nil
		}
	}

	// Cache miss: Ambil dari database Postgres
	err := r.db.WithContext(ctx).First(&year, "id = ?", id).Error
	if err != nil {
		return nil, err
	}

	// Simpan ke Redis cache untuk pembacaan berikutnya (TTL 12 Jam)
	if cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, "academic_year:id:"+id, &year, 12*time.Hour)
	}

	return &year, nil
}

func (r *academicYearRepository) Create(ctx context.Context, data *AcademicYear) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *academicYearRepository) Update(ctx context.Context, data *AcademicYear) error {
	err := r.db.WithContext(ctx).Save(data).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "academic_year:id:"+data.ID.String())
	}
	return err
}

func (r *academicYearRepository) Delete(ctx context.Context, id string) error {
	err := r.db.WithContext(ctx).Delete(&AcademicYear{}, "id = ?", id).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "academic_year:id:"+id)
	}
	return err
}

// DeactivateAll digunakan jika ada Tahun Ajaran baru yang diset Active, maka yang lain dinonaktifkan
func (r *academicYearRepository) DeactivateAll(ctx context.Context) error {
	err := r.db.WithContext(ctx).Model(&AcademicYear{}).Where("is_active = ?", true).Update("is_active", false).Error
	if err == nil && cache.GlobalCache != nil {
		// Bersihkan seluruh cache tahun akademik untuk menghindari is_active basi
		var years []AcademicYear
		if r.db.Model(&AcademicYear{}).Find(&years).Error == nil {
			for _, y := range years {
				_ = cache.GlobalCache.Delete(ctx, "academic_year:id:"+y.ID.String())
			}
		}
	}
	return err
}

func (r *academicYearRepository) SetActiveTransaction(ctx context.Context, id string) error {
	err := r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		// 1. Nonaktifkan semua
		if err := tx.Model(&AcademicYear{}).Where("is_active = ?", true).Update("is_active", false).Error; err != nil {
			return err
		}
		// 2. Aktifkan yang dipilih
		if err := tx.Model(&AcademicYear{}).Where("id = ?", id).Update("is_active", true).Error; err != nil {
			return err
		}
		return nil
	})

	if err == nil && cache.GlobalCache != nil {
		// Bersihkan cache seluruh tahun akademik untuk mencerminkan status keaktifan baru
		var years []AcademicYear
		if r.db.Model(&AcademicYear{}).Find(&years).Error == nil {
			for _, y := range years {
				_ = cache.GlobalCache.Delete(ctx, "academic_year:id:"+y.ID.String())
			}
		}
	}
	return err
}
