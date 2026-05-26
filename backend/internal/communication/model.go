package communication

import (
	"time"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// Announcement Types
const (
	AnnouncementTypeGeneral   = "GENERAL"
	AnnouncementTypeAcademic  = "ACADEMIC"
	AnnouncementTypeEvent     = "EVENT"
	AnnouncementTypeEmergency = "EMERGENCY"
	AnnouncementTypeHoliday   = "HOLIDAY"
)

// Announcement Priority
const (
	AnnouncementPriorityLow    = "LOW"
	AnnouncementPriorityMedium = "MEDIUM"
	AnnouncementPriorityHigh   = "HIGH"
	AnnouncementPriorityUrgent = "URGENT"
)

// Message Status
const (
	MessageStatusDraft     = "DRAFT"
	MessageStatusSent      = "SENT"
	MessageStatusDelivered = "DELIVERED"
	MessageStatusRead      = "READ"
	MessageStatusArchived  = "ARCHIVED"
)

// Notification Types
const (
	NotificationTypeAnnouncement = "ANNOUNCEMENT"
	NotificationTypeMessage      = "MESSAGE"
	NotificationTypeReminder     = "REMINDER"
	NotificationTypeAlert        = "ALERT"
	NotificationTypeSystem       = "SYSTEM"
)

// Notification Status
const (
	NotificationStatusPending   = "PENDING"
	NotificationStatusSent      = "SENT"
	NotificationStatusDelivered = "DELIVERED"
	NotificationStatusRead      = "READ"
	NotificationStatusDismissed = "DISMISSED"
)

// Announcement represents school announcements
type Announcement struct {
	ID               uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Title            string    `gorm:"type:varchar(200);not null" json:"title"`
	Content          string    `gorm:"type:text;not null" json:"content"`
	AnnouncementType string    `gorm:"type:varchar(20);not null" json:"announcement_type"`
	Priority         string    `gorm:"type:varchar(20);not null" json:"priority"`
	TargetAudience   string    `gorm:"type:varchar(50)" json:"target_audience"` // ALL, TEACHERS, STUDENTS, PARENTS, SPECIFIC_CLASS
	TargetIDs        string    `gorm:"type:text" json:"target_ids"`             // JSON array of target user/class IDs
	PublishDate      time.Time `gorm:"type:date;not null" json:"publish_date"`
	ExpiryDate       time.Time `gorm:"type:date" json:"expiry_date"`
	CreatedBy        uuid.UUID `gorm:"type:uuid;not null" json:"created_by"`
	IsPublished      bool      `gorm:"default:false" json:"is_published"`
	IsFeatured       bool      `gorm:"default:false" json:"is_featured"`
	AttachmentURL    string    `gorm:"type:varchar(500)" json:"attachment_url"`
	AttachmentName   string    `gorm:"type:varchar(255)" json:"attachment_name"`

	common.Auditable
}

func (Announcement) TableName() string {
	return "announcements"
}

// Message represents direct messages between users (teacher-parent, teacher-student, etc.)
type Message struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SenderID       uuid.UUID `gorm:"type:uuid;not null;index" json:"sender_id"`
	ReceiverID     uuid.UUID `gorm:"type:uuid;not null;index" json:"receiver_id"`
	Subject        string    `gorm:"type:varchar(200);not null" json:"subject"`
	Body           string    `gorm:"type:text;not null" json:"body"`
	MessageType    string    `gorm:"type:varchar(20);not null" json:"message_type"` // DIRECT, GROUP, BROADCAST
	Status         string    `gorm:"type:varchar(20);not null;default:DRAFT" json:"status"`
	SentAt         time.Time `gorm:"type:timestamp" json:"sent_at"`
	ReadAt         time.Time `gorm:"type:timestamp" json:"read_at"`
	ParentID       uuid.UUID `gorm:"type:uuid;index" json:"parent_id"` // For message threads
	AttachmentURL  string    `gorm:"type:varchar(500)" json:"attachment_url"`
	AttachmentName string    `gorm:"type:varchar(255)" json:"attachment_name"`

	common.Auditable
}

func (Message) TableName() string {
	return "messages"
}

