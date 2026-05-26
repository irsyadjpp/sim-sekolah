package database_monitoring

import (
	"context"
	"database/sql"
	"fmt"
	"time"
)

// Repository handles database monitoring data access
type Repository struct {
	db *sql.DB
}

// NewRepository creates a new database monitoring repository
func NewRepository(db *sql.DB) *Repository {
	return &Repository{db: db}
}

// GetDatabaseMetrics retrieves overall database performance metrics
func (r *Repository) GetDatabaseMetrics(ctx context.Context) (*DatabaseMetrics, error) {
	metrics := &DatabaseMetrics{
		CollectedAt: time.Now(),
	}

	// Get total database size
	var totalSize int64
	err := r.db.QueryRowContext(ctx,
		"SELECT pg_database_size(current_database())").Scan(&totalSize)
	if err != nil {
		return nil, fmt.Errorf("failed to get database size: %w", err)
	}
	metrics.TotalSizeBytes = totalSize
	metrics.TotalSizeFormatted = formatBytes(totalSize)

	// Get total tables
	err = r.db.QueryRowContext(ctx,
		"SELECT COUNT(*) FROM pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema')").Scan(&metrics.TotalTables)
	if err != nil {
		return nil, fmt.Errorf("failed to get table count: %w", err)
	}

	// Get total indexes
	err = r.db.QueryRowContext(ctx,
		"SELECT COUNT(*) FROM pg_indexes WHERE schemaname NOT IN ('pg_catalog', 'information_schema')").Scan(&metrics.TotalIndexes)
	if err != nil {
		return nil, fmt.Errorf("failed to get index count: %w", err)
	}

	// Get total sequences
	err = r.db.QueryRowContext(ctx, "SELECT COUNT(*) FROM pg_sequences").Scan(&metrics.TotalSequences)
	if err != nil {
		return nil, fmt.Errorf("failed to get sequence count: %w", err)
	}

	// Get connection statistics
	err = r.db.QueryRowContext(ctx,
		"SELECT COUNT(*) FROM pg_stat_activity").Scan(&metrics.ActiveConnections)
	if err != nil {
		return nil, fmt.Errorf("failed to get active connections: %w", err)
	}

	// Get max connections
	err = r.db.QueryRowContext(ctx, "SHOW max_connections").Scan(&metrics.MaxConnections)
	if err != nil {
		return nil, fmt.Errorf("failed to get max connections: %w", err)
	}

	// Get cache hit ratio
	err = r.db.QueryRowContext(ctx,
		"SELECT round(sum(blks_hit)::numeric / (sum(blks_hit) + sum(blks_read))::numeric, 4) FROM pg_stat_database WHERE datname = current_database()").Scan(&metrics.CacheHitRatio)
	if err != nil {
		return nil, fmt.Errorf("failed to get cache hit ratio: %w", err)
	}

	return metrics, nil
}

// GetTableSizes retrieves size information for tables
func (r *Repository) GetTableSizes(ctx context.Context, schemaName, tableName string, limit, offset int) ([]TableSize, int, error) {
	query := `
		SELECT 
			schemaname,
			tablename,
			pg_total_relation_size(schemaname::text||'.'||tablename) as size_bytes,
			pg_relation_size(schemaname::text||'.'||tablename) - pg_total_relation_size(schemaname::text||'.'||tablename) as bloat_bytes,
			COALESCE((SELECT n_live_tup FROM pg_stat_user_tables WHERE schemaname = t.schemaname AND relname = t.tablename), 0) as row_count
		FROM pg_tables t
		WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
	`

	args := []interface{}{}
	argCount := 1

	if schemaName != "" {
		query += fmt.Sprintf(" AND schemaname = $%d", argCount)
		args = append(args, schemaName)
		argCount++
	}

	if tableName != "" {
		query += fmt.Sprintf(" AND tablename ILIKE $%d", argCount)
		args = append(args, "%"+tableName+"%")
		argCount++
	}

	// Get total count
	countQuery := "SELECT COUNT(*) FROM (" + query + ") as count_query"
	var total int
	err := r.db.QueryRowContext(ctx, countQuery, args...).Scan(&total)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to get table count: %w", err)
	}

	// Add pagination
	query += " ORDER BY pg_total_relation_size(schemaname::text||'.'||tablename) DESC"
	if limit > 0 {
		query += fmt.Sprintf(" LIMIT $%d", argCount)
		args = append(args, limit)
		argCount++
	}
	if offset > 0 {
		query += fmt.Sprintf(" OFFSET $%d", argCount)
		args = append(args, offset)
	}

	rows, err := r.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to query table sizes: %w", err)
	}
	defer rows.Close()

	var tableSizes []TableSize
	for rows.Next() {
		var ts TableSize
		var bloatBytes int64
		err := rows.Scan(
			&ts.SchemaName,
			&ts.TableName,
			&ts.SizeBytes,
			&bloatBytes,
			&ts.RowCount,
		)
		if err != nil {
			return nil, 0, fmt.Errorf("failed to scan table size: %w", err)
		}

		ts.SizeFormatted = formatBytes(ts.SizeBytes)
		ts.IndexSizeBytes = ts.SizeBytes - bloatBytes
		ts.IndexSizeFormatted = formatBytes(ts.IndexSizeBytes)
		ts.PartitionType = "REGULAR"

		tableSizes = append(tableSizes, ts)
	}

	return tableSizes, total, nil
}

