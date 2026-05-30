"""
Reranking Service - Monolith Architecture
Reranking functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class RerankingService:
    """Reranking service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize reranking service with actual components"""
        self.initialized = False
        
        # Initialize actual reranking components
        try:
            # Import from the actual reranking-service code
            from reranking.main import RerankingEngine
            
            self.reranking_engine = RerankingEngine()
            
        except Exception as e:
            logger.error(f"Error initializing reranking components: {e}")
    
    def initialize(self):
        """Initialize reranking service"""
        try:
            logger.info("Initializing Reranking Service with actual microservice code")
            self.initialized = True
            logger.info("Reranking Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Reranking Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for reranking service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "reranking_service",
            "architecture": "monolith",
            "components": {
                "reranking_engine": "ready"
            }
        }
    
    async def rerank_results(self, query: str, initial_results: List[Dict[str, Any]], 
                            strategy: str = "cross_encoder") -> Dict[str, Any]:
        """
        Rerank retrieval results using actual microservice logic
        
        Args:
            query: Original query
            initial_results: Initial retrieval results
            strategy: Reranking strategy
            
        Returns:
            Reranked results
        """
        try:
            logger.info("Reranking retrieval results")
            
            # Use actual reranking engine logic
            result = await self.reranking_engine.rerank_results(query, initial_results, strategy)
            
            logger.info("Results reranked successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error reranking results: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def cross_encoder_rerank(self, query: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Rerank using cross-encoder using actual microservice logic
        
        Args:
            query: Query string
            documents: Documents to rerank
            
        Returns:
            Cross-encoder reranked results
        """
        try:
            logger.info("Cross-encoder reranking")
            
            # Use actual reranking engine logic
            result = await self.reranking_engine.cross_encoder_rerank(query, documents)
            
            logger.info("Cross-encoder reranking completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in cross-encoder reranking: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def score_documents(self, query: str, documents: List[Dict[str, Any]], 
                           scoring_method: str = "relevance") -> Dict[str, Any]:
        """
        Score documents for reranking using actual microservice logic
        
        Args:
            query: Query string
            documents: Documents to score
            scoring_method: Scoring method
            
        Returns:
            Document scores
        """
        try:
            logger.info("Scoring documents for reranking")
            
            # Use actual reranking engine logic
            result = await self.reranking_engine.score_documents(query, documents, scoring_method)
            
            logger.info("Document scoring completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error scoring documents: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
