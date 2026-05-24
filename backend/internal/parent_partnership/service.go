package parent_partnership

import (
	"context"
	"errors"
	"time"

	"github.com/google/uuid"
)

type ParentPartnershipService interface {
	// ParentPartnership
	GetAll(ctx context.Context) ([]ParentPartnershipResponse, error)
	GetByID(ctx context.Context, id string) (*ParentPartnershipResponse, error)
	GetByStudentID(ctx context.Context, studentID string) ([]ParentPartnershipResponse, error)
	GetActiveByStudentID(ctx context.Context, studentID string) ([]ParentPartnershipResponse, error)
	Create(ctx context.Context, req CreateParentPartnershipRequest) (*ParentPartnershipResponse, error)
	Update(ctx context.Context, id string, req UpdateParentPartnershipRequest) (*ParentPartnershipResponse, error)
	Delete(ctx context.Context, id string) error

	// ParentCommunication
	GetAllCommunications(ctx context.Context) ([]ParentCommunicationResponse, error)
	GetCommunicationByID(ctx context.Context, id string) (*ParentCommunicationResponse, error)
	GetCommunicationsByPartnership(ctx context.Context, partnershipID string) ([]ParentCommunicationResponse, error)
	GetPendingFollowUps(ctx context.Context) ([]ParentCommunicationResponse, error)
	CreateCommunication(ctx context.Context, req CreateParentCommunicationRequest) (*ParentCommunicationResponse, error)
	UpdateCommunication(ctx context.Context, id string, req UpdateParentCommunicationRequest) (*ParentCommunicationResponse, error)
	DeleteCommunication(ctx context.Context, id string) error

	// ParentMeeting
	GetAllMeetings(ctx context.Context) ([]ParentMeetingResponse, error)
	GetMeetingByID(ctx context.Context, id string) (*ParentMeetingResponse, error)
	GetMeetingsByPartnership(ctx context.Context, partnershipID string) ([]ParentMeetingResponse, error)
	GetMeetingsByTeacher(ctx context.Context, teacherID string) ([]ParentMeetingResponse, error)
	GetScheduledMeetings(ctx context.Context) ([]ParentMeetingResponse, error)
	CreateMeeting(ctx context.Context, req CreateParentMeetingRequest) (*ParentMeetingResponse, error)
	UpdateMeeting(ctx context.Context, id string, req UpdateParentMeetingRequest) (*ParentMeetingResponse, error)
	DeleteMeeting(ctx context.Context, id string) error

	// PartnershipActivity
	GetAllActivities(ctx context.Context) ([]PartnershipActivityResponse, error)
	GetActivityByID(ctx context.Context, id string) (*PartnershipActivityResponse, error)
	GetActivitiesByPartnership(ctx context.Context, partnershipID string) ([]PartnershipActivityResponse, error)
	GetActivitiesByDateRange(ctx context.Context, startDate, endDate string) ([]PartnershipActivityResponse, error)
	CreateActivity(ctx context.Context, req CreatePartnershipActivityRequest) (*PartnershipActivityResponse, error)
	UpdateActivity(ctx context.Context, id string, req UpdatePartnershipActivityRequest) (*PartnershipActivityResponse, error)
	DeleteActivity(ctx context.Context, id string) error

	// Summary
	GetPartnershipSummary(ctx context.Context) (*PartnershipSummaryResponse, error)
}

type parentPartnershipService struct {
	repo ParentPartnershipRepository
}

func NewParentPartnershipService(repo ParentPartnershipRepository) ParentPartnershipService {
	return &parentPartnershipService{repo: repo}
}

// ParentPartnership Methods
func (s *parentPartnershipService) GetAll(ctx context.Context) ([]ParentPartnershipResponse, error) {
	partnerships, err := s.repo.GetAll(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]ParentPartnershipResponse, len(partnerships))
	for i, p := range partnerships {
		responses[i] = *s.partnershipToResponse(&p)
	}
	return responses, nil
}

