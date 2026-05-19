package user

import (
	"context"
	"errors"
	"time"

	"sim-sekolah/internal/auth"
	"sim-sekolah/internal/common"
	bcryptpkg "sim-sekolah/pkg/bcrypt"
	"sim-sekolah/pkg/cache"
)

type UserService interface {
	GetAll(ctx context.Context, pagination common.Pagination, search string) ([]auth.User, int64, error)
	GetByID(ctx context.Context, id string) (*auth.User, error)
	UpdateStatus(ctx context.Context, id string, req UpdateUserStatusRequest) (*auth.User, error)
	AssignRoles(ctx context.Context, id string, req AssignRoleRequest) (*auth.User, error)
	ResetPassword(ctx context.Context, id string, req ResetPasswordRequest) error
	GetAllRoles(ctx context.Context) ([]auth.Role, error)
}

type userService struct {
	repo UserRepository
}

func NewUserService(repo UserRepository) UserService {
	return &userService{repo: repo}
}

func (s *userService) GetAll(ctx context.Context, pagination common.Pagination, search string) ([]auth.User, int64, error) {
	return s.repo.GetAll(ctx, pagination.Limit, pagination.Offset, search)
}

func (s *userService) GetByID(ctx context.Context, id string) (*auth.User, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *userService) UpdateStatus(ctx context.Context, id string, req UpdateUserStatusRequest) (*auth.User, error) {
	user, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("user tidak ditemukan")
	}

	if req.IsEnabled != nil {
		user.IsEnabled = *req.IsEnabled
	}
	if req.AccountNonLocked != nil {
		user.AccountNonLocked = *req.AccountNonLocked
	}
	if req.AccountNonExpired != nil {
		user.AccountNonExpired = *req.AccountNonExpired
	}
	if req.CredentialsNonExpired != nil {
		user.CredentialsNonExpired = *req.CredentialsNonExpired
	}

	if err := s.repo.UpdateStatus(ctx, user); err != nil {
		return nil, err
	}
	return user, nil
}

func (s *userService) AssignRoles(ctx context.Context, id string, req AssignRoleRequest) (*auth.User, error) {
	user, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, errors.New("user tidak ditemukan")
	}

	roles, err := s.repo.GetRolesByNames(ctx, req.RoleNames)
	if err != nil || len(roles) == 0 {
		return nil, errors.New("satu atau lebih role tidak valid")
	}

	if err := s.repo.UpdateRoles(ctx, user, roles); err != nil {
		return nil, err
	}

	if cache.GlobalCache != nil {
		_ = cache.GlobalCache.Delete(ctx, "user:id:"+id)
	}

	// Refresh user to get updated roles
	return s.repo.GetByID(ctx, id)
}

func (s *userService) ResetPassword(ctx context.Context, id string, req ResetPasswordRequest) error {
	if _, err := s.repo.GetByID(ctx, id); err != nil {
		return errors.New("user tidak ditemukan")
	}

	hash, err := bcryptpkg.HashPassword(req.NewPassword)
	if err != nil {
		return err
	}

	return s.repo.UpdatePassword(ctx, id, hash)
}

func (s *userService) GetAllRoles(ctx context.Context) ([]auth.Role, error) {
	if cache.GlobalCache != nil {
		var cached []auth.Role
		if err := cache.GlobalCache.Get(ctx, "roles:list", &cached); err == nil {
			return cached, nil
		}
	}

	roles, err := s.repo.GetAllRoles(ctx)
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, "roles:list", roles, 12*time.Hour)
	}
	return roles, err
}
