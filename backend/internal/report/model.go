package report

import (
	"sim-sekolah/internal/classroom"
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/student"
	"sim-sekolah/internal/subject"

	"github.com/google/uuid"
)

// ============================================================
// ENTITIES
// ============================================================

type Report struct {
	ID                   uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ClassroomID          uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_report_class_student_sem" json:"classroom_id"`
	StudentID            uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_report_class_student_sem;index" json:"student_id"`
	Semester             string    `gorm:"type:varchar(10);not null;uniqueIndex:idx_report_class_student_sem" json:"semester"`
	HomeroomNotes        string    `gorm:"type:text" json:"homeroom_notes"`
	StudentReflection    string    `gorm:"type:text" json:"student_reflection"`
	AcademicNarrativeAI  string    `gorm:"type:text" json:"academic_narrative_ai"`
	CharacterNarrativeAI string    `gorm:"type:text" json:"character_narrative_ai"`
	Status               string    `gorm:"type:varchar(20);default:'DRAFT'" json:"status"` // DRAFT, FINAL
	IsFinalized          bool      `gorm:"type:boolean;default:false" json:"is_finalized"`

	common.Auditable

	// Relasi
	Classroom       *classroom.Classroom    `gorm:"foreignKey:ClassroomID" json:"classroom,omitempty"`
	Student         *student.MasterStudent  `gorm:"foreignKey:StudentID" json:"student,omitempty"`
	Scores          []ReportScore           `gorm:"foreignKey:ReportID" json:"scores,omitempty"`
	P5              []ReportP5              `gorm:"foreignKey:ReportID" json:"p5,omitempty"`
	DeepLearning    []ReportDeepLearning    `gorm:"foreignKey:ReportID" json:"deep_learning,omitempty"`
	Extracurricular []ReportExtracurricular `gorm:"foreignKey:ReportID" json:"extracurriculars,omitempty"`
	Attendance      *ReportAttendance       `gorm:"foreignKey:ReportID" json:"attendance,omitempty"`
}

func (Report) TableName() string {
	return "trx_report"
}

type ReportScore struct {
	ID                         uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ReportID                   uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_report_subject" json:"report_id"`
	SubjectID                  uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_report_subject" json:"subject_id"`
	FinalScore                 float64   `gorm:"type:numeric(5,2);default:0" json:"final_score"`
	CompetencyAchieved         string    `gorm:"type:text" json:"competency_achieved"`
	CompetencyNeedsImprovement string    `gorm:"type:text" json:"competency_needs_improvement"`

	common.Auditable

	Subject *subject.Subject `gorm:"foreignKey:SubjectID" json:"subject,omitempty"`
}

func (ReportScore) TableName() string {
	return "trx_report_score"
}

type ReportP5 struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ReportID    uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_report_p5_theme" json:"report_id"`
	Theme       string    `gorm:"type:varchar(255);not null;uniqueIndex:idx_report_p5_theme" json:"theme"`
	Description string    `gorm:"type:text" json:"description"`
	Predicate   string    `gorm:"type:varchar(50)" json:"predicate"`

	common.Auditable
}

func (ReportP5) TableName() string { return "trx_report_p5" }

type ReportDeepLearning struct {
	ID               uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ReportID         uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_report_dl_aspect" json:"report_id"`
	Aspect           string    `gorm:"type:varchar(100);not null;uniqueIndex:idx_report_dl_aspect" json:"aspect"`
	ObservationNotes string    `gorm:"type:text" json:"observation_notes"`

	common.Auditable
}

func (ReportDeepLearning) TableName() string {
	return "trx_report_deep_learning"
}

type ReportExtracurricular struct {
	ID           uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ReportID     uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_report_extra_activity" json:"report_id"`
	ActivityName string    `gorm:"type:varchar(255);not null;uniqueIndex:idx_report_extra_activity" json:"activity_name"`
	Predicate    string    `gorm:"type:varchar(50)" json:"predicate"`
	Description  string    `gorm:"type:text" json:"description"`

	common.Auditable
}

func (ReportExtracurricular) TableName() string {
	return "trx_report_extracurricular"
}

type ReportAttendance struct {
	ID         uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ReportID   uuid.UUID `gorm:"type:uuid;not null;uniqueIndex" json:"report_id"`
	Sick       int       `gorm:"type:int;default:0" json:"sick"`
	Permission int       `gorm:"type:int;default:0" json:"permission"`
	Unexcused  int       `gorm:"type:int;default:0" json:"unexcused"`

	common.Auditable
}

func (ReportAttendance) TableName() string {
	return "trx_report_attendance"
}