func (s *parentPartnershipService) GetByID(ctx context.Context, id string) (*ParentPartnershipResponse, error) {
	partnership, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("partnership tidak ditemukan")
	}
	return s.partnershipToResponse(partnership), nil
}

func (s *parentPartnershipService) GetByStudentID(ctx context.Context, studentID string) ([]ParentPartnershipResponse, error) {
	partnerships, err := s.repo.GetByStudentID(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]ParentPartnershipResponse, len(partnerships))
	for i, p := range partnerships {
		responses[i] = *s.partnershipToResponse(&p)
	}
	return responses, nil
}

func (s *parentPartnershipService) GetActiveByStudentID(ctx context.Context, studentID string) ([]ParentPartnershipResponse, error) {
	partnerships, err := s.repo.GetActiveByStudentID(ctx, studentID)
	if err != nil {
		return nil, err
	}

	responses := make([]ParentPartnershipResponse, len(partnerships))
	for i, p := range partnerships {
		responses[i] = *s.partnershipToResponse(&p)
	}
	return responses, nil
}

func (s *parentPartnershipService) Create(ctx context.Context, req CreateParentPartnershipRequest) (*ParentPartnershipResponse, error) {
	studentUUID, err := uuid.Parse(req.StudentID)
	if err != nil {
		return nil, errors.New("invalid student ID format")
	}

	var parentUUID *uuid.UUID
	if req.ParentID != nil {
		parsed, err := uuid.Parse(*req.ParentID)
		if err != nil {
			return nil, errors.New("invalid parent ID format")
		}
		parentUUID = &parsed
	}

	partnership := &ParentPartnership{
		ID:                      uuid.New(),
		StudentID:               studentUUID,
		ParentID:                parentUUID,
		PartnershipType:         req.PartnershipType,
		Relationship:            req.Relationship,
		ContactPrimary:          req.ContactPrimary,
		ContactSecondary:        req.ContactSecondary,
		Email:                   req.Email,
		Address:                 req.Address,
		CommunicationPreference: req.CommunicationPreference,
		InvolvementLevel:        req.InvolvementLevel,
		Notes:                   req.Notes,
		IsActive:                true,
	}

	if req.IsActive != nil {
		partnership.IsActive = *req.IsActive
	}

	if req.CommunicationPreference == "" {
		partnership.CommunicationPreference = CommunicationPreferencePhone
	}

	if req.InvolvementLevel == "" {
		partnership.InvolvementLevel = InvolvementLevelModerate
	}

	if err := s.repo.Create(ctx, partnership); err != nil {
		return nil, err
	}
	return s.partnershipToResponse(partnership), nil
}

func (s *parentPartnershipService) Update(ctx context.Context, id string, req UpdateParentPartnershipRequest) (*ParentPartnershipResponse, error) {
	partnership, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("partnership tidak ditemukan")
	}

	if req.ParentID != nil {
		if *req.ParentID != "" {
			parsed, err := uuid.Parse(*req.ParentID)
			if err != nil {
				return nil, errors.New("invalid parent ID format")
			}
			partnership.ParentID = &parsed
		} else {
			partnership.ParentID = nil
		}
	}

	if req.PartnershipType != "" {
		partnership.PartnershipType = req.PartnershipType
	}
	if req.Relationship != "" {
		partnership.Relationship = req.Relationship
	}
	if req.ContactPrimary != "" {
		partnership.ContactPrimary = req.ContactPrimary
	}
	if req.ContactSecondary != "" {
		partnership.ContactSecondary = req.ContactSecondary
	}
	if req.Email != "" {
		partnership.Email = req.Email
	}
	if req.Address != "" {
		partnership.Address = req.Address
	}
	if req.CommunicationPreference != "" {
		partnership.CommunicationPreference = req.CommunicationPreference
	}
	if req.InvolvementLevel != "" {
		partnership.InvolvementLevel = req.InvolvementLevel
	}
	if req.Notes != "" {
		partnership.Notes = req.Notes
	}
	if req.IsActive != nil {
		partnership.IsActive = *req.IsActive
	}

	if err := s.repo.Update(ctx, partnership); err != nil {
		return nil, err
	}
	return s.partnershipToResponse(partnership), nil
}

