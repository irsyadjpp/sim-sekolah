package parent_partnership

import (
	"context"

	"gorm.io/gorm"
)

type ParentPartnershipRepository interface {
	// ParentPartnership
	GetAll(ctx context.Context) ([]ParentPartnership, error)
	GetByID(ctx context.Context, id string) (*ParentPartnership, error)
	GetByStudentID(ctx context.Context, studentID string) ([]ParentPartnership, error)
	GetActiveByStudentID(ctx context.Context, studentID string) ([]ParentPartnership, error)
	Create(ctx context.Context, data *ParentPartnership) error
	Update(ctx context.Context, data *ParentPartnership) error
	Delete(ctx context.Context, id string) error

	// ParentCommunication
	GetAllCommunications(ctx context.Context) ([]ParentCommunication, error)
	GetCommunicationByID(ctx context.Context, id string) (*ParentCommunication, error)
	GetCommunicationsByPartnership(ctx context.Context, partnershipID string) ([]ParentCommunication, error)
	GetPendingFollowUps(ctx context.Context) ([]ParentCommunication, error)
	CreateCommunication(ctx context.Context, data *ParentCommunication) error
	UpdateCommunication(ctx context.Context, data *ParentCommunication) error
	DeleteCommunication(ctx context.Context, id string) error

	// ParentMeeting
	GetAllMeetings(ctx context.Context) ([]ParentMeeting, error)
	GetMeetingByID(ctx context.Context, id string) (*ParentMeeting, error)
	GetMeetingsByPartnership(ctx context.Context, partnershipID string) ([]ParentMeeting, error)
	GetMeetingsByTeacher(ctx context.Context, teacherID string) ([]ParentMeeting, error)
	GetScheduledMeetings(ctx context.Context) ([]ParentMeeting, error)
	CreateMeeting(ctx context.Context, data *ParentMeeting) error
	UpdateMeeting(ctx context.Context, data *ParentMeeting) error
	DeleteMeeting(ctx context.Context, id string) error

	// PartnershipActivity
	GetAllActivities(ctx context.Context) ([]PartnershipActivity, error)
	GetActivityByID(ctx context.Context, id string) (*PartnershipActivity, error)
	GetActivitiesByPartnership(ctx context.Context, partnershipID string) ([]PartnershipActivity, error)
	GetActivitiesByDateRange(ctx context.Context, startDate, endDate string) ([]PartnershipActivity, error)
	CreateActivity(ctx context.Context, data *PartnershipActivity) error
	UpdateActivity(ctx context.Context, data *PartnershipActivity) error
	DeleteActivity(ctx context.Context, id string) error

	// Summary
	GetPartnershipSummary(ctx context.Context) (*PartnershipSummaryResponse, error)
}

type parentPartnershipRepository struct {
	db *gorm.DB
}

func NewParentPartnershipRepository(db *gorm.DB) ParentPartnershipRepository {
	return &parentPartnershipRepository{db: db}
}

// ParentPartnership Methods
func (r *parentPartnershipRepository) GetAll(ctx context.Context) ([]ParentPartnership, error) {
	var partnerships []ParentPartnership
	err := r.db.WithContext(ctx).
		Where("deleted_at IS NULL").
		Order("created_at DESC").
		Find(&partnerships).Error
	return partnerships, err
}

func (r *parentPartnershipRepository) GetByID(ctx context.Context, id string) (*ParentPartnership, error) {
	var partnership ParentPartnership
	err := r.db.WithContext(ctx).
		Where("id = ? AND deleted_at IS NULL", id).
		First(&partnership).Error
	if err != nil {
		return nil, err
	}
	return &partnership, nil
}

func (r *parentPartnershipRepository) GetByStudentID(ctx context.Context, studentID string) ([]ParentPartnership, error) {
	var partnerships []ParentPartnership
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND deleted_at IS NULL", studentID).
		Order("partnership_type ASC").
		Find(&partnerships).Error
	return partnerships, err
}

func (r *parentPartnershipRepository) GetActiveByStudentID(ctx context.Context, studentID string) ([]ParentPartnership, error) {
	var partnerships []ParentPartnership
	err := r.db.WithContext(ctx).
		Where("student_id = ? AND is_active = true AND deleted_at IS NULL", studentID).
		Order("partnership_type ASC").
		Find(&partnerships).Error
	return partnerships, err
}

