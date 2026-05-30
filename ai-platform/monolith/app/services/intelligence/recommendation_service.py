"""
Recommendation Service - Monolith Architecture
Recommendation functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class RecommendationService:
    """Recommendation service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize recommendation service with actual components"""
        self.initialized = False
        
        # Initialize actual recommendation components
        try:
            # Import from the actual recommendation-engine code
            from recommendation.main import RecommendationEngine
            
            self.recommendation_engine = RecommendationEngine()
            
        except Exception as e:
            logger.error(f"Error initializing recommendation components: {e}")
    
    def initialize(self):
        """Initialize recommendation service"""
        try:
            logger.info("Initializing Recommendation Service with actual microservice code")
            self.initialized = True
            logger.info("Recommendation Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Recommendation Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for recommendation service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "recommendation_service",
            "architecture": "monolith",
            "components": {
                "recommendation_engine": "ready"
            }
        }
    
    async def get_content_recommendations(self, user_id: str, 
                                         context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get content recommendations using actual microservice logic
        
        Args:
            user_id: User identifier
            context: Recommendation context
            
        Returns:
            Content recommendations
        """
        try:
            logger.info(f"Getting content recommendations for user: {user_id}")
            
            # Use actual recommendation engine logic
            result = self.recommendation_engine.get_recommendations(user_id, context)
            
            logger.info(f"Content recommendations generated successfully for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting content recommendations: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def update_user_profile(self, user_id: str, 
                                 interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user profile using actual microservice logic
        
        Args:
            user_id: User identifier
            interaction_data: User interaction data
            
        Returns:
            Updated user profile
        """
        try:
            logger.info(f"Updating user profile for user: {user_id}")
            
            # Use actual recommendation engine logic
            result = self.recommendation_engine.update_profile(user_id, interaction_data)
            
            logger.info(f"User profile updated successfully for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
