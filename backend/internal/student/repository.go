package student

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type StudentRepository interface {
	GetAll(ctx context.Context, limit, offset int, search string) ([]Student, int64, error)
	GetByID(ctx context.Context, id string) (*Student, error)
	GetBySchoolID(ctx context.Context, schoolID string) ([]Student, error)
	Create(ctx context.Context, data *Student) error
	Update(ctx context.Context, data *Student) error
	Delete(ctx context.Context, id string) error
	UpsertParent(ctx context.Context, studentID string, req UpsertParentRequest) (*StudentParent, error)
	DeleteParent(ctx context.Context, studentID, parentID string) error
}

type studentRepository struct {
	db *gorm.DB
}

// NewStudentRepository creates a new StudentRepository with an injected *gorm.DB.
func NewStudentRepository(db *gorm.DB) StudentRepository {
	return &studentRepository{db: db}
}

func (r *studentRepository) GetAll(ctx context.Context, limit, offset int, search string) ([]Student, int64, error) {
	var students []Student
	var total int64

	query := r.db.WithContext(ctx).Model(&Student{})
	if search != "" {
		like := "%" + search + "%"
		query = query.Where("full_name ILIKE ? OR nisn ILIKE ? OR nis ILIKE ?", like, like, like)
	}

	query.Count(&total)
	err := query.Limit(limit).Offset(offset).Order("full_name ASC").Find(&students).Error
	return students, total, err
}

func (r *studentRepository) GetByID(ctx context.Context, id string) (*Student, error) {
	var s Student
	err := r.db.WithContext(ctx).Preload("Parents").First(&s, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return &s, nil
}

func (r *studentRepository) GetBySchoolID(ctx context.Context, schoolID string) ([]Student, error) {
	var students []Student
	err := r.db.WithContext(ctx).Where("school_id = ?", schoolID).Order("full_name ASC").Find(&students).Error
	return students, err
}

func (r *studentRepository) Create(ctx context.Context, data *Student) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *studentRepository) Update(ctx context.Context, data *Student) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *studentRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&Student{}, "id = ?", id).Error
}

// UpsertParent: insert baru atau update berdasarkan student_id + parent_type (max 1 per tipe)
func (r *studentRepository) UpsertParent(ctx context.Context, studentID string, req UpsertParentRequest) (*StudentParent, error) {
	studentUUID, _ := uuid.Parse(studentID)

	var parent StudentParent
	result := r.db.WithContext(ctx).
		Where("student_id = ? AND parent_type = ?", studentUUID, req.ParentType).
		First(&parent)

	if result.Error != nil {
		// Buat baru
		parent = StudentParent{
			ID:         uuid.New(),
			StudentID:  studentUUID,
			ParentType: req.ParentType,
		}
	}

	// Update field
	parent.FullName = req.FullName
	parent.NIK = req.NIK
	parent.Education = req.Education
	parent.Occupation = req.Occupation
	parent.Income = req.Income
	parent.Phone = req.Phone

	if err := r.db.WithContext(ctx).Save(&parent).Error; err != nil {
		return nil, err
	}
	return &parent, nil
}

func (r *studentRepository) DeleteParent(ctx context.Context, studentID, parentID string) error {
	return r.db.WithContext(ctx).
		Where("id = ? AND student_id = ?", parentID, studentID).
		Delete(&StudentParent{}).Error
}
