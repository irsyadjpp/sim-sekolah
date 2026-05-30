package teacher

import (
	"sim-sekolah/internal/common"
	"time"

	"github.com/google/uuid"
)

// MasterTeacher - normalized basic teacher info
type MasterTeacher struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	SchoolID    uuid.UUID  `gorm:"type:uuid;not null" json:"school_id"`
	FullName    string     `gorm:"type:varchar(255);not null" json:"full_name"`
	Gender      string     `gorm:"type:char(1)" json:"gender"` // L / P
	BirthPlace  string     `gorm:"type:varchar(100)" json:"birth_place"`
	BirthDate   *time.Time `gorm:"type:date" json:"birth_date"`
	NIK         string     `gorm:"type:varchar(20);uniqueIndex" json:"nik"`
	NUPTK       string     `gorm:"type:varchar(20);uniqueIndex" json:"nuptk"`
	NIYNIGK     string     `gorm:"type:varchar(30)" json:"niy_nigk"` // Opsional swasta
	Religion    string     `gorm:"type:varchar(20)" json:"religion"` // Islam, Kristen, dll
	Nationality string     `gorm:"type:varchar(50);default:'WNI'" json:"nationality"`
	PhotoURL    string     `gorm:"type:text" json:"photo_url"`

	common.Auditable
}

func (MasterTeacher) TableName() string {
	return "master_teacher"
}

// TeacherContact - normalized contact and address data
type TeacherContact struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	TeacherID   uuid.UUID `gorm:"type:uuid;not null" json:"teacher_id"`
	FullAddress string    `gorm:"type:text" json:"full_address"`
	Hamlet      string    `gorm:"type:varchar(100)" json:"hamlet"`   // Dusun/Jalan
	RTRW        string    `gorm:"type:varchar(10)" json:"rt_rw"`     // contoh: 001/002
	Village     string    `gorm:"type:varchar(100)" json:"village"`  // Desa/Kelurahan
	District    string    `gorm:"type:varchar(100)" json:"district"` // Kecamatan
	Regency     string    `gorm:"type:varchar(100)" json:"regency"`  // Kabupaten/Kota
	Province    string    `gorm:"type:varchar(100)" json:"province"`
	PostalCode  string    `gorm:"type:varchar(10)" json:"postal_code"`
	Phone       string    `gorm:"type:varchar(30)" json:"phone"`
	Email       string    `gorm:"type:varchar(100)" json:"email"`

	common.Auditable
}

func (TeacherContact) TableName() string {
	return "teacher_contact"
}

// TeacherEmployment - normalized employment data
type TeacherEmployment struct {
	ID                 uuid.UUID  `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	TeacherID          uuid.UUID  `gorm:"type:uuid;not null" json:"teacher_id"`
	NIP                string     `gorm:"type:varchar(30)" json:"nip"`                 // NIP di TeacherEmployment sebagai data employment
	EmploymentStatus   string     `gorm:"type:varchar(20)" json:"employment_status"`   // PNS, PPPK, Honorer, GTY
	StartTeachingDate  *time.Time `gorm:"type:date" json:"start_teaching_date"`        // TMT Mengajar
	AppointmentDecree  string     `gorm:"type:varchar(100)" json:"appointment_decree"` // SK Pengangkatan
	SalarySource       string     `gorm:"type:varchar(50)" json:"salary_source"`
	TeachingSubject    string     `gorm:"type:varchar(255)" json:"teaching_subject"`    // Mata pelajaran diampu
	AdditionalPosition string     `gorm:"type:varchar(100)" json:"additional_position"` // Jabatan tambahan
	TeachingHours      int        `gorm:"type:smallint;default:0" json:"teaching_hours"`
	IsActive           bool       `gorm:"type:boolean;default:true" json:"is_active"`

	common.Auditable
}

func (TeacherEmployment) TableName() string {
	return "teacher_employment"
}

// TeacherEducation - normalized education data
type TeacherEducation struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	TeacherID      uuid.UUID `gorm:"type:uuid;not null" json:"teacher_id"`
	LastEducation  string    `gorm:"type:varchar(20)" json:"last_education"` // S1, S2, dll
	Major          string    `gorm:"type:varchar(100)" json:"major"`         // Jurusan
	UniversityName string    `gorm:"type:varchar(255)" json:"university_name"`
	GraduationYear int       `gorm:"type:smallint" json:"graduation_year"`

	common.Auditable
}

func (TeacherEducation) TableName() string {
	return "teacher_education"
}

// TeacherCertification - normalized certification data
type TeacherCertification struct {
	ID                 uuid.UUID  `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	TeacherID          uuid.UUID  `gorm:"type:uuid;not null" json:"teacher_id"`
	IsCertified        bool       `gorm:"type:boolean;default:false" json:"is_certified"`
	CertificateNumber  string     `gorm:"type:varchar(50)" json:"certificate_number"`
	CertificationDate  *time.Time `gorm:"type:date" json:"certification_date"`
	CertificationLevel string     `gorm:"type:varchar(100)" json:"certification_level"`

	common.Auditable
}

func (TeacherCertification) TableName() string {
	return "teacher_certification"
}

// TeacherPreference - normalized teaching preference (AI)
type TeacherPreference struct {
	ID                 uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	TeacherID          uuid.UUID `gorm:"type:uuid;not null" json:"teacher_id"`
	TeachingPreference string    `gorm:"type:text" json:"teaching_preference"`

	common.Auditable
}

func (TeacherPreference) TableName() string {
	return "teacher_preference"
}

// TeacherComplete - composite struct for API responses (all normalized tables combined)
type TeacherComplete struct {
	MasterTeacher
	TeacherContact
	TeacherEmployment
	TeacherEducation
	TeacherCertification
	TeacherPreference
}
