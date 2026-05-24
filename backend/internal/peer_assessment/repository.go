package peer_assessment

import (
	"context"

	"gorm.io/gorm"
)

type PeerAssessmentRepository interface {
	// PeerAssessmentTemplate
	GetAllTemplates(ctx context.Context) ([]PeerAssessmentTemplate, error)
	GetTemplateByID(ctx context.Context, id string) (*PeerAssessmentTemplate, error)
	GetTemplatesByType(ctx context.Context, assessmentType string) ([]PeerAssessmentTemplate, error)
	GetTemplatesByPhase(ctx context.Context, phase string) ([]PeerAssessmentTemplate, error)
	GetTemplatesBySubject(ctx context.Context, subjectID string) ([]PeerAssessmentTemplate, error)
	GetActiveTemplates(ctx context.Context) ([]PeerAssessmentTemplate, error)
	CreateTemplate(ctx context.Context, data *PeerAssessmentTemplate) error
	UpdateTemplate(ctx context.Context, data *PeerAssessmentTemplate) error
	DeleteTemplate(ctx context.Context, id string) error

	// SelfAssessment
	GetAllSelfAssessments(ctx context.Context) ([]SelfAssessment, error)
	GetSelfAssessmentByID(ctx context.Context, id string) (*SelfAssessment, error)
	GetSelfAssessmentsByStudent(ctx context.Context, studentID string) ([]SelfAssessment, error)
	GetSelfAssessmentsByTemplate(ctx context.Context, templateID string) ([]SelfAssessment, error)
	CreateSelfAssessment(ctx context.Context, data *SelfAssessment) error
	UpdateSelfAssessment(ctx context.Context, data *SelfAssessment) error
	DeleteSelfAssessment(ctx context.Context, id string) error

	// PeerAssessment
	GetAllPeerAssessments(ctx context.Context) ([]PeerAssessment, error)
	GetPeerAssessmentByID(ctx context.Context, id string) (*PeerAssessment, error)
	GetPeerAssessmentsByAssessor(ctx context.Context, assessorID string) ([]PeerAssessment, error)
	GetPeerAssessmentsByAssessed(ctx context.Context, assessedID string) ([]PeerAssessment, error)
	GetPeerAssessmentsByTemplate(ctx context.Context, templateID string) ([]PeerAssessment, error)
	GetPendingPeerReviews(ctx context.Context) ([]PeerAssessment, error)
	CreatePeerAssessment(ctx context.Context, data *PeerAssessment) error
	UpdatePeerAssessment(ctx context.Context, data *PeerAssessment) error
	DeletePeerAssessment(ctx context.Context, id string) error

	// GroupAssessment
	GetAllGroupAssessments(ctx context.Context) ([]GroupAssessment, error)
	GetGroupAssessmentByID(ctx context.Context, id string) (*GroupAssessment, error)
	GetGroupAssessmentsByGroup(ctx context.Context, groupID string) ([]GroupAssessment, error)
	GetGroupAssessmentsByTemplate(ctx context.Context, templateID string) ([]GroupAssessment, error)
	CreateGroupAssessment(ctx context.Context, data *GroupAssessment) error
	UpdateGroupAssessment(ctx context.Context, data *GroupAssessment) error
	DeleteGroupAssessment(ctx context.Context, id string) error

	// GroupAssessmentMember
	GetAllGroupAssessmentMembers(ctx context.Context) ([]GroupAssessmentMember, error)
	GetGroupAssessmentMemberByID(ctx context.Context, id string) (*GroupAssessmentMember, error)
	GetGroupAssessmentMembersByGroupAssessment(ctx context.Context, groupAssessmentID string) ([]GroupAssessmentMember, error)
	GetGroupAssessmentMembersByStudent(ctx context.Context, studentID string) ([]GroupAssessmentMember, error)
	CreateGroupAssessmentMember(ctx context.Context, data *GroupAssessmentMember) error
	UpdateGroupAssessmentMember(ctx context.Context, data *GroupAssessmentMember) error
	DeleteGroupAssessmentMember(ctx context.Context, id string) error

	// PeerAssessmentGuideline
	GetAllGuidelines(ctx context.Context) ([]PeerAssessmentGuideline, error)
	GetGuidelineByID(ctx context.Context, id string) (*PeerAssessmentGuideline, error)
	GetGuidelinesByPhase(ctx context.Context, phase string) ([]PeerAssessmentGuideline, error)
	GetGuidelinesByCategory(ctx context.Context, category string) ([]PeerAssessmentGuideline, error)
	GetActiveGuidelines(ctx context.Context) ([]PeerAssessmentGuideline, error)
	CreateGuideline(ctx context.Context, data *PeerAssessmentGuideline) error
	UpdateGuideline(ctx context.Context, data *PeerAssessmentGuideline) error
	DeleteGuideline(ctx context.Context, id string) error

	// Summary
	GetPeerAssessmentSummary(ctx context.Context) (*PeerAssessmentSummaryResponse, error)
}

