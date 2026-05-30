package strategic_planning

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"strings"
	"time"

	"sim-sekolah/internal/common"

	grpc_clients "sim-sekolah/internal/ai/grpc"
	pb "sim-sekolah/internal/ai/grpc/pb/strategicanalysisservice"

	"github.com/google/uuid"
)

// Service interface defines all business logic operations
type Service interface {
	// Rapor Pendidikan operations
	CreateRaporPendidikan(ctx context.Context, req CreateRaporPendidikanRequest) (*RaporPendidikan, error)
	GetRaporPendidikanByID(ctx context.Context, id string) (*RaporPendidikan, error)
	GetRaporPendidikanBySchool(ctx context.Context, schoolID string, year string) ([]*RaporPendidikan, error)
	UpdateRaporPendidikan(ctx context.Context, id string, req UpdateRaporPendidikanRequest) (*RaporPendidikan, error)
	DeleteRaporPendidikan(ctx context.Context, id string) error
	SyncRaporPendidikan(ctx context.Context, req SyncRaporPendidikanRequest) (*RaporPendidikan, error)

	// Survey operations
	CreateSurvey(ctx context.Context, req CreateSurveyRequest) (*Survey, error)
	GetSurveyByID(ctx context.Context, id string) (*Survey, error)
	GetSurveysBySchool(ctx context.Context, schoolID string, pagination common.Pagination) ([]*Survey, int64, error)
	UpdateSurvey(ctx context.Context, id string, req UpdateSurveyRequest) (*Survey, error)
	DeleteSurvey(ctx context.Context, id string) error
	GetSurveyTemplates(ctx context.Context, category string) ([]*Survey, error)
	GetActiveSurveys(ctx context.Context, schoolID string) ([]*Survey, error)
	SubmitSurveyResponse(ctx context.Context, req CreateSurveyResponseRequest) (*SurveyResponse, error)
	GetSurveyResponses(ctx context.Context, surveyID string, pagination common.Pagination) ([]*SurveyResponse, int64, error)
	GetSurveyAnalytics(ctx context.Context, surveyID string) (*SurveyAnalyticsResponse, error)

	// FGD Session operations
	CreateFGDSession(ctx context.Context, req CreateFGDSessionRequest) (*FGDSession, error)
	GetFGDSessionByID(ctx context.Context, id string) (*FGDSession, error)
	GetFGDSessionsBySchool(ctx context.Context, schoolID string, pagination common.Pagination) ([]*FGDSession, int64, error)
	UpdateFGDSession(ctx context.Context, id string, req UpdateFGDSessionRequest) (*FGDSession, error)
	DeleteFGDSession(ctx context.Context, id string) error
	GetUpcomingFGDSessions(ctx context.Context, schoolID string) ([]*FGDSession, error)
	AddFGDParticipant(ctx context.Context, req AddFGDParticipantRequest) (*FGDParticipant, error)
	GetFGDParticipants(ctx context.Context, sessionID string) ([]*FGDParticipant, error)
	UpdateFGDParticipant(ctx context.Context, id string, req UpdateFGDParticipantRequest) (*FGDParticipant, error)
	DeleteFGDParticipant(ctx context.Context, id string) error

	// Student Needs Enhanced operations
	CreateStudentNeedsEnhanced(ctx context.Context, req CreateStudentNeedsEnhancedRequest) (*StudentNeedsEnhanced, error)
	GetStudentNeedsEnhancedByID(ctx context.Context, id string) (*StudentNeedsEnhanced, error)
	GetStudentNeedsEnhancedBySchool(ctx context.Context, schoolID string, pagination common.Pagination) ([]*StudentNeedsEnhanced, int64, error)
	GetStudentNeedsEnhancedByProfile(ctx context.Context, schoolID string, profilDimensi string) ([]*StudentNeedsEnhanced, error)
	UpdateStudentNeedsEnhanced(ctx context.Context, id string, req UpdateStudentNeedsEnhancedRequest) (*StudentNeedsEnhanced, error)
	DeleteStudentNeedsEnhanced(ctx context.Context, id string) error

	// SWOT operations
	CreateSWOTItem(ctx context.Context, req CreateSWOTItemRequest) (*SWOTItem, error)
	GetSWOTItemByID(ctx context.Context, id string) (*SWOTItem, error)
	GetSWOTItemsBySchool(ctx context.Context, schoolID string, quadrant string) ([]*SWOTItem, error)
	UpdateSWOTItem(ctx context.Context, id string, req UpdateSWOTItemRequest) (*SWOTItem, error)
	DeleteSWOTItem(ctx context.Context, id string) error
	CreateSWOTAnalysisSession(ctx context.Context, req CreateSWOTAnalysisSessionRequest) (*SWOTAnalysisSession, error)
	GetSWOTAnalysisSessionByID(ctx context.Context, id string) (*SWOTAnalysisSession, error)
	GetSWOTAnalysisSessionsBySchool(ctx context.Context, schoolID string) ([]*SWOTAnalysisSession, error)
	UpdateSWOTAnalysisSession(ctx context.Context, id string, req UpdateSWOTAnalysisSessionRequest) (*SWOTAnalysisSession, error)
	DeleteSWOTAnalysisSession(ctx context.Context, id string) error
	AddSWOTItemToSession(ctx context.Context, req AddSWOTSessionItemRequest) error
	GetSWOTSessionItems(ctx context.Context, sessionID string) ([]*SWOTSessionItem, error)

	// Root Cause operations
	CreateRootCause(ctx context.Context, req CreateRootCauseRequest) (*RootCause, error)
	GetRootCauseByID(ctx context.Context, id string) (*RootCause, error)
	GetRootCausesBySchool(ctx context.Context, schoolID string, status string) ([]*RootCause, error)
	UpdateRootCause(ctx context.Context, id string, req UpdateRootCauseRequest) (*RootCause, error)
	DeleteRootCause(ctx context.Context, id string) error
	ValidateRootCause(ctx context.Context, id string, req ValidateRootCauseRequest) error
	GetRootCauseHistory(ctx context.Context, rootCauseID string) ([]*RootCauseHistory, error)

	// Fishbone operations
	CreateFishboneDiagram(ctx context.Context, req CreateFishboneDiagramRequest) (*FishboneDiagram, error)
	GetFishboneDiagramByID(ctx context.Context, id string) (*FishboneDiagram, error)
	GetFishboneDiagramsBySchool(ctx context.Context, schoolID string) ([]*FishboneDiagram, error)
	UpdateFishboneDiagram(ctx context.Context, id string, req UpdateFishboneDiagramRequest) (*FishboneDiagram, error)
	DeleteFishboneDiagram(ctx context.Context, id string) error
	CreateFishboneNode(ctx context.Context, req CreateFishboneNodeRequest) (*FishboneNode, error)
	GetFishboneNodesByDiagram(ctx context.Context, diagramID string) ([]*FishboneNode, error)
	UpdateFishboneNode(ctx context.Context, id string, req UpdateFishboneNodeRequest) (*FishboneNode, error)
	DeleteFishboneNode(ctx context.Context, id string) error
	CreateFishboneConnection(ctx context.Context, req CreateFishboneConnectionRequest) (*FishboneConnection, error)
	GetFishboneConnections(ctx context.Context, diagramID string) ([]*FishboneConnection, error)
	DeleteFishboneConnection(ctx context.Context, id string) error

	// KSP Integration operations
	CreateKSPAnalysisIntegration(ctx context.Context, req CreateKSPAnalysisIntegrationRequest) (*KSPAnalysisIntegration, error)
	GetKSPAnalysisIntegrationByID(ctx context.Context, id string) (*KSPAnalysisIntegration, error)
	GetKSPAnalysisIntegrationsByDocument(ctx context.Context, documentID string) ([]*KSPAnalysisIntegration, error)
	UpdateKSPAnalysisIntegration(ctx context.Context, id string, req UpdateKSPAnalysisIntegrationRequest) (*KSPAnalysisIntegration, error)
	DeleteKSPAnalysisIntegration(ctx context.Context, id string) error
	ApproveKSPAnalysisIntegration(ctx context.Context, id string, req ApproveKSPAnalysisIntegrationRequest) error
	CreateKSPAnalysisRecommendation(ctx context.Context, req CreateKSPAnalysisRecommendationRequest) (*KSPAnalysisRecommendation, error)
	GetKSPAnalysisRecommendations(ctx context.Context, integrationID string) ([]*KSPAnalysisRecommendation, error)
	UpdateKSPAnalysisRecommendation(ctx context.Context, id string, req UpdateKSPAnalysisRecommendationRequest) (*KSPAnalysisRecommendation, error)
	DeleteKSPAnalysisRecommendation(ctx context.Context, id string) error
	CreateKSPAnalysisTemplate(ctx context.Context, req CreateKSPAnalysisTemplateRequest) (*KSPAnalysisTemplate, error)
	GetKSPAnalysisTemplateByID(ctx context.Context, id string) (*KSPAnalysisTemplate, error)
	GetPublicKSPAnalysisTemplates(ctx context.Context, category string) ([]*KSPAnalysisTemplate, error)
	GetKSPAnalysisTemplatesBySchool(ctx context.Context, schoolID string) ([]*KSPAnalysisTemplate, error)
	UpdateKSPAnalysisTemplate(ctx context.Context, id string, req UpdateKSPAnalysisTemplateRequest) (*KSPAnalysisTemplate, error)
	DeleteKSPAnalysisTemplate(ctx context.Context, id string) error

	// FASE 4: Integration operations

	// Local Context Integration (FR 2.1)
	GetLocalContextForSWOT(ctx context.Context, schoolID string) (*LocalContextAnalysisResponse, error)
	AnalyzeLearningPotential(ctx context.Context, schoolID string) (*LearningPotentialAnalysisResponse, error)
	GetEnhancedLocalCategories(ctx context.Context, schoolID string) ([]*EnhancedCategoryResponse, error)

	// Student Context Analytics (FR 2.2)
	GetSurveyAnalyticsAggregated(ctx context.Context, schoolID string, surveyID string) (*SurveyAnalyticsAggregatedResponse, error)
	GetStudentProfileAnalysis(ctx context.Context, schoolID string, profileDimension string) (*StudentProfileAnalysisResponse, error)
	GetStatisticalAnalysis(ctx context.Context, schoolID string, analysisType string) (*StatisticalAnalysisResponse, error)
	GenerateActionPlanRecommendations(ctx context.Context, schoolID string) ([]*ActionPlanRecommendationResponse, error)

	// School Data Integration (FR 2.3)
	GetSchoolDataForSWOT(ctx context.Context, schoolID string) (*SchoolDataAnalysisResponse, error)
	GetDigitalReadinessAssessment(ctx context.Context, schoolID string) (*DigitalReadinessResponse, error)
	GetSarprasPrioritization(ctx context.Context, schoolID string) ([]*SarprasPriorityResponse, error)

	// FASE 5: Analysis Tool Enhancements

	// SWOT Builder Enhancements (FR 3.1)
	GetSWOTAnalyticsAggregation(ctx context.Context, sessionID string) (*SWOTAnalyticsResponse, error)
	MapDataToSWOTItem(ctx context.Context, req SWOTDataMappingRequest) (*SWOTItem, error)
	GetAvailableDataSourceTypes(ctx context.Context, schoolID string) ([]*DataSourceTypeResponse, error)
	ExportSWOTAnalysis(ctx context.Context, sessionID string, format string) ([]byte, error)

	// Root Cause Analyzer Enhancements (FR 3.2)
	Perform5WhysAnalysis(ctx context.Context, req FiveWhysRequest) (*FiveWhysResponse, error)
	LinkRaporMetricToRootCause(ctx context.Context, req RaporMetricLinkRequest) error
	GetRootCauseSuggestions(ctx context.Context, rootCauseID string) ([]*RootCauseSuggestionResponse, error)
	ExportRootCauseAnalysis(ctx context.Context, rootCauseID string, format string) ([]byte, error)

	// Fishbone Diagram Enhancements (FR 3.3)
	GetFishboneAnalytics(ctx context.Context, diagramID string) (*FishboneAnalyticsResponse, error)
	ValidateFishboneStructure(ctx context.Context, diagramID string) (*FishboneValidationResponse, error)
	GetFishboneCategories(ctx context.Context) ([]*FishboneCategoryResponse, error)
	ExportFishboneDiagram(ctx context.Context, diagramID string, format string) ([]byte, error)

	// Fishbone Template Management (T-5.3.14)
	CreateFishboneTemplate(ctx context.Context, req CreateFishboneTemplateRequest, createdBy string) (*FishboneTemplate, error)
	GetFishboneTemplateByID(ctx context.Context, id string) (*FishboneTemplate, error)
	GetPublicFishboneTemplates(ctx context.Context, category string) ([]*FishboneTemplate, error)
	GetFishboneTemplatesBySchool(ctx context.Context, schoolID string) ([]*FishboneTemplate, error)
	UpdateFishboneTemplate(ctx context.Context, id string, req UpdateFishboneTemplateRequest) (*FishboneTemplate, error)
	DeleteFishboneTemplate(ctx context.Context, id string) error
	IncrementTemplateUsage(ctx context.Context, templateID string) error
	ApplyTemplateToDiagram(ctx context.Context, templateID string, diagramID string) error

	// FASE 6: KSP Enhanced Generation

	// Document Compilation Service (FR 4.1.1)
	CompileDocumentWithAnalysis(ctx context.Context, req DocumentCompilationRequest) (*DocumentCompilationResponse, error)
	GenerateAnalysisSnapshot(ctx context.Context, integrationID string) (*AnalysisDataSnapshot, error)

	// Chart Generation (FR 4.1.3)
	GenerateChartsFromAnalysis(ctx context.Context, req ChartGenerationRequest) ([]*ChartGenerationResponse, error)
	GenerateSWOTChart(ctx context.Context, data SWOTChartData, chartType string) (*ChartGenerationResponse, error)
	GenerateRootCauseChart(ctx context.Context, data RootCauseChartData, chartType string) (*ChartGenerationResponse, error)
	GenerateFishboneChart(ctx context.Context, data FishboneChartData, chartType string) (*ChartGenerationResponse, error)
	GenerateStudentNeedsChart(ctx context.Context, data StudentNeedsChartData, chartType string) (*ChartGenerationResponse, error)

	// AI Platform Integration (FR 4.1.4)
	GenerateContentWithAI(ctx context.Context, req AIContentGenerationRequest) (*AIContentGenerationResponse, error)
	GenerateRecommendationsWithAI(ctx context.Context, req AIRecommendationRequest) (*AIRecommendationResponse, error)
	GetAIIntegrationConfig(ctx context.Context) (*AIIntegrationConfig, error)
	UpdateAIIntegrationConfig(ctx context.Context, config AIIntegrationConfig) error

	// Version History Management (FR 4.1.5)
	CreateAnalysisVersionHistory(ctx context.Context, req AnalysisVersionHistoryRequest, changedBy string) (*AnalysisVersionHistory, error)
	GetAnalysisVersionHistory(ctx context.Context, analysisID string, analysisType string) ([]*AnalysisVersionHistory, error)
	GetAnalysisVersionByID(ctx context.Context, versionID string) (*AnalysisVersionHistory, error)
	CompareAnalysisVersions(ctx context.Context, analysisID string, version1 int, version2 int) (*AnalysisVersionComparison, error)
	RestoreAnalysisVersion(ctx context.Context, req VersionRestoreRequest, changedBy string) error

	// Extended Review and Approval Workflow (FR 4.1.13)
	CreateApprovalWorkflow(ctx context.Context, req ApprovalWorkflowRequest, createdBy string) (*ApprovalWorkflow, error)
	GetApprovalWorkflowByID(ctx context.Context, workflowID string) (*ApprovalWorkflow, error)
	GetApprovalWorkflowsBySchool(ctx context.Context, schoolID string, workflowType string) ([]*ApprovalWorkflow, error)
	UpdateApprovalWorkflow(ctx context.Context, workflowID string, req ApprovalWorkflowRequest) (*ApprovalWorkflow, error)
	DeleteApprovalWorkflow(ctx context.Context, workflowID string) error
	SubmitForApproval(ctx context.Context, documentID string, workflowID string, submittedBy string) (*DocumentApprovalStatus, error)
	ProcessApproval(ctx context.Context, req ApprovalRequest, approverID string) (*ApprovalResponse, error)
	GetDocumentApprovalStatus(ctx context.Context, documentID string) (*DocumentApprovalStatus, error)
	AssignWorkflowStep(ctx context.Context, workflowID string, stepID string, documentID string, assignedTo string, assignedBy string) (*WorkflowStepAssignment, error)
	GetPendingApprovals(ctx context.Context, approverID string) ([]*DocumentApprovalStatus, error)
	SendApprovalNotification(ctx context.Context, notification ApprovalNotification) error
	GetApprovalNotifications(ctx context.Context, recipientID string) ([]*ApprovalNotification, error)
}

