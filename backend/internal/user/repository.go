package user

import (
	"context"

	"sim-sekolah/internal/auth"

	"gorm.io/gorm"
)

type UserRepository interface {
	GetAll(ctx context.Context, limit, offset int, search string) ([]auth.User, int64, error)
	GetByID(ctx context.Context, id string) (*auth.User, error)
	UpdateStatus(ctx context.Context, user *auth.User) error
	UpdateRoles(ctx context.Context, user *auth.User, roles []auth.Role) error
	UpdatePassword(ctx context.Context, id string, hashedPassword string) error
	GetRolesByNames(ctx context.Context, roleNames []string) ([]auth.Role, error)
	GetTeacherID(ctx context.Context, userID string) (string, error)
	GetStudentID(ctx context.Context, userID string) (string, error)
	GetAllRoles(ctx context.Context) ([]auth.Role, error)
}

type userRepository struct {
	db *gorm.DB
}

func NewUserRepository(db *gorm.DB) UserRepository {
	return &userRepository{db: db}
}

func (r *userRepository) GetAll(ctx context.Context, limit, offset int, search string) ([]auth.User, int64, error) {
	var users []auth.User
	var total int64

	query := r.db.WithContext(ctx).Model(&auth.User{})
	if search != "" {
		like := "%" + search + "%"
		query = query.Where("full_name ILIKE ? OR username ILIKE ? OR email ILIKE ?", like, like, like)
	}

	query.Count(&total)
	err := query.Preload("Roles").Limit(limit).Offset(offset).Order("created_at DESC").Find(&users).Error

	// Hilangkan hash password dari hasil
	for i := range users {
		users[i].PasswordHash = ""
	}
	return users, total, err
}

func (r *userRepository) GetByID(ctx context.Context, id string) (*auth.User, error) {
	var u auth.User
	err := r.db.WithContext(ctx).Preload("Roles").First(&u, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	u.PasswordHash = ""
	return &u, nil
}

func (r *userRepository) UpdateStatus(ctx context.Context, user *auth.User) error {
	// Update kolom spesifik saja untuk status
	return r.db.WithContext(ctx).Model(user).Updates(map[string]interface{}{
		"is_enabled":              user.IsEnabled,
		"account_non_locked":      user.AccountNonLocked,
		"account_non_expired":     user.AccountNonExpired,
		"credentials_non_expired": user.CredentialsNonExpired,
	}).Error
}

func (r *userRepository) UpdateRoles(ctx context.Context, user *auth.User, roles []auth.Role) error {
	// Replace semua role dengan role baru di tabel join (many2many)
	return r.db.WithContext(ctx).Model(user).Association("Roles").Replace(roles)
}

func (r *userRepository) UpdatePassword(ctx context.Context, id string, hashedPassword string) error {
	return r.db.WithContext(ctx).Model(&auth.User{}).Where("id = ?", id).Update("password_hash", hashedPassword).Error
}

func (r *userRepository) GetRolesByNames(ctx context.Context, roleNames []string) ([]auth.Role, error) {
	var roles []auth.Role
	err := r.db.WithContext(ctx).Where("role_name IN ?", roleNames).Find(&roles).Error
	return roles, err
}

func (r *userRepository) GetTeacherID(ctx context.Context, userID string) (string, error) {
	var teacherID string
	err := r.db.WithContext(ctx).Table("users").Select("CAST(teacher_id AS VARCHAR)").Where("id = ?", userID).Scan(&teacherID).Error
	return teacherID, err
}

func (r *userRepository) GetStudentID(ctx context.Context, userID string) (string, error) {
	var studentID string
	err := r.db.WithContext(ctx).Table("users").Select("CAST(student_id AS VARCHAR)").Where("id = ?", userID).Scan(&studentID).Error
	return studentID, err
}

func (r *userRepository) GetAllRoles(ctx context.Context) ([]auth.Role, error) {
	var roles []auth.Role
	err := r.db.WithContext(ctx).Find(&roles).Error
	return roles, err
}
