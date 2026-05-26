package database_monitoring

import (
	"time"
)

// DatabaseMetrics represents overall database performance metrics
type DatabaseMetrics struct {
	TotalSizeBytes     int64     `json:"total_size_bytes"`
	TotalSizeFormatted string    `json:"total_size_formatted"`
	TotalTables        int       `json:"total_tables"`
	TotalIndexes       int       `json:"total_indexes"`
	TotalSequences     int       `json:"total_sequences"`
	ActiveConnections  int       `json:"active_connections"`
	MaxConnections     int       `json:"max_connections"`
	CacheHitRatio      float64   `json:"cache_hit_ratio"`
	CollectedAt        time.Time `json:"collected_at"`
}

// TableSize represents size information for a specific table
type TableSize struct {
	SchemaName         string `json:"schema_name"`
	TableName          string `json:"table_name"`
	SizeBytes          int64  `json:"size_bytes"`
	SizeFormatted      string `json:"size_formatted"`
	PartitionType      string `json:"partition_type"`
	RowCount           int64  `json:"row_count"`
	IndexSizeBytes     int64  `json:"index_size_bytes"`
	IndexSizeFormatted string `json:"index_size_formatted"`
}

// IndexUsage represents index usage statistics
type IndexUsage struct {
	SchemaName         string `json:"schema_name"`
	TableName          string `json:"table_name"`
	IndexName          string `json:"index_name"`
	IndexScans         int64  `json:"index_scans"`
	TuplesRead         int64  `json:"tuples_read"`
	TuplesFetched      int64  `json:"tuples_fetched"`
	IndexSizeBytes     int64  `json:"index_size_bytes"`
	IndexSizeFormatted string `json:"index_size_formatted"`
	Recommendation     string `json:"recommendation"`
	Priority           string `json:"priority"`
}

// TableStatistics represents table statistics for maintenance
type TableStatistics struct {
	SchemaName        string     `json:"schema_name"`
	TableName         string     `json:"table_name"`
	LiveTuples        int64      `json:"live_tuples"`
	DeadTuples        int64      `json:"dead_tuples"`
	LastVacuum        *time.Time `json:"last_vacuum"`
	LastAutoVacuum    *time.Time `json:"last_auto_vacuum"`
	VacuumCount       int        `json:"vacuum_count"`
	AutoVacuumCount   int        `json:"auto_vacuum_count"`
	BloatPercentage   float64    `json:"bloat_percentage"`
	RequiresAction    bool       `json:"requires_action"`
	RecommendedAction string     `json:"recommended_action"`
}

// SlowQuery represents slow query information
type SlowQuery struct {
	Query        string    `json:"query"`
	Calls        int64     `json:"calls"`
	TotalTime    float64   `json:"total_time_ms"`
	MeanTime     float64   `json:"mean_time_ms"`
	MaxTime      float64   `json:"max_time_ms"`
	Rows         int64     `json:"rows"`
	LastExecuted time.Time `json:"last_executed"`
}

// SecurityEvent represents security-related events
type SecurityEvent struct {
	ID               string    `json:"id"`
	EventType        string    `json:"event_type"`
	EventDescription string    `json:"event_description"`
	Severity         string    `json:"severity"`
	UserID           string    `json:"user_id"`
	IPAddress        string    `json:"ip_address"`
	EventTime        time.Time `json:"event_time"`
	AdditionalData   string    `json:"additional_data"`
}

// SecurityReport represents security compliance report
type SecurityReport struct {
	ReportSection string `json:"report_section"`
	MetricName    string `json:"metric_name"`
	MetricValue   string `json:"metric_value"`
	Status        string `json:"status"`
}

// MaintenanceRecommendation represents maintenance suggestions
type MaintenanceRecommendation struct {
	TableName       string `json:"table_name"`
	ActionRequired  string `json:"action_required"`
	Priority        string `json:"priority"`
	Reason          string `json:"reason"`
	EstimatedImpact string `json:"estimated_impact"`
}

// DatabaseHealth represents overall database health status
type DatabaseHealth struct {
	OverallStatus   string    `json:"overall_status"`
	HealthScore     int       `json:"health_score"`
	Issues          []string  `json:"issues"`
	Recommendations []string  `json:"recommendations"`
	LastCheck       time.Time `json:"last_check"`
}

// PartitionInfo represents partition information
type PartitionInfo struct {
	SchemaName     string `json:"schema_name"`
	TableName      string `json:"table_name"`
	PartitionType  string `json:"partition_type"`
	SizeBytes      int64  `json:"size_bytes"`
	SizeFormatted  string `json:"size_formatted"`
	RowCount       int64  `json:"row_count"`
	PartitionKey   string `json:"partition_key"`
	PartitionCount int    `json:"partition_count"`
}

// ConnectionPoolStats represents connection pool statistics
type ConnectionPoolStats struct {
	ActiveConnections  int     `json:"active_connections"`
	IdleConnections    int     `json:"idle_connections"`
	WaitingConnections int     `json:"waiting_connections"`
	MaxConnections     int     `json:"max_connections"`
	PoolUtilization    float64 `json:"pool_utilization"`
	AverageWaitTime    float64 `json:"average_wait_time_ms"`
}

// QueryPerformance represents query performance metrics
type QueryPerformance struct {
	QueryType    string  `json:"query_type"`
	TotalQueries int64   `json:"total_queries"`
	AverageTime  float64 `json:"average_time_ms"`
	MaxTime      float64 `json:"max_time_ms"`
	SlowQueries  int64   `json:"slow_queries"`
	ErrorRate    float64 `json:"error_rate"`
	CacheHitRate float64 `json:"cache_hit_rate"`
}

// BackupStatus represents backup and recovery status
type BackupStatus struct {
	LastBackupTime      *time.Time `json:"last_backup_time"`
	BackupSizeBytes     int64      `json:"backup_size_bytes"`
	BackupSizeFormatted string     `json:"backup_size_formatted"`
	BackupStatus        string     `json:"backup_status"`
	BackupRetention     string     `json:"backup_retention"`
	NextScheduledBackup *time.Time `json:"next_scheduled_backup"`
}
