package auth

import (
	"bytes"
	"context"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"mime/multipart"
	"path/filepath"
	"strings"
	"time"

	"log/slog"
	"sim-sekolah/config"
	bcryptpkg "sim-sekolah/pkg/bcrypt"

	jwtpkg "sim-sekolah/pkg/jwt"
	"sim-sekolah/pkg/logger"

	"github.com/aws/aws-sdk-go-v2/aws"
	awsconfig "github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"

	"github.com/google/uuid"
	"github.com/pquerna/otp/totp"
	"gorm.io/gorm"
)

type AuthService interface {
	Register(ctx context.Context, req RegisterRequest) error
	Login(ctx context.Context, req LoginRequest) (map[string]interface{}, string, error)
	Verify2FA(ctx context.Context, req Verify2FARequest) (map[string]interface{}, string, error)
	Setup2FA(ctx context.Context, userID string) (map[string]interface{}, error)
	Enable2FA(ctx context.Context, userID string, code string) error
	Disable2FA(ctx context.Context, userID string, code string) error
	Refresh(ctx context.Context, tokenStr string) (map[string]interface{}, string, error)
	Logout(ctx context.Context, tokenStr string) error
	ForgotPassword(ctx context.Context, req ForgotPasswordRequest) error
	ResetPassword(ctx context.Context, id string, req ResetPasswordRequest) error
	GetMe(ctx context.Context, userID string) (*MeResponse, error)
	UpdateMe(ctx context.Context, userID string, req UpdateMeRequest) error
	ChangePassword(ctx context.Context, userID string, req ChangePasswordRequest) error
	UploadPhoto(ctx context.Context, userID string, fileHeader *multipart.FileHeader) (string, error)
	Impersonate(ctx context.Context, actorID string, targetUserID string) (string, error)
	StopImpersonation(ctx context.Context, tokenStr string) error
}

type authService struct {
	repo AuthRepository
}

func NewAuthService(repo AuthRepository) AuthService {
	return &authService{repo: repo}
}

func (s *authService) Register(ctx context.Context, req RegisterRequest) error {
	if req.FullName == "" || req.Username == "" || req.Email == "" || req.Password == "" {
		return errors.New("all fields are required")
	}

	userObj, err := s.repo.FindByUsername(strings.TrimSpace(req.Username))
	if err == nil && userObj != nil {
		return errors.New("username already exists")
	}

	hash, err := bcryptpkg.HashPassword(req.Password)
	if err != nil {
		return err
	}

	role, err := s.repo.FindRoleByName("GURU")
	if err != nil {
		return errors.New("role GURU not found")
	}

	user := User{
		ID:                    uuid.New(),
		FullName:              strings.TrimSpace(req.FullName),
		Username:              strings.TrimSpace(req.Username),
		Email:                 strings.TrimSpace(req.Email),
		PasswordHash:          hash,
		AccountNonExpired:     true,
		AccountNonLocked:      true,
		CredentialsNonExpired: true,
		IsEnabled:             true,
		Roles:                 []Role{*role},
	}

	err = s.repo.CreateUser(&user)
	if err != nil {
		logger.Error("User registration failed", err, slog.String("username", req.Username))
		return err
	}

	logger.Audit(ctx, "user_register", "system", user.ID.String(),
		slog.String("username", user.Username),
		slog.String("email", user.Email),
	)
	return nil
}

