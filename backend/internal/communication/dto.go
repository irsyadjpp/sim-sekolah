package communication

import (
	"time"

	"github.com/google/uuid"
)

// AnnouncementRequest represents request body for creating/updating announcement
type AnnouncementRequest struct {
	Title            string    `json:"title" validate:"required"`
	Content          string    `json:"content" validate:"required"`
	AnnouncementType string    `json:"announcement_type" validate:"required"`
	Priority         string    `json:"priority" validate:"required"`
	TargetAudience   string    `json:"target_audience"`
	TargetIDs        string    `json:"target_ids"`
	PublishDate      time.Time `json:"publish_date" validate:"required"`
	ExpiryDate       time.Time `json:"expiry_date"`
	AttachmentURL    string    `json:"attachment_url"`
	AttachmentName   string    `json:"attachment_name"`
	IsPublished      *bool     `json:"is_published"`
	IsFeatured       *bool     `json:"is_featured"`
}

// AnnouncementResponse represents response body for announcement
type AnnouncementResponse struct {
	ID               uuid.UUID `json:"id"`
	Title            string    `json:"title"`
	Content          string    `json:"content"`
	AnnouncementType string    `json:"announcement_type"`
	TypeName         string    `json:"type_name,omitempty"`
	Priority         string    `json:"priority"`
	PriorityName     string    `json:"priority_name,omitempty"`
	TargetAudience   string    `json:"target_audience"`
	TargetIDs        string    `json:"target_ids"`
	PublishDate      time.Time `json:"publish_date"`
	ExpiryDate       time.Time `json:"expiry_date"`
	CreatedBy        uuid.UUID `json:"created_by"`
	CreatorName      string    `json:"creator_name,omitempty"`
	IsPublished      bool      `json:"is_published"`
	IsFeatured       bool      `json:"is_featured"`
	AttachmentURL    string    `json:"attachment_url"`
	AttachmentName   string    `json:"attachment_name"`
	CreatedAt        time.Time `json:"created_at"`
	UpdatedAt        time.Time `json:"updated_at"`
}

// MessageRequest represents request body for creating/updating message
type MessageRequest struct {
	ReceiverID     uuid.UUID `json:"receiver_id" validate:"required"`
	Subject        string    `json:"subject" validate:"required"`
	Body           string    `json:"body" validate:"required"`
	MessageType    string    `json:"message_type" validate:"required"`
	Status         string    `json:"status"`
	ParentID       uuid.UUID `json:"parent_id"`
	AttachmentURL  string    `json:"attachment_url"`
	AttachmentName string    `json:"attachment_name"`
}

// MessageResponse represents response body for message
type MessageResponse struct {
	ID             uuid.UUID `json:"id"`
	SenderID       uuid.UUID `json:"sender_id"`
	SenderName     string    `json:"sender_name,omitempty"`
	ReceiverID     uuid.UUID `json:"receiver_id"`
	ReceiverName   string    `json:"receiver_name,omitempty"`
	Subject        string    `json:"subject"`
	Body           string    `json:"body"`
	MessageType    string    `json:"message_type"`
	Status         string    `json:"status"`
	StatusName     string    `json:"status_name,omitempty"`
	SentAt         time.Time `json:"sent_at"`
	ReadAt         time.Time `json:"read_at"`
	ParentID       uuid.UUID `json:"parent_id"`
	AttachmentURL  string    `json:"attachment_url"`
	AttachmentName string    `json:"attachment_name"`
	CreatedAt      time.Time `json:"created_at"`
	UpdatedAt      time.Time `json:"updated_at"`
}

// MessageThreadResponse represents a thread of messages between users
type MessageThreadResponse struct {
	ThreadID      uuid.UUID         `json:"thread_id"`
	Participants  []ParticipantInfo `json:"participants"`
	Messages      []MessageResponse `json:"messages"`
	UnreadCount   int               `json:"unread_count"`
	LastMessageAt time.Time         `json:"last_message_at"`
	LastMessage   string            `json:"last_message"`
}

// ParticipantInfo represents basic info about a message participant
type ParticipantInfo struct {
	UserID uuid.UUID `json:"user_id"`
	Name   string    `json:"name"`
	Role   string    `json:"role"`
}

