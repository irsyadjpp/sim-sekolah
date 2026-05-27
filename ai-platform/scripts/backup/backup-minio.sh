#!/bin/bash
# MinIO Backup Script for AI Platform
# This script backs up MinIO object storage

set -e

# Configuration
BACKUP_DIR="/backups/minio"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# MinIO configuration
MINIO_ENDPOINT="${MINIO_ENDPOINT:-localhost:9000}"
MINIO_ACCESS_KEY="${MINIO_ACCESS_KEY:-}"
MINIO_SECRET_KEY="${MINIO_SECRET_KEY:-}"
MINIO_ALIAS="aiplatform"
BUCKETS_TO_BACKUP="documents embeddings models knowledge-graph"

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Log function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting MinIO backup..."

# Configure MinIO client
if [ -n "${MINIO_ACCESS_KEY}" ] && [ -n "${MINIO_SECRET_KEY}" ]; then
    mc alias set ${MINIO_ALIAS} ${MINIO_ENDPOINT} ${MINIO_ACCESS_KEY} ${MINIO_SECRET_KEY}
else
    log "ERROR: MinIO credentials not provided"
    exit 1
fi

# Backup each bucket
for bucket in ${BUCKETS_TO_BACKUP}; do
    log "Backing up bucket: ${bucket}"
    
    # Check if bucket exists
    if mc ls ${MINIO_ALIAS}/${bucket} > /dev/null 2>&1; then
        # Create backup directory for this bucket
        BUCKET_BACKUP_DIR="${BACKUP_DIR}/${bucket}_${TIMESTAMP}"
        mkdir -p "${BUCKET_BACKUP_DIR}"
        
        # Mirror bucket to backup directory
        mc mirror ${MINIO_ALIAS}/${bucket} ${BUCKET_BACKUP_DIR}/
        
        # Create archive
        ARCHIVE_FILE="${BACKUP_DIR}/minio_${bucket}_backup_${TIMESTAMP}.tar.gz"
        tar -czf "${ARCHIVE_FILE}" -C "${BACKUP_DIR}" "$(basename ${BUCKET_BACKUP_DIR})"
        
        # Remove temporary directory
        rm -rf "${BUCKET_BACKUP_DIR}"
        
        # Verify backup
        if [ -f "${ARCHIVE_FILE}" ]; then
            ARCHIVE_SIZE=$(du -h "${ARCHIVE_FILE}" | cut -f1)
            log "Backup completed successfully: ${ARCHIVE_FILE} (${ARCHIVE_SIZE})"
        else
            log "ERROR: Backup file not created for bucket: ${bucket}"
        fi
    else
        log "WARNING: Bucket ${bucket} does not exist, skipping"
    fi
done

# Clean up old backups
log "Cleaning up backups older than ${RETENTION_DAYS} days..."
find "${BACKUP_DIR}" -name "minio_*_backup_*.tar.gz" -type f -mtime +${RETENTION_DAYS} -delete

log "MinIO backup completed"
