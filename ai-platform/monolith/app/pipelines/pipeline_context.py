"""
Pipeline Context for Shared State Between Stages

Modern document understanding requires sharing expensive computations
between pipeline stages (rendered images, layout analysis, etc.).

This context object prevents redundant work and enables efficient
stage-to-stage communication.
"""
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import logging

from app.models.document_models import Document, Page, Region, BoundingBox

logger = logging.getLogger(__name__)


@dataclass
class PipelineContext:
    """
    Shared context for document processing pipeline.
    
    This object is passed between stages to share:
    - Expensive computations (rendered images, layout analysis)
    - Intermediate results (regions, elements)
    - Configuration and options
    - Processing metadata
    
    Benefits:
    - Avoid redundant rendering/processing
    - Enable stage-to-stage communication
    - Support incremental processing
    - Facilitate debugging and tracing
    """
    
    # Document identification
    document_id: str
    file_path: str
    
    # Processing options
    options: Dict[str, Any] = field(default_factory=dict)
    
    # Document model (built incrementally)
    document: Optional[Document] = None
    
    # Page-level cache (expensive computations)
    rendered_images: Dict[int, str] = field(default_factory=dict)  # page_number -> image_path
    page_layouts: Dict[int, Dict[str, Any]] = field(default_factory=dict)  # page_number -> layout_data
    
    # Region cache (shared between stages)
    regions_by_page: Dict[int, List[Region]] = field(default_factory=dict)
    
    # OCR cache (region-aware)
    ocr_results_by_region: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # region_id -> ocr_result
    
    # Extraction cache (tables, formulas, figures)
    extraction_results_by_region: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # region_id -> extraction_result
    
    # Processing metadata
    stage_results: Dict[str, Any] = field(default_factory=dict)  # stage_name -> result
    stage_timings: Dict[str, float] = field(default_factory=dict)  # stage_name -> duration
    stages_completed: List[str] = field(default_factory=list)  # List of completed stage names
    errors: List[str] = field(default_factory=list)
    
    # Monitoring metrics
    cache_hits: Dict[str, int] = field(default_factory=dict)  # cache_type -> hit_count
    cache_misses: Dict[str, int] = field(default_factory=dict)  # cache_type -> miss_count
    region_counts: Dict[str, int] = field(default_factory=dict)  # region_type -> count
    extraction_counts: Dict[str, int] = field(default_factory=dict)  # extraction_type -> count
    
    # Timestamps
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize timestamps"""
        if self.started_at is None:
            self.started_at = datetime.now()
    
    def get_option(self, key: str, default: Any = None) -> Any:
        """Get processing option with fallback"""
        return self.options.get(key, default)
    
    def set_option(self, key: str, value: Any) -> None:
        """Set processing option"""
        self.options[key] = value
    
    def get_rendered_image(self, page_number: int) -> Optional[str]:
        """Get cached rendered image path for page"""
        result = self.rendered_images.get(page_number)
        if result is not None:
            self.cache_hits['rendered_images'] = self.cache_hits.get('rendered_images', 0) + 1
        else:
            self.cache_misses['rendered_images'] = self.cache_misses.get('rendered_images', 0) + 1
        return result
    
    def set_rendered_image(self, page_number: int, image_path: str) -> None:
        """Cache rendered image path for page"""
        self.rendered_images[page_number] = image_path
        logger.debug(f"Cached rendered image for page {page_number}: {image_path}")
    
    def get_page_layout(self, page_number: int) -> Optional[Dict[str, Any]]:
        """Get cached layout analysis for page"""
        result = self.page_layouts.get(page_number)
        if result is not None:
            self.cache_hits['page_layouts'] = self.cache_hits.get('page_layouts', 0) + 1
        else:
            self.cache_misses['page_layouts'] = self.cache_misses.get('page_layouts', 0) + 1
        return result
    
    def set_page_layout(self, page_number: int, layout_data: Dict[str, Any]) -> None:
        """Cache layout analysis for page"""
        self.page_layouts[page_number] = layout_data
        logger.debug(f"Cached layout analysis for page {page_number}")
    
    def get_regions_for_page(self, page_number: int) -> List[Region]:
        """Get all regions for a specific page"""
        return self.regions_by_page.get(page_number, [])
    
    def set_regions_for_page(self, page_number: int, regions: List[Region]) -> None:
        """Cache regions for a specific page"""
        self.regions_by_page[page_number] = regions
        # Track region counts for monitoring
        for region in regions:
            region_type = region.region_type.value
            self.region_counts[region_type] = self.region_counts.get(region_type, 0) + 1
        logger.debug(f"Cached {len(regions)} regions for page {page_number}")
    
    def add_region_to_page(self, page_number: int, region: Region) -> None:
        """Add a single region to page cache"""
        if page_number not in self.regions_by_page:
            self.regions_by_page[page_number] = []
        self.regions_by_page[page_number].append(region)
        # Track region count for monitoring
        region_type = region.region_type.value
        self.region_counts[region_type] = self.region_counts.get(region_type, 0) + 1
    
    def get_ocr_result(self, region_id: str) -> Optional[Dict[str, Any]]:
        """Get cached OCR result for a region"""
        return self.ocr_results_by_region.get(region_id)
    
    def set_ocr_result(self, region_id: str, ocr_result: Dict[str, Any]) -> None:
        """Cache OCR result for a region"""
        self.ocr_results_by_region[region_id] = ocr_result
        logger.debug(f"Cached OCR result for region {region_id}")
    
    def get_extraction_result(self, region_id: str) -> Optional[Dict[str, Any]]:
        """Get cached extraction result for a region"""
        return self.extraction_results_by_region.get(region_id)
    
    def set_extraction_result(self, region_id: str, extraction_result: Dict[str, Any]) -> None:
        """Cache extraction result for a region"""
        self.extraction_results_by_region[region_id] = extraction_result
        logger.debug(f"Cached extraction result for region {region_id}")
    
    def set_stage_result(self, stage_name: str, result: Any) -> None:
        """Store result from a pipeline stage"""
        self.stage_results[stage_name] = result
        logger.debug(f"Stored result for stage: {stage_name}")
    
    def get_stage_result(self, stage_name: str) -> Any:
        """Get result from a pipeline stage"""
        return self.stage_results.get(stage_name)
    
    def set_stage_timing(self, stage_name: str, duration: float) -> None:
        """Record timing for a pipeline stage"""
        self.stage_timings[stage_name] = duration
        logger.debug(f"Stage {stage_name} completed in {duration:.2f}s")
    
    def get_stage_timing(self, stage_name: str) -> Optional[float]:
        """Get timing for a pipeline stage"""
        return self.stage_timings.get(stage_name)
    
    def add_error(self, error: str) -> None:
        """Add an error to the context"""
        self.errors.append(error)
        logger.error(f"Pipeline error: {error}")
    
    def get_total_processing_time(self) -> float:
        """Get total processing time"""
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        elif self.started_at:
            return (datetime.now() - self.started_at).total_seconds()
        return 0.0
    
    def get_stage_timings_summary(self) -> Dict[str, float]:
        """Get summary of all stage timings"""
        return self.stage_timings.copy()
    
    def mark_completed(self) -> None:
        """Mark pipeline as completed"""
        self.completed_at = datetime.now()
        logger.info(f"Pipeline completed in {self.get_total_processing_time():.2f}s")
    
    def has_errors(self) -> bool:
        """Check if pipeline has errors"""
        return len(self.errors) > 0
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring"""
        return {
            "rendered_images_cached": len(self.rendered_images),
            "page_layouts_cached": len(self.page_layouts),
            "total_regions_cached": sum(len(regions) for regions in self.regions_by_page.values()),
            "ocr_results_cached": len(self.ocr_results_by_region),
            "extraction_results_cached": len(self.extraction_results_by_region),
            "stage_results_stored": len(self.stage_results),
            "total_processing_time": self.get_total_processing_time(),
            # Monitoring metrics
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rates": {
                cache_type: self._calculate_hit_rate(cache_type)
                for cache_type in set(list(self.cache_hits.keys()) + list(self.cache_misses.keys()))
            },
            "region_counts": self.region_counts,
            "extraction_counts": self.extraction_counts,
            "total_regions_processed": sum(self.region_counts.values()),
            "total_extractions": sum(self.extraction_counts.values())
        }
    
    def _calculate_hit_rate(self, cache_type: str) -> float:
        """Calculate cache hit rate for a specific cache type"""
        hits = self.cache_hits.get(cache_type, 0)
        misses = self.cache_misses.get(cache_type, 0)
        total = hits + misses
        if total == 0:
            return 0.0
        return hits / total
    
    def invalidate_page_cache(self, page_number: int) -> None:
        """Invalidate cache for a specific page"""
        if page_number in self.rendered_images:
            del self.rendered_images[page_number]
        if page_number in self.page_layouts:
            del self.page_layouts[page_number]
        if page_number in self.regions_by_page:
            del self.regions_by_page[page_number]
        logger.debug(f"Invalidated cache for page {page_number}")
    
    def invalidate_all_cache(self) -> None:
        """Invalidate all cached data"""
        self.rendered_images.clear()
        self.page_layouts.clear()
        self.regions_by_page.clear()
        self.ocr_results_by_region.clear()
        self.extraction_results_by_region.clear()
        logger.debug("Invalidated all cache")
    
    def ensure_document(self) -> Document:
        """Ensure document object exists, create if needed"""
        if self.document is None:
            self.document = Document(
                document_id=self.document_id,
                file_path=self.file_path
            )
        return self.document
    
    def get_or_create_page(self, page_number: int, width: float, height: float) -> Page:
        """Get existing page or create new one"""
        document = self.ensure_document()
        page = document.get_page(page_number)
        
        if page is None:
            page = Page(
                page_number=page_number,
                width=width,
                height=height
            )
            document.add_page(page)
        
        return page
    
    def merge_regions_to_document(self) -> None:
        """Merge cached regions into document model"""
        if self.document is None:
            logger.warning("Cannot merge regions: document not initialized")
            return
        
        for page_number, regions in self.regions_by_page.items():
            page = self.document.get_page(page_number)
            if page is None:
                logger.warning(f"Page {page_number} not found in document, skipping region merge")
                continue
            
            # Add regions to page
            for region in regions:
                if not page.get_region_by_id(region.region_id):
                    page.add_region(region)
        
        logger.info(f"Merged {sum(len(regions) for regions in self.regions_by_page.values())} regions into document")