func (s *parentPartnershipService) Delete(ctx context.Context, id string) error {
	_, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return errors.New("partnership tidak ditemukan")
	}
	return s.repo.Delete(ctx, id)
}

// ParentCommunication Methods
func (s *parentPartnershipService) GetAllCommunications(ctx context.Context) ([]ParentCommunicationResponse, error) {
	communications, err := s.repo.GetAllCommunications(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]ParentCommunicationResponse, len(communications))
	for i, c := range communications {
		responses[i] = *s.communicationToResponse(&c)
	}
	return responses, nil
}

func (s *parentPartnershipService) GetCommunicationByID(ctx context.Context, id string) (*ParentCommunicationResponse, error) {
	communication, err := s.repo.GetCommunicationByID(ctx, id)
	if err != nil {
		return nil, errors.New("communication tidak ditemukan")
	}
	return s.communicationToResponse(communication), nil
}

func (s *parentPartnershipService) GetCommunicationsByPartnership(ctx context.Context, partnershipID string) ([]ParentCommunicationResponse, error) {
	communications, err := s.repo.GetCommunicationsByPartnership(ctx, partnershipID)
	if err != nil {
		return nil, err
	}

	responses := make([]ParentCommunicationResponse, len(communications))
	for i, c := range communications {
		responses[i] = *s.communicationToResponse(&c)
	}
	return responses, nil
}

func (s *parentPartnershipService) GetPendingFollowUps(ctx context.Context) ([]ParentCommunicationResponse, error) {
	communications, err := s.repo.GetPendingFollowUps(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]ParentCommunicationResponse, len(communications))
	for i, c := range communications {
		responses[i] = *s.communicationToResponse(&c)
	}
	return responses, nil
}

func (s *parentPartnershipService) CreateCommunication(ctx context.Context, req CreateParentCommunicationRequest) (*ParentCommunicationResponse, error) {
	partnershipUUID, err := uuid.Parse(req.PartnershipID)
	if err != nil {
		return nil, errors.New("invalid partnership ID format")
	}

	teacherUUID, err := uuid.Parse(req.TeacherID)
	if err != nil {
		return nil, errors.New("invalid teacher ID format")
	}

	communicationDate, err := time.Parse(time.RFC3339, req.CommunicationDate)
	if err != nil {
		return nil, errors.New("invalid communication date format, use RFC3339")
	}

	communication := &ParentCommunication{
		ID:                uuid.New(),
		PartnershipID:     partnershipUUID,
		TeacherID:         teacherUUID,
		CommunicationType: req.CommunicationType,
		CommunicationDate: communicationDate,
		Subject:           req.Subject,
		Content:           req.Content,
		Direction:         req.Direction,
		Status:            req.Status,
		Notes:             req.Notes,
	}

	if req.Status == "" {
		communication.Status = CommunicationStatusCompleted
	}

	if req.FollowUpRequired != nil {
		communication.FollowUpRequired = *req.FollowUpRequired
	}

	if req.FollowUpDate != nil {
		followUpDate, err := time.Parse(time.RFC3339, *req.FollowUpDate)
		if err != nil {
			return nil, errors.New("invalid follow-up date format, use RFC3339")
		}
		communication.FollowUpDate = &followUpDate
	}

	if req.ResponseReceived != nil {
		communication.ResponseReceived = *req.ResponseReceived
	}

	if req.ResponseDate != nil {
		responseDate, err := time.Parse(time.RFC3339, *req.ResponseDate)
		if err != nil {
			return nil, errors.New("invalid response date format, use RFC3339")
		}
		communication.ResponseDate = &responseDate
	}

	if err := s.repo.CreateCommunication(ctx, communication); err != nil {
		return nil, err
	}
	return s.communicationToResponse(communication), nil
}

