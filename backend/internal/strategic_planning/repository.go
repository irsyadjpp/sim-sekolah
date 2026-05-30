package strategic_planning

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// Repository interface defines all database operations
type Repository interface {
	// Rapor Pendidikan operations
	CreateRaporPendidikan(ctx context.Context, rapor *RaporPendidikan) error
	GetRaporPendidikanByID(ctx context.Context, id uuid.UUID) (*RaporPendidikan, error)
	GetRaporPendidikanBySchool(ctx context.Context, schoolID uuid.UUID, year string) ([]*RaporPendidikan, error)
	UpdateRaporPendidikan(ctx context.Context, rapor *RaporPendidikan) error
	DeleteRaporPendidikan(ctx context.Context, id uuid.UUID) error
	GetRaporPendidikanBySchoolYear(ctx context.Context, schoolID uuid.UUID, year, semester string) (*RaporPendidikan, error)

	// Survey operations
	CreateSurvey(ctx context.Context, survey *Survey) error
	GetSurveyByID(ctx context.Context, id uuid.UUID) (*Survey, error)
	GetSurveysBySchool(ctx context.Context, schoolID uuid.UUID, pagination Pagination) ([]*Survey, int64, error)
	UpdateSurvey(ctx context.Context, survey *Survey) error
	DeleteSurvey(ctx context.Context, id uuid.UUID) error
	GetSurveyTemplates(ctx context.Context, category string) ([]*Survey, error)
	GetActiveSurveys(ctx context.Context, schoolID uuid.UUID) ([]*Survey, error)

	// Survey Response operations
	CreateSurveyResponse(ctx context.Context, response *SurveyResponse) error
	GetSurveyResponseByID(ctx context.Context, id uuid.UUID) (*SurveyResponse, error)
	GetSurveyResponsesBySurveyID(ctx context.Context, surveyID uuid.UUID, pagination Pagination) ([]*SurveyResponse, int64, error)
	GetSurveyResponsesByRespondent(ctx context.Context, respondentID uuid.UUID) ([]*SurveyResponse, error)
	UpdateSurveyResponse(ctx context.Context, response *SurveyResponse) error
	DeleteSurveyResponse(ctx context.Context, id uuid.UUID) error

	// FGD Session operations
	CreateFGDSession(ctx context.Context, session *FGDSession) error
	GetFGDSessionByID(ctx context.Context, id uuid.UUID) (*FGDSession, error)
	GetFGDSessionsBySchool(ctx context.Context, schoolID uuid.UUID, pagination Pagination) ([]*FGDSession, int64, error)
	UpdateFGDSession(ctx context.Context, session *FGDSession) error
	DeleteFGDSession(ctx context.Context, id uuid.UUID) error
	GetUpcomingFGDSessions(ctx context.Context, schoolID uuid.UUID) ([]*FGDSession, error)

	// FGD Participant operations
	AddFGDParticipant(ctx context.Context, participant *FGDParticipant) error
	GetFGDParticipantsBySession(ctx context.Context, sessionID uuid.UUID) ([]*FGDParticipant, error)
	UpdateFGDParticipant(ctx context.Context, participant *FGDParticipant) error
	DeleteFGDParticipant(ctx context.Context, id uuid.UUID) error

	// Student Needs Enhanced operations
	CreateStudentNeedsEnhanced(ctx context.Context, needs *StudentNeedsEnhanced) error
	GetStudentNeedsEnhancedByID(ctx context.Context, id uuid.UUID) (*StudentNeedsEnhanced, error)
	GetStudentNeedsEnhancedBySchool(ctx context.Context, schoolID uuid.UUID, pagination Pagination) ([]*StudentNeedsEnhanced, int64, error)
	GetStudentNeedsEnhancedByProfile(ctx context.Context, schoolID uuid.UUID, profilDimensi string) ([]*StudentNeedsEnhanced, error)
	UpdateStudentNeedsEnhanced(ctx context.Context, needs *StudentNeedsEnhanced) error
	DeleteStudentNeedsEnhanced(ctx context.Context, id uuid.UUID) error

	// Student Needs History operations
	CreateStudentNeedsHistory(ctx context.Context, history *StudentNeedsHistory) error
	GetStudentNeedsHistoryByNeedsID(ctx context.Context, needsID uuid.UUID) ([]*StudentNeedsHistory, error)

	// SWOT Item operations
	CreateSWOTItem(ctx context.Context, item *SWOTItem) error
	GetSWOTItemByID(ctx context.Context, id uuid.UUID) (*SWOTItem, error)
	GetSWOTItemsBySchool(ctx context.Context, schoolID uuid.UUID, quadrant string) ([]*SWOTItem, error)
	GetSWOTItemsByQuadrant(ctx context.Context, schoolID uuid.UUID, quadrant string) ([]*SWOTItem, error)
	UpdateSWOTItem(ctx context.Context, item *SWOTItem) error
	DeleteSWOTItem(ctx context.Context, id uuid.UUID) error
	GetSWOTItemsBySource(ctx context.Context, sourceType string, sourceDataID uuid.UUID) ([]*SWOTItem, error)

	// SWOT Session operations
	CreateSWOTAnalysisSession(ctx context.Context, session *SWOTAnalysisSession) error
	GetSWOTAnalysisSessionByID(ctx context.Context, id uuid.UUID) (*SWOTAnalysisSession, error)
	GetSWOTSessionByID(ctx context.Context, id uuid.UUID) (*SWOTAnalysisSession, error)
	GetSWOTAnalysisSessionsBySchool(ctx context.Context, schoolID uuid.UUID) ([]*SWOTAnalysisSession, error)
	UpdateSWOTAnalysisSession(ctx context.Context, session *SWOTAnalysisSession) error
	DeleteSWOTAnalysisSession(ctx context.Context, id uuid.UUID) error
	AddSWOTItemToSession(ctx context.Context, sessionItem *SWOTSessionItem) error
	GetSWOTSessionItems(ctx context.Context, sessionID uuid.UUID) ([]*SWOTSessionItem, error)

	// Root Cause operations
	CreateRootCause(ctx context.Context, rootCause *RootCause) error
	GetRootCauseByID(ctx context.Context, id uuid.UUID) (*RootCause, error)
	GetRootCausesBySchool(ctx context.Context, schoolID uuid.UUID, status string) ([]*RootCause, error)
	GetRootCausesByRaporMetric(ctx context.Context, raporMetricID uuid.UUID) ([]*RootCause, error)
	UpdateRootCause(ctx context.Context, rootCause *RootCause) error
	DeleteRootCause(ctx context.Context, id uuid.UUID) error
	ValidateRootCause(ctx context.Context, id uuid.UUID, validatorID uuid.UUID, notes string) error

	// Root Cause History operations
	CreateRootCauseHistory(ctx context.Context, history *RootCauseHistory) error
	GetRootCauseHistoryByRootCauseID(ctx context.Context, rootCauseID uuid.UUID) ([]*RootCauseHistory, error)

	// Fishbone Diagram operations
	CreateFishboneDiagram(ctx context.Context, diagram *FishboneDiagram) error
	GetFishboneDiagramByID(ctx context.Context, id uuid.UUID) (*FishboneDiagram, error)
	GetFishboneDiagramsBySchool(ctx context.Context, schoolID uuid.UUID) ([]*FishboneDiagram, error)
	UpdateFishboneDiagram(ctx context.Context, diagram *FishboneDiagram) error
	DeleteFishboneDiagram(ctx context.Context, id uuid.UUID) error
	UpdateDiagramNodeCount(ctx context.Context, diagramID uuid.UUID) error

	// Fishbone Node operations
	CreateFishboneNode(ctx context.Context, node *FishboneNode) error
	GetFishboneNodeByID(ctx context.Context, id uuid.UUID) (*FishboneNode, error)
	GetFishboneNodesByDiagram(ctx context.Context, diagramID uuid.UUID) ([]*FishboneNode, error)
	GetFishboneNodesByCategory(ctx context.Context, diagramID uuid.UUID, category string) ([]*FishboneNode, error)
	UpdateFishboneNode(ctx context.Context, node *FishboneNode) error
	DeleteFishboneNode(ctx context.Context, id uuid.UUID) error

	// Fishbone Connection operations
	CreateFishboneConnection(ctx context.Context, connection *FishboneConnection) error
	GetFishboneConnectionsByDiagram(ctx context.Context, diagramID uuid.UUID) ([]*FishboneConnection, error)
	DeleteFishboneConnection(ctx context.Context, id uuid.UUID) error

	// KSP Analysis Integration operations
	CreateKSPAnalysisIntegration(ctx context.Context, integration *KSPAnalysisIntegration) error
	GetKSPAnalysisIntegrationByID(ctx context.Context, id uuid.UUID) (*KSPAnalysisIntegration, error)
	GetKSPAnalysisIntegrationsByDocument(ctx context.Context, documentID uuid.UUID) ([]*KSPAnalysisIntegration, error)
	UpdateKSPAnalysisIntegration(ctx context.Context, integration *KSPAnalysisIntegration) error
	DeleteKSPAnalysisIntegration(ctx context.Context, id uuid.UUID) error
	ApproveKSPAnalysisIntegration(ctx context.Context, id uuid.UUID, approverID uuid.UUID, notes string) error

	// KSP Analysis Recommendation operations
	CreateKSPAnalysisRecommendation(ctx context.Context, recommendation *KSPAnalysisRecommendation) error
	GetKSPAnalysisRecommendationsByIntegration(ctx context.Context, integrationID uuid.UUID) ([]*KSPAnalysisRecommendation, error)
	UpdateKSPAnalysisRecommendation(ctx context.Context, recommendation *KSPAnalysisRecommendation) error
	DeleteKSPAnalysisRecommendation(ctx context.Context, id uuid.UUID) error

	// KSP Analysis Template operations
	CreateKSPAnalysisTemplate(ctx context.Context, template *KSPAnalysisTemplate) error
	GetKSPAnalysisTemplateByID(ctx context.Context, id uuid.UUID) (*KSPAnalysisTemplate, error)
	GetPublicKSPAnalysisTemplates(ctx context.Context, category string) ([]*KSPAnalysisTemplate, error)
	GetKSPAnalysisTemplatesBySchool(ctx context.Context, schoolID uuid.UUID) ([]*KSPAnalysisTemplate, error)
	UpdateKSPAnalysisTemplate(ctx context.Context, template *KSPAnalysisTemplate) error
	DeleteKSPAnalysisTemplate(ctx context.Context, id uuid.UUID) error
	IncrementTemplateUsage(ctx context.Context, templateID uuid.UUID) error
}

