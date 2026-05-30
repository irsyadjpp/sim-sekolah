"""
Table embedder for generating embeddings from tabular data
Supports structured table data embedding
"""
import torch
from typing import List, Optional, Dict, Any
import json
import logging

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("sentence-transformers not available")

logger = logging.getLogger(__name__)


class TableEmbedder:
    """Table embedder for generating embeddings from table data"""
    
    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        device: str = "cuda"
    ):
        """
        Initialize table embedder
        
        Args:
            model_name: Model name (default: BAAI/bge-m3 for table text)
            device: Device to use (cuda/cpu)
        """
        self.model_name = model_name
        self.device = device if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Loading table embedding model: {model_name}")
        logger.info(f"Using device: {self.device}")
        
        try:
            if TRANSFORMERS_AVAILABLE:
                # Load text model for table content
                self.model = SentenceTransformer(model_name, device=self.device)
                self.dimension = self.model.get_sentence_embedding_dimension()
                logger.info(f"Table embedder loaded successfully. Dimension: {self.dimension}")
            else:
                self.model = None
                self.dimension = 1024
                logger.warning("Transformers not available, using fallback implementation")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            self.model = None
            self.dimension = 1024
    
    def _table_to_text(
        self,
        table_data: Dict[str, Any],
        method: str = "structured"
    ) -> str:
        """
        Convert table data to text representation
        
        Args:
            table_data: Table data as dictionary
            method: Conversion method ('structured', 'flat', 'json')
        
        Returns:
            String representation of the table
        """
        try:
            if method == "json":
                return json.dumps(table_data, ensure_ascii=False)
            
            elif method == "flat":
                # Flatten the table structure
                texts = []
                if "headers" in table_data:
                    texts.append("Headers: " + ", ".join(table_data["headers"]))
                if "rows" in table_data:
                    for i, row in enumerate(table_data["rows"]):
                        texts.append(f"Row {i}: {', '.join(str(cell) for cell in row)}")
                return " | ".join(texts)
            
            elif method == "structured":
                # Structured representation with hierarchy
                parts = []
                
                if "headers" in table_data:
                    parts.append(f"Table headers: {', '.join(table_data['headers'])}")
                
                if "rows" in table_data:
                    parts.append(f"Number of rows: {len(table_data['rows'])}")
                    
                    # Add first few rows as context
                    sample_rows = table_data["rows"][:3]
                    for i, row in enumerate(sample_rows):
                        row_text = ", ".join(str(cell) for cell in row)
                        parts.append(f"Row {i+1}: {row_text}")
                
                if "title" in table_data:
                    parts.insert(0, f"Table title: {table_data['title']}")
                
                if "caption" in table_data:
                    parts.append(f"Caption: {table_data['caption']}")
                
                return " | ".join(parts)
            
            else:
                # Default to JSON
                return json.dumps(table_data, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error converting table to text: {str(e)}")
            # Fallback to JSON
            return json.dumps(table_data, ensure_ascii=False)
    
    async def embed(
        self,
        table_data: Dict[str, Any],
        model: Optional[str] = None,
        method: str = "structured"
    ) -> List[float]:
        """
        Generate embedding for table data
        
        Args:
            table_data: Table data as dictionary
            model: Optional model name
            method: Table to text conversion method
        
        Returns:
            List of floats representing the embedding vector
        """
        try:
            # Convert table to text
            table_text = self._table_to_text(table_data, method)
            
            if self.model is None:
                # Fallback: generate simple hash-based embedding
                return self._fallback_embedding(table_text)
            
            # Generate embedding using text model
            embedding = self.model.encode(
                table_text,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating table embedding: {str(e)}")
            raise
    
    async def embed_batch(
        self,
        tables_data: List[Dict[str, Any]],
        model: Optional[str] = None,
        batch_size: int = 32,
        method: str = "structured"
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple tables in batch
        
        Args:
            tables_data: List of table data dictionaries
            model: Optional model name
            batch_size: Batch size for processing
            method: Table to text conversion method
        
        Returns:
            List of embedding vectors
        """
        try:
            # Convert tables to text
            table_texts = [self._table_to_text(table, method) for table in tables_data]
            
            if self.model is None:
                # Fallback for each table
                return [self._fallback_embedding(text) for text in table_texts]
            
            # Generate embeddings in batch
            embeddings = self.model.encode(
                table_texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating batch table embeddings: {str(e)}")
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
            "transformers_available": TRANSFORMERS_AVAILABLE
        }