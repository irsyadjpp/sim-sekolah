"""
Cross-encoder reranker for document re-ranking
Uses cross-encoder models for precise relevance scoring
"""
import torch
from typing import List, Optional, Dict, Any
import logging

try:
    from sentence_transformers import CrossEncoder
    CROSS_ENCODER_AVAILABLE = True
except ImportError:
    CROSS_ENCODER_AVAILABLE = False
    logging.warning("sentence-transformers not available for cross-encoder")

logger = logging.getLogger(__name__)


class CrossEncoderReranker:
    """Cross-encoder reranker for document re-ranking"""
    
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        device: str = "cuda"
    ):
        """
        Initialize cross-encoder reranker
        
        Args:
            model_name: Cross-encoder model name
            device: Device to use (cuda/cpu)
        """
        self.model_name = model_name
        self.device = device if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Loading cross-encoder model: {model_name}")
        logger.info(f"Using device: {self.device}")
        
        try:
            if CROSS_ENCODER_AVAILABLE:
                self.model = CrossEncoder(model_name, device=self.device)
                logger.info("Cross-encoder model loaded successfully")
            else:
                self.model = None
                logger.warning("Cross-encoder not available, using fallback scoring")
        except Exception as e:
            logger.error(f"Failed to load cross-encoder model: {str(e)}")
            self.model = None
    
    async def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents using cross-encoder model
        
        Args:
            query: Search query
            documents: List of documents with content and metadata
            top_k: Number of top results to return
        
        Returns:
            List of reranked documents with new scores
        """
        try:
            if self.model is None:
                # Fallback to simple scoring
                return self._fallback_rerank(query, documents, top_k)
            
            # Prepare query-document pairs
            pairs = []
            for doc in documents:
                content = doc.get("content", "")
                pairs.append([query, content])
            
            # Predict scores
            scores = self.model.predict(pairs)
            
            # Add scores to documents and sort
            scored_documents = []
            for doc, score in zip(documents, scores):
                scored_doc = doc.copy()
                scored_doc["rerank_score"] = float(score)
                scored_documents.append(scored_doc)
            
            # Sort by score (descending)
            scored_documents.sort(key=lambda x: x["rerank_score"], reverse=True)
            
            # Add rank
            for i, doc in enumerate(scored_documents):
                doc["rank"] = i + 1
            
            # Return top_k if specified
            if top_k:
                return scored_documents[:top_k]
            
            return scored_documents
            
        except Exception as e:
            logger.error(f"Error in cross-encoder reranking: {str(e)}")
            # Fallback to simple scoring
            return self._fallback_rerank(query, documents, top_k)
    
    def _fallback_rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: Optional[int]
    ) -> List[Dict[str, Any]]:
        """
        Fallback reranking using simple text similarity
        
        Args:
            query: Search query
            documents: List of documents
            top_k: Number of top results
        
        Returns:
            List of reranked documents
        """
        query_terms = set(query.lower().split())
        
        scored_documents = []
        for doc in documents:
            content = doc.get("content", "").lower()
            content_terms = set(content.split())
            
            # Simple term overlap score
            intersection = query_terms & content_terms
            score = len(intersection) / len(query_terms) if query_terms else 0.0
            
            scored_doc = doc.copy()
            scored_doc["rerank_score"] = score
            scored_documents.append(scored_doc)
        
        # Sort by score (descending)
        scored_documents.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        # Add rank
        for i, doc in enumerate(scored_documents):
            doc["rank"] = i + 1
        
        # Return top_k if specified
        if top_k:
            return scored_documents[:top_k]
        
        return scored_documents
    
    async def rerank_with_metadata(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        metadata_weights: Optional[Dict[str, float]] = None,
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents with metadata weighting
        
        Args:
            query: Search query
            documents: List of documents
            metadata_weights: Weights for metadata fields
            top_k: Number of top results
        
        Returns:
            List of reranked documents with combined scores
        """
        # First, get cross-encoder scores
        reranked = await self.rerank(query, documents, top_k=None)
        
        if not metadata_weights:
            return reranked[:top_k] if top_k else reranked
        
        # Apply metadata weights
        for doc in reranked:
            base_score = doc.get("rerank_score", 0.0)
            metadata_score = 0.0
            
            for field, weight in metadata_weights.items():
                metadata = doc.get("metadata", {})
                value = metadata.get(field, "")
                
                # Simple term overlap for metadata
                if value:
                    query_terms = set(query.lower().split())
                    value_terms = set(str(value).lower().split())
                    intersection = query_terms & value_terms
                    field_score = len(intersection) / len(query_terms) if query_terms else 0.0
                    metadata_score += field_score * weight
            
            # Combine scores (weighted average)
            combined_score = 0.7 * base_score + 0.3 * metadata_score
            doc["rerank_score"] = combined_score
        
        # Re-sort by combined score
        reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        # Update ranks
        for i, doc in enumerate(reranked):
            doc["rank"] = i + 1
        
        # Return top_k if specified
        if top_k:
            return reranked[:top_k]
        
        return reranked
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "cross_encoder_available": CROSS_ENCODER_AVAILABLE
        }