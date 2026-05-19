package permission

import (
	"context"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type PermissionRepository interface {
	GetAll(ctx context.Context) ([]Permission, error)
	GetByID(ctx context.Context, id string) (*Permission, error)
	Create(ctx context.Context, p *Permission) error
	Delete(ctx context.Context, id string) error
	GetPermissionsByRoleID(ctx context.Context, roleID string) ([]Permission, error)
	AssignPermissionsToRole(ctx context.Context, roleID string, permissionIDs []uuid.UUID) error
}

type permissionRepository struct {
	db *gorm.DB
}

func NewPermissionRepository(db *gorm.DB) PermissionRepository {
	return &permissionRepository{db: db}
}

func (r *permissionRepository) GetAll(ctx context.Context) ([]Permission, error) {
	var permissions []Permission
	err := r.db.WithContext(ctx).Order("permission_name ASC").Find(&permissions).Error
	return permissions, err
}

func (r *permissionRepository) GetByID(ctx context.Context, id string) (*Permission, error) {
	var p Permission
	err := r.db.WithContext(ctx).First(&p, "id = ?", id).Error
	if err != nil {
		return nil, err
	}
	return &p, nil
}

func (r *permissionRepository) Create(ctx context.Context, p *Permission) error {
	return r.db.WithContext(ctx).Create(p).Error
}

func (r *permissionRepository) Delete(ctx context.Context, id string) error {
	return r.db.WithContext(ctx).Delete(&Permission{}, "id = ?", id).Error
}

func (r *permissionRepository) GetPermissionsByRoleID(ctx context.Context, roleID string) ([]Permission, error) {
	var permissions []Permission
	err := r.db.WithContext(ctx).Table("auth_permission p").
		Joins("JOIN auth_role_permission rp ON rp.permission_id = p.id").
		Where("rp.role_id = ?", roleID).
		Order("p.permission_name ASC").
		Find(&permissions).Error
	return permissions, err
}

func (r *permissionRepository) AssignPermissionsToRole(ctx context.Context, roleID string, permissionIDs []uuid.UUID) error {
	return r.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		// Hapus pemetaan lama terlebih dahulu
		if err := tx.Exec("DELETE FROM auth_role_permission WHERE role_id = ?", roleID).Error; err != nil {
			return err
		}

		if len(permissionIDs) == 0 {
			return nil
		}

		type RolePermission struct {
			RoleID       uuid.UUID `gorm:"column:role_id"`
			PermissionID uuid.UUID `gorm:"column:permission_id"`
		}

		var mappings []RolePermission
		rUUID, err := uuid.Parse(roleID)
		if err != nil {
			return err
		}

		for _, pID := range permissionIDs {
			mappings = append(mappings, RolePermission{
				RoleID:       rUUID,
				PermissionID: pID,
			})
		}

		return tx.Table("auth_role_permission").Create(&mappings).Error
	})
}
