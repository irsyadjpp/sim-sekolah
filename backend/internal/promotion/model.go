package promotion

import (
	"time"

	"github.com/google/uuid"
)

type PromoteRequest struct {
	SourceClassroomID string   `json:"source_classroom_id" validate:"required,uuid"`
	TargetClassroomID string   `json:"target_classroom_id" validate:"required,uuid"`
	StudentIDs        []string `json:"student_ids" validate:"required"`
}

type GraduateRequest struct {
	StudentIDs []string `json:"student_ids" validate:"required"`
}

type AcademicPromotionLog struct {
	ID                uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	StudentID         uuid.UUID `gorm:"type:uuid;not null" json:"student_id"`
	SourceClassroomID uuid.UUID `gorm:"type:uuid;not null" json:"source_classroom_id"`
	TargetClassroomID uuid.UUID `gorm:"type:uuid;not null" json:"target_classroom_id"`
	PromotedBy        uuid.UUID `gorm:"type:uuid;not null" json:"promoted_by"`
	PromotedAt        time.Time `gorm:"type:timestamp;default:CURRENT_TIMESTAMP" json:"promoted_at"`
}

func (AcademicPromotionLog) TableName() string {
	return "trx_academic_promotion_log"
}