// Pagination represents pagination parameters
type Pagination struct {
	Page   int
	Limit  int
	Offset int
}

// repository implements Repository interface
type repository struct {
	db *gorm.DB
}

// NewRepository creates a new repository instance
func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

// Rapor Pendidikan operations implementation
func (r *repository) CreateRaporPendidikan(ctx context.Context, rapor *RaporPendidikan) error {
	return r.db.WithContext(ctx).Create(rapor).Error
}

func (r *repository) GetRaporPendidikanByID(ctx context.Context, id uuid.UUID) (*RaporPendidikan, error) {
	var rapor RaporPendidikan
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&rapor).Error
	return &rapor, err
}

func (r *repository) GetRaporPendidikanBySchool(ctx context.Context, schoolID uuid.UUID, year string) ([]*RaporPendidikan, error) {
	var rapors []*RaporPendidikan
	err := r.db.WithContext(ctx).
		Where("school_id = ? AND year = ? AND deleted_at IS NULL", schoolID, year).
		Find(&rapors).Error
	return rapors, err
}

func (r *repository) UpdateRaporPendidikan(ctx context.Context, rapor *RaporPendidikan) error {
	return r.db.WithContext(ctx).Save(rapor).Error
}

func (r *repository) DeleteRaporPendidikan(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&RaporPendidikan{}).Error
}

