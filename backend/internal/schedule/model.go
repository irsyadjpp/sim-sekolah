package schedule

import (
	"time"

	"sim-sekolah/internal/classroom"
	"sim-sekolah/internal/teaching_assignment"

	"github.com/google/uuid"
)

type ClassSchedule struct {
	ID                   uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ClassroomID          uuid.UUID `gorm:"type:uuid;not null" json:"classroom_id"`
	TeachingAssignmentID uuid.UUID `gorm:"type:uuid;not null" json:"teaching_assignment_id"`
	DayOfWeek            int       `gorm:"type:smallint;not null" json:"day_of_week"`  // 1 = Monday, 7 = Sunday
	StartTime            string    `gorm:"type:varchar(5);not null" json:"start_time"` // "HH:MM"
	EndTime              string    `gorm:"type:varchar(5);not null" json:"end_time"`   // "HH:MM"
	CreatedAt            time.Time `json:"created_at"`
	UpdatedAt            time.Time `json:"updated_at"`

	// Relasi
	Classroom          *classroom.Classroom                    `gorm:"foreignKey:ClassroomID" json:"classroom,omitempty"`
	TeachingAssignment *teaching_assignment.TeachingAssignment `gorm:"foreignKey:TeachingAssignmentID" json:"teaching_assignment,omitempty"`
}

func (ClassSchedule) TableName() string {
	return "trx_class_schedule"
}
