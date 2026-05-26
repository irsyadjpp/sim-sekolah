package communication

import (
	"errors"
	"fmt"
	"time"

	"github.com/google/uuid"
)

type Service interface {
	// Announcement operations
	CreateAnnouncement(request AnnouncementRequest) (*AnnouncementResponse, error)
	GetAnnouncementByID(id uuid.UUID) (*AnnouncementResponse, error)
	GetAnnouncements(filter map[string]interface{}) ([]AnnouncementResponse, error)
	UpdateAnnouncement(id uuid.UUID, request AnnouncementRequest) (*AnnouncementResponse, error)
	DeleteAnnouncement(id uuid.UUID) error
	GetPublishedAnnouncements() ([]AnnouncementResponse, error)
	PublishAnnouncement(id uuid.UUID) (*AnnouncementResponse, error)

	// Message operations
	CreateMessage(request MessageRequest) (*MessageResponse, error)
	GetMessageByID(id uuid.UUID) (*MessageResponse, error)
	GetMessages(filter map[string]interface{}) ([]MessageResponse, error)
	UpdateMessage(id uuid.UUID, request MessageRequest) (*MessageResponse, error)
	DeleteMessage(id uuid.UUID) error
	GetUserMessages(userID uuid.UUID, userType string) ([]MessageResponse, error)
	GetConversation(user1ID, user2ID uuid.UUID) ([]MessageResponse, error)
	SendMessage(request MessageRequest) (*MessageResponse, error)

	// Notification operations
	CreateNotification(request NotificationRequest) (*NotificationResponse, error)
	GetNotificationByID(id uuid.UUID) (*NotificationResponse, error)
	GetNotifications(filter map[string]interface{}) ([]NotificationResponse, error)
	UpdateNotification(id uuid.UUID, request NotificationRequest) (*NotificationResponse, error)
	DeleteNotification(id uuid.UUID) error
	GetUserNotifications(userID uuid.UUID) ([]NotificationResponse, error)
	MarkNotificationAsRead(id uuid.UUID) error
	MarkAllNotificationsAsRead(userID uuid.UUID) error
	CreateAnnouncementNotification(announcementID uuid.UUID) error

	// MessageReadReceipt operations
	CreateReadReceipt(request MessageReadReceiptRequest) (*MessageReadReceiptResponse, error)
	GetMessageReadReceipts(messageID uuid.UUID) ([]MessageReadReceiptResponse, error)
	GetUserReadReceipts(userID uuid.UUID) ([]MessageReadReceiptResponse, error)

	// Analytics operations
	GetCommunicationAnalytics(request CommunicationAnalyticsRequest) (*CommunicationAnalyticsResponse, error)
}

type service struct {
	repo Repository
}

func NewService(repo Repository) Service {
	return &service{repo: repo}
}

// Announcement operations
func (s *service) CreateAnnouncement(request AnnouncementRequest) (*AnnouncementResponse, error) {
	// Validate announcement type
	if !IsValidAnnouncementType(request.AnnouncementType) {
		return nil, errors.New("invalid announcement type")
	}

	// Validate priority
	if !IsValidPriority(request.Priority) {
		return nil, errors.New("invalid priority")
	}

	announcement := &Announcement{
		ID:               uuid.New(),
		Title:            request.Title,
		Content:          request.Content,
		AnnouncementType: request.AnnouncementType,
		Priority:         request.Priority,
		TargetAudience:   request.TargetAudience,
		TargetIDs:        request.TargetIDs,
		PublishDate:      request.PublishDate,
		ExpiryDate:       request.ExpiryDate,
		CreatedBy:        uuid.New(), // This should be set from context in real app
		AttachmentURL:    request.AttachmentURL,
		AttachmentName:   request.AttachmentName,
	}

	if request.IsPublished != nil {
		announcement.IsPublished = *request.IsPublished
	}
	if request.IsFeatured != nil {
		announcement.IsFeatured = *request.IsFeatured
	}

	err := s.repo.CreateAnnouncement(announcement)
	if err != nil {
		return nil, err
	}

	return s.modelToAnnouncementResponse(announcement), nil
}

func (s *service) GetAnnouncementByID(id uuid.UUID) (*AnnouncementResponse, error) {
	announcement, err := s.repo.GetAnnouncementByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToAnnouncementResponse(announcement), nil
}

