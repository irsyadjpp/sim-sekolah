package parent_partnership

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewParentPartnershipRepository(db)
	service := NewParentPartnershipService(repo)
	handler := NewParentPartnershipHandler(service)

	registerParentPartnershipRoutes(group, handler)
}

func registerParentPartnershipRoutes(router fiber.Router, handler *ParentPartnershipHandler) {
	// ParentPartnership routes
	partnerships := router.Group("/parent-partnerships")
	{
		partnerships.Get("", handler.GetAll)
		partnerships.Get("/summary", handler.GetPartnershipSummary)
		partnerships.Get("/:id", handler.GetByID)
		partnerships.Post("", handler.Create)
		partnerships.Put("/:id", handler.Update)
		partnerships.Delete("/:id", handler.Delete)
	}

	// Student-specific partnership routes
	students := router.Group("/students/:studentId")
	{
		students.Get("/parent-partnerships", handler.GetByStudentID)
		students.Get("/parent-partnerships/active", handler.GetActiveByStudentID)
	}

	// ParentCommunication routes
	communications := router.Group("/parent-communications")
	{
		communications.Get("", handler.GetAllCommunications)
		communications.Get("/pending-follow-ups", handler.GetPendingFollowUps)
		communications.Get("/:id", handler.GetCommunicationByID)
		communications.Post("", handler.CreateCommunication)
		communications.Put("/:id", handler.UpdateCommunication)
		communications.Delete("/:id", handler.DeleteCommunication)
	}

	// Partnership-specific communication routes
	partnershipCommunications := router.Group("/parent-partnerships/:partnershipId")
	{
		partnershipCommunications.Get("/communications", handler.GetCommunicationsByPartnership)
	}

	// ParentMeeting routes
	meetings := router.Group("/parent-meetings")
	{
		meetings.Get("", handler.GetAllMeetings)
		meetings.Get("/scheduled", handler.GetScheduledMeetings)
		meetings.Get("/:id", handler.GetMeetingByID)
		meetings.Post("", handler.CreateMeeting)
		meetings.Put("/:id", handler.UpdateMeeting)
		meetings.Delete("/:id", handler.DeleteMeeting)
	}

	// Partnership-specific meeting routes
	partnershipMeetings := router.Group("/parent-partnerships/:partnershipId")
	{
		partnershipMeetings.Get("/meetings", handler.GetMeetingsByPartnership)
	}

	// Teacher-specific meeting routes
	teachers := router.Group("/teachers/:teacherId")
	{
		teachers.Get("/parent-meetings", handler.GetMeetingsByTeacher)
	}

	// PartnershipActivity routes
	activities := router.Group("/partnership-activities")
	{
		activities.Get("", handler.GetAllActivities)
		activities.Get("/date-range", handler.GetActivitiesByDateRange)
		activities.Get("/:id", handler.GetActivityByID)
		activities.Post("", handler.CreateActivity)
		activities.Put("/:id", handler.UpdateActivity)
		activities.Delete("/:id", handler.DeleteActivity)
	}

	// Partnership-specific activity routes
	partnershipActivities := router.Group("/parent-partnerships/:partnershipId")
	{
		partnershipActivities.Get("/activities", handler.GetActivitiesByPartnership)
	}
}