// GetIndexUsage retrieves index usage statistics
func (r *Repository) GetIndexUsage(ctx context.Context, schemaName, tableName string, showUnused bool, minScans int, limit int) ([]IndexUsage, int, error) {
	query := `
		SELECT 
			schemaname,
			tablename,
			indexname,
			idx_scan as index_scans,
			idx_tup_read as tuples_read,
			idx_tup_fetch as tuples_fetched,
			pg_relation_size(indexrelid) as index_size
		FROM pg_stat_user_indexes
		WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
	`

	args := []interface{}{}
	argCount := 1

	if schemaName != "" {
		query += fmt.Sprintf(" AND schemaname = $%d", argCount)
		args = append(args, schemaName)
		argCount++
	}

	if tableName != "" {
		query += fmt.Sprintf(" AND tablename ILIKE $%d", argCount)
		args = append(args, "%"+tableName+"%")
		argCount++
	}

	if showUnused {
		query += " AND idx_scan = 0"
	}

	if minScans > 0 {
		query += fmt.Sprintf(" AND idx_scan >= $%d", argCount)
		args = append(args, minScans)
		argCount++
	}

	// Get total count
	countQuery := "SELECT COUNT(*) FROM (" + query + ") as count_query"
	var total int
	err := r.db.QueryRowContext(ctx, countQuery, args...).Scan(&total)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to get index count: %w", err)
	}

	query += " ORDER BY idx_scan ASC, idx_tup_read ASC"
	if limit > 0 {
		query += fmt.Sprintf(" LIMIT $%d", argCount)
		args = append(args, limit)
	}

	rows, err := r.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, 0, fmt.Errorf("failed to query index usage: %w", err)
	}
	defer rows.Close()

	var indexUsages []IndexUsage
	for rows.Next() {
		var iu IndexUsage
		err := rows.Scan(
			&iu.SchemaName,
			&iu.TableName,
			&iu.IndexName,
			&iu.IndexScans,
			&iu.TuplesRead,
			&iu.TuplesFetched,
			&iu.IndexSizeBytes,
		)
		if err != nil {
			return nil, 0, fmt.Errorf("failed to scan index usage: %w", err)
		}

		iu.IndexSizeFormatted = formatBytes(iu.IndexSizeBytes)
		iu.Recommendation = generateIndexRecommendation(iu.IndexScans, iu.TuplesRead, iu.IndexSizeBytes)
		iu.Priority = generateIndexPriority(iu.IndexScans, iu.TuplesRead)

		indexUsages = append(indexUsages, iu)
	}

	return indexUsages, total, nil
}

// GetTableStatistics retrieves table statistics for maintenance
func (r *Repository) GetTableStatistics(ctx context.Context) ([]TableStatistics, error) {
	query := `
		SELECT 
			schemaname,
			tablename,
			n_live_tup as live_tuples,
			n_dead_tup as dead_tuples,
			last_vacuum,
			last_autovacuum,
			vacuum_count,
			autovacuum_count
		FROM pg_stat_user_tables
		WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
		ORDER BY n_dead_tup DESC
	`

	rows, err := r.db.QueryContext(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("failed to query table statistics: %w", err)
	}
	defer rows.Close()

	var tableStats []TableStatistics
	for rows.Next() {
		var ts TableStatistics
		err := rows.Scan(
			&ts.SchemaName,
			&ts.TableName,
			&ts.LiveTuples,
			&ts.DeadTuples,
			&ts.LastVacuum,
			&ts.LastAutoVacuum,
			&ts.VacuumCount,
			&ts.AutoVacuumCount,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan table statistics: %w", err)
		}

		// Calculate bloat percentage
		if ts.LiveTuples > 0 {
			ts.BloatPercentage = float64(ts.DeadTuples) / float64(ts.LiveTuples) * 100
		}

		// Determine if action is required
		ts.RequiresAction = ts.BloatPercentage > 10 ||
			(ts.LastAutoVacuum != nil && time.Since(*ts.LastAutoVacuum) > 30*24*time.Hour)

		ts.RecommendedAction = generateMaintenanceRecommendation(ts.BloatPercentage, ts.LastAutoVacuum)

		tableStats = append(tableStats, ts)
	}

	return tableStats, nil
}

