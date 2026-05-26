package database_monitoring

import (
	"context"
	"fmt"
	"time"
)

// Service handles database monitoring business logic
type Service struct {
	repo *Repository
}

// NewService creates a new database monitoring service
func NewService(repo *Repository) *Service {
	return &Service{repo: repo}
}

// GetDatabaseMetrics retrieves overall database performance metrics
func (s *Service) GetDatabaseMetrics(ctx context.Context, req DatabaseMetricsRequest) (*DatabaseMetrics, error) {
	metrics, err := s.repo.GetDatabaseMetrics(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get database metrics: %w", err)
	}

	// Calculate health score based on metrics
	metrics.TotalSizeFormatted = formatBytes(metrics.TotalSizeBytes)

	return metrics, nil
}

// GetTableSizes retrieves size information for tables
func (s *Service) GetTableSizes(ctx context.Context, req TableSizeRequest) ([]TableSize, int, error) {
	limit := req.Limit
	if limit <= 0 || limit > 100 {
		limit = 50 // Default limit
	}

	offset := req.Offset
	if offset < 0 {
		offset = 0
	}

	tableSizes, total, err := s.repo.GetTableSizes(ctx, req.SchemaName, req.TableName, limit, offset)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to get table sizes: %w", err)
	}

	return tableSizes, total, nil
}

// GetIndexUsage retrieves index usage statistics
func (s *Service) GetIndexUsage(ctx context.Context, req IndexUsageRequest) ([]IndexUsage, int, error) {
	limit := req.Limit
	if limit <= 0 || limit > 100 {
		limit = 50 // Default limit
	}

	minScans := req.MinScans
	if minScans < 0 {
		minScans = 0
	}

	indexUsages, total, err := s.repo.GetIndexUsage(ctx, req.SchemaName, req.TableName, req.ShowUnused, minScans, limit)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to get index usage: %w", err)
	}

	return indexUsages, total, nil
}

// GetTableStatistics retrieves table statistics for maintenance
func (s *Service) GetTableStatistics(ctx context.Context) ([]TableStatistics, error) {
	tableStats, err := s.repo.GetTableStatistics(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get table statistics: %w", err)
	}

	return tableStats, nil
}

// GetSecurityEvents retrieves security-related events
func (s *Service) GetSecurityEvents(ctx context.Context, req SecurityReportRequest) ([]SecurityEvent, error) {
	limit := 100 // Default limit
	if req.TimeRange == "" {
		req.TimeRange = "24h" // Default time range
	}
	if req.Severity == "" {
		req.Severity = "ALL" // Default severity
	}

	events, err := s.repo.GetSecurityEvents(ctx, req.TimeRange, req.Severity, limit)
	if err != nil {
		return nil, fmt.Errorf("failed to get security events: %w", err)
	}

	return events, nil
}

// GenerateSecurityReport generates a security compliance report
func (s *Service) GenerateSecurityReport(ctx context.Context, req SecurityReportRequest) ([]SecurityReport, error) {
	reports, err := s.repo.GenerateSecurityReport(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to generate security report: %w", err)
	}

	return reports, nil
}

// GetMaintenanceRecommendations retrieves maintenance recommendations
func (s *Service) GetMaintenanceRecommendations(ctx context.Context) ([]MaintenanceRecommendation, error) {
	recommendations, err := s.repo.GetMaintenanceRecommendations(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get maintenance recommendations: %w", err)
	}

	return recommendations, nil
}

