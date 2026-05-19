package auth

import (
	"time"

	"github.com/google/uuid"
)

type Role struct {
	ID        uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey"`
	RoleName  string    `gorm:"unique"`
	CreatedAt time.Time
}

func (Role) TableName() string {
	return "auth_role"
}

type User struct {
	ID           uuid.UUID  `gorm:"type:uuid;default:uuid_generate_v4();primaryKey" json:"id"`
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
	CreatedAt time.Time  `json:"created_at"`
	UpdatedAt time.Time  `json:"updated_at"`

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
	ID        uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey"`
	UserID    uuid.UUID
	Token     string
	ExpiredAt time.Time
	CreatedAt time.Time
}

func (RefreshToken) TableName() string {
	return "auth_refresh_token"
}

type PasswordResetToken struct {
	ID        uuid.UUID `gorm:"type:uuid;default:uuid_generate_v4();primaryKey"`
	UserID    uuid.UUID
	Token     string
	ExpiredAt time.Time
	CreatedAt time.Time
}

func (PasswordResetToken) TableName() string {
	return "auth_password_reset_token"
}
