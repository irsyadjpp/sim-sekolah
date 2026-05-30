"""
Hallucination Guard Service - Monolith Architecture
Hallucination detection and prevention functionality using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List, Optional

sys.path.append('/app')

logger = logging.getLogger(__name__)


class HallucinationGuardService:
    """Hallucination guard service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize hallucination guard service with actual components"""
        self.initialized = False
        
        # Initialize actual hallucination guard components
        try:
            # Import from the actual hallucination-guard-service code
            from hallucination_guard.main import HallucinationGuardEngine
            
            self.guard_engine = HallucinationGuardEngine()
            
        except Exception as e:
            logger.error(f"Error initializing hallucination guard components: {e}")
    
    def initialize(self):
        """Initialize hallucination guard service"""
        try:
            logger.info("Initializing Hallucination Guard Service with actual microservice code")
            self.initialized = True
            logger.info("Hallucination Guard Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Hallucination Guard Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for hallucination guard service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "hallucination_guard_service",
            "architecture": "monolith",
            "components": {
                "guard_engine": "ready"
            }
        }
    
    async def detect_hallucination(self, generated_text: str, context: str, 
                                  confidence_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Detect hallucination in generated text using actual microservice logic
        
        Args:
            generated_text: Generated text to check
            context: Original context
            confidence_threshold: Threshold for hallucination detection
            
        Returns:
            Hallucination detection result
        """
        try:
            logger.info("Detecting hallucination in generated text")
            
            # Use actual guard engine logic
            result = await self.guard_engine.detect_hallucination(generated_text, context, confidence_threshold)
            
            logger.info("Hallucination detection completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error detecting hallucination: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def validate_facts(self, statements: List[str], knowledge_base: str = None) -> Dict[str, Any]:
        """
        Validate factual accuracy of statements using actual microservice logic
        
        Args:
            statements: Statements to validate
            knowledge_base: Optional knowledge base to validate against
            
        Returns:
            Fact validation result
        """
        try:
            logger.info("Validating facts in statements")
            
            # Use actual guard engine logic
            result = await self.guard_engine.validate_facts(statements, knowledge_base)
            
            logger.info("Fact validation completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error validating facts: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def check_consistency(self, response: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Check consistency of response with conversation history using actual microservice logic
        
        Args:
            response: Response to check
            conversation_history: Optional conversation history
            
        Returns:
            Consistency check result
        """
        try:
            logger.info("Checking response consistency")
            
            # Use actual guard engine logic
            result = await self.guard_engine.check_consistency(response, conversation_history or [])
            
            logger.info("Consistency check completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error checking consistency: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
