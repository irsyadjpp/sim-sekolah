package offline

import (
	"fmt"
	"time"

	"github.com/google/uuid"
)

type Service interface {
	// SyncState operations
	CreateSyncState(request SyncStateRequest) (*SyncStateResponse, error)
	GetSyncStateByID(id uuid.UUID) (*SyncStateResponse, error)
	GetSyncStatesByEntity(entityType string, entityID string) ([]SyncStateResponse, error)
	GetSyncStatesByDevice(deviceID string) ([]SyncStateResponse, error)
	GetSyncStatesByUser(userID string) ([]SyncStateResponse, error)
	GetPendingSyncStates(limit int) ([]SyncStateResponse, error)
	UpdateSyncState(id uuid.UUID, request SyncStateRequest) (*SyncStateResponse, error)
	DeleteSyncState(id uuid.UUID) error

	// ConflictResolution operations
	CreateConflictResolution(request ConflictResolutionRequest) (*ConflictResolutionResponse, error)
	GetConflictResolutionByID(id uuid.UUID) (*ConflictResolutionResponse, error)
	GetConflictsByEntity(entityType string, entityID string) ([]ConflictResolutionResponse, error)
	GetPendingConflicts(limit int) ([]ConflictResolutionResponse, error)
	UpdateConflictResolution(id uuid.UUID, request ConflictResolutionRequest) (*ConflictResolutionResponse, error)
	DeleteConflictResolution(id uuid.UUID) error

	// Sync operations
	SyncPending(request SyncRequest) (*SyncResponse, error)
	GetSyncStatistics() (*SyncStatisticsResponse, error)
	GetConflictStatistics() (map[string]int64, error)
}

type service struct {
	repo Repository
}

func NewService(repo Repository) Service {
	return &service{repo: repo}
}

// SyncState operations
func (s *service) CreateSyncState(request SyncStateRequest) (*SyncStateResponse, error) {
	entityID, err := uuid.Parse(request.EntityID)
	if err != nil {
		return nil, fmt.Errorf("invalid entity ID: %w", err)
	}

	userID, err := uuid.Parse(request.UserID)
	if err != nil {
		return nil, fmt.Errorf("invalid user ID: %w", err)
	}

	dataPayload, err := mapToJSON(request.DataPayload)
	if err != nil {
		return nil, fmt.Errorf("failed to serialize data payload: %w", err)
	}

	state := &SyncState{
		ID:          uuid.New(),
		EntityType:  request.EntityType,
		EntityID:    entityID,
		SyncStatus:  SyncStatusPending,
		DataPayload: dataPayload,
		Version:     1,
		DeviceID:    request.DeviceID,
		UserID:      userID,
	}

	if request.SyncStatus != "" {
		state.SyncStatus = request.SyncStatus
	}

	err = s.repo.CreateSyncState(state)
	if err != nil {
		return nil, err
	}

	return s.modelToSyncStateResponse(state), nil
}

func (s *service) GetSyncStateByID(id uuid.UUID) (*SyncStateResponse, error) {
	state, err := s.repo.GetSyncStateByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToSyncStateResponse(state), nil
}

func (s *service) GetSyncStatesByEntity(entityType string, entityID string) ([]SyncStateResponse, error) {
	id, err := uuid.Parse(entityID)
	if err != nil {
		return nil, fmt.Errorf("invalid entity ID: %w", err)
	}

	states, err := s.repo.GetSyncStatesByEntity(entityType, id)
	if err != nil {
		return nil, err
	}

	responses := make([]SyncStateResponse, len(states))
	for i, state := range states {
		responses[i] = *s.modelToSyncStateResponse(&state)
	}
	return responses, nil
}

func (s *service) GetSyncStatesByDevice(deviceID string) ([]SyncStateResponse, error) {
	states, err := s.repo.GetSyncStatesByDevice(deviceID)
	if err != nil {
		return nil, err
	}

	responses := make([]SyncStateResponse, len(states))
	for i, state := range states {
		responses[i] = *s.modelToSyncStateResponse(&state)
	}
	return responses, nil
}

func (s *service) GetSyncStatesByUser(userID string) ([]SyncStateResponse, error) {
	id, err := uuid.Parse(userID)
	if err != nil {
		return nil, fmt.Errorf("invalid user ID: %w", err)
	}

	states, err := s.repo.GetSyncStatesByUser(id)
	if err != nil {
		return nil, err
	}

	responses := make([]SyncStateResponse, len(states))
	for i, state := range states {
		responses[i] = *s.modelToSyncStateResponse(&state)
	}
	return responses, nil
}

func (s *service) GetPendingSyncStates(limit int) ([]SyncStateResponse, error) {
	states, err := s.repo.GetPendingSyncStates(limit)
	if err != nil {
		return nil, err
	}

	responses := make([]SyncStateResponse, len(states))
	for i, state := range states {
		responses[i] = *s.modelToSyncStateResponse(&state)
	}
	return responses, nil
}

