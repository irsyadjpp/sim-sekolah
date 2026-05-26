package communication

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB) {
	group := api.Group("/api/v1")
	group.Use(middleware.Protected())

	repo := NewRepository(db)
	service := NewService(repo)
	handler := NewHandler(service)

	handler.RegisterRoutes(group)
}

func (h *Handler) RegisterRoutes(group fiber.Router) {
	// Announcement routes
	announcements := group.Group("/announcements")
	announcements.Post("/", h.CreateAnnouncement)
	announcements.Get("/:id", h.GetAnnouncementByID)
	announcements.Get("/", h.GetAnnouncements)
	announcements.Put("/:id", h.UpdateAnnouncement)
	announcements.Delete("/:id", h.DeleteAnnouncement)
	announcements.Get("/published", h.GetPublishedAnnouncements)
	announcements.Put("/:id/publish", h.PublishAnnouncement)

	// Message routes
	messages := group.Group("/messages")
	messages.Post("/", h.CreateMessage)
	messages.Post("/send", h.SendMessage)
	messages.Get("/:id", h.GetMessageByID)
	messages.Get("/", h.GetMessages)
	messages.Put("/:id", h.UpdateMessage)
	messages.Delete("/:id", h.DeleteMessage)
	messages.Get("/user/:user_id", h.GetUserMessages)
	messages.Get("/conversation/:user1_id/:user2_id", h.GetConversation)

	// Notification routes
	notifications := group.Group("/notifications")
	notifications.Post("/", h.CreateNotification)
	notifications.Get("/:id", h.GetNotificationByID)
	notifications.Get("/", h.GetNotifications)
	notifications.Put("/:id", h.UpdateNotification)
	notifications.Delete("/:id", h.DeleteNotification)
	notifications.Get("/user/:user_id", h.GetUserNotifications)
	notifications.Put("/:id/read", h.MarkNotificationAsRead)
	notifications.Put("/user/:user_id/read-all", h.MarkAllNotificationsAsRead)

	// MessageReadReceipt routes
	readReceipts := group.Group("/message-read-receipts")
	readReceipts.Post("/", h.CreateReadReceipt)
	readReceipts.Get("/message/:message_id", h.GetMessageReadReceipts)
	readReceipts.Get("/user/:user_id", h.GetUserReadReceipts)

	// Analytics routes
	analytics := group.Group("/communication-analytics")
	analytics.Get("/", h.GetCommunicationAnalytics)
}