type peerAssessmentRepository struct {
	db *gorm.DB
}

func NewPeerAssessmentRepository(db *gorm.DB) PeerAssessmentRepository {
	return &peerAssessmentRepository{db: db}
}

// PeerAssessmentTemplate Methods
func (r *peerAssessmentRepository) GetAllTemplates(ctx context.Context) ([]PeerAssessmentTemplate, error) {
	var templates []PeerAssessmentTemplate
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("phase, assessment_type, assessment_focus ASC").
		Find(&templates).Error
	return templates, err
}

func (r *peerAssessmentRepository) GetTemplateByID(ctx context.Context, id string) (*PeerAssessmentTemplate, error) {
	var template PeerAssessmentTemplate
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&template).Error
	if err != nil {
		return nil, err
	}
	return &template, nil
}

func (r *peerAssessmentRepository) GetTemplatesByType(ctx context.Context, assessmentType string) ([]PeerAssessmentTemplate, error) {
	var templates []PeerAssessmentTemplate
	err := r.db.WithContext(ctx).
		Where("assessment_type = ? AND is_active = true AND deleted_at IS NULL", assessmentType).
		Order("phase, assessment_focus ASC").
		Find(&templates).Error
	return templates, err
}

func (r *peerAssessmentRepository) GetTemplatesByPhase(ctx context.Context, phase string) ([]PeerAssessmentTemplate, error) {
	var templates []PeerAssessmentTemplate
	err := r.db.WithContext(ctx).
		Where("phase = ? AND is_active = true AND deleted_at IS NULL", phase).
		Order("assessment_type, assessment_focus ASC").
		Find(&templates).Error
	return templates, err
}

func (r *peerAssessmentRepository) GetTemplatesBySubject(ctx context.Context, subjectID string) ([]PeerAssessmentTemplate, error) {
	var templates []PeerAssessmentTemplate
	err := r.db.WithContext(ctx).
		Where("subject_id = ? AND is_active = true AND deleted_at IS NULL", subjectID).
		Order("phase, assessment_type ASC").
		Find(&templates).Error
	return templates, err
}

func (r *peerAssessmentRepository) GetActiveTemplates(ctx context.Context) ([]PeerAssessmentTemplate, error) {
	var templates []PeerAssessmentTemplate
	err := r.db.WithContext(ctx).
		Where("is_active = true AND deleted_at IS NULL").
		Order("phase, assessment_type, assessment_focus ASC").
		Find(&templates).Error
	return templates, err
}

func (r *peerAssessmentRepository) CreateTemplate(ctx context.Context, data *PeerAssessmentTemplate) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *peerAssessmentRepository) UpdateTemplate(ctx context.Context, data *PeerAssessmentTemplate) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *peerAssessmentRepository) DeleteTemplate(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&PeerAssessmentTemplate{}).Error
}

// SelfAssessment Methods
func (r *peerAssessmentRepository) GetAllSelfAssessments(ctx context.Context) ([]SelfAssessment, error) {
	var assessments []SelfAssessment
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) GetSelfAssessmentByID(ctx context.Context, id string) (*SelfAssessment, error) {
	var assessment SelfAssessment
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&assessment).Error
	if err != nil {
		return nil, err
	}
	return &assessment, nil
}

func (r *peerAssessmentRepository) GetSelfAssessmentsByStudent(ctx context.Context, studentID string) ([]SelfAssessment, error) {
	var assessments []SelfAssessment
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND deleted_at IS NULL", studentID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) GetSelfAssessmentsByTemplate(ctx context.Context, templateID string) ([]SelfAssessment, error) {
	var assessments []SelfAssessment
	err := r.db.WithContext(ctx).
		Where("template_id = ? AND deleted_at IS NULL", templateID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) CreateSelfAssessment(ctx context.Context, data *SelfAssessment) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *peerAssessmentRepository) UpdateSelfAssessment(ctx context.Context, data *SelfAssessment) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *peerAssessmentRepository) DeleteSelfAssessment(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&SelfAssessment{}).Error
}