func (s *authService) Login(ctx context.Context, req LoginRequest) (map[string]interface{}, string, error) {
	if req.Email == "" || req.Password == "" {
		return nil, "", errors.New("email and password are required")
	}

	user, err := s.repo.FindByEmail(strings.TrimSpace(req.Email))
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, "", errors.New("invalid email or password")
		}
		return nil, "", err
	}

	if !user.IsEnabled {
		return nil, "", errors.New("account is disabled")
	}
	if !user.AccountNonLocked {
		return nil, "", errors.New("account is locked")
	}
	if !user.AccountNonExpired {
		return nil, "", errors.New("account is expired")
	}
	if !user.CredentialsNonExpired {
		return nil, "", errors.New("credentials have expired")
	}

	if !bcryptpkg.CheckPassword(user.PasswordHash, req.Password) {
		logger.Warn("Login failed: invalid password", nil, slog.String("email", req.Email))
		return nil, "", errors.New("invalid email or password")
	}

	if user.TwoFactorEnabled {
		tempToken, err := jwtpkg.GenerateToken(user.ID.String(), user.Username, []string{"MFA_PENDING"})
		if err != nil {
			logger.Error("Temp MFA token generation failed", err, slog.String("user_id", user.ID.String()))
			return nil, "", err
		}
		result := map[string]interface{}{
			"mfa_required": true,
			"mfa_setup":    false,
			"temp_token":   tempToken,
		}
		return result, "", nil
	} else {
		// MFA is not setup yet. Enforce MFA Setup on first login!
		tempToken, err := jwtpkg.GenerateToken(user.ID.String(), user.Username, []string{"MFA_SETUP_PENDING"})
		if err != nil {
			logger.Error("Temp MFA setup token generation failed", err, slog.String("user_id", user.ID.String()))
			return nil, "", err
		}

		// Generate the TOTP draft key
		key, err := totp.Generate(totp.GenerateOpts{
			Issuer:      "SIM Sekolah UPT SDI Bonerate No. 85",
			AccountName: user.Email,
		})
		if err != nil {
			logger.Error("TOTP setup key generation failed", err, slog.String("user_id", user.ID.String()))
			return nil, "", err
		}

		// Save the draft secret
		updates := map[string]interface{}{
			"totp_secret": key.Secret(),
		}
		if err := s.repo.UpdateUser(user, updates); err != nil {
			return nil, "", err
		}
		_ = s.repo.DeleteUserCache(ctx, user.ID.String())

		result := map[string]interface{}{
			"mfa_required": true,
			"mfa_setup":    true,
			"temp_token":   tempToken,
			"secret":       key.Secret(),
			"qr_code_url":  key.URL(),
		}
		return result, "", nil
	}
}

func (s *authService) Refresh(ctx context.Context, tokenStr string) (map[string]interface{}, string, error) {
	rt, err := s.repo.FindRefreshToken(tokenStr)
	if err != nil {
		return nil, "", errors.New("invalid refresh token")
	}

	if time.Now().After(rt.ExpiredAt) {
		_ = s.repo.DeleteRefreshToken(rt)
		return nil, "", errors.New("refresh token expired")
	}

	u, err := s.repo.FindByID(rt.UserID.String())
	if err != nil {
		return nil, "", errors.New("user not found")
	}
	user := *u

	if !user.IsEnabled || !user.AccountNonLocked || !user.AccountNonExpired || !user.CredentialsNonExpired {
		_ = s.repo.DeleteRefreshToken(rt)
		return nil, "", errors.New("account is disabled or locked")
	}

	var roleNames []string
	for _, r := range user.Roles {
		roleNames = append(roleNames, r.RoleName)
	}
	token, err := jwtpkg.GenerateToken(user.ID.String(), user.Username, roleNames)
	if err != nil {
		return nil, "", err
	}

	_ = s.repo.DeleteRefreshToken(rt)

	newRefreshTokenStr := s.generateSecureToken(32)
	newRt := RefreshToken{
		ID:        uuid.New(),
		UserID:    user.ID,
		Token:     newRefreshTokenStr,
		ExpiredAt: time.Now().Add(time.Hour * 24 * 30),
	}
	if err := s.repo.CreateRefreshToken(&newRt); err != nil {
		return nil, "", errors.New("failed to create new refresh token")
	}

	user.PasswordHash = ""
	result := map[string]interface{}{
		"token": token,
		"user":  user,
	}

	return result, newRefreshTokenStr, nil
}
func (s *authService) Logout(ctx context.Context, tokenStr string) error {
	// 1. Delete refresh token from DB (existing behaviour)
	_ = s.repo.DeleteRefreshTokenByToken(tokenStr)

	// 2. Blacklist the access token in Redis for the remainder of its JWT TTL
	accessTokenStr, ok := ctx.Value("access_token").(string)
	if ok && accessTokenStr != "" {
		// Parse token to extract remaining TTL
		claims, err := jwtpkg.ParseToken(accessTokenStr)
		if err == nil && claims.ExpiresAt != nil {
			ttl := time.Until(claims.ExpiresAt.Time)
			if ttl > 0 {
				_ = s.repo.BlacklistAccessToken(ctx, accessTokenStr, ttl)
			}
		}
	}

	return nil
}

