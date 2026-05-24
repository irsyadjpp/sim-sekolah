package learning_principle

import (
	"context"
	"fmt"
	"time"

	"sim-sekolah/pkg/cache"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// LearningPrincipleRepository defines the data access contract for LearningPrinciple entities
type LearningPrincipleRepository interface {
	GetAll(limit, offset int, search string) ([]LearningPrinciple, int64, error)
	GetByID(id string) (*LearningPrinciple, error)
	GetByCode(code string) (*LearningPrinciple, error)
	Create(ctx context.Context, principle *LearningPrinciple) error
	Update(ctx context.Context, principle *LearningPrinciple) error
	Delete(ctx context.Context, id string) error
	Seed(ctx context.Context) error
}

type learningPrincipleRepository struct {
	db *gorm.DB
}

// NewLearningPrincipleRepository creates a new LearningPrincipleRepository with injected GORM DB
func NewLearningPrincipleRepository(db *gorm.DB) LearningPrincipleRepository {
	return &learningPrincipleRepository{db: db}
}

func (r *learningPrincipleRepository) GetAll(limit, offset int, search string) ([]LearningPrinciple, int64, error) {
	ctx := context.Background()
	cacheKey := fmt.Sprintf("learning_principle:list:limit:%d:offset:%d:search:%s", limit, offset, search)

	type CacheData struct {
		Principles []LearningPrinciple `json:"principles"`
		Total      int64               `json:"total"`
	}

	var cached CacheData
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, cacheKey, &cached); err == nil {
			return cached.Principles, cached.Total, nil
		}
	}

	var principles []LearningPrinciple
	var total int64

	query := r.db.Model(&LearningPrinciple{})

	if search != "" {
		like := "%" + search + "%"
		query = query.Where("principle_name ILIKE ? OR principle_code ILIKE ? OR description ILIKE ?", like, like, like)
	}

	query.Count(&total)

	err := query.
		Limit(limit).
		Offset(offset).
		Order("principle_code ASC").
		Find(&principles).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, cacheKey, CacheData{Principles: principles, Total: total}, 12*time.Hour)
	}

	return principles, total, err
}

func (r *learningPrincipleRepository) GetByID(id string) (*LearningPrinciple, error) {
	var principle LearningPrinciple
	ctx := context.Background()

	// Try to get from Redis cache first
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, "learning_principle:id:"+id, &principle); err == nil {
			return &principle, nil
		}
	}

	// Cache miss: Get from database Postgres
	err := r.db.First(&principle, "id = ?", id).Error
	if err != nil {
		return nil, err
	}

	// Save to Redis cache for subsequent reads (TTL 12 Hours)
	if cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, "learning_principle:id:"+id, &principle, 12*time.Hour)
	}

	return &principle, nil
}

func (r *learningPrincipleRepository) GetByCode(code string) (*LearningPrinciple, error) {
	var principle LearningPrinciple
	err := r.db.Where("principle_code = ?", code).First(&principle).Error
	if err != nil {
		return nil, err
	}
	return &principle, nil
}

func (r *learningPrincipleRepository) Create(ctx context.Context, principle *LearningPrinciple) error {
	err := r.db.WithContext(ctx).Create(principle).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(ctx, "learning_principle:list:*")
	}
	return err
}

func (r *learningPrincipleRepository) Update(ctx context.Context, principle *LearningPrinciple) error {
	err := r.db.WithContext(ctx).Save(principle).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "learning_principle:id:"+principle.ID.String())
		_ = cache.GlobalCache.DeletePattern(ctx, "learning_principle:list:*")
	}
	return err
}

func (r *learningPrincipleRepository) Delete(ctx context.Context, id string) error {
	var principle LearningPrinciple
	if err := r.db.WithContext(ctx).First(&principle, "id = ?", id).Error; err != nil {
		return err
	}

	now := time.Now()
	principle.DeletedAt = gorm.DeletedAt{Time: now, Valid: true}

	if userIDStr, ok := ctx.Value("user_id").(string); ok && userIDStr != "" {
		if uid, err := uuid.Parse(userIDStr); err == nil {
			principle.DeletedBy = &uid
		}
	}

	err := r.db.WithContext(ctx).Model(&principle).Updates(map[string]interface{}{
		"deleted_at": principle.DeletedAt,
		"deleted_by": principle.DeletedBy,
	}).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "learning_principle:id:"+id)
		_ = cache.GlobalCache.DeletePattern(ctx, "learning_principle:list:*")
	}

	return err
}

func (r *learningPrincipleRepository) Seed(ctx context.Context) error {
	standardPrinciples := GetStandardPrinciples()

	for _, principle := range standardPrinciples {
		var count int64
		r.db.Model(&LearningPrinciple{}).Where("principle_code = ?", principle.PrincipleCode).Count(&count)
		if count == 0 {
			r.db.Create(&principle)
		}
	}
	return nil
}
