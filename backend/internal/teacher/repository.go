package teacher

import (
	"context"

	"gorm.io/gorm"
)

type TeacherRepository interface {
	GetAll(ctx context.Context, limit, offset int, search string) ([]Teacher, int64, error)
	GetByID(ctx context.Context, id string) (*Teacher, error)
	GetBySchoolID(ctx context.Context, schoolID string) ([]Teacher, error)
	Create(ctx context.Context, data *Teacher) error
	Update(ctx context.Context, data *Teacher) error
	Delete(ctx context.Context, id string) error
}

type teacherRepository struct {
	db *gorm.DB
}

// NewTeacherRepository creates a new TeacherRepository with an injected *gorm.DB.
func NewTeacherRepository(db *gorm.DB) TeacherRepository {
	return &teacherRepository{db: db}
}

func (r *teacherRepository) GetAll(ctx context.Context, limit, offset int, search string) ([]Teacher, int64, error) {
	var teachers []Teacher
	var total int64

	query := r.db.WithContext(ctx).Model(&Teacher{})
	if search != "" {
		like := "%" + search + "%"
		query = query.Where("full_name ILIKE ? OR nip ILIKE ? OR email ILIKE ?", like, like, like)
	}

	query.Count(&total)
	err := query.Limit(limit).Offset(offset).Order("full_name ASC").Find(&teachers).Error
	return teachers, total, err
}

func (r *teacherRepository) GetByID(ctx context.Context, id string) (*Teacher, error) {
	var t Teacher
	if err := r.db.WithContext(ctx).First(&t, "id = ?", id).Error; err != nil {
		return nil, err
	}
	return &t, nil
}

func (r *teacherRepository) GetBySchoolID(ctx context.Context, schoolID string) ([]Teacher, error) {
	var teachers []Teacher
	err := r.db.WithContext(ctx).Where("school_id = ?", schoolID).Order("full_name ASC").Find(&teachers).Error
	return teachers, err
}

func (r *teacherRepository) Create(ctx context.Context, data *Teacher) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *teacherRepository) Update(ctx context.Context, data *Teacher) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *teacherRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&Teacher{}, "id = ?", id).Error
}
