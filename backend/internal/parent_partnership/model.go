package parent_partnership

import (
	"time"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// Partnership Type Constants
const (
	PartnershipTypePrimary   = "PRIMARY"
	PartnershipTypeSecondary = "SECONDARY"
	PartnershipTypeEmergency = "EMERGENCY"
)

// Relationship Constants
const (
	RelationshipFather      = "FATHER"
	RelationshipMother      = "MOTHER"
	RelationshipGuardian    = "GUARDIAN"
	RelationshipGrandparent = "GRANDPARENT"
)

// Communication Preference Constants
const (
	CommunicationPreferencePhone    = "PHONE"
	CommunicationPreferenceEmail    = "EMAIL"
	CommunicationPreferenceWhatsApp = "WHATSAPP"
	CommunicationPreferenceInPerson = "IN_PERSON"
)

// Involvement Level Constants
const (
	InvolvementLevelLow      = "LOW"
	InvolvementLevelModerate = "MODERATE"
	InvolvementLevelHigh     = "HIGH"
	InvolvementLevelVeryHigh = "VERY_HIGH"
)

// Communication Type Constants
const (
	CommunicationTypePhoneCall = "PHONE_CALL"
	CommunicationTypeEmail     = "EMAIL"
	CommunicationTypeMeeting   = "MEETING"
	CommunicationTypeWhatsApp  = "WHATSAPP"
	CommunicationTypeNote      = "NOTE"
)

// Communication Direction Constants
const (
	DirectionIncoming = "INCOMING"
	DirectionOutgoing = "OUTGOING"
)

// Communication Status Constants
const (
	CommunicationStatusScheduled = "SCHEDULED"
	CommunicationStatusCompleted = "COMPLETED"
	CommunicationStatusCancelled = "CANCELLED"
	CommunicationStatusFollowUp  = "FOLLOW_UP"
)

// Meeting Type Constants
const (
	MeetingTypeParentTeacherConference = "PARENT_TEACHER_CONFERENCE"
	MeetingTypeIEPMeeting              = "IEP_MEETING"
	MeetingTypeBehaviorDiscussion      = "BEHAVIOR_DISCUSSION"
	MeetingTypeAcademicReview          = "ACADEMIC_REVIEW"
)

// Meeting Status Constants
const (
	MeetingStatusScheduled = "SCHEDULED"
	MeetingStatusConfirmed = "CONFIRMED"
	MeetingStatusCompleted = "COMPLETED"
	MeetingStatusCancelled = "CANCELLED"
	MeetingStatusNoShow    = "NO_SHOW"
)

// Attendance Status Constants
const (
	AttendanceStatusAttended    = "ATTENDED"
	AttendanceStatusNoShow      = "NO_SHOW"
	AttendanceStatusRescheduled = "RESCHEDULED"
)

// Activity Type Constants
const (
	ActivityTypeVolunteer       = "VOLUNTEER"
	ActivityTypeEventAttendance = "EVENT_ATTENDANCE"
	ActivityTypeHomeworkSupport = "HOMEWORK_SUPPORT"
	ActivityTypeSchoolVisit     = "SCHOOL_VISIT"
	ActivityTypeWorkshop        = "WORKSHOP"
)

// Impact Rating Constants
const (
	ImpactRatingLow    = "LOW"
	ImpactRatingMedium = "MEDIUM"
	ImpactRatingHigh   = "HIGH"
)

// ParentPartnership represents the parent-teacher partnership record
type ParentPartnership struct {
	ID                      uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID               uuid.UUID  `gorm:"type:uuid;not null" json:"student_id"`
	ParentID                *uuid.UUID `gorm:"type:uuid" json:"parent_id"`
	PartnershipType         string     `gorm:"type:varchar(50);not null" json:"partnership_type"`
	Relationship            string     `gorm:"type:varchar(50);not null" json:"relationship"`
	ContactPrimary          string     `gorm:"type:varchar(20);not null" json:"contact_primary"`
	ContactSecondary        string     `gorm:"type:varchar(20)" json:"contact_secondary"`
	Email                   string     `gorm:"type:varchar(100)" json:"email"`
	Address                 string     `gorm:"type:text" json:"address"`
	CommunicationPreference string     `gorm:"type:varchar(50);default:PHONE" json:"communication_preference"`
	InvolvementLevel        string     `gorm:"type:varchar(20);default:MODERATE" json:"involvement_level"`
	Notes                   string     `gorm:"type:text" json:"notes"`
	IsActive                bool       `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (ParentPartnership) TableName() string {
	return "master_parent_partnership"
}

// ParentCommunication represents communication logs between teachers and parents
type ParentCommunication struct {
	ID                uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	PartnershipID     uuid.UUID  `gorm:"type:uuid;not null" json:"partnership_id"`
	TeacherID         uuid.UUID  `gorm:"type:uuid;not null" json:"teacher_id"`
	CommunicationType string     `gorm:"type:varchar(50);not null" json:"communication_type"`
	CommunicationDate time.Time  `gorm:"type:timestamp;not null;default:CURRENT_TIMESTAMP" json:"communication_date"`
	Subject           string     `gorm:"type:varchar(200)" json:"subject"`
	Content           string     `gorm:"type:text;not null" json:"content"`
	Direction         string     `gorm:"type:varchar(20);not null" json:"direction"`
	Status            string     `gorm:"type:varchar(20);default:COMPLETED" json:"status"`
	FollowUpRequired  bool       `gorm:"default:false" json:"follow_up_required"`
	FollowUpDate      *time.Time `gorm:"type:timestamp" json:"follow_up_date"`
	ResponseReceived  bool       `gorm:"default:false" json:"response_received"`
	ResponseDate      *time.Time `gorm:"type:timestamp" json:"response_date"`
	Notes             string     `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (ParentCommunication) TableName() string {
	return "trx_parent_communication"
}

// ParentMeeting represents scheduled parent-teacher meetings
type ParentMeeting struct {
	ID               uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	PartnershipID    uuid.UUID  `gorm:"type:uuid;not null" json:"partnership_id"`
	TeacherID        uuid.UUID  `gorm:"type:uuid;not null" json:"teacher_id"`
	MeetingType      string     `gorm:"type:varchar(50);not null" json:"meeting_type"`
	ScheduledDate    time.Time  `gorm:"type:timestamp;not null" json:"scheduled_date"`
	DurationMinutes  int        `gorm:"default:30" json:"duration_minutes"`
	Location         string     `gorm:"type:varchar(100);default:SCHOOL" json:"location"`
	Agenda           string     `gorm:"type:text" json:"agenda"`
	Status           string     `gorm:"type:varchar(20);default:SCHEDULED" json:"status"`
	AttendanceStatus string     `gorm:"type:varchar(20)" json:"attendance_status"`
	Summary          string     `gorm:"type:text" json:"summary"`
	ActionItems      []string   `gorm:"type:text[]" json:"action_items"`
	NextMeetingDate  *time.Time `gorm:"type:timestamp" json:"next_meeting_date"`

	common.Auditable
}

func (ParentMeeting) TableName() string {
	return "trx_parent_meeting"
}

// PartnershipActivity tracks parent involvement activities
type PartnershipActivity struct {
	ID               uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	PartnershipID    uuid.UUID `gorm:"type:uuid;not null" json:"partnership_id"`
	ActivityType     string    `gorm:"type:varchar(50);not null" json:"activity_type"`
	ActivityDate     time.Time `gorm:"type:date;not null" json:"activity_date"`
	Description      string    `gorm:"type:text" json:"description"`
	HoursContributed *float64  `gorm:"type:numeric(4,2)" json:"hours_contributed"`
	ImpactRating     string    `gorm:"type:varchar(20)" json:"impact_rating"`
	Notes            string    `gorm:"type:text" json:"notes"`

	common.Auditable
}

func (PartnershipActivity) TableName() string {
	return "trx_partnership_activity"
}
