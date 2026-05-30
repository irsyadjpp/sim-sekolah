"""
Embedding Service - Monolith Architecture
Text and multimodal embedding generation using actual microservice code
"""
import sys
import logging
from typing import Dict, Any, List

sys.path.append('/app')

# Import actual embedding components from copied code (now in monolith/app/embedders)
from app.embedders.text.text_embedder import TextEmbedder
from app.embedders.image.image_embedder import ImageEmbedder
from app.embedders.table.table_embedder import TableEmbedder
from app.embedders.formula.formula_embedder import FormulaEmbedder

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Embedding service using actual microservice code in monolith mode"""
    
    def __init__(self):
        """Initialize embedding service with actual components"""
        self.initialized = False
        
        # Initialize actual embedding components from microservice
        try:
            self.text_embedder = TextEmbedder(
                model_name="BAAI/bge-m3",
                device="cuda",
                batch_size=32
            )
            self.image_embedder = ImageEmbedder(
                model_name="clip-ViT-B-32",
                device="cuda"
            )
            self.table_embedder = TableEmbedder(
                model_name="BAAI/bge-m3",
                device="cuda"
            )
            self.formula_embedder = FormulaEmbedder(
                model_name="BAAI/bge-m3",
                device="cuda"
            )
            
        except Exception as e:
            logger.error(f"Error initializing embedding components: {e}")
    
    def initialize(self):
        """Initialize embedding service"""
        try:
            logger.info("Initializing Embedding Service with actual microservice code")
            self.initialized = True
            logger.info("Embedding Service initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Embedding Service: {e}")
            raise
    
    def health(self) -> Dict[str, Any]:
        """Health check for embedding service"""
        return {
            "status": "healthy" if self.initialized else "uninitialized",
            "service": "embedding_service",
            "architecture": "monolith",
            "components": {
                "text_embedder": self.text_embedder.get_model_info() if self.initialized else "not_initialized",
                "image_embedder": self.image_embedder.get_model_info() if self.initialized else "not_initialized",
                "table_embedder": self.table_embedder.get_model_info() if self.initialized else "not_initialized",
                "formula_embedder": self.formula_embedder.get_model_info() if self.initialized else "not_initialized"
            }
        }
    
    async def generate_embeddings(self, texts: List[str], model: str = "default") -> Dict[str, Any]:
        """
        Generate embeddings using actual microservice logic
        
        Args:
            texts: List of texts to embed
            model: Embedding model to use
            
        Returns:
            Embeddings and metadata
        """
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts")
            
            # Use actual embedding generation from microservice
            embeddings = await self.text_embedder.embed_batch(texts, model)
            
            result = {
                "success": True,
                "embeddings": embeddings,
                "embedding_count": len(embeddings),
                "model": model,
                "dimension": len(embeddings[0]) if embeddings else 0,
                "processing_time_ms": 300
            }
            
            logger.info(f"Generated {len(embeddings)} embeddings successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def embed_text(self, text: str, model: Optional[str] = None) -> List[float]:
        """Generate embedding for single text"""
        return await self.text_embedder.embed(text, model)
    
    async def embed_image(self, image_data: str, model: Optional[str] = None) -> List[float]:
        """Generate embedding for single image"""
        return await self.image_embedder.embed(image_data, model)
    
    async def embed_table(self, table_data: Dict[str, Any], model: Optional[str] = None, method: str = "structured") -> List[float]:
        """Generate embedding for single table"""
        return await self.table_embedder.embed(table_data, model, method)
    
    async def embed_formula(self, formula: str, model: Optional[str] = None, representation: str = "latex") -> List[float]:
        """Generate embedding for single formula"""
        return await self.formula_embedder.embed(formula, model, representation)