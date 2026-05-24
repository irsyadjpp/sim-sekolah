package differentiated_instruction

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type DIRepository interface {
	// DI Strategy CRUD
	CreateDIStrategy(ctx context.Context, strategy *DIStrategy) error
	GetDIStrategyByID(ctx context.Context, id uuid.UUID) (*DIStrategy, error)
	GetAllDIStrategies(ctx context.Context) ([]DIStrategy, error)
	GetActiveDIStrategies(ctx context.Context) ([]DIStrategy, error)
	GetDIStrategiesByTargetGroup(ctx context.Context, targetGroup string) ([]DIStrategy, error)
	UpdateDIStrategy(ctx context.Context, strategy *DIStrategy) error
	DeleteDIStrategy(ctx context.Context, id uuid.UUID) error
	GetDIStrategyByCode(ctx context.Context, code string) (*DIStrategy, error)

	// Module Differentiation CRUD
	CreateModuleDifferentiation(ctx context.Context, differentiation *ModuleDifferentiation) error
	GetModuleDifferentiationByID(ctx context.Context, id uuid.UUID) (*ModuleDifferentiation, error)
	GetDifferentiationsByModuleID(ctx context.Context, moduleID uuid.UUID) ([]ModuleDifferentiation, error)
	GetDifferentiationsByStudentID(ctx context.Context, studentID uuid.UUID) ([]ModuleDifferentiation, error)
	UpdateModuleDifferentiation(ctx context.Context, differentiation *ModuleDifferentiation) error
	DeleteModuleDifferentiation(ctx context.Context, id uuid.UUID) error
	DeleteDifferentiationsByModuleID(ctx context.Context, moduleID uuid.UUID) error

	// Student DI Need CRUD
	CreateStudentDINeed(ctx context.Context, need *StudentDINeed) error
	GetStudentDINeedByID(ctx context.Context, id uuid.UUID) (*StudentDINeed, error)
	GetDINeedsByStudentID(ctx context.Context, studentID uuid.UUID) ([]StudentDINeed, error)
	GetActiveDINeedsByStudentID(ctx context.Context, studentID uuid.UUID) ([]StudentDINeed, error)
	GetDINeedsByStudentAndSubject(ctx context.Context, studentID, subjectID uuid.UUID) ([]StudentDINeed, error)
	UpdateStudentDINeed(ctx context.Context, need *StudentDINeed) error
	DeleteStudentDINeed(ctx context.Context, id uuid.UUID) error
	GetAllStudentDINeeds(ctx context.Context) ([]StudentDINeed, error)
}

type diRepository struct {
	db *gorm.DB
}

func NewDIRepository(db *gorm.DB) DIRepository {
	return &diRepository{db: db}
}

// DI Strategy CRUD

func (r *diRepository) CreateDIStrategy(ctx context.Context, strategy *DIStrategy) error {
	return r.db.WithContext(ctx).Create(strategy).Error
}

func (r *diRepository) GetDIStrategyByID(ctx context.Context, id uuid.UUID) (*DIStrategy, error) {
	var strategy DIStrategy
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&strategy).Error
	if err != nil {
		return nil, err
	}
	return &strategy, nil
}

func (r *diRepository) GetAllDIStrategies(ctx context.Context) ([]DIStrategy, error) {
	var strategies []DIStrategy
	err := r.db.WithContext(ctx).Where("deleted_at IS NULL").Order("strategy_code").Find(&strategies).Error
	return strategies, err
}

func (r *diRepository) GetActiveDIStrategies(ctx context.Context) ([]DIStrategy, error) {
	var strategies []DIStrategy
	err := r.db.WithContext(ctx).Where("is_active = ? AND deleted_at IS NULL", true).Order("strategy_code").Find(&strategies).Error
	return strategies, err
}

func (r *diRepository) GetDIStrategiesByTargetGroup(ctx context.Context, targetGroup string) ([]DIStrategy, error) {
	var strategies []DIStrategy
	err := r.db.WithContext(ctx).Where("target_group = ? AND is_active = ? AND deleted_at IS NULL", targetGroup, true).Order("strategy_code").Find(&strategies).Error
	return strategies, err
}

func (r *diRepository) UpdateDIStrategy(ctx context.Context, strategy *DIStrategy) error {
	return r.db.WithContext(ctx).Model(&DIStrategy{}).Where("id = ?", strategy.ID).Updates(strategy).Error
}