func (s *service) UpdateSyncState(id uuid.UUID, request SyncStateRequest) (*SyncStateResponse, error) {
	state, err := s.repo.GetSyncStateByID(id)
	if err != nil {
		return nil, err
	}

	if request.EntityType != "" {
		state.EntityType = request.EntityType
	}

	if request.EntityID != "" {
		entityID, err := uuid.Parse(request.EntityID)
		if err != nil {
			return nil, fmt.Errorf("invalid entity ID: %w", err)
		}
		state.EntityID = entityID
	}

	if request.SyncStatus != "" {
		state.SyncStatus = request.SyncStatus
	}

	if request.DataPayload != nil {
		dataPayload, err := mapToJSON(request.DataPayload)
		if err != nil {
			return nil, fmt.Errorf("failed to serialize data payload: %w", err)
		}
		state.DataPayload = dataPayload
	}

	if request.DeviceID != "" {
		state.DeviceID = request.DeviceID
	}

	if request.UserID != "" {
		userID, err := uuid.Parse(request.UserID)
		if err != nil {
			return nil, fmt.Errorf("invalid user ID: %w", err)
		}
		state.UserID = userID
	}

	state.Version = state.Version + 1

	err = s.repo.UpdateSyncState(state)
	if err != nil {
		return nil, err
	}

	return s.modelToSyncStateResponse(state), nil
}

func (s *service) DeleteSyncState(id uuid.UUID) error {
	return s.repo.DeleteSyncState(id)
}

// ConflictResolution operations
func (s *service) CreateConflictResolution(request ConflictResolutionRequest) (*ConflictResolutionResponse, error) {
	entityID, err := uuid.Parse(request.EntityID)
	if err != nil {
		return nil, fmt.Errorf("invalid entity ID: %w", err)
	}

	localData, err := mapToJSON(request.LocalData)
	if err != nil {
		return nil, fmt.Errorf("failed to serialize local data: %w", err)
	}

	remoteData, err := mapToJSON(request.RemoteData)
	if err != nil {
		return nil, fmt.Errorf("failed to serialize remote data: %w", err)
	}

	conflict := &ConflictResolution{
		ID:           uuid.New(),
		EntityType:   request.EntityType,
		EntityID:     entityID,
		ConflictType: request.ConflictType,
		LocalData:    localData,
		RemoteData:   remoteData,
		Resolution:   ResolutionPending,
		DeviceID:     request.DeviceID,
	}

	if request.Resolution != "" {
		conflict.Resolution = request.Resolution
	}

	if request.ResolvedData != nil {
		resolvedData, err := mapToJSON(request.ResolvedData)
		if err != nil {
			return nil, fmt.Errorf("failed to serialize resolved data: %w", err)
		}
		conflict.ResolvedData = resolvedData
	}

	if request.ResolvedBy != "" {
		resolvedBy, err := uuid.Parse(request.ResolvedBy)
		if err != nil {
			return nil, fmt.Errorf("invalid resolved by user ID: %w", err)
		}
		conflict.ResolvedBy = resolvedBy
	}

	err = s.repo.CreateConflictResolution(conflict)
	if err != nil {
		return nil, err
	}

	return s.modelToConflictResolutionResponse(conflict), nil
}

func (s *service) GetConflictResolutionByID(id uuid.UUID) (*ConflictResolutionResponse, error) {
	conflict, err := s.repo.GetConflictResolutionByID(id)
	if err != nil {
		return nil, err
	}
	return s.modelToConflictResolutionResponse(conflict), nil
}

func (s *service) GetConflictsByEntity(entityType string, entityID string) ([]ConflictResolutionResponse, error) {
	id, err := uuid.Parse(entityID)
	if err != nil {
		return nil, fmt.Errorf("invalid entity ID: %w", err)
	}

	conflicts, err := s.repo.GetConflictsByEntity(entityType, id)
	if err != nil {
		return nil, err
	}

	responses := make([]ConflictResolutionResponse, len(conflicts))
	for i, conflict := range conflicts {
		responses[i] = *s.modelToConflictResolutionResponse(&conflict)
	}
	return responses, nil
}

func (s *service) GetPendingConflicts(limit int) ([]ConflictResolutionResponse, error) {
	conflicts, err := s.repo.GetPendingConflicts(limit)
	if err != nil {
		return nil, err
	}

	responses := make([]ConflictResolutionResponse, len(conflicts))
	for i, conflict := range conflicts {
		responses[i] = *s.modelToConflictResolutionResponse(&conflict)
	}
	return responses, nil
}

