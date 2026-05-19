package system

import (
	"context"
	"time"

	"github.com/google/uuid"
	"sim-sekolah/pkg/logger"
)

type AuditService interface {
	LogEvent(ctx context.Context, userIDStr string, action string, entity string, entityID string, ipAddress string)
	GetAuditLogs(ctx context.Context, page int, limit int, search string, actionFilter string) ([]AuditLog, int64, error)
}

type auditService struct {
	repo AuditRepository
}

var GlobalAuditService AuditService

func NewAuditService(repo AuditRepository) AuditService {
	svc := &auditService{repo: repo}
	GlobalAuditService = svc
	return svc
}

func (s *auditService) LogEvent(ctx context.Context, userIDStr string, action string, entity string, entityID string, ipAddress string) {
	// Run asynchronously to avoid blocking the main request cycle
	go func() {
		bgCtx := context.Background()

		var uID *uuid.UUID
		if userIDStr != "" {
			parsedID, err := uuid.Parse(userIDStr)
			if err == nil {
				uID = &parsedID
			}
		}

		log := &AuditLog{
			ID:        uuid.New(),
			UserID:    uID,
			Action:    action,
			Entity:    entity,
			EntityID:  entityID,
			IPAddress: ipAddress,
			CreatedAt: time.Now(),
		}

		if err := s.repo.Create(bgCtx, log); err != nil {
			logger.Error("Failed to persist audit log into database", err)
		} else {
			// Also log it structured to stdout/observability pipeline
			actorName := "System"
			if userIDStr != "" {
				actorName = userIDStr
			}
			logger.Audit(bgCtx, action, actorName, entity, "entity_id", entityID, "ip_address", ipAddress)
		}
	}()
}

func (s *auditService) GetAuditLogs(ctx context.Context, page int, limit int, search string, actionFilter string) ([]AuditLog, int64, error) {
	if page <= 0 {
		page = 1
	}
	if limit <= 0 {
		limit = 10
	}
	return s.repo.FindAll(ctx, page, limit, search, actionFilter)
}
