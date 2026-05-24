package olah_aspect

import (
	"context"
	"fmt"
	"time"

	"sim-sekolah/pkg/cache"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// OlahAspectRepository defines the data access contract for OlahAspect entities
type OlahAspectRepository interface {
	GetAll(limit, offset int, search string) ([]OlahAspect, int64, error)
	GetByID(id string) (*OlahAspect, error)
	GetByCode(code string) (*OlahAspect, error)
	Create(ctx context.Context, aspect *OlahAspect) error
	Update(ctx context.Context, aspect *OlahAspect) error
	Delete(ctx context.Context, id string) error
	Seed(ctx context.Context) error
}

type olahAspectRepository struct {
	db *gorm.DB
}

// NewOlahAspectRepository creates a new OlahAspectRepository with injected GORM DB
func NewOlahAspectRepository(db *gorm.DB) OlahAspectRepository {
	return &olahAspectRepository{db: db}
}

func (r *olahAspectRepository) GetAll(limit, offset int, search string) ([]OlahAspect, int64, error) {
	ctx := context.Background()
	cacheKey := fmt.Sprintf("olah_aspect:list:limit:%d:offset:%d:search:%s", limit, offset, search)

	type CacheData struct {
		Aspects []OlahAspect `json:"aspects"`
		Total   int64        `json:"total"`
	}

	var cached CacheData
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, cacheKey, &cached); err == nil {
			return cached.Aspects, cached.Total, nil
		}
	}

	var aspects []OlahAspect
	var total int64

	query := r.db.Model(&OlahAspect{})

	if search != "" {
		like := "%" + search + "%"
		query = query.Where("aspect_name ILIKE ? OR aspect_code ILIKE ? OR definition ILIKE ?", like, like, like)
	}

	query.Count(&total)

	err := query.
		Limit(limit).
		Offset(offset).
		Order("aspect_code ASC").
		Find(&aspects).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, cacheKey, CacheData{Aspects: aspects, Total: total}, 12*time.Hour)
	}

	return aspects, total, err
}

func (r *olahAspectRepository) GetByID(id string) (*OlahAspect, error) {
	var aspect OlahAspect
	ctx := context.Background()

	// Try to get from Redis cache first
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, "olah_aspect:id:"+id, &aspect); err == nil {
			return &aspect, nil
		}
	}

	// Cache miss: Get from database Postgres
	err := r.db.First(&aspect, "id = ?", id).Error
	if err != nil {
		return nil, err
	}

	// Save to Redis cache for subsequent reads (TTL 12 Hours)
	if cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, "olah_aspect:id:"+id, &aspect, 12*time.Hour)
	}

	return &aspect, nil
}

func (r *olahAspectRepository) GetByCode(code string) (*OlahAspect, error) {
	var aspect OlahAspect
	err := r.db.Where("aspect_code = ?", code).First(&aspect).Error
	if err != nil {
		return nil, err
	}
	return &aspect, nil
}

func (r *olahAspectRepository) Create(ctx context.Context, aspect *OlahAspect) error {
	err := r.db.WithContext(ctx).Create(aspect).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(ctx, "olah_aspect:list:*")
	}
	return err
}

func (r *olahAspectRepository) Update(ctx context.Context, aspect *OlahAspect) error {
	err := r.db.WithContext(ctx).Save(aspect).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "olah_aspect:id:"+aspect.ID.String())
		_ = cache.GlobalCache.DeletePattern(ctx, "olah_aspect:list:*")
	}
	return err
}

func (r *olahAspectRepository) Delete(ctx context.Context, id string) error {
	var aspect OlahAspect
	if err := r.db.WithContext(ctx).First(&aspect, "id = ?", id).Error; err != nil {
		return err
	}

	now := time.Now()
	aspect.DeletedAt = gorm.DeletedAt{Time: now, Valid: true}

	if userIDStr, ok := ctx.Value("user_id").(string); ok && userIDStr != "" {
		if uid, err := uuid.Parse(userIDStr); err == nil {
			aspect.DeletedBy = &uid
		}
	}

	err := r.db.WithContext(ctx).Model(&aspect).Updates(map[string]interface{}{
		"deleted_at": aspect.DeletedAt,
		"deleted_by": aspect.DeletedBy,
	}).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "olah_aspect:id:"+id)
		_ = cache.GlobalCache.DeletePattern(ctx, "olah_aspect:list:*")
	}

	return err
}

func (r *olahAspectRepository) Seed(ctx context.Context) error {
	standardAspects := GetStandardAspects()

	for _, aspect := range standardAspects {
		var count int64
		r.db.Model(&OlahAspect{}).Where("aspect_code = ?", aspect.AspectCode).Count(&count)
		if count == 0 {
			r.db.Create(&aspect)
		}
	}
	return nil
}