func (s *service) UpdateConflictResolution(id uuid.UUID, request ConflictResolutionRequest) (*ConflictResolutionResponse, error) {
	conflict, err := s.repo.GetConflictResolutionByID(id)
	if err != nil {
		return nil, err
	}

	if request.Resolution != "" {
		conflict.Resolution = request.Resolution
		now := time.Now()
		conflict.ResolvedAt = &now
	}

	if request.ResolvedData != nil {
		resolvedData, err := mapToJSON(request.ResolvedData)
		if err != nil {
			return nil, fmt.Errorf("failed to serialize resolved data: %w", err)
		}
		conflict.ResolvedData = resolvedData
	}

	if request.ResolvedBy != "" {
		resolvedBy, err := uuid.Parse(request.ResolvedBy)
		if err != nil {
			return nil, fmt.Errorf("invalid resolved by user ID: %w", err)
		}
		conflict.ResolvedBy = resolvedBy
	}

	conflict.ResolutionNotes = request.ResolutionNotes

	err = s.repo.UpdateConflictResolution(conflict)
	if err != nil {
		return nil, err
	}

	return s.modelToConflictResolutionResponse(conflict), nil
}

func (s *service) DeleteConflictResolution(id uuid.UUID) error {
	return s.repo.DeleteConflictResolution(id)
}

// Sync operations
func (s *service) SyncPending(request SyncRequest) (*SyncResponse, error) {
	syncedCount := 0
	failedCount := 0
	conflictCount := 0

	// Get pending sync states
	states, err := s.repo.GetPendingSyncStates(100) // Process up to 100 at a time
	if err != nil {
		return nil, err
	}

	for _, state := range states {
		// Update state to syncing
		state.SyncStatus = SyncStatusSyncing
		now := time.Now()
		state.LastSyncAttempt = &now
		err := s.repo.UpdateSyncState(&state)
		if err != nil {
			failedCount++
			continue
		}

		// Here you would implement the actual sync logic
		// For now, we'll just mark it as synced
		state.SyncStatus = SyncStatusSynced
		state.LastSyncSuccess = &now
		state.ErrorMessage = ""

		err = s.repo.UpdateSyncState(&state)
		if err != nil {
			failedCount++
			state.SyncStatus = SyncStatusFailed
			state.ErrorMessage = err.Error()
			state.RetryCount = state.RetryCount + 1
			_ = s.repo.UpdateSyncState(&state)
		} else {
			syncedCount++
		}
	}

	response := &SyncResponse{
		SyncedCount:   syncedCount,
		FailedCount:   failedCount,
		ConflictCount: conflictCount,
	}

	return response, nil
}

func (s *service) GetSyncStatistics() (*SyncStatisticsResponse, error) {
	stats, err := s.repo.GetSyncStatistics()
	if err != nil {
		return nil, err
	}

	conflictStats, err := s.repo.GetConflictStatistics()
	if err != nil {
		return nil, err
	}

	response := &SyncStatisticsResponse{
		PendingCount:  int(stats["pending"]),
		SyncingCount:  int(stats["syncing"]),
		SyncedCount:   int(stats["synced"]),
		FailedCount:   int(stats["failed"]),
		ConflictCount: int(conflictStats["pending"]),
	}

	return response, nil
}

func (s *service) GetConflictStatistics() (map[string]int64, error) {
	return s.repo.GetConflictStatistics()
}

// Helper functions
func (s *service) modelToSyncStateResponse(state *SyncState) *SyncStateResponse {
	dataPayload, _ := jsonToMap(state.DataPayload)

	response := &SyncStateResponse{
		ID:              state.ID,
		EntityType:      state.EntityType,
		EntityID:        state.EntityID,
		SyncStatus:      state.SyncStatus,
		SyncStatusName:  GetSyncStatusDescription(state.SyncStatus),
		LastSyncAttempt: state.LastSyncAttempt,
		LastSyncSuccess: state.LastSyncSuccess,
		ErrorMessage:    state.ErrorMessage,
		RetryCount:      state.RetryCount,
		DataPayload:     dataPayload,
		Version:         state.Version,
		DeviceID:        state.DeviceID,
		UserID:          state.UserID,
		CreatedAt:       state.CreatedAt,
		UpdatedAt:       state.UpdatedAt,
	}

	return response
}

func (s *service) modelToConflictResolutionResponse(conflict *ConflictResolution) *ConflictResolutionResponse {
	localData, _ := jsonToMap(conflict.LocalData)
	remoteData, _ := jsonToMap(conflict.RemoteData)
	resolvedData, _ := jsonToMap(conflict.ResolvedData)

	response := &ConflictResolutionResponse{
		ID:               conflict.ID,
		EntityType:       conflict.EntityType,
		EntityID:         conflict.EntityID,
		ConflictType:     conflict.ConflictType,
		ConflictTypeName: GetConflictTypeDescription(conflict.ConflictType),
		LocalData:        localData,
		RemoteData:       remoteData,
		Resolution:       conflict.Resolution,
		ResolutionName:   GetResolutionDescription(conflict.Resolution),
		ResolvedData:     resolvedData,
		ResolvedAt:       conflict.ResolvedAt,
		ResolvedBy:       conflict.ResolvedBy,
		ResolutionNotes:  conflict.ResolutionNotes,
		DeviceID:         conflict.DeviceID,
		CreatedAt:        conflict.CreatedAt,
		UpdatedAt:        conflict.UpdatedAt,
	}

	return response
}