// GetSecurityEvents retrieves security-related events
func (r *Repository) GetSecurityEvents(ctx context.Context, timeRange string, severity string, limit int) ([]SecurityEvent, error) {
	query := `
		SELECT 
			id,
			action as event_type,
			changes->>'event_description' as event_description,
			changes->>'severity' as severity,
			actor as user_id,
			ip_address,
			created_at as event_time,
			changes->>'additional_data' as additional_data
		FROM audit_logs
		WHERE action IN ('SUSPICIOUS_LOGIN', 'UNAUTHORIZED_ACCESS', 'DATA_BREACH_ATTEMPT', 'PRIVILEGE_ESCALATION', 'SECURITY_EVENT')
	`

	args := []interface{}{}
	argCount := 1

	// Apply time range filter
	if timeRange != "" {
		var timeFilter time.Time
		switch timeRange {
		case "1h":
			timeFilter = time.Now().Add(-1 * time.Hour)
		case "24h":
			timeFilter = time.Now().Add(-24 * time.Hour)
		case "7d":
			timeFilter = time.Now().Add(-7 * 24 * time.Hour)
		case "30d":
			timeFilter = time.Now().Add(-30 * 24 * time.Hour)
		}
		query += fmt.Sprintf(" AND created_at >= $%d", argCount)
		args = append(args, timeFilter)
		argCount++
	}

	// Apply severity filter
	if severity != "" && severity != "ALL" {
		query += fmt.Sprintf(" AND changes->>'severity' = $%d", argCount)
		args = append(args, severity)
		argCount++
	}

	query += " ORDER BY created_at DESC"
	if limit > 0 {
		query += fmt.Sprintf(" LIMIT $%d", argCount)
		args = append(args, limit)
	}

	rows, err := r.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, fmt.Errorf("failed to query security events: %w", err)
	}
	defer rows.Close()

	var events []SecurityEvent
	for rows.Next() {
		var event SecurityEvent
		err := rows.Scan(
			&event.ID,
			&event.EventType,
			&event.EventDescription,
			&event.Severity,
			&event.UserID,
			&event.IPAddress,
			&event.EventTime,
			&event.AdditionalData,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan security event: %w", err)
		}

		events = append(events, event)
	}

	return events, nil
}

// GenerateSecurityReport generates a security compliance report
func (r *Repository) GenerateSecurityReport(ctx context.Context) ([]SecurityReport, error) {
	query := `
		WITH security_events AS (
			SELECT 
				COUNT(*) as event_count
			FROM audit_logs
			WHERE action IN ('SUSPICIOUS_LOGIN', 'UNAUTHORIZED_ACCESS', 'DATA_BREACH_ATTEMPT')
			AND created_at > NOW() - INTERVAL '24 hours'
		),
		failed_auth AS (
			SELECT 
				COUNT(*) as failed_count
			FROM audit_logs
			WHERE action IN ('LOGIN_FAILED', 'AUTHENTICATION_FAILED')
			AND created_at > NOW() - INTERVAL '24 hours'
		),
		high_volume_access AS (
			SELECT 
				COUNT(*) as access_count
			FROM (
				SELECT actor, COUNT(*) as cnt
				FROM audit_logs
				WHERE action IN ('SELECT', 'READ', 'VIEW')
				AND created_at > NOW() - INTERVAL '7 days'
				GROUP BY actor
				HAVING COUNT(*) > 100
			) as high_access
		)
		SELECT 
			'SECURITY_EVENTS' as report_section,
			'Total security events (24h)' as metric_name,
			event_count::text as metric_value,
			CASE WHEN event_count < 10 THEN 'OK' ELSE 'REVIEW' END as status
		FROM security_events
		UNION ALL
		SELECT 
			'AUTHENTICATION' as report_section,
			'Failed login attempts (24h)' as metric_name,
			failed_count::text as metric_value,
			CASE WHEN failed_count < 50 THEN 'OK' ELSE 'ALERT' END as status
		FROM failed_auth
		UNION ALL
		SELECT 
			'DATA_ACCESS' as report_section,
			'High-volume data access (7d)' as metric_name,
			access_count::text as metric_value,
			CASE WHEN access_count < 1000 THEN 'OK' ELSE 'REVIEW' END as status
		FROM high_volume_access
	`

	rows, err := r.db.QueryContext(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("failed to generate security report: %w", err)
	}
	defer rows.Close()

	var reports []SecurityReport
	for rows.Next() {
		var report SecurityReport
		err := rows.Scan(
			&report.ReportSection,
			&report.MetricName,
			&report.MetricValue,
			&report.Status,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan security report: %w", err)
		}

		reports = append(reports, report)
	}

	return reports, nil
}

