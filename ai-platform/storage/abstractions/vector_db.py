"""
Vector database abstraction (Qdrant)
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import numpy as np

from .base import StorageBackend, StorageConfig


class VectorDB(StorageBackend):
    """
    Abstract vector database backend.
    
    Provides unified interface for vector similarity search and storage.
    """
    
    @abstractmethod
    async def create_collection(
        self,
        collection_name: str,
        vector_size: int,
        distance_metric: str = "Cosine",
        **kwargs
    ) -> bool:
        """
        Create a new collection in vector database.
        
        Args:
            collection_name: Name of the collection
            vector_size: Dimension of vectors
            distance_metric: Distance metric (Cosine, Euclidean, Dot)
            **kwargs: Additional collection parameters
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection from vector database.
        
        Args:
            collection_name: Name of the collection
            
        List[str] Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def collection_exists(self, collection_name: str) -> bool:
        """
        Check if collection exists.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            True if collection exists
        """
        pass
    
    @abstractmethod
    async def list_collections(self) -> List[str]:
        """
        List all collections in the database.
        
        Returns:
            List of collection names
        """
        pass
    
    @abstractmethod
    async def insert_vectors(
        self,
        collection_name: str,
        vectors: List[List[float]],
        payloads: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Insert vectors into collection.
        
        Args:
            collection_name: Name of the collection
            vectors: List of vectors to insert
            payloads: Optional metadata for each vector
            ids: Optional custom IDs for vectors
            
        Returns:
            List of inserted vector IDs
        """
        pass
    
    @abstractmethod
    async def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: Optional[float] = None,
        filter_condition: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.
        
        Args:
            collection_name: Name of the collection
            query_vector: Query vector
            limit: Maximum number of results
            score_threshold: Minimum similarity score
            filter_condition: Optional filter for results
            **kwargs: Additional search parameters
            
        Returns:
            List of search results with scores and payloads
        """
        pass
    
    @abstractmethod
    async def delete_vectors(
        self,
        collection_name: str,
        ids: List[str],
    ) -> bool:
        """
        Delete vectors by IDs.
        
        Args:
            collection_name: Name of the collection
            ids: List of vector IDs to delete
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
 async def get_vector(
        self,
        collection_name: str,
        vector_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific vector by ID.
        
        Args:
            collection_name: Name of the collection
            vector_id: ID of the vector
            
        Returns:
            Vector data or None if not found
        """
        pass
    
    @abstractmethod
    async def update_vectors(
        self,
        collection_name: str,
        ids: List[str],
        vectors: Optional[List[List[float]]] = None,
        payloads: Optional[List[Dict[str, Any]]] = None,
    ) -> bool:
        """
        Update vectors by IDs.
        
        Args:
            collection_name: Name of the collection
            ids: List of vector IDs to update
            vectors: Optional new vectors
            payloads: Optional new payloads
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
 async def get_collection_info(
        self,
        collection_name: str,
    ) -> Dict[str, Any]:
        """
        Get collection information.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection information
        """
        pass


class QdrantDB(VectorDB):
    """
    Qdrant vector database implementation.
    
    Provides high-performance vector similarity search using Qdrant.
    """
    
    def __init__(self, config: StorageConfig):
        """
        Initialize Qdrant backend.
        
        Args:
            config: Storage configuration
        """
        super().__init__(config)
        self._client = None
    
    async def connect(self) -> None:
        """Establish Qdrant connection."""
        from qdrant_client import QdrantClient
        
        self._client = QdrantClient(
            url=f"http://{self.config.host}:{self.config.port}",
            prefer_grpc=False
        )
        
        # Verify connection
        collections = self._client.get_collections()
        self._is_connected = True
    
    async def disconnect(self) -> None:
        """Close Qdrant connection."""
        if self._client:
            self._client.close()
            self._client = None
        self._is_connected = False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Qdrant health."""
        try:
            collections = self._client.get_collections()
            return {
                "status": "healthy",
                "backend": "qdrant",
                "collections_count": len(collections),
                "details": {
                    "endpoint": f"{self.config.host}:{self.config.port}",
                    "version": self._client.get_version()
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": "qdrant",
                "error": str(e)
            }
    
    async def ping(self) -> bool:
        """Ping Qdrant backend."""
        try:
            self._client.get_collections()
            return True
        except:
            return False
    
    async def create_collection(
        self,
        collection_name: str,
        vector_size: int,
        distance_metric: str = "Cosine",
        **kwargs
    ) -> bool:
        """Create collection in Qdrant."""
        from qdrant_client.models import Distance, VectorParams, CollectionInfo
        
        # Map distance metric names
        distance_mapping = {
            "Cosine": Distance.COSINE,
            "Euclidean": Distance.EUCLID,
            "Dot": Distance.DOT,
        }
        
        qdrant_metric = distance_mapping.get(distance_metric, Distance.COSINE)
        
        self._client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=qdrant_metric,
                **kwargs
            )
        )
        
        return True
    
    async def delete_collection(self, collection_name: str) -> bool:
        """Delete collection from Qdrant."""
        self._client.delete_collection(collection_name)
        return True
    
    async def collection_exists(self, collection_name: str) -> bool:
        """Check if collection exists in Qdrant."""
        collections = self._client.get_collections()
        return any(c.name == collection_name for c in collections)
    
    async def list_collections(self) -> List[str]:
        """List all collections in Qdrant."""
        collections = self._client.get_collections()
        return [c.name for c in collections]
    
    async def insert_vectors(
        self,
        collection_name: str,
        vectors: List[List[float]],
        payloads: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Insert vectors into Qdrant collection."""
        from qdrant_client.models import PointStruct
        
        points = []
        for i, vector in enumerate(vectors):
            point = PointStruct(
                id=ids[i] if ids else None,
                vector=vector,
                payload=payloads[i] if payloads else None
            )
            points.append(point)
        
        operation_info = self._client.upsert(
            collection_name=collection_name,
            points=points
        )
        
        return [p.id for p in points]
    
    async def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: Optional[float] = None,
        filter_condition: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors in Qdrant."""
        from qdrant_client.models import Filter, SearchRequest
        
        search_result = self._client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=Filter(**filter_condition) if filter_condition else None,
            **kwargs
        )
        
        results = []
        for hit in search_result:
            results.append({
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload,
                "vector": hit.vector
            })
        
        return results
    
    async def delete_vectors(
        self,
        collection_name: str,
        ids: List[str],
    ) -> bool:
        """Delete vectors from Qdrant collection."""
        self._client.delete(
            collection_name=collection_name,
            points_selector=ids
        )
        return True
    
    async def get_vector(
        self,
        collection_name: str,
        vector_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve vector from Qdrant by ID."""
        points = self._client.retrieve(
            collection_name=collection_name,
            ids=[vector_id]
        )
        
        if points:
            point = points[0]
            return {
                "id": point.id,
                "vector": point.vector,
                "payload": point.payload
            }
        return None
    
    async def update_vectors(
        self,
        collection_name: str,
        ids: List[str],
        vectors: Optional[List[List[float]]] = None,
        payloads: Optional[List[Dict[str, Any]] = None,
    ) -> bool:
        """Update vectors in Qdrant."""
        from qdrant_client.models import PointStruct
        
        points = []
        for i, vector_id in enumerate(ids):
            point = PointStruct(
                id=vector_id,
                vector=vectors[i] if vectors else None,
                payload=payloads[i] if payloads else None
            )
            points.append(point)
        
        self._client.upsert(
            collection_name=collection_name,
            points=points
        )
        
        return True
    
    async def get_collection_info(
        self,
        collection_name: str,
    ) -> Dict[str, Any]:
        """Get collection information from Qdrant."""
        collection_info = self._client.get_collection(collection_name)
        return {
            "name": collection_info.name,
            "vector_size": collection_info.config.params.vectors.size,
            "distance_metric": str(collection_info.config.params.distance),
            "vectors_count": collection_info.points_count,
            "status": collection_info.status
        }