func (s *service) GetAnnouncements(filter map[string]interface{}) ([]AnnouncementResponse, error) {
	announcements, err := s.repo.GetAnnouncements(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]AnnouncementResponse, len(announcements))
	for i, announcement := range announcements {
		responses[i] = *s.modelToAnnouncementResponse(&announcement)
	}
	return responses, nil
}

func (s *service) UpdateAnnouncement(id uuid.UUID, request AnnouncementRequest) (*AnnouncementResponse, error) {
	// Validate announcement type
	if !IsValidAnnouncementType(request.AnnouncementType) {
		return nil, errors.New("invalid announcement type")
	}

	// Validate priority
	if !IsValidPriority(request.Priority) {
		return nil, errors.New("invalid priority")
	}

	announcement, err := s.repo.GetAnnouncementByID(id)
	if err != nil {
		return nil, err
	}

	announcement.Title = request.Title
	announcement.Content = request.Content
	announcement.AnnouncementType = request.AnnouncementType
	announcement.Priority = request.Priority
	announcement.TargetAudience = request.TargetAudience
	announcement.TargetIDs = request.TargetIDs
	announcement.PublishDate = request.PublishDate
	announcement.ExpiryDate = request.ExpiryDate
	announcement.AttachmentURL = request.AttachmentURL
	announcement.AttachmentName = request.AttachmentName

	if request.IsPublished != nil {
		announcement.IsPublished = *request.IsPublished
	}
	if request.IsFeatured != nil {
		announcement.IsFeatured = *request.IsFeatured
	}

	err = s.repo.UpdateAnnouncement(announcement)
	if err != nil {
		return nil, err
	}

	return s.modelToAnnouncementResponse(announcement), nil
}

func (s *service) DeleteAnnouncement(id uuid.UUID) error {
	return s.repo.DeleteAnnouncement(id)
}

func (s *service) GetPublishedAnnouncements() ([]AnnouncementResponse, error) {
	announcements, err := s.repo.GetPublishedAnnouncements()
	if err != nil {
		return nil, err
	}

	responses := make([]AnnouncementResponse, len(announcements))
	for i, announcement := range announcements {
		responses[i] = *s.modelToAnnouncementResponse(&announcement)
	}
	return responses, nil
}

func (s *service) PublishAnnouncement(id uuid.UUID) (*AnnouncementResponse, error) {
	announcement, err := s.repo.GetAnnouncementByID(id)
	if err != nil {
		return nil, err
	}

	announcement.IsPublished = true

	err = s.repo.UpdateAnnouncement(announcement)
	if err != nil {
		return nil, err
	}

	// Create notifications for target audience
	err = s.CreateAnnouncementNotification(id)
	if err != nil {
		// Log error but don't fail the publish
		fmt.Printf("Failed to create notifications for announcement %s: %v\n", id, err)
	}

	return s.modelToAnnouncementResponse(announcement), nil
}

// Message operations
func (s *service) CreateMessage(request MessageRequest) (*MessageResponse, error) {
	message := &Message{
		ID:             uuid.New(),
		SenderID:       uuid.New(), // This should be set from context in real app
		ReceiverID:     request.ReceiverID,
		Subject:        request.Subject,
		Body:           request.Body,
		MessageType:    request.MessageType,
		Status:         request.Status,
		ParentID:       request.ParentID,
		AttachmentURL:  request.AttachmentURL,
		AttachmentName: request.AttachmentName,
	}

	if message.Status == "" {
		message.Status = MessageStatusDraft
	}

	err := s.repo.CreateMessage(message)
	if err != nil {
		return nil, err
	}

	return s.modelToMessageResponse(message), nil
}

func (s *service) GetMessageByID(id uuid.UUID) (*MessageResponse, error) {
	message, err := s.repo.GetMessageByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToMessageResponse(message), nil
}

func (s *service) GetMessages(filter map[string]interface{}) ([]MessageResponse, error) {
	messages, err := s.repo.GetMessages(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]MessageResponse, len(messages))
	for i, message := range messages {
		responses[i] = *s.modelToMessageResponse(&message)
	}
	return responses, nil
}