// PeerAssessment Methods
func (r *peerAssessmentRepository) GetAllPeerAssessments(ctx context.Context) ([]PeerAssessment, error) {
	var assessments []PeerAssessment
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) GetPeerAssessmentByID(ctx context.Context, id string) (*PeerAssessment, error) {
	var assessment PeerAssessment
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&assessment).Error
	if err != nil {
		return nil, err
	}
	return &assessment, nil
}

func (r *peerAssessmentRepository) GetPeerAssessmentsByAssessor(ctx context.Context, assessorID string) ([]PeerAssessment, error) {
	var assessments []PeerAssessment
	err := r.db.WithContext(ctx).
		Where("assessor_student_id = ? AND deleted_at IS NULL", assessorID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) GetPeerAssessmentsByAssessed(ctx context.Context, assessedID string) ([]PeerAssessment, error) {
	var assessments []PeerAssessment
	err := r.db.WithContext(ctx).
		Where("assessed_student_id = ? AND deleted_at IS NULL", assessedID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) GetPeerAssessmentsByTemplate(ctx context.Context, templateID string) ([]PeerAssessment, error) {
	var assessments []PeerAssessment
	err := r.db.WithContext(ctx).
		Where("template_id = ? AND deleted_at IS NULL", templateID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) GetPendingPeerReviews(ctx context.Context) ([]PeerAssessment, error) {
	var assessments []PeerAssessment
	err := r.db.WithContext(ctx).
		Where("teacher_review_status = ? AND deleted_at IS NULL", ReviewStatusPending).
		Order("assessment_date ASC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) CreatePeerAssessment(ctx context.Context, data *PeerAssessment) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *peerAssessmentRepository) UpdatePeerAssessment(ctx context.Context, data *PeerAssessment) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *peerAssessmentRepository) DeletePeerAssessment(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&PeerAssessment{}).Error
}

// GroupAssessment Methods
func (r *peerAssessmentRepository) GetAllGroupAssessments(ctx context.Context) ([]GroupAssessment, error) {
	var assessments []GroupAssessment
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) GetGroupAssessmentByID(ctx context.Context, id string) (*GroupAssessment, error) {
	var assessment GroupAssessment
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&assessment).Error
	if err != nil {
		return nil, err
	}
	return &assessment, nil
}

func (r *peerAssessmentRepository) GetGroupAssessmentsByGroup(ctx context.Context, groupID string) ([]GroupAssessment, error) {
	var assessments []GroupAssessment
	err := r.db.WithContext(ctx).
		Where("group_id = ? AND deleted_at IS NULL", groupID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) GetGroupAssessmentsByTemplate(ctx context.Context, templateID string) ([]GroupAssessment, error) {
	var assessments []GroupAssessment
	err := r.db.WithContext(ctx).
		Where("template_id = ? AND deleted_at IS NULL", templateID).
		Order("assessment_date DESC").
		Find(&assessments).Error
	return assessments, err
}

func (r *peerAssessmentRepository) CreateGroupAssessment(ctx context.Context, data *GroupAssessment) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *peerAssessmentRepository) UpdateGroupAssessment(ctx context.Context, data *GroupAssessment) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *peerAssessmentRepository) DeleteGroupAssessment(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&GroupAssessment{}).Error
}

// GroupAssessmentMember Methods
func (r *peerAssessmentRepository) GetAllGroupAssessmentMembers(ctx context.Context) ([]GroupAssessmentMember, error) {
	var members []GroupAssessmentMember
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("created_at DESC").
		Find(&members).Error
	return members, err
}

func (r *peerAssessmentRepository) GetGroupAssessmentMemberByID(ctx context.Context, id string) (*GroupAssessmentMember, error) {
	var member GroupAssessmentMember
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&member).Error
	if err != nil {
		return nil, err
	}
	return &member, nil
}

func (r *peerAssessmentRepository) GetGroupAssessmentMembersByGroupAssessment(ctx context.Context, groupAssessmentID string) ([]GroupAssessmentMember, error) {
	var members []GroupAssessmentMember
	err := r.db.WithContext(ctx).
		Where("group_assessment_id = ? AND deleted_at IS NULL", groupAssessmentID).
		Order("created_at ASC").
		Find(&members).Error
	return members, err
}

func (r *peerAssessmentRepository) GetGroupAssessmentMembersByStudent(ctx context.Context, studentID string) ([]GroupAssessmentMember, error) {
	var members []GroupAssessmentMember
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND deleted_at IS NULL", studentID).
		Order("created_at DESC").
		Find(&members).Error
	return members, err
}