func (s *parentPartnershipService) UpdateCommunication(ctx context.Context, id string, req UpdateParentCommunicationRequest) (*ParentCommunicationResponse, error) {
	communication, err := s.repo.GetCommunicationByID(ctx, id)
	if err != nil {
		return nil, errors.New("communication tidak ditemukan")
	}

	if req.CommunicationType != "" {
		communication.CommunicationType = req.CommunicationType
	}
	if req.CommunicationDate != "" {
		date, err := time.Parse(time.RFC3339, req.CommunicationDate)
		if err != nil {
			return nil, errors.New("invalid communication date format, use RFC3339")
		}
		communication.CommunicationDate = date
	}
	if req.Subject != "" {
		communication.Subject = req.Subject
	}
	if req.Content != "" {
		communication.Content = req.Content
	}
	if req.Direction != "" {
		communication.Direction = req.Direction
	}
	if req.Status != "" {
		communication.Status = req.Status
	}
	if req.FollowUpRequired != nil {
		communication.FollowUpRequired = *req.FollowUpRequired
	}
	if req.FollowUpDate != nil {
		if *req.FollowUpDate != "" {
			date, err := time.Parse(time.RFC3339, *req.FollowUpDate)
			if err != nil {
				return nil, errors.New("invalid follow-up date format, use RFC3339")
			}
			communication.FollowUpDate = &date
		} else {
			communication.FollowUpDate = nil
		}
	}
	if req.ResponseReceived != nil {
		communication.ResponseReceived = *req.ResponseReceived
	}
	if req.ResponseDate != nil {
		if *req.ResponseDate != "" {
			date, err := time.Parse(time.RFC3339, *req.ResponseDate)
			if err != nil {
				return nil, errors.New("invalid response date format, use RFC3339")
			}
			communication.ResponseDate = &date
		} else {
			communication.ResponseDate = nil
		}
	}
	if req.Notes != "" {
		communication.Notes = req.Notes
	}

	if err := s.repo.UpdateCommunication(ctx, communication); err != nil {
		return nil, err
	}
	return s.communicationToResponse(communication), nil
}

func (s *parentPartnershipService) DeleteCommunication(ctx context.Context, id string) error {
	_, err := s.repo.GetCommunicationByID(ctx, id)
	if err != nil {
		return errors.New("communication tidak ditemukan")
	}
	return s.repo.DeleteCommunication(ctx, id)
}

// ParentMeeting Methods
func (s *parentPartnershipService) GetAllMeetings(ctx context.Context) ([]ParentMeetingResponse, error) {
	meetings, err := s.repo.GetAllMeetings(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]ParentMeetingResponse, len(meetings))
	for i, m := range meetings {
		responses[i] = *s.meetingToResponse(&m)
	}
	return responses, nil
}

func (s *parentPartnershipService) GetMeetingByID(ctx context.Context, id string) (*ParentMeetingResponse, error) {
	meeting, err := s.repo.GetMeetingByID(ctx, id)
	if err != nil {
		return nil, errors.New("meeting tidak ditemukan")
	}
	return s.meetingToResponse(meeting), nil
}

func (s *parentPartnershipService) GetMeetingsByPartnership(ctx context.Context, partnershipID string) ([]ParentMeetingResponse, error) {
	meetings, err := s.repo.GetMeetingsByPartnership(ctx, partnershipID)
	if err != nil {
		return nil, err
	}

	responses := make([]ParentMeetingResponse, len(meetings))
	for i, m := range meetings {
		responses[i] = *s.meetingToResponse(&m)
	}
	return responses, nil
}

func (s *parentPartnershipService) GetMeetingsByTeacher(ctx context.Context, teacherID string) ([]ParentMeetingResponse, error) {
	meetings, err := s.repo.GetMeetingsByTeacher(ctx, teacherID)
	if err != nil {
		return nil, err
	}

	responses := make([]ParentMeetingResponse, len(meetings))
	for i, m := range meetings {
		responses[i] = *s.meetingToResponse(&m)
	}
	return responses, nil
}

