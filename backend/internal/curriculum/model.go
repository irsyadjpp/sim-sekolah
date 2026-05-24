package curriculum

import (
	"time"

	"github.com/google/uuid"

	"sim-sekolah/internal/academic_year"
	"sim-sekolah/internal/common"
	"sim-sekolah/internal/school"
)

// Curriculum Types
const (
	CurriculumTypeIntrakurikuler  = "INTRAKURIKULER"  // Intra-curricular
	CurriculumTypeKokurikuler     = "KOKURIKULER"     // Co-curricular
	CurriculumTypeEkstrakurikuler = "EKSTRAKURIKULER" // Extra-curricular
)

// GetCurriculumTypeDescription returns Indonesian description of curriculum type
func GetCurriculumTypeDescription(curriculumType string) string {
	descriptions := map[string]string{
		CurriculumTypeIntrakurikuler:  "Intrakurikuler (Kegiatan Kurikuler Utama)",
		CurriculumTypeKokurikuler:     "Kokurikuler (Kegiatan Pendukung Kurikulum)",
		CurriculumTypeEkstrakurikuler: "Ekstrakurikuler (Kegiatan di luar Kurikulum)",
	}
	return descriptions[curriculumType]
}

const (
	CurriculumClassificationKumer       = "KUMER"
	CurriculumClassificationK13         = "K13"
	CurriculumClassificationMuatanLokal = "MUATAN_LOKAL"
)

// IsValidCurriculumClassification validates curriculum classification
func IsValidCurriculumClassification(classification string) bool {
	validClasses := map[string]bool{
		CurriculumClassificationKumer:       true,
		CurriculumClassificationK13:         true,
		CurriculumClassificationMuatanLokal: true,
	}
	return validClasses[classification]
}

// IsValidCurriculumType validates curriculum type
func IsValidCurriculumType(curriculumType string) bool {
	validTypes := map[string]bool{
		CurriculumTypeIntrakurikuler:  true,
		CurriculumTypeKokurikuler:     true,
		CurriculumTypeEkstrakurikuler: true,
	}
	return validTypes[curriculumType]
}

type CurriculumDocument struct {
	ID                       uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	AcademicYearID           uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:uni_curriculum_school_year" json:"academic_year_id"`
	SchoolID                 uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:uni_curriculum_school_year" json:"school_id"`
	CurriculumType           string    `gorm:"type:varchar(20);not null;default:'INTRAKURIKULER'" json:"curriculum_type"` // INTRAKURIKULER, KOKURIKULER, EKSTRAKURIKULER
	CurriculumClassification string    `gorm:"type:varchar(30);default:'KUMER'" json:"curriculum_classification"`         // KUMER, K13, MUATAN_LOKAL
	Status                   string    `gorm:"type:varchar(20);default:'DRAFT';not null" json:"status"`                   // DRAFT, REVIEW, FINAL
	CreatedAt                time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt                time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"updated_at"`

	// Relasi
	AcademicYear *academic_year.AcademicYear `gorm:"foreignKey:AcademicYearID" json:"academic_year,omitempty"`
	School       *school.School              `gorm:"foreignKey:SchoolID" json:"school,omitempty"`
	Chapters     []CurriculumChapter         `gorm:"foreignKey:CurriculumDocumentID;constraint:OnDelete:CASCADE" json:"chapters,omitempty"`
}

func (CurriculumDocument) TableName() string {
	return "trx_curriculum_document"
}

type CurriculumChapter struct {
	ID                   uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	CurriculumDocumentID uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:uni_curriculum_doc_chapter" json:"curriculum_document_id"`
	ChapterNumber        int       `gorm:"type:int2;not null;uniqueIndex:uni_curriculum_doc_chapter" json:"chapter_number"`
	Title                string    `gorm:"type:varchar(150);not null" json:"title"`
	Content              string    `gorm:"type:text" json:"content"`
	UpdatedAt            time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"updated_at"`
}

func (CurriculumChapter) TableName() string {
	return "trx_curriculum_chapter"
}

type ReadinessData struct {
	SchoolID                     uuid.UUID `gorm:"column:school_id" json:"school_id"`
	SchoolName                   string    `gorm:"column:school_name" json:"school_name"`
	PersentaseProfilDasar        float64   `gorm:"column:persentase_profil_dasar" json:"-"`
	PersentaseDataGuru           float64   `gorm:"column:persentase_data_guru" json:"-"`
	PersentaseDataSiswa          float64   `gorm:"column:persentase_data_siswa" json:"-"`
	PersentaseKarakteristikLokal float64   `gorm:"column:persentase_karakteristik_lokal" json:"-"`
}

func (ReadinessData) TableName() string {
	return "vw_dashboard_operator_kelengkapan_data"
}

// KokurikulerActivity represents co-curricular activities
type KokurikulerActivity struct {
	ID                   uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	CurriculumDocumentID uuid.UUID `gorm:"column:curriculum_document_id;not null" json:"curriculum_document_id"`
	ActivityName         string    `gorm:"column:activity_name;not null" json:"activity_name"`
	LinkedSubjectID      uuid.UUID `gorm:"column:linked_subject_id" json:"linked_subject_id"`
	Description          string    `gorm:"column:description;type:text" json:"description"`
	Schedule             string    `gorm:"column:schedule;type:text" json:"schedule"`
	IsActive             bool      `gorm:"column:is_active;default:true" json:"is_active"`

	common.Auditable
}

func (KokurikulerActivity) TableName() string {
	return "trx_kokurikuler_activity"
}

// EkstrakurikulerActivity represents extra-curricular activities
type EkstrakurikulerActivity struct {
	ID                   uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	CurriculumDocumentID uuid.UUID `gorm:"column:curriculum_document_id;not null" json:"curriculum_document_id"`
	ActivityName         string    `gorm:"column:activity_name;not null" json:"activity_name"`
	ActivityCategory     string    `gorm:"column:activity_category" json:"activity_category"` // OLAHRAGA, SENI, ORGANISASI, LAINNYA
	Description          string    `gorm:"column:description;type:text" json:"description"`
	Schedule             string    `gorm:"column:schedule;type:text" json:"schedule"`
	InstructorID         uuid.UUID `gorm:"column:instructor_id" json:"instructor_id"`
	IsActive             bool      `gorm:"column:is_active;default:true" json:"is_active"`

	common.Auditable
}

func (EkstrakurikulerActivity) TableName() string {
	return "trx_ekstrakurikuler_activity"
}

// Ekstrakurikuler Categories
const (
	EkstraKategoriOlahraga   = "OLAHRAGA"   // Sports
	EkstraKategoriSeni       = "SENI"       // Arts
	EkstraKategoriOrganisasi = "ORGANISASI" // Organizations
	EkstraKategoriLainnya    = "LAINNYA"    // Others
)

// GetEkstraKategoriDescription returns Indonesian description of extra-curricular category
func GetEkstraKategoriDescription(category string) string {
	descriptions := map[string]string{
		EkstraKategoriOlahraga:   "Olahraga",
		EkstraKategoriSeni:       "Seni dan Budaya",
		EkstraKategoriOrganisasi: "Organisasi Siswa",
		EkstraKategoriLainnya:    "Lainnya",
	}
	return descriptions[category]
}
