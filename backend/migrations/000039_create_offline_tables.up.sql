-- Migration: Create Offline-First Readiness Tables
-- Created: 2026-05-25
-- Description: This migration creates tables for offline-first functionality including sync state management and conflict resolution

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Sync State Table
-- This table tracks the synchronization status of data for offline operations
CREATE TABLE IF NOT EXISTS sync_state (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID NOT NULL,
    sync_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    last_sync_attempt TIMESTAMPTZ,
    last_sync_success TIMESTAMPTZ,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    data_payload JSONB,
    version BIGINT DEFAULT 1,
    device_id VARCHAR(100),
    user_id UUID,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for sync_state
CREATE INDEX IF NOT EXISTS idx_sync_state_entity_type ON sync_state(entity_type);
CREATE INDEX IF NOT EXISTS idx_sync_state_entity_id ON sync_state(entity_id);
CREATE INDEX IF NOT EXISTS idx_sync_state_sync_status ON sync_state(sync_status);
CREATE INDEX IF NOT EXISTS idx_sync_state_device_id ON sync_state(device_id);
CREATE INDEX IF NOT EXISTS idx_sync_state_user_id ON sync_state(user_id);
CREATE INDEX IF NOT EXISTS idx_sync_state_deleted_at ON sync_state(deleted_at);

-- Conflict Resolution Table
-- This table manages data merge conflicts from offline operations
CREATE TABLE IF NOT EXISTS conflict_resolution (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID NOT NULL,
    conflict_type VARCHAR(50) NOT NULL,
    local_data JSONB NOT NULL,
    remote_data JSONB NOT NULL,
    resolution VARCHAR(50) NOT NULL DEFAULT 'pending',
    resolved_data JSONB,
    resolved_at TIMESTAMPTZ,
    resolved_by UUID,
    resolution_notes TEXT,
    device_id VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    created_by UUID,
    updated_by UUID,
    deleted_by UUID
);

-- Create indexes for conflict_resolution
CREATE INDEX IF NOT EXISTS idx_conflict_resolution_entity_type ON conflict_resolution(entity_type);
CREATE INDEX IF NOT EXISTS idx_conflict_resolution_entity_id ON conflict_resolution(entity_id);
CREATE INDEX IF NOT EXISTS idx_conflict_resolution_resolution ON conflict_resolution(resolution);
CREATE INDEX IF NOT EXISTS idx_conflict_resolution_device_id ON conflict_resolution(device_id);
CREATE INDEX IF NOT EXISTS idx_conflict_resolution_resolved_by ON conflict_resolution(resolved_by);
CREATE INDEX IF NOT EXISTS idx_conflict_resolution_deleted ON conflict_resolution(deleted_at);

-- Add comments for documentation
COMMENT ON TABLE sync_state IS 'Tracks synchronization status for offline data operations';
COMMENT ON COLUMN sync_state.sync_status IS 'Status values: pending, syncing, synced, failed';
COMMENT ON COLUMN sync_state.data_payload IS 'JSONB field storing the actual data for offline operations';
COMMENT ON COLUMN sync_state.version IS 'Optimistic locking version for conflict prevention';
COMMENT ON TABLE conflict_resolution IS 'Manages data merge conflicts from offline-first operations';
COMMENT ON COLUMN conflict_resolution.conflict_type IS 'Conflict types: version_conflict, data_conflict, deletion_conflict';
COMMENT ON COLUMN conflict_resolution.resolution IS 'Resolution values: pending, local_wins, remote_wins, manual_merge';
