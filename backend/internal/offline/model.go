package offline

import (
	"sim-sekolah/internal/common"
	"time"

	"github.com/google/uuid"
)

// SyncState represents the synchronization status of data
type SyncState struct {
	ID              uuid.UUID  `gorm:"type:uuid;primary_key;default:uuid_generate_v4()"`
	EntityType      string     `gorm:"type:varchar(100);not null;index"`
	EntityID        uuid.UUID  `gorm:"type:uuid;not null;index"`
	SyncStatus      string     `gorm:"type:varchar(50);not null;index"` // pending, syncing, synced, failed
	LastSyncAttempt *time.Time `gorm:"type:timestamp"`
	LastSyncSuccess *time.Time `gorm:"type:timestamp"`
	ErrorMessage    string     `gorm:"type:text"`
	RetryCount      int        `gorm:"type:integer;default:0"`
	DataPayload     string     `gorm:"type:jsonb"`              // Store the actual data for offline
	Version         int64      `gorm:"type:bigint;default:1"`   // Optimistic locking
	DeviceID        string     `gorm:"type:varchar(100);index"` // Device that created the offline entry
	UserID          uuid.UUID  `gorm:"type:uuid;index"`         // User who created the offline entry

	common.Auditable
}

// ConflictResolution represents data merge conflicts
type ConflictResolution struct {
	ID              uuid.UUID  `gorm:"type:uuid;primary_key;default:uuid_generate_v4()"`
	EntityType      string     `gorm:"type:varchar(100);not null;index"`
	EntityID        uuid.UUID  `gorm:"type:uuid;not null;index"`
	ConflictType    string     `gorm:"type:varchar(50);not null"`       // version_conflict, data_conflict, deletion_conflict
	LocalData       string     `gorm:"type:jsonb;not null"`             // Data from local device
	RemoteData      string     `gorm:"type:jsonb;not null"`             // Data from server
	Resolution      string     `gorm:"type:varchar(50);not null;index"` // pending, local_wins, remote_wins, manual_merge
	ResolvedData    string     `gorm:"type:jsonb"`                      // Final merged data
	ResolvedAt      *time.Time `gorm:"type:timestamp"`
	ResolvedBy      uuid.UUID  `gorm:"type:uuid;index"` // User who resolved the conflict
	ResolutionNotes string     `gorm:"type:text"`
	DeviceID        string     `gorm:"type:varchar(100);index"` // Device that detected the conflict

	common.Auditable
}

// TableName specifies the table name for SyncState
func (SyncState) TableName() string {
	return "sync_state"
}

// TableName specifies the table name for ConflictResolution
func (ConflictResolution) TableName() string {
	return "conflict_resolution"
}

// Sync status constants
const (
	SyncStatusPending = "pending"
	SyncStatusSyncing = "syncing"
	SyncStatusSynced  = "synced"
	SyncStatusFailed  = "failed"
)

// Conflict type constants
const (
	ConflictTypeVersion  = "version_conflict"
	ConflictTypeData     = "data_conflict"
	ConflictTypeDeletion = "deletion_conflict"
)

// Resolution constants
const (
	ResolutionPending     = "pending"
	ResolutionLocalWins   = "local_wins"
	ResolutionRemoteWins  = "remote_wins"
	ResolutionManualMerge = "manual_merge"
)

// GetSyncStatusDescription returns Indonesian description for sync status
func GetSyncStatusDescription(status string) string {
	descriptions := map[string]string{
		SyncStatusPending: "Menunggu Sinkronisasi",
		SyncStatusSyncing: "Sedang Sinkronisasi",
		SyncStatusSynced:  "Tersinkronisasi",
		SyncStatusFailed:  "Gagal Sinkronisasi",
	}
	if desc, exists := descriptions[status]; exists {
		return desc
	}
	return status
}

// GetConflictTypeDescription returns Indonesian description for conflict type
func GetConflictTypeDescription(conflictType string) string {
	descriptions := map[string]string{
		ConflictTypeVersion:  "Konflik Versi",
		ConflictTypeData:     "Konflik Data",
		ConflictTypeDeletion: "Konflik Penghapusan",
	}
	if desc, exists := descriptions[conflictType]; exists {
		return desc
	}
	return conflictType
}

// GetResolutionDescription returns Indonesian description for resolution
func GetResolutionDescription(resolution string) string {
	descriptions := map[string]string{
		ResolutionPending:     "Menunggu Resolusi",
		ResolutionLocalWins:   "Data Lokal Dipilih",
		ResolutionRemoteWins:  "Data Server Dipilih",
		ResolutionManualMerge: "Gabungan Manual",
	}
	if desc, exists := descriptions[resolution]; exists {
		return desc
	}
	return resolution
}