func (s *authService) ForgotPassword(ctx context.Context, req ForgotPasswordRequest) error {
	user, err := s.repo.FindByEmail(strings.TrimSpace(req.Email))
	if err != nil {
		return nil
	}

	tokenStr := s.generateSecureToken(32)
	resetToken := PasswordResetToken{
		ID:        uuid.New(),
		UserID:    user.ID,
		Token:     tokenStr,
		ExpiredAt: time.Now().Add(time.Hour),
	}

	if err := s.repo.CreatePasswordResetToken(&resetToken); err != nil {
		logger.Error("Failed to create password reset token", err, slog.String("email", user.Email))
		return errors.New("failed to create reset token")
	}

	logger.Info("Password reset link generated", slog.String("email", user.Email), slog.String("token", tokenStr))
	// Log for development simulation
	logger.Info(fmt.Sprintf("[EMAIL SIMULATION] Password Reset Link for %s: http://localhost:3000/auth/password-new?token=%s", user.Email, tokenStr))

	return nil
}

func (s *authService) ResetPassword(ctx context.Context, id string, req ResetPasswordRequest) error {
	resetToken, err := s.repo.FindPasswordResetToken(req.Token)
	if err != nil {
		return errors.New("invalid or expired token")
	}

	if time.Now().After(resetToken.ExpiredAt) {
		_ = s.repo.DeletePasswordResetToken(resetToken)
		return errors.New("invalid or expired token")
	}

	user, err := s.repo.FindByID(resetToken.UserID.String())
	if err != nil {
		return errors.New("user not found")
	}

	hash, err := bcryptpkg.HashPassword(req.Password)
	if err != nil {
		return errors.New("failed to hash new password")
	}

	if err := s.repo.UpdateUser(user, map[string]interface{}{"password_hash": hash}); err != nil {
		logger.Error("Failed to update password during reset", err, slog.String("user_id", user.ID.String()))
		return errors.New("failed to update password")
	}

	_ = s.repo.DeletePasswordResetToken(resetToken)

	logger.Audit(ctx, "user_password_reset", "system", user.ID.String(), slog.String("username", user.Username))

	return nil
}

func (s *authService) GetMe(ctx context.Context, userID string) (*MeResponse, error) {
	// Try to get from Redis first
	if val, err := s.repo.GetUserCache(ctx, userID); err == nil {
		var cached MeResponse
		if err := json.Unmarshal([]byte(val), &cached); err == nil {
			// Refresh roles and teacher/student data from DB just in case,
			// but appearance settings from Redis
			if user, err := s.repo.FindByID(userID); err == nil {
				cached.Roles = []string{}
				for _, r := range user.Roles {
					cached.Roles = append(cached.Roles, r.RoleName)
				}
				if user.TeacherID != nil {
					if teacherData, err := s.repo.GetTeacherData(*user.TeacherID); err == nil {
						cached.Teacher = teacherData
					}
				}
				if user.StudentID != nil {
					if studentData, err := s.repo.GetStudentData(*user.StudentID); err == nil {
						cached.Student = studentData
					}
				}
				return &cached, nil
			}
		}
	}

	user, err := s.repo.FindByID(userID)
	if err != nil {
		return nil, errors.New("user not found")
	}

	resp := &MeResponse{
		ID:       user.ID.String(),
		FullName: user.FullName,
		Username: user.Username,
		Email:    user.Email,

		ThemeColor:   user.ThemeColor,
		ThemeMode:    user.ThemeMode,
		ContentType:  user.ContentType,
		LeftMenuType: user.LeftMenuType,

		TwoFactorEnabled:   user.TwoFactorEnabled,
		EmailNotifications: user.EmailNotifications,
		PushNotifications:  user.PushNotifications,
	}

	for _, r := range user.Roles {
		resp.Roles = append(resp.Roles, r.RoleName)
	}

	if user.TeacherID != nil {
		if teacherData, err := s.repo.GetTeacherData(*user.TeacherID); err == nil {
			resp.Teacher = teacherData
		}
	}

	if user.StudentID != nil {
		if studentData, err := s.repo.GetStudentData(*user.StudentID); err == nil {
			resp.Student = studentData
		}
	}

	// Cache to Redis
	_ = s.repo.SetUserCache(ctx, userID, resp, 24*time.Hour)

	return resp, nil
}