func (s *parentPartnershipService) GetScheduledMeetings(ctx context.Context) ([]ParentMeetingResponse, error) {
	meetings, err := s.repo.GetScheduledMeetings(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]ParentMeetingResponse, len(meetings))
	for i, m := range meetings {
		responses[i] = *s.meetingToResponse(&m)
	}
	return responses, nil
}

func (s *parentPartnershipService) CreateMeeting(ctx context.Context, req CreateParentMeetingRequest) (*ParentMeetingResponse, error) {
	partnershipUUID, err := uuid.Parse(req.PartnershipID)
	if err != nil {
		return nil, errors.New("invalid partnership ID format")
	}

	teacherUUID, err := uuid.Parse(req.TeacherID)
	if err != nil {
		return nil, errors.New("invalid teacher ID format")
	}

	scheduledDate, err := time.Parse(time.RFC3339, req.ScheduledDate)
	if err != nil {
		return nil, errors.New("invalid scheduled date format, use RFC3339")
	}

	meeting := &ParentMeeting{
		ID:              uuid.New(),
		PartnershipID:   partnershipUUID,
		TeacherID:       teacherUUID,
		MeetingType:     req.MeetingType,
		ScheduledDate:   scheduledDate,
		DurationMinutes: req.DurationMinutes,
		Location:        req.Location,
		Agenda:          req.Agenda,
		Status:          req.Status,
		ActionItems:     req.ActionItems,
	}

	if req.DurationMinutes == 0 {
		meeting.DurationMinutes = 30
	}

	if req.Location == "" {
		meeting.Location = "SCHOOL"
	}

	if req.Status == "" {
		meeting.Status = MeetingStatusScheduled
	}

	if req.NextMeetingDate != nil {
		nextDate, err := time.Parse(time.RFC3339, *req.NextMeetingDate)
		if err != nil {
			return nil, errors.New("invalid next meeting date format, use RFC3339")
		}
		meeting.NextMeetingDate = &nextDate
	}

	if err := s.repo.CreateMeeting(ctx, meeting); err != nil {
		return nil, err
	}
	return s.meetingToResponse(meeting), nil
}

func (s *parentPartnershipService) UpdateMeeting(ctx context.Context, id string, req UpdateParentMeetingRequest) (*ParentMeetingResponse, error) {
	meeting, err := s.repo.GetMeetingByID(ctx, id)
	if err != nil {
		return nil, errors.New("meeting tidak ditemukan")
	}

	if req.MeetingType != "" {
		meeting.MeetingType = req.MeetingType
	}
	if req.ScheduledDate != "" {
		date, err := time.Parse(time.RFC3339, req.ScheduledDate)
		if err != nil {
			return nil, errors.New("invalid scheduled date format, use RFC3339")
		}
		meeting.ScheduledDate = date
	}
	if req.DurationMinutes != 0 {
		meeting.DurationMinutes = req.DurationMinutes
	}
	if req.Location != "" {
		meeting.Location = req.Location
	}
	if req.Agenda != "" {
		meeting.Agenda = req.Agenda
	}
	if req.Status != "" {
		meeting.Status = req.Status
	}
	if req.AttendanceStatus != "" {
		meeting.AttendanceStatus = req.AttendanceStatus
	}
	if req.Summary != "" {
		meeting.Summary = req.Summary
	}
	if req.ActionItems != nil {
		meeting.ActionItems = req.ActionItems
	}
	if req.NextMeetingDate != nil {
		if *req.NextMeetingDate != "" {
			date, err := time.Parse(time.RFC3339, *req.NextMeetingDate)
			if err != nil {
				return nil, errors.New("invalid next meeting date format, use RFC3339")
			}
			meeting.NextMeetingDate = &date
		} else {
			meeting.NextMeetingDate = nil
		}
	}

	if err := s.repo.UpdateMeeting(ctx, meeting); err != nil {
		return nil, err
	}
	return s.meetingToResponse(meeting), nil
}

func (s *parentPartnershipService) DeleteMeeting(ctx context.Context, id string) error {
	_, err := s.repo.GetMeetingByID(ctx, id)
	if err != nil {
		return errors.New("meeting tidak ditemukan")
	}
	return s.repo.DeleteMeeting(ctx, id)
}