// NotificationRequest represents request body for creating notification
type NotificationRequest struct {
	UserID     uuid.UUID `json:"user_id" validate:"required"`
	Type       string    `json:"type" validate:"required"`
	Title      string    `json:"title" validate:"required"`
	Body       string    `json:"body" validate:"required"`
	Data       string    `json:"data"`
	Priority   string    `json:"priority"`
	ActionURL  string    `json:"action_url"`
	ActionText string    `json:"action_text"`
	ExpiresAt  time.Time `json:"expires_at"`
	SourceID   uuid.UUID `json:"source_id"`
	SourceType string    `json:"source_type"`
}

// NotificationResponse represents response body for notification
type NotificationResponse struct {
	ID           uuid.UUID `json:"id"`
	UserID       uuid.UUID `json:"user_id"`
	UserName     string    `json:"user_name,omitempty"`
	Type         string    `json:"type"`
	TypeName     string    `json:"type_name,omitempty"`
	Title        string    `json:"title"`
	Body         string    `json:"body"`
	Data         string    `json:"data"`
	Status       string    `json:"status"`
	StatusName   string    `json:"status_name,omitempty"`
	Priority     string    `json:"priority"`
	PriorityName string    `json:"priority_name,omitempty"`
	ActionURL    string    `json:"action_url"`
	ActionText   string    `json:"action_text"`
	SentAt       time.Time `json:"sent_at"`
	ReadAt       time.Time `json:"read_at"`
	ExpiresAt    time.Time `json:"expires_at"`
	SourceID     uuid.UUID `json:"source_id"`
	SourceType   string    `json:"source_type"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

// MessageReadReceiptRequest represents request for marking message as read
type MessageReadReceiptRequest struct {
	MessageID uuid.UUID `json:"message_id" validate:"required"`
	ReadAt    time.Time `json:"read_at"`
}

// MessageReadReceiptResponse represents response for read receipt
type MessageReadReceiptResponse struct {
	ID        uuid.UUID `json:"id"`
	MessageID uuid.UUID `json:"message_id"`
	UserID    uuid.UUID `json:"user_id"`
	UserName  string    `json:"user_name,omitempty"`
	ReadAt    time.Time `json:"read_at"`
	CreatedAt time.Time `json:"created_at"`
}

// CommunicationAnalyticsRequest represents request for communication analytics
type CommunicationAnalyticsRequest struct {
	StartDate *time.Time `json:"start_date,omitempty"`
	EndDate   *time.Time `json:"end_date,omitempty"`
	UserID    *uuid.UUID `json:"user_id,omitempty"`
}

// CommunicationAnalyticsResponse represents communication analytics data
type CommunicationAnalyticsResponse struct {
	TotalAnnouncements     int64                         `json:"total_announcements"`
	TotalMessages          int64                         `json:"total_messages"`
	TotalNotifications     int64                         `json:"total_notifications"`
	PublishedAnnouncements int64                         `json:"published_announcements"`
	SentMessages           int64                         `json:"sent_messages"`
	ReadMessages           int64                         `json:"read_messages"`
	ReadNotifications      int64                         `json:"read_notifications"`
	ByAnnouncementType     []AnnouncementTypeStats       `json:"by_announcement_type"`
	ByMessageType          []MessageTypeStats            `json:"by_message_type"`
	ByNotificationType     []NotificationTypeStats       `json:"by_notification_type"`
	RecentActivity         []RecentCommunicationActivity `json:"recent_activity,omitempty"`
}

// AnnouncementTypeStats represents statistics by announcement type
type AnnouncementTypeStats struct {
	Type       string  `json:"type"`
	TypeName   string  `json:"type_name"`
	Count      int64   `json:"count"`
	Percentage float64 `json:"percentage"`
}

// MessageTypeStats represents statistics by message type
type MessageTypeStats struct {
	Type       string  `json:"type"`
	Count      int64   `json:"count"`
	Percentage float64 `json:"percentage"`
}

// NotificationTypeStats represents statistics by notification type
type NotificationTypeStats struct {
	Type       string  `json:"type"`
	TypeName   string  `json:"type_name"`
	Count      int64   `json:"count"`
	Percentage float64 `json:"percentage"`
}

// RecentCommunicationActivity represents recent communication activity
type RecentCommunicationActivity struct {
	ActivityID   uuid.UUID `json:"activity_id"`
	ActivityType string    `json:"activity_type"` // ANNOUNCEMENT, MESSAGE, NOTIFICATION
	Title        string    `json:"title"`
	TargetUser   string    `json:"target_user"`
	Timestamp    time.Time `json:"timestamp"`
	Status       string    `json:"status"`
}