type service struct {
	repo                    Repository
	fishboneTemplates       map[uuid.UUID]*FishboneTemplate
	kspAnalysisTemplates    map[uuid.UUID]*KSPAnalysisTemplate
	kspAnalysisIntegrations map[uuid.UUID]*KSPAnalysisIntegration
	aiClient                *grpc_clients.StrategicAnalysisClient
}

func NewService(repo Repository, aiClient *grpc_clients.StrategicAnalysisClient) Service {
	return &service{repo: repo, aiClient: aiClient}
}

// Rapor Pendidikan implementation
func (s *service) CreateRaporPendidikan(ctx context.Context, req CreateRaporPendidikanRequest) (*RaporPendidikan, error) {
	schoolID, err := uuid.Parse(req.SchoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}

	rapor := &RaporPendidikan{
		SchoolID:       schoolID,
		Year:           req.Year,
		Semester:       req.Semester,
		LiteracyScore:  req.LiteracyScore,
		NumeracyScore:  req.NumeracyScore,
		CharacterScore: req.CharacterScore,
		RawData:        req.RawData,
		SyncStatus:     "SUCCESS",
	}

	if err := s.repo.CreateRaporPendidikan(ctx, rapor); err != nil {
		return nil, err
	}

	return rapor, nil
}

func (s *service) GetRaporPendidikanByID(ctx context.Context, id string) (*RaporPendidikan, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetRaporPendidikanByID(ctx, uid)
}

func (s *service) GetRaporPendidikanBySchool(ctx context.Context, schoolID string, year string) ([]*RaporPendidikan, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}
	return s.repo.GetRaporPendidikanBySchool(ctx, uid, year)
}

func (s *service) UpdateRaporPendidikan(ctx context.Context, id string, req UpdateRaporPendidikanRequest) (*RaporPendidikan, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	rapor, err := s.repo.GetRaporPendidikanByID(ctx, uid)
	if err != nil {
		return nil, errors.New("rapor pendidikan not found")
	}

	if req.Year != "" {
		rapor.Year = req.Year
	}
	if req.Semester != "" {
		rapor.Semester = req.Semester
	}
	if req.LiteracyScore != nil {
		rapor.LiteracyScore = req.LiteracyScore
	}
	if req.NumeracyScore != nil {
		rapor.NumeracyScore = req.NumeracyScore
	}
	if req.CharacterScore != nil {
		rapor.CharacterScore = req.CharacterScore
	}
	if req.RawData != nil {
		rapor.RawData = req.RawData
	}
	if req.SyncStatus != "" {
		rapor.SyncStatus = req.SyncStatus
	}
	if req.SyncErrorMessage != nil {
		rapor.SyncErrorMessage = req.SyncErrorMessage
	}

	if err := s.repo.UpdateRaporPendidikan(ctx, rapor); err != nil {
		return nil, err
	}

	return rapor, nil
}

func (s *service) DeleteRaporPendidikan(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteRaporPendidikan(ctx, uid)
}

func (s *service) SyncRaporPendidikan(ctx context.Context, req SyncRaporPendidikanRequest) (*RaporPendidikan, error) {
	schoolID, err := uuid.Parse(req.SchoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}

	// Check if already exists
	existing, err := s.repo.GetRaporPendidikanBySchoolYear(ctx, schoolID, req.Year, req.Semester)
	if err == nil && existing != nil {
		// Update existing
		existing.SyncStatus = "SUCCESS"
		existing.SyncAt = time.Now()
		if err := s.repo.UpdateRaporPendidikan(ctx, existing); err != nil {
			return nil, err
		}
		return existing, nil
	}

	// Create new
	rapor := &RaporPendidikan{
		SchoolID:   schoolID,
		Year:       req.Year,
		Semester:   req.Semester,
		SyncStatus: "SUCCESS",
		SyncAt:     time.Now(),
	}

	// TODO: Implement actual API call to Rapor Pendidikan API
	// For now, create with placeholder data
	if err := s.repo.CreateRaporPendidikan(ctx, rapor); err != nil {
		return nil, err
	}

	return rapor, nil
}

// Survey implementation
func (s *service) CreateSurvey(ctx context.Context, req CreateSurveyRequest) (*Survey, error) {
	schoolID, err := uuid.Parse(req.SchoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}

	survey := &Survey{
		SchoolID:         schoolID,
		TargetAudience:   req.TargetAudience,
		Title:            req.Title,
		Description:      req.Description,
		FormSchema:       req.FormSchema,
		Status:           "DRAFT",
		IsAnonymous:      req.IsAnonymous,
		AllowMultiple:    req.AllowMultiple,
		MaxResponses:     req.MaxResponses,
		IsTemplate:       req.IsTemplate,
		TemplateCategory: req.TemplateCategory,
		StartDate:        req.StartDate,
		EndDate:          req.EndDate,
	}

	if err := s.repo.CreateSurvey(ctx, survey); err != nil {
		return nil, err
	}

	return survey, nil
}

func (s *service) GetSurveyByID(ctx context.Context, id string) (*Survey, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetSurveyByID(ctx, uid)
}

func (s *service) GetSurveysBySchool(ctx context.Context, schoolID string, pagination common.Pagination) ([]*Survey, int64, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, 0, errors.New("invalid school ID")
	}
	repoPagination := Pagination{
		Page:   pagination.Page,
		Limit:  pagination.Limit,
		Offset: pagination.Offset,
	}
	return s.repo.GetSurveysBySchool(ctx, uid, repoPagination)
}

func (s *service) UpdateSurvey(ctx context.Context, id string, req UpdateSurveyRequest) (*Survey, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	survey, err := s.repo.GetSurveyByID(ctx, uid)
	if err != nil {
		return nil, errors.New("survey not found")
	}

	if req.TargetAudience != "" {
		survey.TargetAudience = req.TargetAudience
	}
	if req.Title != nil {
		survey.Title = *req.Title
	}
	if req.Description != nil {
		survey.Description = req.Description
	}
	if req.FormSchema != nil {
		survey.FormSchema = *req.FormSchema
	}
	if req.Status != nil {
		survey.Status = *req.Status
	}
	if req.IsAnonymous != nil {
		survey.IsAnonymous = *req.IsAnonymous
	}
	if req.AllowMultiple != nil {
		survey.AllowMultiple = *req.AllowMultiple
	}
	if req.MaxResponses != nil {
		survey.MaxResponses = req.MaxResponses
	}
	if req.IsTemplate != nil {
		survey.IsTemplate = *req.IsTemplate
	}
	if req.TemplateCategory != nil {
		survey.TemplateCategory = req.TemplateCategory
	}
	if req.StartDate != nil {
		survey.StartDate = req.StartDate
	}
	if req.EndDate != nil {
		survey.EndDate = req.EndDate
	}

	if err := s.repo.UpdateSurvey(ctx, survey); err != nil {
		return nil, err
	}

	return survey, nil
}

func (s *service) DeleteSurvey(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteSurvey(ctx, uid)
}

func (s *service) GetSurveyTemplates(ctx context.Context, category string) ([]*Survey, error) {
	return s.repo.GetSurveyTemplates(ctx, category)
}

func (s *service) GetActiveSurveys(ctx context.Context, schoolID string) ([]*Survey, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}
	return s.repo.GetActiveSurveys(ctx, uid)
}

func (s *service) SubmitSurveyResponse(ctx context.Context, req CreateSurveyResponseRequest) (*SurveyResponse, error) {
	surveyID, err := uuid.Parse(req.SurveyID)
	if err != nil {
		return nil, errors.New("invalid survey ID")
	}

	var respondentID *uuid.UUID
	if req.RespondentID != nil {
		uid, err := uuid.Parse(*req.RespondentID)
		if err != nil {
			return nil, errors.New("invalid respondent ID")
		}
		respondentID = &uid
	}

	response := &SurveyResponse{
		SurveyID:       surveyID,
		RespondentID:   respondentID,
		RespondentName: req.RespondentName,
		RespondentType: req.RespondentType,
		AnswersJSON:    req.AnswersJSON,
		SubmittedAt:    time.Now(),
		IPAddress:      req.IPAddress,
		UserAgent:      req.UserAgent,
	}

	if err := s.repo.CreateSurveyResponse(ctx, response); err != nil {
		return nil, err
	}

	return response, nil
}

func (s *service) GetSurveyResponses(ctx context.Context, surveyID string, pagination common.Pagination) ([]*SurveyResponse, int64, error) {
	uid, err := uuid.Parse(surveyID)
	if err != nil {
		return nil, 0, errors.New("invalid survey ID")
	}
	repoPagination := Pagination{
		Page:   pagination.Page,
		Limit:  pagination.Limit,
		Offset: pagination.Offset,
	}
	return s.repo.GetSurveyResponsesBySurveyID(ctx, uid, repoPagination)
}

func (s *service) GetSurveyAnalytics(ctx context.Context, surveyID string) (*SurveyAnalyticsResponse, error) {
	uid, err := uuid.Parse(surveyID)
	if err != nil {
		return nil, errors.New("invalid survey ID")
	}

	responses, total, err := s.repo.GetSurveyResponsesBySurveyID(ctx, uid, Pagination{Limit: 10000, Offset: 0})
	if err != nil {
		return nil, err
	}

	analytics := &SurveyAnalyticsResponse{
		TotalResponses:        int(total),
		CompletionRate:        100.0, // TODO: Calculate actual completion rate
		AverageTimeToComplete: 0,     // TODO: Calculate actual average time
		ResponsesByDate:       make(map[string]int),
		ResponseData:          make(map[string]interface{}),
	}

	// Aggregate responses by date
	for _, resp := range responses {
		dateKey := resp.SubmittedAt.Format("2006-01-02")
		analytics.ResponsesByDate[dateKey]++
	}

	// Parse form schema and aggregate responses
	survey, err := s.repo.GetSurveyByID(ctx, uid)
	if err == nil {
		var schema map[string]interface{}
		if err := json.Unmarshal([]byte(survey.FormSchema), &schema); err == nil {
			analytics.ResponseData["schema"] = schema
		}
	}

	return analytics, nil
}

// FGD Session implementation
func (s *service) CreateFGDSession(ctx context.Context, req CreateFGDSessionRequest) (*FGDSession, error) {
	schoolID, err := uuid.Parse(req.SchoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}

	session := &FGDSession{
		SchoolID:            schoolID,
		Topic:               req.Topic,
		Description:         req.Description,
		SessionType:         req.SessionType,
		ScheduledDate:       req.ScheduledDate,
		DurationMinutes:     req.DurationMinutes,
		ConferencePlatform:  req.ConferencePlatform,
		ConferenceLink:      req.ConferenceLink,
		ConferenceMeetingID: req.ConferenceMeetingID,
		ConferencePassword:  req.ConferencePassword,
		MaxParticipants:     req.MaxParticipants,
		Status:              "SCHEDULED",
		IsRecorded:          req.IsRecorded,
	}

	if err := s.repo.CreateFGDSession(ctx, session); err != nil {
		return nil, err
	}

	return session, nil
}