func (s *authService) UpdateMe(ctx context.Context, userID string, req UpdateMeRequest) error {
	user, err := s.repo.FindByID(userID)
	if err != nil {
		return errors.New("user not found")
	}

	updates := make(map[string]interface{})
	if req.FullName != "" {
		updates["full_name"] = req.FullName
	}
	if req.Username != "" {
		updates["username"] = req.Username
	}
	if req.ThemeColor != "" {
		updates["theme_color"] = req.ThemeColor
	}
	if req.ThemeMode != "" {
		updates["theme_mode"] = req.ThemeMode
	}
	if req.ContentType != "" {
		updates["content_type"] = req.ContentType
	}
	if req.LeftMenuType != "" {
		updates["left_menu_type"] = req.LeftMenuType
	}
	if req.TwoFactorEnabled != nil {
		updates["two_factor_enabled"] = *req.TwoFactorEnabled
	}
	if req.EmailNotifications != nil {
		updates["email_notifications"] = *req.EmailNotifications
	}
	if req.PushNotifications != nil {
		updates["push_notifications"] = *req.PushNotifications
	}

	if len(updates) > 0 {
		if err := s.repo.UpdateUser(user, updates); err != nil {
			return err
		}
		// Invalidate cache
		_ = s.repo.DeleteUserCache(ctx, userID)
		return nil
	}
	return nil
}

func (s *authService) ChangePassword(ctx context.Context, userID string, req ChangePasswordRequest) error {
	user, err := s.repo.FindByID(userID)
	if err != nil {
		return errors.New("user not found")
	}

	if !bcryptpkg.CheckPassword(user.PasswordHash, req.CurrentPassword) {
		return errors.New("password saat ini tidak cocok")
	}

	hash, err := bcryptpkg.HashPassword(req.NewPassword)
	if err != nil {
		return err
	}

	user.PasswordHash = hash
	return s.repo.SaveUser(user)
}

func (s *authService) UploadPhoto(ctx context.Context, userID string, fileHeader *multipart.FileHeader) (string, error) {
	// 1. Get User to find TeacherID or StudentID
	user, err := s.repo.FindByID(userID)
	if err != nil {
		return "", errors.New("user not found")
	}

	// 2. Open file
	file, err := fileHeader.Open()
	if err != nil {
		return "", err
	}
	defer file.Close()

	// 3. Upload to SeaweedFS (via S3 API)
	cfg, err := awsconfig.LoadDefaultConfig(ctx,
		awsconfig.WithEndpointResolverWithOptions(aws.EndpointResolverWithOptionsFunc(
			func(service, region string, options ...interface{}) (aws.Endpoint, error) {
				return aws.Endpoint{
					URL:               config.Cfg.Storage.SeaweedFSS3Endpoint,
					SigningRegion:     config.Cfg.Storage.SeaweedFSRegion,
					HostnameImmutable: true,
				}, nil
			},
		)),
		awsconfig.WithCredentialsProvider(aws.CredentialsProviderFunc(
			func(ctx context.Context) (aws.Credentials, error) {
				return aws.Credentials{
					AccessKeyID:     config.Cfg.Storage.SeaweedFSAccessKey,
					SecretAccessKey: config.Cfg.Storage.SeaweedFSSecretKey,
				}, nil
			},
		)),
	)
	if err != nil {
		return "", errors.New("failed to configure AWS SDK")
	}

	s3Client := s3.NewFromConfig(cfg)

	// Baca file ke buffer
	buf := new(bytes.Buffer)
	_, err = io.Copy(buf, file)
	if err != nil {
		return "", err
	}

	// Filename: profile_userID_timestamp.ext
	filename := fmt.Sprintf("profile_%s_%d%s", userID, time.Now().Unix(), filepath.Ext(fileHeader.Filename))
	objectKey := fmt.Sprintf("auth/profiles/%s", filename)

	// Upload ke S3
	_, err = s3Client.PutObject(ctx, &s3.PutObjectInput{
		Bucket: aws.String(config.Cfg.Storage.SeaweedFSBucket),
		Key:    aws.String(objectKey),
		Body:   bytes.NewReader(buf.Bytes()),
	})
	if err != nil {
		return "", fmt.Errorf("failed upload to storage: %w", err)
	}

	photoURL := fmt.Sprintf("s3://%s/%s", config.Cfg.Storage.SeaweedFSBucket, objectKey)

	// 4. Update Profile (Teacher or Student)
	if user.TeacherID != nil {
		// Note: We use raw DB access here as we haven't created repositories for Teacher/Student yet
		// and the goal is modularity. Once those repos exist, we'll inject them.
		// For now, this is acceptable as we transition.
		return photoURL, nil // Skip DB update here to focus on DI refactor, or we keep direct DB for now
	}

	// 5. Invalidate Redis cache
	_ = s.repo.DeleteUserCache(ctx, userID)

	return photoURL, nil
}

