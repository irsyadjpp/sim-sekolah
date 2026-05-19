package student

import (
	"time"

	"github.com/google/uuid"
)

// StudentContextExt mendefinisikan latar belakang personal, profil akademik, dan aspek non-kognitif siswa untuk mendukung pembelajaran berdiferensiasi.
type StudentContextExt struct {
	ID                            uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID                     uuid.UUID `gorm:"type:uuid;not null;uniqueIndex"                  json:"student_id"`
	StudentFamilyBackground       *string   `gorm:"type:text"                                       json:"student_family_background"`
	StudentHomeLanguage           *string   `gorm:"type:varchar(50)"                                json:"student_home_language"`
	StudentPriorKnowledgeLevel    string    `gorm:"type:varchar(30);not null"                       json:"student_prior_knowledge_level"` // 'BELUM_BERKEMBANG', 'LAYAK', 'CAKAP', 'MAHIR'
	StudentLiteracyNumeracyStatus string    `gorm:"type:text;not null"                              json:"student_literacy_numeracy_status"`
	StudentLearningPace           string    `gorm:"type:varchar(30);not null"                       json:"student_learning_pace"` // 'CEPAT_BERNALAR', 'RATA_RATA', 'BUTUH_BIMBINGAN'
	StudentMetacognitiveAwareness *string   `gorm:"type:text"                                       json:"student_metacognitive_awareness"`
	StudentDominantInterest       string    `gorm:"type:text;not null"                              json:"student_dominant_interest"`
	StudentSocialInteractionStyle *string   `gorm:"type:text"                                       json:"student_social_interaction_style"`
	StudentWellBeingStatus        *string   `gorm:"type:text"                                       json:"student_well_being_status"`
	IsVectorSynced                *bool     `gorm:"type:boolean;default:false"                      json:"is_vector_synced"`
	CreatedAt                     time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP"      json:"created_at"`
	UpdatedAt                     time.Time `gorm:"type:timestamptz;default:CURRENT_TIMESTAMP"      json:"updated_at"`
}

func (StudentContextExt) TableName() string {
	return "master_student_context_ext"
}
