package parent_partnership

import "time"

// ParentPartnership DTOs

type CreateParentPartnershipRequest struct {
	StudentID               string  `json:"student_id" binding:"required"`
	ParentID                *string `json:"parent_id"`
	PartnershipType         string  `json:"partnership_type" binding:"required,oneof=PRIMARY SECONDARY EMERGENCY"`
	Relationship            string  `json:"relationship" binding:"required,oneof=FATHER MOTHER GUARDIAN GRANDPARENT"`
	ContactPrimary          string  `json:"contact_primary" binding:"required"`
	ContactSecondary        string  `json:"contact_secondary"`
	Email                   string  `json:"email"`
	Address                 string  `json:"address"`
	CommunicationPreference string  `json:"communication_preference" binding:"omitempty,oneof=PHONE EMAIL WHATSAPP IN_PERSON"`
	InvolvementLevel        string  `json:"involvement_level" binding:"omitempty,oneof=LOW MODERATE HIGH VERY_HIGH"`
	Notes                   string  `json:"notes"`
	IsActive                *bool   `json:"is_active"`
}

type UpdateParentPartnershipRequest struct {
	ParentID                *string `json:"parent_id"`
	PartnershipType         string  `json:"partnership_type" binding:"omitempty,oneof=PRIMARY SECONDARY EMERGENCY"`
	Relationship            string  `json:"relationship" binding:"omitempty,oneof=FATHER MOTHER GUARDIAN GRANDPARENT"`
	ContactPrimary          string  `json:"contact_primary" binding:"omitempty"`
	ContactSecondary        string  `json:"contact_secondary"`
	Email                   string  `json:"email"`
	Address                 string  `json:"address"`
	CommunicationPreference string  `json:"communication_preference" binding:"omitempty,oneof=PHONE EMAIL WHATSAPP IN_PERSON"`
	InvolvementLevel        string  `json:"involvement_level" binding:"omitempty,oneof=LOW MODERATE HIGH VERY_HIGH"`
	Notes                   string  `json:"notes"`
	IsActive                *bool   `json:"is_active"`
}

type ParentPartnershipResponse struct {
	ID                      string    `json:"id"`
	StudentID               string    `json:"student_id"`
	ParentID                *string   `json:"parent_id"`
	PartnershipType         string    `json:"partnership_type"`
	Relationship            string    `json:"relationship"`
	ContactPrimary          string    `json:"contact_primary"`
	ContactSecondary        string    `json:"contact_secondary"`
	Email                   string    `json:"email"`
	Address                 string    `json:"address"`
	CommunicationPreference string    `json:"communication_preference"`
	InvolvementLevel        string    `json:"involvement_level"`
	Notes                   string    `json:"notes"`
	IsActive                bool      `json:"is_active"`
	CreatedAt               time.Time `json:"created_at"`
	UpdatedAt               time.Time `json:"updated_at"`
	CreatedBy               *string   `json:"created_by,omitempty"`
	UpdatedBy               *string   `json:"updated_by,omitempty"`
}

type ParentPartnershipListResponse struct {
	Partnerships []ParentPartnershipResponse `json:"partnerships"`
	Total        int                         `json:"total"`
}

// ParentCommunication DTOs

type CreateParentCommunicationRequest struct {
	PartnershipID     string  `json:"partnership_id" binding:"required"`
	TeacherID         string  `json:"teacher_id" binding:"required"`
	CommunicationType string  `json:"communication_type" binding:"required,oneof=PHONE_CALL EMAIL MEETING WHATSAPP NOTE"`
	CommunicationDate string  `json:"communication_date" binding:"required"` // RFC3339 format
	Subject           string  `json:"subject"`
	Content           string  `json:"content" binding:"required"`
	Direction         string  `json:"direction" binding:"required,oneof=INCOMING OUTGOING"`
	Status            string  `json:"status" binding:"omitempty,oneof=SCHEDULED COMPLETED CANCELLED FOLLOW_UP"`
	FollowUpRequired  *bool   `json:"follow_up_required"`
	FollowUpDate      *string `json:"follow_up_date"` // RFC3339 format
	ResponseReceived  *bool   `json:"response_received"`
	ResponseDate      *string `json:"response_date"` // RFC3339 format
	Notes             string  `json:"notes"`
}

