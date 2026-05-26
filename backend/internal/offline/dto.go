package offline

import (
	"time"

	"github.com/google/uuid"
)

// SyncStateRequest represents request data for sync state operations
type SyncStateRequest struct {
	EntityType  string                 `json:"entity_type" binding:"required"`
	EntityID    string                 `json:"entity_id" binding:"required,uuid"`
	SyncStatus  string                 `json:"sync_status"`
	DataPayload map[string]interface{} `json:"data_payload"`
	DeviceID    string                 `json:"device_id"`
	UserID      string                 `json:"user_id" binding:"required,uuid"`
}

// SyncStateResponse represents response data for sync state operations
type SyncStateResponse struct {
	ID              uuid.UUID              `json:"id"`
	EntityType      string                 `json:"entity_type"`
	EntityID        uuid.UUID              `json:"entity_id"`
	SyncStatus      string                 `json:"sync_status"`
	SyncStatusName  string                 `json:"sync_status_name"`
	LastSyncAttempt *time.Time             `json:"last_sync_attempt"`
	LastSyncSuccess *time.Time             `json:"last_sync_success"`
	ErrorMessage    string                 `json:"error_message"`
	RetryCount      int                    `json:"retry_count"`
	DataPayload     map[string]interface{} `json:"data_payload"`
	Version         int64                  `json:"version"`
	DeviceID        string                 `json:"device_id"`
	UserID          uuid.UUID              `json:"user_id"`
	CreatedAt       time.Time              `json:"created_at"`
	UpdatedAt       time.Time              `json:"updated_at"`
}

// ConflictResolutionRequest represents request data for conflict resolution operations
type ConflictResolutionRequest struct {
	EntityType      string                 `json:"entity_type" binding:"required"`
	EntityID        string                 `json:"entity_id" binding:"required,uuid"`
	ConflictType    string                 `json:"conflict_type" binding:"required"`
	LocalData       map[string]interface{} `json:"local_data" binding:"required"`
	RemoteData      map[string]interface{} `json:"remote_data" binding:"required"`
	Resolution      string                 `json:"resolution"`
	ResolvedData    map[string]interface{} `json:"resolved_data"`
	ResolvedBy      string                 `json:"resolved_by"`
	ResolutionNotes string                 `json:"resolution_notes"`
	DeviceID        string                 `json:"device_id"`
}

// ConflictResolutionResponse represents response data for conflict resolution operations
type ConflictResolutionResponse struct {
	ID               uuid.UUID              `json:"id"`
	EntityType       string                 `json:"entity_type"`
	EntityID         uuid.UUID              `json:"entity_id"`
	ConflictType     string                 `json:"conflict_type"`
	ConflictTypeName string                 `json:"conflict_type_name"`
	LocalData        map[string]interface{} `json:"local_data"`
	RemoteData       map[string]interface{} `json:"remote_data"`
	Resolution       string                 `json:"resolution"`
	ResolutionName   string                 `json:"resolution_name"`
	ResolvedData     map[string]interface{} `json:"resolved_data"`
	ResolvedAt       *time.Time             `json:"resolved_at"`
	ResolvedBy       uuid.UUID              `json:"resolved_by"`
	ResolutionNotes  string                 `json:"resolution_notes"`
	DeviceID         string                 `json:"device_id"`
	CreatedAt        time.Time              `json:"created_at"`
	UpdatedAt        time.Time              `json:"updated_at"`
}

// SyncRequest represents request for manual sync operation
type SyncRequest struct {
	EntityTypes []string `json:"entity_types"` // Specific entity types to sync, empty means sync all
	DeviceID    string   `json:"device_id" binding:"required"`
	UserID      string   `json:"user_id" binding:"required,uuid"`
}

// SyncResponse represents response for sync operation
type SyncResponse struct {
	SyncedCount   int `json:"synced_count"`
	FailedCount   int `json:"failed_count"`
	ConflictCount int `json:"conflict_count"`
}

// PendingSyncResponse represents response for pending sync items
type PendingSyncResponse struct {
	TotalCount int                 `json:"total_count"`
	Items      []SyncStateResponse `json:"items"`
}

// ConflictListResponse represents response for conflict list
type ConflictListResponse struct {
	TotalCount int                          `json:"total_count"`
	Items      []ConflictResolutionResponse `json:"items"`
}

// SyncStatisticsResponse represents sync statistics
type SyncStatisticsResponse struct {
	PendingCount  int `json:"pending_count"`
	SyncingCount  int `json:"syncing_count"`
	SyncedCount   int `json:"synced_count"`
	FailedCount   int `json:"failed_count"`
	ConflictCount int `json:"conflict_count"`
}
