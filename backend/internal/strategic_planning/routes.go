package strategic_planning

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
	
	grpc_clients "sim-sekolah/internal/ai/grpc"
)

func SetupRoutes(router fiber.Router, db *gorm.DB) {
	// Initialize AI Client
	aiClient, err := grpc_clients.NewStrategicAnalysisClient("strategic-analysis-service:50063")
	if err != nil {
		// Log error but continue to allow non-AI features to work
		// A proper logger would be better here
		_ = err
	}

	repo := NewRepository(db)
	svc := NewService(repo, aiClient)
	h := NewHandler(svc)

	group := router.Group("/strategic-planning")
	group.Use(middleware.Protected())

	// Rapor Pendidikan Routes
	rapor := group.Group("/rapor")
	rapor.Post("/", h.CreateRaporPendidikan)
	rapor.Get("/:id", h.GetRaporPendidikanByID)
	rapor.Get("/school/:schoolId", h.GetRaporPendidikanBySchool)
	rapor.Put("/:id", h.UpdateRaporPendidikan)
	rapor.Delete("/:id", h.DeleteRaporPendidikan)
	rapor.Post("/sync", h.SyncRaporPendidikan)

	// Survey Routes
	surveys := group.Group("/surveys")
	surveys.Post("/", h.CreateSurvey)
	surveys.Get("/:id", h.GetSurveyByID)
	surveys.Get("/school/:schoolId", h.GetSurveysBySchool)
	surveys.Put("/:id", h.UpdateSurvey)
	surveys.Delete("/:id", h.DeleteSurvey)
	surveys.Get("/templates", h.GetSurveyTemplates)
	surveys.Get("/school/:schoolId/active", h.GetActiveSurveys)
	surveys.Post("/:id/responses", h.SubmitSurveyResponse)
	surveys.Get("/:id/responses", h.GetSurveyResponses)
	surveys.Get("/:id/analytics", h.GetSurveyAnalytics)

	// FGD Session Routes
	fgd := group.Group("/fgd")
	fgd.Post("/", h.CreateFGDSession)
	fgd.Get("/:id", h.GetFGDSessionByID)
	fgd.Get("/school/:schoolId", h.GetFGDSessionsBySchool)
	fgd.Put("/:id", h.UpdateFGDSession)
	fgd.Delete("/:id", h.DeleteFGDSession)
	fgd.Get("/school/:schoolId/upcoming", h.GetUpcomingFGDSessions)
	fgd.Post("/:id/participants", h.AddFGDParticipant)
	fgd.Get("/:id/participants", h.GetFGDParticipants)
	fgd.Put("/participants/:id", h.UpdateFGDParticipant)
	fgd.Delete("/participants/:id", h.DeleteFGDParticipant)

	// Student Needs Enhanced Routes
	studentNeeds := group.Group("/student-needs")
	studentNeeds.Post("/", h.CreateStudentNeedsEnhanced)
	studentNeeds.Get("/:id", h.GetStudentNeedsEnhancedByID)
	studentNeeds.Get("/school/:schoolId", h.GetStudentNeedsEnhancedBySchool)
	studentNeeds.Get("/school/:schoolId/profile", h.GetStudentNeedsEnhancedByProfile)
	studentNeeds.Put("/:id", h.UpdateStudentNeedsEnhanced)
	studentNeeds.Delete("/:id", h.DeleteStudentNeedsEnhanced)

	// SWOT Routes
	swot := group.Group("/swot")
	swot.Post("/items", h.CreateSWOTItem)
	swot.Get("/items/:id", h.GetSWOTItemByID)
	swot.Get("/items/school/:schoolId", h.GetSWOTItemsBySchool)
	swot.Put("/items/:id", h.UpdateSWOTItem)
	swot.Delete("/items/:id", h.DeleteSWOTItem)
	swot.Post("/sessions", h.CreateSWOTAnalysisSession)
	swot.Get("/sessions/:id", h.GetSWOTAnalysisSessionByID)
	swot.Get("/sessions/school/:schoolId", h.GetSWOTAnalysisSessionsBySchool)
	swot.Put("/sessions/:id", h.UpdateSWOTAnalysisSession)
	swot.Delete("/sessions/:id", h.DeleteSWOTAnalysisSession)
	swot.Post("/sessions/:id/items", h.AddSWOTItemToSession)
	swot.Get("/sessions/:id/items", h.GetSWOTSessionItems)

	// Root Cause Routes
	rootCause := group.Group("/root-cause")
	rootCause.Post("/", h.CreateRootCause)
	rootCause.Get("/:id", h.GetRootCauseByID)
	rootCause.Get("/school/:schoolId", h.GetRootCausesBySchool)
	rootCause.Put("/:id", h.UpdateRootCause)
	rootCause.Delete("/:id", h.DeleteRootCause)
	rootCause.Post("/:id/validate", h.ValidateRootCause)
	rootCause.Get("/:id/history", h.GetRootCauseHistory)

	// Fishbone Routes
	fishbone := group.Group("/fishbone")
	fishbone.Post("/diagrams", h.CreateFishboneDiagram)
	fishbone.Get("/diagrams/:id", h.GetFishboneDiagramByID)
	fishbone.Get("/diagrams/school/:schoolId", h.GetFishboneDiagramsBySchool)
	fishbone.Put("/diagrams/:id", h.UpdateFishboneDiagram)
	fishbone.Delete("/diagrams/:id", h.DeleteFishboneDiagram)
	fishbone.Post("/diagrams/:diagramId/nodes", h.CreateFishboneNode)
	fishbone.Get("/diagrams/:diagramId/nodes", h.GetFishboneNodesByDiagram)
	fishbone.Put("/nodes/:id", h.UpdateFishboneNode)
	fishbone.Delete("/nodes/:id", h.DeleteFishboneNode)
	fishbone.Post("/diagrams/:diagramId/connections", h.CreateFishboneConnection)
	fishbone.Get("/diagrams/:diagramId/connections", h.GetFishboneConnections)
	fishbone.Delete("/connections/:id", h.DeleteFishboneConnection)

	// KSP Integration Routes
	kspIntegration := group.Group("/ksp-integration")
	kspIntegration.Post("/", h.CreateKSPAnalysisIntegration)
	kspIntegration.Get("/:id", h.GetKSPAnalysisIntegrationByID)
	kspIntegration.Get("/document/:documentId", h.GetKSPAnalysisIntegrationsByDocument)
	kspIntegration.Put("/:id", h.UpdateKSPAnalysisIntegration)
	kspIntegration.Delete("/:id", h.DeleteKSPAnalysisIntegration)
	kspIntegration.Post("/:id/approve", h.ApproveKSPAnalysisIntegration)
	kspIntegration.Post("/:id/recommendations", h.CreateKSPAnalysisRecommendation)
	kspIntegration.Get("/:id/recommendations", h.GetKSPAnalysisRecommendations)
	kspIntegration.Put("/recommendations/:id", h.UpdateKSPAnalysisRecommendation)
	kspIntegration.Delete("/recommendations/:id", h.DeleteKSPAnalysisRecommendation)

	// KSP Template Routes
	kspTemplates := group.Group("/ksp-templates")
	kspTemplates.Post("/", h.CreateKSPAnalysisTemplate)
	kspTemplates.Get("/:id", h.GetKSPAnalysisTemplateByID)
	kspTemplates.Get("/public", h.GetPublicKSPAnalysisTemplates)
	kspTemplates.Get("/school/:schoolId", h.GetKSPAnalysisTemplatesBySchool)
	kspTemplates.Put("/:id", h.UpdateKSPAnalysisTemplate)
	kspTemplates.Delete("/:id", h.DeleteKSPAnalysisTemplate)
	kspTemplates.Post("/:id/increment-usage", h.IncrementTemplateUsage)

	// FASE 4: Integration Routes

	// Local Context Integration (FR 2.1)
	localContext := group.Group("/local-context")
	localContext.Get("/school/:schoolId/swot", h.GetLocalContextForSWOT)
	localContext.Get("/school/:schoolId/learning-potential", h.AnalyzeLearningPotential)
	localContext.Get("/school/:schoolId/categories-enhanced", h.GetEnhancedLocalCategories)

	// Student Context Analytics (FR 2.2)
	analytics := group.Group("/analytics")
	analytics.Get("/school/:schoolId/surveys/:surveyId/aggregated", h.GetSurveyAnalyticsAggregated)
	analytics.Get("/school/:schoolId/student-profile", h.GetStudentProfileAnalysis)
	analytics.Get("/school/:schoolId/statistical", h.GetStatisticalAnalysis)
	analytics.Get("/school/:schoolId/action-plans", h.GenerateActionPlanRecommendations)

	// School Data Integration (FR 2.3)
	schoolData := group.Group("/school-data")
	schoolData.Get("/:schoolId/swot", h.GetSchoolDataForSWOT)
	schoolData.Get("/:schoolId/digital-readiness", h.GetDigitalReadinessAssessment)
	schoolData.Get("/:schoolId/sarpras-prioritization", h.GetSarprasPrioritization)

	// FASE 5: Analysis Tool Enhancement Routes

	// SWOT Builder Enhancements (FR 3.1)
	swot.Get("/sessions/:sessionId/analytics", h.GetSWOTAnalyticsAggregation)
	swot.Post("/map-data", h.MapDataToSWOTItem)
	swot.Get("/school/:schoolId/data-sources", h.GetAvailableDataSourceTypes)
	swot.Get("/sessions/:sessionId/export", h.ExportSWOTAnalysis)

	// Root Cause Analyzer Enhancements (FR 3.2)
	rootCause.Post("/5-whys", h.Perform5WhysAnalysis)
	rootCause.Post("/link-rapor-metric", h.LinkRaporMetricToRootCause)
	rootCause.Get("/:rootCauseId/suggestions", h.GetRootCauseSuggestions)
	rootCause.Get("/:rootCauseId/export", h.ExportRootCauseAnalysis)

	// Fishbone Diagram Enhancements (FR 3.3)
	fishbone.Get("/diagrams/:diagramId/analytics", h.GetFishboneAnalytics)
	fishbone.Get("/diagrams/:diagramId/validate", h.ValidateFishboneStructure)
	fishbone.Get("/categories", h.GetFishboneCategories)
	fishbone.Get("/diagrams/:diagramId/export", h.ExportFishboneDiagram)

	// Fishbone Template Routes (T-5.3.14)
	fishboneTemplates := group.Group("/fishbone-templates")
	fishboneTemplates.Post("/", h.CreateFishboneTemplate)
	fishboneTemplates.Get("/:id", h.GetFishboneTemplateByID)
	fishboneTemplates.Get("/public", h.GetPublicFishboneTemplates)
	fishboneTemplates.Get("/school/:schoolId", h.GetFishboneTemplatesBySchool)
	fishboneTemplates.Put("/:id", h.UpdateFishboneTemplate)
	fishboneTemplates.Delete("/:id", h.DeleteFishboneTemplate)
	fishboneTemplates.Post("/:id/increment-usage", h.IncrementFishboneTemplateUsage)
	fishbone.Post("/fishbone-templates/:templateId/apply/:diagramId", h.ApplyFishboneTemplate)

	// FASE 6: KSP Enhanced Generation Routes

	// Document Compilation Routes (FR 4.1.1)
	documentCompilation := group.Group("/document-compilation")
	documentCompilation.Post("/compile", h.CompileDocumentWithAnalysis)
	documentCompilation.Get("/snapshot/:integrationId", h.GenerateAnalysisSnapshot)

	// KSP Analysis Template Routes (FR 4.1.2)
	kspTemplatesGroup := group.Group("/ksp-templates")
	kspTemplatesGroup.Post("/", h.CreateKSPAnalysisTemplate)
	kspTemplatesGroup.Get("/:id", h.GetKSPAnalysisTemplateByID)
	kspTemplatesGroup.Get("/public", h.GetPublicKSPAnalysisTemplates)
	kspTemplatesGroup.Get("/school/:schoolId", h.GetKSPAnalysisTemplatesBySchool)
	kspTemplatesGroup.Put("/:id", h.UpdateKSPAnalysisTemplate)
	kspTemplatesGroup.Delete("/:id", h.DeleteKSPAnalysisTemplate)
	kspTemplatesGroup.Post("/:id/increment-usage", h.IncrementTemplateUsage)

	// KSP Analysis Integration Routes (FR 4.1.6)
	kspIntegrationGroup := group.Group("/ksp-integration")
	kspIntegrationGroup.Post("/", h.CreateKSPAnalysisIntegration)
	kspIntegrationGroup.Get("/:id", h.GetKSPAnalysisIntegrationByID)
	kspIntegrationGroup.Get("/document/:documentId", h.GetKSPAnalysisIntegrationsByDocument)
	kspIntegrationGroup.Put("/:id", h.UpdateKSPAnalysisIntegration)
	kspIntegrationGroup.Delete("/:id", h.DeleteKSPAnalysisIntegration)
	kspIntegrationGroup.Post("/:id/approve", h.ApproveKSPAnalysisIntegration)
	kspIntegrationGroup.Post("/:id/recommendations", h.CreateKSPAnalysisRecommendation)
	kspIntegrationGroup.Get("/:id/recommendations", h.GetKSPAnalysisRecommendations)
	kspIntegrationGroup.Put("/recommendations/:id", h.UpdateKSPAnalysisRecommendation)
	kspIntegrationGroup.Delete("/recommendations/:id", h.DeleteKSPAnalysisRecommendation)

	// Chart Generation Routes (FR 4.1.3)
	charts := group.Group("/charts")
	charts.Post("/generate", h.GenerateChartsFromAnalysis)
	charts.Post("/swot", h.GenerateSWOTChart)
	charts.Post("/root-cause", h.GenerateRootCauseChart)
	charts.Post("/fishbone", h.GenerateFishboneChart)
	charts.Post("/student-needs", h.GenerateStudentNeedsChart)

	// AI Platform Integration Routes (FR 4.1.4)
	ai := group.Group("/ai")
	ai.Post("/generate-content", h.GenerateContentWithAI)
	ai.Post("/generate-recommendations", h.GenerateRecommendationsWithAI)
	ai.Get("/config", h.GetAIIntegrationConfig)
	ai.Put("/config", h.UpdateAIIntegrationConfig)

	// Version History Routes (FR 4.1.5)
	versionHistory := group.Group("/version-history")
	versionHistory.Post("/", h.CreateAnalysisVersionHistory)
	versionHistory.Get("/analysis/:analysisId", h.GetAnalysisVersionHistory)
	versionHistory.Get("/:versionId", h.GetAnalysisVersionByID)
	versionHistory.Get("/compare/:analysisId", h.CompareAnalysisVersions)
	versionHistory.Post("/restore", h.RestoreAnalysisVersion)

	// Extended Review and Approval Workflow Routes (FR 4.1.13)
	approvalWorkflows := group.Group("/approval-workflows")
	approvalWorkflows.Post("/", h.CreateApprovalWorkflow)
	approvalWorkflows.Get("/:workflowId", h.GetApprovalWorkflowByID)
	approvalWorkflows.Get("/school/:schoolId", h.GetApprovalWorkflowsBySchool)
	approvalWorkflows.Put("/:workflowId", h.UpdateApprovalWorkflow)
	approvalWorkflows.Delete("/:workflowId", h.DeleteApprovalWorkflow)

	approvals := group.Group("/approvals")
	approvals.Post("/submit/:documentId", h.SubmitForApproval)
	approvals.Post("/process", h.ProcessApproval)
	approvals.Get("/status/:documentId", h.GetDocumentApprovalStatus)
	approvals.Post("/assign", h.AssignWorkflowStep)
	approvals.Get("/pending", h.GetPendingApprovals)
	approvals.Post("/notifications", h.SendApprovalNotification)
	approvals.Get("/notifications", h.GetApprovalNotifications)
}
