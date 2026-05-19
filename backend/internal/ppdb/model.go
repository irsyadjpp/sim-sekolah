package ppdb

import (
	"time"

	"sim-sekolah/internal/academic_year"

	"github.com/google/uuid"
)

// ============================================================
// ENTITIES
// ============================================================

type AdmissionPath struct {
	ID          uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	Name        string    `gorm:"type:varchar(50);not null;unique" json:"name"`
	Description string    `gorm:"type:text" json:"description"`
	IsActive    bool      `gorm:"type:boolean;default:true" json:"is_active"`
}

func (AdmissionPath) TableName() string {
	return "trx_ppdb_admission_path"
}

type Applicant struct {
	ID              uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	RegistrationNo  string    `gorm:"type:varchar(50);not null;unique" json:"registration_no"`
	SchoolYearID    uuid.UUID `gorm:"type:uuid;not null" json:"school_year_id"`
	AdmissionPathID uuid.UUID `gorm:"type:uuid;not null" json:"admission_path_id"`

	// Identitas
	FullName   string    `gorm:"type:varchar(150);not null" json:"full_name"`
	NIK        string    `gorm:"type:varchar(16);not null;unique" json:"nik"`
	NISN       string    `gorm:"type:varchar(20)" json:"nisn"`
	BirthPlace string    `gorm:"type:varchar(100);not null" json:"birth_place"`
	BirthDate  time.Time `gorm:"type:date;not null" json:"birth_date"`
	Gender     string    `gorm:"type:varchar(1);not null" json:"gender"`
	Religion   string    `gorm:"type:varchar(20);not null" json:"religion"`

	// Alamat
	Address            string  `gorm:"type:text;not null" json:"address"`
	Village            string  `gorm:"type:varchar(100)" json:"village"`
	District           string  `gorm:"type:varchar(100)" json:"district"`
	Regency            string  `gorm:"type:varchar(100)" json:"regency"`
	Province           string  `gorm:"type:varchar(100)" json:"province"`
	PostalCode         string  `gorm:"type:varchar(10)" json:"postal_code"`
	DistanceToSchoolKm float64 `gorm:"type:numeric(5,2)" json:"distance_to_school_km"`

	Status     string     `gorm:"type:varchar(50);default:'Submitted'" json:"status"`
	AcceptedAt *time.Time `gorm:"type:timestamp" json:"accepted_at"`
	CreatedAt  time.Time  `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`

	// Relations
	SchoolYear    *academic_year.AcademicYear `gorm:"foreignKey:SchoolYearID" json:"school_year,omitempty"`
	AdmissionPath *AdmissionPath              `gorm:"foreignKey:AdmissionPathID" json:"admission_path,omitempty"`
	Parents       *ApplicantParent            `gorm:"foreignKey:ApplicantID" json:"parents,omitempty"`
	Documents     []ApplicantDocument         `gorm:"foreignKey:ApplicantID" json:"documents,omitempty"`
}

func (Applicant) TableName() string { return "trx_ppdb_applicant" }

type ApplicantParent struct {
	ID               uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ApplicantID      uuid.UUID `gorm:"type:uuid;not null;uniqueIndex" json:"applicant_id"`
	FatherName       string    `gorm:"type:varchar(150)" json:"father_name"`
	FatherNIK        string    `gorm:"type:varchar(16)" json:"father_nik"`
	FatherOccupation string    `gorm:"type:varchar(100)" json:"father_occupation"`
	MotherName       string    `gorm:"type:varchar(150)" json:"mother_name"`
	MotherNIK        string    `gorm:"type:varchar(16)" json:"mother_nik"`
	MotherOccupation string    `gorm:"type:varchar(100)" json:"mother_occupation"`
	PhoneNumber      string    `gorm:"type:varchar(20);not null" json:"phone_number"`
}

func (ApplicantParent) TableName() string { return "trx_ppdb_parent" }

type ApplicantDocument struct {
	ID           uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ApplicantID  uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:idx_app_doc" json:"applicant_id"`
	DocumentType string    `gorm:"type:varchar(50);not null;uniqueIndex:idx_app_doc" json:"document_type"` // KK, AKTA, dll
	FilePath     string    `gorm:"type:text;not null" json:"file_path"`                                    // RustFS path
	UploadedAt   time.Time `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"uploaded_at"`
}

func (ApplicantDocument) TableName() string { return "trx_ppdb_document" }

type VerificationLog struct {
	ID              uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	ApplicantID     uuid.UUID `gorm:"type:uuid;not null" json:"applicant_id"`
	VerifiedBy      uuid.UUID `gorm:"type:uuid" json:"verified_by"`
	StatusChangedTo string    `gorm:"type:varchar(50);not null" json:"status_changed_to"`
	Notes           string    `gorm:"type:text" json:"notes"`
	CreatedAt       time.Time `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`
}

func (VerificationLog) TableName() string { return "trx_ppdb_verification_log" }

type PPDBAcademicYear struct {
	ID       uuid.UUID `gorm:"primaryKey" json:"id"`
	YearName string    `gorm:"column:year_name" json:"year_name"`
	Semester string    `gorm:"column:semester" json:"semester"`
	IsActive bool      `gorm:"column:is_active" json:"is_active"`
}

func (PPDBAcademicYear) TableName() string {
	return "master_academic_year"
}
