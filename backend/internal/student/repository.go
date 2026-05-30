package student

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type StudentRepository interface {
	GetAll(ctx context.Context, limit, offset int, search string) ([]StudentComplete, int64, error)
	GetByID(ctx context.Context, id string) (*StudentComplete, error)
	GetBySchoolID(ctx context.Context, schoolID string) ([]StudentComplete, error)
	CreateComplete(ctx context.Context, data *StudentComplete) error
	UpdateComplete(ctx context.Context, data *StudentComplete) error
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

func (r *studentRepository) GetAll(ctx context.Context, limit, offset int, search string) ([]StudentComplete, int64, error) {
	var students []StudentComplete
	var total int64

	query := r.db.WithContext(ctx).Model(&MasterStudent{})
	if search != "" {
		like := "%" + search + "%"
		query = query.Where("full_name ILIKE ? OR nisn ILIKE ? OR nis ILIKE ?", like, like, like)
	}

	query.Count(&total)
	err := query.Limit(limit).Offset(offset).Order("full_name ASC").Find(&students).Error
	return students, total, err
}

func (r *studentRepository) GetByID(ctx context.Context, id string) (*StudentComplete, error) {
	var s StudentComplete
	if err := r.db.WithContext(ctx).First(&s.MasterStudent, "id = ?", id).Error; err != nil {
		return nil, err
	}

	// Load related data
	r.db.WithContext(ctx).First(&s.StudentContact, "student_id = ?", id)
	r.db.WithContext(ctx).First(&s.StudentFamily, "student_id = ?", id)
	r.db.WithContext(ctx).First(&s.StudentEnrollment, "student_id = ?", id)
	r.db.WithContext(ctx).First(&s.StudentHealth, "student_id = ?", id)

	return &s, nil
}

func (r *studentRepository) GetBySchoolID(ctx context.Context, schoolID string) ([]StudentComplete, error) {
	var students []StudentComplete
	err := r.db.WithContext(ctx).Where("school_id = ?", schoolID).Order("full_name ASC").Find(&students).Error
	return students, err
}

func (r *studentRepository) CreateComplete(ctx context.Context, data *StudentComplete) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		if err := tx.Create(&data.MasterStudent).Error; err != nil {
			return err
		}

		data.StudentContact.StudentID = data.MasterStudent.ID
		if err := tx.Create(&data.StudentContact).Error; err != nil {
			return err
		}

		data.StudentFamily.StudentID = data.MasterStudent.ID
		if err := tx.Create(&data.StudentFamily).Error; err != nil {
			return err
		}

		data.StudentEnrollment.StudentID = data.MasterStudent.ID
		if err := tx.Create(&data.StudentEnrollment).Error; err != nil {
			return err
		}

		data.StudentHealth.StudentID = data.MasterStudent.ID
		if err := tx.Create(&data.StudentHealth).Error; err != nil {
			return err
		}

		return nil
	})
}

func (r *studentRepository) UpdateComplete(ctx context.Context, data *StudentComplete) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		if err := tx.Save(&data.MasterStudent).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.StudentContact).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.StudentFamily).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.StudentEnrollment).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.StudentHealth).Error; err != nil {
			return err
		}

		return nil
	})
}

func (r *studentRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		// Delete related records first
		tx.Where("student_id = ?", id).Delete(&StudentContact{})
		tx.Where("student_id = ?", id).Delete(&StudentFamily{})
		tx.Where("student_id = ?", id).Delete(&StudentEnrollment{})
		tx.Where("student_id = ?", id).Delete(&StudentHealth{})

		// Delete main record
		return tx.Delete(&MasterStudent{}, "id = ?", id).Error
	})
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
