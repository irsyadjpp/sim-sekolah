package individual_learning_plan

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type ILPRepository interface {
	// Individual Learning Plan CRUD
	CreateILP(ctx context.Context, ilp *IndividualLearningPlan) error
	GetILPByID(ctx context.Context, id uuid.UUID) (*IndividualLearningPlan, error)
	GetILPByStudentID(ctx context.Context, studentID uuid.UUID) ([]IndividualLearningPlan, error)
	GetILPByStudentAndAcademicYear(ctx context.Context, studentID, academicYearID uuid.UUID) (*IndividualLearningPlan, error)
	GetAllILPs(ctx context.Context) ([]IndividualLearningPlan, error)
	UpdateILP(ctx context.Context, ilp *IndividualLearningPlan) error
	DeleteILP(ctx context.Context, id uuid.UUID) error

	// ILP Milestone CRUD
	CreateMilestone(ctx context.Context, milestone *ILPMilestone) error
	GetMilestoneByID(ctx context.Context, id uuid.UUID) (*ILPMilestone, error)
	GetMilestonesByILPID(ctx context.Context, ilpID uuid.UUID) ([]ILPMilestone, error)
	UpdateMilestone(ctx context.Context, milestone *ILPMilestone) error
	DeleteMilestone(ctx context.Context, id uuid.UUID) error

	// ILP Template CRUD
	CreateTemplate(ctx context.Context, template *ILPTemplate) error
	GetTemplateByID(ctx context.Context, id uuid.UUID) (*ILPTemplate, error)
	GetAllTemplates(ctx context.Context) ([]ILPTemplate, error)
	GetActiveTemplates(ctx context.Context) ([]ILPTemplate, error)
	GetTemplatesByPhase(ctx context.Context, phaseID uuid.UUID) ([]ILPTemplate, error)
	UpdateTemplate(ctx context.Context, template *ILPTemplate) error
	DeleteTemplate(ctx context.Context, id uuid.UUID) error
	GetTemplateByCode(ctx context.Context, code string) (*ILPTemplate, error)
}

type ilpRepository struct {
	db *gorm.DB
}

func NewILPRepository(db *gorm.DB) ILPRepository {
	return &ilpRepository{db: db}
}

// Individual Learning Plan CRUD

func (r *ilpRepository) CreateILP(ctx context.Context, ilp *IndividualLearningPlan) error {
	return r.db.WithContext(ctx).Create(ilp).Error
}

func (r *ilpRepository) GetILPByID(ctx context.Context, id uuid.UUID) (*IndividualLearningPlan, error) {
	var ilp IndividualLearningPlan
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&ilp).Error
	if err != nil {
		return nil, err
	}
	return &ilp, nil
}

func (r *ilpRepository) GetILPByStudentID(ctx context.Context, studentID uuid.UUID) ([]IndividualLearningPlan, error) {
	var ilps []IndividualLearningPlan
	err := r.db.WithContext(ctx).Where("student_id = ? AND deleted_at IS NULL", studentID).Order("created_at DESC").Find(&ilps).Error
	return ilps, err
}

func (r *ilpRepository) GetILPByStudentAndAcademicYear(ctx context.Context, studentID, academicYearID uuid.UUID) (*IndividualLearningPlan, error) {
	var ilp IndividualLearningPlan
	err := r.db.WithContext(ctx).Where("student_id = ? AND academic_year_id = ? AND deleted_at IS NULL", studentID, academicYearID).First(&ilp).Error
	if err != nil {
		return nil, err
	}
	return &ilp, nil
}

func (r *ilpRepository) GetAllILPs(ctx context.Context) ([]IndividualLearningPlan, error) {
	var ilps []IndividualLearningPlan
	err := r.db.WithContext(ctx).Where("deleted_at IS NULL").Order("created_at DESC").Find(&ilps).Error
	return ilps, err
}

func (r *ilpRepository) UpdateILP(ctx context.Context, ilp *IndividualLearningPlan) error {
	return r.db.WithContext(ctx).Model(&IndividualLearningPlan{}).Where("id = ?", ilp.ID).Updates(ilp).Error
}

func (r *ilpRepository) DeleteILP(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Model(&IndividualLearningPlan{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

// ILP Milestone CRUD

func (r *ilpRepository) CreateMilestone(ctx context.Context, milestone *ILPMilestone) error {
	return r.db.WithContext(ctx).Create(milestone).Error
}

func (r *ilpRepository) GetMilestoneByID(ctx context.Context, id uuid.UUID) (*ILPMilestone, error) {
	var milestone ILPMilestone
	err := r.db.WithContext(ctx).Where("id = ?", id).First(&milestone).Error
	if err != nil {
		return nil, err
	}
	return &milestone, nil
}

func (r *ilpRepository) GetMilestonesByILPID(ctx context.Context, ilpID uuid.UUID) ([]ILPMilestone, error) {
	var milestones []ILPMilestone
	err := r.db.WithContext(ctx).Where("ilp_id = ?", ilpID).Order("target_date").Find(&milestones).Error
	return milestones, err
}

func (r *ilpRepository) UpdateMilestone(ctx context.Context, milestone *ILPMilestone) error {
	return r.db.WithContext(ctx).Model(&ILPMilestone{}).Where("id = ?", milestone.ID).Updates(milestone).Error
}

func (r *ilpRepository) DeleteMilestone(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&ILPMilestone{}, "id = ?", id).Error
}

// ILP Template CRUD

func (r *ilpRepository) CreateTemplate(ctx context.Context, template *ILPTemplate) error {
	return r.db.WithContext(ctx).Create(template).Error
}

func (r *ilpRepository) GetTemplateByID(ctx context.Context, id uuid.UUID) (*ILPTemplate, error) {
	var template ILPTemplate
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&template).Error
	if err != nil {
		return nil, err
	}
	return &template, nil
}

func (r *ilpRepository) GetAllTemplates(ctx context.Context) ([]ILPTemplate, error) {
	var templates []ILPTemplate
	err := r.db.WithContext(ctx).Where("deleted_at IS NULL").Order("template_code").Find(&templates).Error
	return templates, err
}

func (r *ilpRepository) GetActiveTemplates(ctx context.Context) ([]ILPTemplate, error) {
	var templates []ILPTemplate
	err := r.db.WithContext(ctx).Where("is_active = ? AND deleted_at IS NULL", true).Order("template_code").Find(&templates).Error
	return templates, err
}

func (r *ilpRepository) GetTemplatesByPhase(ctx context.Context, phaseID uuid.UUID) ([]ILPTemplate, error) {
	var templates []ILPTemplate
	err := r.db.WithContext(ctx).Where("phase_id = ? AND is_active = ? AND deleted_at IS NULL", phaseID, true).Order("template_code").Find(&templates).Error
	return templates, err
}

func (r *ilpRepository) UpdateTemplate(ctx context.Context, template *ILPTemplate) error {
	return r.db.WithContext(ctx).Model(&ILPTemplate{}).Where("id = ?", template.ID).Updates(template).Error
}

func (r *ilpRepository) DeleteTemplate(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Model(&ILPTemplate{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *ilpRepository) GetTemplateByCode(ctx context.Context, code string) (*ILPTemplate, error) {
	var template ILPTemplate
	err := r.db.WithContext(ctx).Where("template_code = ? AND deleted_at IS NULL", code).First(&template).Error
	if err != nil {
		return nil, err
	}
	return &template, nil
}
