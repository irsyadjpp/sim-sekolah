package permission

import (
	"sim-sekolah/internal/common"

	"github.com/google/uuid"
)

type Permission struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
	PermissionName string    `gorm:"unique;not null" json:"permission_name"`
	Description    string    `json:"description"`

	common.Auditable
}

func (Permission) TableName() string {
	return "auth_permission"
}

type AssignPermissionsRequest struct {
	PermissionIDs []string `json:"permission_ids" validate:"required"`
}
