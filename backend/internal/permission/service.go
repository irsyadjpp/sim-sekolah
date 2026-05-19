package permission

import (
	"context"
	"time"

	"sim-sekolah/pkg/cache"

	"github.com/google/uuid"
)

type PermissionService interface {
	GetAll(ctx context.Context) ([]Permission, error)
	GetByID(ctx context.Context, id string) (*Permission, error)
	Create(ctx context.Context, p *Permission) error
	Delete(ctx context.Context, id string) error
	GetPermissionsByRoleID(ctx context.Context, roleID string) ([]Permission, error)
	AssignPermissionsToRole(ctx context.Context, roleID string, permissionIDs []string) error
}

type permissionService struct {
	repo PermissionRepository
}

func NewPermissionService(repo PermissionRepository) PermissionService {
	return &permissionService{repo: repo}
}

func (s *permissionService) GetAll(ctx context.Context) ([]Permission, error) {
	return s.repo.GetAll(ctx)
}

func (s *permissionService) GetByID(ctx context.Context, id string) (*Permission, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *permissionService) Create(ctx context.Context, p *Permission) error {
	return s.repo.Create(ctx, p)
}

func (s *permissionService) Delete(ctx context.Context, id string) error {
	err := s.repo.Delete(ctx, id)
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.DeletePattern(ctx, "perms:*")
	}
	return err
}

func (s *permissionService) GetPermissionsByRoleID(ctx context.Context, roleID string) ([]Permission, error) {
	if cache.GlobalCache != nil {
		var cached []Permission
		if err := cache.GlobalCache.Get(ctx, "perms:role:"+roleID, &cached); err == nil {
			return cached, nil
		}
	}

	res, err := s.repo.GetPermissionsByRoleID(ctx, roleID)
	if err == nil && cache.GlobalCache != nil {
		_ = cache.GlobalCache.Set(ctx, "perms:role:"+roleID, res, 12*time.Hour)
	}
	return res, err
}

func (s *permissionService) AssignPermissionsToRole(ctx context.Context, roleID string, permissionIDs []string) error {
	var uuids []uuid.UUID
	for _, idStr := range permissionIDs {
		u, err := uuid.Parse(idStr)
		if err != nil {
			return err
		}
		uuids = append(uuids, u)
	}

	err := s.repo.AssignPermissionsToRole(ctx, roleID, uuids)
	if err == nil && cache.GlobalCache != nil {
		// Invalidate all dynamic permission caches in Redis in real-time
		_ = cache.GlobalCache.DeletePattern(ctx, "perms:*")
	}
	return err
}