func (r *repository) GetRaporPendidikanBySchoolYear(ctx context.Context, schoolID uuid.UUID, year, semester string) (*RaporPendidikan, error) {
	var rapor RaporPendidikan
	err := r.db.WithContext(ctx).
		Where("school_id = ? AND year = ? AND semester = ? AND deleted_at IS NULL", schoolID, year, semester).
		First(&rapor).Error
	return &rapor, err
}

// Survey operations implementation
func (r *repository) CreateSurvey(ctx context.Context, survey *Survey) error {
	return r.db.WithContext(ctx).Create(survey).Error
}

func (r *repository) GetSurveyByID(ctx context.Context, id uuid.UUID) (*Survey, error) {
	var survey Survey
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&survey).Error
	return &survey, err
}

func (r *repository) GetSurveysBySchool(ctx context.Context, schoolID uuid.UUID, pagination Pagination) ([]*Survey, int64, error) {
	var surveys []*Survey
	var total int64

	query := r.db.WithContext(ctx).Model(&Survey{}).Where("school_id = ? AND deleted_at IS NULL", schoolID)

	query.Count(&total)

	err := query.Offset(pagination.Offset).Limit(pagination.Limit).Find(&surveys).Error
	return surveys, total, err
}

func (r *repository) UpdateSurvey(ctx context.Context, survey *Survey) error {
	return r.db.WithContext(ctx).Save(survey).Error
}