func (r *diRepository) DeleteDIStrategy(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Model(&DIStrategy{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *diRepository) GetDIStrategyByCode(ctx context.Context, code string) (*DIStrategy, error) {
	var strategy DIStrategy
	err := r.db.WithContext(ctx).Where("strategy_code = ? AND deleted_at IS NULL", code).First(&strategy).Error
	if err != nil {
		return nil, err
	}
	return &strategy, nil
}

// Module Differentiation CRUD

func (r *diRepository) CreateModuleDifferentiation(ctx context.Context, differentiation *ModuleDifferentiation) error {
	return r.db.WithContext(ctx).Preload("Strategy").Create(differentiation).Error
}

func (r *diRepository) GetModuleDifferentiationByID(ctx context.Context, id uuid.UUID) (*ModuleDifferentiation, error) {
	var differentiation ModuleDifferentiation
	err := r.db.WithContext(ctx).Preload("Strategy").Where("id = ?", id).First(&differentiation).Error
	if err != nil {
		return nil, err
	}
	return &differentiation, nil
}

func (r *diRepository) GetDifferentiationsByModuleID(ctx context.Context, moduleID uuid.UUID) ([]ModuleDifferentiation, error) {
	var differentiations []ModuleDifferentiation
	err := r.db.WithContext(ctx).Preload("Strategy").Where("module_id = ?", moduleID).Order("created_at").Find(&differentiations).Error
	return differentiations, err
}

func (r *diRepository) GetDifferentiationsByStudentID(ctx context.Context, studentID uuid.UUID) ([]ModuleDifferentiation, error) {
	var differentiations []ModuleDifferentiation
	// This is a simplified query - in practice, you'd need to parse the JSON array
	err := r.db.WithContext(ctx).Preload("Strategy").Where("target_students LIKE ?", "%"+studentID.String()+"%").Order("created_at").Find(&differentiations).Error
	return differentiations, err
}

func (r *diRepository) UpdateModuleDifferentiation(ctx context.Context, differentiation *ModuleDifferentiation) error {
	return r.db.WithContext(ctx).Model(&ModuleDifferentiation{}).Where("id = ?", differentiation.ID).Updates(differentiation).Error
}

func (r *diRepository) DeleteModuleDifferentiation(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&ModuleDifferentiation{}, "id = ?", id).Error
}

func (r *diRepository) DeleteDifferentiationsByModuleID(ctx context.Context, moduleID uuid.UUID) error {
	return r.db.WithContext(ctx).Where("module_id = ?", moduleID).Delete(&ModuleDifferentiation{}).Error
}

// Student DI Need CRUD

func (r *diRepository) CreateStudentDINeed(ctx context.Context, need *StudentDINeed) error {
	return r.db.WithContext(ctx).Create(need).Error
}

func (r *diRepository) GetStudentDINeedByID(ctx context.Context, id uuid.UUID) (*StudentDINeed, error) {
	var need StudentDINeed
	err := r.db.WithContext(ctx).Where("id = ?", id).First(&need).Error
	if err != nil {
		return nil, err
	}
	return &need, nil
}

func (r *diRepository) GetDINeedsByStudentID(ctx context.Context, studentID uuid.UUID) ([]StudentDINeed, error) {
	var needs []StudentDINeed
	err := r.db.WithContext(ctx).Where("student_id = ?", studentID).Order("assessment_date DESC").Find(&needs).Error
	return needs, err
}

func (r *diRepository) GetActiveDINeedsByStudentID(ctx context.Context, studentID uuid.UUID) ([]StudentDINeed, error) {
	var needs []StudentDINeed
	err := r.db.WithContext(ctx).Where("student_id = ? AND is_active = ?", studentID, true).Order("assessment_date DESC").Find(&needs).Error
	return needs, err
}

func (r *diRepository) GetDINeedsByStudentAndSubject(ctx context.Context, studentID, subjectID uuid.UUID) ([]StudentDINeed, error) {
	var needs []StudentDINeed
	err := r.db.WithContext(ctx).Where("student_id = ? AND subject_id = ?", studentID, subjectID).Order("assessment_date DESC").Find(&needs).Error
	return needs, err
}

func (r *diRepository) UpdateStudentDINeed(ctx context.Context, need *StudentDINeed) error {
	return r.db.WithContext(ctx).Model(&StudentDINeed{}).Where("id = ?", need.ID).Updates(need).Error
}

func (r *diRepository) DeleteStudentDINeed(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&StudentDINeed{}, "id = ?", id).Error
}

func (r *diRepository) GetAllStudentDINeeds(ctx context.Context) ([]StudentDINeed, error) {
	var needs []StudentDINeed
	err := r.db.WithContext(ctx).Find(&needs).Error
	return needs, err
}
