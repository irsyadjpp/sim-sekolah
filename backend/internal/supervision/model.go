package supervision

import (
	"time"

	"github.com/lib/pq"

	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

// SupervisionCycle Status Constants
const (
	SupervisionCycleStatusPlanned   = "PLANNED"
	SupervisionCycleStatusActive    = "ACTIVE"
	SupervisionCycleStatusCompleted = "COMPLETED"
	SupervisionCycleStatusCancelled = "CANCELLED"
)

// Observation Type Constants
const (
	ObservationTypeClassroom     = "CLASSROOM"
	ObservationTypeLessonPlan    = "LESSON_PLAN"
	ObservationTypeDocumentation = "DOCUMENTATION"
	ObservationTypeStudentWork   = "STUDENT_WORK"
)

// Observation Status Constants
const (
	ObservationStatusScheduled  = "SCHEDULED"
	ObservationStatusInProgress = "IN_PROGRESS"
	ObservationStatusCompleted  = "COMPLETED"
	ObservationStatusCancelled  = "CANCELLED"
)

// Feedback Status Constants
const (
	FeedbackStatusDraft     = "DRAFT"
	FeedbackStatusSubmitted = "SUBMITTED"
	FeedbackStatusReviewed  = "REVIEWED"
	FeedbackStatusAccepted  = "ACCEPTED"
)

// SupervisionCycle represents a supervision cycle
type SupervisionCycle struct {
	ID               uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	CycleName        string         `gorm:"type:varchar(100);not null" json:"cycle_name"`
	AcademicYearID   uuid.UUID      `gorm:"type:uuid;not null" json:"academic_year_id"`
	SchoolID         uuid.UUID      `gorm:"type:uuid;not null" json:"school_id"`
	StartDate        time.Time      `gorm:"type:date;not null" json:"start_date"`
	EndDate          time.Time      `gorm:"type:date;not null" json:"end_date"`
	Status           string         `gorm:"type:varchar(20);default:PLANNED" json:"status"`
	Description      string         `gorm:"type:text" json:"description"`
	SupervisorID     uuid.UUID      `gorm:"type:uuid;not null" json:"supervisor_id"`
	Goals            pq.StringArray `gorm:"type:jsonb" json:"goals"`
	ExpectedOutcomes pq.StringArray `gorm:"type:jsonb" json:"expected_outcomes"`
	IsActive         bool           `gorm:"default:true" json:"is_active"`

	common.Auditable
}

func (SupervisionCycle) TableName() string {
	return "supervision_cycles"
}

// TeacherObservation represents classroom observations
type TeacherObservation struct {
	ID                  uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SupervisionCycleID  *uuid.UUID     `gorm:"type:uuid" json:"supervision_cycle_id"`
	TeacherID           uuid.UUID      `gorm:"type:uuid;not null" json:"teacher_id"`
	ObserverID          uuid.UUID      `gorm:"type:uuid;not null" json:"observer_id"`
	SubjectID           *uuid.UUID     `gorm:"type:uuid" json:"subject_id"`
	ClassroomID         *uuid.UUID     `gorm:"type:uuid" json:"classroom_id"`
	ObservationDate     time.Time      `gorm:"type:date;not null" json:"observation_date"`
	ObservationType     string         `gorm:"type:varchar(50);default:CLASSROOM" json:"observation_type"`
	Status              string         `gorm:"type:varchar(20);default:SCHEDULED" json:"status"`
	StartTime           *time.Time     `gorm:"type:timestamp" json:"start_time"`
	EndTime             *time.Time     `gorm:"type:timestamp" json:"end_time"`
	LessonTopic         string         `gorm:"type:varchar(200)" json:"lesson_topic"`
	ClassGrade          string         `gorm:"type:varchar(50)" json:"class_grade"`
	Strengths           pq.StringArray `gorm:"type:jsonb" json:"strengths"`
	AreasForImprovement pq.StringArray `gorm:"type:jsonb" json:"areas_for_improvement"`
	Notes               string         `gorm:"type:text" json:"notes"`
	Score               *float64       `gorm:"type:numeric(3,2)" json:"score"`
	MaxScore            float64        `gorm:"default:100.0" json:"max_score"`

	common.Auditable
}

func (TeacherObservation) TableName() string {
	return "teacher_observations"
}

// SupervisionFeedback represents feedback given to teachers
type SupervisionFeedback struct {
	ID                 uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ObservationID      uuid.UUID      `gorm:"type:uuid;not null" json:"observation_id"`
	TeacherID          uuid.UUID      `gorm:"type:uuid;not null" json:"teacher_id"`
	FeedbackDate       time.Time      `gorm:"type:date;not null;default:CURRENT_DATE" json:"feedback_date"`
	FeedbackProviderID uuid.UUID      `gorm:"type:uuid;not null" json:"feedback_provider_id"`
	Status             string         `gorm:"type:varchar(20);default:DRAFT" json:"status"`
	Strengths          pq.StringArray `gorm:"type:jsonb" json:"strengths"`
	ImprovementAreas   pq.StringArray `gorm:"type:jsonb" json:"improvement_areas"`
	Recommendations    pq.StringArray `gorm:"type:jsonb" json:"recommendations"`
	ActionPlan         string         `gorm:"type:text" json:"action_plan"`
	FollowUpDate       *time.Time     `gorm:"type:date" json:"follow_up_date"`
	TeacherResponse    string         `gorm:"type:text" json:"teacher_response"`
	ResponseDate       *time.Time     `gorm:"type:timestamp" json:"response_date"`
	IsAcknowledged     bool           `gorm:"default:false" json:"is_acknowledged"`
	OverallRating      *float64       `gorm:"type:numeric(3,2)" json:"overall_rating"`
	Comments           string         `gorm:"type:text" json:"comments"`

	common.Auditable
}

func (SupervisionFeedback) TableName() string {
	return "supervision_feedback"
}

// SupervisionAnalytics represents aggregated supervision analytics
type SupervisionAnalytics struct {
	ID                     uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID               uuid.UUID      `gorm:"type:uuid;not null" json:"school_id"`
	AcademicYearID         uuid.UUID      `gorm:"type:uuid;not null" json:"academic_year_id"`
	SupervisionCycleID     *uuid.UUID     `gorm:"type:uuid" json:"supervision_cycle_id"`
	AnalyticsDate          time.Time      `gorm:"type:date;not null;default:CURRENT_DATE" json:"analytics_date"`
	TotalObservations      int64          `gorm:"default:0" json:"total_observations"`
	CompletedObservations  int64          `gorm:"default:0" json:"completed_observations"`
	AverageScore           *float64       `gorm:"type:numeric(5,2)" json:"average_score"`
	TeachersSupervised     int64          `gorm:"default:0" json:"teachers_supervised"`
	ImprovementRate        *float64       `gorm:"type:numeric(5,2)" json:"improvement_rate"`
	FeedbackCompletionRate *float64       `gorm:"type:numeric(5,2)" json:"feedback_completion_rate"`
	TopStrengths           pq.StringArray `gorm:"type:jsonb" json:"top_strengths"`
	CommonImprovementAreas pq.StringArray `gorm:"type:jsonb" json:"common_improvement_areas"`

	common.Auditable
}

func (SupervisionAnalytics) TableName() string {
	return "supervision_analytics"
}
