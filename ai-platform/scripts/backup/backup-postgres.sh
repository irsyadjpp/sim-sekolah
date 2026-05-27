#!/bin/bash
# PostgreSQL Backup Script for AI Platform
# This script backs up PostgreSQL databases

set -e

# Configuration
BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Database configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-ai_platform}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-}"

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Backup filename
BACKUP_FILE="${BACKUP_DIR}/postgres_backup_${TIMESTAMP}.sql.gz"

# Log function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting PostgreSQL backup..."

# Set PGPASSWORD if provided
if [ -n "${DB_PASSWORD}" ]; then
    export PGPASSWORD="${DB_PASSWORD}"
fi

# Perform backup
log "Backing up database: ${DB_NAME}"
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" | gzip > "${BACKUP_FILE}"

# Verify backup
if [ -f "${BACKUP_FILE}" ]; then
    BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    log "Backup completed successfully: ${BACKUP_FILE} (${BACKUP_SIZE})"
else
    log "ERROR: Backup file not created"
    exit 1
fi

# Clean up old backups
log "Cleaning up backups older than ${RETENTION_DAYS} days..."
find "${BACKUP_DIR}" -name "postgres_backup_*.sql.gz" -type f -mtime +${RETENTION_DAYS} -delete

# Unset PGPASSWORD
if [ -n "${DB_PASSWORD}" ]; then
    unset PGPASSWORD
fi

log "PostgreSQL backup completed"
