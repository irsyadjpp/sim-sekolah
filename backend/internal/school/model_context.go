package school

import (
	"time"

	"github.com/google/uuid"
	"github.com/lib/pq"
)

// SchoolLocalContext mendefinisikan karakteristik demografis, monografis, dan sosio-kultural area sekolah.
type SchoolLocalContext struct {
	ID                       uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID                 uuid.UUID `gorm:"type:uuid;not null;uniqueIndex"                  json:"school_id"`
	LocalDominantOccupations string    `gorm:"type:text;not null"                              json:"local_dominant_occupations"`
	LocalIncomeLevel         string    `gorm:"type:text;not null"                              json:"local_income_level"`
	LocalLanguageNuance      string    `gorm:"type:text;not null"                              json:"local_language_nuance"`
	LocalGeographicType      string    `gorm:"type:text;not null"                              json:"local_geographic_type"`
	LocalNaturalResources    string    `gorm:"type:text;not null"                              json:"local_natural_resources"`
	LocalEnvironmentalIssues string    `gorm:"type:text;not null"                              json:"local_environmental_issues"`
	LocalCulturalHeritage    *string   `gorm:"type:text"                                       json:"local_cultural_heritage"`
	LocalUMKMPotential       *string   `gorm:"type:text"                                       json:"local_umkm_potential"`
	IsVectorSynced           *bool     `gorm:"type:boolean;default:false"                      json:"is_vector_synced"`
	CreatedAt                time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP"      json:"created_at"`
	UpdatedAt                time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP"      json:"updated_at"`
}

func (SchoolLocalContext) TableName() string {
	return "master_school_local_context"
}

// SchoolContextExt mendefinisikan kapasitas, sumber daya, visi misi, dan kemitraan satuan pendidikan.
type SchoolContextExt struct {
	ID                            uuid.UUID      `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	SchoolID                      uuid.UUID      `gorm:"type:uuid;not null;uniqueIndex"                  json:"school_id"`
	SchoolVisionCore              string         `gorm:"type:text;not null"                              json:"school_vision_core"`
	SchoolDistinctiveValues       string         `gorm:"type:text;not null"                              json:"school_distinctive_values"`
	SchoolLocationSetting         string         `gorm:"type:text;not null"                              json:"school_location_setting"`
	SchoolFacilitiesList          pq.StringArray `gorm:"type:text[];not null"                            json:"school_facilities_list"`
	SchoolDigitalAdoptionLevel    string         `gorm:"type:varchar(20);not null"                       json:"school_digital_adoption_level"` // 'LOW', 'MEDIUM', 'HIGH'
	SchoolTeacherProfileMatrix    string         `gorm:"type:text;not null"                              json:"school_teacher_profile_matrix"`
	SchoolExternalPartners        *string        `gorm:"type:text"                                       json:"school_external_partners"`
	SchoolParentalInvolvementType string         `gorm:"type:varchar(50);not null"                       json:"school_parental_involvement_type"` // 'AKTIF_KOLABORATIF', 'PASIF_INFORMATIF'
	IsVectorSynced                *bool          `gorm:"type:boolean;default:false"                      json:"is_vector_synced"`
	CreatedAt                     time.Time      `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP"      json:"created_at"`
	UpdatedAt                     time.Time      `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP"      json:"updated_at"`
}

func (SchoolContextExt) TableName() string {
	return "master_school_context_ext"
}