// PerformMaintenance performs maintenance operations on tables
func (s *Service) PerformMaintenance(ctx context.Context, req MaintenanceRequest) (*MaintenanceResponse, error) {
	response := &MaintenanceResponse{
		Operation: req.Operation,
		TableName: req.TableName,
		Success:   true,
		Message:   "Maintenance operation completed successfully",
	}

	if req.DryRun {
		response.Message = "Dry run completed - no changes made"
		return response, nil
	}

	startTime := time.Now()

	switch req.Operation {
	case "vacuum":
		err := s.repo.ExecuteVacuum(ctx, req.TableName)
		if err != nil {
			response.Success = false
			response.Message = fmt.Sprintf("VACUUM failed: %v", err)
			return response, nil
		}
		response.Message = "VACUUM completed successfully"

	case "analyze":
		err := s.repo.ExecuteAnalyze(ctx, req.TableName)
		if err != nil {
			response.Success = false
			response.Message = fmt.Sprintf("ANALYZE failed: %v", err)
			return response, nil
		}
		response.Message = "ANALYZE completed successfully"

	case "reindex":
		err := s.repo.ExecuteReindex(ctx, req.TableName)
		if err != nil {
			response.Success = false
			response.Message = fmt.Sprintf("REINDEX failed: %v", err)
			return response, nil
		}
		response.Message = "REINDEX completed successfully"

	case "cluster":
		err := s.repo.ExecuteCluster(ctx, req.TableName)
		if err != nil {
			response.Success = false
			response.Message = fmt.Sprintf("CLUSTER failed: %v", err)
			return response, nil
		}
		response.Message = "CLUSTER completed successfully"

	default:
		response.Success = false
		response.Message = fmt.Sprintf("Unknown operation: %s", req.Operation)
		return response, nil
	}

	response.Duration = time.Since(startTime).String()
	return response, nil
}

// GetDatabaseHealth performs a comprehensive health check
func (s *Service) GetDatabaseHealth(ctx context.Context, req HealthCheckRequest) (*DatabaseHealth, error) {
	health := &DatabaseHealth{
		LastCheck: time.Now(),
	}

	// Get basic metrics
	metrics, err := s.repo.GetDatabaseMetrics(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get database metrics for health check: %w", err)
	}

	// Calculate health score based on various factors
	healthScore := 100
	issues := []string{}
	recommendations := []string{}

	// Check cache hit ratio
	if metrics.CacheHitRatio < 0.95 {
		healthScore -= 10
		issues = append(issues, fmt.Sprintf("Low cache hit ratio: %.2f%%", metrics.CacheHitRatio*100))
		recommendations = append(recommendations, "Consider increasing shared_buffers or review query patterns")
	}

	// Check connection pool utilization
	poolUtilization := float64(metrics.ActiveConnections) / float64(metrics.MaxConnections)
	if poolUtilization > 0.8 {
		healthScore -= 15
		issues = append(issues, fmt.Sprintf("High connection pool utilization: %.1f%%", poolUtilization*100))
		recommendations = append(recommendations, "Consider increasing max_connections or implementing connection pooling")
	}

	// Check for table bloat
	tableStats, err := s.repo.GetTableStatistics(ctx)
	if err == nil {
		for _, stat := range tableStats {
			if stat.BloatPercentage > 20 {
				healthScore -= 5
				issues = append(issues, fmt.Sprintf("High table bloat in %s: %.1f%%", stat.TableName, stat.BloatPercentage))
			}
		}
		if len(tableStats) > 0 {
			recommendations = append(recommendations, "Run VACUUM ANALYZE on tables with high bloat")
		}
	}

	// Check for unused indexes
	indexUsages, _, err := s.repo.GetIndexUsage(ctx, "", "", true, 0, 10)
	if err == nil && len(indexUsages) > 0 {
		healthScore -= 5
		issues = append(issues, fmt.Sprintf("Found %d unused indexes", len(indexUsages)))
		recommendations = append(recommendations, "Review and drop unused indexes to improve performance")
	}

	// Set overall status
	if healthScore >= 90 {
		health.OverallStatus = "HEALTHY"
	} else if healthScore >= 70 {
		health.OverallStatus = "WARNING"
	} else {
		health.OverallStatus = "CRITICAL"
	}

	health.HealthScore = healthScore
	health.Issues = issues
	health.Recommendations = recommendations

	return health, nil
}