func (s *service) GetFGDSessionByID(ctx context.Context, id string) (*FGDSession, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetFGDSessionByID(ctx, uid)
}

func (s *service) GetFGDSessionsBySchool(ctx context.Context, schoolID string, pagination common.Pagination) ([]*FGDSession, int64, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, 0, errors.New("invalid school ID")
	}
	repoPagination := Pagination{
		Page:   pagination.Page,
		Limit:  pagination.Limit,
		Offset: pagination.Offset,
	}
	return s.repo.GetFGDSessionsBySchool(ctx, uid, repoPagination)
}

func (s *service) UpdateFGDSession(ctx context.Context, id string, req UpdateFGDSessionRequest) (*FGDSession, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	session, err := s.repo.GetFGDSessionByID(ctx, uid)
	if err != nil {
		return nil, errors.New("FGD session not found")
	}

	if req.Topic != nil {
		session.Topic = *req.Topic
	}
	if req.Description != nil {
		session.Description = req.Description
	}
	if req.SessionType != nil {
		session.SessionType = *req.SessionType
	}
	if req.ScheduledDate != nil {
		session.ScheduledDate = *req.ScheduledDate
	}
	if req.DurationMinutes != nil {
		session.DurationMinutes = *req.DurationMinutes
	}
	if req.ConferencePlatform != nil {
		session.ConferencePlatform = req.ConferencePlatform
	}
	if req.ConferenceLink != nil {
		session.ConferenceLink = req.ConferenceLink
	}
	if req.ConferenceMeetingID != nil {
		session.ConferenceMeetingID = req.ConferenceMeetingID
	}
	if req.ConferencePassword != nil {
		session.ConferencePassword = req.ConferencePassword
	}
	if req.NotesContent != nil {
		session.NotesContent = req.NotesContent
	}
	if req.NotesFormat != nil {
		session.NotesFormat = *req.NotesFormat
	}
	if req.MaxParticipants != nil {
		session.MaxParticipants = req.MaxParticipants
	}
	if req.Status != nil {
		session.Status = *req.Status
	}
	if req.RecordingURL != nil {
		session.RecordingURL = req.RecordingURL
	}
	if req.IsRecorded != nil {
		session.IsRecorded = *req.IsRecorded
	}
	if req.SentimentSummary != nil {
		session.SentimentSummary = req.SentimentSummary
	}
	if req.SentimentScore != nil {
		session.SentimentScore = req.SentimentScore
	}

	if err := s.repo.UpdateFGDSession(ctx, session); err != nil {
		return nil, err
	}

	return session, nil
}

func (s *service) DeleteFGDSession(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteFGDSession(ctx, uid)
}

func (s *service) GetUpcomingFGDSessions(ctx context.Context, schoolID string) ([]*FGDSession, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}
	return s.repo.GetUpcomingFGDSessions(ctx, uid)
}

func (s *service) AddFGDParticipant(ctx context.Context, req AddFGDParticipantRequest) (*FGDParticipant, error) {
	sessionID, err := uuid.Parse(req.FGDSessionID)
	if err != nil {
		return nil, errors.New("invalid session ID")
	}

	var userID *uuid.UUID
	if req.UserID != nil {
		uid, err := uuid.Parse(*req.UserID)
		if err != nil {
			return nil, errors.New("invalid user ID")
		}
		userID = &uid
	}

	participant := &FGDParticipant{
		FGDSessionID:    sessionID,
		UserID:          userID,
		ParticipantName: req.ParticipantName,
		ParticipantRole: req.ParticipantRole,
		Email:           req.Email,
		IsInvited:       req.IsInvited,
		IsAttended:      false,
	}

	if err := s.repo.AddFGDParticipant(ctx, participant); err != nil {
		return nil, err
	}

	return participant, nil
}

func (s *service) GetFGDParticipants(ctx context.Context, sessionID string) ([]*FGDParticipant, error) {
	uid, err := uuid.Parse(sessionID)
	if err != nil {
		return nil, errors.New("invalid session ID")
	}
	return s.repo.GetFGDParticipantsBySession(ctx, uid)
}

func (s *service) UpdateFGDParticipant(ctx context.Context, id string, req UpdateFGDParticipantRequest) (*FGDParticipant, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	// Get current participant from repository
	// Note: This assumes we have a GetFGDParticipantByID method, or we need to add it
	// For now, we'll implement a basic update
	participant := &FGDParticipant{
		ID: uid,
	}

	if req.ParticipantName != nil {
		participant.ParticipantName = *req.ParticipantName
	}
	if req.ParticipantRole != nil {
		participant.ParticipantRole = *req.ParticipantRole
	}
	if req.Email != nil {
		participant.Email = req.Email
	}
	if req.IsInvited != nil {
		participant.IsInvited = *req.IsInvited
	}
	if req.IsAttended != nil {
		participant.IsAttended = *req.IsAttended
	}
	if req.JoinedAt != nil {
		participant.JoinedAt = req.JoinedAt
	}
	if req.LeftAt != nil {
		participant.LeftAt = req.LeftAt
	}
	if req.ContributionRating != nil {
		participant.ContributionRating = req.ContributionRating
	}
	if req.Feedback != nil {
		participant.Feedback = req.Feedback
	}

	if err := s.repo.UpdateFGDParticipant(ctx, participant); err != nil {
		return nil, err
	}

	return participant, nil
}

func (s *service) DeleteFGDParticipant(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteFGDParticipant(ctx, uid)
}

// Student Needs Enhanced implementation
func (s *service) CreateStudentNeedsEnhanced(ctx context.Context, req CreateStudentNeedsEnhancedRequest) (*StudentNeedsEnhanced, error) {
	schoolID, err := uuid.Parse(req.SchoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}

	var studentContextExtID *uuid.UUID
	if req.StudentContextExtID != nil {
		uid, err := uuid.Parse(*req.StudentContextExtID)
		if err != nil {
			return nil, errors.New("invalid student context ext ID")
		}
		studentContextExtID = &uid
	}

	var surveyResponseID *uuid.UUID
	if req.SurveyResponseID != nil {
		uid, err := uuid.Parse(*req.SurveyResponseID)
		if err != nil {
			return nil, errors.New("invalid survey response ID")
		}
		surveyResponseID = &uid
	}

	var surveyID *uuid.UUID
	if req.SurveyID != nil {
		uid, err := uuid.Parse(*req.SurveyID)
		if err != nil {
			return nil, errors.New("invalid survey ID")
		}
		surveyID = &uid
	}

	needs := &StudentNeedsEnhanced{
		SchoolID:             schoolID,
		StudentContextExtID:  studentContextExtID,
		ProfilDimensi:        req.ProfilDimensi,
		SurveyResponseID:     surveyResponseID,
		SurveyID:             surveyID,
		CurrentStatus:        req.CurrentStatus,
		GapAnalysis:          req.GapAnalysis,
		PriorityLevel:        req.PriorityLevel,
		ActionPlan:           req.ActionPlan,
		ActionPlanStatus:     "NOT_STARTED",
		ActionPlanAssignedTo: nil, // TODO: Parse if provided
		ActionPlanDueDate:    req.ActionPlanDueDate,
		ProgressPercentage:   0,
		NextAssessmentDate:   req.NextAssessmentDate,
		Notes:                req.Notes,
		Tags:                 req.Tags,
	}

	if err := s.repo.CreateStudentNeedsEnhanced(ctx, needs); err != nil {
		return nil, err
	}

	return needs, nil
}

func (s *service) GetStudentNeedsEnhancedByID(ctx context.Context, id string) (*StudentNeedsEnhanced, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetStudentNeedsEnhancedByID(ctx, uid)
}

func (s *service) GetStudentNeedsEnhancedBySchool(ctx context.Context, schoolID string, pagination common.Pagination) ([]*StudentNeedsEnhanced, int64, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, 0, errors.New("invalid school ID")
	}
	repoPagination := Pagination{
		Page:   pagination.Page,
		Limit:  pagination.Limit,
		Offset: pagination.Offset,
	}
	return s.repo.GetStudentNeedsEnhancedBySchool(ctx, uid, repoPagination)
}

func (s *service) GetStudentNeedsEnhancedByProfile(ctx context.Context, schoolID string, profilDimensi string) ([]*StudentNeedsEnhanced, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}
	return s.repo.GetStudentNeedsEnhancedByProfile(ctx, uid, profilDimensi)
}

func (s *service) UpdateStudentNeedsEnhanced(ctx context.Context, id string, req UpdateStudentNeedsEnhancedRequest) (*StudentNeedsEnhanced, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	needs, err := s.repo.GetStudentNeedsEnhancedByID(ctx, uid)
	if err != nil {
		return nil, errors.New("student needs not found")
	}

	if req.StudentContextExtID != nil {
		studentID, err := uuid.Parse(*req.StudentContextExtID)
		if err != nil {
			return nil, errors.New("invalid student context ext ID")
		}
		needs.StudentContextExtID = &studentID
	}
	if req.ProfilDimensi != nil {
		needs.ProfilDimensi = *req.ProfilDimensi
	}
	if req.SurveyResponseID != nil {
		respID, err := uuid.Parse(*req.SurveyResponseID)
		if err != nil {
			return nil, errors.New("invalid survey response ID")
		}
		needs.SurveyResponseID = &respID
	}
	if req.SurveyID != nil {
		surveyID, err := uuid.Parse(*req.SurveyID)
		if err != nil {
			return nil, errors.New("invalid survey ID")
		}
		needs.SurveyID = &surveyID
	}
	if req.CurrentStatus != nil {
		needs.CurrentStatus = req.CurrentStatus
	}
	if req.GapAnalysis != nil {
		needs.GapAnalysis = req.GapAnalysis
	}
	if req.PriorityLevel != nil {
		needs.PriorityLevel = *req.PriorityLevel
	}
	if req.ActionPlan != nil {
		needs.ActionPlan = req.ActionPlan
	}
	if req.ActionPlanStatus != nil {
		needs.ActionPlanStatus = *req.ActionPlanStatus
	}
	if req.ActionPlanAssignedTo != nil {
		assignedID, err := uuid.Parse(*req.ActionPlanAssignedTo)
		if err != nil {
			return nil, errors.New("invalid assigned to ID")
		}
		needs.ActionPlanAssignedTo = &assignedID
	}
	if req.ActionPlanDueDate != nil {
		needs.ActionPlanDueDate = req.ActionPlanDueDate
	}
	if req.ProgressPercentage != nil {
		needs.ProgressPercentage = *req.ProgressPercentage
	}
	if req.LastAssessmentDate != nil {
		needs.LastAssessmentDate = req.LastAssessmentDate
	}
	if req.NextAssessmentDate != nil {
		needs.NextAssessmentDate = req.NextAssessmentDate
	}
	if req.Notes != nil {
		needs.Notes = req.Notes
	}
	if req.Tags != nil {
		needs.Tags = req.Tags
	}

	if err := s.repo.UpdateStudentNeedsEnhanced(ctx, needs); err != nil {
		return nil, err
	}

	return needs, nil
}

func (s *service) DeleteStudentNeedsEnhanced(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteStudentNeedsEnhanced(ctx, uid)
}

// SWOT implementation
func (s *service) CreateSWOTItem(ctx context.Context, req CreateSWOTItemRequest) (*SWOTItem, error) {
	schoolID, err := uuid.Parse(req.SchoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}

	var sourceDataID *uuid.UUID
	if req.SourceDataID != nil {
		uid, err := uuid.Parse(*req.SourceDataID)
		if err != nil {
			return nil, errors.New("invalid source data ID")
		}
		sourceDataID = &uid
	}

	item := &SWOTItem{
		SchoolID:       schoolID,
		Quadrant:       req.Quadrant,
		Statement:      req.Statement,
		SourceDataID:   sourceDataID,
		SourceDataType: req.SourceType,
		Priority:       req.Priority,
	}

	if err := s.repo.CreateSWOTItem(ctx, item); err != nil {
		return nil, err
	}

	return item, nil
}

func (s *service) GetSWOTItemByID(ctx context.Context, id string) (*SWOTItem, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetSWOTItemByID(ctx, uid)
}

func (s *service) GetSWOTItemsBySchool(ctx context.Context, schoolID string, quadrant string) ([]*SWOTItem, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}
	return s.repo.GetSWOTItemsBySchool(ctx, uid, quadrant)
}

func (s *service) UpdateSWOTItem(ctx context.Context, id string, req UpdateSWOTItemRequest) (*SWOTItem, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	item, err := s.repo.GetSWOTItemByID(ctx, uid)
	if err != nil {
		return nil, errors.New("SWOT item not found")
	}

	if req.Quadrant != nil {
		item.Quadrant = *req.Quadrant
	}
	if req.Statement != nil {
		item.Statement = *req.Statement
	}
	if req.SourceDataID != nil {
		sourceID, err := uuid.Parse(*req.SourceDataID)
		if err != nil {
			return nil, errors.New("invalid source data ID")
		}
		item.SourceDataID = &sourceID
	}
	if req.SourceType != nil {
		item.SourceDataType = req.SourceType
	}
	if req.Priority != nil {
		item.Priority = *req.Priority
	}

	if err := s.repo.UpdateSWOTItem(ctx, item); err != nil {
		return nil, err
	}

	return item, nil
}

func (s *service) DeleteSWOTItem(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteSWOTItem(ctx, uid)
}