func (r *peerAssessmentRepository) CreateGroupAssessmentMember(ctx context.Context, data *GroupAssessmentMember) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *peerAssessmentRepository) UpdateGroupAssessmentMember(ctx context.Context, data *GroupAssessmentMember) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *peerAssessmentRepository) DeleteGroupAssessmentMember(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&GroupAssessmentMember{}).Error
}

// PeerAssessmentGuideline Methods
func (r *peerAssessmentRepository) GetAllGuidelines(ctx context.Context) ([]PeerAssessmentGuideline, error) {
	var guidelines []PeerAssessmentGuideline
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("phase, guideline_category, display_order ASC").
		Find(&guidelines).Error
	return guidelines, err
}

func (r *peerAssessmentRepository) GetGuidelineByID(ctx context.Context, id string) (*PeerAssessmentGuideline, error) {
	var guideline PeerAssessmentGuideline
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&guideline).Error
	if err != nil {
		return nil, err
	}
	return &guideline, nil
}

func (r *peerAssessmentRepository) GetGuidelinesByPhase(ctx context.Context, phase string) ([]PeerAssessmentGuideline, error) {
	var guidelines []PeerAssessmentGuideline
	err := r.db.WithContext(ctx).
		Where("phase = ? AND is_active = true AND deleted_at IS NULL", phase).
		Order("guideline_category, display_order ASC").
		Find(&guidelines).Error
	return guidelines, err
}

func (r *peerAssessmentRepository) GetGuidelinesByCategory(ctx context.Context, category string) ([]PeerAssessmentGuideline, error) {
	var guidelines []PeerAssessmentGuideline
	err := r.db.WithContext(ctx).
		Where("guideline_category = ? AND is_active = true AND deleted_at IS NULL", category).
		Order("phase, display_order ASC").
		Find(&guidelines).Error
	return guidelines, err
}

func (r *peerAssessmentRepository) GetActiveGuidelines(ctx context.Context) ([]PeerAssessmentGuideline, error) {
	var guidelines []PeerAssessmentGuideline
	err := r.db.WithContext(ctx).
		Where("is_active = true AND deleted_at IS NULL").
		Order("phase, guideline_category, display_order ASC").
		Find(&guidelines).Error
	return guidelines, err
}

func (r *peerAssessmentRepository) CreateGuideline(ctx context.Context, data *PeerAssessmentGuideline) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *peerAssessmentRepository) UpdateGuideline(ctx context.Context, data *PeerAssessmentGuideline) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *peerAssessmentRepository) DeleteGuideline(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&PeerAssessmentGuideline{}).Error
}

// Summary Method
func (r *peerAssessmentRepository) GetPeerAssessmentSummary(ctx context.Context) (*PeerAssessmentSummaryResponse, error) {
	var totalTemplates int64
	r.db.WithContext(ctx).Model(&PeerAssessmentTemplate{}).Count(&totalTemplates)

	var activeTemplates int64
	r.db.WithContext(ctx).Model(&PeerAssessmentTemplate{}).Where("is_active = true").Count(&activeTemplates)

	var totalSelfAssessments int64
	r.db.WithContext(ctx).Model(&SelfAssessment{}).Count(&totalSelfAssessments)

	var totalPeerAssessments int64
	r.db.WithContext(ctx).Model(&PeerAssessment{}).Count(&totalPeerAssessments)

	var totalGroupAssessments int64
	r.db.WithContext(ctx).Model(&GroupAssessment{}).Count(&totalGroupAssessments)

	var pendingPeerReviews int64
	r.db.WithContext(ctx).Model(&PeerAssessment{}).Where("teacher_review_status = ?", ReviewStatusPending).Count(&pendingPeerReviews)

	var totalGuidelines int64
	r.db.WithContext(ctx).Model(&PeerAssessmentGuideline{}).Count(&totalGuidelines)

	return &PeerAssessmentSummaryResponse{
		TotalTemplates:        int(totalTemplates),
		ActiveTemplates:       int(activeTemplates),
		TotalSelfAssessments:  int(totalSelfAssessments),
		TotalPeerAssessments:  int(totalPeerAssessments),
		TotalGroupAssessments: int(totalGroupAssessments),
		PendingPeerReviews:    int(pendingPeerReviews),
		TotalGuidelines:       int(totalGuidelines),
	}, nil
}
