package common

import (
	"context"
	"errors"

	"sim-sekolah/config"

	"github.com/google/uuid"
)

// CheckOwnership memverifikasi apakah user yang merequest berhak mengubah resource ini.
// SUPER_ADMIN selalu diizinkan. GURU hanya diizinkan jika mereka adalah pembuatnya.
func CheckOwnership(ctx context.Context, resourceCreatedBy *uuid.UUID) error {
	rolesStr, ok := ctx.Value("roles").([]string)
	if !ok {
		return errors.New("unauthorized: no roles found in context")
	}

	isSuperAdmin := false
	for _, r := range rolesStr {
		if r == "SUPER_ADMIN" || r == "ADMIN" {
			isSuperAdmin = true
			break
		}
	}

	// SUPER_ADMIN bebas melakukan apapun
	if isSuperAdmin {
		return nil
	}

	// Jika bukan SUPER_ADMIN, cek apakah resource ini dibuat oleh user tersebut
	userIDStr, ok := ctx.Value("user_id").(string)
	if !ok {
		return errors.New("unauthorized: no user ID found in context")
	}

	if resourceCreatedBy == nil {
		return errors.New("forbidden: you cannot modify a system-created resource")
	}

	if resourceCreatedBy.String() != userIDStr {
		return errors.New("forbidden: you are not the owner of this resource")
	}

	return nil
}

// CheckTeachingAssignmentOwnership memverifikasi apakah user (GURU) berhak mengelola data (misal: assessment)
// yang terkait dengan suatu teaching_assignment_id.
func CheckTeachingAssignmentOwnership(ctx context.Context, assignmentID string) error {
	rolesStr, ok := ctx.Value("roles").([]string)
	if !ok {
		return errors.New("unauthorized: no roles found in context")
	}

	isSuperAdminOrAdmin := false
	for _, r := range rolesStr {
		if r == "SUPER_ADMIN" || r == "ADMIN_SEKOLAH" || r == "ADMIN" {
			isSuperAdminOrAdmin = true
			break
		}
	}

	// SUPER_ADMIN dan ADMIN_SEKOLAH diizinkan
	if isSuperAdminOrAdmin {
		return nil
	}

	userIDStr, ok := ctx.Value("user_id").(string)
	if !ok {
		return errors.New("unauthorized: no user ID found in context")
	}

	// Ambil data User untuk mengetahui teacher_id nya
	var teacherIDStr string
	err := config.DB.WithContext(ctx).
		Table("users").
		Select("CAST(teacher_id AS VARCHAR)").
		Where("id = ?", userIDStr).
		Scan(&teacherIDStr).Error

	if err != nil || teacherIDStr == "" {
		return errors.New("forbidden: user is not associated with any teacher profile")
	}

	// Cek apakah teaching_assignment ini dimiliki oleh guru tersebut
	var count int64
	err = config.DB.WithContext(ctx).
		Table("teaching_assignments").
		Where("id = ? AND teacher_id = ?", assignmentID, teacherIDStr).
		Count(&count).Error

	if err != nil || count == 0 {
		return errors.New("forbidden: you don't have permission to modify this resource")
	}

	return nil
}
