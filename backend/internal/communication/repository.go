package communication

import (
	"fmt"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Repository interface {
	// Announcement operations
	CreateAnnouncement(announcement *Announcement) error
	GetAnnouncementByID(id uuid.UUID) (*Announcement, error)
	GetAnnouncements(filter map[string]interface{}) ([]Announcement, error)
	UpdateAnnouncement(announcement *Announcement) error
	DeleteAnnouncement(id uuid.UUID) error
	GetPublishedAnnouncements() ([]Announcement, error)

	// Message operations
	CreateMessage(message *Message) error
	GetMessageByID(id uuid.UUID) (*Message, error)
	GetMessages(filter map[string]interface{}) ([]Message, error)
	UpdateMessage(message *Message) error
	DeleteMessage(id uuid.UUID) error
	GetUserMessages(userID uuid.UUID, userType string) ([]Message, error)
	GetConversation(user1ID, user2ID uuid.UUID) ([]Message, error)

	// Notification operations
	CreateNotification(notification *Notification) error
	GetNotificationByID(id uuid.UUID) (*Notification, error)
	GetNotifications(filter map[string]interface{}) ([]Notification, error)
	UpdateNotification(notification *Notification) error
	DeleteNotification(id uuid.UUID) error
	GetUserNotifications(userID uuid.UUID) ([]Notification, error)
	MarkNotificationAsRead(id uuid.UUID) error
	MarkAllNotificationsAsRead(userID uuid.UUID) error

	// MessageReadReceipt operations
	CreateReadReceipt(receipt *MessageReadReceipt) error
	GetMessageReadReceipts(messageID uuid.UUID) ([]MessageReadReceipt, error)
	GetUserReadReceipts(userID uuid.UUID) ([]MessageReadReceipt, error)

	// Analytics operations
	GetCommunicationAnalytics(request CommunicationAnalyticsRequest) (*CommunicationAnalyticsResponse, error)
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

// Announcement operations
func (r *repository) CreateAnnouncement(announcement *Announcement) error {
	return r.db.Create(announcement).Error
}

func (r *repository) GetAnnouncementByID(id uuid.UUID) (*Announcement, error) {
	var announcement Announcement
	err := r.db.Where("id = ? AND deleted_at IS NULL", id).First(&announcement).Error
	if err != nil {
		return nil, err
	}
	return &announcement, nil
}

func (r *repository) GetAnnouncements(filter map[string]interface{}) ([]Announcement, error) {
	var announcements []Announcement
	query := r.db.Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Order("publish_date DESC, created_at DESC").Find(&announcements).Error
	return announcements, err
}

func (r *repository) UpdateAnnouncement(announcement *Announcement) error {
	return r.db.Save(announcement).Error
}

func (r *repository) DeleteAnnouncement(id uuid.UUID) error {
	return r.db.Model(&Announcement{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *repository) GetPublishedAnnouncements() ([]Announcement, error) {
	var announcements []Announcement
	err := r.db.Where("is_published = true AND deleted_at IS NULL AND (expiry_date IS NULL OR expiry_date >= CURRENT_DATE)").Order("publish_date DESC, created_at DESC").Find(&announcements).Error
	return announcements, err
}

// Message operations
func (r *repository) CreateMessage(message *Message) error {
	return r.db.Create(message).Error
}

func (r *repository) GetMessageByID(id uuid.UUID) (*Message, error) {
	var message Message
	err := r.db.Where("id = ? AND deleted_at IS NULL", id).First(&message).Error
	if err != nil {
		return nil, err
	}
	return &message, nil
}

func (r *repository) GetMessages(filter map[string]interface{}) ([]Message, error) {
	var messages []Message
	query := r.db.Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Order("sent_at DESC, created_at DESC").Find(&messages).Error
	return messages, err
}

func (r *repository) UpdateMessage(message *Message) error {
	return r.db.Save(message).Error
}

func (r *repository) DeleteMessage(id uuid.UUID) error {
	return r.db.Model(&Message{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *repository) GetUserMessages(userID uuid.UUID, userType string) ([]Message, error) {
	var messages []Message
	query := r.db.Preload("Sender").Preload("Receiver").Where("deleted_at IS NULL")

	if userType == "sender" {
		query = query.Where("sender_id = ?", userID)
	} else {
		query = query.Where("receiver_id = ?", userID)
	}

	err := query.Order("sent_at DESC, created_at DESC").Find(&messages).Error
	return messages, err
}

func (r *repository) GetConversation(user1ID, user2ID uuid.UUID) ([]Message, error) {
	var messages []Message
	err := r.db.Preload("Sender").Preload("Receiver").Where("(sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?) AND deleted_at IS NULL", user1ID, user2ID, user2ID, user1ID).Order("sent_at ASC, created_at ASC").Find(&messages).Error
	return messages, err
}

// Notification operations
func (r *repository) CreateNotification(notification *Notification) error {
	return r.db.Create(notification).Error
}

func (r *repository) GetNotificationByID(id uuid.UUID) (*Notification, error) {
	var notification Notification
	err := r.db.Preload("User").Where("id = ? AND deleted_at IS NULL", id).First(&notification).Error
	if err != nil {
		return nil, err
	}
	return &notification, nil
}

func (r *repository) GetNotifications(filter map[string]interface{}) ([]Notification, error) {
	var notifications []Notification
	query := r.db.Preload("User").Where("deleted_at IS NULL")

	for key, value := range filter {
		query = query.Where(fmt.Sprintf("%s = ?", key), value)
	}

	err := query.Order("sent_at DESC, created_at DESC").Find(&notifications).Error
	return notifications, err
}

func (r *repository) UpdateNotification(notification *Notification) error {
	return r.db.Save(notification).Error
}

func (r *repository) DeleteNotification(id uuid.UUID) error {
	return r.db.Model(&Notification{}).Where("id = ?", id).Update("deleted_at", gorm.Expr("NOW()")).Error
}

func (r *repository) GetUserNotifications(userID uuid.UUID) ([]Notification, error) {
	var notifications []Notification
	err := r.db.Preload("User").Where("user_id = ? AND deleted_at IS NULL AND (expires_at IS NULL OR expires_at >= CURRENT_TIMESTAMP)", userID).Order("sent_at DESC, created_at DESC").Find(&notifications).Error
	return notifications, err
}

func (r *repository) MarkNotificationAsRead(id uuid.UUID) error {
	return r.db.Model(&Notification{}).Where("id = ?", id).Updates(map[string]interface{}{
		"status":  "READ",
		"read_at": gorm.Expr("NOW()"),
	}).Error
}

func (r *repository) MarkAllNotificationsAsRead(userID uuid.UUID) error {
	return r.db.Model(&Notification{}).Where("user_id = ? AND status != 'READ' AND deleted_at IS NULL", userID).Updates(map[string]interface{}{
		"status":  "READ",
		"read_at": gorm.Expr("NOW()"),
	}).Error
}

// MessageReadReceipt operations
func (r *repository) CreateReadReceipt(receipt *MessageReadReceipt) error {
	return r.db.Create(receipt).Error
}

func (r *repository) GetMessageReadReceipts(messageID uuid.UUID) ([]MessageReadReceipt, error) {
	var receipts []MessageReadReceipt
	err := r.db.Where("message_id = ? AND deleted_at IS NULL", messageID).Order("read_at DESC").Find(&receipts).Error
	return receipts, err
}

func (r *repository) GetUserReadReceipts(userID uuid.UUID) ([]MessageReadReceipt, error) {
	var receipts []MessageReadReceipt
	err := r.db.Where("user_id = ? AND deleted_at IS NULL", userID).Order("read_at DESC").Find(&receipts).Error
	return receipts, err
}

// Analytics operations
func (r *repository) GetCommunicationAnalytics(request CommunicationAnalyticsRequest) (*CommunicationAnalyticsResponse, error) {
	response := &CommunicationAnalyticsResponse{}

	// Base queries with filters
	announcementQuery := r.db.Model(&Announcement{}).Where("deleted_at IS NULL")
	messageQuery := r.db.Model(&Message{}).Where("deleted_at IS NULL")
	notificationQuery := r.db.Model(&Notification{}).Where("deleted_at IS NULL")

	// Apply date filters
	if request.StartDate != nil {
		announcementQuery = announcementQuery.Where("created_at >= ?", *request.StartDate)
		messageQuery = messageQuery.Where("created_at >= ?", *request.StartDate)
		notificationQuery = notificationQuery.Where("created_at >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		announcementQuery = announcementQuery.Where("created_at <= ?", *request.EndDate)
		messageQuery = messageQuery.Where("created_at <= ?", *request.EndDate)
		notificationQuery = notificationQuery.Where("created_at <= ?", *request.EndDate)
	}

	// Apply user filter
	if request.UserID != nil {
		messageQuery = messageQuery.Where("(sender_id = ? OR receiver_id = ?)", *request.UserID, *request.UserID)
		notificationQuery = notificationQuery.Where("user_id = ?", *request.UserID)
	}

	// Get totals
	announcementQuery.Count(&response.TotalAnnouncements)
	messageQuery.Count(&response.TotalMessages)
	notificationQuery.Count(&response.TotalNotifications)

	// Get published announcements
	var publishedCount int64
	publishedAnnouncementQuery := r.db.Model(&Announcement{}).Where("is_published = true AND deleted_at IS NULL")
	if request.StartDate != nil {
		publishedAnnouncementQuery = publishedAnnouncementQuery.Where("created_at >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		publishedAnnouncementQuery = publishedAnnouncementQuery.Where("created_at <= ?", *request.EndDate)
	}
	publishedAnnouncementQuery.Count(&publishedCount)
	response.PublishedAnnouncements = publishedCount

	// Get sent messages
	var sentCount int64
	sentMessageQuery := r.db.Model(&Message{}).Where("status = 'SENT' AND deleted_at IS NULL")
	if request.StartDate != nil {
		sentMessageQuery = sentMessageQuery.Where("created_at >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		sentMessageQuery = sentMessageQuery.Where("created_at <= ?", *request.EndDate)
	}
	if request.UserID != nil {
		sentMessageQuery = sentMessageQuery.Where("(sender_id = ? OR receiver_id = ?)", *request.UserID, *request.UserID)
	}
	sentMessageQuery.Count(&sentCount)
	response.SentMessages = sentCount

	// Get read messages
	var readCount int64
	readMessageQuery := r.db.Model(&Message{}).Where("status = 'READ' AND deleted_at IS NULL")
	if request.StartDate != nil {
		readMessageQuery = readMessageQuery.Where("created_at >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		readMessageQuery = readMessageQuery.Where("created_at <= ?", *request.EndDate)
	}
	if request.UserID != nil {
		readMessageQuery = readMessageQuery.Where("(sender_id = ? OR receiver_id = ?)", *request.UserID, *request.UserID)
	}
	readMessageQuery.Count(&readCount)
	response.ReadMessages = readCount

	// Get read notifications
	var readNotificationCount int64
	readNotificationQuery := r.db.Model(&Notification{}).Where("status = 'READ' AND deleted_at IS NULL")
	if request.StartDate != nil {
		readNotificationQuery = readNotificationQuery.Where("created_at >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		readNotificationQuery = readNotificationQuery.Where("created_at <= ?", *request.EndDate)
	}
	if request.UserID != nil {
		readNotificationQuery = readNotificationQuery.Where("user_id = ?", *request.UserID)
	}
	readNotificationQuery.Count(&readNotificationCount)
	response.ReadNotifications = readNotificationCount

	// Get statistics by announcement type
	typeStatsQuery := r.db.Model(&Announcement{}).Select("announcement_type, COUNT(*) as count").Where("deleted_at IS NULL")
	if request.StartDate != nil {
		typeStatsQuery = typeStatsQuery.Where("created_at >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		typeStatsQuery = typeStatsQuery.Where("created_at <= ?", *request.EndDate)
	}
	typeStatsQuery.Group("announcement_type")

	typeStats := []struct {
		AnnouncementType string
		Count            int64
	}{}
	typeStatsQuery.Scan(&typeStats)

	totalAnnouncements := response.TotalAnnouncements
	for _, stat := range typeStats {
		percentage := float64(0)
		if totalAnnouncements > 0 {
			percentage = float64(stat.Count) / float64(totalAnnouncements) * 100
		}
		response.ByAnnouncementType = append(response.ByAnnouncementType, AnnouncementTypeStats{
			Type:       stat.AnnouncementType,
			TypeName:   GetAnnouncementTypeDescription(stat.AnnouncementType),
			Count:      stat.Count,
			Percentage: percentage,
		})
	}

	// Get statistics by message type
	messageTypeStatsQuery := r.db.Model(&Message{}).Select("message_type, COUNT(*) as count").Where("deleted_at IS NULL")
	if request.StartDate != nil {
		messageTypeStatsQuery = messageTypeStatsQuery.Where("created_at >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		messageTypeStatsQuery = messageTypeStatsQuery.Where("created_at <= ?", *request.EndDate)
	}
	if request.UserID != nil {
		messageTypeStatsQuery = messageTypeStatsQuery.Where("(sender_id = ? OR receiver_id = ?)", *request.UserID, *request.UserID)
	}
	messageTypeStatsQuery.Group("message_type")

	messageTypeStats := []struct {
		MessageType string
		Count       int64
	}{}
	messageTypeStatsQuery.Scan(&messageTypeStats)

	totalMessages := response.TotalMessages
	for _, stat := range messageTypeStats {
		percentage := float64(0)
		if totalMessages > 0 {
			percentage = float64(stat.Count) / float64(totalMessages) * 100
		}
		response.ByMessageType = append(response.ByMessageType, MessageTypeStats{
			Type:       stat.MessageType,
			Count:      stat.Count,
			Percentage: percentage,
		})
	}

	// Get statistics by notification type
	notificationTypeStatsQuery := r.db.Model(&Notification{}).Select("type, COUNT(*) as count").Where("deleted_at IS NULL")
	if request.StartDate != nil {
		notificationTypeStatsQuery = notificationTypeStatsQuery.Where("created_at >= ?", *request.StartDate)
	}
	if request.EndDate != nil {
		notificationTypeStatsQuery = notificationTypeStatsQuery.Where("created_at <= ?", *request.EndDate)
	}
	if request.UserID != nil {
		notificationTypeStatsQuery = notificationTypeStatsQuery.Where("user_id = ?", *request.UserID)
	}
	notificationTypeStatsQuery.Group("type")

	notificationTypeStats := []struct {
		Type  string
		Count int64
	}{}
	notificationTypeStatsQuery.Scan(&notificationTypeStats)

	totalNotifications := response.TotalNotifications
	for _, stat := range notificationTypeStats {
		percentage := float64(0)
		if totalNotifications > 0 {
			percentage = float64(stat.Count) / float64(totalNotifications) * 100
		}
		response.ByNotificationType = append(response.ByNotificationType, NotificationTypeStats{
			Type:       stat.Type,
			TypeName:   GetNotificationTypeDescription(stat.Type),
			Count:      stat.Count,
			Percentage: percentage,
		})
	}

	return response, nil
}