func (r *repository) DeleteSurvey(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&Survey{}).Error
}

func (r *repository) GetSurveyTemplates(ctx context.Context, category string) ([]*Survey, error) {
	var templates []*Survey
	query := r.db.WithContext(ctx).Where("is_template = ? AND deleted_at IS NULL", true)

	if category != "" {
		query = query.Where("template_category = ?", category)
	}

	err := query.Find(&templates).Error
	return templates, err
}

func (r *repository) GetActiveSurveys(ctx context.Context, schoolID uuid.UUID) ([]*Survey, error) {
	var surveys []*Survey
	err := r.db.WithContext(ctx).
		Where("school_id = ? AND status = 'ACTIVE' AND deleted_at IS NULL", schoolID).
		Find(&surveys).Error
	return surveys, err
}

// Survey Response operations implementation
func (r *repository) CreateSurveyResponse(ctx context.Context, response *SurveyResponse) error {
	return r.db.WithContext(ctx).Create(response).Error
}

func (r *repository) GetSurveyResponseByID(ctx context.Context, id uuid.UUID) (*SurveyResponse, error) {
	var response SurveyResponse
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&response).Error
	return &response, err
}

func (r *repository) GetSurveyResponsesBySurveyID(ctx context.Context, surveyID uuid.UUID, pagination Pagination) ([]*SurveyResponse, int64, error) {
	var responses []*SurveyResponse
	var total int64

	query := r.db.WithContext(ctx).Model(&SurveyResponse{}).Where("survey_id = ? AND deleted_at IS NULL", surveyID)

	query.Count(&total)

	err := query.Offset(pagination.Offset).Limit(pagination.Limit).Find(&responses).Error
	return responses, total, err
}

func (r *repository) GetSurveyResponsesByRespondent(ctx context.Context, respondentID uuid.UUID) ([]*SurveyResponse, error) {
	var responses []*SurveyResponse
	err := r.db.WithContext(ctx).
		Where("respondent_id = ? AND deleted_at IS NULL", respondentID).
		Find(&responses).Error
	return responses, err
}

func (r *repository) UpdateSurveyResponse(ctx context.Context, response *SurveyResponse) error {
	return r.db.WithContext(ctx).Save(response).Error
}

func (r *repository) DeleteSurveyResponse(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&SurveyResponse{}).Error
}

// FGD Session operations implementation
func (r *repository) CreateFGDSession(ctx context.Context, session *FGDSession) error {
	return r.db.WithContext(ctx).Create(session).Error
}

func (r *repository) GetFGDSessionByID(ctx context.Context, id uuid.UUID) (*FGDSession, error) {
	var session FGDSession
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&session).Error
	return &session, err
}

func (r *repository) GetFGDSessionsBySchool(ctx context.Context, schoolID uuid.UUID, pagination Pagination) ([]*FGDSession, int64, error) {
	var sessions []*FGDSession
	var total int64

	query := r.db.WithContext(ctx).Model(&FGDSession{}).Where("school_id = ? AND deleted_at IS NULL", schoolID)

	query.Count(&total)

	err := query.Offset(pagination.Offset).Limit(pagination.Limit).Find(&sessions).Error
	return sessions, total, err
}

func (r *repository) UpdateFGDSession(ctx context.Context, session *FGDSession) error {
	return r.db.WithContext(ctx).Save(session).Error
}

func (r *repository) DeleteFGDSession(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&FGDSession{}).Error
}

func (r *repository) GetUpcomingFGDSessions(ctx context.Context, schoolID uuid.UUID) ([]*FGDSession, error) {
	var sessions []*FGDSession
	err := r.db.WithContext(ctx).
		Where("school_id = ? AND scheduled_date > NOW() AND status = 'SCHEDULED' AND deleted_at IS NULL", schoolID).
		Order("scheduled_date ASC").
		Find(&sessions).Error
	return sessions, err
}

// FGD Participant operations implementation
func (r *repository) AddFGDParticipant(ctx context.Context, participant *FGDParticipant) error {
	return r.db.WithContext(ctx).Create(participant).Error
}

