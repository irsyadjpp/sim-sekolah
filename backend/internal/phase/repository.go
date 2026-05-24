package phase

import (
	"context"
	"fmt"
	"strings"
	"time"

	"sim-sekolah/pkg/cache"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// PhaseRepository mendefinisikan kontrak akses data untuk entitas Phase.
type PhaseRepository interface {
	GetAll(limit, offset int, search string) ([]Phase, int64, error)
	GetByID(id string) (*Phase, error)
	Create(ctx context.Context, p *Phase) error
	Update(ctx context.Context, p *Phase) error
	Delete(ctx context.Context, id string) error
	Seed(ctx context.Context) error
}

type phaseRepository struct {
	db *gorm.DB
}

// NewPhaseRepository membuat instance PhaseRepository baru dengan injected *gorm.DB.
func NewPhaseRepository(db *gorm.DB) PhaseRepository {
	return &phaseRepository{db: db}
}

func (r *phaseRepository) GetAll(limit, offset int, search string) ([]Phase, int64, error) {
	ctx := context.Background()
	cacheKey := fmt.Sprintf("phase:list:limit:%d:offset:%d:search:%s", limit, offset, search)

	type CacheData struct {
		Phases []Phase `json:"phases"`
		Total  int64   `json:"total"`
	}

	var cached CacheData
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, cacheKey, &cached); err == nil {
			return cached.Phases, cached.Total, nil
		}
	}

	var phases []Phase
	var total int64

	query := r.db.Model(&Phase{})

	if search != "" {
		like := "%" + search + "%"
		query = query.Where("phase_name ILIKE ? OR phase_code ILIKE ?", like, like)
	}

	query.Count(&total)

	err := query.
		Limit(limit).
		Offset(offset).
		Order("phase_code ASC").
		Find(&phases).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, cacheKey, CacheData{Phases: phases, Total: total}, 12*time.Hour)
	}

	return phases, total, err
}

func (r *phaseRepository) GetByID(id string) (*Phase, error) {
	var p Phase
	ctx := context.Background()

	// Coba ambil dari Redis cache terlebih dahulu
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, "phase:id:"+id, &p); err == nil {
			return &p, nil
		}
	}

	// Cache miss: Ambil dari database Postgres
	err := r.db.First(&p, "id = ?", id).Error
	if err != nil {
		return nil, err
	}

	// Simpan ke Redis cache untuk pembacaan berikutnya (TTL 12 Jam)
	if cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, "phase:id:"+id, &p, 12*time.Hour)
	}

	return &p, nil
}

func (r *phaseRepository) Create(ctx context.Context, p *Phase) error {
	if !strings.HasPrefix(strings.ToUpper(p.Code), "FAS-") {
		p.Code = "FAS-" + strings.ToUpper(p.Code)
	} else {
		p.Code = strings.ToUpper(p.Code)
	}
	err := r.db.WithContext(ctx).Create(p).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(ctx, "phase:list:*")
	}
	return err
}

func (r *phaseRepository) Update(ctx context.Context, p *Phase) error {
	err := r.db.WithContext(ctx).Save(p).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "phase:id:"+p.ID.String())
		_ = cache.GlobalCache.DeletePattern(ctx, "phase:list:*")
	}
	return err
}

func (r *phaseRepository) Delete(ctx context.Context, id string) error {
	var p Phase
	if err := r.db.WithContext(ctx).First(&p, "id = ?", id).Error; err != nil {
		return err
	}

	now := time.Now()
	p.DeletedAt = gorm.DeletedAt{Time: now, Valid: true}

	if userIDStr, ok := ctx.Value("user_id").(string); ok && userIDStr != "" {
		if uid, err := uuid.Parse(userIDStr); err == nil {
			p.DeletedBy = &uid
		}
	}

	err := r.db.WithContext(ctx).Model(&p).Updates(map[string]interface{}{
		"deleted_at": p.DeletedAt,
		"deleted_by": p.DeletedBy,
	}).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "phase:id:"+id)
		_ = cache.GlobalCache.DeletePattern(ctx, "phase:list:*")
	}
	return err
}

func (r *phaseRepository) Seed(ctx context.Context) error {
	// SD-only phases - Fase A, B, C for Sekolah Dasar
	seeds := []struct {
		Code string
		Name string
		Desc string
	}{
		{"FAS-A", "Fase A", "Kelas 1-2 SD/Sederajat"},
		{"FAS-B", "Fase B", "Kelas 3-4 SD/Sederajat"},
		{"FAS-C", "Fase C", "Kelas 5-6 SD/Sederajat"},
		// Removed Fase D, E, F as they are for SMP/SMA, not relevant for SD
	}

	for _, s := range seeds {
		var count int64
		r.db.Model(&Phase{}).Where("phase_code = ?", s.Code).Count(&count)
		if count == 0 {
			r.db.Create(&Phase{
				Code:        s.Code,
				Name:        s.Name,
				Description: s.Desc,
			})
		}
	}

	// Delete any non-SD phases that might exist (cleanup)
	r.db.Where("phase_code IN (?)", []string{"FAS-D", "FAS-E", "FAS-F"}).Delete(&Phase{})

	return nil
}
