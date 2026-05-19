package auth

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"
)

type AuthRepository interface {
	// User operations
	CreateUser(user *User) error
	FindByUsername(username string) (*User, error)
	FindByEmail(email string) (*User, error)
	FindByID(id string) (*User, error)
	UpdateUser(user *User, updates map[string]interface{}) error
	SaveUser(user *User) error

	// Role operations
	FindRoleByName(name string) (*Role, error)

	// Token operations
	CreateRefreshToken(rt *RefreshToken) error
	FindRefreshToken(token string) (*RefreshToken, error)
	DeleteRefreshToken(rt *RefreshToken) error
	DeleteRefreshTokenByToken(token string) error
	CreatePasswordResetToken(prt *PasswordResetToken) error
	FindPasswordResetToken(token string) (*PasswordResetToken, error)
	DeletePasswordResetToken(prt *PasswordResetToken) error

	// Cache operations
	SetUserCache(ctx context.Context, userID string, data interface{}, expiration time.Duration) error
	GetUserCache(ctx context.Context, userID string) (string, error)
	DeleteUserCache(ctx context.Context, userID string) error

	// Token blacklist (logout)
	BlacklistAccessToken(ctx context.Context, token string, ttl time.Duration) error
	IsBlacklisted(ctx context.Context, token string) (bool, error)

	// External data (Teacher/Student) - temporary until their modules have proper repos
	GetTeacherData(teacherID uuid.UUID) (map[string]interface{}, error)
	GetStudentData(studentID uuid.UUID) (map[string]interface{}, error)
}

type authRepository struct {
	db  *gorm.DB
	rdb *redis.Client
}

func NewAuthRepository(db *gorm.DB, rdb *redis.Client) AuthRepository {
	return &authRepository{db: db, rdb: rdb}
}

func (r *authRepository) CreateUser(user *User) error {
	return r.db.Create(user).Error
}

func (r *authRepository) FindByUsername(username string) (*User, error) {
	var user User
	err := r.db.Where("username = ?", username).First(&user).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *authRepository) FindByEmail(email string) (*User, error) {
	var user User
	err := r.db.Preload("Roles").Where("email = ?", email).First(&user).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *authRepository) FindByID(id string) (*User, error) {
	var user User
	err := r.db.Preload("Roles").Where("id = ?", id).First(&user).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *authRepository) UpdateUser(user *User, updates map[string]interface{}) error {
	return r.db.Model(user).Updates(updates).Error
}

func (r *authRepository) SaveUser(user *User) error {
	return r.db.Save(user).Error
}

func (r *authRepository) FindRoleByName(name string) (*Role, error) {
	var role Role
	err := r.db.Where("role_name = ?", name).First(&role).Error
	if err != nil {
		return nil, err
	}
	return &role, nil
}

func (r *authRepository) CreateRefreshToken(rt *RefreshToken) error {
	return r.db.Create(rt).Error
}

func (r *authRepository) FindRefreshToken(token string) (*RefreshToken, error) {
	var rt RefreshToken
	err := r.db.Where("token = ?", token).First(&rt).Error
	if err != nil {
		return nil, err
	}
	return &rt, nil
}

func (r *authRepository) DeleteRefreshToken(rt *RefreshToken) error {
	return r.db.Delete(rt).Error
}

func (r *authRepository) DeleteRefreshTokenByToken(token string) error {
	return r.db.Where("token = ?", token).Delete(&RefreshToken{}).Error
}

func (r *authRepository) CreatePasswordResetToken(prt *PasswordResetToken) error {
	return r.db.Create(prt).Error
}

func (r *authRepository) FindPasswordResetToken(token string) (*PasswordResetToken, error) {
	var prt PasswordResetToken
	err := r.db.Where("token = ?", token).First(&prt).Error
	if err != nil {
		return nil, err
	}
	return &prt, nil
}

func (r *authRepository) DeletePasswordResetToken(prt *PasswordResetToken) error {
	return r.db.Delete(prt).Error
}

func (r *authRepository) SetUserCache(ctx context.Context, userID string, data interface{}, expiration time.Duration) error {
	if r.rdb == nil {
		return nil
	}
	cacheKey := fmt.Sprintf("user_settings:%s", userID)
	jsonData, err := json.Marshal(data)
	if err != nil {
		return err
	}
	return r.rdb.Set(ctx, cacheKey, jsonData, expiration).Err()
}

func (r *authRepository) GetUserCache(ctx context.Context, userID string) (string, error) {
	if r.rdb == nil {
		return "", redis.Nil
	}
	cacheKey := fmt.Sprintf("user_settings:%s", userID)
	return r.rdb.Get(ctx, cacheKey).Result()
}

func (r *authRepository) DeleteUserCache(ctx context.Context, userID string) error {
	if r.rdb == nil {
		return nil
	}
	cacheKey := fmt.Sprintf("user_settings:%s", userID)
	return r.rdb.Del(ctx, cacheKey).Err()
}

func (r *authRepository) BlacklistAccessToken(ctx context.Context, token string, ttl time.Duration) error {
	if r.rdb == nil {
		return nil
	}
	return r.rdb.Set(ctx, "blacklist:"+token, "1", ttl).Err()
}

func (r *authRepository) IsBlacklisted(ctx context.Context, token string) (bool, error) {
	if r.rdb == nil {
		return false, nil
	}
	count, err := r.rdb.Exists(ctx, "blacklist:"+token).Result()
	return count > 0, err
}

func (r *authRepository) GetTeacherData(teacherID uuid.UUID) (map[string]interface{}, error) {
	var data map[string]interface{}
	err := r.db.Table("teachers").Where("id = ?", teacherID).Take(&data).Error
	return data, err
}

func (r *authRepository) GetStudentData(studentID uuid.UUID) (map[string]interface{}, error) {
	var data map[string]interface{}
	err := r.db.Table("students").Where("id = ?", studentID).Take(&data).Error
	return data, err
}
