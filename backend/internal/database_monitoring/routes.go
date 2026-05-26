package database_monitoring

import (
	"github.com/gofiber/fiber/v2"
	"gorm.io/gorm"
)

// SetupRoutes sets up database monitoring routes
func SetupRoutes(app fiber.Router, db *gorm.DB) {
	sqlDB, err := db.DB()
	if err != nil {
		panic("Failed to get database connection: " + err.Error())
	}
	repo := NewRepository(sqlDB)
	service := NewService(repo)
	handler := NewHandler(service)

	monitoring := app.Group("/api/database-monitoring")
	{
		// Database metrics and statistics
		monitoring.Get("/metrics", handler.GetDatabaseMetrics)
		monitoring.Get("/health", handler.GetDatabaseHealth)

		// Table monitoring
		monitoring.Get("/tables/sizes", handler.GetTableSizes)
		monitoring.Get("/tables/statistics", handler.GetTableStatistics)

		// Index monitoring
		monitoring.Get("/indexes/usage", handler.GetIndexUsage)

		// Query monitoring
		monitoring.Get("/queries/slow", handler.GetSlowQueries)

		// Connection monitoring
		monitoring.Get("/connection-pool", handler.GetConnectionPoolStats)

		// Partition monitoring
		monitoring.Get("/partitions", handler.GetPartitionInfo)

		// Security monitoring
		monitoring.Get("/security/events", handler.GetSecurityEvents)
		monitoring.Get("/security/report", handler.GenerateSecurityReport)
		monitoring.Post("/security/log", handler.LogSecurityEvent)

		// Maintenance operations
		monitoring.Get("/maintenance/recommendations", handler.GetMaintenanceRecommendations)
		monitoring.Post("/maintenance/execute", handler.PerformMaintenance)

		// Database optimization
		monitoring.Post("/optimization/execute", handler.OptimizeDatabase)

		// Backup operations
		monitoring.Get("/backup/status", handler.GetBackupStatus)
		monitoring.Post("/backup/create", handler.CreateBackup)
	}
}
