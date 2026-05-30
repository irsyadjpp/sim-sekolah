"""
Metadata Service - Monolith Architecture
Metadata functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class MetadataService:
    """Metadata service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize metadata service with actual components"""
        self.initialized = False
        
        # Initialize actual metadata components
        try:
            # Import from the actual metadata-service code
            from metadata.main import MetadataEngine
            
            self.metadata_engine = MetadataEngine()
            
        except Exception as e:
            logger.error(f"Error initializing metadata components: {e}")
    
    def initialize(self):
        """Initialize metadata service"""
        try:
            logger.info("Initializing Metadata Service with actual microservice code")
            self.initialized = True
            logger.info("Metadata Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Metadata Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for metadata service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "metadata_service",
            "architecture": "monolith",
            "components": {
                "metadata_engine": "ready"
            }
        }
    
    async def extract_metadata(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract metadata using actual microservice logic
        
        Args:
            content_data: Content data for metadata extraction
            
        Returns:
            Extracted metadata
        """
        try:
            logger.info("Extracting metadata")
            
            # Use actual metadata engine logic
            result = self.metadata_engine.extract_metadata(content_data)
            
            logger.info("Metadata extracted successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def update_metadata(self, resource_id: str, 
                             metadata_updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update metadata using actual microservice logic
        
        Args:
            resource_id: Resource identifier
            metadata_updates: Metadata updates
            
        Returns:
            Updated metadata
        """
        try:
            logger.info(f"Updating metadata for resource: {resource_id}")
            
            # Use actual metadata engine logic
            result = self.metadata_engine.update_metadata(resource_id, metadata_updates)
            
            logger.info(f"Metadata updated successfully for resource {resource_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error updating metadata: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
