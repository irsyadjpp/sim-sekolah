"""
Formula embedder for generating embeddings from mathematical formulas
Supports LaTeX formula embedding
"""
import torch
from typing import List, Optional
import re
import logging

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("sentence-transformers not available")

logger = logging.getLogger(__name__)


class FormulaEmbedder:
    """Formula embedder for generating embeddings from mathematical formulas"""
    
    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        device: str = "cuda"
    ):
        """
        Initialize formula embedder
        
        Args:
            model_name: Model name (default: BAAI/bge-m3 for formula text)
            device: Device to use (cuda/cpu)
        """
        self.model_name = model_name
        self.device = device if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Loading formula embedding model: {model_name}")
        logger.info(f"Using device: {self.device}")
        
        try:
            if TRANSFORMERS_AVAILABLE:
                # Load text model for formula representation
                self.model = SentenceTransformer(model_name, device=self.device)
                self.dimension = self.model.get_sentence_embedding_dimension()
                logger.info(f"Formula embedder loaded successfully. Dimension: {self.dimension}")
            else:
                self.model = None
                self.dimension = 1024
                logger.warning("Transformers not available, using fallback implementation")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            self.model = None
            self.dimension = 1024
    
    def _normalize_formula(self, formula: str) -> str:
        """
        Normalize LaTeX formula for consistent embedding
        
        Args:
            formula: LaTeX formula string
        
        Returns:
            Normalized formula string
        """
        try:
            # Remove extra whitespace
            formula = re.sub(r'\s+', ' ', formula).strip()
            
            # Remove common LaTeX commands that don't affect meaning
            # (this is a simple implementation, could be more sophisticated)
            formula = re.sub(r'\\[a-z]+(?:\[[^\]]*\])?', '', formula)
            
            # Replace special characters with spaces
            formula = re.sub(r'[^a-zA-Z0-9\+\-\*\/\=\<\>]', ' ', formula)
            
            # Remove multiple spaces
            formula = re.sub(r'\s+', ' ', formula).strip()
            
            return formula
            
        except Exception as e:
            logger.error(f"Error normalizing formula: {str(e)}")
            return formula
    
    def _formula_to_text(
        self,
        formula: str,
        representation: str = "latex"
    ) -> str:
        """
        Convert formula to text representation
        
        Args:
            formula: LaTeX formula string
            representation: Representation type ('latex', 'normalized', 'descriptive')
        
        Returns:
            String representation of the formula
        """
        try:
            if representation == "latex":
                return formula
            
            elif representation == "normalized":
                return self._normalize_formula(formula)
            
            elif representation == "descriptive":
                # Add descriptive context
                normalized = self._normalize_formula(formula)
                return f"Mathematical formula: {normalized}"
            
            else:
                return formula
                
        except Exception as e:
            logger.error(f"Error converting formula to text: {str(e)}")
            return formula
    
    async def embed(
        self,
        formula: str,
        model: Optional[str] = None,
        representation: str = "latex"
    ) -> List[float]:
        """
        Generate embedding for mathematical formula
        
        Args:
            formula: LaTeX formula string
            model: Optional model name
            representation: Formula representation type
        
        Returns:
            List of floats representing the embedding vector
        """
        try:
            # Convert formula to text
            formula_text = self._formula_to_text(formula, representation)
            
            if self.model is None:
                # Fallback: generate simple hash-based embedding
                return self._fallback_embedding(formula_text)
            
            # Generate embedding using text model
            embedding = self.model.encode(
                formula_text,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating formula embedding: {str(e)}")
            raise
    
    async def embed_batch(
        self,
        formulas: List[str],
        model: Optional[str] = None,
        batch_size: int = 32,
        representation: str = "latex"
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple formulas in batch
        
        Args:
            formulas: List of LaTeX formula strings
            model: Optional model name
            batch_size: Batch size for processing
            representation: Formula representation type
        
        Returns:
            List of embedding vectors
        """
        try:
            # Convert formulas to text
            formula_texts = [self._formula_to_text(formula, representation) for formula in formulas]
            
            if self.model is None:
                # Fallback for each formula
                return [self._fallback_embedding(text) for text in formula_texts]
            
            # Generate embeddings in batch
            embeddings = self.model.encode(
                formula_texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating batch formula embeddings: {str(e)}")
            raise
    
    def _fallback_embedding(self, text: str) -> List[float]:
        """
        Generate fallback embedding when model is not available
        
        Args:
            text: Text representation
        
        Returns:
            List of floats representing a simple embedding
        """
        # Simple hash-based embedding
        import hashlib
        import numpy as np
        
        # Create hash of the text
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to float array and expand to target dimension
        hash_array = np.frombuffer(hash_bytes, dtype=np.uint8).astype(np.float32) / 255.0
        
        # Pad to target dimension
        if len(hash_array) < self.dimension:
            padded = np.pad(hash_array, (0, self.dimension - len(hash_array)))
        else:
            padded = hash_array[:self.dimension]
        
        return padded.tolist()
    
    def get_dimension(self) -> int:
        """Get the embedding dimension"""
        return self.dimension
    
    def get_model_info(self) -> dict:
        """Get model information"""
        return {
            "model_name": self.model_name,
            "dimension": self.dimension,
            "device": self.device,
            "transformers_available": TRANSFORMERS_AVAILABLE,
            "note": "Formula embedding uses text model on LaTeX representation"
        }