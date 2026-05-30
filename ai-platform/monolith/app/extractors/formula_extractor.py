"""
Formula Extractor untuk Parser Service
Khusus untuk ekstraksi formula matematika dari buku/pelajaran
Mendukung berbagai format: LaTeX, MathML, gambar formula, dll
"""
import logging
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import fitz  # PyMuPDF
import io
from pathlib import Path

from app.models.document_models import Region, BoundingBox

logger = logging.getLogger(__name__)


class FormulaType(Enum):
    """Tipe formula matematika"""
    INLINE = "inline"          # Inline formula dalam teks (e.g., $E=mc^2$)
    DISPLAY = "display"        # Display formula terpisah (e.g., $$\int f(x)dx$$)
    CHEMICAL = "chemical"      # Formula kimia (e.g., H₂O, CO₂)
    EQUATION = "equation"      # Persamaan lengkap dengan nomor
    INEQUALITY = "inequality"  # Pertidaksamaan
    EXPRESSION = "expression"  # Ekspresi matematika
    UNKNOWN = "unknown"


class FormulaFormat(Enum):
    """Format formula"""
    LATEX = "latex"
    MATHML = "mathml"
    IMAGE = "image"
    PLAIN_TEXT = "plain_text"
    UNICODE = "unicode"
    UNKNOWN = "unknown"


@dataclass
class RawFormulaMetadata:
    """Metadata mentah untuk formula yang diekstrak"""
    formula_id: str
    xref: Optional[int] = None
    page_number: int = 0
    page_width: int = 0
    page_height: int = 0
    bbox: List[float] = field(default_factory=list)          # [x0, y0, x1, y1]
    bbox_normalized: List[float] = field(default_factory=list)
    
    # Formula content
    formula_content: str = ""
    formula_format: FormulaFormat = FormulaFormat.UNKNOWN
    formula_type: FormulaType = FormulaType.UNKNOWN
    latex_representation: str = ""
    
    # Quality indicators
    extraction_confidence: float = 0.0
    is_likely_noise: bool = False
    noise_reason: str = ""
    
    # Context
    surrounding_text: str = ""
    has_numbering: bool = False
    equation_number: str = ""
    
    # Advanced features
    variables: List[str] = field(default_factory=list)
    operators: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    symbols: List[str] = field(default_factory=list)
    
    # Subject classification
    subject_area: str = ""
    difficulty_level: str = ""
    grade_level: str = ""


@dataclass
class FormulaExtractionResult:
    """Hasil ekstraksi formula"""
    doc_id: str
    file_path: str
    total_formulas_extracted: int
    formulas: List[RawFormulaMetadata] = field(default_factory=list)
    by_format: Dict[str, int] = field(default_factory=dict)
    by_type: Dict[str, int] = field(default_factory=dict)
    by_page: Dict[int, int] = field(default_factory=dict)
    processing_time: float = 0.0
    errors: List[str] = field(default_factory=list)