// GetMaintenanceRecommendations retrieves maintenance recommendations
func (r *Repository) GetMaintenanceRecommendations(ctx context.Context) ([]MaintenanceRecommendation, error) {
	query := `
		WITH table_stats AS (
			SELECT 
				schemaname||'.'||tablename as tablename,
				n_live_tup,
				n_dead_tup,
				last_vacuum,
				last_autovacuum
			FROM pg_stat_user_tables
			WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
		)
		SELECT 
			tablename,
			'VACUUM' as action_required,
			CASE 
				WHEN n_dead_tup > n_live_tup * 0.1 THEN 'HIGH'
				WHEN n_dead_tup > n_live_tup * 0.05 THEN 'MEDIUM'
				ELSE 'LOW'
			END as priority,
			'High table bloat: ' || n_dead_tup || ' dead tuples out of ' || n_live_tup || ' live tuples' as reason,
			CASE 
				WHEN n_dead_tup > n_live_tup * 0.1 THEN 'Significant performance improvement expected'
				ELSE 'Moderate performance improvement expected'
			END as estimated_impact
		FROM table_stats
		WHERE n_dead_tup > n_live_tup * 0.05
		UNION ALL
		SELECT 
			tablename,
			'ANALYZE' as action_required,
			CASE 
				WHEN last_autovacuum < CURRENT_DATE - INTERVAL '7 days' THEN 'HIGH'
				WHEN last_autovacuum < CURRENT_DATE - INTERVAL '30 days' THEN 'MEDIUM'
				ELSE 'LOW'
			END as priority,
			'Statistics not updated since: ' || COALESCE(last_autovacuum::text, 'never') as reason,
			'Improved query planning and performance' as estimated_impact
		FROM table_stats
		WHERE last_autovacuum IS NULL OR last_autovacuum < CURRENT_DATE - INTERVAL '7 days'
		ORDER BY priority DESC
	`

	rows, err := r.db.QueryContext(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("failed to get maintenance recommendations: %w", err)
	}
	defer rows.Close()

	var recommendations []MaintenanceRecommendation
	for rows.Next() {
		var rec MaintenanceRecommendation
		err := rows.Scan(
			&rec.TableName,
			&rec.ActionRequired,
			&rec.Priority,
			&rec.Reason,
			&rec.EstimatedImpact,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan maintenance recommendation: %w", err)
		}

		recommendations = append(recommendations, rec)
	}

	return recommendations, nil
}

// Helper functions

func formatBytes(bytes int64) string {
	const unit = 1024
	if bytes < unit {
		return fmt.Sprintf("%d B", bytes)
	}
	div, exp := int64(unit), 0
	for n := bytes / unit; n >= unit; n /= unit {
		div *= unit
		exp++
	}
	return fmt.Sprintf("%.1f %cB", float64(bytes)/float64(div), "KMGTPE"[exp])
}

func generateIndexRecommendation(scans, tuplesRead int64, indexSize int64) string {
	if scans == 0 {
		return "Index never used - consider dropping"
	}
	if tuplesRead < 1000 {
		return "Low usage index - evaluate necessity"
	}
	if indexSize > 10*1024*1024 { // > 10MB
		return "Large index - consider optimization"
	}
	return "Index appears healthy"
}

func generateIndexPriority(scans, tuplesRead int64) string {
	if scans == 0 {
		return "HIGH"
	}
	if tuplesRead < 1000 {
		return "MEDIUM"
	}
	return "LOW"
}

func generateMaintenanceRecommendation(bloatPercentage float64, lastAutoVacuum *time.Time) string {
	if bloatPercentage > 10 {
		return "VACUUM ANALYZE recommended - high bloat detected"
	}
	if bloatPercentage > 5 {
		return "VACUUM recommended - moderate bloat detected"
	}
	if lastAutoVacuum == nil || time.Since(*lastAutoVacuum) > 30*24*time.Hour {
		return "ANALYZE recommended - statistics outdated"
	}
	return "No immediate action required"
}
