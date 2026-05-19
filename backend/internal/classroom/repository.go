package classroom

import (
	"context"
	"time"

	"sim-sekolah/pkg/cache"

	"gorm.io/gorm"
)

type ClassroomRepository interface {
	GetAll(ctx context.Context, limit, offset int, schoolID string) ([]Classroom, int64, error)
	GetByID(ctx context.Context, id string) (*Classroom, error)
	Create(ctx context.Context, data *Classroom) error
	Update(ctx context.Context, data *Classroom) error
	Delete(ctx context.Context, id string) error
}

type classroomRepository struct {
	db *gorm.DB
}

func NewClassroomRepository(db *gorm.DB) ClassroomRepository {
	return &classroomRepository{db: db}
}

func (r *classroomRepository) GetAll(ctx context.Context, limit, offset int, schoolID string) ([]Classroom, int64, error) {
	var classrooms []Classroom
	var total int64

	query := r.db.WithContext(ctx).Model(&Classroom{}).
		Preload("School").
		Preload("AcademicYear").
		Preload("Grade").
		Preload("Homeroom")

	if schoolID != "" {
		query = query.Where("school_id = ?", schoolID)
	}

	query.Count(&total)
	err := query.Limit(limit).Offset(offset).Order("classroom_name ASC").Find(&classrooms).Error
	return classrooms, total, err
}

func (r *classroomRepository) GetByID(ctx context.Context, id string) (*Classroom, error) {
	var c Classroom
	// Coba ambil dari Redis cache terlebih dahulu
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, "classroom:id:"+id, &c); err == nil {
			return &c, nil
		}
	}

	// Cache miss: Ambil dari database Postgres
	err := r.db.WithContext(ctx).
		Preload("School").
		Preload("AcademicYear").
		Preload("Grade").
		Preload("Homeroom").
		First(&c, "id = ?", id).Error
	if err != nil {
		return nil, err
	}

	// Simpan ke Redis cache untuk pembacaan berikutnya (TTL 12 Jam)
	if cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, "classroom:id:"+id, &c, 12*time.Hour)
	}

	return &c, nil
}

func (r *classroomRepository) Create(ctx context.Context, data *Classroom) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *classroomRepository) Update(ctx context.Context, data *Classroom) error {
	err := r.db.WithContext(ctx).Save(data).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "classroom:id:"+data.ID.String())
	}
	return err
}

func (r *classroomRepository) Delete(ctx context.Context, id string) error {
	err := r.db.WithContext(ctx).Delete(&Classroom{}, "id = ?", id).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "classroom:id:"+id)
	}
	return err
}