func (s *service) UpdateMessage(id uuid.UUID, request MessageRequest) (*MessageResponse, error) {
	message, err := s.repo.GetMessageByID(id)
	if err != nil {
		return nil, err
	}

	message.ReceiverID = request.ReceiverID
	message.Subject = request.Subject
	message.Body = request.Body
	message.MessageType = request.MessageType
	message.Status = request.Status
	message.ParentID = request.ParentID
	message.AttachmentURL = request.AttachmentURL
	message.AttachmentName = request.AttachmentName

	err = s.repo.UpdateMessage(message)
	if err != nil {
		return nil, err
	}

	return s.modelToMessageResponse(message), nil
}

func (s *service) DeleteMessage(id uuid.UUID) error {
	return s.repo.DeleteMessage(id)
}

func (s *service) GetUserMessages(userID uuid.UUID, userType string) ([]MessageResponse, error) {
	messages, err := s.repo.GetUserMessages(userID, userType)
	if err != nil {
		return nil, err
	}

	responses := make([]MessageResponse, len(messages))
	for i, message := range messages {
		responses[i] = *s.modelToMessageResponse(&message)
	}
	return responses, nil
}

func (s *service) GetConversation(user1ID, user2ID uuid.UUID) ([]MessageResponse, error) {
	messages, err := s.repo.GetConversation(user1ID, user2ID)
	if err != nil {
		return nil, err
	}

	responses := make([]MessageResponse, len(messages))
	for i, message := range messages {
		responses[i] = *s.modelToMessageResponse(&message)
	}
	return responses, nil
}

func (s *service) SendMessage(request MessageRequest) (*MessageResponse, error) {
	request.Status = MessageStatusSent
	now := time.Now()

	message := &Message{
		ID:             uuid.New(),
		SenderID:       uuid.New(), // This should be set from context in real app
		ReceiverID:     request.ReceiverID,
		Subject:        request.Subject,
		Body:           request.Body,
		MessageType:    request.MessageType,
		Status:         request.Status,
		SentAt:         now,
		ParentID:       request.ParentID,
		AttachmentURL:  request.AttachmentURL,
		AttachmentName: request.AttachmentName,
	}

	err := s.repo.CreateMessage(message)
	if err != nil {
		return nil, err
	}

	// Create notification for recipient
	notification := NotificationRequest{
		UserID:     request.ReceiverID,
		Type:       NotificationTypeMessage,
		Title:      "Pesan Baru",
		Body:       request.Subject,
		SourceID:   message.ID,
		SourceType: "MESSAGE",
		ActionURL:  "/messages/" + message.ID.String(),
		ActionText: "Lihat Pesan",
		Priority:   AnnouncementPriorityMedium,
	}

	_, err = s.CreateNotification(notification)
	if err != nil {
		fmt.Printf("Failed to create notification for message: %v\n", err)
	}

	return s.modelToMessageResponse(message), nil
}

// Notification operations
func (s *service) CreateNotification(request NotificationRequest) (*NotificationResponse, error) {
	notification := &Notification{
		ID:         uuid.New(),
		UserID:     request.UserID,
		Type:       request.Type,
		Title:      request.Title,
		Body:       request.Body,
		Data:       request.Data,
		Status:     NotificationStatusPending,
		Priority:   request.Priority,
		ActionURL:  request.ActionURL,
		ActionText: request.ActionText,
		ExpiresAt:  request.ExpiresAt,
		SourceID:   request.SourceID,
		SourceType: request.SourceType,
	}

	if notification.Priority == "" {
		notification.Priority = AnnouncementPriorityMedium
	}

	err := s.repo.CreateNotification(notification)
	if err != nil {
		return nil, err
	}

	// Mark as sent
	notification.Status = NotificationStatusSent
	notification.SentAt = time.Now()
	err = s.repo.UpdateNotification(notification)
	if err != nil {
		return nil, err
	}

	return s.modelToNotificationResponse(notification), nil
}

func (s *service) GetNotificationByID(id uuid.UUID) (*NotificationResponse, error) {
	notification, err := s.repo.GetNotificationByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToNotificationResponse(notification), nil
}

