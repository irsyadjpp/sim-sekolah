"""
Table Processor untuk Parser Service
Post-processing untuk extracted tables dengan HTML normalization
Converts raw table data ke structured HTML format dengan proper formatting
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re
from html import escape

logger = logging.getLogger(__name__)


class TableFormat(Enum):
    """Output format untuk tables"""
    HTML = "html"
    MARKDOWN = "markdown"
    CSV = "csv"
    JSON = "json"
    LATEX = "latex"


class TableStyle(Enum):
    """Styling options untuk HTML tables"""
    BASIC = "basic"              # Simple HTML table
    BOOTSTRAP = "bootstrap"      # Bootstrap styled
    MATERIAL = "material"        # Material Design styled
    EDUCATIONAL = "educational"  # Educational content specific
    COMPACT = "compact"          # Compact layout


@dataclass
class TableProcessingOptions:
    """Options untuk table processing"""
    output_format: TableFormat = TableFormat.HTML
    table_style: TableStyle = TableStyle.EDUCATIONAL
    include_headers: bool = True
    include_captions: bool = False
    caption_text: str = ""
    strip_whitespace: bool = True
    normalize_cells: bool = True
    add_row_numbers: bool = False
    merge_empty_cells: bool = False
    preserve_formatting: bool = False
    
    # HTML-specific options
    add_css_classes: bool = True
    add_responsive_wrapper: bool = True
    add_sorting_support: bool = False
    
    # Educational-specific options
    highlight_important_cells: bool = False
    add_row_headers: bool = False
    enable_search: bool = False


@dataclass
class ProcessedTable:
    """Hasil processing untuk table"""
    table_id: str
    original_data: Dict[str, Any]
    processed_content: str
    output_format: TableFormat
    processing_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Quality metrics
    row_count: int = 0
    column_count: int = 0
    empty_cells: int = 0
    merged_cells: int = 0
    
    # Content analysis
    has_numeric_data: bool = False
    has_text_data: bool = False
    has_mixed_data: bool = False
    data_types: List[str] = field(default_factory=list)


class TableProcessor:
    """
    Processor untuk extracted tables
    
    Functionality:
    - HTML normalization dengan proper structure
    - Data cleaning dan normalization
    - Educational formatting
    - Format conversion (HTML, Markdown, CSV, JSON, LaTeX)
    - Quality assessment
    """
    
    def __init__(self, default_style: TableStyle = TableStyle.EDUCATIONAL):
        """
        Initialize Table Processor
        
        Args:
            default_style: Default styling untuk HTML tables
        """
        self.default_style = default_style
        
        logger.info("TableProcessor initialized with educational table formatting")
    
    def process_table(
        self,
        table_data: Dict[str, Any],
        table_id: str,
        options: Optional[TableProcessingOptions] = None
    ) -> ProcessedTable:
        """
        Process extracted table dengan normalization
        
        Args:
            table_data: Raw table data dari extractor
            table_id: Unique identifier untuk table
            options: Processing options
        
        Returns:
            ProcessedTable dengan normalized content
        """
        if options is None:
            options = TableProcessingOptions()
        
        try:
            # Extract table components
            headers = table_data.get('headers', [])
            rows = table_data.get('rows', [])
            metadata = table_data.get('metadata', {})
            
            # Normalize table data
            normalized_headers, normalized_rows = self._normalize_table_data(
                headers, rows, options
            )
            
            # Generate output based on format
            if options.output_format == TableFormat.HTML:
                processed_content = self._generate_html_table(
                    normalized_headers, normalized_rows, table_id, options
                )
            elif options.output_format == TableFormat.MARKDOWN:
                processed_content = self._generate_markdown_table(
                    normalized_headers, normalized_rows, options
                )
            elif options.output_format == TableFormat.CSV:
                processed_content = self._generate_csv_table(
                    normalized_headers, normalized_rows, options
                )
            elif options.output_format == TableFormat.JSON:
                processed_content = self._generate_json_table(
                    normalized_headers, normalized_rows, metadata, options
                )
            elif options.output_format == TableFormat.LATEX:
                processed_content = self._generate_latex_table(
                    normalized_headers, normalized_rows, options
                )
            else:
                processed_content = self._generate_html_table(
                    normalized_headers, normalized_rows, table_id, options
                )
            
            # Analyze content
            content_analysis = self._analyze_table_content(normalized_headers, normalized_rows)
            
            # Count empty cells
            empty_cells = self._count_empty_cells(normalized_headers, normalized_rows)
            
            result = ProcessedTable(
                table_id=table_id,
                original_data=table_data,
                processed_content=processed_content,
                output_format=options.output_format,
                processing_metadata={
                    'options': options.__dict__,
                    'page_number': metadata.get('page_number', 0),
                    'processing_timestamp': metadata.get('timestamp', '')
                },
                row_count=len(normalized_rows),
                column_count=len(normalized_headers),
                empty_cells=empty_cells,
                has_numeric_data=content_analysis['has_numeric'],
                has_text_data=content_analysis['has_text'],
                has_mixed_data=content_analysis['has_mixed'],
                data_types=content_analysis['data_types']
            )
            
            logger.info(f"Processed table {table_id}: {result.row_count} rows, {result.column_count} cols")
            return result
            
        except Exception as e:
            logger.error(f"Error processing table {table_id}: {e}")
            # Return minimally processed table
            return ProcessedTable(
                table_id=table_id,
                original_data=table_data,
                processed_content="<p>Error processing table</p>",
                output_format=options.output_format
            )
    
    def _normalize_table_data(
        self,
        headers: List[str],
        rows: List[List[str]],
        options: TableProcessingOptions
    ) -> Tuple[List[str], List[List[str]]]:
        """Normalize table data"""
        # Normalize headers
        normalized_headers = []
        for header in headers:
            if options.strip_whitespace:
                header = header.strip()
            if options.normalize_cells:
                header = self._normalize_cell(header)
            normalized_headers.append(header)
        
        # Normalize rows
        normalized_rows = []
        for row in rows:
            normalized_row = []
            for cell in row:
                if options.strip_whitespace:
                    cell = str(cell).strip()
                if options.normalize_cells:
                    cell = self._normalize_cell(cell)
                normalized_row.append(cell)
            normalized_rows.append(normalized_row)
        
        return normalized_headers, normalized_rows
    
    def _normalize_cell(self, cell: str) -> str:
        """Normalize individual cell content"""
        cell = str(cell)
        # Remove excessive whitespace
        cell = re.sub(r'\s+', ' ', cell)
        # Normalize line breaks
        cell = cell.replace('\n', ' ').replace('\r', ' ')
        return cell.strip()
    
    def _generate_html_table(
        self,
        headers: List[str],
        rows: List[List[str]],
        table_id: str,
        options: TableProcessingOptions
    ) -> str:
        """Generate HTML table"""
        css_class = self._get_css_class(options.table_style)
        
        html_parts = []
        
        # Responsive wrapper
        if options.add_responsive_wrapper:
            html_parts.append('<div class="table-responsive">')
        
        # Table opening
        table_attrs = [
            f'id="{table_id}"',
            f'class="{css_class}"'
        ]
        if options.add_sorting_support:
            table_attrs.append('data-toggle="table"')
        
        html_parts.append(f'<table {" ".join(table_attrs)}>')
        
        # Caption
        if options.include_captions and options.caption_text:
            html_parts.append(f'<caption>{escape(options.caption_text)}</caption>')
        
        # Table header
        if options.include_headers:
            html_parts.append('<thead>')
            html_parts.append('<tr>')
            
            if options.add_row_numbers:
                html_parts.append('<th>#</th>')
            
            for header in headers:
                header_html = escape(header)
                if options.highlight_important_cells and self._is_important_header(header):
                    header_html = f'<strong>{header_html}</strong>'
                html_parts.append(f'<th>{header_html}</th>')
            
            html_parts.append('</tr>')
            html_parts.append('</thead>')
        
        # Table body
        html_parts.append('<tbody>')
        for row_idx, row in enumerate(rows, 1):
            html_parts.append('<tr>')
            
            if options.add_row_numbers:
                html_parts.append(f'<td>{row_idx}</td>')
            
            for cell in row:
                cell_html = escape(cell)
                if options.highlight_important_cells and self._is_important_cell(cell):
                    cell_html = f'<strong>{cell_html}</strong>'
                html_parts.append(f'<td>{cell_html}</td>')
            
            html_parts.append('</tr>')
        html_parts.append('</tbody>')
        
        # Table footer (optional)
        if options.include_headers:
            html_parts.append('<tfoot>')
            html_parts.append('<tr>')
            
            if options.add_row_numbers:
                html_parts.append('<th>#</th>')
            
            for header in headers:
                html_parts.append(f'<th>{escape(header)}</th>')
            
            html_parts.append('</tr>')
            html_parts.append('</tfoot>')
        
        html_parts.append('</table>')
        
        # Close responsive wrapper
        if options.add_responsive_wrapper:
            html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    def _generate_markdown_table(
        self,
        headers: List[str],
        rows: List[List[str]],
        options: TableProcessingOptions
    ) -> str:
        """Generate Markdown table"""
        md_parts = []
        
        # Header row
        if options.add_row_numbers:
            header_row = ['#'] + headers
        else:
            header_row = headers
        
        md_parts.append('| ' + ' | '.join(header_row) + ' |')
        
        # Separator row
        separators = ['---'] * len(header_row)
        md_parts.append('| ' + ' | '.join(separators) + ' |')
        
        # Data rows
        for row_idx, row in enumerate(rows, 1):
            if options.add_row_numbers:
                data_row = [str(row_idx)] + row
            else:
                data_row = row
            
            md_parts.append('| ' + ' | '.join(data_row) + ' |')
        
        return '\n'.join(md_parts)
    
    def _generate_csv_table(
        self,
        headers: List[str],
        rows: List[List[str]],
        options: TableProcessingOptions
    ) -> str:
        """Generate CSV table"""
        import io
        import csv
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        if options.add_row_numbers:
            csv_headers = ['#'] + headers
        else:
            csv_headers = headers
        
        writer.writerow(csv_headers)
        
        for row_idx, row in enumerate(rows, 1):
            if options.add_row_numbers:
                csv_row = [row_idx] + row
            else:
                csv_row = row
            writer.writerow(csv_row)
        
        return output.getvalue()
    
    def _generate_json_table(
        self,
        headers: List[str],
        rows: List[List[str]],
        metadata: Dict[str, Any],
        options: TableProcessingOptions
    ) -> str:
        """Generate JSON table"""
        import json
        
        json_data = {
            'headers': headers,
            'rows': rows,
            'metadata': metadata,
            'options': options.__dict__
        }
        
        return json.dumps(json_data, indent=2)
    
    def _generate_latex_table(
        self,
        headers: List[str],
        rows: List[List[str]],
        options: TableProcessingOptions
    ) -> str:
        """Generate LaTeX table"""
        col_count = len(headers)
        col_spec = 'c' * col_count
        
        latex_parts = []
        latex_parts.append(f'\\begin{{tabular}}{{{col_spec}}}')
        latex_parts.append('\\hline')
        
        # Header row
        header_line = ' & '.join([h.replace('_', '\\_') for h in headers])
        latex_parts.append(header_line + ' \\\\')
        latex_parts.append('\\hline')
        
        # Data rows
        for row in rows:
            row_line = ' & '.join([str(cell).replace('_', '\\_') for cell in row])
            latex_parts.append(row_line + ' \\\\')
            latex_parts.append('\\hline')
        
        latex_parts.append('\\end{tabular}')
        
        return '\n'.join(latex_parts)
    
    def _get_css_class(self, style: TableStyle) -> str:
        """Get CSS class untuk table style"""
        classes = {
            TableStyle.BASIC: 'table table-bordered',
            TableStyle.BOOTSTRAP: 'table table-striped table-hover table-bordered',
            TableStyle.MATERIAL: 'table table-sm table-responsive-md',
            TableStyle.EDUCATIONAL: 'table table-bordered table-hover educational-table',
            TableStyle.COMPACT: 'table table-sm table-bordered'
        }
        return classes.get(style, 'table table-bordered')
    
    def _is_important_header(self, header: str) -> bool:
        """Check jika header is important (highlighting)"""
        important_keywords = ['total', 'jumlah', 'sum', 'average', 'rata-rata', 'score', 'nilai']
        return any(keyword.lower() in header.lower() for keyword in important_keywords)
    
    def _is_important_cell(self, cell: str) -> bool:
        """Check jika cell is important (highlighting)"""
        # Numeric values yang terlihat important
        numeric_pattern = r'^\d+(\.\d+)?%$|^[\d,]+$'
        if re.match(numeric_pattern, cell.strip()):
            return True
        return False
    
    def _analyze_table_content(
        self,
        headers: List[str],
        rows: List[List[str]]
    ) -> Dict[str, Any]:
        """Analyze table content untuk quality assessment"""
        has_numeric = False
        has_text = False
        data_types = []
        
        all_cells = headers + [cell for row in rows for cell in row]
        
        for cell in all_cells:
            if self._is_numeric(cell):
                has_numeric = True
                if 'numeric' not in data_types:
                    data_types.append('numeric')
            else:
                has_text = True
                if 'text' not in data_types:
                    data_types.append('text')
        
        has_mixed = has_numeric and has_text
        
        return {
            'has_numeric': has_numeric,
            'has_text': has_text,
            'has_mixed': has_mixed,
            'data_types': data_types
        }
    
    def _is_numeric(self, value: str) -> bool:
        """Check jika value is numeric"""
        try:
            float(str(value).replace(',', ''))
            return True
        except (ValueError, TypeError):
            return False
    
    def _count_empty_cells(
        self,
        headers: List[str],
        rows: List[List[str]]
    ) -> int:
        """Count empty cells dalam table"""
        empty_count = 0
        
        for header in headers:
            if not header or header.strip() == '':
                empty_count += 1
        
        for row in rows:
            for cell in row:
                if not cell or cell.strip() == '':
                    empty_count += 1
        
        return empty_count
    
    def batch_process_tables(
        self,
        tables_data: List[Dict[str, Any]],
        options: Optional[TableProcessingOptions] = None
    ) -> List[ProcessedTable]:
        """
        Process multiple tables secara batch
        
        Args:
            tables_data: List of table data dictionaries
            options: Processing options (applied ke semua tables)
        
        Returns:
            List of ProcessedTable objects
        """
        results = []
        
        for idx, table_data in enumerate(tables_data):
            table_id = table_data.get('chunk_id', f'table_{idx}')
            try:
                processed_table = self.process_table(table_data, table_id, options)
                results.append(processed_table)
            except Exception as e:
                logger.error(f"Error processing table {table_id}: {e}")
                continue
        
        logger.info(f"Batch processed {len(results)}/{len(tables_data)} tables")
        return results