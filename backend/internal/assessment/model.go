package assessment

import (
	"time"

	"sim-sekolah/internal/classroom"
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/student"
	"sim-sekolah/internal/teaching_assignment"

	"github.com/google/uuid"
)

type Assessment struct {
	ID                   uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	TeachingAssignmentID uuid.UUID `gorm:"type:uuid;not null" json:"teaching_assignment_id"`
	AssessmentName       string    `gorm:"type:varchar(100);not null" json:"assessment_name"`
	AssessmentType       string    `gorm:"type:varchar(20);not null" json:"assessment_type"` // Formatif, Sumatif, Proyek, UTS, UAS
	AssessmentDate       time.Time `gorm:"type:date;not null" json:"assessment_date"`
	CreatedAt            time.Time `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`

	// Relasi
	TeachingAssignment *teaching_assignment.TeachingAssignment `gorm:"foreignKey:TeachingAssignmentID" json:"teaching_assignment,omitempty"`
	Scores             []AssessmentScore                       `gorm:"foreignKey:AssessmentID" json:"scores,omitempty"`
}

func (Assessment) TableName() string {
	return "trx_assessment"
}

type AssessmentScore struct {
	ID           uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	AssessmentID uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_assessment_student" json:"assessment_id"`
	StudentID    uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_assessment_student" json:"student_id"`
	Score        float64   `gorm:"type:numeric(5,2);default:0" json:"score"`
	Notes        string    `gorm:"type:text" json:"notes"` // Narasi umpan balik

	// Relasi
	Student *student.Student `gorm:"foreignKey:StudentID" json:"student,omitempty"`
}

func (AssessmentScore) TableName() string {
	return "trx_assessment_score"
}

// QuestionBank (Bank Soal)
type QuestionBank struct {
	ID       uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ModuleID uuid.UUID `gorm:"type:uuid;not null" json:"module_id"`
	Question string    `gorm:"type:text;not null" json:"question"`
	LevelID  uuid.UUID `gorm:"type:uuid;not null" json:"level_id"`       // FK to dl_assessment_level
	Tingkat  string    `gorm:"type:varchar(10);not null" json:"tingkat"` // LOTS, HOTS

	common.Auditable
}

func (QuestionBank) TableName() string {
	return "trx_question_bank"
}

// AssessmentP5 stores character scores using rubric scale
type AssessmentP5 struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID   uuid.UUID `gorm:"type:uuid;not null;index" json:"student_id"`
	ProjectID   uuid.UUID `gorm:"type:uuid;not null" json:"project_id"` // Modul Projek
	DimensionID uuid.UUID `gorm:"type:uuid;not null" json:"dimension_id"`
	Capaian     string    `gorm:"type:varchar(50);not null" json:"capaian"` // MB, SB, BSH, SAB

	common.Auditable

	Student *student.Student `gorm:"foreignKey:StudentID" json:"student,omitempty"`
}

func (AssessmentP5) TableName() string {
	return "trx_assessment_p5"
}

// Attendance (Absensi Siswa)
type Attendance struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID   uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_attendance" json:"student_id"`
	ClassroomID uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_attendance" json:"classroom_id"`
	Semester    string    `gorm:"type:varchar(10);not null;uniqueIndex:idx_attendance" json:"semester"`
	Sick        int       `gorm:"default:0" json:"sick"`
	Permission  int       `gorm:"default:0" json:"permission"`
	Unexcused   int       `gorm:"default:0" json:"unexcused"`

	common.Auditable
}

func (Attendance) TableName() string {
	return "trx_attendance"
}

// DailyAttendance (Absensi Harian Siswa)
type DailyAttendance struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ClassroomID uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_daily_attendance" json:"classroom_id"`
	StudentID   uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_daily_attendance" json:"student_id"`
	Date        time.Time `gorm:"type:date;not null;uniqueIndex:idx_daily_attendance" json:"date"`
	Status      string    `gorm:"type:varchar(20);not null" json:"status"` // HADIR, SAKIT, IZIN, ALPA
	Notes       string    `gorm:"type:text" json:"notes,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`

	Classroom *classroom.Classroom `gorm:"foreignKey:ClassroomID" json:"classroom,omitempty"`
	Student   *student.Student     `gorm:"foreignKey:StudentID" json:"student,omitempty"`
}

func (DailyAttendance) TableName() string {
	return "trx_daily_attendance"
}

// AcademicScore (Detailed score per question)
type AcademicScore struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID      uuid.UUID `gorm:"type:uuid;not null;index" json:"student_id"`
	QuestionID     uuid.UUID `gorm:"type:uuid;not null" json:"question_id"`
	AssessmentType string    `gorm:"type:varchar(20);not null" json:"assessment_type"` // FORMATIF, SUMATIF
	Score          float64   `gorm:"type:numeric(5,2);default:0" json:"score"`

	common.Auditable

	Student  *student.Student `gorm:"foreignKey:StudentID" json:"student,omitempty"`
	Question *QuestionBank    `gorm:"foreignKey:QuestionID" json:"question,omitempty"`
}

func (AcademicScore) TableName() string {
	return "trx_academic_score"
}