// OptimizeDatabase performs database optimization operations
func (s *Service) OptimizeDatabase(ctx context.Context, req DatabaseOptimizationRequest) (*DatabaseOptimizationResponse, error) {
	response := &DatabaseOptimizationResponse{
		OptimizationType: req.OptimizationType,
		Success:          true,
		Message:          "Database optimization completed successfully",
	}

	if !req.Confirm {
		response.Success = false
		response.Message = "Confirmation required. Set confirm=true to proceed with optimization."
		return response, nil
	}

	startTime := time.Now()
	improvements := []string{}
	tablesProcessed := 0
	indexesOptimized := 0

	switch req.OptimizationType {
	case "all":
		// Perform all optimization operations
		tableStats, err := s.repo.GetTableStatistics(ctx)
		if err != nil {
			response.Success = false
			response.Message = fmt.Sprintf("Failed to get table statistics: %v", err)
			return response, nil
		}

		for _, stat := range tableStats {
			if stat.RequiresAction {
				err := s.repo.ExecuteVacuum(ctx, stat.TableName)
				if err == nil {
					tablesProcessed++
					improvements = append(improvements, fmt.Sprintf("VACUUM completed on %s", stat.TableName))
				}
			}
		}

		// Optimize indexes
		indexUsages, _, err := s.repo.GetIndexUsage(ctx, "", "", true, 0, 100)
		if err == nil {
			for _, idx := range indexUsages {
				if idx.IndexScans == 0 {
					// Log recommendation for unused index
					improvements = append(improvements, fmt.Sprintf("Unused index identified: %s.%s", idx.TableName, idx.IndexName))
					indexesOptimized++
				}
			}
		}

	case "statistics":
		// Update statistics only
		tableStats, err := s.repo.GetTableStatistics(ctx)
		if err != nil {
			response.Success = false
			response.Message = fmt.Sprintf("Failed to get table statistics: %v", err)
			return response, nil
		}

		for _, stat := range tableStats {
			if stat.RequiresAction {
				err := s.repo.ExecuteAnalyze(ctx, stat.TableName)
				if err == nil {
					tablesProcessed++
					improvements = append(improvements, fmt.Sprintf("ANALYZE completed on %s", stat.TableName))
				}
			}
		}

	case "indexes":
		// Optimize indexes only
		indexUsages, _, err := s.repo.GetIndexUsage(ctx, "", "", true, 0, 100)
		if err != nil {
			response.Success = false
			response.Message = fmt.Sprintf("Failed to get index usage: %v", err)
			return response, nil
		}

		for _, idx := range indexUsages {
			if idx.IndexScans == 0 {
				improvements = append(improvements, fmt.Sprintf("Unused index: %s.%s (consider dropping)", idx.TableName, idx.IndexName))
				indexesOptimized++
			}
		}

	case "vacuum":
		// Run vacuum only
		tableStats, err := s.repo.GetTableStatistics(ctx)
		if err != nil {
			response.Success = false
			response.Message = fmt.Sprintf("Failed to get table statistics: %v", err)
			return response, nil
		}

		for _, stat := range tableStats {
			if stat.BloatPercentage > 5 {
				err := s.repo.ExecuteVacuum(ctx, stat.TableName)
				if err == nil {
					tablesProcessed++
					improvements = append(improvements, fmt.Sprintf("VACUUM completed on %s", stat.TableName))
				}
			}
		}

	default:
		response.Success = false
		response.Message = fmt.Sprintf("Unknown optimization type: %s", req.OptimizationType)
		return response, nil
	}

	response.TablesProcessed = tablesProcessed
	response.IndexesOptimized = indexesOptimized
	response.Improvements = improvements
	response.Duration = time.Since(startTime).String()

	return response, nil
}

// Additional repository methods that need to be added

func (r *Repository) ExecuteVacuum(ctx context.Context, tableName string) error {
	_, err := r.db.ExecContext(ctx, fmt.Sprintf("VACUUM ANALYZE %s", tableName))
	return err
}

func (r *Repository) ExecuteAnalyze(ctx context.Context, tableName string) error {
	_, err := r.db.ExecContext(ctx, fmt.Sprintf("ANALYZE %s", tableName))
	return err
}

func (r *Repository) ExecuteReindex(ctx context.Context, tableName string) error {
	_, err := r.db.ExecContext(ctx, fmt.Sprintf("REINDEX TABLE %s", tableName))
	return err
}

func (r *Repository) ExecuteCluster(ctx context.Context, tableName string) error {
	// Get the primary key index for clustering
	var pkIndex string
	err := r.db.QueryRowContext(ctx,
		fmt.Sprintf("SELECT indexname FROM pg_indexes WHERE tablename = '%s' AND indexname LIKE '%s_pkey'", tableName, tableName)).Scan(&pkIndex)
	if err != nil {
		return fmt.Errorf("failed to find primary key index: %w", err)
	}

	_, err = r.db.ExecContext(ctx, fmt.Sprintf("CLUSTER %s USING %s", tableName, pkIndex))
	return err
}