func (s *service) CreateSWOTAnalysisSession(ctx context.Context, req CreateSWOTAnalysisSessionRequest) (*SWOTAnalysisSession, error) {
	schoolID, err := uuid.Parse(req.SchoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}

	session := &SWOTAnalysisSession{
		SchoolID:     schoolID,
		SessionName:  req.SessionName,
		Description:  req.Description,
		Participants: req.Participants,
		Status:       "DRAFT",
		IsTemplate:   req.IsTemplate,
	}

	if err := s.repo.CreateSWOTAnalysisSession(ctx, session); err != nil {
		return nil, err
	}

	return session, nil
}

func (s *service) GetSWOTAnalysisSessionByID(ctx context.Context, id string) (*SWOTAnalysisSession, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetSWOTAnalysisSessionByID(ctx, uid)
}

func (s *service) GetSWOTAnalysisSessionsBySchool(ctx context.Context, schoolID string) ([]*SWOTAnalysisSession, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}
	return s.repo.GetSWOTAnalysisSessionsBySchool(ctx, uid)
}

func (s *service) UpdateSWOTAnalysisSession(ctx context.Context, id string, req UpdateSWOTAnalysisSessionRequest) (*SWOTAnalysisSession, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	session, err := s.repo.GetSWOTAnalysisSessionByID(ctx, uid)
	if err != nil {
		return nil, errors.New("SWOT session not found")
	}

	if req.SessionName != nil {
		session.SessionName = *req.SessionName
	}
	if req.Description != nil {
		session.Description = req.Description
	}
	if req.AnalysisScope != nil {
		// AnalysisScope doesn't exist in model, skip or use Description
		session.Description = req.AnalysisScope
	}
	if req.Participants != nil {
		session.Participants = req.Participants
	}
	if req.Status != nil {
		session.Status = *req.Status
	}

	if err := s.repo.UpdateSWOTAnalysisSession(ctx, session); err != nil {
		return nil, err
	}

	return session, nil
}

func (s *service) DeleteSWOTAnalysisSession(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteSWOTAnalysisSession(ctx, uid)
}

func (s *service) AddSWOTItemToSession(ctx context.Context, req AddSWOTSessionItemRequest) error {
	sessionID, err := uuid.Parse(req.SessionID)
	if err != nil {
		return errors.New("invalid session ID")
	}

	itemID, err := uuid.Parse(req.ItemID)
	if err != nil {
		return errors.New("invalid item ID")
	}

	sessionItem := &SWOTSessionItem{
		SWOTSessionID: sessionID,
		SWOTItemID:    itemID,
	}

	return s.repo.AddSWOTItemToSession(ctx, sessionItem)
}

func (s *service) GetSWOTSessionItems(ctx context.Context, sessionID string) ([]*SWOTSessionItem, error) {
	uid, err := uuid.Parse(sessionID)
	if err != nil {
		return nil, errors.New("invalid session ID")
	}
	return s.repo.GetSWOTSessionItems(ctx, uid)
}

// Root Cause implementation
func (s *service) CreateRootCause(ctx context.Context, req CreateRootCauseRequest) (*RootCause, error) {
	schoolID, err := uuid.Parse(req.SchoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}

	var raporMetricID *uuid.UUID
	if req.RaporMetricID != nil {
		uid, err := uuid.Parse(*req.RaporMetricID)
		if err != nil {
			return nil, errors.New("invalid rapor metric ID")
		}
		raporMetricID = &uid
	}

	var assignedTo *uuid.UUID
	if req.AssignedTo != nil {
		uid, err := uuid.Parse(*req.AssignedTo)
		if err != nil {
			return nil, errors.New("invalid assigned to ID")
		}
		assignedTo = &uid
	}

	rootCauseValue := ""
	if req.RootCause != nil {
		rootCauseValue = *req.RootCause
	}

	kegiatanBenahiValue := ""
	if req.KegiatanBenahi != nil {
		kegiatanBenahiValue = *req.KegiatanBenahi
	}

	rootCause := &RootCause{
		SchoolID:          schoolID,
		RaporMetricID:     raporMetricID,
		IdentifiedProblem: req.IdentifiedProblem,
		Why1:              req.Why1,
		Why2:              req.Why2,
		Why3:              req.Why3,
		Why4:              req.Why4,
		Why5:              req.Why5,
		RootCause:         rootCauseValue,
		KegiatanBenahi:    kegiatanBenahiValue,
		Status:            "IDENTIFIED",
		AssignedTo:        assignedTo,
		DueDate:           req.DueDate,
	}

	if err := s.repo.CreateRootCause(ctx, rootCause); err != nil {
		return nil, err
	}

	return rootCause, nil
}

func (s *service) GetRootCauseByID(ctx context.Context, id string) (*RootCause, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetRootCauseByID(ctx, uid)
}

func (s *service) GetRootCausesBySchool(ctx context.Context, schoolID string, status string) ([]*RootCause, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}
	return s.repo.GetRootCausesBySchool(ctx, uid, status)
}

func (s *service) UpdateRootCause(ctx context.Context, id string, req UpdateRootCauseRequest) (*RootCause, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	rootCause, err := s.repo.GetRootCauseByID(ctx, uid)
	if err != nil {
		return nil, errors.New("root cause not found")
	}

	if req.RaporMetricID != nil {
		metricID, err := uuid.Parse(*req.RaporMetricID)
		if err != nil {
			return nil, errors.New("invalid rapor metric ID")
		}
		rootCause.RaporMetricID = &metricID
	}
	if req.IdentifiedProblem != nil {
		rootCause.IdentifiedProblem = *req.IdentifiedProblem
	}
	if req.Why1 != nil {
		rootCause.Why1 = req.Why1
	}
	if req.Why2 != nil {
		rootCause.Why2 = req.Why2
	}
	if req.Why3 != nil {
		rootCause.Why3 = req.Why3
	}
	if req.Why4 != nil {
		rootCause.Why4 = req.Why4
	}
	if req.Why5 != nil {
		rootCause.Why5 = req.Why5
	}
	if req.RootCause != nil {
		rootCause.RootCause = *req.RootCause
	}
	if req.KegiatanBenahi != nil {
		rootCause.KegiatanBenahi = *req.KegiatanBenahi
	}
	if req.Status != nil {
		rootCause.Status = *req.Status

		// Create history entry if status changed
		if err := s.createRootCauseHistory(ctx, rootCause, req.Status); err != nil {
			return nil, fmt.Errorf("failed to create history: %w", err)
		}
	}
	if req.AssignedTo != nil {
		assignedID, err := uuid.Parse(*req.AssignedTo)
		if err != nil {
			return nil, errors.New("invalid assigned to ID")
		}
		rootCause.AssignedTo = &assignedID
	}
	if req.DueDate != nil {
		rootCause.DueDate = req.DueDate
	}

	if err := s.repo.UpdateRootCause(ctx, rootCause); err != nil {
		return nil, err
	}

	return rootCause, nil
}

func (s *service) createRootCauseHistory(ctx context.Context, rootCause *RootCause, newStatus *string) error {
	validationDate := time.Now()
	validationResult := "STATUS_CHANGE"

	history := &RootCauseHistory{
		RootCauseID:      rootCause.ID,
		PreviousStatus:   &rootCause.Status,
		NewStatus:        newStatus,
		ValidationDate:   &validationDate,
		ValidationResult: &validationResult,
	}

	if err := s.repo.CreateRootCauseHistory(ctx, history); err != nil {
		return err
	}

	return nil
}

func (s *service) DeleteRootCause(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteRootCause(ctx, uid)
}

func (s *service) ValidateRootCause(ctx context.Context, id string, req ValidateRootCauseRequest) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}

	validatorID, err := uuid.Parse(req.ValidatorID)
	if err != nil {
		return errors.New("invalid validator ID")
	}

	return s.repo.ValidateRootCause(ctx, uid, validatorID, req.Notes)
}

func (s *service) GetRootCauseHistory(ctx context.Context, rootCauseID string) ([]*RootCauseHistory, error) {
	uid, err := uuid.Parse(rootCauseID)
	if err != nil {
		return nil, errors.New("invalid root cause ID")
	}
	return s.repo.GetRootCauseHistoryByRootCauseID(ctx, uid)
}

// Fishbone implementation
func (s *service) CreateFishboneDiagram(ctx context.Context, req CreateFishboneDiagramRequest) (*FishboneDiagram, error) {
	schoolID, err := uuid.Parse(req.SchoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}

	diagram := &FishboneDiagram{
		SchoolID:    schoolID,
		HeadEffect:  req.HeadEffect,
		Description: req.Description,
	}

	if err := s.repo.CreateFishboneDiagram(ctx, diagram); err != nil {
		return nil, err
	}

	return diagram, nil
}

func (s *service) GetFishboneDiagramByID(ctx context.Context, id string) (*FishboneDiagram, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetFishboneDiagramByID(ctx, uid)
}

func (s *service) GetFishboneDiagramsBySchool(ctx context.Context, schoolID string) ([]*FishboneDiagram, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}
	return s.repo.GetFishboneDiagramsBySchool(ctx, uid)
}

func (s *service) UpdateFishboneDiagram(ctx context.Context, id string, req UpdateFishboneDiagramRequest) (*FishboneDiagram, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	diagram, err := s.repo.GetFishboneDiagramByID(ctx, uid)
	if err != nil {
		return nil, errors.New("fishbone diagram not found")
	}

	if req.HeadEffect != nil {
		diagram.HeadEffect = *req.HeadEffect
	}
	if req.Description != nil {
		diagram.Description = req.Description
	}

	if err := s.repo.UpdateFishboneDiagram(ctx, diagram); err != nil {
		return nil, err
	}

	return diagram, nil
}

func (s *service) DeleteFishboneDiagram(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteFishboneDiagram(ctx, uid)
}

func (s *service) CreateFishboneNode(ctx context.Context, req CreateFishboneNodeRequest) (*FishboneNode, error) {
	diagramID, err := uuid.Parse(req.DiagramID)
	if err != nil {
		return nil, errors.New("invalid diagram ID")
	}

	var parentNodeID *uuid.UUID
	if req.ParentNodeID != nil {
		uid, err := uuid.Parse(*req.ParentNodeID)
		if err != nil {
			return nil, errors.New("invalid parent node ID")
		}
		parentNodeID = &uid
	}

	node := &FishboneNode{
		DiagramID:    diagramID,
		BoneCategory: req.BoneCategory,
		ParentNodeID: parentNodeID,
		CauseText:    req.CauseText,
		PositionX:    req.PositionX,
		PositionY:    req.PositionY,
		SequenceNo:   req.SequenceNo,
	}

	if err := s.repo.CreateFishboneNode(ctx, node); err != nil {
		return nil, err
	}

	// Update diagram node count
	if err := s.repo.UpdateDiagramNodeCount(ctx, diagramID); err != nil {
		return nil, err
	}

	return node, nil
}

func (s *service) GetFishboneNodesByDiagram(ctx context.Context, diagramID string) ([]*FishboneNode, error) {
	uid, err := uuid.Parse(diagramID)
	if err != nil {
		return nil, errors.New("invalid diagram ID")
	}
	return s.repo.GetFishboneNodesByDiagram(ctx, uid)
}

func (s *service) UpdateFishboneNode(ctx context.Context, id string, req UpdateFishboneNodeRequest) (*FishboneNode, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	node, err := s.repo.GetFishboneNodeByID(ctx, uid)
	if err != nil {
		return nil, errors.New("fishbone node not found")
	}

	if req.BoneCategory != nil {
		node.BoneCategory = *req.BoneCategory
	}
	if req.ParentNodeID != nil {
		parentID, err := uuid.Parse(*req.ParentNodeID)
		if err != nil {
			return nil, errors.New("invalid parent node ID")
		}
		node.ParentNodeID = &parentID
	}
	if req.CauseText != nil {
		node.CauseText = *req.CauseText
	}
	if req.PositionX != nil {
		node.PositionX = req.PositionX
	}
	if req.PositionY != nil {
		node.PositionY = req.PositionY
	}
	if req.SequenceNo != nil {
		node.SequenceNo = *req.SequenceNo
	}

	if err := s.repo.UpdateFishboneNode(ctx, node); err != nil {
		return nil, err
	}

	return node, nil
}

func (s *service) DeleteFishboneNode(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteFishboneNode(ctx, uid)
}

func (s *service) CreateFishboneConnection(ctx context.Context, req CreateFishboneConnectionRequest) (*FishboneConnection, error) {
	diagramID, err := uuid.Parse(req.DiagramID)
	if err != nil {
		return nil, errors.New("invalid diagram ID")
	}

	fromNodeID, err := uuid.Parse(req.FromNodeID)
	if err != nil {
		return nil, errors.New("invalid from node ID")
	}

	toNodeID, err := uuid.Parse(req.ToNodeID)
	if err != nil {
		return nil, errors.New("invalid to node ID")
	}

	connection := &FishboneConnection{
		DiagramID:      diagramID,
		FromNodeID:     fromNodeID,
		ToNodeID:       toNodeID,
		ConnectionType: req.ConnectionType,
	}

	if err := s.repo.CreateFishboneConnection(ctx, connection); err != nil {
		return nil, err
	}

	return connection, nil
}

func (s *service) GetFishboneConnections(ctx context.Context, diagramID string) ([]*FishboneConnection, error) {
	uid, err := uuid.Parse(diagramID)
	if err != nil {
		return nil, errors.New("invalid diagram ID")
	}
	return s.repo.GetFishboneConnectionsByDiagram(ctx, uid)
}

func (s *service) DeleteFishboneConnection(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteFishboneConnection(ctx, uid)
}

