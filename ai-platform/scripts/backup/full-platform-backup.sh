#!/bin/bash
# Full Platform Backup Script for AI Platform
# This script backs up all components of the AI Platform

set -e

# Configuration
BACKUP_DIR="/backups/full-platform"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Log function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting full platform backup..."

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Backup PostgreSQL
log "Backing up PostgreSQL..."
if [ -f "/scripts/backup/backup-postgres.sh" ]; then
    /scripts/backup/backup-postgres.sh
else
    log "ERROR: PostgreSQL backup script not found"
    exit 1
fi

# Backup MinIO
log "Backing up MinIO..."
if [ -f "/scripts/backup/backup-minio.sh" ]; then
    /scripts/backup/backup-minio.sh
else
    log "ERROR: MinIO backup script not found"
    exit 1
fi

# Backup Qdrant (vector database)
log "Backing up Qdrant..."
QDRANT_BACKUP_DIR="${BACKUP_DIR}/qdrant_${TIMESTAMP}"
mkdir -p "${QDRANT_BACKUP_DIR}"
if [ -n "${QDRANT_ENDPOINT}" ]; then
    curl -X POST "${QDRANT_ENDPOINT}/collections/_snapshot" \
        -H "Content-Type: application/json" \
        -d '{"location": "/qdrant/storage/snapshots"}'
    cp -r /qdrant/storage/snapshots/* "${QDRANT_BACKUP_DIR}/" 2>/dev/null || log "WARNING: Qdrant snapshots not found"
    log "Qdrant backup completed"
else
    log "WARNING: Qdrant endpoint not configured, skipping Qdrant backup"
fi

# Backup configuration files
log "Backing up configuration files..."
CONFIG_BACKUP_DIR="${BACKUP_DIR}/config_${TIMESTAMP}"
mkdir -p "${CONFIG_BACKUP_DIR}"
cp -r /ai-platform/.env.example "${CONFIG_BACKUP_DIR}/" 2>/dev/null || true
cp -r /ai-platform/docker-compose.yml "${CONFIG_BACKUP_DIR}/" 2>/dev/null || true
cp -r /ai-platform/infra "${CONFIG_BACKUP_DIR}/" 2>/dev/null || true
log "Configuration backup completed"

# Create full backup archive
log "Creating full backup archive..."
ARCHIVE_FILE="${BACKUP_DIR}/full_platform_backup_${TIMESTAMP}.tar.gz"
tar -czf "${ARCHIVE_FILE}" -C "${BACKUP_DIR}" .

# Verify backup
if [ -f "${ARCHIVE_FILE}" ]; then
    ARCHIVE_SIZE=$(du -h "${ARCHIVE_FILE}" | cut -f1)
    log "Full platform backup completed successfully: ${ARCHIVE_FILE} (${ARCHIVE_SIZE})"
else
    log "ERROR: Full backup archive not created"
    exit 1
fi

# Clean up old backups
log "Cleaning up backups older than ${RETENTION_DAYS} days..."
find "${BACKUP_DIR}" -name "full_platform_backup_*.tar.gz" -type f -mtime +${RETENTION_DAYS} -delete

# Clean up temporary directories
rm -rf "${QDRANT_BACKUP_DIR}" "${CONFIG_BACKUP_DIR}"

log "Full platform backup completed"
