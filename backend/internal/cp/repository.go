package cp

import (
	"context"
	"fmt"
	"time"

	"sim-sekolah/pkg/cache"

	"gorm.io/gorm"
)

// CPRepository defines database operations for LearningOutcome.
type CPRepository interface {
	GetAll(limit int, offset int, search string) ([]LearningOutcome, int64, error)
	GetByID(id string) (*LearningOutcome, error)
	Create(ctx context.Context, data *LearningOutcome) error
	Update(ctx context.Context, data *LearningOutcome) error
	Delete(ctx context.Context, id string) error
}

type cpRepository struct {
	db *gorm.DB
}

// NewCPRepository creates a new CPRepository with an injected *gorm.DB.
func NewCPRepository(db *gorm.DB) CPRepository {
	return &cpRepository{db: db}
}

func (r *cpRepository) GetAll(limit int, offset int, search string) ([]LearningOutcome, int64, error) {
	ctx := context.Background()
	cacheKey := fmt.Sprintf("cp:list:limit:%d:offset:%d:search:%s", limit, offset, search)

	type CacheData struct {
		CPs   []LearningOutcome `json:"cps"`
		Total int64             `json:"total"`
	}

	var cached CacheData
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, cacheKey, &cached); err == nil {
			return cached.CPs, cached.Total, nil
		}
	}

	var cps []LearningOutcome
	var total int64

	query := r.db.Model(&LearningOutcome{}).
		Preload("Phase").
		Preload("Subject")

	if search != "" {
		like := "%" + search + "%"
		query = query.Where("outcome_text ILIKE ? OR cp_code ILIKE ?", like, like)
	}

	query.Count(&total)

	err := query.
		Limit(limit).
		Offset(offset).
		Order("cp_code ASC").
		Find(&cps).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, cacheKey, CacheData{CPs: cps, Total: total}, 1*time.Hour)
	}

	return cps, total, err
}

func (r *cpRepository) GetByID(id string) (*LearningOutcome, error) {
	var cp LearningOutcome
	err := r.db.
		Preload("Phase").
		Preload("Subject").
		Preload("Details").
		Preload("Details.Element").
		First(&cp, "id = ?", id).Error

	if err != nil {
		return nil, err
	}
	return &cp, nil
}

func (r *cpRepository) Create(ctx context.Context, data *LearningOutcome) error {
	if data.CPCode == "" {
		var count int64
		r.db.WithContext(ctx).Model(&LearningOutcome{}).Count(&count)
		data.CPCode = fmt.Sprintf("CP-%04d", count+1)
	}
	err := r.db.WithContext(ctx).Create(data).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "cp:list:*")
	}
	return err
}

func (r *cpRepository) Update(ctx context.Context, data *LearningOutcome) error {
	// Cleanly replace Details association to remove deleted ones and prevent duplicates
	if err := r.db.WithContext(ctx).Model(data).Association("Details").Replace(data.Details); err != nil {
		return err
	}
	err := r.db.WithContext(ctx).Save(data).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "cp:list:*")
	}
	return err
}

func (r *cpRepository) Delete(ctx context.Context, id string) error {
	var cp LearningOutcome
	if err := r.db.WithContext(ctx).First(&cp, "id = ?", id).Error; err != nil {
		return err
	}

	updates := map[string]interface{}{
		"deleted_at": time.Now(),
	}
	if userID, ok := ctx.Value("user_id").(string); ok && userID != "" {
		updates["deleted_by"] = userID
	}

	err := r.db.WithContext(ctx).Model(&cp).Updates(updates).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "cp:list:*")
	}
	return err
}

// CPDetailRepository defines database operations for CPDetail.
type CPDetailRepository interface {
	GetAllByCP(cpID string) ([]CPDetail, error)
	GetByID(id string) (*CPDetail, error)
	Create(ctx context.Context, data *CPDetail) error
	Update(ctx context.Context, data *CPDetail) error
	Delete(ctx context.Context, id string) error
}

type cpDetailRepository struct {
	db *gorm.DB
}

// NewCPDetailRepository creates a new CPDetailRepository with an injected *gorm.DB.
func NewCPDetailRepository(db *gorm.DB) CPDetailRepository {
	return &cpDetailRepository{db: db}
}

func (r *cpDetailRepository) GetAllByCP(cpID string) ([]CPDetail, error) {
	var details []CPDetail
	err := r.db.Where("learning_outcome_id = ?", cpID).
		Preload("Element").
		Order("sequence_no ASC").
		Find(&details).Error
	return details, err
}

func (r *cpDetailRepository) GetByID(id string) (*CPDetail, error) {
	var d CPDetail
	err := r.db.First(&d, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return &d, nil
}

func (r *cpDetailRepository) Create(ctx context.Context, data *CPDetail) error {
	err := r.db.WithContext(ctx).Create(data).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "cp:list:*")
	}
	return err
}

func (r *cpDetailRepository) Update(ctx context.Context, data *CPDetail) error {
	err := r.db.WithContext(ctx).Save(data).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "cp:list:*")
	}
	return err
}

func (r *cpDetailRepository) Delete(ctx context.Context, id string) error {
	var d CPDetail
	if err := r.db.WithContext(ctx).First(&d, "id = ?", id).Error; err != nil {
		return err
	}

	updates := map[string]interface{}{
		"deleted_at": time.Now(),
	}
	if userID, ok := ctx.Value("user_id").(string); ok && userID != "" {
		updates["deleted_by"] = userID
	}

	err := r.db.WithContext(ctx).Model(&d).Updates(updates).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "cp:list:*")
	}
	return err
}

// LearningObjectiveRepository
type LearningObjectiveRepository interface {
	GetAllByCP(cpID string) ([]LearningObjective, error)
	GetByID(id string) (*LearningObjective, error)
	Create(ctx context.Context, data *LearningObjective) error
	Update(ctx context.Context, data *LearningObjective) error
	Delete(ctx context.Context, id string) error
}

type learningObjectiveRepository struct {
	db *gorm.DB
}

func NewLearningObjectiveRepository(db *gorm.DB) LearningObjectiveRepository {
	return &learningObjectiveRepository{db: db}
}

func (r *learningObjectiveRepository) GetAllByCP(cpID string) ([]LearningObjective, error) {
	var objectives []LearningObjective
	err := r.db.Where("learning_outcome_id = ?", cpID).Order("sequence ASC, created_at ASC").Find(&objectives).Error
	return objectives, err
}

func (r *learningObjectiveRepository) GetByID(id string) (*LearningObjective, error) {
	var objective LearningObjective
	err := r.db.Where("id = ?", id).First(&objective).Error
	if err != nil {
		return nil, err
	}
	return &objective, nil
}

func (r *learningObjectiveRepository) Create(ctx context.Context, data *LearningObjective) error {
	err := r.db.WithContext(ctx).Create(data).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "cp:list:*")
	}
	return err
}

func (r *learningObjectiveRepository) Update(ctx context.Context, data *LearningObjective) error {
	err := r.db.WithContext(ctx).Save(data).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "cp:list:*")
	}
	return err
}

func (r *learningObjectiveRepository) Delete(ctx context.Context, id string) error {
	var obj LearningObjective
	if err := r.db.WithContext(ctx).First(&obj, "id = ?", id).Error; err != nil {
		return err
	}

	updates := map[string]interface{}{
		"deleted_at": time.Now(),
	}
	if userID, ok := ctx.Value("user_id").(string); ok && userID != "" {
		updates["deleted_by"] = userID
	}

	err := r.db.WithContext(ctx).Model(&obj).Updates(updates).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(context.Background(), "cp:list:*")
	}
	return err
}