// KSP Integration implementation
func (s *service) CreateKSPAnalysisIntegration(ctx context.Context, req CreateKSPAnalysisIntegrationRequest) (*KSPAnalysisIntegration, error) {
	documentID, err := uuid.Parse(req.DocumentID)
	if err != nil {
		return nil, errors.New("invalid document ID")
	}

	schoolID, err := uuid.Parse(req.SchoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}

	integration := &KSPAnalysisIntegration{
		CurriculumDocumentID: documentID,
		SchoolID:             schoolID,
		IntegrationType:      req.IntegrationType,
		IntegratedContent:    &req.AnalysisData,
		IntegrationStatus:    "PENDING",
	}

	if err := s.repo.CreateKSPAnalysisIntegration(ctx, integration); err != nil {
		return nil, err
	}

	return integration, nil
}

func (s *service) GetKSPAnalysisIntegrationByID(ctx context.Context, id string) (*KSPAnalysisIntegration, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetKSPAnalysisIntegrationByID(ctx, uid)
}

func (s *service) GetKSPAnalysisIntegrationsByDocument(ctx context.Context, documentID string) ([]*KSPAnalysisIntegration, error) {
	uid, err := uuid.Parse(documentID)
	if err != nil {
		return nil, errors.New("invalid document ID")
	}
	return s.repo.GetKSPAnalysisIntegrationsByDocument(ctx, uid)
}

func (s *service) UpdateKSPAnalysisIntegration(ctx context.Context, id string, req UpdateKSPAnalysisIntegrationRequest) (*KSPAnalysisIntegration, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	integration, err := s.repo.GetKSPAnalysisIntegrationByID(ctx, uid)
	if err != nil {
		return nil, errors.New("integration not found")
	}

	if req.AnalysisData != nil {
		integration.IntegratedContent = req.AnalysisData
	}
	if req.IntegrationType != nil {
		integration.IntegrationType = *req.IntegrationType
	}
	if req.Status != nil {
		integration.IntegrationStatus = *req.Status
	}
	if req.Notes != nil {
		integration.Notes = req.Notes
	}

	if err := s.repo.UpdateKSPAnalysisIntegration(ctx, integration); err != nil {
		return nil, err
	}

	return integration, nil
}

func (s *service) DeleteKSPAnalysisIntegration(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteKSPAnalysisIntegration(ctx, uid)
}

func (s *service) ApproveKSPAnalysisIntegration(ctx context.Context, id string, req ApproveKSPAnalysisIntegrationRequest) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}

	approverID, err := uuid.Parse(req.ApproverID)
	if err != nil {
		return errors.New("invalid approver ID")
	}

	return s.repo.ApproveKSPAnalysisIntegration(ctx, uid, approverID, req.Notes)
}

func (s *service) CreateKSPAnalysisRecommendation(ctx context.Context, req CreateKSPAnalysisRecommendationRequest) (*KSPAnalysisRecommendation, error) {
	integrationID, err := uuid.Parse(req.IntegrationID)
	if err != nil {
		return nil, errors.New("invalid integration ID")
	}

	recommendation := &KSPAnalysisRecommendation{
		KSPAnalysisIntegrationID: integrationID,
		RecommendationType:       "GENERAL", // Default type
		RecommendationText:       req.Recommendation,
		Priority:                 req.Priority,
		SuggestedAction:          &req.Recommendation,
		Status:                   "PENDING",
	}

	if err := s.repo.CreateKSPAnalysisRecommendation(ctx, recommendation); err != nil {
		return nil, err
	}

	return recommendation, nil
}

func (s *service) GetKSPAnalysisRecommendations(ctx context.Context, integrationID string) ([]*KSPAnalysisRecommendation, error) {
	uid, err := uuid.Parse(integrationID)
	if err != nil {
		return nil, errors.New("invalid integration ID")
	}
	return s.repo.GetKSPAnalysisRecommendationsByIntegration(ctx, uid)
}

func (s *service) UpdateKSPAnalysisRecommendation(ctx context.Context, id string, req UpdateKSPAnalysisRecommendationRequest) (*KSPAnalysisRecommendation, error) {
	// Get the recommendation (we need to add a GetKSPAnalysisRecommendationByID method to repository)
	// For now, we'll just return an error
	return nil, errors.New("repository method not implemented yet")
}

func (s *service) DeleteKSPAnalysisRecommendation(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteKSPAnalysisRecommendation(ctx, uid)
}

func (s *service) CreateKSPAnalysisTemplate(ctx context.Context, req CreateKSPAnalysisTemplateRequest) (*KSPAnalysisTemplate, error) {
	var schoolID *uuid.UUID
	if req.SchoolID != nil {
		uid, err := uuid.Parse(*req.SchoolID)
		if err != nil {
			return nil, errors.New("invalid school ID")
		}
		schoolID = &uid
	}

	template := &KSPAnalysisTemplate{
		TemplateName:         req.TemplateName,
		TemplateCategory:     &req.TemplateCategory,
		TemplateDescription:  req.TemplateDescription,
		IntegrationStructure: req.TemplateStructure,
		IsPublic:             req.IsPublic,
		SchoolID:             schoolID,
		IsActive:             true,
		UsageCount:           0,
	}

	if err := s.repo.CreateKSPAnalysisTemplate(ctx, template); err != nil {
		return nil, err
	}

	return template, nil
}

func (s *service) GetKSPAnalysisTemplateByID(ctx context.Context, id string) (*KSPAnalysisTemplate, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetKSPAnalysisTemplateByID(ctx, uid)
}

func (s *service) GetPublicKSPAnalysisTemplates(ctx context.Context, category string) ([]*KSPAnalysisTemplate, error) {
	return s.repo.GetPublicKSPAnalysisTemplates(ctx, category)
}

func (s *service) GetKSPAnalysisTemplatesBySchool(ctx context.Context, schoolID string) ([]*KSPAnalysisTemplate, error) {
	uid, err := uuid.Parse(schoolID)
	if err != nil {
		return nil, errors.New("invalid school ID")
	}
	return s.repo.GetKSPAnalysisTemplatesBySchool(ctx, uid)
}

func (s *service) UpdateKSPAnalysisTemplate(ctx context.Context, id string, req UpdateKSPAnalysisTemplateRequest) (*KSPAnalysisTemplate, error) {
	uid, err := uuid.Parse(id)
	if err != nil {
		return nil, errors.New("invalid ID")
	}

	template, err := s.repo.GetKSPAnalysisTemplateByID(ctx, uid)
	if err != nil {
		return nil, errors.New("template not found")
	}

	if req.TemplateName != nil {
		template.TemplateName = *req.TemplateName
	}
	if req.TemplateCategory != nil {
		template.TemplateCategory = req.TemplateCategory
	}
	if req.TemplateDescription != nil {
		template.TemplateDescription = req.TemplateDescription
	}
	if req.TemplateStructure != nil {
		template.IntegrationStructure = *req.TemplateStructure
	}
	if req.IsPublic != nil {
		template.IsPublic = *req.IsPublic
	}
	if req.IsActive != nil {
		template.IsActive = *req.IsActive
	}

	if err := s.repo.UpdateKSPAnalysisTemplate(ctx, template); err != nil {
		return nil, err
	}

	return template, nil
}

