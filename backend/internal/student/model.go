package student

import (
	"sim-sekolah/internal/common"
	"time"

	"github.com/google/uuid"
)

type StudentStatus string

const (
	StatusApplicant StudentStatus = "applicant"
	StatusAccepted  StudentStatus = "accepted"
	StatusEnrolled  StudentStatus = "enrolled"
	StatusActive    StudentStatus = "active"
	StatusGraduated StudentStatus = "graduated"
	StatusAlumni    StudentStatus = "alumni"
	StatusWithdrawn StudentStatus = "withdrawn"
)

// MasterStudent - normalized basic student info
type MasterStudent struct {
	ID          uuid.UUID  `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	NIK         string     `gorm:"type:varchar(20);uniqueIndex" json:"nik"` // Nomor Induk Kependudukan
	SchoolID    uuid.UUID  `gorm:"type:uuid;not null" json:"school_id"`
	FullName    string     `gorm:"type:varchar(255);not null" json:"full_name"`
	Gender      string     `gorm:"type:char(1)" json:"gender"` // L / P
	BirthPlace  string     `gorm:"type:varchar(100)" json:"birth_place"`
	BirthDate   *time.Time `gorm:"type:date" json:"birth_date"`
	Religion    string     `gorm:"type:varchar(20)" json:"religion"`
	Nationality string     `gorm:"type:varchar(50);default:'WNI'" json:"nationality"`
	PhotoURL    string     `gorm:"type:text" json:"photo_url"`

	common.Auditable
}

func (MasterStudent) TableName() string {
	return "master_student"
}

// StudentContact - normalized contact and address data
type StudentContact struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	StudentID   uuid.UUID `gorm:"type:uuid;not null" json:"student_id"`
	FullAddress string    `gorm:"type:text" json:"full_address"`
	RTRW        string    `gorm:"type:varchar(10)" json:"rt_rw"`
	Village     string    `gorm:"type:varchar(100)" json:"village"`
	District    string    `gorm:"type:varchar(100)" json:"district"`
	Regency     string    `gorm:"type:varchar(100)" json:"regency"`
	Province    string    `gorm:"type:varchar(100)" json:"province"`
	PostalCode  string    `gorm:"type:varchar(10)" json:"postal_code"`
	Coordinates string    `gorm:"type:varchar(50)" json:"coordinates"` // lat,lng (opsional)

	common.Auditable
}

func (StudentContact) TableName() string {
	return "student_contact"
}

// StudentFamily - normalized family data
type StudentFamily struct {
	ID               uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	StudentID        uuid.UUID `gorm:"type:uuid;not null" json:"student_id"`
	ChildOrder       int       `gorm:"type:smallint;default:1" json:"child_order"` // Anak ke-
	Siblings         int       `gorm:"type:smallint;default:0" json:"siblings"`    // Jumlah saudara
	FamilyCardNumber string    `gorm:"type:varchar(20)" json:"family_card_number"` // Nomor KK
	BirthCertificate string    `gorm:"type:varchar(50)" json:"birth_certificate"`  // No. Akta Lahir
	KIPNumber        string    `gorm:"type:varchar(30)" json:"kip_number"`         // KIP/KKS/PKH

	common.Auditable
}

func (StudentFamily) TableName() string {
	return "student_family"
}

// StudentEnrollment - normalized enrollment and school status data
type StudentEnrollment struct {
	ID             uuid.UUID     `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	StudentID      uuid.UUID     `gorm:"type:uuid;not null" json:"student_id"`
	NIS            string        `gorm:"type:varchar(20)" json:"nis"`              // Nomor Induk Siswa lokal
	NISN           string        `gorm:"type:varchar(20);uniqueIndex" json:"nisn"` // Nasional
	EnrollmentYear int           `gorm:"type:smallint" json:"enrollment_year"`     // Tahun masuk
	Curriculum     string        `gorm:"type:varchar(50)" json:"curriculum"`       // Kurikulum
	StudentStatus  StudentStatus `gorm:"type:varchar(20);default:'active'" json:"student_status"`
	EntryPath      string        `gorm:"type:varchar(50)" json:"entry_path"`       // Jalur masuk (SPMB/Mutasi/dll)
	PreviousSchool string        `gorm:"type:varchar(255)" json:"previous_school"` // Asal sekolah
	ExamNumber     string        `gorm:"type:varchar(30)" json:"exam_number"`      // Nomor peserta ujian

	common.Auditable
}

func (StudentEnrollment) TableName() string {
	return "student_academic"
}

// StudentHealth - normalized health data
type StudentHealth struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	StudentID      uuid.UUID `gorm:"type:uuid;not null" json:"student_id"`
	BloodType      string    `gorm:"type:varchar(5)" json:"blood_type"`
	Height         float64   `gorm:"type:numeric(5,2);default:0" json:"height"` // cm
	Weight         float64   `gorm:"type:numeric(5,2);default:0" json:"weight"` // kg
	MedicalHistory string    `gorm:"type:text" json:"medical_history"`
	Disability     string    `gorm:"type:varchar(100)" json:"disability"` // Jenis disabilitas, kosong jika tidak ada

	common.Auditable
}

func (StudentHealth) TableName() string {
	return "student_medical"
}

// StudentComplete - composite struct for API responses (all normalized tables combined)
type StudentComplete struct {
	MasterStudent
	StudentContact
	StudentFamily
	StudentEnrollment
	StudentHealth
}

// StudentParent menyimpan data orang tua / wali siswa
type StudentParent struct {
	ID         uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	StudentID  uuid.UUID `gorm:"type:uuid;not null" json:"student_id"`
	ParentType string    `gorm:"type:varchar(10);not null" json:"parent_type"` // FATHER, MOTHER, GUARDIAN
	FullName   string    `gorm:"type:varchar(255)" json:"full_name"`
	NIK        string    `gorm:"type:varchar(20)" json:"nik"`
	Education  string    `gorm:"type:varchar(20)" json:"education"` // SD, SMP, SMA, S1, dll
	Occupation string    `gorm:"type:varchar(100)" json:"occupation"`
	Income     int64     `gorm:"type:bigint;default:0" json:"income"` // Per bulan (Rupiah)
	Phone      string    `gorm:"type:varchar(30)" json:"phone"`

	common.Auditable
}

func (StudentParent) TableName() string {
	return "master_student_parent"
}