func (r *repository) GetFGDParticipantsBySession(ctx context.Context, sessionID uuid.UUID) ([]*FGDParticipant, error) {
	var participants []*FGDParticipant
	err := r.db.WithContext(ctx).
		Where("fgd_session_id = ?", sessionID).
		Find(&participants).Error
	return participants, err
}

func (r *repository) UpdateFGDParticipant(ctx context.Context, participant *FGDParticipant) error {
	return r.db.WithContext(ctx).Save(participant).Error
}

func (r *repository) DeleteFGDParticipant(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&FGDParticipant{}).Error
}

// Student Needs Enhanced operations implementation
func (r *repository) CreateStudentNeedsEnhanced(ctx context.Context, needs *StudentNeedsEnhanced) error {
	return r.db.WithContext(ctx).Create(needs).Error
}

func (r *repository) GetStudentNeedsEnhancedByID(ctx context.Context, id uuid.UUID) (*StudentNeedsEnhanced, error) {
	var needs StudentNeedsEnhanced
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&needs).Error
	return &needs, err
}

func (r *repository) GetStudentNeedsEnhancedBySchool(ctx context.Context, schoolID uuid.UUID, pagination Pagination) ([]*StudentNeedsEnhanced, int64, error) {
	var needsList []*StudentNeedsEnhanced
	var total int64

	query := r.db.WithContext(ctx).Model(&StudentNeedsEnhanced{}).Where("school_id = ? AND deleted_at IS NULL", schoolID)

	query.Count(&total)

	err := query.Offset(pagination.Offset).Limit(pagination.Limit).Find(&needsList).Error
	return needsList, total, err
}

func (r *repository) GetStudentNeedsEnhancedByProfile(ctx context.Context, schoolID uuid.UUID, profilDimensi string) ([]*StudentNeedsEnhanced, error) {
	var needsList []*StudentNeedsEnhanced
	err := r.db.WithContext(ctx).
		Where("school_id = ? AND profil_dimensi = ? AND deleted_at IS NULL", schoolID, profilDimensi).
		Find(&needsList).Error
	return needsList, err
}

func (r *repository) UpdateStudentNeedsEnhanced(ctx context.Context, needs *StudentNeedsEnhanced) error {
	return r.db.WithContext(ctx).Save(needs).Error
}

func (r *repository) DeleteStudentNeedsEnhanced(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&StudentNeedsEnhanced{}).Error
}

// Student Needs History operations implementation
func (r *repository) CreateStudentNeedsHistory(ctx context.Context, history *StudentNeedsHistory) error {
	return r.db.WithContext(ctx).Create(history).Error
}

func (r *repository) GetStudentNeedsHistoryByNeedsID(ctx context.Context, needsID uuid.UUID) ([]*StudentNeedsHistory, error) {
	var historyList []*StudentNeedsHistory
	err := r.db.WithContext(ctx).
		Where("student_needs_enhanced_id = ?", needsID).
		Order("assessment_date DESC").
		Find(&historyList).Error
	return historyList, err
}

// SWOT Item operations implementation
func (r *repository) CreateSWOTItem(ctx context.Context, item *SWOTItem) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *repository) GetSWOTItemByID(ctx context.Context, id uuid.UUID) (*SWOTItem, error) {
	var item SWOTItem
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&item).Error
	return &item, err
}

func (r *repository) GetSWOTItemsBySchool(ctx context.Context, schoolID uuid.UUID, quadrant string) ([]*SWOTItem, error) {
	var items []*SWOTItem
	query := r.db.WithContext(ctx).Where("school_id = ? AND deleted_at IS NULL", schoolID)

	if quadrant != "" {
		query = query.Where("quadrant = ?", quadrant)
	}

	err := query.Order("priority ASC").Find(&items).Error
	return items, err
}

func (r *repository) GetSWOTItemsByQuadrant(ctx context.Context, schoolID uuid.UUID, quadrant string) ([]*SWOTItem, error) {
	return r.GetSWOTItemsBySchool(ctx, schoolID, quadrant)
}

func (r *repository) UpdateSWOTItem(ctx context.Context, item *SWOTItem) error {
	return r.db.WithContext(ctx).Save(item).Error
}

func (r *repository) DeleteSWOTItem(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&SWOTItem{}).Error
}