class FormulaExtractor:
    """
    Extractor khusus untuk formula matematika dari PDF documents
    
    NEW: Region-aware extraction for modern pipeline.
    
    Mendukung:
    - Inline LaTeX formulas ($...$)
    - Display LaTeX formulas ($$...$$, \[...\], \begin{equation}...\end{equation})
    - Mathematical expressions dalam text
    - Chemical formulas
    - Image-based formulas dengan OCR
    - Unicode mathematical symbols
    """
    
    def __init__(
        self,
        detect_inline: bool = True,
        detect_display: bool = True,
        detect_chemical: bool = True,
        extract_variables: bool = True,
        min_confidence: float = 0.5
    ):
        """
        Initialize Formula Extractor
        
        Args:
            detect_inline: Detect inline formulas ($...$)
            detect_display: Detect display formulas ($$...$$)
            detect_chemical: Detect chemical formulas
            extract_variables: Extract variables dari formulas
            min_confidence: Minimum confidence score untuk extraction
        """
        self.detect_inline = detect_inline
        self.detect_display = detect_display
        self.detect_chemical = detect_chemical
        self.extract_variables = extract_variables
        self.min_confidence = min_confidence
        
        # Regex patterns untuk formula detection
        self._init_regex_patterns()
        
        # Mathematical patterns untuk classification
        self._init_mathematical_patterns()
        
        logger.info("FormulaExtractor initialized with mathematical formula detection")
    
    def extract_from_region(
        self, 
        region: Region, 
        page: fitz.Page,
        options: Optional[Dict[str, Any]] = None
    ) -> Optional[RawFormulaMetadata]:
        """
        Extract formula content from a specific region (region-aware).
        
        This is the NEW method for the modern pipeline.
        
        Args:
            region: Region object with bounding box and text content
            page: PyMuPDF page object
            options: Extraction options
            
        Returns:
            Formula metadata for this specific region
        """
        try:
            options = options or {}
            
            # Get text content from region
            text = region.text_content or ""
            
            if not text or len(text.strip()) < 2:
                return None
            
            # Detect formula type and format
            formula_type = self._classify_formula_type(text)
            formula_format = self._classify_formula_format(text)
            
            # Check if this is actually a formula
            if formula_type == FormulaType.UNKNOWN:
                return None
            
            # Extract formula content
            formula_content = self._extract_formula_content(text, formula_format)
            
            # Create formula metadata
            formula_metadata = RawFormulaMetadata(
                formula_id=f"{region.region_id}_formula",
                page_number=region.page_number,
                bbox=region.bbox.to_list(),
                formula_content=formula_content,
                formula_format=formula_format,
                formula_type=formula_type,
                extraction_confidence=self._calculate_confidence(text, formula_type),
                surrounding_text=text[:200],  # First 200 chars as context
            )
            
            # Extract variables if enabled
            if self.extract_variables:
                formula_metadata.variables = self._extract_variables(formula_content)
                formula_metadata.operators = self._extract_operators(formula_content)
                formula_metadata.functions = self._extract_functions(formula_content)
            
            logger.info(f"Extracted formula from region {region.region_id}: {formula_type.value}")
            
            return formula_metadata
            
        except Exception as e:
            logger.error(f"Error extracting formula from region {region.region_id}: {e}")
            return None
    
    def _classify_formula_type(self, text: str) -> FormulaType:
        """Classify the type of formula based on content"""
        # Check for LaTeX patterns
        if self.latex_inline_pattern.search(text):
            return FormulaType.INLINE
        if self.latex_display_pattern.search(text) or self.latex_equation_pattern.search(text):
            return FormulaType.DISPLAY
        
        # Check for chemical formulas
        if self.chemical_formula_pattern.search(text):
            return FormulaType.CHEMICAL
        
        # Check for mathematical operators
        if self.math_operators_pattern.search(text):
            # Check if it's an equation (has =)
            if '=' in text:
                return FormulaType.EQUATION
            # Check if it's an inequality
            if any(op in text for op in ['<', '>', '≤', '≥', '≠']):
                return FormulaType.INEQUALITY
            return FormulaType.EXPRESSION
        
        return FormulaType.UNKNOWN
    
    def _classify_formula_format(self, text: str) -> FormulaFormat:
        """Classify the format of formula"""
        if self.latex_inline_pattern.search(text) or self.latex_display_pattern.search(text):
            return FormulaFormat.LATEX
        if self.latex_equation_pattern.search(text):
            return FormulaFormat.LATEX
        if self.greek_letters_pattern.search(text):
            return FormulaFormat.UNICODE
        return FormulaFormat.PLAIN_TEXT
    
    def _extract_formula_content(self, text: str, formula_format: FormulaFormat) -> str:
        """Extract the actual formula content from text"""
        if formula_format == FormulaFormat.LATEX:
            # Extract LaTeX content
            match = self.latex_inline_pattern.search(text)
            if match:
                return match.group(1)
            match = self.latex_display_pattern.search(text)
            if match:
                return match.group(1) or match.group(2)
            match = self.latex_equation_pattern.search(text)
            if match:
                return match.group(1)
        
        # Return the text as-is for plain text
        return text.strip()
    
    def _calculate_confidence(self, text: str, formula_type: FormulaType) -> float:
        """Calculate confidence score for formula extraction"""
        base_confidence = 0.7
        
        # Increase confidence for LaTeX formulas
        if formula_type in [FormulaType.INLINE, FormulaType.DISPLAY]:
            base_confidence += 0.2
        
        # Increase confidence for mathematical operators
        if self.math_operators_pattern.search(text):
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _extract_variables(self, formula: str) -> List[str]:
        """Extract variables from formula"""
        variables = []
        for var in self.common_variables:
            if var in formula:
                variables.append(var)
        return variables
    
    def _extract_operators(self, formula: str) -> List[str]:
        """Extract operators from formula"""
        operators = []
        for op in self.math_operators:
            if op in formula:
                operators.append(op)
        return operators
    
    def _extract_functions(self, formula: str) -> List[str]:
        """Extract mathematical functions from formula"""
        functions = []
        for func in self.math_functions:
            if func in formula:
                functions.append(func)
        return functions
    
    def _init_regex_patterns(self):
        """Initialize regex patterns untuk formula detection"""
        # LaTeX inline formulas: $...$
        self.latex_inline_pattern = re.compile(r'\$([^$]+)\$')
        
        # LaTeX display formulas: $$...$$, \[...\]
        self.latex_display_pattern = re.compile(r'\$\$([^$]+)\$\$|\\\[([^\\]+)\\\]')
        
        # LaTeX equation environment: \begin{equation}...\end{equation}
        self.latex_equation_pattern = re.compile(
            r'\\begin\{equation\}([^\\]+)\\end\{equation\}',
            re.MULTILINE | re.DOTALL
        )
        
        # Chemical formulas: H₂O, CO₂, etc.
        self.chemical_formula_pattern = re.compile(
            r'\b[A-Z][a-z]?(?:\d+)?(?:[A-Z][a-z]?(?:\d+)?)*\b'
        )
        
        # Mathematical operators
        self.math_operators_pattern = re.compile(
            r'[+\-*/=<>≤≥≠≈±∑∏∫√∂∇∞]'
        )
        
        # Greek letters dan mathematical symbols
        self.greek_letters_pattern = re.compile(
            r'[αβγδεζηθικλμνξπρστυφχψω]'
        )
        
        # Subscript/superscript notation
        self.subscript_pattern = re.compile(r'_[a-zA-Z0-9]+')
        self.superscript_pattern = re.compile(r'\^[a-zA-Z0-9]+')
    
    def _init_mathematical_patterns(self):
        """Initialize mathematical patterns untuk classification"""
        # Common mathematical functions
        self.math_functions = [
            'sin', 'cos', 'tan', 'cot', 'sec', 'csc',
            'arcsin', 'arccos', 'arctan',
            'sinh', 'cosh', 'tanh', 'log', 'ln', 'exp',
            'sqrt', 'abs', 'sign', 'max', 'min', 'avg'
        ]
        
        # Common mathematical variables
        self.common_variables = [
            'x', 'y', 'z', 'a', 'b', 'c', 'n', 'm', 'k', 'i', 'j'
        ]
        
        # Mathematical operators
        self.math_operators = [
            '+', '-', '*', '/', '=', '<', '>', '≤', '≥', '≠', '≈', '±'
        ]
        
        # Greek letters
        self.greek_letters = [
            'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ',
            'ν', 'ξ', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω',
            'Delta', 'Sigma', 'Pi', 'Theta', 'Omega'
        ]
        
        # Mathematical symbols
        self.math_symbols = [
            '∑', '∏', '∫', '√', '∂', '∇', '∞', '∅', '∈', '∉', '⊂', '⊃',
            '∪', '∩', '∀', '∃', '→', '⇒', '⇔', '≡', '≈', '≠'
        ]
    
    def extract(
        self,
        file_path: str,
        doc_id: str,
        page_range: Optional[Tuple[int, int]] = None
    ) -> FormulaExtractionResult:
        """
        Extract formulas dari PDF document
        
        Args:
            file_path: Path ke PDF file
            doc_id: Document ID
            page_range: Optional tuple (start_page, end_page) untuk specific pages
        
        Returns:
            FormulaExtractionResult dengan semua formulas yang diekstrak
        """
        import time
        start_time = time.time()
        
        result = FormulaExtractionResult(
            doc_id=doc_id,
            file_path=file_path,
            total_formulas_extracted=0
        )
        
        try:
            doc = fitz.open(file_path)
            result.total_formulas_extracted = 0
            
            for page_num in range(doc.page_count):
                # Check page range
                if page_range and (page_num < page_range[0] - 1 or page_num > page_range[1] - 1):
                    continue
                
                page = doc[page_num]
                page_result = self._extract_formulas_from_page(page, page_num, doc_id)
                
                # Add formulas ke result
                result.formulas.extend(page_result['formulas'])
                result.total_formulas_extracted += len(page_result['formulas'])
                
                # Update statistics
                result.by_page[page_num + 1] = len(page_result['formulas'])
            
            doc.close()
            
            # Calculate statistics
            result.by_format = self._calculate_by_format(result.formulas)
            result.by_type = self._calculate_by_type(result.formulas)
            result.processing_time = time.time() - start_time
            
            logger.info(f"Extracted {result.total_formulas_extracted} formulas from {file_path}")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting formulas from {file_path}: {e}")
            result.errors.append(str(e))
            result.processing_time = time.time() - start_time
            return result
    
    def _extract_formulas_from_page(
        self,
        page: fitz.Page,
        page_num: int,
        doc_id: str
    ) -> Dict[str, Any]:
        """Extract formulas dari single page"""
        formulas = []
        
        # Get text dari page
        text_content = page.get_text()
        
        # Detect inline LaTeX formulas
        if self.detect_inline:
            inline_formulas = self._detect_inline_formulas(text_content, page, page_num, doc_id)
            formulas.extend(inline_formulas)
        
        # Detect display LaTeX formulas
        if self.detect_display:
            display_formulas = self._detect_display_formulas(text_content, page, page_num, doc_id)
            formulas.extend(display_formulas)
        
        # Detect chemical formulas
        if self.detect_chemical:
            chemical_formulas = self._detect_chemical_formulas(text_content, page, page_num, doc_id)
            formulas.extend(chemical_formulas)
        
        # Detect image-based formulas (lebih advanced)
        image_formulas = self._detect_image_formulas(page, page_num, doc_id)
        formulas.extend(image_formulas)
        
        return {'formulas': formulas}
    
    def _detect_inline_formulas(
        self,
        text: str,
        page: fitz.Page,
        page_num: int,
        doc_id: str
    ) -> List[RawFormulaMetadata]:
        """Detect inline LaTeX formulas ($...$)"""
        formulas = []
        matches = self.latex_inline_pattern.finditer(text)
        
        for match in matches:
            formula_content = match.group(1).strip()
            
            # Skip jika terlalu pendek atau noise
            if len(formula_content) < 2:
                continue
            
            # Extract components
            variables = self._extract_variables(formula_content)
            operators = self._extract_operators(formula_content)
            functions = self._extract_functions(formula_content)
            symbols = self._extract_symbols(formula_content)
            
            # Calculate confidence
            confidence = self._calculate_formula_confidence(
                formula_content, variables, operators, functions, symbols
            )
            
            if confidence < self.min_confidence:
                continue
            
            formula_id = f"{doc_id}_formula_inline_{page_num + 1}_{len(formulas)}"
            
            formula = RawFormulaMetadata(
                formula_id=formula_id,
                page_number=page_num + 1,
                page_width=page.rect.width,
                page_height=page.rect.height,
                formula_content=formula_content,
                formula_format=FormulaFormat.LATEX,
                formula_type=FormulaType.INLINE,
                latex_representation=formula_content,
                extraction_confidence=confidence,
                surrounding_text=self._get_surrounding_text(text, match.start(), match.end()),
                variables=variables,
                operators=operators,
                functions=functions,
                symbols=symbols
            )
            
            formulas.append(formula)
        
        return formulas
    
    def _detect_display_formulas(
        self,
        text: str,
        page: fitz.Page,
        page_num: int,
        doc_id: str
    ) -> List[RawFormulaMetadata]:
        """Detect display LaTeX formulas ($$...$$, \[...\])"""
        formulas = []
        matches = self.latex_display_pattern.finditer(text)
        
        for match in matches:
            # Get the matched group (either $$...$$ or \[...\])
            formula_content = match.group(1) if match.group(1) else match.group(2)
            if formula_content:
                formula_content = formula_content.strip()
            else:
                continue
            
            # Skip jika terlalu pendek
            if len(formula_content) < 2:
                continue
            
            # Extract components
            variables = self._extract_variables(formula_content)
            operators = self._extract_operators(formula_content)
            functions = self._extract_functions(formula_content)
            symbols = self._extract_symbols(formula_content)
            
            # Calculate confidence
            confidence = self._calculate_formula_confidence(
                formula_content, variables, operators, functions, symbols
            )
            
            if confidence < self.min_confidence:
                continue
            
            # Check untuk equation numbering
            has_numbering, equation_number = self._detect_equation_numbering(
                text, match.end()
            )
            
            formula_id = f"{doc_id}_formula_display_{page_num + 1}_{len(formulas)}"
            
            formula_type = FormulaType.EQUATION if has_numbering else FormulaType.DISPLAY
            
            formula = RawFormulaMetadata(
                formula_id=formula_id,
                page_number=page_num + 1,
                page_width=page.rect.width,
                page_height=page.rect.height,
                formula_content=formula_content,
                formula_format=FormulaFormat.LATEX,
                formula_type=formula_type,
                latex_representation=formula_content,
                extraction_confidence=confidence,
                surrounding_text=self._get_surrounding_text(text, match.start(), match.end()),
                has_numbering=has_numbering,
                equation_number=equation_number,
                variables=variables,
                operators=operators,
                functions=functions,
                symbols=symbols
            )
            
            formulas.append(formula)
        
        return formulas
    
    def _detect_chemical_formulas(
        self,
        text: str,
        page: fitz.Page,
        page_num: int,
        doc_id: str
    ) -> List[RawFormulaMetadata]:
        """Detect chemical formulas"""
        formulas = []
        matches = self.chemical_formula_pattern.finditer(text)
        
        for match in matches:
            formula_content = match.group(0)
            
            # Filter hanya chemical formulas yang valid
            if not self._is_chemical_formula(formula_content):
                continue
            
            formula_id = f"{doc_id}_formula_chemical_{page_num + 1}_{len(formulas)}"
            
            formula = RawFormulaMetadata(
                formula_id=formula_id,
                page_number=page_num + 1,
                page_width=page.rect.width,
                page_height=page.rect.height,
                formula_content=formula_content,
                formula_format=FormulaFormat.PLAIN_TEXT,
                formula_type=FormulaType.CHEMICAL,
                latex_representation=self._chemical_to_latex(formula_content),
                extraction_confidence=0.85,  # Chemical formulas biasanya high confidence
                surrounding_text=self._get_surrounding_text(text, match.start(), match.end()),
                subject_area="Chemistry",
                difficulty_level="basic"
            )
            
            formulas.append(formula)
        
        return formulas
    
    def _detect_image_formulas(
        self,
        page: fitz.Page,
        page_num: int,
        doc_id: str
    ) -> List[RawFormulaMetadata]:
        """Detect image-based formulas (advanced, memerlukan Vision Service)"""
        # For now, ini adalah placeholder
        # In production, ini akan call Vision Service untuk OCR and formula recognition
        formulas = []
        
        # Extract images dari page
        image_list = page.get_images(full=True)
        
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = page.parent.extract_image(xref)
            
            # Basic heuristic: jika image contains mathematical symbols
            # Ini bisa ditingkatkan dengan Vision Service integration
            
            # Untuk sekarang, skip image-based formula detection
            # karena butuh ML model untuk accuracy
            pass
        
        return formulas
    
    def _extract_variables(self, formula_content: str) -> List[str]:
        """Extract variables dari formula"""
        variables = []
        for var in self.common_variables:
            if var in formula_content:
                variables.append(var)
        return variables
    
    def _extract_operators(self, formula_content: str) -> List[str]:
        """Extract operators dari formula"""
        operators = []
        for op in self.math_operators:
            if op in formula_content:
                operators.append(op)
        return operators
    
    def _extract_functions(self, formula_content: str) -> List[str]:
        """Extract functions dari formula"""
        functions = []
        for func in self.math_functions:
            if func in formula_content:
                functions.append(func)
        return functions
    
    def _extract_symbols(self, formula_content: str) -> List[str]:
        """Extract mathematical symbols dari formula"""
        symbols = []
        for symbol in self.math_symbols:
            if symbol in formula_content:
                symbols.append(symbol)
        return symbols
    
    def _calculate_formula_confidence(
        self,
        formula_content: str,
        variables: List[str],
        operators: List[str],
        functions: List[str],
        symbols: List[str]
    ) -> float:
        """Calculate confidence score untuk formula"""
        confidence = 0.0
        
        # Base score untuk having mathematical content
        if variables or operators or functions or symbols:
            confidence += 0.4
        
        # Bonus untuk operators
        if operators:
            confidence += 0.2
        
        # Bonus untuk functions
        if functions:
            confidence += 0.2
        
        # Bonus untuk symbols
        if symbols:
            confidence += 0.1
        
        # Bonus untuk Greek letters
        if self.greek_letters_pattern.search(formula_content):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _get_surrounding_text(self, text: str, start: int, end: int, context_chars: int = 100) -> str:
        """Get surrounding text untuk context"""
        start_context = max(0, start - context_chars)
        end_context = min(len(text), end + context_chars)
        return text[start_context:end_context]
    
    def _detect_equation_numbering(self, text: str, position: int) -> Tuple[bool, str]:
        """Detect jika formula memiliki equation numbering"""
        # Look ahead untuk numbering patterns seperti (1), [1], etc.
        ahead_text = text[position:min(position + 50, len(text))]
        numbering_match = re.search(r'\((\d+)\)|\[(\d+)\]', ahead_text)
        
        if numbering_match:
            equation_num = numbering_match.group(1) if numbering_match.group(1) else numbering_match.group(2)
            return True, equation_num
        
        return False, ""
    
    def _is_chemical_formula(self, text: str) -> bool:
        """Check jika text adalah valid chemical formula"""
        # Basic heuristic: harus memiliki uppercase letter diikuti lowercase atau digit
        # dan multiple elements
        return (re.search(r'[A-Z][a-z]?\d*', text) and 
                len(re.findall(r'[A-Z]', text)) >= 2)
    
    def _chemical_to_latex(self, chemical_formula: str) -> str:
        """Convert chemical formula ke LaTeX representation"""
        # Simple conversion - gunakan subscripts
        latex_formula = chemical_formula
        latex_formula = re.sub(r'(\d+)', r'_{\1}', latex_formula)
        return f"${latex_formula}$"
    
    def _calculate_by_format(self, formulas: List[RawFormulaMetadata]) -> Dict[str, int]:
        """Calculate statistics by format"""
        by_format = {}
        for formula in formulas:
            format_name = formula.formula_format.value
            by_format[format_name] = by_format.get(format_name, 0) + 1
        return by_format
    
    def _calculate_by_type(self, formulas: List[RawFormulaMetadata]) -> Dict[str, int]:
        """Calculate statistics by type"""
        by_type = {}
        for formula in formulas:
            type_name = formula.formula_type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
        return by_type