type UpdateParentCommunicationRequest struct {
	CommunicationType string  `json:"communication_type" binding:"omitempty,oneof=PHONE_CALL EMAIL MEETING WHATSAPP NOTE"`
	CommunicationDate string  `json:"communication_date"` // RFC3339 format
	Subject           string  `json:"subject"`
	Content           string  `json:"content" binding:"omitempty"`
	Direction         string  `json:"direction" binding:"omitempty,oneof=INCOMING OUTGOING"`
	Status            string  `json:"status" binding:"omitempty,oneof=SCHEDULED COMPLETED CANCELLED FOLLOW_UP"`
	FollowUpRequired  *bool   `json:"follow_up_required"`
	FollowUpDate      *string `json:"follow_up_date"` // RFC3339 format
	ResponseReceived  *bool   `json:"response_received"`
	ResponseDate      *string `json:"response_date"` // RFC3339 format
	Notes             string  `json:"notes"`
}

type ParentCommunicationResponse struct {
	ID                string     `json:"id"`
	PartnershipID     string     `json:"partnership_id"`
	TeacherID         string     `json:"teacher_id"`
	CommunicationType string     `json:"communication_type"`
	CommunicationDate time.Time  `json:"communication_date"`
	Subject           string     `json:"subject"`
	Content           string     `json:"content"`
	Direction         string     `json:"direction"`
	Status            string     `json:"status"`
	FollowUpRequired  bool       `json:"follow_up_required"`
	FollowUpDate      *time.Time `json:"follow_up_date"`
	ResponseReceived  bool       `json:"response_received"`
	ResponseDate      *time.Time `json:"response_date"`
	Notes             string     `json:"notes"`
	CreatedAt         time.Time  `json:"created_at"`
	UpdatedAt         time.Time  `json:"updated_at"`
}

type ParentCommunicationListResponse struct {
	Communications []ParentCommunicationResponse `json:"communications"`
	Total          int                           `json:"total"`
}

// ParentMeeting DTOs

type CreateParentMeetingRequest struct {
	PartnershipID   string   `json:"partnership_id" binding:"required"`
	TeacherID       string   `json:"teacher_id" binding:"required"`
	MeetingType     string   `json:"meeting_type" binding:"required,oneof=PARENT_TEACHER_CONFERENCE IEP_MEETING BEHAVIOR_DISCUSSION ACADEMIC_REVIEW"`
	ScheduledDate   string   `json:"scheduled_date" binding:"required"` // RFC3339 format
	DurationMinutes int      `json:"duration_minutes" binding:"omitempty,min=5"`
	Location        string   `json:"location"`
	Agenda          string   `json:"agenda"`
	Status          string   `json:"status" binding:"omitempty,oneof=SCHEDULED CONFIRMED COMPLETED CANCELLED NO_SHOW"`
	ActionItems     []string `json:"action_items"`
	NextMeetingDate *string  `json:"next_meeting_date"` // RFC3339 format
}

type UpdateParentMeetingRequest struct {
	MeetingType      string   `json:"meeting_type" binding:"omitempty,oneof=PARENT_TEACHER_CONFERENCE IEP_MEETING BEHAVIOR_DISCUSSION ACADEMIC_REVIEW"`
	ScheduledDate    string   `json:"scheduled_date"` // RFC3339 format
	DurationMinutes  int      `json:"duration_minutes" binding:"omitempty,min=5"`
	Location         string   `json:"location"`
	Agenda           string   `json:"agenda"`
	Status           string   `json:"status" binding:"omitempty,oneof=SCHEDULED CONFIRMED COMPLETED CANCELLED NO_SHOW"`
	AttendanceStatus string   `json:"attendance_status" binding:"omitempty,oneof=ATTENDED NO_SHOW RESCHEDULED"`
	Summary          string   `json:"summary"`
	ActionItems      []string `json:"action_items"`
	NextMeetingDate  *string  `json:"next_meeting_date"` // RFC3339 format
}

