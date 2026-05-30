#!/usr/bin/env python3
"""
Knowledge Migration to MinIO AIStor

Script untuk migrate knowledge folder ke MinIO AIStor S3-compatible storage.
"""

import os
import sys
import boto3
from pathlib import Path
from datetime import datetime
import hashlib
import json
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configuration
MINIO_S3_ENDPOINT = "http://minio:9000"
AWS_ACCESS_KEY_ID = "admin"
AWS_SECRET_ACCESS_KEY = "admin123"
BUCKET_NAME = "knowledge-assets"
KNOWLEDGE_ROOT = "/path/to/ai-platform/knowledge"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KnowledgeMigrator:
    """Migrator untuk knowledge folder ke MinIO AIStor."""
    
    def __init__(self, s3_endpoint: str, access_key: str, secret_key: str, bucket: str):
        """
        Initialize migrator.
        
        Args:
            s3_endpoint: MinIO AIStor S3 endpoint
            access_key: AWS access key
            secret_key: AWS secret key  
            bucket: Target bucket name
        """
        self.s3_client = boto3.client(
            's3',
            endpoint_url=s3_endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='us-east-1'
        )
        self.bucket = bucket
        self.migration_log = []
        
    def setup_bucket(self):
        """Create bucket jika belum ada."""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket)
            logger.info(f"Bucket {self.bucket} already exists")
        except:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket)
                logger.info(f"Created bucket: {self.bucket}")
            except Exception as e:
                logger.error(f"Failed to create bucket: {e}")
                raise
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash dari file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def upload_file(self, file_path: Path, s3_key: str) -> Dict:
        """
        Upload single file ke MinIO AIStor dengan metadata.
        
        Args:
            file_path: Local file path
            s3_key: Target S3 key
            
        Returns:
            Upload result metadata
        """
        try:
            # Calculate hash untuk integrity check
            file_hash = self.calculate_file_hash(file_path)
            
            # Parse metadata dari path structure
            relative_path = file_path.relative_to(KNOWLEDGE_ROOT)
            parts = str(relative_path).parts
            
            # Extract educational metadata dari path
            category = parts[0] if len(parts) > 0 else None
            subject = parts[1] if len(parts) > 1 else None
            grade_level = parts[2] if len(parts) > 2 and parts[2].startswith('kelas-') else None
            version = parts[3] if len(parts) > 3 and parts[3].startswith('v') else None
            
            # Check untuk metadata.json file
            metadata = {}
            metadata_file = file_path.parent / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            
            # Add system metadata
            metadata.update({
                'original_path': str(relative_path),
                'file_hash': file_hash,
                'upload_timestamp': datetime.utcnow().isoformat(),
                'category': category,
                'subject': subject,
                'grade_level': grade_level,
                'version': version,
                'file_size': file_path.stat().st_size,
                'file_type': file_path.suffix.lower()
            })
            
            # Upload dengan metadata
            extra_args = {}
            if file_path.suffix.lower() in ['.pdf', '.docx', '.doc']:
                extra_args['ContentType'] = 'application/pdf' if file_path.suffix.lower() == '.pdf' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            elif file_path.suffix.lower() == '.json':
                extra_args['ContentType'] = 'application/json'
            elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                extra_args['ContentType'] = 'image/jpeg' if file_path.suffix.lower() in ['.jpg', '.jpeg'] else 'image/png'
            
            # Add metadata sebagai custom headers
            for key, value in metadata.items():
                extra_args[f'Metadata-{key}'] = str(value)
            
            self.s3_client.upload_file(
                str(file_path),
                self.bucket,
                s3_key,
                ExtraArgs=extra_args
            )
            
            result = {
                'status': 'success',
                'local_path': str(file_path),
                's3_key': s3_key,
                'file_hash': file_hash,
                'metadata': metadata
            }
            
            logger.info(f"✅ Uploaded to MinIO: {s3_key}")
            return result
            
        except Exception as e:
            result = {
                'status': 'error',
                'local_path': str(file_path),
                's3_key': s3_key,
                'error': str(e)
            }
            logger.error(f"❌ Failed to upload to MinIO {s3_key}: {e}")
            return result
    
    def migrate_directory(self, directory: Path, base_prefix: str = ""):
        """
        Migrate seluruh directory tree.
        
        Args:
            directory: Directory path to migrate
            base_prefix: S3 key prefix
        """
        if not directory.exists():
            logger.warning(f"Directory does not exist: {directory}")
            return
        
        files_to_upload = []
        
        # Collect semua files
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.name not in ['.gitkeep', '.DS_Store']:
                # Calculate S3 key
                relative_path = file_path.relative_to(directory)
                s3_key = f"{base_prefix}{relative_path}".replace("\\", "/")
                files_to_upload.append((file_path, s3_key))
        
        logger.info(f"Found {len(files_to_upload)} files to upload")
        
        # Upload dengan parallel processing
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self.upload_file, file_path, s3_key): (file_path, s3_key)
                for file_path, s3_key in files_to_upload
            }
            
            for future in as_completed(futures):
                file_path, s3_key = futures[future]
                try:
                    result = future.result()
                    self.migration_log.append(result)
                except Exception as e:
                    logger.error(f"Exception processing {file_path}: {e}")
                    self.migration_log.append({
                        'status': 'error',
                        'local_path': str(file_path),
                        's3_key': s3_key,
                        'error': str(e)
                    })
    
    def generate_migration_report(self):
        """Generate migration summary report."""
        total = len(self.migration_log)
        successful = len([r for r in self.migration_log if r['status'] == 'success'])
        failed = total - successful
        
        report = {
            'migration_timestamp': datetime.utcnow().isoformat(),
            'bucket': self.bucket,
            'total_files': total,
            'successful_uploads': successful,
            'failed_uploads': failed,
            'success_rate': f"{(successful/total*100):.2f}%" if total > 0 else "0%",
            'failed_files': [r for r in self.migration_log if r['status'] == 'error']
        }
        
        # Save report
        report_file = f"migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\n📊 Migration Summary:")
        logger.info(f"Total files: {total}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Success rate: {report['success_rate']}")
        logger.info(f"Report saved: {report_file}")
        
        return report


def main():
    """Main execution function."""
    migrator = KnowledgeMigrator(
        s3_endpoint=SEAWEDFS_S3_ENDPOINT,
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY,
        bucket=BUCKET_NAME
    )
    
    # Setup bucket
    migrator.setup_bucket()
    
    # Migrate knowledge directory
    knowledge_dir = Path(KNOWLEDGE_ROOT)
    if knowledge_dir.exists():
        logger.info(f"Starting migration of: {knowledge_dir}")
        migrator.migrate_directory(knowledge_dir, base_prefix="")
        
        # Generate report
        migrator.generate_migration_report()
    else:
        logger.error(f"Knowledge directory not found: {KNOWLEDGE_ROOT}")
        sys.exit(1)


if __name__ == "__main__":
    main()