// PartnershipActivity Methods
func (s *parentPartnershipService) GetAllActivities(ctx context.Context) ([]PartnershipActivityResponse, error) {
	activities, err := s.repo.GetAllActivities(ctx)
	if err != nil {
		return nil, err
	}

	responses := make([]PartnershipActivityResponse, len(activities))
	for i, a := range activities {
		responses[i] = *s.activityToResponse(&a)
	}
	return responses, nil
}

func (s *parentPartnershipService) GetActivityByID(ctx context.Context, id string) (*PartnershipActivityResponse, error) {
	activity, err := s.repo.GetActivityByID(ctx, id)
	if err != nil {
		return nil, errors.New("activity tidak ditemukan")
	}
	return s.activityToResponse(activity), nil
}

func (s *parentPartnershipService) GetActivitiesByPartnership(ctx context.Context, partnershipID string) ([]PartnershipActivityResponse, error) {
	activities, err := s.repo.GetActivitiesByPartnership(ctx, partnershipID)
	if err != nil {
		return nil, err
	}

	responses := make([]PartnershipActivityResponse, len(activities))
	for i, a := range activities {
		responses[i] = *s.activityToResponse(&a)
	}
	return responses, nil
}

func (s *parentPartnershipService) GetActivitiesByDateRange(ctx context.Context, startDate, endDate string) ([]PartnershipActivityResponse, error) {
	activities, err := s.repo.GetActivitiesByDateRange(ctx, startDate, endDate)
	if err != nil {
		return nil, err
	}

	responses := make([]PartnershipActivityResponse, len(activities))
	for i, a := range activities {
		responses[i] = *s.activityToResponse(&a)
	}
	return responses, nil
}

func (s *parentPartnershipService) CreateActivity(ctx context.Context, req CreatePartnershipActivityRequest) (*PartnershipActivityResponse, error) {
	partnershipUUID, err := uuid.Parse(req.PartnershipID)
	if err != nil {
		return nil, errors.New("invalid partnership ID format")
	}

	activityDate, err := time.Parse("2006-01-02", req.ActivityDate)
	if err != nil {
		return nil, errors.New("invalid activity date format, use YYYY-MM-DD")
	}

	activity := &PartnershipActivity{
		ID:               uuid.New(),
		PartnershipID:    partnershipUUID,
		ActivityType:     req.ActivityType,
		ActivityDate:     activityDate,
		Description:      req.Description,
		HoursContributed: req.HoursContributed,
		ImpactRating:     req.ImpactRating,
		Notes:            req.Notes,
	}

	if err := s.repo.CreateActivity(ctx, activity); err != nil {
		return nil, err
	}
	return s.activityToResponse(activity), nil
}

func (s *parentPartnershipService) UpdateActivity(ctx context.Context, id string, req UpdatePartnershipActivityRequest) (*PartnershipActivityResponse, error) {
	activity, err := s.repo.GetActivityByID(ctx, id)
	if err != nil {
		return nil, errors.New("activity tidak ditemukan")
	}

	if req.ActivityType != "" {
		activity.ActivityType = req.ActivityType
	}
	if req.ActivityDate != "" {
		date, err := time.Parse("2006-01-02", req.ActivityDate)
		if err != nil {
			return nil, errors.New("invalid activity date format, use YYYY-MM-DD")
		}
		activity.ActivityDate = date
	}
	if req.Description != "" {
		activity.Description = req.Description
	}
	if req.HoursContributed != nil {
		activity.HoursContributed = req.HoursContributed
	}
	if req.ImpactRating != "" {
		activity.ImpactRating = req.ImpactRating
	}
	if req.Notes != "" {
		activity.Notes = req.Notes
	}

	if err := s.repo.UpdateActivity(ctx, activity); err != nil {
		return nil, err
	}
	return s.activityToResponse(activity), nil
}

