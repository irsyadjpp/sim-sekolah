import fitz  # PyMuPDF
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging

from app.models.document_models import BoundingBox, Region

logger = logging.getLogger(__name__)


class TableExtractor:
    """
    Extract tables from documents using PyMuPDF.
    
    NEW: Region-aware extraction for modern pipeline.
    """
    
    def __init__(self):
        """Initialize table extractor"""
        self.supported_formats = ['.pdf']
    
    def extract_from_region(
        self, 
        region: Region, 
        page: fitz.Page,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract table content from a specific region (region-aware).
        
        This is the NEW method for the modern pipeline.
        
        Args:
            region: Region object with bounding box
            page: PyMuPDF page object
            options: Extraction options
            
        Returns:
            Table data for this specific region
        """
        try:
            options = options or {}
            
            # Get bounding box from region
            bbox = region.bbox.to_list()
            
            # Find tables within the region's bounding box
            clip_rect = fitz.Rect(*bbox)
            tables_found = page.find_tables(clip=clip_rect)
            
            if not tables_found.tables:
                logger.debug(f"No tables found in region {region.region_id}")
                return None
            
            # Extract the first table in this region
            table = tables_found.tables[0]
            
            # Extract table data using the extract() method
            table_data = {
                "region_id": region.region_id,
                "page_number": region.page_number,
                "bbox": BoundingBox.from_list(list(table.bbox)).to_list(),
                "confidence": 0.9
            }
            
            # Try to extract table content using extract() method
            try:
                table_content = table.extract()
                if table_content:
                    # The extract() method returns a list of lists (rows)
                    # First row is typically the header
                    if len(table_content) > 0:
                        table_data["headers"] = table_content[0]
                        table_data["rows"] = table_content[1:] if len(table_content) > 1 else []
                        table_data["row_count"] = len(table_content) - 1
                        table_data["col_count"] = len(table_content[0]) if table_content[0] else 0
                        
                        logger.info(f"Extracted table from region {region.region_id}: {table_data['row_count']} rows x {table_data['col_count']} cols")
                    else:
                        table_data["headers"] = []
                        table_data["rows"] = []
                        table_data["row_count"] = 0
                        table_data["col_count"] = 0
            except Exception as e:
                logger.warning(f"Could not extract table content using extract() method: {e}")
                # Fallback: use basic table info
                table_data["headers"] = []
                table_data["rows"] = []
                table_data["row_count"] = 0
                table_data["col_count"] = 0
            
            return table_data
            
        except Exception as e:
            logger.error(f"Error extracting table from region {region.region_id}: {e}")
            return None
    
    def extract(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Extract tables from document
        
        Args:
            file_path: Path to document file
            options: Extraction options
            
        Returns:
            List of extracted tables
        """
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension != '.pdf':
                logger.warning(f"Table extraction optimized for PDF, got {file_extension}")
                return []
            
            options = options or {}
            flavor = options.get('table_flavor', 'lattice')
            
            return self._extract_from_pdf(file_path, flavor)
                
        except Exception as e:
            logger.error(f"Error extracting tables from {file_path}: {str(e)}")
            return []
    
    def _extract_from_pdf(self, file_path: str, flavor: str = 'lattice') -> List[Dict[str, Any]]:
        """Extract tables from PDF using PyMuPDF table finder"""
        try:
            doc = fitz.open(file_path)
            tables = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                
                # Find tables on the page
                tables_found = page.find_tables()
                
                if tables_found.tables:
                    for table_num, table in enumerate(tables_found.tables):
                        # Extract table data
                        table_data = []
                        
                        # Extract header (first row)
                        if table.to_dict():
                            header_cells = table.to_dict().get('header', [])
                            headers = [cell.get('text', '').strip() for cell in header_cells]
                            
                            # Extract rows
                            rows = []
                            for row in table.to_dict().get('cells', []):
                                row_data = [cell.get('text', '').strip() for cell in row]
                                rows.append(row_data)
                            
                            table_info = {
                                "page_number": page_num + 1,
                                "table_number": table_num + 1,
                                "headers": headers,
                                "rows": rows,
                                "bbox": BoundingBox.from_list(list(table.bbox)).to_list(),
                                "accuracy": table.extract_results.get('accuracy', 0.0) if hasattr(table, 'extract_results') else None
                            }
                            
                            tables.append(table_info)
                            logger.info(f"Extracted table on page {page_num + 1}, {len(rows)} rows")
            
            doc.close()
            logger.info(f"Total tables extracted: {len(tables)}")
            
            return tables
            
        except Exception as e:
            logger.error(f"Error extracting tables from PDF: {str(e)}")
            return []
    
    def extract_table_from_page(self, page, table_num: int) -> Dict[str, Any]:
        """
        Extract a specific table from a page
        
        Args:
            page: PyMuPDF page object
            table_num: Table number on the page
            
        Returns:
            Table information
        """
        try:
            tables_found = page.find_tables()
            
            if table_num < len(tables_found.tables):
                table = tables_found.tables[table_num]
                
                table_data = {
                    "page_number": page.number + 1,
                    "table_number": table_num + 1,
                    "bbox": BoundingBox.from_list(list(table.bbox)).to_list()
                }
                
                # Try to extract table content
                if table.to_dict():
                    header_cells = table.to_dict().get('header', [])
                    headers = [cell.get('text', '').strip() for cell in header_cells]
                    
                    rows = []
                    for row in table.to_dict().get('cells', []):
                        row_data = [cell.get('text', '').strip() for cell in row]
                        rows.append(row_data)
                    
                    table_data["headers"] = headers
                    table_data["rows"] = rows
                
                return table_data
                
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error extracting table {table_num} from page: {str(e)}")
            return None
    
    def detect_tables(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Detect table locations in document without extracting content
        
        Args:
            file_path: Path to document file
            
        Returns:
            List of table locations
        """
        try:
            doc = fitz.open(file_path)
            table_locations = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                tables_found = page.find_tables()
                
                for table in tables_found.tables:
                    table_locations.append({
                        "page_number": page_num + 1,
                        "bbox": BoundingBox.from_list(list(table.bbox)).to_list(),
                        "type": "table"
                    })
            
            doc.close()
            
            return table_locations
            
        except Exception as e:
            logger.error(f"Error detecting tables: {str(e)}")
            return []