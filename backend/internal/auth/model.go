package auth

import (
	"sim-sekolah/internal/common"
	"time"

	"github.com/google/uuid"
)

type Role struct {
	ID       uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey"`
	RoleName string    `gorm:"unique"`

	common.Auditable
}

func (Role) TableName() string {
	return "auth_role"
}

type User struct {
	ID           uuid.UUID  `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	TeacherID    *uuid.UUID `gorm:"type:uuid" json:"teacher_id"`
	StudentID    *uuid.UUID `gorm:"type:uuid" json:"student_id"`
	FullName     string     `json:"full_name"`
	Username     string     `gorm:"unique" json:"username"`
	Email        string     `gorm:"unique" json:"email"`
	PasswordHash string     `gorm:"column:password_hash" json:"-"`

	// Spring Security Flags
	AccountNonExpired     bool `gorm:"default:true" json:"account_non_expired"`
	AccountNonLocked      bool `gorm:"default:true" json:"account_non_locked"`
	CredentialsNonExpired bool `gorm:"default:true" json:"credentials_non_expired"`
	IsEnabled             bool `gorm:"default:true" json:"is_enabled"`

	LastLogin *time.Time `json:"last_login"`

	common.Auditable

	// Appearance Settings
	ThemeColor   string `gorm:"default:theme-purple" json:"theme_color"`
	ThemeMode    string `gorm:"default:system" json:"theme_mode"`
	ContentType  string `gorm:"default:boxed" json:"content_type"`
	LeftMenuType string `gorm:"default:comfort" json:"left_menu_type"`

	// Security & Notifications
	TwoFactorEnabled   bool   `gorm:"default:false" json:"two_factor_enabled"`
	TotpSecret         string `gorm:"column:totp_secret" json:"-"`
	EmailNotifications bool   `gorm:"default:true" json:"email_notifications"`
	PushNotifications  bool   `gorm:"default:true" json:"push_notifications"`

	Roles []Role `gorm:"many2many:auth_user_role;" json:"roles,omitempty"`
}

func (User) TableName() string {
	return "auth_user"
}

type RefreshToken struct {
	ID        uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey"`
	UserID    uuid.UUID
	Token     string
	ExpiredAt time.Time

	common.Auditable
}

func (RefreshToken) TableName() string {
	return "auth_refresh_token"
}

type PasswordResetToken struct {
	ID        uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey"`
	UserID    uuid.UUID
	Token     string
	ExpiredAt time.Time

	common.Auditable
}

func (PasswordResetToken) TableName() string {
	return "auth_password_reset_token"
}

type UserSession struct {
	ID        uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	UserID    uuid.UUID `gorm:"type:uuid;not null" json:"user_id"`
	UserAgent string    `gorm:"type:text;not null" json:"user_agent"`
	IPAddress string    `gorm:"type:varchar(50);not null" json:"ip_address"`
	IsRevoked bool      `gorm:"default:false" json:"is_revoked"`
	ExpiresAt time.Time `gorm:"type:timestamptz;not null" json:"expires_at"`

	common.Auditable
}

func (UserSession) TableName() string {
	return "auth_user_session"
}

type Permission struct {
	ID             uuid.UUID `gorm:"type:uuid;default:uuidv7();primaryKey" json:"id"`
	PermissionName string    `gorm:"type:varchar(100);unique;not null" json:"permission_name"`
	Description    string    `gorm:"type:text" json:"description"`

	common.Auditable
}

func (Permission) TableName() string {
	return "auth_permission"
}
