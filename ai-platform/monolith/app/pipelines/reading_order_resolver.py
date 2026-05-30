"""
Reading Order Resolver for Document Understanding

PDF documents often have object order ≠ reading order.
This component reconstructs the correct reading order for regions.

Critical for:
- RAG applications (prevents garbled text)
- Text extraction accuracy
- Content understanding
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from app.models.document_models import Region, RegionType, BoundingBox, Page

logger = logging.getLogger(__name__)


class ReadingOrderResolver:
    """
    Reconstruct correct reading order for document regions.
    
    PDF reading order is complex due to:
    - Multi-column layouts
    - Sidebars and callouts
    - Tables and figures interrupting text flow
    - Different writing directions
    
    This resolver uses multiple heuristics to determine correct order.
    """
    
    def __init__(self, detect_columns: bool = True):
        """
        Initialize reading order resolver.
        
        Args:
            detect_columns: Whether to detect multi-column layouts
        """
        self.detect_columns = detect_columns
        logger.info("ReadingOrderResolver initialized")
    
    def resolve_reading_order(
        self, 
        page: Page,
        regions: List[Region]
    ) -> List[Region]:
        """
        Resolve reading order for regions on a page.
        
        Args:
            page: Page object with dimensions
            regions: List of regions to order
            
        Returns:
            Regions with updated reading_order field
        """
        try:
            if not regions:
                return regions
            
            # Separate structural regions (header/footer) from content
            structural_regions = [r for r in regions if r.region_type in 
                                 [RegionType.HEADER, RegionType.FOOTER, RegionType.PAGE_NUMBER]]
            content_regions = [r for r in regions if r not in structural_regions]
            
            # Order structural regions (header first, footer last)
            for i, region in enumerate(structural_regions):
                if region.region_type == RegionType.HEADER:
                    region.reading_order = 0
                elif region.region_type == RegionType.FOOTER:
                    region.reading_order = len(regions) - 1
                else:
                    region.reading_order = i
            
            # Detect columns if enabled
            if self.detect_columns:
                columns = self._detect_columns(content_regions, page.width)
                if len(columns) > 1:
                    # Multi-column layout
                    ordered_content = self._order_multi_column(content_regions, columns)
                else:
                    # Single column layout
                    ordered_content = self._order_single_column(content_regions)
            else:
                # Simple top-to-bottom ordering
                ordered_content = self._order_single_column(content_regions)
            
            # Assign reading order to content regions
            base_order = 1  # Start after header
            for i, region in enumerate(ordered_content):
                region.reading_order = base_order + i
            
            # Merge structural and content regions
            all_regions = structural_regions + ordered_content
            
            # Sort by reading order
            all_regions.sort(key=lambda r: r.reading_order)
            
            page.reading_order_resolved = True
            
            logger.info(f"Resolved reading order for {len(all_regions)} regions on page {page.page_number}")
            
            return all_regions
            
        except Exception as e:
            logger.error(f"Error resolving reading order: {e}")
            # Fallback to simple Y-ordering
            return self._order_single_column(regions)
    
    def _detect_columns(self, regions: List[Region], page_width: float) -> List[Dict[str, Any]]:
        """
        Detect column layout from region positions using advanced clustering.
        
        Returns list of column definitions with x ranges.
        """
        if not regions:
            return []
        
        # Get X positions and widths of all regions
        region_data = []
        for r in regions:
            center_x = (r.bbox.x1 + r.bbox.x2) / 2
            width = r.bbox.x2 - r.bbox.x1
            region_data.append({
                "region": r,
                "center_x": center_x,
                "width": width,
                "x1": r.bbox.x1,
                "x2": r.bbox.x2
            })
        
        # Sort by center X position
        region_data.sort(key=lambda d: d["center_x"])
        
        # Advanced column detection using DBSCAN-like clustering
        columns = []
        column_threshold = page_width * 0.15  # 15% of page width as threshold
        
        for data in region_data:
            assigned = False
            for col in columns:
                # Check if region belongs to this column
                # Region belongs if its center is within column range or overlaps significantly
                col_center = (col["x_start"] + col["x_end"]) / 2
                if abs(data["center_x"] - col_center) < column_threshold:
                    col["x_start"] = min(col["x_start"], data["x1"])
                    col["x_end"] = max(col["x_end"], data["x2"])
                    col["regions"].append(data["region"])
                    assigned = True
                    break
            
            if not assigned:
                # Create new column
                columns.append({
                    "x_start": data["x1"],
                    "x_end": data["x2"],
                    "regions": [data["region"]]
                })
        
        # Merge overlapping columns
        merged_columns = []
        for col in sorted(columns, key=lambda c: c["x_start"]):
            if not merged_columns:
                merged_columns.append(col)
            else:
                last_col = merged_columns[-1]
                # Check if columns overlap
                if col["x_start"] < last_col["x_end"]:
                    # Merge columns
                    last_col["x_start"] = min(last_col["x_start"], col["x_start"])
                    last_col["x_end"] = max(last_col["x_end"], col["x_end"])
                    last_col["regions"].extend(col["regions"])
                else:
                    merged_columns.append(col)
        
        # Filter out empty columns
        columns = [col for col in merged_columns if col["regions"]]
        
        logger.debug(f"Detected {len(columns)} columns using advanced clustering")
        
        return columns
    
    def _order_single_column(self, regions: List[Region]) -> List[Region]:
        """
        Order regions for single-column layout (top-to-bottom, left-to-right).
        """
        # Primary sort by Y position (top to bottom)
        # Secondary sort by X position (left to right for same Y)
        ordered = sorted(regions, key=lambda r: (r.bbox.y1, r.bbox.x1))
        
        return ordered
    
    def _order_multi_column(
        self, 
        regions: List[Region], 
        columns: List[Dict[str, Any]]
    ) -> List[Region]:
        """
        Order regions for multi-column layout with advanced heuristics.
        
        Strategy: Detect zig-zag vs column-by-column reading patterns.
        """
        ordered = []
        
        # Sort columns by X position (left to right)
        columns_sorted = sorted(columns, key=lambda c: c["x_start"])
        
        # Detect reading pattern: zig-zag vs column-by-column
        reading_pattern = self._detect_reading_pattern(regions, columns_sorted)
        
        if reading_pattern == "zigzag":
            # Zig-zag pattern: read across columns row by row
            ordered = self._order_zigzag(columns_sorted)
        else:
            # Column-by-column pattern: read entire column before moving to next
            for col in columns_sorted:
                column_regions = sorted(col["regions"], key=lambda r: r.bbox.y1)
                ordered.extend(column_regions)
        
        return ordered
    
    def _detect_reading_pattern(
        self, 
        regions: List[Region], 
        columns: List[Dict[str, Any]]
    ) -> str:
        """
        Detect whether document uses zig-zag or column-by-column reading pattern.
        
        Zig-zag: Read row 1 (col1, col2, col3), then row 2 (col1, col2, col3)
        Column-by-column: Read col1 completely, then col2, then col3
        """
        if len(columns) < 2:
            return "column"
        
        # Get Y positions of regions in each column
        column_y_positions = []
        for col in columns:
            y_positions = sorted([r.bbox.y1 for r in col["regions"]])
            column_y_positions.append(y_positions)
        
        # Calculate correlation between Y positions of adjacent columns
        # High correlation suggests zig-zag pattern
        correlations = []
        for i in range(len(column_y_positions) - 1):
            y1 = column_y_positions[i]
            y2 = column_y_positions[i + 1]
            
            # Calculate correlation using simple overlap measure
            overlap = 0
            for y in y1:
                for y2_val in y2:
                    if abs(y - y2_val) < 50:  # Within 50 pixels
                        overlap += 1
            
            correlation = overlap / max(len(y1), len(y2), 1)
            correlations.append(correlation)
        
        # If average correlation is high, use zig-zag
        avg_correlation = sum(correlations) / len(correlations) if correlations else 0
        
        if avg_correlation > 0.5:
            logger.debug("Detected zig-zag reading pattern")
            return "zigzag"
        else:
            logger.debug("Detected column-by-column reading pattern")
            return "column"
    
    def _order_zigzag(self, columns: List[Dict[str, Any]]) -> List[Region]:
        """
        Order regions using zig-zag pattern (row by row across columns).
        """
        # Sort columns by X position
        columns_sorted = sorted(columns, key=lambda c: c["x_start"])
        
        # Group regions by approximate Y position (rows)
        all_regions = []
        for col in columns_sorted:
            for region in col["regions"]:
                all_regions.append(region)
        
        # Sort all regions by Y position
        all_regions_sorted = sorted(all_regions, key=lambda r: r.bbox.y1)
        
        # Group into rows based on Y proximity
        rows = []
        current_row = [all_regions_sorted[0]]
        row_threshold = 50  # pixels
        
        for region in all_regions_sorted[1:]:
            if abs(region.bbox.y1 - current_row[0].bbox.y1) < row_threshold:
                current_row.append(region)
            else:
                # Sort current row by X position (left to right)
                current_row.sort(key=lambda r: r.bbox.x1)
                rows.append(current_row)
                current_row = [region]
        
        # Add last row
        if current_row:
            current_row.sort(key=lambda r: r.bbox.x1)
            rows.append(current_row)
        
        # Flatten rows
        ordered = []
        for row in rows:
            ordered.extend(row)
        
        return ordered
    
    def resolve_document_reading_order(
        self, 
        pages: List[Page]
    ) -> List[Page]:
        """
        Resolve reading order for entire document with cross-page continuity.
        
        Args:
            pages: List of pages to process
            
        Returns:
            Pages with resolved reading order
        """
        # First, resolve reading order within each page
        for page in pages:
            regions = page.regions
            if regions:
                ordered_regions = self.resolve_reading_order(page, regions)
                page.regions = ordered_regions
        
        # Then, resolve cross-page reading order for text continuity
        if len(pages) > 1:
            pages = self._resolve_cross_page_reading_order(pages)
        
        logger.info(f"Resolved reading order for {len(pages)} pages with cross-page continuity")
        
        return pages
    
    def _resolve_cross_page_reading_order(self, pages: List[Page]) -> List[Page]:
        """
        Resolve reading order across pages for text continuity.
        
        Detects when text continues from one page to the next and adjusts
        reading order to maintain flow.
        """
        for i in range(len(pages) - 1):
            current_page = pages[i]
            next_page = pages[i + 1]
            
            # Get last text region from current page
            current_text_regions = [r for r in current_page.regions 
                                   if r.region_type in [RegionType.PARAGRAPH, RegionType.HEADING]]
            next_text_regions = [r for r in next_page.regions 
                               if r.region_type in [RegionType.PARAGRAPH, RegionType.HEADING]]
            
            if not current_text_regions or not next_text_regions:
                continue
            
            # Check if last region on current page is incomplete
            last_region = current_text_regions[-1]
            last_text = last_region.get_text().strip()
            
            # Check for incomplete sentences (no ending punctuation)
            if last_text and not last_text[-1] in ['.', '!', '?', ':', ';']:
                # Text likely continues to next page
                # Mark this region for cross-page continuity
                last_region.metadata = last_region.metadata or {}
                last_region.metadata["cross_page_continuation"] = True
                last_region.metadata["continues_to_page"] = next_page.page_number
                
                # Mark first region on next page as continuation
                first_region = next_text_regions[0]
                first_region.metadata = first_region.metadata or {}
                first_region.metadata["cross_page_continuation"] = True
                first_region.metadata["continues_from_page"] = current_page.page_number
                
                logger.debug(f"Detected cross-page text continuation from page {current_page.page_number} to {next_page.page_number}")
        
        return pages