func (r *repository) GetSWOTItemsBySource(ctx context.Context, sourceType string, sourceDataID uuid.UUID) ([]*SWOTItem, error) {
	var items []*SWOTItem
	err := r.db.WithContext(ctx).
		Where("source_data_type = ? AND source_data_id = ? AND deleted_at IS NULL", sourceType, sourceDataID).
		Find(&items).Error
	return items, err
}

// SWOT Session operations implementation
func (r *repository) CreateSWOTAnalysisSession(ctx context.Context, session *SWOTAnalysisSession) error {
	return r.db.WithContext(ctx).Create(session).Error
}

func (r *repository) GetSWOTAnalysisSessionByID(ctx context.Context, id uuid.UUID) (*SWOTAnalysisSession, error) {
	var session SWOTAnalysisSession
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&session).Error
	return &session, err
}

func (r *repository) GetSWOTSessionByID(ctx context.Context, id uuid.UUID) (*SWOTAnalysisSession, error) {
	var session SWOTAnalysisSession
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&session).Error
	return &session, err
}

func (r *repository) GetSWOTAnalysisSessionsBySchool(ctx context.Context, schoolID uuid.UUID) ([]*SWOTAnalysisSession, error) {
	var sessions []*SWOTAnalysisSession
	err := r.db.WithContext(ctx).
		Where("school_id = ? AND deleted_at IS NULL", schoolID).
		Order("analysis_date DESC").
		Find(&sessions).Error
	return sessions, err
}

func (r *repository) UpdateSWOTAnalysisSession(ctx context.Context, session *SWOTAnalysisSession) error {
	return r.db.WithContext(ctx).Save(session).Error
}

func (r *repository) DeleteSWOTAnalysisSession(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&SWOTAnalysisSession{}).Error
}

func (r *repository) AddSWOTItemToSession(ctx context.Context, sessionItem *SWOTSessionItem) error {
	return r.db.WithContext(ctx).Create(sessionItem).Error
}

func (r *repository) GetSWOTSessionItems(ctx context.Context, sessionID uuid.UUID) ([]*SWOTSessionItem, error) {
	var items []*SWOTSessionItem
	err := r.db.WithContext(ctx).
		Preload("SWOTItem").
		Where("swot_session_id = ?", sessionID).
		Order("sequence_order").
		Find(&items).Error
	return items, err
}

// Root Cause operations implementation
func (r *repository) CreateRootCause(ctx context.Context, rootCause *RootCause) error {
	return r.db.WithContext(ctx).Create(rootCause).Error
}

func (r *repository) GetRootCauseByID(ctx context.Context, id uuid.UUID) (*RootCause, error) {
	var rootCause RootCause
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&rootCause).Error
	return &rootCause, err
}

func (r *repository) GetRootCausesBySchool(ctx context.Context, schoolID uuid.UUID, status string) ([]*RootCause, error) {
	var rootCauses []*RootCause
	query := r.db.WithContext(ctx).Where("school_id = ? AND deleted_at IS NULL", schoolID)

	if status != "" {
		query = query.Where("status = ?", status)
	}

	err := query.Order("action_priority ASC").Find(&rootCauses).Error
	return rootCauses, err
}

func (r *repository) GetRootCausesByRaporMetric(ctx context.Context, raporMetricID uuid.UUID) ([]*RootCause, error) {
	var rootCauses []*RootCause
	err := r.db.WithContext(ctx).
		Where("rapor_metric_id = ? AND deleted_at IS NULL", raporMetricID).
		Find(&rootCauses).Error
	return rootCauses, err
}

func (r *repository) UpdateRootCause(ctx context.Context, rootCause *RootCause) error {
	return r.db.WithContext(ctx).Save(rootCause).Error
}

func (r *repository) DeleteRootCause(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&RootCause{}).Error
}

func (r *repository) ValidateRootCause(ctx context.Context, id uuid.UUID, validatorID uuid.UUID, notes string) error {
	return r.db.WithContext(ctx).
		Model(&RootCause{}).
		Where("id = ?", id).
		Updates(map[string]interface{}{
			"is_validated":     true,
			"validated_by":     validatorID,
			"validated_at":     gorm.Expr("NOW()"),
			"validation_notes": notes,
		}).Error
}

// Root Cause History operations implementation
func (r *repository) CreateRootCauseHistory(ctx context.Context, history *RootCauseHistory) error {
	return r.db.WithContext(ctx).Create(history).Error
}