func (s *service) GetNotifications(filter map[string]interface{}) ([]NotificationResponse, error) {
	notifications, err := s.repo.GetNotifications(filter)
	if err != nil {
		return nil, err
	}

	responses := make([]NotificationResponse, len(notifications))
	for i, notification := range notifications {
		responses[i] = *s.modelToNotificationResponse(&notification)
	}
	return responses, nil
}

func (s *service) UpdateNotification(id uuid.UUID, request NotificationRequest) (*NotificationResponse, error) {
	notification, err := s.repo.GetNotificationByID(id)
	if err != nil {
		return nil, err
	}

	notification.UserID = request.UserID
	notification.Type = request.Type
	notification.Title = request.Title
	notification.Body = request.Body
	notification.Data = request.Data
	notification.Priority = request.Priority
	notification.ActionURL = request.ActionURL
	notification.ActionText = request.ActionText
	notification.ExpiresAt = request.ExpiresAt
	notification.SourceID = request.SourceID
	notification.SourceType = request.SourceType

	err = s.repo.UpdateNotification(notification)
	if err != nil {
		return nil, err
	}

	return s.modelToNotificationResponse(notification), nil
}

func (s *service) DeleteNotification(id uuid.UUID) error {
	return s.repo.DeleteNotification(id)
}

func (s *service) GetUserNotifications(userID uuid.UUID) ([]NotificationResponse, error) {
	notifications, err := s.repo.GetUserNotifications(userID)
	if err != nil {
		return nil, err
	}

	responses := make([]NotificationResponse, len(notifications))
	for i, notification := range notifications {
		responses[i] = *s.modelToNotificationResponse(&notification)
	}
	return responses, nil
}

func (s *service) MarkNotificationAsRead(id uuid.UUID) error {
	return s.repo.MarkNotificationAsRead(id)
}

func (s *service) MarkAllNotificationsAsRead(userID uuid.UUID) error {
	return s.repo.MarkAllNotificationsAsRead(userID)
}

func (s *service) CreateAnnouncementNotification(announcementID uuid.UUID) error {
	announcement, err := s.repo.GetAnnouncementByID(announcementID)
	if err != nil {
		return err
	}

	// Parse target IDs to create notifications
	// This is a simplified version - in real app would parse JSON and create notifications per user
	// For now, we'll create a general notification that can be expanded later
	notification := NotificationRequest{
		UserID:     uuid.New(), // This would be the actual target user IDs
		Type:       NotificationTypeAnnouncement,
		Title:      announcement.Title,
		Body:       announcement.Content[:100] + "...",
		SourceID:   announcement.ID,
		SourceType: "ANNOUNCEMENT",
		ActionURL:  "/announcements/" + announcement.ID.String(),
		ActionText: "Lihat Pengumuman",
		Priority:   announcement.Priority,
	}

	_, err = s.CreateNotification(notification)
	return err
}

// MessageReadReceipt operations
func (s *service) CreateReadReceipt(request MessageReadReceiptRequest) (*MessageReadReceiptResponse, error) {
	receipt := &MessageReadReceipt{
		ID:        uuid.New(),
		MessageID: request.MessageID,
		UserID:    uuid.New(), // This should be set from context in real app
		ReadAt:    request.ReadAt,
	}

	err := s.repo.CreateReadReceipt(receipt)
	if err != nil {
		return nil, err
	}

	// Mark message as read
	message, err := s.repo.GetMessageByID(request.MessageID)
	if err == nil {
		message.Status = MessageStatusRead
		message.ReadAt = request.ReadAt
		_ = s.repo.UpdateMessage(message)
	}

	return s.modelToReadReceiptResponse(receipt), nil
}

func (s *service) GetMessageReadReceipts(messageID uuid.UUID) ([]MessageReadReceiptResponse, error) {
	receipts, err := s.repo.GetMessageReadReceipts(messageID)
	if err != nil {
		return nil, err
	}

	responses := make([]MessageReadReceiptResponse, len(receipts))
	for i, receipt := range receipts {
		responses[i] = *s.modelToReadReceiptResponse(&receipt)
	}
	return responses, nil
}

func (s *service) GetUserReadReceipts(userID uuid.UUID) ([]MessageReadReceiptResponse, error) {
	receipts, err := s.repo.GetUserReadReceipts(userID)
	if err != nil {
		return nil, err
	}

	responses := make([]MessageReadReceiptResponse, len(receipts))
	for i, receipt := range receipts {
		responses[i] = *s.modelToReadReceiptResponse(&receipt)
	}
	return responses, nil
}

