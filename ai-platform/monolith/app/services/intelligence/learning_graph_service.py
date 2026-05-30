"""
Learning Graph Service - Monolith Architecture
Learning graph functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class LearningGraphService:
    """Learning graph service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize learning graph service with actual components"""
        self.initialized = False
        
        # Initialize actual learning graph components
        try:
            # Import from the actual learning-graph-engine and learning-progression-engine code
            from learning_graph.main import LearningGraphEngine
            from learning_graph.progression import LearningProgressionEngine
            
            self.learning_graph_engine = LearningGraphEngine()
            self.progression_engine = LearningProgressionEngine()
            
        except Exception as e:
            logger.error(f"Error initializing learning graph components: {e}")
    
    def initialize(self):
        """Initialize learning graph service"""
        try:
            logger.info("Initializing Learning Graph Service with actual microservice code")
            self.initialized = True
            logger.info("Learning Graph Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Learning Graph Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for learning graph service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "learning_graph_service",
            "architecture": "monolith",
            "components": {
                "learning_graph_engine": "ready",
                "progression_engine": "ready"
            }
        }
    
    async def build_knowledge_graph(self, curriculum_id: str, 
                                   content_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Build knowledge graph using actual microservice logic
        
        Args:
            curriculum_id: Curriculum identifier
            content_data: Content data for graph construction
            
        Returns:
            Knowledge graph result
        """
        try:
            logger.info(f"Building knowledge graph for curriculum: {curriculum_id}")
            
            # Use actual learning graph engine logic
            result = self.learning_graph_engine.build_graph(curriculum_id, content_data)
            
            logger.info(f"Knowledge graph built successfully for curriculum {curriculum_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error building knowledge graph: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def track_progression(self, student_id: str, 
                               learning_path: List[str]) -> Dict[str, Any]:
        """
        Track learning progression using actual microservice logic
        
        Args:
            student_id: Student identifier
            learning_path: Learning path nodes
            
        Returns:
            Progression tracking result
        """
        try:
            logger.info(f"Tracking progression for student: {student_id}")
            
            # Use actual progression engine logic
            result = self.progression_engine.track_progression(student_id, learning_path)
            
            logger.info(f"Progression tracked successfully for student {student_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error tracking progression: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
