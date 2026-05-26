package database_monitoring

import "time"

// DatabaseMetricsRequest represents request parameters for database metrics
type DatabaseMetricsRequest struct {
	IncludeDetails bool   `json:"include_details" form:"include_details"`
	TimeRange      string `json:"time_range" form:"time_range"` // "1h", "24h", "7d", "30d"
}

// TableSizeRequest represents request parameters for table size information
type TableSizeRequest struct {
	SchemaName string `json:"schema_name" form:"schema_name"`
	TableName  string `json:"table_name" form:"table_name"`
	SortBy     string `json:"sort_by" form:"sort_by"`       // "size", "rows", "name"
	SortOrder  string `json:"sort_order" form:"sort_order"` // "asc", "desc"
	Limit      int    `json:"limit" form:"limit"`
	Offset     int    `json:"offset" form:"offset"`
}

// IndexUsageRequest represents request parameters for index usage statistics
type IndexUsageRequest struct {
	SchemaName string `json:"schema_name" form:"schema_name"`
	TableName  string `json:"table_name" form:"table_name"`
	ShowUnused bool   `json:"show_unused" form:"show_unused"`
	MinScans   int    `json:"min_scans" form:"min_scans"`
	Limit      int    `json:"limit" form:"limit"`
}

// MaintenanceRequest represents request parameters for maintenance operations
type MaintenanceRequest struct {
	TableName string `json:"table_name" binding:"required"`
	Operation string `json:"operation" binding:"required"` // "vacuum", "analyze", "reindex", "cluster"
	DryRun    bool   `json:"dry_run"`
}

// SecurityReportRequest represents request parameters for security reports
type SecurityReportRequest struct {
	ReportType string `json:"report_type" form:"report_type"` // "compliance", "events", "activity"
	TimeRange  string `json:"time_range" form:"time_range"`   // "24h", "7d", "30d"
	Severity   string `json:"severity" form:"severity"`       // "ALL", "HIGH", "MEDIUM", "LOW"
}

// PartitionManagementRequest represents request parameters for partition management
type PartitionManagementRequest struct {
	TableName    string `json:"table_name" binding:"required"`
	Operation    string `json:"operation" binding:"required"` // "create", "drop", "migrate"
	PartitionKey string `json:"partition_key"`
	StartDate    string `json:"start_date"`
	EndDate      string `json:"end_date"`
	Confirm      bool   `json:"confirm"`
}

// DatabaseOptimizationRequest represents request parameters for database optimization
type DatabaseOptimizationRequest struct {
	OptimizationType string   `json:"optimization_type" binding:"required"` // "indexes", "statistics", "vacuum", "all"`
	TargetTables     []string `json:"target_tables"`
	Confirm          bool     `json:"confirm"`
}

// HealthCheckRequest represents request parameters for health checks
type HealthCheckRequest struct {
	CheckType string `json:"check_type" form:"check_type"` // "basic", "detailed", "security"
}

// SlowQueryRequest represents request parameters for slow query analysis
type SlowQueryRequest struct {
	MinExecutionTime float64 `json:"min_execution_time" form:"min_execution_time"`
	Limit            int     `json:"limit" form:"limit"`
	TimeRange        string  `json:"time_range" form:"time_range"`
}

// BackupRequest represents request parameters for backup operations
type BackupRequest struct {
	BackupType  string `json:"backup_type" binding:"required"` // "full", "incremental", "schema_only"
	Compression bool   `json:"compression"`
	Description string `json:"description"`
}

// SecurityEventLogRequest represents request parameters for security event logging
type SecurityEventLogRequest struct {
	EventType        string `json:"event_type" binding:"required"`
	EventDescription string `json:"event_description" binding:"required"`
	Severity         string `json:"severity"` // "INFO", "WARNING", "ERROR", "CRITICAL"`
	UserID           string `json:"user_id"`
	IPAddress        string `json:"ip_address"`
	AdditionalData   string `json:"additional_data"`
}

// DatabaseMetricsResponse represents response with database metrics
type DatabaseMetricsResponse struct {
	Success bool             `json:"success"`
	Message string           `json:"message"`
	Data    *DatabaseMetrics `json:"data,omitempty"`
}

// TableSizeResponse represents response with table size information
type TableSizeResponse struct {
	Success bool        `json:"success"`
	Message string      `json:"message"`
	Data    []TableSize `json:"data,omitempty"`
	Total   int         `json:"total"`
}

// IndexUsageResponse represents response with index usage statistics
type IndexUsageResponse struct {
	Success bool         `json:"success"`
	Message string       `json:"message"`
	Data    []IndexUsage `json:"data,omitempty"`
	Total   int          `json:"total"`
}

// MaintenanceResponse represents response for maintenance operations
type MaintenanceResponse struct {
	Success      bool   `json:"success"`
	Message      string `json:"message"`
	Operation    string `json:"operation"`
	TableName    string `json:"table_name"`
	Duration     string `json:"duration"`
	RowsAffected int64  `json:"rows_affected"`
}

// SecurityReportResponse represents response with security report
type SecurityReportResponse struct {
	Success     bool             `json:"success"`
	Message     string           `json:"message"`
	Data        []SecurityReport `json:"data,omitempty"`
	GeneratedAt time.Time        `json:"generated_at"`
}

// HealthCheckResponse represents response for health checks
type HealthCheckResponse struct {
	Success bool            `json:"success"`
	Message string          `json:"message"`
	Data    *DatabaseHealth `json:"data,omitempty"`
}

// SlowQueryResponse represents response with slow query information
type SlowQueryResponse struct {
	Success bool        `json:"success"`
	Message string      `json:"message"`
	Data    []SlowQuery `json:"data,omitempty"`
	Total   int         `json:"total"`
}

// BackupResponse represents response for backup operations
type BackupResponse struct {
	Success    bool      `json:"success"`
	Message    string    `json:"message"`
	BackupID   string    `json:"backup_id"`
	BackupSize string    `json:"backup_size"`
	StartTime  time.Time `json:"start_time"`
	EndTime    time.Time `json:"end_time"`
	Duration   string    `json:"duration"`
}

// PartitionManagementResponse represents response for partition management
type PartitionManagementResponse struct {
	Success        bool   `json:"success"`
	Message        string `json:"message"`
	Operation      string `json:"operation"`
	TableName      string `json:"table_name"`
	PartitionCount int    `json:"partition_count"`
	DataMigrated   int64  `json:"data_migrated"`
}

// DatabaseOptimizationResponse represents response for database optimization
type DatabaseOptimizationResponse struct {
	Success          bool     `json:"success"`
	Message          string   `json:"message"`
	OptimizationType string   `json:"optimization_type"`
	TablesProcessed  int      `json:"tables_processed"`
	IndexesOptimized int      `json:"indexes_optimized"`
	Improvements     []string `json:"improvements"`
	Duration         string   `json:"duration"`
}
