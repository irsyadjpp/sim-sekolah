"""
Image Processor untuk Parser Service
Post-processing untuk extracted images dengan compression, resize, dan MinIO storage
Optimizes images untuk storage dan educational content delivery
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import io
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import PIL, fall back gracefully if not available
try:
    from PIL import Image, ImageOps, ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("PIL not available, image processing will be limited")


class ImageFormat(Enum):
    """Output format untuk images"""
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"
    GIF = "gif"
    ORIGINAL = "original"


class ImageQuality(Enum):
    """Quality level untuk image compression"""
    HIGH = "high"          # High quality, larger file size
    MEDIUM = "medium"      # Balance quality dan size
    LOW = "low"            # Lower quality, smaller file size
    THUMBNAIL = "thumbnail"  # Very small untuk thumbnails


class ResizeStrategy(Enum):
    """Resize strategy untuk images"""
    NONE = "none"                      # No resizing
    MAINTAIN_ASPECT = "maintain_aspect"  # Maintain aspect ratio
    FIXED_DIMENSIONS = "fixed_dimensions"  # Fixed width/height
    FIT_TO_CONTAINER = "fit_to_container"  # Fit within bounds
    COVER = "cover"                      # Cover area completely


@dataclass
class ImageProcessingOptions:
    """Options untuk image processing"""
    output_format: ImageFormat = ImageFormat.JPEG
    
    # Resize options
    resize_strategy: ResizeStrategy = ResizeStrategy.MAINTAIN_ASPECT
    max_width: int = 1920              # Maximum width in pixels
    max_height: int = 1080             # Maximum height in pixels
    target_width: Optional[int] = None  # Target width (fixed dimensions)
    target_height: Optional[int] = None # Target height (fixed dimensions)
    
    # Quality options
    quality: ImageQuality = ImageQuality.MEDIUM
    compression_level: int = 85        # JPEG compression (1-100)
    
    # Enhancement options
    enhance_contrast: bool = False
    enhance_brightness: bool = False
    enhance_sharpness: bool = False
    remove_alpha: bool = True         # Remove transparency for JPEG
    
    # Storage options
    generate_thumbnails: bool = True
    thumbnail_size: Tuple[int, int] = (150, 150)
    generate_multiple_sizes: bool = False  # Generate multiple resolution versions
    
    # Metadata options
    preserve_metadata: bool = False
    add_watermark: bool = False
    watermark_text: str = ""
    
    # MinIO options
    upload_to_minio: bool = True
    minio_bucket: str = "knowledge-assets"
    minio_prefix: str = "images/"


@dataclass
class ProcessedImage:
    """Hasil processing untuk image"""
    image_id: str
    original_data: bytes
    processed_data: bytes
    output_format: ImageFormat
    
    # Dimensions
    original_width: int = 0
    original_height: int = 0
    processed_width: int = 0
    processed_height: int = 0
    
    # File size
    original_size: int = 0
    processed_size: int = 0
    compression_ratio: float = 0.0
    
    # Storage info
    minio_key: str = ""
    thumbnail_key: str = ""
    additional_sizes: Dict[str, str] = field(default_factory=dict)
    
    # Processing metadata
    is_resized: bool = False
    is_compressed: bool = False
    is_enhanced: bool = False
    
    # Quality metrics
    quality_score: float = 0.0
    processing_time: float = 0.0
    processing_errors: List[str] = field(default_factory=list)


class ImageProcessor:
    """
    Processor untuk extracted images
    
    Functionality:
    - Image compression dan optimization
    - Resizing dan aspect ratio maintenance
    - Format conversion (PNG, JPEG, WebP, etc.)
    - Thumbnail generation
    - Image enhancement
    - MinIO storage integration
    - Quality assessment
    """
    
    def __init__(self, default_quality: ImageQuality = ImageQuality.MEDIUM):
        """
        Initialize Image Processor
        
        Args:
            default_quality: Default quality level untuk processing
        """
        self.default_quality = default_quality
        
        if not PIL_AVAILABLE:
            logger.warning("ImageProcessor initialized without PIL - limited functionality")
        else:
            logger.info("ImageProcessor initialized with full image processing capabilities")
    
    def process_image(
        self,
        image_data: bytes,
        image_id: str,
        options: Optional[ImageProcessingOptions] = None
    ) -> ProcessedImage:
        """
        Process extracted image dengan compression dan optimization
        
        Args:
            image_data: Raw image bytes
            image_id: Unique identifier untuk image
            options: Processing options
        
        Returns:
            ProcessedImage dengan optimized content
        """
        if options is None:
            options = ImageProcessingOptions()
        
        import time
        start_time = time.time()
        
        try:
            # Check PIL availability
            if not PIL_AVAILABLE:
                return self._process_without_pil(image_data, image_id, options)
            
            # Load image
            img = Image.open(io.BytesIO(image_data))
            
            # Get original dimensions
            original_width, original_height = img.size
            original_size = len(image_data)
            
            # Apply enhancements if requested
            if options.enhance_contrast:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.2)
            
            if options.enhance_brightness:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.1)
            
            if options.enhance_sharpness:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.1)
            
            # Resize image
            processed_width, processed_height = original_width, original_height
            is_resized = False
            
            if options.resize_strategy != ResizeStrategy.NONE:
                img = self._resize_image(img, options)
                processed_width, processed_height = img.size
                is_resized = True
            
            # Convert format if needed
            output_format = options.output_format
            if output_format == ImageFormat.ORIGINAL:
                output_format = self._get_original_format(img)
            
            # Remove alpha channel untuk JPEG
            if output_format == ImageFormat.JPEG and img.mode in ('RGBA', 'LA', 'P'):
                if options.remove_alpha:
                    img = img.convert('RGB')
            
            # Compress image
            compression_level = self._get_compression_level(options.quality)
            img_byte_arr = io.BytesIO()
            
            if output_format == ImageFormat.JPEG:
                img.save(img_byte_arr, format='JPEG', quality=compression_level, optimize=True)
            elif output_format == ImageFormat.PNG:
                img.save(img_byte_arr, format='PNG', optimize=True)
            elif output_format == ImageFormat.WEBP:
                img.save(img_byte_arr, format='WEBP', quality=compression_level, method=6)
            else:
                img.save(img_byte_arr, format='PNG', optimize=True)
            
            processed_data = img_byte_arr.getvalue()
            processed_size = len(processed_data)
            
            # Calculate compression ratio
            compression_ratio = (original_size - processed_size) / original_size if original_size > 0 else 0
            
            # Generate thumbnail if requested
            thumbnail_key = ""
            if options.generate_thumbnails:
                thumbnail_data = self._generate_thumbnail(img, options.thumbnail_size)
                thumbnail_key = self._get_thumbnail_key(image_id, options)
                # In production, upload thumbnail ke MinIO here
            
            # Generate additional sizes if requested
            additional_sizes = {}
            if options.generate_multiple_sizes:
                additional_sizes = self._generate_multiple_sizes(img, image_id, options)
            
            # Upload ke MinIO if requested
            minio_key = ""
            if options.upload_to_minio:
                minio_key = self._upload_to_minio(processed_data, image_id, options)
            
            result = ProcessedImage(
                image_id=image_id,
                original_data=image_data,
                processed_data=processed_data,
                output_format=output_format,
                original_width=original_width,
                original_height=original_height,
                processed_width=processed_width,
                processed_height=processed_height,
                original_size=original_size,
                processed_size=processed_size,
                compression_ratio=compression_ratio,
                minio_key=minio_key,
                thumbnail_key=thumbnail_key,
                additional_sizes=additional_sizes,
                is_resized=is_resized,
                is_compressed=compression_ratio > 0,
                is_enhanced=options.enhance_contrast or options.enhance_brightness or options.enhance_sharpness,
                processing_time=time.time() - start_time
            )
            
            logger.info(
                f"Processed image {image_id}: {original_width}x{original_height} → "
                f"{processed_width}x{processed_height}, "
                f"size: {original_size} → {processed_size} bytes "
                f"({compression_ratio:.1%} reduction)"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing image {image_id}: {e}")
            return ProcessedImage(
                image_id=image_id,
                original_data=image_data,
                processed_data=image_data,  # Return original if processing fails
                output_format=ImageFormat.ORIGINAL,
                processing_time=time.time() - start_time,
                processing_errors=[str(e)]
            )
    
    def _process_without_pil(
        self,
        image_data: bytes,
        image_id: str,
        options: ImageProcessingOptions
    ) -> ProcessedImage:
        """Process image tanpa PIL (limited functionality)"""
        return ProcessedImage(
            image_id=image_id,
            original_data=image_data,
            processed_data=image_data,
            output_format=ImageFormat.ORIGINAL,
            original_size=len(image_data),
            processed_size=len(image_data),
            processing_errors=["PIL not available for advanced processing"]
        )
    
    def _resize_image(self, img: Image.Image, options: ImageProcessingOptions) -> Image.Image:
        """Resize image sesuai strategy"""
        original_width, original_height = img.size
        
        if options.resize_strategy == ResizeStrategy.MAINTAIN_ASPECT:
            # Resize maintaining aspect ratio within bounds
            ratio = min(options.max_width / original_width, options.max_height / original_height)
            if ratio < 1:  # Only resize if image is larger than bounds
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
                return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        elif options.resize_strategy == ResizeStrategy.FIXED_DIMENSIONS:
            # Fixed dimensions (may distort aspect ratio)
            target_width = options.target_width or options.max_width
            target_height = options.target_height or options.max_height
            return img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        elif options.resize_strategy == ResizeStrategy.FIT_TO_CONTAINER:
            # Fit within bounds without maintaining aspect ratio
            target_width = min(original_width, options.max_width)
            target_height = min(original_height, options.max_height)
            if target_width != original_width or target_height != original_height:
                return img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        elif options.resize_strategy == ResizeStrategy.COVER:
            # Cover area completely (crop jika necessary)
            ratio_w = options.max_width / original_width
            ratio_h = options.max_height / original_height
            ratio = max(ratio_w, ratio_h)
            
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Crop ke exact dimensions
            left = (new_width - options.max_width) // 2
            top = (new_height - options.max_height) // 2
            right = left + options.max_width
            bottom = top + options.max_height
            
            return img_resized.crop((left, top, right, bottom))
        
        return img
    
    def _generate_thumbnail(self, img: Image.Image, size: Tuple[int, int]) -> bytes:
        """Generate thumbnail dari image"""
        thumbnail = img.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        
        thumb_byte_arr = io.BytesIO()
        thumbnail.save(thumb_byte_arr, format='JPEG', quality=80, optimize=True)
        return thumb_byte_arr.getvalue()
    
    def _generate_multiple_sizes(
        self,
        img: Image.Image,
        image_id: str,
        options: ImageProcessingOptions
    ) -> Dict[str, str]:
        """Generate multiple resolution versions"""
        sizes = {
            'small': (640, 480),
            'medium': (1024, 768),
            'large': (1920, 1080)
        }
        
        result = {}
        for size_name, size in sizes.items():
            resized = img.copy()
            resized.thumbnail(size, Image.Resampling.LANCZOS)
            
            byte_arr = io.BytesIO()
            resized.save(byte_arr, format='JPEG', quality=85, optimize=True)
            
            # In production, upload each size ke MinIO
            result[size_name] = f"{options.minio_prefix}{image_id}/{size_name}.jpg"
        
        return result
    
    def _upload_to_minio(
        self,
        image_data: bytes,
        image_id: str,
        options: ImageProcessingOptions
    ) -> str:
        """Upload processed image ke MinIO"""
        try:
            from app.config.minio_config import get_minio_client
            
            minio_client = get_minio_client()
            
            # Generate MinIO key
            extension = options.output_format.value
            minio_key = f"{options.minio_prefix}{image_id}.{extension}"
            
            # Upload to MinIO
            minio_client.upload_image(image_data, minio_key)
            
            return minio_key
            
        except Exception as e:
            logger.error(f"Error uploading to MinIO: {e}")
            return ""
    
    def _get_thumbnail_key(self, image_id: str, options: ImageProcessingOptions) -> str:
        """Generate MinIO key untuk thumbnail"""
        return f"{options.minio_prefix}{image_id}/thumbnail.jpg"
    
    def _get_original_format(self, img: Image.Image) -> ImageFormat:
        """Determine original image format"""
        if img.format == 'PNG':
            return ImageFormat.PNG
        elif img.format == 'JPEG':
            return ImageFormat.JPEG
        elif img.format == 'WEBP':
            return ImageFormat.WEBP
        elif img.format == 'GIF':
            return ImageFormat.GIF
        else:
            return ImageFormat.ORIGINAL
    
    def _get_compression_level(self, quality: ImageQuality) -> int:
        """Get compression level based on quality setting"""
        quality_levels = {
            ImageQuality.HIGH: 95,
            ImageQuality.MEDIUM: 85,
            ImageQuality.LOW: 70,
            ImageQuality.THUMBNAIL: 60
        }
        return quality_levels.get(quality, 85)
    
    def batch_process_images(
        self,
        images_data: List[Dict[str, Any]],
        options: Optional[ImageProcessingOptions] = None
    ) -> List[ProcessedImage]:
        """
        Process multiple images secara batch
        
        Args:
            images_data: List of image data dictionaries
            options: Processing options (applied ke semua images)
        
        Returns:
            List of ProcessedImage objects
        """
        results = []
        
        for idx, image_info in enumerate(images_data):
            image_id = image_info.get('image_id', f'image_{idx}')
            image_data = image_info.get('image_data', b'')
            
            try:
                if image_data:
                    processed_image = self.process_image(image_data, image_id, options)
                    results.append(processed_image)
                else:
                    logger.warning(f"Skipping image {image_id}: no data")
            except Exception as e:
                logger.error(f"Error processing image {image_id}: {e}")
                continue
        
        logger.info(f"Batch processed {len(results)}/{len(images_data)} images")
        return results
    
    def validate_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        Validate image integrity dan quality
        
        Args:
            image_data: Image bytes untuk validate
        
        Returns:
            Dictionary dengan validation results
        """
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'format': 'unknown',
            'dimensions': (0, 0),
            'size': len(image_data),
            'quality_score': 0.0
        }
        
        if not PIL_AVAILABLE:
            result['warnings'].append("PIL not available for detailed validation")
            return result
        
        try:
            img = Image.open(io.BytesIO(image_data))
            result['format'] = img.format
            result['dimensions'] = img.size
            
            # Check jika image is too small
            width, height = img.size
            if width < 50 or height < 50:
                result['warnings'].append("Image dimensions very small")
                result['quality_score'] -= 0.3
            
            # Check jika image is too large
            if len(image_data) > 10 * 1024 * 1024:  # 10MB
                result['warnings'].append("Image file size very large")
                result['quality_score'] -= 0.2
            
            # Check untuk potential corruption
            try:
                img.verify()
            except Exception as e:
                result['is_valid'] = False
                result['errors'].append(f"Image corruption detected: {e}")
            
            # Overall quality score
            result['quality_score'] = max(0.0, result['quality_score'] + 0.8)
            
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Image validation failed: {e}")
        
        return result