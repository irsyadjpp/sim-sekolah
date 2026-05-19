package common

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// Auditable adalah struct base yang akan di-embed oleh model lain
// untuk menyediakan fitur auditing otomatis.
type Auditable struct {
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"deleted_at,omitempty"`

	CreatedBy *uuid.UUID `json:"created_by,omitempty"`
	UpdatedBy *uuid.UUID `json:"updated_by,omitempty"`
	DeletedBy *uuid.UUID `json:"deleted_by,omitempty"`
}

// BeforeCreate dipanggil oleh GORM secara otomatis sebelum insert data baru.
func (a *Auditable) BeforeCreate(tx *gorm.DB) error {
	ctx := tx.Statement.Context
	if userIDStr, ok := ctx.Value("user_id").(string); ok && userIDStr != "" {
		if uid, err := uuid.Parse(userIDStr); err == nil {
			a.CreatedBy = &uid
		}
	}
	return nil
}

// BeforeUpdate dipanggil oleh GORM secara otomatis sebelum update data.
func (a *Auditable) BeforeUpdate(tx *gorm.DB) error {
	ctx := tx.Statement.Context
	if userIDStr, ok := ctx.Value("user_id").(string); ok && userIDStr != "" {
		if uid, err := uuid.Parse(userIDStr); err == nil {
			a.UpdatedBy = &uid
		}
	}
	return nil
}

// BeforeDelete dipanggil oleh GORM secara otomatis sebelum soft-delete.
// Note: GORM's BeforeDelete hook doesn't easily allow modifying the struct
// being deleted if it's a batch delete, but for single record delete it works
// if we save it back or modify the current statement.
// A simpler way for soft-delete auditing is to manually set DeletedBy before calling Delete(),
// but we can try to intercept it here.
func (a *Auditable) BeforeDelete(tx *gorm.DB) error {
	ctx := tx.Statement.Context
	if userIDStr, ok := ctx.Value("user_id").(string); ok && userIDStr != "" {
		if uid, err := uuid.Parse(userIDStr); err == nil {
			a.DeletedBy = &uid
			// We need to explicitly update the DeletedBy column during soft delete
			tx.Statement.SetColumn("DeletedBy", &uid)
		}
	}
	return nil
}