func (r *parentPartnershipRepository) Create(ctx context.Context, data *ParentPartnership) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *parentPartnershipRepository) Update(ctx context.Context, data *ParentPartnership) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *parentPartnershipRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&ParentPartnership{}, "id = ?", id).Error
}

// ParentCommunication Methods
func (r *parentPartnershipRepository) GetAllCommunications(ctx context.Context) ([]ParentCommunication, error) {
	var communications []ParentCommunication
	err := r.db.WithContext(ctx).
		Order("communication_date DESC").
		Find(&communications).Error
	return communications, err
}

func (r *parentPartnershipRepository) GetCommunicationByID(ctx context.Context, id string) (*ParentCommunication, error) {
	var communication ParentCommunication
	err := r.db.WithContext(ctx).
		Where("id = ?", id).
		First(&communication).Error
	if err != nil {
		return nil, err
	}
	return &communication, nil
}

func (r *parentPartnershipRepository) GetCommunicationsByPartnership(ctx context.Context, partnershipID string) ([]ParentCommunication, error) {
	var communications []ParentCommunication
	err := r.db.WithContext(ctx).
		Where("partnership_id = ?", partnershipID).
		Order("communication_date DESC").
		Find(&communications).Error
	return communications, err
}

func (r *parentPartnershipRepository) GetPendingFollowUps(ctx context.Context) ([]ParentCommunication, error) {
	var communications []ParentCommunication
	err := r.db.WithContext(ctx).
		Where("follow_up_required = true AND status != ?", "COMPLETED").
		Order("communication_date ASC").
		Find(&communications).Error
	return communications, err
}

func (r *parentPartnershipRepository) CreateCommunication(ctx context.Context, data *ParentCommunication) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *parentPartnershipRepository) UpdateCommunication(ctx context.Context, data *ParentCommunication) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *parentPartnershipRepository) DeleteCommunication(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&ParentCommunication{}, "id = ?", id).Error
}

// ParentMeeting Methods
func (r *parentPartnershipRepository) GetAllMeetings(ctx context.Context) ([]ParentMeeting, error) {
	var meetings []ParentMeeting
	err := r.db.WithContext(ctx).
		Order("scheduled_date DESC").
		Find(&meetings).Error
	return meetings, err
}

func (r *parentPartnershipRepository) GetMeetingByID(ctx context.Context, id string) (*ParentMeeting, error) {
	var meeting ParentMeeting
	err := r.db.WithContext(ctx).
		Where("id = ?", id).
		First(&meeting).Error
	if err != nil {
		return nil, err
	}
	return &meeting, nil
}

func (r *parentPartnershipRepository) GetMeetingsByPartnership(ctx context.Context, partnershipID string) ([]ParentMeeting, error) {
	var meetings []ParentMeeting
	err := r.db.WithContext(ctx).
		Where("partnership_id = ?", partnershipID).
		Order("scheduled_date DESC").
		Find(&meetings).Error
	return meetings, err
}

func (r *parentPartnershipRepository) GetMeetingsByTeacher(ctx context.Context, teacherID string) ([]ParentMeeting, error) {
	var meetings []ParentMeeting
	err := r.db.WithContext(ctx).
		Where("teacher_id = ?", teacherID).
		Order("scheduled_date ASC").
		Find(&meetings).Error
	return meetings, err
}

func (r *parentPartnershipRepository) GetScheduledMeetings(ctx context.Context) ([]ParentMeeting, error) {
	var meetings []ParentMeeting
	err := r.db.WithContext(ctx).
		Where("status IN ?", []string{"SCHEDULED", "CONFIRMED"}).
		Order("scheduled_date ASC").
		Find(&meetings).Error
	return meetings, err
}

func (r *parentPartnershipRepository) CreateMeeting(ctx context.Context, data *ParentMeeting) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *parentPartnershipRepository) UpdateMeeting(ctx context.Context, data *ParentMeeting) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *parentPartnershipRepository) DeleteMeeting(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&ParentMeeting{}, "id = ?", id).Error
}

// PartnershipActivity Methods
func (r *parentPartnershipRepository) GetAllActivities(ctx context.Context) ([]PartnershipActivity, error) {
	var activities []PartnershipActivity
	err := r.db.WithContext(ctx).
		Order("activity_date DESC").
		Find(&activities).Error
	return activities, err
}

func (r *parentPartnershipRepository) GetActivityByID(ctx context.Context, id string) (*PartnershipActivity, error) {
	var activity PartnershipActivity
	err := r.db.WithContext(ctx).
		Where("id = ?", id).
		First(&activity).Error
	if err != nil {
		return nil, err
	}
	return &activity, nil
}

