package teacher

import (
	"context"

	"gorm.io/gorm"
)

type TeacherRepository interface {
	GetAll(ctx context.Context, limit, offset int, search string) ([]TeacherComplete, int64, error)
	GetByID(ctx context.Context, id string) (*TeacherComplete, error)
	GetBySchoolID(ctx context.Context, schoolID string) ([]TeacherComplete, error)
	CreateComplete(ctx context.Context, data *TeacherComplete) error
	UpdateComplete(ctx context.Context, data *TeacherComplete) error
	Delete(ctx context.Context, id string) error
}

type teacherRepository struct {
	db *gorm.DB
}

// NewTeacherRepository creates a new TeacherRepository with an injected *gorm.DB.
func NewTeacherRepository(db *gorm.DB) TeacherRepository {
	return &teacherRepository{db: db}
}

func (r *teacherRepository) GetAll(ctx context.Context, limit, offset int, search string) ([]TeacherComplete, int64, error) {
	var teachers []TeacherComplete
	var total int64

	query := r.db.WithContext(ctx).Model(&MasterTeacher{})
	if search != "" {
		like := "%" + search + "%"
		query = query.Where("full_name ILIKE ? OR nik ILIKE ? OR nuptk ILIKE ?", like, like, like)
	}

	query.Count(&total)
	err := query.Limit(limit).Offset(offset).Order("full_name ASC").Find(&teachers).Error
	return teachers, total, err
}

func (r *teacherRepository) GetByID(ctx context.Context, id string) (*TeacherComplete, error) {
	var t TeacherComplete
	if err := r.db.WithContext(ctx).First(&t.MasterTeacher, "id = ?", id).Error; err != nil {
		return nil, err
	}

	// Load related data
	r.db.WithContext(ctx).First(&t.TeacherContact, "teacher_id = ?", id)
	r.db.WithContext(ctx).First(&t.TeacherEmployment, "teacher_id = ?", id)
	r.db.WithContext(ctx).First(&t.TeacherEducation, "teacher_id = ?", id)
	r.db.WithContext(ctx).First(&t.TeacherCertification, "teacher_id = ?", id)
	r.db.WithContext(ctx).First(&t.TeacherPreference, "teacher_id = ?", id)

	return &t, nil
}

func (r *teacherRepository) GetBySchoolID(ctx context.Context, schoolID string) ([]TeacherComplete, error) {
	var teachers []TeacherComplete
	err := r.db.WithContext(ctx).Where("school_id = ?", schoolID).Order("full_name ASC").Find(&teachers).Error
	return teachers, err
}

func (r *teacherRepository) CreateComplete(ctx context.Context, data *TeacherComplete) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		if err := tx.Create(&data.MasterTeacher).Error; err != nil {
			return err
		}

		data.TeacherContact.TeacherID = data.MasterTeacher.ID
		if err := tx.Create(&data.TeacherContact).Error; err != nil {
			return err
		}

		data.TeacherEmployment.TeacherID = data.MasterTeacher.ID
		if err := tx.Create(&data.TeacherEmployment).Error; err != nil {
			return err
		}

		data.TeacherEducation.TeacherID = data.MasterTeacher.ID
		if err := tx.Create(&data.TeacherEducation).Error; err != nil {
			return err
		}

		data.TeacherCertification.TeacherID = data.MasterTeacher.ID
		if err := tx.Create(&data.TeacherCertification).Error; err != nil {
			return err
		}

		data.TeacherPreference.TeacherID = data.MasterTeacher.ID
		if err := tx.Create(&data.TeacherPreference).Error; err != nil {
			return err
		}

		return nil
	})
}

func (r *teacherRepository) UpdateComplete(ctx context.Context, data *TeacherComplete) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		if err := tx.Save(&data.MasterTeacher).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.TeacherContact).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.TeacherEmployment).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.TeacherEducation).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.TeacherCertification).Error; err != nil {
			return err
		}

		if err := tx.Save(&data.TeacherPreference).Error; err != nil {
			return err
		}

		return nil
	})
}

func (r *teacherRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		// Delete related records first
		tx.Where("teacher_id = ?", id).Delete(&TeacherContact{})
		tx.Where("teacher_id = ?", id).Delete(&TeacherEmployment{})
		tx.Where("teacher_id = ?", id).Delete(&TeacherEducation{})
		tx.Where("teacher_id = ?", id).Delete(&TeacherCertification{})
		tx.Where("teacher_id = ?", id).Delete(&TeacherPreference{})

		// Delete main record
		return tx.Delete(&MasterTeacher{}, "id = ?", id).Error
	})
}
