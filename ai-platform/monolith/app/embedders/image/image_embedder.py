"""
Image embedder using CLIP and other vision models
Supports image embeddings for educational content
"""
import torch
import base64
from typing import List, Optional
from PIL import Image
import io
import logging

try:
    from sentence_transformers import SentenceTransformer
    CLIP_AVAILABLE = True
except ImportError:
    CLIP_AVAILABLE = False
    logging.warning("sentence-transformers not available for CLIP")

logger = logging.getLogger(__name__)


class ImageEmbedder:
    """Image embedder for generating embeddings from images"""
    
    def __init__(
        self,
        model_name: str = "clip-ViT-B-32",
        device: str = "cuda"
    ):
        """
        Initialize image embedder
        
        Args:
            model_name: Model name (default: clip-ViT-B-32)
            device: Device to use (cuda/cpu)
        """
        self.model_name = model_name
        self.device = device if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Loading image embedding model: {model_name}")
        logger.info(f"Using device: {self.device}")
        
        try:
            if CLIP_AVAILABLE:
                # Load CLIP model from sentence-transformers
                self.model = SentenceTransformer(model_name, device=self.device)
                self.dimension = self.model.get_sentence_embedding_dimension()
                logger.info(f"CLIP model loaded successfully. Dimension: {self.dimension}")
            else:
                # Fallback to basic implementation
                self.model = None
                self.dimension = 512  # Default CLIP dimension
                logger.warning("CLIP not available, using fallback implementation")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            self.model = None
            self.dimension = 512
            raise
    
    def _decode_image(self, image_data: str) -> Image.Image:
        """
        Decode image from base64 or URL
        
        Args:
            image_data: Base64 encoded image or URL
        
        Returns:
            PIL Image object
        """
        try:
            # Check if it's a base64 encoded image
            if image_data.startswith("data:image"):
                # Remove data URL prefix
                image_data = image_data.split(",")[1]
            
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            return image
            
        except Exception as e:
            logger.error(f"Error decoding image: {str(e)}")
            raise
    
    async def embed(
        self,
        image_data: str,
        model: Optional[str] = None
    ) -> List[float]:
        """
        Generate embedding for a single image
        
        Args:
            image_data: Base64 encoded image data or URL
            model: Optional model name
        
        Returns:
            List of floats representing the embedding vector
        """
        try:
            # Decode image
            image = self._decode_image(image_data)
            
            if self.model is None:
                # Fallback: generate simple hash-based embedding
                return self._fallback_embedding(image)
            
            # Generate embedding
            embedding = self.model.encode(
                image,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            
            return embedding.tolist()
            
        except Exception as e:
            logger.error(f"Error generating image embedding: {str(e)}")
            raise
    
    async def embed_batch(
        self,
        images_data: List[str],
        model: Optional[str] = None,
        batch_size: int = 32
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple images in batch
        
        Args:
            images_data: List of base64 encoded images or URLs
            model: Optional model name
            batch_size: Batch size for processing
        
        Returns:
            List of embedding vectors
        """
        try:
            # Decode images
            images = [self._decode_image(img_data) for img_data in images_data]
            
            if self.model is None:
                # Fallback for each image
                return [self._fallback_embedding(img) for img in images]
            
            # Generate embeddings in batch
            embeddings = self.model.encode(
                images,
                batch_size=batch_size,
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            
            return embeddings.tolist()
            
        except Exception as e:
            logger.error(f"Error generating batch image embeddings: {str(e)}")
            raise
    
    def _fallback_embedding(self, image: Image.Image) -> List[float]:
        """
        Generate fallback embedding when CLIP is not available
        
        Args:
            image: PIL Image object
        
        Returns:
            List of floats representing a simple embedding
        """
        # Resize to fixed size
        image = image.resize((32, 32))
        
        # Convert to numpy array and normalize
        import numpy as np
        img_array = np.array(image, dtype=np.float32) / 255.0
        
        # Flatten and pad/truncate to 512 dimensions
        flattened = img_array.flatten()
        
        if len(flattened) < 512:
            # Pad with zeros
            padded = np.pad(flattened, (0, 512 - len(flattened)))
        else:
            # Truncate
            padded = flattened[:512]
        
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
            "clip_available": CLIP_AVAILABLE
        }