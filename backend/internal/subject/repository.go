package subject

import (
	"context"
	"fmt"
	"log/slog"
	"strings"
	"time"

	"sim-sekolah/pkg/cache"
	"sim-sekolah/pkg/logger"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// SubjectRepository mendefinisikan operasi DB untuk Subject
type SubjectRepository interface {
	GetAll(limit, offset int, search string, isActive *bool) ([]Subject, int64, error)
	GetByID(id string) (*Subject, error)
	Create(ctx context.Context, s *Subject) error
	Update(ctx context.Context, s *Subject) error
	Delete(ctx context.Context, id string) error
}

type subjectRepository struct {
	db *gorm.DB
}

// NewSubjectRepository creates a new SubjectRepository with an injected *gorm.DB.
func NewSubjectRepository(db *gorm.DB) SubjectRepository {
	return &subjectRepository{db: db}
}

func (r *subjectRepository) GetAll(limit, offset int, search string, isActive *bool) ([]Subject, int64, error) {
	ctx := context.Background()
	isActiveStr := "nil"
	if isActive != nil {
		isActiveStr = fmt.Sprintf("%t", *isActive)
	}
	cacheKey := fmt.Sprintf("subject:list:limit:%d:offset:%d:search:%s:is_active:%s", limit, offset, search, isActiveStr)

	type CacheData struct {
		Subjects []Subject `json:"subjects"`
		Total    int64     `json:"total"`
	}

	var cached CacheData
	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, cacheKey, &cached); err == nil {
			return cached.Subjects, cached.Total, nil
		}
	}

	var subjects []Subject
	var total int64

	query := r.db.Model(&Subject{})

	if search != "" {
		like := "%" + search + "%"
		query = query.Where("subject_name ILIKE ? OR subject_code ILIKE ?", like, like)
	}

	if isActive != nil {
		query = query.Where("is_active = ?", *isActive)
	}

	query.Count(&total)

	err := query.
		Limit(limit).
		Offset(offset).
		Order("subject_code ASC").
		Find(&subjects).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, cacheKey, CacheData{Subjects: subjects, Total: total}, 12*time.Hour)
	}

	return subjects, total, err
}

func (r *subjectRepository) GetByID(id string) (*Subject, error) {
	var s Subject
	ctx := context.Background()

	if cache.GlobalCache != nil {
		if err := cache.GlobalCache.Get(ctx, "subject:id:"+id, &s); err == nil {
			return &s, nil
		}
	}

	err := r.db.
		Preload("Elements").
		Preload("CharacteristicPoints").
		Preload("CharacteristicPoints.Elements").
		First(&s, "id = ?", id).Error
	if err != nil {
		return nil, err
	}

	if cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, "subject:id:"+id, &s, 12*time.Hour)
	}

	return &s, nil
}

func (r *subjectRepository) Create(ctx context.Context, s *Subject) error {
	if s.SubjectCode == "" {
		s.SubjectCode = strings.ToUpper(fmt.Sprintf("MAP-%s-%s", s.Level, s.Abbreviation))
	}
	err := r.db.WithContext(ctx).Create(s).Error
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(ctx, "subject:list:*")
	}
	return err
}

func (r *subjectRepository) Update(ctx context.Context, s *Subject) error {
	err := r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		// 1. Update basic fields
		if err := tx.Omit("Elements", "CharacteristicPoints").Save(s).Error; err != nil {
			return err
		}

		// 2. Manual association management for stability
		// Delete existing elements and points first (Atomic in Transaction)
		if err := tx.Where("subject_id = ?", s.ID).Delete(&SubjectElement{}).Error; err != nil {
			return err
		}
		if err := tx.Where("subject_id = ?", s.ID).Delete(&CharacteristicPoint{}).Error; err != nil {
			return err
		}

		// 3. Insert new CharacteristicPoints (and their nested Elements)
		for _, cp := range s.CharacteristicPoints {
			cp.SubjectID = s.ID
			// Ensure ID is zeroed for new points if they don't have one
			// to let GORM/Postgres generate it
			if err := tx.Create(&cp).Error; err != nil {
				logger.Error("Failed to create CharacteristicPoint during update", err, slog.String("subject_id", s.ID.String()))
				return err
			}
		}

		return nil
	})

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "subject:id:"+s.ID.String())
		_ = cache.GlobalCache.DeletePattern(ctx, "subject:list:*")
	}
	return err
}

func (r *subjectRepository) Delete(ctx context.Context, id string) error {
	var s Subject
	if err := r.db.WithContext(ctx).First(&s, "id = ?", id).Error; err != nil {
		return err
	}

	now := time.Now()
	s.DeletedAt = gorm.DeletedAt{Time: now, Valid: true}

	if userIDStr, ok := ctx.Value("user_id").(string); ok && userIDStr != "" {
		if uid, err := uuid.Parse(userIDStr); err == nil {
			s.DeletedBy = &uid
		}
	}

	err := r.db.WithContext(ctx).Model(&s).Updates(map[string]interface{}{
		"deleted_at": s.DeletedAt,
		"deleted_by": s.DeletedBy,
	}).Error

	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "subject:id:"+id)
		_ = cache.GlobalCache.DeletePattern(ctx, "subject:list:*")
	}
	return err
}

// SubjectElementRepository mendefinisikan operasi DB untuk SubjectElement
type SubjectElementRepository interface {
	GetAllBySubject(subjectID string) ([]SubjectElement, error)
	GetByID(id string) (*SubjectElement, error)
	Create(ctx context.Context, e *SubjectElement) error
	Update(ctx context.Context, e *SubjectElement) error
	Delete(ctx context.Context, id string) error
}

type subjectElementRepository struct {
	db *gorm.DB
}

// NewSubjectElementRepository creates a new SubjectElementRepository with an injected *gorm.DB.
func NewSubjectElementRepository(db *gorm.DB) SubjectElementRepository {
	return &subjectElementRepository{db: db}
}

func (r *subjectElementRepository) GetAllBySubject(subjectID string) ([]SubjectElement, error) {
	var elements []SubjectElement
	err := r.db.Where("subject_id = ?", subjectID).Order("element_name ASC").Find(&elements).Error
	return elements, err
}

func (r *subjectElementRepository) GetByID(id string) (*SubjectElement, error) {
	var e SubjectElement
	err := r.db.First(&e, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return &e, nil
}

func (r *subjectElementRepository) Create(ctx context.Context, e *SubjectElement) error {
	return r.db.WithContext(ctx).Create(e).Error
}

func (r *subjectElementRepository) Update(ctx context.Context, e *SubjectElement) error {
	return r.db.WithContext(ctx).Save(e).Error
}

func (r *subjectElementRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&SubjectElement{}, "id = ?", id).Error
}