// Analytics operations
func (s *service) GetCommunicationAnalytics(request CommunicationAnalyticsRequest) (*CommunicationAnalyticsResponse, error) {
	return s.repo.GetCommunicationAnalytics(request)
}

// Helper functions to convert models to DTOs
func (s *service) modelToAnnouncementResponse(announcement *Announcement) *AnnouncementResponse {
	response := &AnnouncementResponse{
		ID:               announcement.ID,
		Title:            announcement.Title,
		Content:          announcement.Content,
		AnnouncementType: announcement.AnnouncementType,
		TypeName:         GetAnnouncementTypeDescription(announcement.AnnouncementType),
		Priority:         announcement.Priority,
		PriorityName:     GetPriorityDescription(announcement.Priority),
		TargetAudience:   announcement.TargetAudience,
		TargetIDs:        announcement.TargetIDs,
		PublishDate:      announcement.PublishDate,
		ExpiryDate:       announcement.ExpiryDate,
		CreatedBy:        announcement.CreatedBy,
		IsPublished:      announcement.IsPublished,
		IsFeatured:       announcement.IsFeatured,
		AttachmentURL:    announcement.AttachmentURL,
		AttachmentName:   announcement.AttachmentName,
		CreatedAt:        announcement.CreatedAt,
		UpdatedAt:        announcement.UpdatedAt,
	}

	return response
}

func (s *service) modelToMessageResponse(message *Message) *MessageResponse {
	response := &MessageResponse{
		ID:             message.ID,
		SenderID:       message.SenderID,
		ReceiverID:     message.ReceiverID,
		Subject:        message.Subject,
		Body:           message.Body,
		MessageType:    message.MessageType,
		Status:         message.Status,
		StatusName:     GetMessageStatusDescription(message.Status),
		SentAt:         message.SentAt,
		ReadAt:         message.ReadAt,
		ParentID:       message.ParentID,
		AttachmentURL:  message.AttachmentURL,
		AttachmentName: message.AttachmentName,
		CreatedAt:      message.CreatedAt,
		UpdatedAt:      message.UpdatedAt,
	}

	return response
}

func (s *service) modelToNotificationResponse(notification *Notification) *NotificationResponse {
	response := &NotificationResponse{
		ID:         notification.ID,
		UserID:     notification.UserID,
		Type:       notification.Type,
		TypeName:   GetNotificationTypeDescription(notification.Type),
		Title:      notification.Title,
		Body:       notification.Body,
		Data:       notification.Data,
		Status:     notification.Status,
		Priority:   notification.Priority,
		ActionURL:  notification.ActionURL,
		ActionText: notification.ActionText,
		SentAt:     notification.SentAt,
		ReadAt:     notification.ReadAt,
		ExpiresAt:  notification.ExpiresAt,
		SourceID:   notification.SourceID,
		SourceType: notification.SourceType,
		CreatedAt:  notification.CreatedAt,
		UpdatedAt:  notification.UpdatedAt,
	}

	statusNames := map[string]string{
		NotificationStatusPending:   "Menunggu",
		NotificationStatusSent:      "Terkirim",
		NotificationStatusDelivered: "Diterima",
		NotificationStatusRead:      "Dibaca",
		NotificationStatusDismissed: "Ditolak",
	}
	response.StatusName = statusNames[notification.Status]

	priorityNames := map[string]string{
		AnnouncementPriorityLow:    "Rendah",
		AnnouncementPriorityMedium: "Sedang",
		AnnouncementPriorityHigh:   "Tinggi",
		AnnouncementPriorityUrgent: "Segera",
	}
	response.PriorityName = priorityNames[notification.Priority]

	return response
}

func (s *service) modelToReadReceiptResponse(receipt *MessageReadReceipt) *MessageReadReceiptResponse {
	response := &MessageReadReceiptResponse{
		ID:        receipt.ID,
		MessageID: receipt.MessageID,
		UserID:    receipt.UserID,
		ReadAt:    receipt.ReadAt,
		CreatedAt: receipt.CreatedAt,
	}

	return response
}
