package grade

import (
	"context"
	"time"

	"sim-sekolah/pkg/cache"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type GradeRepository interface {
	GetAll(ctx context.Context, limit, offset int) ([]Grade, int64, error)
	GetByPhaseID(ctx context.Context, phaseID string) ([]Grade, error)
	GetByID(ctx context.Context, id string) (*Grade, error)
	Create(ctx context.Context, data *Grade) error
	Update(ctx context.Context, data *Grade) error
	Delete(ctx context.Context, id string) error
	Seed(ctx context.Context) error
}

type gradeRepository struct {
	db *gorm.DB
}

func NewGradeRepository(db *gorm.DB) GradeRepository {
	return &gradeRepository{db: db}
}

func (r *gradeRepository) GetAll(ctx context.Context, limit, offset int) ([]Grade, int64, error) {
	var grades []Grade
	var total int64

	query := r.db.WithContext(ctx).Model(&Grade{})
	query.Count(&total)
	err := query.Limit(limit).Offset(offset).Order("grade_level ASC").Find(&grades).Error
	return grades, total, err
}

func (r *gradeRepository) GetByPhaseID(ctx context.Context, phaseID string) ([]Grade, error) {
	var grades []Grade
	err := r.db.WithContext(ctx).Where("phase_id = ?", phaseID).Order("grade_level ASC").Find(&grades).Error
	return grades, err
}

func (r *gradeRepository) GetByID(ctx context.Context, id string) (*Grade, error) {
	var g Grade
	// Coba ambil dari Redis cache terlebih dahulu
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, "grade:id:"+id, &g); err == nil {
			return &g, nil
		}
	}

	// Cache miss: Ambil dari database Postgres
	if err := r.db.WithContext(ctx).First(&g, "id = ?", id).Error; err != nil {
		return nil, err
	}

	// Simpan ke Redis cache untuk pembacaan berikutnya (TTL 12 Jam)
	if cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, "grade:id:"+id, &g, 12*time.Hour)
	}

	return &g, nil
}

func (r *gradeRepository) Create(ctx context.Context, data *Grade) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *gradeRepository) Update(ctx context.Context, data *Grade) error {
	err := r.db.WithContext(ctx).Save(data).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "grade:id:"+data.ID.String())
	}
	return err
}

func (r *gradeRepository) Delete(ctx context.Context, id string) error {
	err := r.db.WithContext(ctx).Delete(&Grade{}, "id = ?", id).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "grade:id:"+id)
	}
	return err
}

func (r *gradeRepository) Seed(ctx context.Context) error {
	var phases []struct {
		ID   uuid.UUID
		Code string
	}
	r.db.Table("master_phase").Select("id, phase_code").Find(&phases)

	phaseMap := make(map[string]uuid.UUID)
	for _, p := range phases {
		phaseMap[p.Code] = p.ID
	}

	seeds := []struct {
		PhaseCode string
		Level     int
		Name      string
	}{
		{"FAS-A", 1, "Kelas 1"},
		{"FAS-A", 2, "Kelas 2"},
		{"FAS-B", 3, "Kelas 3"},
		{"FAS-B", 4, "Kelas 4"},
		{"FAS-C", 5, "Kelas 5"},
		{"FAS-C", 6, "Kelas 6"},
	}

	for _, s := range seeds {
		phaseID, ok := phaseMap[s.PhaseCode]
		if !ok {
			continue
		}

		var count int64
		r.db.Model(&Grade{}).Where("grade_level = ?", s.Level).Count(&count)
		if count == 0 {
			r.db.Create(&Grade{
				PhaseID:    phaseID,
				GradeLevel: s.Level,
				GradeName:  s.Name,
			})
		}
	}
	return nil
}
