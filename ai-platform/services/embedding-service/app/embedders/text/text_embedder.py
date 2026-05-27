"""
Text embedder using BAAI/bge-m3 and other multilingual models
Supports Indonesian and English text embedding
"""
import torch
from typing import List, Optional
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

logger = logging.getLogger(__name__)


class TextEmbedder:
    """Text embedder for generating embeddings from text"""
    
    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        device: str = "cuda",
        batch_size: int = 32
    ):
        """
        Initialize text embedder
        
        Args:
            model_name: Model name (default: BAAI/bge-m3)
            device: Device to use (cuda/cpu)
            batch_size: Batch size for processing
        """
        self.model_name = model_name
        self.device = device if torch.cuda.is_available() else "cpu"
        self.batch_size = batch_size
        
        logger.info(f"Loading text embedding model: {model_name}")
        logger.info(f"Using device: {self.device}")
        
        try:
            # Load the model
            self.model = SentenceTransformer(model_name, device=self.device)
            self.dimension = self.model.get_sentence_embedding_dimension()
            logger.info(f"Model loaded successfully. Dimension: {self.dimension}")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            raise
    
    async def embed(
        self,
        text: str,
        model: Optional[str] = None
    ) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            model: Optional model name (defaults to initialized model)
        
        Returns:
            List of floats representing the embedding vector
        """
        try:
            # Use specified model or default
            model_to_use = model if model else self.model_name
            
            # Generate embedding
            embedding = self.model.encode(
                text,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False
            )
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    async def embed_batch(
        self,
        texts: List[str],
        model: Optional[str] = None,
        batch_size: Optional[int] = None
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch
        
        Args:
            texts: List of texts to embed
            model: Optional model name
            batch_size: Optional batch size
        
        Returns:
            List of embedding vectors
        """
        try:
            # Use specified batch size or default
            bs = batch_size if batch_size else self.batch_size
            
            # Generate embeddings in batch
            embeddings = self.model.encode(
                texts,
                batch_size=bs,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False
            )
            
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise
    
    async def embed_with_metadata(
        self,
        text: str,
        metadata: Optional[dict] = None
    ) -> dict:
        """
        Generate embedding with metadata
        
        Args:
            text: Text to embed
            metadata: Optional metadata dictionary
        
        Returns:
            Dictionary with embedding and metadata
        """
        embedding = await self.embed(text)
        
        result = {
            "embedding": embedding,
            "text": text,
            "text_length": len(text),
            "word_count": len(text.split()),
            "model": self.model_name,
            "dimension": self.dimension
        }
        
        if metadata:
            result["metadata"] = metadata
        
        return result
    
    def switch_model(self, model_name: str):
        """
        Switch to a different embedding model
        
        Args:
            model_name: New model name to load
        """
        logger.info(f"Switching to model: {model_name}")
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, device=self.device)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Model switched successfully. New dimension: {self.dimension}")
    
    def get_dimension(self) -> int:
        """Get the embedding dimension"""
        return self.dimension
    
    def get_model_info(self) -> dict:
        """Get model information"""
        return {
            "model_name": self.model_name,
            "dimension": self.dimension,
            "device": self.device,
            "batch_size": self.batch_size
        }