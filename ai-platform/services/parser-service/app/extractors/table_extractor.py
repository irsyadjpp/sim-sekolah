import fitz  # PyMuPDF
from typing import Optional, Dict, Any, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class TableExtractor:
    """Extract tables from documents using PyMuPDF"""
    
    def __init__(self):
        """Initialize table extractor"""
        self.supported_formats = ['.pdf']
    
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
                                "bbox": table.bbox,
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
                    "bbox": table.bbox
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
                        "bbox": table.bbox,
                        "type": "table"
                    })
            
            doc.close()
            
            return table_locations
            
        except Exception as e:
            logger.error(f"Error detecting tables: {str(e)}")
            return []