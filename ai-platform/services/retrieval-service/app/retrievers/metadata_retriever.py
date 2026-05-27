"""
Metadata retriever for filtering and searching by metadata
Supports complex filtering on document metadata
"""
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchText, Range
import logging

logger = logging.getLogger(__name__)


class MetadataRetriever:
    """Metadata retriever for filtering-based search"""
    
    def __init__(
        self,
        qdrant_url: str,
        qdrant_api_key: Optional[str] = None
    ):
        """
        Initialize metadata retriever
        
        Args:
            qdrant_url: Qdrant server URL
            qdrant_api_key: Optional Qdrant API key
        """
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        
        logger.info(f"Initializing metadata retriever with Qdrant: {qdrant_url}")
        
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
        collection_name: str = "documents",
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        order_by: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform metadata-based search
        
        Args:
            collection_name: Qdrant collection name
            filters: Metadata filters
            limit: Number of results to return
            order_by: Field to order results by
        
        Returns:
            List of filtered results
        """
        try:
            # Build filter
            query_filter = None
            if filters:
                query_filter = self._build_filter(filters)
            
            # Perform scroll search with filters
            search_result = self.client.scroll(
                collection_name=collection_name,
                limit=limit,
                order_by=order_by,
                with_payload=True,
                with_vectors=False,
                query_filter=query_filter
            )
            
            # Format results
            results = []
            for point in search_result[0]:
                results.append({
                    "id": point.id,
                    "score": 1.0,  # Perfect match for filter-based search
                    "content": point.payload.get("content", ""),
                    "metadata": point.payload.get("metadata", {})
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in metadata search: {str(e)}")
            raise
    
    def _build_filter(self, filters: Dict[str, Any]) -> Filter:
        """
        Build Qdrant filter from dictionary
        
        Args:
            filters: Filter dictionary with operators
        
        Returns:
            Qdrant Filter object
        """
        conditions = []
        
        for key, value in filters.items():
            if isinstance(value, dict):
                # Handle operators
                for op, val in value.items():
                    if op == "$eq":
                        conditions.append(FieldCondition(key=key, match=MatchValue(value=val)))
                    elif op == "$ne":
                        # Handle not equal (Qdrant doesn't have direct not equal)
                        pass  # Would need to implement using must_not
                    elif op == "$gt":
                        conditions.append(FieldCondition(key=key, range=Range(gt=val)))
                    elif op == "$gte":
                        conditions.append(FieldCondition(key=key, range=Range(gte=val)))
                    elif op == "$lt":
                        conditions.append(FieldCondition(key=key, range=Range(lt=val)))
                    elif op == "$lte":
                        conditions.append(FieldCondition(key=key, range=Range(lte=val)))
                    elif op == "$in":
                        if isinstance(val, list):
                            # Handle in operator (Qdrant doesn't have direct in)
                            # Would need to implement multiple MatchValue conditions
                            for v in val:
                                conditions.append(FieldCondition(key=key, match=MatchValue(value=v)))
                    elif op == "$contains":
                        conditions.append(FieldCondition(key=key, match=MatchText(text=val)))
            else:
                # Simple equality
                conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
        
        return Filter(must=conditions)
    
    async def search_by_curriculum(
        self,
        collection_name: str,
        curriculum_level: str,
        subject: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search by curriculum metadata (Kurikulum Merdeka specific)
        
        Args:
            collection_name: Collection name
            curriculum_level: Curriculum level (SD, SMP, SMA)
            subject: Subject name
            limit: Number of results
        
        Returns:
            Filtered results
        """
        filters = {
            "curriculum_level": curriculum_level,
            "subject": subject
        }
        
        return await self.search(
            collection_name=collection_name,
            filters=filters,
            limit=limit
        )
    
    async def search_by_competency(
        self,
        collection_name: str,
        competency_type: str,  # KI-1, KI-2, KI-3, KI-4
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search by competency type
        
        Args:
            collection_name: Collection name
            competency_type: Competency type
            limit: Number of results
        
        Returns:
            Filtered results
        """
        filters = {
            "competency_type": competency_type
        }
        
        return await self.search(
            collection_name=collection_name,
            filters=filters,
            limit=limit
        )
    
    async def search_by_difficulty(
        self,
        collection_name: str,
        difficulty: str,  # easy, medium, hard
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search by difficulty level
        
        Args:
            collection_name: Collection name
            difficulty: Difficulty level
            limit: Number of results
        
        Returns:
            Filtered results
        """
        filters = {
            "difficulty": difficulty
        }
        
        return await self.search(
            collection_name=collection_name,
            filters=filters,
            limit=limit
        )
    
    async def search_by_taxonomy(
        self,
        collection_name: str,
        bloom_level: str,  # remember, understand, apply, analyze, evaluate, create
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search by Bloom's taxonomy level
        
        Args:
            collection_name: Collection name
            bloom_level: Bloom's taxonomy level
            limit: Number of results
        
        Returns:
            Filtered results
        """
        filters = {
            "bloom_taxonomy": bloom_level
        }
        
        return await self.search(
            collection_name=collection_name,
            filters=filters,
            limit=limit
        )