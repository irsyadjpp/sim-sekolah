package system

import (
	"context"

	"gorm.io/gorm"
)

type AuditRepository interface {
	Create(ctx context.Context, log *AuditLog) error
	FindAll(ctx context.Context, page int, limit int, search string, actionFilter string) ([]AuditLog, int64, error)
}

type auditRepository struct {
	db *gorm.DB
}

func NewAuditRepository(db *gorm.DB) AuditRepository {
	return &auditRepository{db: db}
}

func (r *auditRepository) Create(ctx context.Context, log *AuditLog) error {
	return r.db.WithContext(ctx).Create(log).Error
}

func (r *auditRepository) FindAll(ctx context.Context, page int, limit int, search string, actionFilter string) ([]AuditLog, int64, error) {
	var logs []AuditLog
	var total int64

	query := r.db.WithContext(ctx).Table("audit_logs").
		Select("audit_logs.*, u.full_name AS user_full_name, u.email AS user_email, imp.full_name AS impersonator_full_name, imp.email AS impersonator_email").
		Joins("LEFT JOIN auth_user u ON audit_logs.user_id = u.id").
		Joins("LEFT JOIN auth_user imp ON audit_logs.impersonator_id = imp.id")

	if actionFilter != "" {
		query = query.Where("audit_logs.action = ?", actionFilter)
	}

	if search != "" {
		searchTerm := "%" + search + "%"
		query = query.Where(
			"u.full_name ILIKE ? OR u.email ILIKE ? OR imp.full_name ILIKE ? OR audit_logs.action ILIKE ? OR audit_logs.entity ILIKE ? OR audit_logs.ip_address ILIKE ?",
			searchTerm, searchTerm, searchTerm, searchTerm, searchTerm, searchTerm,
		)
	}

	// Count total
	if err := query.Count(&total).Error; err != nil {
		return nil, 0, err
	}

	// Fetch paginated
	offset := (page - 1) * limit
	err := query.Order("audit_logs.created_at DESC").Limit(limit).Offset(offset).Find(&logs).Error
	if err != nil {
		return nil, 0, err
	}

	return logs, total, nil
}
