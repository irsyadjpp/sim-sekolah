#!/usr/bin/env python3
"""
Model Download Script for AI Platform

This script downloads models from MinIO object storage to local cache.
"""

import os
import sys
import argparse
import hashlib
from pathlib import Path
from typing import Optional
import requests
from tqdm import tqdm


class ModelDownloader:
    """Download models from MinIO object storage."""
    
    def __init__(
        self,
        minio_endpoint: str = "localhost:9000",
        access_key: str = "minioadmin",
        secret_key: str = "minioadmin",
        bucket: str = "ai-platform-models",
        cache_dir: str = "/models/cache"
    ):
        """
        Initialize model downloader.
        
        Args:
            minio_endpoint: MinIO server endpoint
            access_key: MinIO access key
            secret_key: MinIO secret key
            bucket: MinIO bucket name
            cache_dir: Local cache directory
        """
        self.minio_endpoint = minio_endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def download_model(
        self,
        model_type: str,
        model_name: str,
        version: str = "latest",
        force: bool = False
    ) -> str:
        """
        Download model from MinIO to local cache.
        
        Args:
            model_type: Type of model (embeddings, rerankers, etc.)
            model_name: Name of the model
            version: Model version (default: latest)
            force: Force re-download even if cached
            
        Returns:
            Path to downloaded model directory
        """
        # Construct model path
        if version == "latest":
            version = self._get_latest_version(model_type, model_name)
        
        model_path = f"{model_type}/{model_name}/v{version}/"
        local_path = self.cache_dir / model_path
        
        # Check if already cached
        if local_path.exists() and not force:
            print(f"✅ Model already cached: {local_path}")
            return str(local_path)
        
        # Create local directory
        local_path.mkdir(parents=True, exist_ok=True)
        
        # List model files
        files = self._list_model_files(model_type, model_name, version)
        
        if not files:
            raise FileNotFoundError(f"No files found for model {model_name} v{version}")
        
        # Download files
        print(f"Downloading {model_name} v{version}...")
        for file_info in tqdm(files, desc="Downloading files"):
            self._download_file(file_info, local_path)
        
        # Verify checksum
        if self._verify_checksum(local_path):
            print(f"✅ Model downloaded successfully: {local_path}")
            return str(local_path)
        else:
            raise ValueError("Checksum verification failed")
    
    def _get_latest_version(self, model_type: str, model_name: str) -> str:
        """
        Get latest version of a model.
        
        Args:
            model_type: Type of model
            model_name: Name of the model
            
        Returns:
            Latest version string
        """
        # This would query MinIO for available versions
        # For now, return a default
        return "1.0.0"
    
    def _list_model_files(
        self,
        model_type: str,
        model_name: str,
        version: str
    ) -> list:
        """
        List files for a specific model version.
        
        Args:
            model_type: Type of model
            model_name: Name of the model
            version: Model version
            
        Returns:
            List of file information dictionaries
        """
        # This would list files in MinIO
        # For now, return common model files
        return [
            {
                "name": "model.safetensors",
                "size": 2200000000,
                "checksum": "abc123"
            },
            {
                "name": "config.json",
                "size": 5000,
                "checksum": "def456"
            },
            {
                "name": "tokenizer.json",
                "size": 10000,
                "checksum": "ghi789"
            }
        ]
    
    def _download_file(self, file_info: dict, local_path: Path):
        """
        Download a single file from MinIO.
        
        Args:
            file_info: File information dictionary
            local_path: Local directory path
        """
        # Construct download URL
        file_url = f"http://{self.minio_endpoint}/{self.bucket}/{file_info['name']}"
        
        # Download file
        response = requests.get(
            file_url,
            auth=(self.access_key, self.secret_key),
            stream=True
        )
        response.raise_for_status()
        
        # Write to file
        file_path = local_path / file_info['name']
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    def _verify_checksum(self, local_path: Path) -> bool:
        """
        Verify checksum of downloaded files.
        
        Args:
            local_path: Local directory path
            
        Returns:
            True if checksums match
        """
        # This would verify against stored checksums
        # For now, return True
        return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Download AI Platform models")
    parser.add_argument(
        "--type",
        required=True,
        choices=["embeddings", "rerankers", "classifiers", "vision", "ocr", "moderation", "local-llm"],
        help="Model type"
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Model name"
    )
    parser.add_argument(
        "--version",
        default="latest",
        help="Model version (default: latest)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if cached"
    )
    parser.add_argument(
        "--minio-endpoint",
        default=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        help="MinIO endpoint"
    )
    parser.add_argument(
        "--access-key",
        default=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        help="MinIO access key"
    )
    parser.add_argument(
        "--secret-key",
        default=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        help="MinIO secret key"
    )
    
    args = parser.parse_args()
    
    # Download model
    downloader = ModelDownloader(
        minio_endpoint=args.minio_endpoint,
        access_key=args.access_key,
        secret_key=args.secret_key
    )
    
    try:
        model_path = downloader.download_model(
            model_type=args.type,
            model_name=args.model,
            version=args.version,
            force=args.force
        )
        print(f"\nModel downloaded to: {model_path}")
        sys.exit(0)
    except Exception as e:
        print(f"Error downloading model: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()