// Notification represents system notifications for users
type Notification struct {
	ID         uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	UserID     uuid.UUID `gorm:"type:uuid;not null;index" json:"user_id"`
	Type       string    `gorm:"type:varchar(20);not null" json:"type"`
	Title      string    `gorm:"type:varchar(200);not null" json:"title"`
	Body       string    `gorm:"type:text;not null" json:"body"`
	Data       string    `gorm:"type:jsonb" json:"data"` // Additional notification data in JSON
	Status     string    `gorm:"type:varchar(20);not null;default:PENDING" json:"status"`
	Priority   string    `gorm:"type:varchar(20);default:MEDIUM" json:"priority"`
	ActionURL  string    `gorm:"type:varchar(500)" json:"action_url"` // URL to redirect when clicked
	ActionText string    `gorm:"type:varchar(50)" json:"action_text"` // Button text for action
	SentAt     time.Time `gorm:"type:timestamp" json:"sent_at"`
	ReadAt     time.Time `gorm:"type:timestamp" json:"read_at"`
	ExpiresAt  time.Time `gorm:"type:timestamp" json:"expires_at"`
	SourceID   uuid.UUID `gorm:"type:uuid" json:"source_id"`          // ID of related entity (announcement_id, message_id, etc.)
	SourceType string    `gorm:"type:varchar(20)" json:"source_type"` // Type of source entity

	common.Auditable
}

func (Notification) TableName() string {
	return "notifications"
}

// MessageReadReceipt represents read receipts for messages
type MessageReadReceipt struct {
	ID        uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	MessageID uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_message_user" json:"message_id"`
	UserID    uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_message_user" json:"user_id"`
	ReadAt    time.Time `gorm:"type:timestamp;not null" json:"read_at"`

	common.Auditable
}

func (MessageReadReceipt) TableName() string {
	return "message_read_receipts"
}

// GetAnnouncementTypeDescription returns Indonesian description of announcement type
func GetAnnouncementTypeDescription(announcementType string) string {
	descriptions := map[string]string{
		AnnouncementTypeGeneral:   "Umum",
		AnnouncementTypeAcademic:  "Akademik",
		AnnouncementTypeEvent:     "Kegiatan",
		AnnouncementTypeEmergency: "Darurat",
		AnnouncementTypeHoliday:   "Libur",
	}
	return descriptions[announcementType]
}

// GetPriorityDescription returns Indonesian description of priority
func GetPriorityDescription(priority string) string {
	descriptions := map[string]string{
		AnnouncementPriorityLow:    "Rendah",
		AnnouncementPriorityMedium: "Sedang",
		AnnouncementPriorityHigh:   "Tinggi",
		AnnouncementPriorityUrgent: "Segera",
	}
	return descriptions[priority]
}

// GetMessageStatusDescription returns Indonesian description of message status
func GetMessageStatusDescription(status string) string {
	descriptions := map[string]string{
		MessageStatusDraft:     "Draft",
		MessageStatusSent:      "Terkirim",
		MessageStatusDelivered: "Diterima",
		MessageStatusRead:      "Dibaca",
		MessageStatusArchived:  "Diarsipkan",
	}
	return descriptions[status]
}

// GetNotificationTypeDescription returns Indonesian description of notification type
func GetNotificationTypeDescription(notificationType string) string {
	descriptions := map[string]string{
		NotificationTypeAnnouncement: "Pengumuman",
		NotificationTypeMessage:      "Pesan",
		NotificationTypeReminder:     "Pengingat",
		NotificationTypeAlert:        "Peringatan",
		NotificationTypeSystem:       "Sistem",
	}
	return descriptions[notificationType]
}

// IsValidAnnouncementType validates announcement type
func IsValidAnnouncementType(announcementType string) bool {
	validTypes := map[string]bool{
		AnnouncementTypeGeneral:   true,
		AnnouncementTypeAcademic:  true,
		AnnouncementTypeEvent:     true,
		AnnouncementTypeEmergency: true,
		AnnouncementTypeHoliday:   true,
	}
	return validTypes[announcementType]
}

// IsValidPriority validates priority
func IsValidPriority(priority string) bool {
	validPriorities := map[string]bool{
		AnnouncementPriorityLow:    true,
		AnnouncementPriorityMedium: true,
		AnnouncementPriorityHigh:   true,
		AnnouncementPriorityUrgent: true,
	}
	return validPriorities[priority]
}
