package teacher

import (
	"time"

	"github.com/google/uuid"
)

type Teacher struct {
	ID       uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID uuid.UUID `gorm:"type:uuid;not null" json:"school_id"`

	// ============================================================
	// 1. IDENTITAS GURU
	// ============================================================
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

	// ============================================================
	// 2. KONTAK & ALAMAT
	// ============================================================
	FullAddress string `gorm:"type:text" json:"full_address"`
	Hamlet      string `gorm:"type:varchar(100)" json:"hamlet"`   // Dusun/Jalan
	RTRW        string `gorm:"type:varchar(10)" json:"rt_rw"`     // contoh: 001/002
	Village     string `gorm:"type:varchar(100)" json:"village"`  // Desa/Kelurahan
	District    string `gorm:"type:varchar(100)" json:"district"` // Kecamatan
	Regency     string `gorm:"type:varchar(100)" json:"regency"`  // Kabupaten/Kota
	Province    string `gorm:"type:varchar(100)" json:"province"`
	PostalCode  string `gorm:"type:varchar(10)" json:"postal_code"`
	Phone       string `gorm:"type:varchar(30)" json:"phone"`
	Email       string `gorm:"type:varchar(100)" json:"email"`

	// ============================================================
	// 3. DATA KEPEGAWAIAN
	// ============================================================
	NIP                string     `gorm:"type:varchar(30)" json:"nip"`
	EmploymentStatus   string     `gorm:"type:varchar(20)" json:"employment_status"`   // PNS, PPPK, Honorer, GTY
	StartTeachingDate  *time.Time `gorm:"type:date" json:"start_teaching_date"`        // TMT Mengajar
	AppointmentDecree  string     `gorm:"type:varchar(100)" json:"appointment_decree"` // SK Pengangkatan
	SalarySource       string     `gorm:"type:varchar(50)" json:"salary_source"`
	TeachingSubject    string     `gorm:"type:varchar(255)" json:"teaching_subject"`    // Mata pelajaran diampu
	AdditionalPosition string     `gorm:"type:varchar(100)" json:"additional_position"` // Jabatan tambahan
	TeachingHours      int        `gorm:"type:smallint;default:0" json:"teaching_hours"`
	IsActive           bool       `gorm:"type:boolean;default:true" json:"is_active"`

	// ============================================================
	// 4. PENDIDIKAN FORMAL & SERTIFIKASI
	// ============================================================
	LastEducation     string `gorm:"type:varchar(20)" json:"last_education"` // S1, S2, dll
	Major             string `gorm:"type:varchar(100)" json:"major"`         // Jurusan
	UniversityName    string `gorm:"type:varchar(255)" json:"university_name"`
	GraduationYear    int    `gorm:"type:smallint" json:"graduation_year"`
	IsCertified       bool   `gorm:"type:boolean;default:false" json:"is_certified"`
	CertificateNumber string `gorm:"type:varchar(50)" json:"certificate_number"`

	// ============================================================
	// 5. NARASI PEMBELAJARAN MENDALAM (AI)
	// ============================================================
	TeachingPreference string `gorm:"type:text" json:"teaching_preference"`

	CreatedAt time.Time `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"created_at"`
}

func (Teacher) TableName() string {
	return "master_teacher"
}
