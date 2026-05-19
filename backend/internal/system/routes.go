package system

import (
	"sim-sekolah/pkg/middleware"

	"github.com/gofiber/fiber/v2"
	"github.com/redis/go-redis/v9"
	"gorm.io/gorm"
)

func SetupRoutes(api fiber.Router, db *gorm.DB, rdb *redis.Client) {
	repo := NewSystemRepository(db)
	svc := NewSystemService(repo, rdb)

	auditRepo := NewAuditRepository(db)
	auditSvc := NewAuditService(auditRepo)

	h := NewHandler(svc, auditSvc)

	group := api.Group("/dashboard")
	group.Use(middleware.Protected())

	group.Get("/pimpinan", h.GetPimpinan)
	group.Get("/guru", h.GetGuru)
	group.Get("/operator", h.GetOperator)

	// API System Audit Logs
	sysGroup := api.Group("/system")
	sysGroup.Use(middleware.Protected())
	sysGroup.Get("/audit-logs", h.GetAuditLogs)
}