func (s *service) DeleteKSPAnalysisTemplate(ctx context.Context, id string) error {
	uid, err := uuid.Parse(id)
	if err != nil {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteKSPAnalysisTemplate(ctx, uid)
}

// Template usage methods moved to service_ksp_phase6.go

// FASE 4: Integration implementations

// Local Context Integration (FR 2.1)
func (s *service) GetLocalContextForSWOT(ctx context.Context, schoolID string) (*LocalContextAnalysisResponse, error) {
	// This would integrate with local_context module
	// For now, returning a placeholder implementation
	response := &LocalContextAnalysisResponse{
		SchoolID: schoolID,
		LocalContexts: []*LocalContextItem{
			{
				ID:          "sample-1",
				Category:    "BAHARI",
				Title:       "Geografis dan Isu Lingkungan Pantai Bonerate",
				Description: "Kawasan pulau terluar dengan ekosistem karang atol",
				Location:    "Desa Bonerate",
				ScopeType:   "SCHOOL",
				IsActive:    true,
			},
		},
		SWOTIntegration: &LocalContextSWOTMapping{
			Strengths: []*LocalContextItem{
				{
					ID:          "strength-1",
					Category:    "BAHARI",
					Title:       "Kekayaan biodiversitas laut",
					Description: "Potensi ekowisata bahari dan perikanan",
					Location:    "Pesisir Bonerate",
					ScopeType:   "VILLAGE",
					IsActive:    true,
				},
			},
			Weaknesses: []*LocalContextItem{},
			Opportunities: []*LocalContextItem{
				{
					ID:          "opportunity-1",
					Category:    "BAHARI",
					Title:       "Pengembangan ekowisata",
					Description: "Potensi pariwisata bahari berkelanjutan",
					Location:    "Taka Bonerate",
					ScopeType:   "VILLAGE",
					IsActive:    true,
				},
			},
			Threats: []*LocalContextItem{
				{
					ID:          "threat-1",
					Category:    "ALAM",
					Title:       "Abrasi pantai",
					Description: "Penurunan garis pantai akibat erosi",
					Location:    "Pantai Bangke",
					ScopeType:   "VILLAGE",
					IsActive:    true,
				},
			},
		},
		LastUpdated: time.Now(),
	}

	return response, nil
}

func (s *service) AnalyzeLearningPotential(ctx context.Context, schoolID string) (*LearningPotentialAnalysisResponse, error) {
	// Placeholder implementation for learning potential analysis
	response := &LearningPotentialAnalysisResponse{
		SchoolID:              schoolID,
		OverallPotentialScore: 75.5,
		CategoryScores: []*LearningCategoryScore{
			{
				Category:    "BAHARI",
				Score:       85.0,
				Potential:   "HIGH",
				Utilization: 60.0,
				Gap:         25.0,
			},
			{
				Category:    "BUDAYA",
				Score:       70.0,
				Potential:   "MEDIUM",
				Utilization: 50.0,
				Gap:         20.0,
			},
			{
				Category:    "SOSIAL",
				Score:       72.0,
				Potential:   "MEDIUM",
				Utilization: 55.0,
				Gap:         17.0,
			},
		},
		Recommendations: []string{
			"Tingkatkan integrasi konteks bahari dalam pembelajaran",
			"Kembangkan project-based learning berbasis kearifan lokal",
			"Fortifikasi kolaborasi dengan komunitas lokal",
		},
		AnalysisDate: time.Now(),
	}

	return response, nil
}

func (s *service) GetEnhancedLocalCategories(ctx context.Context, schoolID string) ([]*EnhancedCategoryResponse, error) {
	// Placeholder implementation for enhanced categories
	response := []*EnhancedCategoryResponse{
		{
			CategoryCode:    "BAHARI",
			CategoryName:    "Kemaritiman & Pesisir Pantai",
			Description:     "Konteks pembelajaran berbasis ekosistem laut dan pesisir",
			StrategicTags:   []string{"ekowisata", "perikanan", "konservasi", "budaya bahari"},
			PriorityLevel:   1,
			IntegrationType: "STRONG",
		},
		{
			CategoryCode:    "BUDAYA",
			CategoryName:    "Tradisi & Kebudayaan",
			Description:     "Kearifan budaya Kepulauan Selayar",
			StrategicTags:   []string{"adat", "seni", "ritual", "bahasa lokal"},
			PriorityLevel:   2,
			IntegrationType: "MODERATE",
		},
		{
			CategoryCode:    "SOSIAL",
			CategoryName:    "Komunitas & Kemitraan",
			Description:     "Relasi sosial komunitas pesisir dan kemitraan",
			StrategicTags:   []string{"gotong-royong", "koperasi", "kelompok-sosial"},
			PriorityLevel:   2,
			IntegrationType: "MODERATE",
		},
	}

	return response, nil
}

// Student Context Analytics (FR 2.2)
func (s *service) GetSurveyAnalyticsAggregated(ctx context.Context, schoolID string, surveyID string) (*SurveyAnalyticsAggregatedResponse, error) {
	surveyUID, err := uuid.Parse(surveyID)
	if err != nil {
		return nil, errors.New("invalid survey ID")
	}

	// Get survey responses for aggregation
	responses, _, err := s.repo.GetSurveyResponsesBySurveyID(ctx, surveyUID, Pagination{Limit: 1000, Offset: 0})
	if err != nil {
		return nil, err
	}

	// Placeholder implementation for aggregated analytics
	response := &SurveyAnalyticsAggregatedResponse{
		SurveyID:       surveyID,
		SchoolID:       schoolID,
		TotalResponses: len(responses),
		ResponseRate:   85.5,
		AggregatedAnswers: map[string]interface{}{
			"field_1": map[string]interface{}{
				"option_a": 45,
				"option_b": 30,
				"option_c": 25,
			},
		},
		StatisticalSummary: &StatisticalSummary{
			Mean:   map[string]float64{"field_1": 3.5},
			Median: map[string]float64{"field_1": 3.0},
			Mode:   map[string]string{"field_1": "option_a"},
			StdDev: map[string]float64{"field_1": 1.2},
			Min:    map[string]float64{"field_1": 1.0},
			Max:    map[string]float64{"field_1": 5.0},
			Percentiles: map[string]map[string]float64{
				"field_1": {
					"25": 2.0,
					"50": 3.0,
					"75": 4.0,
				},
			},
		},
		TrendAnalysis: &TrendAnalysis{
			Period: "monthly",
			TrendData: []TrendDataPoint{
				{
					Date:   "2026-01",
					Values: map[string]interface{}{"response_count": 45},
				},
				{
					Date:   "2026-02",
					Values: map[string]interface{}{"response_count": 52},
				},
			},
			Insights: []string{
				"Tren peningkatan partisipasi survei",
				"Peningkatan 15% dari bulan sebelumnya",
			},
			Forecast: []ForecastDataPoint{
				{
					Date:       "2026-03",
					Predicted:  map[string]interface{}{"response_count": 58},
					Confidence: map[string]float64{"lower": 50, "upper": 66},
				},
			},
		},
		LastUpdated: time.Now(),
	}

	return response, nil
}

func (s *service) GetStudentProfileAnalysis(ctx context.Context, schoolID string, profileDimension string) (*StudentProfileAnalysisResponse, error) {
	// Placeholder implementation for student profile analysis
	response := &StudentProfileAnalysisResponse{
		SchoolID:         schoolID,
		ProfileDimension: profileDimension,
		TotalStudents:    180,
		ProfileDistribution: []*ProfileDistribution{
			{
				ProfileLevel:    "BERIMAN",
				Count:           45,
				Percentage:      25.0,
				Characteristics: []string{"aktif di kegiatan keagamaan", "berakhlak mulia"},
			},
			{
				ProfileLevel:    "BERGOTONG_ROYONG",
				Count:           38,
				Percentage:      21.1,
				Characteristics: []string{"sukarela dalam kegiatan kelompok", "peduli lingkungan"},
			},
			{
				ProfileLevel:    "MANDIRI",
				Count:           52,
				Percentage:      28.9,
				Characteristics: []string{"dapat mengerjakan tugas sendiri", "bertanggung jawab"},
			},
		},
		RiskFactors: []*RiskFactor{
			{
				Factor:        "Keterbatasan akses digital",
				Severity:      "MEDIUM",
				AffectedCount: 35,
				Percentage:    19.4,
				Mitigation:    "Penyediaan fasilitas komunal dan akses internet terpadu",
			},
		},
		Recommendations: []string{
			"Intensifkan pembinaan karakter melalui kegiatan kokurikuler",
			"Kembangkan program mentoring antar tingkat",
			"Optimalkan pemanfaatan sarana digital sekolah",
		},
		AnalysisDate: time.Now(),
	}

	return response, nil
}

func (s *service) GetStatisticalAnalysis(ctx context.Context, schoolID string, analysisType string) (*StatisticalAnalysisResponse, error) {
	// Use schoolID directly
	if schoolID == "" {
		return nil, errors.New("invalid school ID")
	}

	// Placeholder implementation for statistical analysis
	response := &StatisticalAnalysisResponse{
		SchoolID:     schoolID,
		AnalysisType: analysisType,
		Results: map[string]interface{}{
			"correlation_analysis": map[string]interface{}{
				"literacy_vs_numeracy":      0.75,
				"attendance_vs_performance": 0.82,
			},
			"regression_analysis": map[string]interface{}{
				"r_squared":  0.68,
				"predictors": []string{"attendance", "participation", "resources"},
			},
		},
		Metadata: &AnalysisMetadata{
			DataPeriod:      "2025-2026",
			Source:          "survey_responses",
			ConfidenceLevel: 0.95,
			SampleSize:      180,
			LastUpdated:     time.Now(),
		},
		GeneratedAt: time.Now(),
	}

	return response, nil
}

func (s *service) GenerateActionPlanRecommendations(ctx context.Context, schoolID string) ([]*ActionPlanRecommendationResponse, error) {
	if schoolID == "" {
		return nil, errors.New("invalid school ID")
	}

	// Placeholder implementation for action plan recommendations
	response := []*ActionPlanRecommendationResponse{
		{
			ID:               uuid.New().String(),
			SchoolID:         schoolID,
			ProfileDimension: "BERIMAN",
			Priority:         1,
			Action:           "Intensifkan kegiatan keagamaan dan pembinaan karakter",
			ExpectedOutcome:  "Peningkatan perilaku berakhlak mulia dan kepedulian sosial",
			Timeline:         "3 bulan",
			Resources:        []string{"guru agama", "tokoh masyarakat", "fasilitas ibadah"},
			Responsible:      "Wakil Kesiswaan",
			SuccessCriteria:  "90% siswa aktif dalam kegiatan keagamaan",
			CreatedAt:        time.Now(),
		},
		{
			ID:               uuid.New().String(),
			SchoolID:         schoolID,
			ProfileDimension: "MANDIRI",
			Priority:         2,
			Action:           "Kembangkan project-based learning mandiri",
			ExpectedOutcome:  "Meningkatkan kemampuan siswa dalam belajar mandiri",
			Timeline:         "6 bulan",
			Resources:        []string{"guru kelas", "perpustakaan", "laboratorium komputer"},
			Responsible:      "Kurikulum",
			SuccessCriteria:  "75% proyek diselesaikan dengan inisiatif siswa",
			CreatedAt:        time.Now(),
		},
	}

	return response, nil
}

// School Data Integration (FR 2.3)
func (s *service) GetSchoolDataForSWOT(ctx context.Context, schoolID string) (*SchoolDataAnalysisResponse, error) {
	if schoolID == "" {
		return nil, errors.New("invalid school ID")
	}

	// Placeholder implementation for school data analysis
	response := &SchoolDataAnalysisResponse{
		SchoolID:   schoolID,
		SchoolName: "UPT SDI Bonerate No. 85",
		InfrastructureData: &InfrastructureAnalysis{
			ClassroomCondition: &ConditionAnalysis{
				Total:    6,
				Good:     4,
				Damaged:  2,
				GoodRate: 66.7,
				Priority: "MEDIUM",
			},
			FacilityAvailability: &FacilityAnalysis{
				Library: &FacilityStatus{
					Available:   true,
					Count:       1,
					Condition:   "GOOD",
					Utilization: 75.0,
					Adequacy:    "ADEQUATE",
				},
				Toilets: &FacilityStatus{
					Available:   true,
					Count:       3,
					Condition:   "FAIR",
					Utilization: 85.0,
					Adequacy:    "NEEDS_IMPROVEMENT",
				},
			},
			MaintenanceNeeds: []*MaintenanceNeed{
				{
					Item:          "Ruang kelas 3",
					CurrentState:  "Atap bocor",
					RequiredState: "Atap kedap air",
					Priority:      2,
					EstimatedCost: 15000000,
					Timeline:      "1 bulan",
					Impact:        "Kenyamanan belajar",
				},
			},
			DigitalReadiness: 65.0,
		},
		HumanResourcesData: &HRAnalysis{
			TeacherData: &TeacherAnalysis{
				Total:         20,
				PNS:           12,
				Honor:         8,
				CertifiedRate: 85.0,
				QualifiedRate: 90.0,
				StudentRatio:  9.0,
				Adequacy:      "ADEQUATE",
			},
		},
		AcademicData: &AcademicAnalysis{
			StudentPerformance: &PerformanceAnalysis{
				AverageScore: 78.5,
				SubjectBreakdown: map[string]float64{
					"matematika": 75.0,
					"bahasa":     82.0,
					"ipa":        76.0,
				},
				Trend:            "IMPROVING",
				ImprovementAreas: []string{"numerasi", "literasi digital"},
			},
		},
		SWOTMapping: &SchoolSWOTMapping{
			Strengths: []*SchoolSWOTItem{
				{
					Category:    "HR",
					Description: "Rasio guru siswa yang ideal",
					Impact:      "HIGH",
					Priority:    1,
					DataSource:  "school_data",
				},
			},
			Weaknesses: []*SchoolSWOTItem{
				{
					Category:    "INFRASTRUCTURE",
					Description: "2 ruang kelas membutuhkan perbaikan",
					Impact:      "MEDIUM",
					Priority:    2,
					DataSource:  "school_data",
				},
			},
		},
		AnalysisDate: time.Now(),
	}

	return response, nil
}

func (s *service) GetDigitalReadinessAssessment(ctx context.Context, schoolID string) (*DigitalReadinessResponse, error) {
	if schoolID == "" {
		return nil, errors.New("invalid school ID")
	}

	// Placeholder implementation for digital readiness assessment
	response := &DigitalReadinessResponse{
		SchoolID:              schoolID,
		OverallReadinessScore: 65.0,
		ReadinessLevel:        "DEVELOPING",
		AssessmentAreas: []*ReadinessArea{
			{
				Area:            "Infrastructure",
				Score:           70.0,
				Level:           "DEVELOPING",
				Gaps:            []string{"Ketersediaan perangkat komunal terbatas"},
				Strengths:       []string{"Koneksi internet tersedia", "Jaringan WiFi sekolah"},
				Recommendations: []string{"Tambah perangkat komunal", "Optimalkan penggunaan perangkat pribadi"},
			},
			{
				Area:            "Teacher Capacity",
				Score:           60.0,
				Level:           "DEVELOPING",
				Gaps:            []string{"Training digital pedagogy terbatas"},
				Strengths:       []string{"Guru muda adaptif terhadap teknologi"},
				Recommendations: []string{"Pelatihan TIK untuk guru", "Mentoring antar guru"},
			},
		},
		CodingReadiness: &CodingReadiness{
			Score:                 55.0,
			Level:                 "EMERGING",
			TeacherCapacity:       50.0,
			Infrastructure:        60.0,
			CurriculumIntegration: 55.0,
			Recommendations:       []string{"Pelatihan coding dasar untuk guru", "Integrasi coding dalam project-based learning"},
		},
		AIReadiness: &AIReadiness{
			Score:             45.0,
			Level:             "EMERGING",
			TeacherAwareness:  40.0,
			Infrastructure:    50.0,
			EthicalGuidelines: 60.0,
			Recommendations:   []string{"Sosialisasi AI untuk pendidikan", "Panduan etika penggunaan AI"},
		},
		Recommendations: []string{
			"Fokus pada pengembangan kapasitas digital guru",
			"Integrasi bertahap teknologi dalam pembelajaran",
			"Kembangkan kebijakan penggunaan AI yang etis",
		},
		AssessmentDate: time.Now(),
	}

	return response, nil
}

func (s *service) GetSarprasPrioritization(ctx context.Context, schoolID string) ([]*SarprasPriorityResponse, error) {
	if schoolID == "" {
		return nil, errors.New("invalid school ID")
	}

	// Placeholder implementation for sarpras prioritization
	response := []*SarprasPriorityResponse{
		{
			ItemName:          "Perbaikan atap ruang kelas 3",
			CurrentCondition:  "Bocor",
			RequiredCondition: "Kedap air",
			PriorityScore:     85.0,
			PriorityLevel:     "HIGH",
			EstimatedCost:     15000000,
			Timeline:          "1 bulan",
			Impact:            "Kenyamanan belajar siswa",
			Urgency:           "HIGH",
			Dependencies:      []string{"Dana BOS", "Kontraktor lokal"},
			Recommendation:    "Segera perbaiki sebelum musim hujan",
		},
		{
			ItemName:          "Pengadaan komputer komunal",
			CurrentCondition:  "Tidak tersedia",
			RequiredCondition: "5 unit komputer lengkap",
			PriorityScore:     75.0,
			PriorityLevel:     "MEDIUM",
			EstimatedCost:     35000000,
			Timeline:          "3 bulan",
			Impact:            "Akses digital siswa",
			Urgency:           "MEDIUM",
			Dependencies:      []string{"Dana BOS", "Teknisi IT"},
			Recommendation:    "Prioritaskan untuk mendukung pembelajaran digital",
		},
		{
			ItemName:          "Perbaikan toilet siswa",
			CurrentCondition:  "Kurang layak",
			RequiredCondition: "Layak dan higienis",
			PriorityScore:     80.0,
			PriorityLevel:     "HIGH",
			EstimatedCost:     8000000,
			Timeline:          "2 bulan",
			Impact:            "Kesehatan dan kenyamanan siswa",
			Urgency:           "HIGH",
			Dependencies:      []string{"Dana BOS", "Tukang bangunan"},
			Recommendation:    "Perbaiki sanitasi untuk kesehatan siswa",
		},
	}

	return response, nil
}

// FASE 5: Analysis Tool Enhancements

// SWOT Builder Enhancements (FR 3.1)

func (s *service) GetSWOTAnalyticsAggregation(ctx context.Context, sessionID string) (*SWOTAnalyticsResponse, error) {
	sessionUID, err := uuid.Parse(sessionID)
	if err != nil {
		return nil, errors.New("invalid session ID")
	}

	// Get SWOT session items
	items, err := s.repo.GetSWOTSessionItems(ctx, sessionUID)
	if err != nil {
		return nil, err
	}

	response := &SWOTAnalyticsResponse{
		SessionID: sessionID,
	}

	// Count items by quadrant
	strengthsCount := 0
	weaknessesCount := 0
	opportunitiesCount := 0
	threatsCount := 0

	for _, item := range items {
		if item.Quadrant == nil {
			continue
		}
		switch *item.Quadrant {
		case "STRENGTHS":
			strengthsCount++
		case "WEAKNESSES":
			weaknessesCount++
		case "OPPORTUNITIES":
			opportunitiesCount++
		case "THREATS":
			threatsCount++
		}
	}

	response.TotalItems = struct {
		Strengths     int `json:"strengths"`
		Weaknesses    int `json:"weaknesses"`
		Opportunities int `json:"opportunities"`
		Threats       int `json:"threats"`
	}{
		Strengths:     strengthsCount,
		Weaknesses:    weaknessesCount,
		Opportunities: opportunitiesCount,
		Threats:       threatsCount,
	}

	// Data mapping counts (placeholder - would need to track mappings in DB)
	response.DataMappingCount = struct {
		Strengths     int `json:"strengths"`
		Weaknesses    int `json:"weaknesses"`
		Opportunities int `json:"opportunities"`
		Threats       int `json:"threats"`
	}{
		Strengths:     0,
		Weaknesses:    0,
		Opportunities: 0,
		Threats:       0,
	}

	// Category breakdown
	categoryMap := make(map[string]int)
	for _, item := range items {
		if item.Category != nil {
			categoryMap[*item.Category]++
		}
	}

	for category, count := range categoryMap {
		response.CategoryBreakdown = append(response.CategoryBreakdown, struct {
			Category string `json:"category"`
			Count    int    `json:"count"`
		}{
			Category: category,
			Count:    count,
		})
	}

	// Data source breakdown (placeholder)
	response.DataSourceBreakdown = []struct {
		SourceType string `json:"source_type"`
		Count      int    `json:"count"`
	}{}

	// Get session for timestamps
	session, err := s.repo.GetSWOTSessionByID(ctx, sessionUID)
	if err == nil {
		response.CreatedAt = session.CreatedAt
		response.UpdatedAt = session.UpdatedAt
	} else {
		response.CreatedAt = time.Now()
		response.UpdatedAt = time.Now()
	}

	return response, nil
}

func (s *service) MapDataToSWOTItem(ctx context.Context, req SWOTDataMappingRequest) (*SWOTItem, error) {
	itemUID, err := uuid.Parse(req.ItemID)
	if err != nil {
		return nil, errors.New("invalid item ID")
	}

	// Get the SWOT item
	item, err := s.repo.GetSWOTItemByID(ctx, itemUID)
	if err != nil {
		return nil, errors.New("SWOT item not found")
	}

	// Store mapping metadata (this would need to be added to the model)
	// For now, we'll add it to the description field
	mappingInfo := fmt.Sprintf("Data Source: %s (ID: %s, Field: %s). Confidence: %.2f. Notes: %s",
		req.SourceType, req.SourceID, req.SourceField, req.Confidence, req.Notes)

	if item.Description != nil {
		*item.Description = *item.Description + "\n\n" + mappingInfo
	} else {
		item.Description = &mappingInfo
	}

	if err := s.repo.UpdateSWOTItem(ctx, item); err != nil {
		return nil, err
	}

	return item, nil
}

func (s *service) GetAvailableDataSourceTypes(ctx context.Context, schoolID string) ([]*DataSourceTypeResponse, error) {
	if schoolID == "" {
		return nil, errors.New("invalid school ID")
	}

	// Check availability of different data sources
	response := []*DataSourceTypeResponse{
		{
			SourceType: "RAPOR",
			SourceName: "Rapor Pendidikan Digital",
			Available:  true, // Would need to check actual data
			Count:      0,
		},
		{
			SourceType: "SURVEY",
			SourceName: "Survei Digital",
			Available:  true,
			Count:      0,
		},
		{
			SourceType: "SARPRAS",
			SourceName: "Sarana Prasarana",
			Available:  true,
			Count:      0,
		},
		{
			SourceType: "SCHOOL_DATA",
			SourceName: "Data Sekolah",
			Available:  true,
			Count:      0,
		},
	}

	return response, nil
}

func (s *service) ExportSWOTAnalysis(ctx context.Context, sessionID string, format string) ([]byte, error) {
	sessionUID, err := uuid.Parse(sessionID)
	if err != nil {
		return nil, errors.New("invalid session ID")
	}

	session, err := s.repo.GetSWOTSessionByID(ctx, sessionUID)
	if err != nil {
		return nil, errors.New("SWOT session not found")
	}

	items, err := s.repo.GetSWOTSessionItems(ctx, sessionUID)
	if err != nil {
		return nil, err
	}

	switch format {
	case "json":
		exportData := map[string]interface{}{
			"session":     session,
			"items":       items,
			"exported_at": time.Now(),
		}
		return json.Marshal(exportData)
	case "csv":
		// Build CSV
		var csvBuilder strings.Builder
		csvBuilder.WriteString("Quadrant,Title,Description,Category,Priority,CreatedAt\n")
		for _, item := range items {
			category := ""
			if item.Category != nil {
				category = *item.Category
			}
			quadrant := ""
			if item.Quadrant != nil {
				quadrant = *item.Quadrant
			}
			csvBuilder.WriteString(fmt.Sprintf("%v,%v,%v,%v,%v,%v\n",
				quadrant,
				item.SWOTItemID.String(),
				strings.ReplaceAll(fmt.Sprintf("%v", item.Notes), ",", ";"),
				category,
				item.SequenceOrder,
				item.CreatedAt.Format("2006-01-02 15:04:05")))
		}
		return []byte(csvBuilder.String()), nil
	default:
		return nil, errors.New("unsupported export format")
	}
}

// Root Cause Analyzer Enhancements (FR 3.2)

func (s *service) Perform5WhysAnalysis(ctx context.Context, req FiveWhysRequest) (*FiveWhysResponse, error) {
	rootCauseUID, err := uuid.Parse(req.RootCauseID)
	if err != nil {
		return nil, errors.New("invalid root cause ID")
	}

	rootCause, err := s.repo.GetRootCauseByID(ctx, rootCauseUID)
	if err != nil {
		return nil, errors.New("root cause not found")
	}

	maxDepth := req.MaxDepth
	if maxDepth == 0 {
		maxDepth = 5
	}

	// Build 5-Whys analysis tree
	analysisTree := s.build5WhysTree(req.Problem, maxDepth, rootCause)

	response := &FiveWhysResponse{
		RootCauseID:  req.RootCauseID,
		Problem:      req.Problem,
		AnalysisTree: analysisTree,
		Conclusion:   s.generate5WhysConclusion(analysisTree),
		Confidence:   0.75, // Placeholder
		CreatedAt:    time.Now(),
	}

	return response, nil
}

func (s *service) build5WhysTree(problem string, maxDepth int, rootCause *RootCause) []FiveWhysNode {
	// Simplified 5-Whys algorithm
	tree := []FiveWhysNode{
		{
			Level:    1,
			Question: "Mengapa " + problem + "?",
			Answer:   rootCause.IdentifiedProblem,
			Evidence: []string{},
			Children: []FiveWhysNode{
				{
					Level:    2,
					Question: "Mengapa " + rootCause.IdentifiedProblem + "?",
					Answer:   rootCause.RootCause,
					Evidence: []string{},
					Children: []FiveWhysNode{},
				},
			},
		},
	}

	return tree
}

func (s *service) generate5WhysConclusion(tree []FiveWhysNode) string {
	// Simple conclusion generation
	if len(tree) == 0 {
		return "Tidak cukup data untuk kesimpulan"
	}

	// Find the deepest answer
	deepestAnswer := tree[0].Answer
	currentNode := tree[0]
	for len(currentNode.Children) > 0 {
		currentNode = currentNode.Children[0]
		deepestAnswer = currentNode.Answer
	}

	return fmt.Sprintf("Akar masalah teridentifikasi: %s", deepestAnswer)
}

func (s *service) LinkRaporMetricToRootCause(ctx context.Context, req RaporMetricLinkRequest) error {
	rootCauseUID, err := uuid.Parse(req.RootCauseID)
	if err != nil {
		return errors.New("invalid root cause ID")
	}

	if req.MetricID == "" {
		return errors.New("invalid metric ID")
	}

	rootCause, err := s.repo.GetRootCauseByID(ctx, rootCauseUID)
	if err != nil {
		return errors.New("root cause not found")
	}

	// Store the link (would need to add a linking table)
	// For now, add to description
	linkInfo := fmt.Sprintf("\n\nRapor Metric Link: Type=%s, MetricID=%s, Confidence=%.2f, Notes=%s",
		req.LinkType, req.MetricID, req.Confidence, req.Notes)

	rootCause.IdentifiedProblem += linkInfo

	return s.repo.UpdateRootCause(ctx, rootCause)
}

func (s *service) GetRootCauseSuggestions(ctx context.Context, rootCauseID string) ([]*RootCauseSuggestionResponse, error) {
	rootCauseUID, err := uuid.Parse(rootCauseID)
	if err != nil {
		return nil, errors.New("invalid root cause ID")
	}

	rootCause, err := s.repo.GetRootCauseByID(ctx, rootCauseUID)
	if err != nil {
		return nil, errors.New("root cause not found")
	}

	// Generate suggestions based on root cause
	suggestions := []*RootCauseSuggestionResponse{
		{
			SuggestionID: uuid.New().String(),
			RootCauseID:  rootCauseID,
			Title:        "Program pembinaan guru",
			Description:  "Laksanakan pelatihan berkelanjutan untuk meningkatkan kompetensi guru",
			Evidence:     []string{rootCause.IdentifiedProblem},
			Priority:     "HIGH",
			Source:       "SYSTEM",
			Relevance:    0.85,
		},
		{
			SuggestionID: uuid.New().String(),
			RootCauseID:  rootCauseID,
			Title:        "Peningkatan sarana prasarana",
			Description:  "Perbaiki dan lengkapi fasilitas pembelajaran yang kurang memadai",
			Evidence:     []string{rootCause.RootCause},
			Priority:     "MEDIUM",
			Source:       "SYSTEM",
			Relevance:    0.70,
		},
	}

	return suggestions, nil
}

func (s *service) ExportRootCauseAnalysis(ctx context.Context, rootCauseID string, format string) ([]byte, error) {
	rootCauseUID, err := uuid.Parse(rootCauseID)
	if err != nil {
		return nil, errors.New("invalid root cause ID")
	}

	rootCause, err := s.repo.GetRootCauseByID(ctx, rootCauseUID)
	if err != nil {
		return nil, errors.New("root cause not found")
	}

	history, err := s.repo.GetRootCauseHistoryByRootCauseID(ctx, rootCauseUID)
	if err != nil {
		history = []*RootCauseHistory{}
	}

	switch format {
	case "json":
		exportData := map[string]interface{}{
			"root_cause":  rootCause,
			"history":     history,
			"exported_at": time.Now(),
		}
		return json.Marshal(exportData)
	case "csv":
		var csvBuilder strings.Builder
		csvBuilder.WriteString("Problem,RootCause,KegiatanBenahi,Status,Priority,CreatedAt\n")
		csvBuilder.WriteString(fmt.Sprintf("%s,%s,%s,%s,%v,%s\n",
			strings.ReplaceAll(rootCause.IdentifiedProblem, ",", ";"),
			strings.ReplaceAll(rootCause.RootCause, ",", ";"),
			strings.ReplaceAll(rootCause.KegiatanBenahi, ",", ";"),
			rootCause.Status,
			rootCause.ActionPriority,
			rootCause.CreatedAt.Format("2006-01-02 15:04:05")))
		return []byte(csvBuilder.String()), nil
	default:
		return nil, errors.New("unsupported export format")
	}
}

// Fishbone Diagram Enhancements (FR 3.3)

func (s *service) GetFishboneAnalytics(ctx context.Context, diagramID string) (*FishboneAnalyticsResponse, error) {
	diagramUID, err := uuid.Parse(diagramID)
	if err != nil {
		return nil, errors.New("invalid diagram ID")
	}

	diagram, err := s.repo.GetFishboneDiagramByID(ctx, diagramUID)
	if err != nil {
		return nil, errors.New("fishbone diagram not found")
	}

	nodes, err := s.repo.GetFishboneNodesByDiagram(ctx, diagramUID)
	if err != nil {
		return nil, err
	}

	connections, err := s.repo.GetFishboneConnectionsByDiagram(ctx, diagramUID)
	if err != nil {
		return nil, err
	}

	response := &FishboneAnalyticsResponse{
		DiagramID:  diagramID,
		TotalNodes: len(nodes),
		TotalEdges: len(connections),
	}

	// Category breakdown
	categoryMap := make(map[string]int)
	for _, node := range nodes {
		categoryMap[node.BoneCategory]++
	}

	for category, count := range categoryMap {
		response.CategoryStats = append(response.CategoryStats, struct {
			Category  string `json:"category"`
			NodeCount int    `json:"node_count"`
		}{
			Category:  category,
			NodeCount: count,
		})
	}

	// Depth analysis
	depthMap := make(map[int]int)
	for _, node := range nodes {
		depth := s.calculateNodeDepth(node, nodes)
		depthMap[depth]++
	}

	for depth, count := range depthMap {
		response.DepthAnalysis = append(response.DepthAnalysis, struct {
			Depth int `json:"depth"`
			Count int `json:"count"`
		}{
			Depth: depth,
			Count: count,
		})
	}

	response.CreatedAt = diagram.CreatedAt
	response.UpdatedAt = diagram.UpdatedAt

	return response, nil
}

func (s *service) calculateNodeDepth(node *FishboneNode, allNodes []*FishboneNode) int {
	depth := 0
	currentNode := node
	for currentNode.ParentNodeID != nil {
		for _, n := range allNodes {
			if n.ID == *currentNode.ParentNodeID {
				currentNode = n
				depth++
				break
			}
		}
	}
	return depth
}

func (s *service) ValidateFishboneStructure(ctx context.Context, diagramID string) (*FishboneValidationResponse, error) {
	diagramUID, err := uuid.Parse(diagramID)
	if err != nil {
		return nil, errors.New("invalid diagram ID")
	}

	diagram, err := s.repo.GetFishboneDiagramByID(ctx, diagramUID)
	if err != nil {
		return nil, errors.New("fishbone diagram not found")
	}

	nodes, err := s.repo.GetFishboneNodesByDiagram(ctx, diagramUID)
	if err != nil {
		return nil, err
	}

	connections, err := s.repo.GetFishboneConnectionsByDiagram(ctx, diagramUID)
	if err != nil {
		return nil, err
	}

	response := &FishboneValidationResponse{
		DiagramID:   diagramID,
		IsValid:     true,
		Issues:      []string{},
		Warnings:    []string{},
		Suggestions: []string{},
	}

	// Validate structure
	if len(nodes) == 0 {
		response.IsValid = false
		response.Issues = append(response.Issues, "Diagram tidak memiliki node")
	}

	if diagram.HeadEffect == "" {
		response.IsValid = false
		response.Issues = append(response.Issues, "Head effect belum diisi")
	}

	// Check for orphaned nodes
	connectedNodes := make(map[uuid.UUID]bool)
	for _, conn := range connections {
		connectedNodes[conn.FromNodeID] = true
		connectedNodes[conn.ToNodeID] = true
	}

	for _, node := range nodes {
		if node.ParentNodeID == nil && !connectedNodes[node.ID] {
			response.Warnings = append(response.Warnings, fmt.Sprintf("Node '%s' tidak terhubung", node.CauseText))
		}
	}

	// Suggestions
	if len(nodes) < 5 {
		response.Suggestions = append(response.Suggestions, "Tambahkan lebih banyak node untuk analisis yang lebih komprehensif")
	}

	if response.IsValid {
		response.Suggestions = append(response.Suggestions, "Struktur diagram valid dan siap digunakan")
	}

	return response, nil
}

func (s *service) GetFishboneCategories(ctx context.Context) ([]*FishboneCategoryResponse, error) {
	// Return preset fishbone categories
	categories := []*FishboneCategoryResponse{
		{
			CategoryID:   "MAN",
			CategoryName: "Manusia",
			Description:  "Faktor terkait SDM (guru, staff, siswa)",
			Icon:         "users",
			Color:        "#3B82F6",
			IsPreset:     true,
		},
		{
			CategoryID:   "METHOD",
			CategoryName: "Metode",
			Description:  "Faktor terkait proses dan metode pembelajaran",
			Icon:         "clipboard",
			Color:        "#10B981",
			IsPreset:     true,
		},
		{
			CategoryID:   "MACHINE",
			CategoryName: "Mesin",
			Description:  "Faktor terkait peralatan dan teknologi",
			Icon:         "cpu",
			Color:        "#8B5CF6",
			IsPreset:     true,
		},
		{
			CategoryID:   "MATERIAL",
			CategoryName: "Material",
			Description:  "Faktor terkait bahan dan sumber belajar",
			Icon:         "book",
			Color:        "#F59E0B",
			IsPreset:     true,
		},
		{
			CategoryID:   "ENVIRONMENT",
			CategoryName: "Lingkungan",
			Description:  "Faktor terkait lingkungan fisik dan sosial",
			Icon:         "globe",
			Color:        "#EF4444",
			IsPreset:     true,
		},
	}

	return categories, nil
}

func (s *service) ExportFishboneDiagram(ctx context.Context, diagramID string, format string) ([]byte, error) {
	diagramUID, err := uuid.Parse(diagramID)
	if err != nil {
		return nil, errors.New("invalid diagram ID")
	}

	diagram, err := s.repo.GetFishboneDiagramByID(ctx, diagramUID)
	if err != nil {
		return nil, errors.New("fishbone diagram not found")
	}

	nodes, err := s.repo.GetFishboneNodesByDiagram(ctx, diagramUID)
	if err != nil {
		return nil, err
	}

	connections, err := s.repo.GetFishboneConnectionsByDiagram(ctx, diagramUID)
	if err != nil {
		return nil, err
	}

	switch format {
	case "json":
		exportData := map[string]interface{}{
			"diagram":     diagram,
			"nodes":       nodes,
			"connections": connections,
			"exported_at": time.Now(),
		}
		return json.Marshal(exportData)
	case "csv":
		var csvBuilder strings.Builder
		csvBuilder.WriteString("NodeType,ID,Text,Category,ParentID,PositionX,PositionY\n")
		csvBuilder.WriteString(fmt.Sprintf("HEAD,%s,%s,,,%f,%f\n",
			diagram.ID,
			strings.ReplaceAll(diagram.HeadEffect, ",", ";"),
			0.0, 0.0))

		for _, node := range nodes {
			parentID := ""
			if node.ParentNodeID != nil {
				parentID = node.ParentNodeID.String()
			}
			csvBuilder.WriteString(fmt.Sprintf("NODE,%s,%s,%s,%s,%v,%v\n",
				node.ID,
				strings.ReplaceAll(node.CauseText, ",", ";"),
				node.BoneCategory,
				parentID,
				node.PositionX,
				node.PositionY))
		}
		return []byte(csvBuilder.String()), nil
	default:
		return nil, errors.New("unsupported export format")
	}
}

// Extended Review and Approval Workflow Methods (FR 4.1.13) - Moved to service_ksp_phase6.go
// Version History Management Methods (FR 4.1.5) - Moved to service_ksp_phase6.go

// FASE 6: KSP Enhanced Generation Methods

// Document Compilation & Snapshot Methods (FR 4.1.1, FR 4.1.2) - Moved to service_ksp_phase6.go

// Chart Generation Methods (FR 4.1.3)
// GenerateChartsFromAnalysis moved to service_ksp_phase6.go

func (s *service) GenerateSWOTChart(ctx context.Context, data SWOTChartData, chartType string) (*ChartGenerationResponse, error) {
	// Validate input data
	if data.Strengths == 0 && data.Weaknesses == 0 && data.Opportunities == 0 && data.Threats == 0 {
		return nil, errors.New("SWOT data cannot be empty")
	}

	// Generate chart data based on chart type
	chartData := make(map[string]interface{})

	switch chartType {
	case "BAR":
		chartData = map[string]interface{}{
			"type": "bar",
			"data": map[string]interface{}{
				"labels": []string{"Strengths", "Weaknesses", "Opportunities", "Threats"},
				"datasets": []map[string]interface{}{
					{
						"label": "Count",
						"data":  []int{data.Strengths, data.Weaknesses, data.Opportunities, data.Threats},
					},
				},
			},
		}
	case "PIE":
		chartData = map[string]interface{}{
			"type": "pie",
			"data": map[string]interface{}{
				"labels": []string{"Strengths", "Weaknesses", "Opportunities", "Threats"},
				"datasets": []map[string]interface{}{
					{
						"data": []int{data.Strengths, data.Weaknesses, data.Opportunities, data.Threats},
					},
				},
			},
		}
	case "RADAR":
		chartData = map[string]interface{}{
			"type": "radar",
			"data": map[string]interface{}{
				"labels": []string{"Strengths", "Weaknesses", "Opportunities", "Threats"},
				"datasets": []map[string]interface{}{
					{
						"label": "SWOT Analysis",
						"data":  []int{data.Strengths, data.Weaknesses, data.Opportunities, data.Threats},
					},
				},
			},
		}
	default:
		return nil, errors.New("unsupported chart type")
	}

	chartID := uuid.New().String()
	chartURL := fmt.Sprintf("/api/v1/strategic-planning/charts/swot/%s.%s", chartID, strings.ToLower(chartType))
	_ = chartData

	response := &ChartGenerationResponse{
		ChartID:     chartID,
		ChartURL:    chartURL,
		ChartType:   chartType,
		GeneratedAt: time.Now().Format(time.RFC3339),
	}

	return response, nil
}

func (s *service) GenerateRootCauseChart(ctx context.Context, data RootCauseChartData, chartType string) (*ChartGenerationResponse, error) {
	response := &ChartGenerationResponse{
		ChartID:     uuid.New().String(),
		ChartURL:    "/charts/root-cause-" + chartType + "-" + uuid.New().String() + ".png",
		ChartType:   chartType,
		GeneratedAt: time.Now().Format(time.RFC3339),
	}

	return response, nil
}

func (s *service) GenerateFishboneChart(ctx context.Context, data FishboneChartData, chartType string) (*ChartGenerationResponse, error) {
	response := &ChartGenerationResponse{
		ChartID:     uuid.New().String(),
		ChartURL:    "/charts/fishbone-" + chartType + "-" + uuid.New().String() + ".png",
		ChartType:   chartType,
		GeneratedAt: time.Now().Format(time.RFC3339),
	}

	return response, nil
}

func (s *service) GenerateStudentNeedsChart(ctx context.Context, data StudentNeedsChartData, chartType string) (*ChartGenerationResponse, error) {
	response := &ChartGenerationResponse{
		ChartID:     uuid.New().String(),
		ChartURL:    "/charts/student-needs-" + chartType + "-" + uuid.New().String() + ".png",
		ChartType:   chartType,
		GeneratedAt: time.Now().Format(time.RFC3339),
	}

	return response, nil
}

// AI Integration Methods (FR 4.1.4)

func (s *service) GenerateAIContent(ctx context.Context, req AIContentGenerationRequest) (*AIContentGenerationResponse, error) {
	return s.GenerateContentWithAI(ctx, req)
}

func (s *service) GetAIRecommendations(ctx context.Context, req AIRecommendationRequest) (*AIRecommendationResponse, error) {
	response := &AIRecommendationResponse{
		Recommendations: []string{
			"Recommendation 1: Improve SWOT analysis depth",
			"Recommendation 2: Add more stakeholder input",
			"Recommendation 3: Consider environmental factors",
		},
		Confidence:  0.85,
		GeneratedAt: time.Now().Format(time.RFC3339),
	}

	return response, nil
}

func (s *service) GetAIIntegrationConfig(ctx context.Context) (*AIIntegrationConfig, error) {
	config := &AIIntegrationConfig{
		APIEndpoint:  "https://api.openai.com/v1",
		APIKey:       "sk-****",
		ModelVersion: "gpt-4",
		MaxTokens:    4000,
		Temperature:  0.7,
		Timeout:      30,
		Enabled:      true,
	}

	return config, nil
}

func (s *service) UpdateAIIntegrationConfig(ctx context.Context, config AIIntegrationConfig) error {
	return nil
}

func (s *service) GenerateContentWithAI(ctx context.Context, req AIContentGenerationRequest) (*AIContentGenerationResponse, error) {
	if s.aiClient == nil {
		return nil, errors.New("AI client not initialized")
	}

	analysisCtx := "{}"
	if req.Context != nil {
		if b, err := json.Marshal(req.Context); err == nil {
			analysisCtx = string(b)
		}
	}

	grpcReq := &pb.GenerateKSPSectionRequest{
		RequestId:       uuid.New().String(),
		Metadata: &pb.AnalysisMetadata{
			Language: req.Language,
		},
		SectionKey:      req.ContentType,
		SectionTitle:    req.ContentType,
		AnalysisContext: analysisCtx,
		MaxWords:        int32(req.MaxLength),
	}

	resp, err := s.aiClient.GenerateKSPSection(ctx, grpcReq)
	if err != nil {
		return nil, fmt.Errorf("failed to call AI service: %w", err)
	}

	if !resp.Success {
		return nil, fmt.Errorf("AI service error: %s", resp.Message)
	}

	return &AIContentGenerationResponse{
		ContentID:        uuid.New().String(),
		GeneratedContent: resp.Section.Content,
		Confidence:       0.95,
		WordCount:        int(resp.TokensUsed), // approximate
		TokensUsed:       int(resp.TokensUsed),
		GeneratedAt:      time.Now().Format(time.RFC3339),
	}, nil
}

// GenerateRecommendationsWithAI moved to service_ksp_phase6.go

// Approval Workflow Methods (FR 4.1.13)

func (s *service) AssignWorkflowStep(ctx context.Context, workflowID string, stepID string, documentID string, assignedTo string, assignedBy string) (*WorkflowStepAssignment, error) {
	assignment := &WorkflowStepAssignment{
		ID:         uuid.New().String(),
		WorkflowID: workflowID,
		StepID:     stepID,
		DocumentID: documentID,
		AssignedTo: assignedTo,
		AssignedBy: assignedBy,
		AssignedAt: time.Now().Format(time.RFC3339),
		Status:     "PENDING",
	}

	return assignment, nil
}

// Fishbone Template Management Methods (T-5.3.14)

func (s *service) CreateFishboneTemplate(ctx context.Context, req CreateFishboneTemplateRequest, createdBy string) (*FishboneTemplate, error) {
	creatorID, _ := uuid.Parse(createdBy)
	template := &FishboneTemplate{
		ID:                  uuid.New(),
		TemplateName:        req.TemplateName,
		TemplateDescription: req.TemplateDescription,
		TemplateCategory:    req.TemplateCategory,
		HeadEffect:          req.HeadEffect,
		PresetNodes:         req.PresetNodes,
		IsPublic:            req.IsPublic,
		IsActive:            true,
		CreatedBy:           creatorID,
		CreatedAt:           time.Now(),
		UpdatedAt:           time.Now(),
	}

	return template, nil
}

func (s *service) GetFishboneTemplateByID(ctx context.Context, id string) (*FishboneTemplate, error) {
	uid, _ := uuid.Parse(id)
	template := &FishboneTemplate{
		ID:                  uid,
		TemplateName:        "Sample Fishbone Template",
		TemplateDescription: "Sample description",
		TemplateCategory:    "Quality",
		HeadEffect:          "Sample Head Effect",
		IsPublic:            true,
		CreatedAt:           time.Now(),
		UpdatedAt:           time.Now(),
	}

	return template, nil
}

func (s *service) GetPublicFishboneTemplates(ctx context.Context, category string) ([]*FishboneTemplate, error) {
	templates := []*FishboneTemplate{
		{
			ID:                  uuid.New(),
			TemplateName:        "Public Template 1",
			TemplateDescription: "Description",
			TemplateCategory:    category,
			IsPublic:            true,
			CreatedAt:           time.Now(),
		},
	}

	return templates, nil
}

func (s *service) GetFishboneTemplatesBySchool(ctx context.Context, schoolID string) ([]*FishboneTemplate, error) {
	templates := []*FishboneTemplate{
		{
			ID:                  uuid.New(),
			TemplateName:        "School Template 1",
			TemplateDescription: "Description",
			IsPublic:            false,
			CreatedAt:           time.Now(),
		},
	}

	return templates, nil
}

func (s *service) UpdateFishboneTemplate(ctx context.Context, id string, req UpdateFishboneTemplateRequest) (*FishboneTemplate, error) {
	uid, _ := uuid.Parse(id)
	template := &FishboneTemplate{
		ID:        uid,
		UpdatedAt: time.Now(),
	}
	if req.TemplateName != nil {
		template.TemplateName = *req.TemplateName
	}
	if req.TemplateDescription != nil {
		template.TemplateDescription = *req.TemplateDescription
	}
	if req.TemplateCategory != nil {
		template.TemplateCategory = *req.TemplateCategory
	}

	return template, nil
}

func (s *service) DeleteFishboneTemplate(ctx context.Context, id string) error {
	return nil
}