func (s *parentPartnershipService) DeleteActivity(ctx context.Context, id string) error {
	_, err := s.repo.GetActivityByID(ctx, id)
	if err != nil {
		return errors.New("activity tidak ditemukan")
	}
	return s.repo.DeleteActivity(ctx, id)
}

// Summary Method
func (s *parentPartnershipService) GetPartnershipSummary(ctx context.Context) (*PartnershipSummaryResponse, error) {
	return s.repo.GetPartnershipSummary(ctx)
}

// Helper methods for converting models to responses
func (s *parentPartnershipService) partnershipToResponse(p *ParentPartnership) *ParentPartnershipResponse {
	var parentID *string
	if p.ParentID != nil {
		pid := p.ParentID.String()
		parentID = &pid
	}

	var createdBy *string
	if p.CreatedBy != nil {
		cb := p.CreatedBy.String()
		createdBy = &cb
	}

	var updatedBy *string
	if p.UpdatedBy != nil {
		ub := p.UpdatedBy.String()
		updatedBy = &ub
	}

	return &ParentPartnershipResponse{
		ID:                      p.ID.String(),
		StudentID:               p.StudentID.String(),
		ParentID:                parentID,
		PartnershipType:         p.PartnershipType,
		Relationship:            p.Relationship,
		ContactPrimary:          p.ContactPrimary,
		ContactSecondary:        p.ContactSecondary,
		Email:                   p.Email,
		Address:                 p.Address,
		CommunicationPreference: p.CommunicationPreference,
		InvolvementLevel:        p.InvolvementLevel,
		Notes:                   p.Notes,
		IsActive:                p.IsActive,
		CreatedAt:               p.CreatedAt,
		UpdatedAt:               p.UpdatedAt,
		CreatedBy:               createdBy,
		UpdatedBy:               updatedBy,
	}
}

func (s *parentPartnershipService) communicationToResponse(c *ParentCommunication) *ParentCommunicationResponse {
	return &ParentCommunicationResponse{
		ID:                c.ID.String(),
		PartnershipID:     c.PartnershipID.String(),
		TeacherID:         c.TeacherID.String(),
		CommunicationType: c.CommunicationType,
		CommunicationDate: c.CommunicationDate,
		Subject:           c.Subject,
		Content:           c.Content,
		Direction:         c.Direction,
		Status:            c.Status,
		FollowUpRequired:  c.FollowUpRequired,
		FollowUpDate:      c.FollowUpDate,
		ResponseReceived:  c.ResponseReceived,
		ResponseDate:      c.ResponseDate,
		Notes:             c.Notes,
		CreatedAt:         c.CreatedAt,
		UpdatedAt:         c.UpdatedAt,
	}
}

func (s *parentPartnershipService) meetingToResponse(m *ParentMeeting) *ParentMeetingResponse {
	return &ParentMeetingResponse{
		ID:               m.ID.String(),
		PartnershipID:    m.PartnershipID.String(),
		TeacherID:        m.TeacherID.String(),
		MeetingType:      m.MeetingType,
		ScheduledDate:    m.ScheduledDate,
		DurationMinutes:  m.DurationMinutes,
		Location:         m.Location,
		Agenda:           m.Agenda,
		Status:           m.Status,
		AttendanceStatus: m.AttendanceStatus,
		Summary:          m.Summary,
		ActionItems:      m.ActionItems,
		NextMeetingDate:  m.NextMeetingDate,
		CreatedAt:        m.CreatedAt,
		UpdatedAt:        m.UpdatedAt,
	}
}

func (s *parentPartnershipService) activityToResponse(a *PartnershipActivity) *PartnershipActivityResponse {
	return &PartnershipActivityResponse{
		ID:               a.ID.String(),
		PartnershipID:    a.PartnershipID.String(),
		ActivityType:     a.ActivityType,
		ActivityDate:     a.ActivityDate,
		Description:      a.Description,
		HoursContributed: a.HoursContributed,
		ImpactRating:     a.ImpactRating,
		Notes:            a.Notes,
		CreatedAt:        a.CreatedAt,
		UpdatedAt:        a.UpdatedAt,
	}
}