type ParentMeetingResponse struct {
	ID               string     `json:"id"`
	PartnershipID    string     `json:"partnership_id"`
	TeacherID        string     `json:"teacher_id"`
	MeetingType      string     `json:"meeting_type"`
	ScheduledDate    time.Time  `json:"scheduled_date"`
	DurationMinutes  int        `json:"duration_minutes"`
	Location         string     `json:"location"`
	Agenda           string     `json:"agenda"`
	Status           string     `json:"status"`
	AttendanceStatus string     `json:"attendance_status"`
	Summary          string     `json:"summary"`
	ActionItems      []string   `json:"action_items"`
	NextMeetingDate  *time.Time `json:"next_meeting_date"`
	CreatedAt        time.Time  `json:"created_at"`
	UpdatedAt        time.Time  `json:"updated_at"`
}

type ParentMeetingListResponse struct {
	Meetings []ParentMeetingResponse `json:"meetings"`
	Total    int                     `json:"total"`
}

// PartnershipActivity DTOs

type CreatePartnershipActivityRequest struct {
	PartnershipID    string   `json:"partnership_id" binding:"required"`
	ActivityType     string   `json:"activity_type" binding:"required,oneof=VOLUNTEER EVENT_ATTENDANCE HOMEWORK_SUPPORT SCHOOL_VISIT WORKSHOP"`
	ActivityDate     string   `json:"activity_date" binding:"required"` // YYYY-MM-DD
	Description      string   `json:"description"`
	HoursContributed *float64 `json:"hours_contributed" binding:"omitempty,min=0"`
	ImpactRating     string   `json:"impact_rating" binding:"omitempty,oneof=LOW MEDIUM HIGH"`
	Notes            string   `json:"notes"`
}

type UpdatePartnershipActivityRequest struct {
	ActivityType     string   `json:"activity_type" binding:"omitempty,oneof=VOLUNTEER EVENT_ATTENDANCE HOMEWORK_SUPPORT SCHOOL_VISIT WORKSHOP"`
	ActivityDate     string   `json:"activity_date"` // YYYY-MM-DD
	Description      string   `json:"description"`
	HoursContributed *float64 `json:"hours_contributed" binding:"omitempty,min=0"`
	ImpactRating     string   `json:"impact_rating" binding:"omitempty,oneof=LOW MEDIUM HIGH"`
	Notes            string   `json:"notes"`
}

type PartnershipActivityResponse struct {
	ID               string    `json:"id"`
	PartnershipID    string    `json:"partnership_id"`
	ActivityType     string    `json:"activity_type"`
	ActivityDate     time.Time `json:"activity_date"`
	Description      string    `json:"description"`
	HoursContributed *float64  `json:"hours_contributed"`
	ImpactRating     string    `json:"impact_rating"`
	Notes            string    `json:"notes"`
	CreatedAt        time.Time `json:"created_at"`
	UpdatedAt        time.Time `json:"updated_at"`
}

type PartnershipActivityListResponse struct {
	Activities []PartnershipActivityResponse `json:"activities"`
	Total      int                           `json:"total"`
}

// Summary Response
type PartnershipSummaryResponse struct {
	TotalPartnerships       int     `json:"total_partnerships"`
	ActivePartnerships      int     `json:"active_partnerships"`
	TotalCommunications     int     `json:"total_communications"`
	PendingFollowUps        int     `json:"pending_follow_ups"`
	ScheduledMeetings       int     `json:"scheduled_meetings"`
	CompletedMeetings       int     `json:"completed_meetings"`
	TotalActivities         int     `json:"total_activities"`
	TotalVolunteerHours     float64 `json:"total_volunteer_hours"`
	AverageInvolvementLevel string  `json:"average_involvement_level"`
}