func (r *parentPartnershipRepository) GetActivitiesByPartnership(ctx context.Context, partnershipID string) ([]PartnershipActivity, error) {
	var activities []PartnershipActivity
	err := r.db.WithContext(ctx).
		Where("partnership_id = ?", partnershipID).
		Order("activity_date DESC").
		Find(&activities).Error
	return activities, err
}

func (r *parentPartnershipRepository) GetActivitiesByDateRange(ctx context.Context, startDate, endDate string) ([]PartnershipActivity, error) {
	var activities []PartnershipActivity
	err := r.db.WithContext(ctx).
		Where("activity_date BETWEEN ? AND ?", startDate, endDate).
		Order("activity_date DESC").
		Find(&activities).Error
	return activities, err
}

func (r *parentPartnershipRepository) CreateActivity(ctx context.Context, data *PartnershipActivity) error {
	return r.db.WithContext(ctx).Create(data).Error
}

func (r *parentPartnershipRepository) UpdateActivity(ctx context.Context, data *PartnershipActivity) error {
	return r.db.WithContext(ctx).Save(data).Error
}

func (r *parentPartnershipRepository) DeleteActivity(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&PartnershipActivity{}, "id = ?", id).Error
}

// Summary Method
func (r *parentPartnershipRepository) GetPartnershipSummary(ctx context.Context) (*PartnershipSummaryResponse, error) {
	var summary PartnershipSummaryResponse

	// Count total partnerships
	var totalPartnerships int64
	r.db.WithContext(ctx).Table("master_parent_partnership").Where("deleted_at IS NULL").Count(&totalPartnerships)
	summary.TotalPartnerships = int(totalPartnerships)

	// Count active partnerships
	var activePartnerships int64
	r.db.WithContext(ctx).Table("master_parent_partnership").Where("is_active = true AND deleted_at IS NULL").Count(&activePartnerships)
	summary.ActivePartnerships = int(activePartnerships)

	// Count total communications
	var totalCommunications int64
	r.db.WithContext(ctx).Table("trx_parent_communication").Count(&totalCommunications)
	summary.TotalCommunications = int(totalCommunications)

	// Count pending follow-ups
	var pendingFollowUps int64
	r.db.WithContext(ctx).Table("trx_parent_communication").Where("follow_up_required = true AND status != ?", "COMPLETED").Count(&pendingFollowUps)
	summary.PendingFollowUps = int(pendingFollowUps)

	// Count scheduled meetings
	var scheduledMeetings int64
	r.db.WithContext(ctx).Table("trx_parent_meeting").Where("status IN ?", []string{"SCHEDULED", "CONFIRMED"}).Count(&scheduledMeetings)
	summary.ScheduledMeetings = int(scheduledMeetings)

	// Count completed meetings
	var completedMeetings int64
	r.db.WithContext(ctx).Table("trx_parent_meeting").Where("status = ?", "COMPLETED").Count(&completedMeetings)
	summary.CompletedMeetings = int(completedMeetings)

	// Count total activities
	var totalActivities int64
	r.db.WithContext(ctx).Table("trx_partnership_activity").Count(&totalActivities)
	summary.TotalActivities = int(totalActivities)

	// Sum volunteer hours
	r.db.WithContext(ctx).Table("trx_partnership_activity").Where("hours_contributed IS NOT NULL").Select("COALESCE(SUM(hours_contributed), 0)").Scan(&summary.TotalVolunteerHours)

	// Calculate average involvement level
	var avgLevel string
	r.db.WithContext(ctx).Table("master_parent_partnership").
		Where("deleted_at IS NULL").
		Select("CASE WHEN AVG(CASE involvement_level WHEN 'LOW' THEN 1 WHEN 'MODERATE' THEN 2 WHEN 'HIGH' THEN 3 WHEN 'VERY_HIGH' THEN 4 ELSE 2 END) < 2 THEN 'LOW' WHEN AVG(CASE involvement_level WHEN 'LOW' THEN 1 WHEN 'MODERATE' THEN 2 WHEN 'HIGH' THEN 3 WHEN 'VERY_HIGH' THEN 4 ELSE 2 END) < 3 THEN 'MODERATE' ELSE 'HIGH' END").
		Scan(&avgLevel)
	summary.AverageInvolvementLevel = avgLevel

	return &summary, nil
}
