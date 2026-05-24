package peer_assessment

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewPeerAssessmentRepository(db)
	service := NewPeerAssessmentService(repo)
	handler := NewPeerAssessmentHandler(service)

	registerPeerAssessmentRoutes(group, handler)
}

func registerPeerAssessmentRoutes(router fiber.Router, handler *PeerAssessmentHandler) {
	// PeerAssessmentTemplate routes
	templates := router.Group("/peer-assessment-templates")
	{
		templates.Get("", handler.GetAllTemplates)
		templates.Get("/active", handler.GetActiveTemplates)
		templates.Get("/summary", handler.GetPeerAssessmentSummary)
		templates.Get("/:id", handler.GetTemplateByID)
		templates.Get("/type/:type", handler.GetTemplatesByType)
		templates.Get("/phase/:phase", handler.GetTemplatesByPhase)
		templates.Get("/subject/:subjectId", handler.GetTemplatesBySubject)
		templates.Post("", handler.CreateTemplate)
		templates.Put("/:id", handler.UpdateTemplate)
		templates.Delete("/:id", handler.DeleteTemplate)
	}

	// SelfAssessment routes
	selfAssessments := router.Group("/self-assessments")
	{
		selfAssessments.Get("", handler.GetAllSelfAssessments)
		selfAssessments.Get("/:id", handler.GetSelfAssessmentByID)
		selfAssessments.Post("", handler.CreateSelfAssessment)
		selfAssessments.Put("/:id", handler.UpdateSelfAssessment)
		selfAssessments.Delete("/:id", handler.DeleteSelfAssessment)
	}

	// Student-specific self assessment routes
	students := router.Group("/students/:studentId")
	{
		students.Get("/self-assessments", handler.GetSelfAssessmentsByStudent)
	}

	// Template-specific self assessment routes
	templateSelfAssessments := router.Group("/peer-assessment-templates/:templateId")
	{
		templateSelfAssessments.Get("/self-assessments", handler.GetSelfAssessmentsByTemplate)
	}

	// PeerAssessment routes
	peerAssessments := router.Group("/peer-assessments")
	{
		peerAssessments.Get("", handler.GetAllPeerAssessments)
		peerAssessments.Get("/pending", handler.GetPendingPeerReviews)
		peerAssessments.Get("/:id", handler.GetPeerAssessmentByID)
		peerAssessments.Post("", handler.CreatePeerAssessment)
		peerAssessments.Put("/:id", handler.UpdatePeerAssessment)
		peerAssessments.Delete("/:id", handler.DeletePeerAssessment)
	}

	// Assessor-specific peer assessment routes
	assessors := router.Group("/students/:assessorId")
	{
		assessors.Get("/peer-assessments-given", handler.GetPeerAssessmentsByAssessor)
	}

	// Assessed-specific peer assessment routes
	assessed := router.Group("/students/:assessedId")
	{
		assessed.Get("/peer-assessments-received", handler.GetPeerAssessmentsByAssessed)
	}

	// Template-specific peer assessment routes
	templatePeerAssessments := router.Group("/peer-assessment-templates/:templateId")
	{
		templatePeerAssessments.Get("/peer-assessments", handler.GetPeerAssessmentsByTemplate)
	}

	// GroupAssessment routes
	groupAssessments := router.Group("/group-assessments")
	{
		groupAssessments.Get("", handler.GetAllGroupAssessments)
		groupAssessments.Get("/:id", handler.GetGroupAssessmentByID)
		groupAssessments.Post("", handler.CreateGroupAssessment)
		groupAssessments.Put("/:id", handler.UpdateGroupAssessment)
		groupAssessments.Delete("/:id", handler.DeleteGroupAssessment)
	}

	// Group-specific group assessment routes
	groups := router.Group("/groups/:groupId")
	{
		groups.Get("/assessments", handler.GetGroupAssessmentsByGroup)
	}

	// Template-specific group assessment routes
	templateGroupAssessments := router.Group("/peer-assessment-templates/:templateId")
	{
		templateGroupAssessments.Get("/group-assessments", handler.GetGroupAssessmentsByTemplate)
	}

	// GroupAssessmentMember routes
	groupAssessmentMembers := router.Group("/group-assessment-members")
	{
		groupAssessmentMembers.Get("", handler.GetAllGroupAssessmentMembers)
		groupAssessmentMembers.Get("/:id", handler.GetGroupAssessmentMemberByID)
		groupAssessmentMembers.Post("", handler.CreateGroupAssessmentMember)
		groupAssessmentMembers.Put("/:id", handler.UpdateGroupAssessmentMember)
		groupAssessmentMembers.Delete("/:id", handler.DeleteGroupAssessmentMember)
	}

	// Group assessment-specific member routes
	groupAssessmentMembersGroup := router.Group("/group-assessments/:groupAssessmentId")
	{
		groupAssessmentMembersGroup.Get("/members", handler.GetGroupAssessmentMembersByGroupAssessment)
	}

	// Student-specific group assessment member routes
	studentGroupMembers := router.Group("/students/:studentId")
	{
		studentGroupMembers.Get("/group-assessment-memberships", handler.GetGroupAssessmentMembersByStudent)
	}

	// PeerAssessmentGuideline routes
	guidelines := router.Group("/peer-assessment-guidelines")
	{
		guidelines.Get("", handler.GetAllGuidelines)
		guidelines.Get("/active", handler.GetActiveGuidelines)
		guidelines.Get("/:id", handler.GetGuidelineByID)
		guidelines.Get("/phase/:phase", handler.GetGuidelinesByPhase)
		guidelines.Get("/category/:category", handler.GetGuidelinesByCategory)
		guidelines.Post("", handler.CreateGuideline)
		guidelines.Put("/:id", handler.UpdateGuideline)
		guidelines.Delete("/:id", handler.DeleteGuideline)
	}
}
