#!/bin/bash
# SeaweedFS Backup Script for AI Platform
# This script backs up SeaweedFS object storage using S3-compatible API

set -e

# Configuration
BACKUP_DIR="/backups/seaweedfs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# SeaweedFS S3 configuration
SEAWEEDFS_S3_ENDPOINT="${SEAWEEDFS_S3_ENDPOINT:-http://localhost:8333}"
SEAWEEDFS_ACCESS_KEY="${SEAWEEDFS_ACCESS_KEY:-}"
SEAWEEDFS_SECRET_KEY="${SEAWEEDFS_SECRET_KEY:-}"
BUCKETS_TO_BACKUP="documents embeddings models knowledge-graph"

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Log function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting SeaweedFS backup..."

# Configure AWS CLI for SeaweedFS
if [ -n "${SEAWEEDFS_ACCESS_KEY}" ] && [ -n "${SEAWEEDFS_SECRET_KEY}" ]; then
    export AWS_ACCESS_KEY_ID="${SEAWEEDFS_ACCESS_KEY}"
    export AWS_SECRET_ACCESS_KEY="${SEAWEEDFS_SECRET_KEY}"
    export AWS_ENDPOINT_URL="${SEAWEEDFS_S3_ENDPOINT}"
    # Disable SSL verification for local development
    export AWS_CA_BUNDLE=""
else
    log "ERROR: SeaweedFS credentials not provided"
    exit 1
fi

# Backup each bucket
for bucket in ${BUCKETS_TO_BACKUP}; do
    log "Backing up bucket: ${bucket}"
    
    # Check if bucket exists
    if aws --endpoint-url="${AWS_ENDPOINT_URL}" s3 ls "s3://${bucket}" > /dev/null 2>&1; then
        # Create backup directory for this bucket
        BUCKET_BACKUP_DIR="${BACKUP_DIR}/${bucket}_${TIMESTAMP}"
        mkdir -p "${BUCKET_BACKUP_DIR}"
        
        # Sync bucket to backup directory
        aws --endpoint-url="${AWS_ENDPOINT_URL}" s3 sync "s3://${bucket}" "${BUCKET_BACKUP_DIR}/"
        
        # Create archive
        ARCHIVE_FILE="${BACKUP_DIR}/seaweedfs_${bucket}_backup_${TIMESTAMP}.tar.gz"
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
find "${BACKUP_DIR}" -name "seaweedfs_*_backup_*.tar.gz" -type f -mtime +${RETENTION_DAYS} -delete

log "SeaweedFS backup completed"