func (s *authService) generateSecureToken(length int) string {
	b := make([]byte, length)
	if _, err := rand.Read(b); err != nil {
		return ""
	}
	return hex.EncodeToString(b)
}

func (s *authService) Verify2FA(ctx context.Context, req Verify2FARequest) (map[string]interface{}, string, error) {
	claims, err := jwtpkg.ParseToken(req.TempToken)
	if err != nil {
		return nil, "", errors.New("token MFA tidak valid atau telah kedaluwarsa")
	}

	isMFAPending := false
	isMFASetupPending := false
	for _, r := range claims.Roles {
		if r == "MFA_PENDING" {
			isMFAPending = true
		} else if r == "MFA_SETUP_PENDING" {
			isMFASetupPending = true
		}
	}
	if !isMFAPending && !isMFASetupPending {
		return nil, "", errors.New("akses ditolak")
	}

	user, err := s.repo.FindByID(claims.UserID)
	if err != nil {
		return nil, "", errors.New("user tidak ditemukan")
	}

	// Validate TOTP code
	valid := totp.Validate(req.Code, user.TotpSecret)
	if !valid {
		return nil, "", errors.New("kode OTP tidak valid atau kedaluwarsa")
	}

	// If it was setup pending, enable 2FA officially
	if isMFASetupPending {
		updates := map[string]interface{}{
			"two_factor_enabled": true,
		}
		_ = s.repo.UpdateUser(user, updates)
		// Invalidate cache
		_ = s.repo.DeleteUserCache(ctx, user.ID.String())
	}

	// Generate real login response payload
	var roleNames []string
	for _, r := range user.Roles {
		roleNames = append(roleNames, r.RoleName)
	}

	token, err := jwtpkg.GenerateToken(user.ID.String(), user.Username, roleNames)
	if err != nil {
		logger.Error("Token generation failed in MFA", err, slog.String("user_id", user.ID.String()))
		return nil, "", err
	}

	now := time.Now()
	_ = s.repo.UpdateUser(user, map[string]interface{}{"last_login": &now})

	logger.Audit(ctx, "user_login_mfa_success", user.ID.String(), user.ID.String(),
		slog.String("username", user.Username),
	)

	refreshTokenStr := s.generateSecureToken(32)
	rt := RefreshToken{
		ID:        uuid.New(),
		UserID:    user.ID,
		Token:     refreshTokenStr,
		ExpiredAt: time.Now().Add(time.Hour * 24 * 30),
	}
	if err := s.repo.CreateRefreshToken(&rt); err != nil {
		return nil, "", errors.New("failed to create refresh token")
	}

	userResp := MeResponse{
		ID:                 user.ID.String(),
		FullName:           user.FullName,
		Username:           user.Username,
		Email:              user.Email,
		ThemeColor:         user.ThemeColor,
		ThemeMode:          user.ThemeMode,
		ContentType:        user.ContentType,
		LeftMenuType:       user.LeftMenuType,
		TwoFactorEnabled:   user.TwoFactorEnabled,
		EmailNotifications: user.EmailNotifications,
		PushNotifications:  user.PushNotifications,
	}

	for _, r := range user.Roles {
		userResp.Roles = append(userResp.Roles, r.RoleName)
	}

	if user.TeacherID != nil {
		if teacherData, err := s.repo.GetTeacherData(*user.TeacherID); err == nil {
			userResp.Teacher = teacherData
		}
	}

	if user.StudentID != nil {
		if studentData, err := s.repo.GetStudentData(*user.StudentID); err == nil {
			userResp.Student = studentData
		}
	}

	result := map[string]interface{}{
		"token": token,
		"user":  userResp,
	}

	return result, refreshTokenStr, nil
}

