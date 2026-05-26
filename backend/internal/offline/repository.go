package offline

import (
	"encoding/json"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Repository interface {
	// SyncState operations
	CreateSyncState(state *SyncState) error
	GetSyncStateByID(id uuid.UUID) (*SyncState, error)
	GetSyncStatesByEntity(entityType string, entityID uuid.UUID) ([]SyncState, error)
	GetSyncStatesByDevice(deviceID string) ([]SyncState, error)
	GetSyncStatesByUser(userID uuid.UUID) ([]SyncState, error)
	GetPendingSyncStates(limit int) ([]SyncState, error)
	UpdateSyncState(state *SyncState) error
	DeleteSyncState(id uuid.UUID) error

	// ConflictResolution operations
	CreateConflictResolution(conflict *ConflictResolution) error
	GetConflictResolutionByID(id uuid.UUID) (*ConflictResolution, error)
	GetConflictsByEntity(entityType string, entityID uuid.UUID) ([]ConflictResolution, error)
	GetPendingConflicts(limit int) ([]ConflictResolution, error)
	UpdateConflictResolution(conflict *ConflictResolution) error
	DeleteConflictResolution(id uuid.UUID) error

	// Statistics
	GetSyncStatistics() (map[string]int64, error)
	GetConflictStatistics() (map[string]int64, error)
}

type repository struct {
	db *gorm.DB
}

func NewRepository(db *gorm.DB) Repository {
	return &repository{db: db}
}

// SyncState operations
func (r *repository) CreateSyncState(state *SyncState) error {
	return r.db.Create(state).Error
}

func (r *repository) GetSyncStateByID(id uuid.UUID) (*SyncState, error) {
	var state SyncState
	err := r.db.Where("id = ? AND deleted_at IS NULL", id).First(&state).Error
	if err != nil {
		return nil, err
	}
	return &state, nil
}

func (r *repository) GetSyncStatesByEntity(entityType string, entityID uuid.UUID) ([]SyncState, error) {
	var states []SyncState
	err := r.db.Where("entity_type = ? AND entity_id = ? AND deleted_at IS NULL", entityType, entityID).
		Order("created_at DESC").
		Find(&states).Error
	return states, err
}

func (r *repository) GetSyncStatesByDevice(deviceID string) ([]SyncState, error) {
	var states []SyncState
	err := r.db.Where("device_id = ? AND deleted_at IS NULL", deviceID).
		Order("created_at DESC").
		Find(&states).Error
	return states, err
}

func (r *repository) GetSyncStatesByUser(userID uuid.UUID) ([]SyncState, error) {
	var states []SyncState
	err := r.db.Where("user_id = ? AND deleted_at IS NULL", userID).
		Order("created_at DESC").
		Find(&states).Error
	return states, err
}

func (r *repository) GetPendingSyncStates(limit int) ([]SyncState, error) {
	var states []SyncState
	query := r.db.Where("sync_status = ? AND deleted_at IS NULL", SyncStatusPending).
		Order("created_at ASC")

	if limit > 0 {
		query = query.Limit(limit)
	}

	err := query.Find(&states).Error
	return states, err
}

func (r *repository) UpdateSyncState(state *SyncState) error {
	return r.db.Save(state).Error
}

func (r *repository) DeleteSyncState(id uuid.UUID) error {
	return r.db.Where("id = ?", id).Delete(&SyncState{}).Error
}

// ConflictResolution operations
func (r *repository) CreateConflictResolution(conflict *ConflictResolution) error {
	return r.db.Create(conflict).Error
}

func (r *repository) GetConflictResolutionByID(id uuid.UUID) (*ConflictResolution, error) {
	var conflict ConflictResolution
	err := r.db.Where("id = ?", id).First(&conflict).Error
	if err != nil {
		return nil, err
	}
	return &conflict, nil
}

func (r *repository) GetConflictsByEntity(entityType string, entityID uuid.UUID) ([]ConflictResolution, error) {
	var conflicts []ConflictResolution
	err := r.db.Where("entity_type = ? AND entity_id = ?", entityType, entityID).
		Order("created_at DESC").
		Find(&conflicts).Error
	return conflicts, err
}

func (r *repository) GetPendingConflicts(limit int) ([]ConflictResolution, error) {
	var conflicts []ConflictResolution
	query := r.db.Where("resolution = ?", ResolutionPending).
		Order("created_at ASC")

	if limit > 0 {
		query = query.Limit(limit)
	}

	err := query.Find(&conflicts).Error
	return conflicts, err
}

func (r *repository) UpdateConflictResolution(conflict *ConflictResolution) error {
	return r.db.Save(conflict).Error
}

func (r *repository) DeleteConflictResolution(id uuid.UUID) error {
	return r.db.Where("id = ?", id).Delete(&ConflictResolution{}).Error
}

// Statistics
func (r *repository) GetSyncStatistics() (map[string]int64, error) {
	stats := make(map[string]int64)

	var result struct {
		PendingCount int64
		SyncingCount int64
		SyncedCount  int64
		FailedCount  int64
	}

	err := r.db.Model(&SyncState{}).
		Select("COUNT(CASE WHEN sync_status = ? THEN 1 END) as pending_count,"+
			"COUNT(CASE WHEN sync_status = ? THEN 1 END) as syncing_count,"+
			"COUNT(CASE WHEN sync_status = ? THEN 1 END) as synced_count,"+
			"COUNT(CASE WHEN sync_status = ? THEN 1 END) as failed_count",
			SyncStatusPending, SyncStatusSyncing, SyncStatusSynced, SyncStatusFailed).
		Where("deleted_at IS NULL").
		Scan(&result).Error

	if err != nil {
		return nil, err
	}

	stats["pending"] = result.PendingCount
	stats["syncing"] = result.SyncingCount
	stats["synced"] = result.SyncedCount
	stats["failed"] = result.FailedCount

	return stats, nil
}

func (r *repository) GetConflictStatistics() (map[string]int64, error) {
	stats := make(map[string]int64)

	var result struct {
		PendingCount     int64
		LocalWinsCount   int64
		RemoteWinsCount  int64
		ManualMergeCount int64
	}

	err := r.db.Model(&ConflictResolution{}).
		Select("COUNT(CASE WHEN resolution = ? THEN 1 END) as pending_count,"+
			"COUNT(CASE WHEN resolution = ? THEN 1 END) as local_wins_count,"+
			"COUNT(CASE WHEN resolution = ? THEN 1 END) as remote_wins_count,"+
			"COUNT(CASE WHEN resolution = ? THEN 1 END) as manual_merge_count",
			ResolutionPending, ResolutionLocalWins, ResolutionRemoteWins, ResolutionManualMerge).
		Scan(&result).Error

	if err != nil {
		return nil, err
	}

	stats["pending"] = result.PendingCount
	stats["local_wins"] = result.LocalWinsCount
	stats["remote_wins"] = result.RemoteWinsCount
	stats["manual_merge"] = result.ManualMergeCount

	return stats, nil
}

// Helper function to convert map to JSON string
func mapToJSON(data map[string]interface{}) (string, error) {
	if data == nil {
		return "", nil
	}
	bytes, err := json.Marshal(data)
	if err != nil {
		return "", err
	}
	return string(bytes), nil
}

// Helper function to convert JSON string to map
func jsonToMap(jsonStr string) (map[string]interface{}, error) {
	if jsonStr == "" {
		return nil, nil
	}
	var result map[string]interface{}
	err := json.Unmarshal([]byte(jsonStr), &result)
	if err != nil {
		return nil, err
	}
	return result, nil
}