func (r *repository) GetRootCauseHistoryByRootCauseID(ctx context.Context, rootCauseID uuid.UUID) ([]*RootCauseHistory, error) {
	var historyList []*RootCauseHistory
	err := r.db.WithContext(ctx).
		Where("root_cause_id = ?", rootCauseID).
		Order("created_at DESC").
		Find(&historyList).Error
	return historyList, err
}

// Fishbone Diagram operations implementation
func (r *repository) CreateFishboneDiagram(ctx context.Context, diagram *FishboneDiagram) error {
	return r.db.WithContext(ctx).Create(diagram).Error
}

func (r *repository) GetFishboneDiagramByID(ctx context.Context, id uuid.UUID) (*FishboneDiagram, error) {
	var diagram FishboneDiagram
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&diagram).Error
	return &diagram, err
}

func (r *repository) GetFishboneDiagramsBySchool(ctx context.Context, schoolID uuid.UUID) ([]*FishboneDiagram, error) {
	var diagrams []*FishboneDiagram
	err := r.db.WithContext(ctx).
		Where("school_id = ? AND deleted_at IS NULL", schoolID).
		Order("created_at DESC").
		Find(&diagrams).Error
	return diagrams, err
}

func (r *repository) UpdateFishboneDiagram(ctx context.Context, diagram *FishboneDiagram) error {
	return r.db.WithContext(ctx).Save(diagram).Error
}

func (r *repository) DeleteFishboneDiagram(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&FishboneDiagram{}).Error
}

func (r *repository) UpdateDiagramNodeCount(ctx context.Context, diagramID uuid.UUID) error {
	return r.db.WithContext(ctx).
		Model(&FishboneDiagram{}).
		Where("id = ?", diagramID).
		Update("last_modified_at", gorm.Expr("NOW()")).Error
}

// Fishbone Node operations implementation
func (r *repository) CreateFishboneNode(ctx context.Context, node *FishboneNode) error {
	return r.db.WithContext(ctx).Create(node).Error
}

func (r *repository) GetFishboneNodeByID(ctx context.Context, id uuid.UUID) (*FishboneNode, error) {
	var node FishboneNode
	err := r.db.WithContext(ctx).Where("id = ?", id).First(&node).Error
	return &node, err
}

func (r *repository) GetFishboneNodesByDiagram(ctx context.Context, diagramID uuid.UUID) ([]*FishboneNode, error) {
	var nodes []*FishboneNode
	err := r.db.WithContext(ctx).
		Where("diagram_id = ? AND deleted_at IS NULL", diagramID).
		Order("sequence_no").
		Find(&nodes).Error
	return nodes, err
}

func (r *repository) GetFishboneNodesByCategory(ctx context.Context, diagramID uuid.UUID, category string) ([]*FishboneNode, error) {
	var nodes []*FishboneNode
	err := r.db.WithContext(ctx).
		Where("diagram_id = ? AND bone_category = ? AND deleted_at IS NULL", diagramID, category).
		Order("sequence_no").
		Find(&nodes).Error
	return nodes, err
}

func (r *repository) UpdateFishboneNode(ctx context.Context, node *FishboneNode) error {
	return r.db.WithContext(ctx).Save(node).Error
}

func (r *repository) DeleteFishboneNode(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&FishboneNode{}).Error
}

// Fishbone Connection operations implementation
func (r *repository) CreateFishboneConnection(ctx context.Context, connection *FishboneConnection) error {
	return r.db.WithContext(ctx).Create(connection).Error
}

func (r *repository) GetFishboneConnectionsByDiagram(ctx context.Context, diagramID uuid.UUID) ([]*FishboneConnection, error) {
	var connections []*FishboneConnection
	err := r.db.WithContext(ctx).
		Where("diagram_id = ?", diagramID).
		Find(&connections).Error
	return connections, err
}

func (r *repository) DeleteFishboneConnection(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&FishboneConnection{}).Error
}

// KSP Analysis Integration operations implementation
func (r *repository) CreateKSPAnalysisIntegration(ctx context.Context, integration *KSPAnalysisIntegration) error {
	return r.db.WithContext(ctx).Create(integration).Error
}

func (r *repository) GetKSPAnalysisIntegrationByID(ctx context.Context, id uuid.UUID) (*KSPAnalysisIntegration, error) {
	var integration KSPAnalysisIntegration
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&integration).Error
	return &integration, err
}