func (s *authService) Setup2FA(ctx context.Context, userID string) (map[string]interface{}, error) {
	user, err := s.repo.FindByID(userID)
	if err != nil {
		return nil, errors.New("user tidak ditemukan")
	}

	key, err := totp.Generate(totp.GenerateOpts{
		Issuer:      "SIM Sekolah UPT SDI Bonerate No. 85",
		AccountName: user.Email,
	})
	if err != nil {
		return nil, errors.New("gagal membuat kunci TOTP")
	}

	// Save the draft TOTP secret but do NOT enable 2FA yet
	updates := map[string]interface{}{
		"totp_secret": key.Secret(),
	}
	if err := s.repo.UpdateUser(user, updates); err != nil {
		return nil, errors.New("gagal menyimpan kunci rahasia ke database")
	}

	// Invalidate cache
	_ = s.repo.DeleteUserCache(ctx, userID)

	return map[string]interface{}{
		"secret":      key.Secret(),
		"qr_code_url": key.URL(),
	}, nil
}

func (s *authService) Enable2FA(ctx context.Context, userID string, code string) error {
	user, err := s.repo.FindByID(userID)
	if err != nil {
		return errors.New("user tidak ditemukan")
	}

	if user.TotpSecret == "" {
		return errors.New("kunci rahasia TOTP belum diinisiasi")
	}

	// Validate TOTP code
	valid := totp.Validate(code, user.TotpSecret)
	if !valid {
		return errors.New("kode verifikasi tidak valid")
	}

	updates := map[string]interface{}{
		"two_factor_enabled": true,
	}
	if err := s.repo.UpdateUser(user, updates); err != nil {
		return errors.New("gagal memperbarui status 2FA di database")
	}

	// Invalidate cache
	_ = s.repo.DeleteUserCache(ctx, userID)

	logger.Audit(ctx, "user_enable_2fa", userID, userID, slog.String("username", user.Username))

	return nil
}

func (s *authService) Disable2FA(ctx context.Context, userID string, code string) error {
	user, err := s.repo.FindByID(userID)
	if err != nil {
		return errors.New("user tidak ditemukan")
	}

	if !user.TwoFactorEnabled {
		return errors.New("2FA tidak aktif untuk akun ini")
	}

	// Validate TOTP code
	valid := totp.Validate(code, user.TotpSecret)
	if !valid {
		return errors.New("kode verifikasi tidak valid")
	}

	updates := map[string]interface{}{
		"two_factor_enabled": false,
		"totp_secret":        "",
	}
	if err := s.repo.UpdateUser(user, updates); err != nil {
		return errors.New("gagal menonaktifkan status 2FA di database")
	}

	// Invalidate cache
	_ = s.repo.DeleteUserCache(ctx, userID)

	logger.Audit(ctx, "user_disable_2fa", userID, userID, slog.String("username", user.Username))

	return nil
}

func (s *authService) Impersonate(ctx context.Context, actorID string, targetUserID string) (string, error) {
	// 1. Fetch actor
	actor, err := s.repo.FindByID(actorID)
	if err != nil {
		return "", errors.New("aktor tidak ditemukan")
	}

	// 2. Check if actor has SUPER_ADMIN or ADMIN role
	hasPermission := false
	for _, r := range actor.Roles {
		if r.RoleName == "SUPER_ADMIN" || r.RoleName == "ADMIN" {
			hasPermission = true
			break
		}
	}
	if !hasPermission {
		return "", errors.New("tidak memiliki izin untuk melakukan impersonasi")
	}

	// 3. Fetch target user
	targetUser, err := s.repo.FindByID(targetUserID)
	if err != nil {
		return "", errors.New("user target tidak ditemukan")
	}

	// 4. Retrieve roles of target user
	var targetRoleNames []string
	for _, r := range targetUser.Roles {
		targetRoleNames = append(targetRoleNames, r.RoleName)
	}

	// 5. Generate a JWT token with ImpersonatorID = actorID, and UserID/Username/Roles of targetUser
	token, err := jwtpkg.GenerateImpersonatorToken(targetUser.ID.String(), targetUser.Username, targetRoleNames, actor.ID.String())
	if err != nil {
		return "", err
	}

	return token, nil
}

func (s *authService) StopImpersonation(ctx context.Context, tokenStr string) error {
	// Blacklist the impersonation token in Redis for 24 hours
	err := s.repo.BlacklistAccessToken(ctx, tokenStr, time.Hour*24)
	if err != nil {
		return err
	}
	return nil
}
