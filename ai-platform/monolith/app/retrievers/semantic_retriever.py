"""
Semantic retriever using Qdrant vector database
Performs semantic search using vector embeddings
"""
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, PointStruct
import logging

logger = logging.getLogger(__name__)


class SemanticRetriever:
    """Semantic retriever for vector-based search"""
    
    def __init__(
        self,
        qdrant_url: str,
        qdrant_api_key: Optional[str] = None
    ):
        """
        Initialize semantic retriever
        
        Args:
            qdrant_url: Qdrant server URL
            qdrant_api_key: Optional Qdrant API key
        """
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        
        logger.info(f"Initializing semantic retriever with Qdrant: {qdrant_url}")
        
        try:
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
                timeout=30
            )
            
            # Test connection
            collections = self.client.get_collections()
            logger.info(f"Connected to Qdrant. Collections: {len(collections.collections)}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {str(e)}")
            raise
    
    async def search(
        self,
        query: str,
        collection_name: str = "documents",
        limit: int = 10,
        score_threshold: Optional[float] = None,
        filters: Optional[Dict[str, Any]] = None,
        embedding_vector: Optional[List[float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search
        
        Args:
            query: Search query text
            collection_name: Qdrant collection name
            limit: Number of results to return
            score_threshold: Minimum score threshold
            filters: Optional metadata filters
            embedding_vector: Optional pre-computed embedding vector
        
        Returns:
            List of search results with scores
        """
        try:
            # Build filter if provided
            query_filter = None
            if filters:
                query_filter = self._build_filter(filters)
            
            # If embedding vector is provided, use it directly
            if embedding_vector:
                search_result = self.client.search(
                    collection_name=collection_name,
                    query_vector=embedding_vector,
                    limit=limit,
                    score_threshold=score_threshold,
                    query_filter=query_filter
                )
            else:
                # Note: In production, you would generate embedding here
                # For now, we'll assume embedding is provided or use a placeholder
                logger.warning("No embedding vector provided, using placeholder search")
                search_result = self.client.search(
                    collection_name=collection_name,
                    query_vector=[0.1] * 1024,  # Placeholder
                    limit=limit,
                    score_threshold=score_threshold,
                    query_filter=query_filter
                )
            
            # Format results
            results = []
            for hit in search_result:
                results.append({
                    "id": hit.id,
                    "score": hit.score,
                    "content": hit.payload.get("content", ""),
                    "metadata": hit.payload.get("metadata", {})
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}")
            raise
    
    def _build_filter(self, filters: Dict[str, Any]) -> Filter:
        """
        Build Qdrant filter from dictionary
        
        Args:
            filters: Filter dictionary
        
        Returns:
            Qdrant Filter object
        """
        conditions = []
        
        for key, value in filters.items():
            if isinstance(value, dict):
                # Handle nested filters
                for op, val in value.items():
                    if op == "$eq":
                        conditions.append(FieldCondition(key=key, match=MatchValue(value=val)))
                    # Add more operators as needed
            else:
                conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
        
        return Filter(must=conditions)
    
    async def list_collections(self) -> List[Dict[str, Any]]:
        """
        List all collections in Qdrant
        
        Returns:
            List of collection information
        """
        try:
            collections = self.client.get_collections()
            return [
                {
                    "name": coll.name,
                    "points_count": coll.points_count,
                    "vectors_count": coll.vectors_count
                }
                for coll in collections.collections
            ]
        except Exception as e:
            logger.error(f"Error listing collections: {str(e)}")
            raise
    
    async def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """
        Get information about a specific collection
        
        Args:
            collection_name: Collection name
        
        Returns:
            Collection information
        """
        try:
            info = self.client.get_collection(collection_name)
            return {
                "name": collection_name,
                "points_count": info.points_count,
                "vectors_count": info.vectors_count,
                "config": info.config
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            raise
    
    async def insert_points(
        self,
        collection_name: str,
        points: List[Dict[str, Any]]
    ) -> bool:
        """
        Insert points into collection
        
        Args:
            collection_name: Collection name
            points: List of points to insert
        
        Returns:
            Success status
        """
        try:
            qdrant_points = [
                PointStruct(
                    id=point["id"],
                    vector=point["vector"],
                    payload=point.get("payload", {})
                )
                for point in points
            ]
            
            self.client.upsert(
                collection_name=collection_name,
                points=qdrant_points
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error inserting points: {str(e)}")
            return False