func (r *repository) GetKSPAnalysisIntegrationsByDocument(ctx context.Context, documentID uuid.UUID) ([]*KSPAnalysisIntegration, error) {
	var integrations []*KSPAnalysisIntegration
	err := r.db.WithContext(ctx).
		Where("curriculum_document_id = ? AND deleted_at IS NULL", documentID).
		Find(&integrations).Error
	return integrations, err
}

func (r *repository) UpdateKSPAnalysisIntegration(ctx context.Context, integration *KSPAnalysisIntegration) error {
	return r.db.WithContext(ctx).Save(integration).Error
}

func (r *repository) DeleteKSPAnalysisIntegration(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&KSPAnalysisIntegration{}).Error
}

func (r *repository) ApproveKSPAnalysisIntegration(ctx context.Context, id uuid.UUID, approverID uuid.UUID, notes string) error {
	return r.db.WithContext(ctx).
		Model(&KSPAnalysisIntegration{}).
		Where("id = ?", id).
		Updates(map[string]interface{}{
			"integration_status": "APPROVED",
			"approved_by":        approverID,
			"approved_at":        gorm.Expr("NOW()"),
			"approval_notes":     notes,
		}).Error
}

// KSP Analysis Recommendation operations implementation
func (r *repository) CreateKSPAnalysisRecommendation(ctx context.Context, recommendation *KSPAnalysisRecommendation) error {
	return r.db.WithContext(ctx).Create(recommendation).Error
}

func (r *repository) GetKSPAnalysisRecommendationsByIntegration(ctx context.Context, integrationID uuid.UUID) ([]*KSPAnalysisRecommendation, error) {
	var recommendations []*KSPAnalysisRecommendation
	err := r.db.WithContext(ctx).
		Where("ksp_analysis_integration_id = ?", integrationID).
		Order("priority ASC").
		Find(&recommendations).Error
	return recommendations, err
}

func (r *repository) UpdateKSPAnalysisRecommendation(ctx context.Context, recommendation *KSPAnalysisRecommendation) error {
	return r.db.WithContext(ctx).Save(recommendation).Error
}

func (r *repository) DeleteKSPAnalysisRecommendation(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&KSPAnalysisRecommendation{}).Error
}

// KSP Analysis Template operations implementation
func (r *repository) CreateKSPAnalysisTemplate(ctx context.Context, template *KSPAnalysisTemplate) error {
	return r.db.WithContext(ctx).Create(template).Error
}

func (r *repository) GetKSPAnalysisTemplateByID(ctx context.Context, id uuid.UUID) (*KSPAnalysisTemplate, error) {
	var template KSPAnalysisTemplate
	err := r.db.WithContext(ctx).Where("id = ? AND deleted_at IS NULL", id).First(&template).Error
	return &template, err
}

func (r *repository) GetPublicKSPAnalysisTemplates(ctx context.Context, category string) ([]*KSPAnalysisTemplate, error) {
	var templates []*KSPAnalysisTemplate
	query := r.db.WithContext(ctx).Where("is_public = ? AND is_active = ? AND deleted_at IS NULL", true, true)

	if category != "" {
		query = query.Where("template_category = ?", category)
	}

	err := query.Find(&templates).Error
	return templates, err
}

func (r *repository) GetKSPAnalysisTemplatesBySchool(ctx context.Context, schoolID uuid.UUID) ([]*KSPAnalysisTemplate, error) {
	var templates []*KSPAnalysisTemplate
	err := r.db.WithContext(ctx).
		Where("(school_id = ? OR school_id IS NULL) AND deleted_at IS NULL", schoolID).
		Order("created_at DESC").
		Find(&templates).Error
	return templates, err
}

func (r *repository) UpdateKSPAnalysisTemplate(ctx context.Context, template *KSPAnalysisTemplate) error {
	return r.db.WithContext(ctx).Save(template).Error
}

func (r *repository) DeleteKSPAnalysisTemplate(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Where("id = ?", id).Delete(&KSPAnalysisTemplate{}).Error
}

func (r *repository) IncrementTemplateUsage(ctx context.Context, templateID uuid.UUID) error {
	return r.db.WithContext(ctx).
		Model(&KSPAnalysisTemplate{}).
		Where("id = ?", templateID).
		UpdateColumn("usage_count", gorm.Expr("usage_count + 1")).Error
}
