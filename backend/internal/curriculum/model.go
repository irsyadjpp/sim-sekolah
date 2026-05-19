package curriculum

import (
	"time"

	"github.com/google/uuid"

	"sim-sekolah/internal/academic_year"
	"sim-sekolah/internal/school"
)

type CurriculumDocument struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	AcademicYearID uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:uni_curriculum_school_year" json:"academic_year_id"`
	SchoolID       uuid.UUID `gorm:"type:uuid;not null;uniqueIndex:uni_curriculum_school_year" json:"school_id"`
	Status         string    `gorm:"type:varchar(20);default:'DRAFT';not null" json:"status"` // DRAFT, REVIEW, FINAL
	CreatedAt      time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt      time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP" json:"updated_at"`

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
