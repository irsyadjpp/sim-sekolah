"""
Hybrid retriever combining semantic and keyword search
Implements fusion of vector and BM25/keyword search
"""
from typing import List, Optional, Dict, Any
import math
import logging

logger = logging.getLogger(__name__)


class HybridRetriever:
    """Hybrid retriever combining semantic and keyword search"""
    
    def __init__(
        self,
        qdrant_url: str,
        qdrant_api_key: Optional[str] = None
    ):
        """
        Initialize hybrid retriever
        
        Args:
            qdrant_url: Qdrant server URL
            qdrant_api_key: Optional Qdrant API key
        """
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        
        logger.info(f"Initializing hybrid retriever with Qdrant: {qdrant_url}")
        
        # Import semantic retriever for vector search
        from .semantic_retriever import SemanticRetriever
        self.semantic_retriever = SemanticRetriever(qdrant_url, qdrant_api_key)
        
        logger.info("Hybrid retriever initialized successfully")
    
    async def search(
        self,
        query: str,
        collection_name: str = "documents",
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining semantic and keyword results
        
        Args:
            query: Search query text
            collection_name: Qdrant collection name
            semantic_weight: Weight for semantic search results
            keyword_weight: Weight for keyword search results
            limit: Number of results to return
            filters: Optional metadata filters
        
        Returns:
            List of fused search results
        """
        try:
            # Perform semantic search
            semantic_results = await self.semantic_retriever.search(
                query=query,
                collection_name=collection_name,
                limit=limit * 2,  # Get more for fusion
                filters=filters
            )
            
            # Perform keyword search (BM25 simulation)
            keyword_results = await self._keyword_search(
                query=query,
                collection_name=collection_name,
                limit=limit * 2,
                filters=filters
            )
            
            # Fuse results using reciprocal rank fusion
            fused_results = self._reciprocal_rank_fusion(
                semantic_results=semantic_results,
                keyword_results=keyword_results,
                semantic_weight=semantic_weight,
                keyword_weight=keyword_weight,
                limit=limit
            )
            
            return fused_results
            
        except Exception as e:
            logger.error(f"Error in hybrid search: {str(e)}")
            raise
    
    async def _keyword_search(
        self,
        query: str,
        collection_name: str,
        limit: int,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform keyword search (BM25 simulation)
        
        Args:
            query: Search query
            collection_name: Collection name
            limit: Number of results
            filters: Optional filters
        
        Returns:
            List of keyword search results
        """
        try:
            # In a full implementation, this would use a proper search engine
            # For now, we'll simulate keyword search using text matching
            
            # Get all documents from collection (in production, use proper search)
            # This is a simplified implementation
            semantic_results = await self.semantic_retriever.search(
                query=query,
                collection_name=collection_name,
                limit=limit,
                filters=filters
            )
            
            # Simulate keyword scoring based on term frequency
            query_terms = query.lower().split()
            keyword_results = []
            
            for result in semantic_results:
                content = result["content"].lower()
                score = self._calculate_keyword_score(content, query_terms)
                
                keyword_results.append({
                    "id": result["id"],
                    "score": score,
                    "content": result["content"],
                    "metadata": result["metadata"]
                })
            
            # Sort by keyword score
            keyword_results.sort(key=lambda x: x["score"], reverse=True)
            
            return keyword_results[:limit]
            
        except Exception as e:
            logger.error(f"Error in keyword search: {str(e)}")
            return []
    
    def _calculate_keyword_score(self, content: str, query_terms: List[str]) -> float:
        """
        Calculate keyword score based on term frequency
        
        Args:
            content: Document content
            query_terms: Query terms
        
        Returns:
            Keyword score
        """
        score = 0.0
        content_words = content.split()
        
        for term in query_terms:
            # Count term frequency
            tf = content_words.count(term)
            
            # Calculate IDF (simplified)
            idf = 1.0  # In production, calculate from corpus
            
            # BM25-like scoring
            score += (tf * (1.5 + 1)) / (tf + 1.5 * (1 - 0.75 + 0.75 * (len(content_words) / 1000))) * idf
        
        return score
    
    def _reciprocal_rank_fusion(
        self,
        semantic_results: List[Dict[str, Any]],
        keyword_results: List[Dict[str, Any]],
        semantic_weight: float,
        keyword_weight: float,
        limit: int,
        k: int = 60
    ) -> List[Dict[str, Any]]:
        """
        Fuse results using reciprocal rank fusion
        
        Args:
            semantic_results: Semantic search results
            keyword_results: Keyword search results
            semantic_weight: Weight for semantic results
            keyword_weight: Weight for keyword results
            limit: Number of results to return
            k: RRF constant
        
        Returns:
            Fused results
        """
        # Score dictionaries
        fused_scores = {}
        result_map = {}
        
        # Process semantic results
        for rank, result in enumerate(semantic_results):
            doc_id = result["id"]
            if doc_id not in fused_scores:
                fused_scores[doc_id] = 0.0
                result_map[doc_id] = result
            
            # RRF score: 1 / (k + rank)
            fused_scores[doc_id] += semantic_weight * (1.0 / (k + rank + 1))
        
        # Process keyword results
        for rank, result in enumerate(keyword_results):
            doc_id = result["id"]
            if doc_id not in fused_scores:
                fused_scores[doc_id] = 0.0
                result_map[doc_id] = result
            
            # RRF score: 1 / (k + rank)
            fused_scores[doc_id] += keyword_weight * (1.0 / (k + rank + 1))
        
        # Sort by fused score
        sorted_results = sorted(
            fused_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Return top results
        final_results = []
        for doc_id, score in sorted_results[:limit]:
            result = result_map[doc_id].copy()
            result["score"] = score
            final_results.append(result)
        
        return final_results