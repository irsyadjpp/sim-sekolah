"""
Formula Processor untuk Parser Service
Post-processing untuk extracted formulas dengan format conversion (LaTeX → display format)
Converts LaTeX formulas ke various display formats untuk educational content
"""
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import re

logger = logging.getLogger(__name__)


class FormulaOutputFormat(Enum):
    """Output format untuk formulas"""
    LATEX = "latex"
    MATHML = "mathml"
    HTML = "html"
    SAGE = "sage"           # SageMath
    SYMPY = "sympy"         # SymPy
    WOLFRAM = "wolfram"     # Wolfram Alpha format
    PLAIN_TEXT = "plain"
    UNICODE = "unicode"


class FormulaRenderingMode(Enum):
    """Rendering mode untuk formulas"""
    INLINE = "inline"          # Inline dalam teks ($E=mc^2$)
    DISPLAY = "display"        # Terpisah di baris sendiri ($$\int f(x)dx$$)
    BLOCK = "block"            # Block centered
    NUMBERED = "numbered"      # Dengan numbering


@dataclass
class FormulaProcessingOptions:
    """Options untuk formula processing"""
    output_format: FormulaOutputFormat = FormulaOutputFormat.LATEX
    rendering_mode: FormulaRenderingMode = FormulaRenderingMode.DISPLAY
    
    # Formatting options
    simplify: bool = True                  # Simplify mathematical expressions
    expand: bool = False                  # Expand expressions
    factor: bool = False                  # Factor expressions
    rational_simplify: bool = False        # Rational simplification
    
    # Display options
    add_numbering: bool = False           # Auto-numbering
    add_captions: bool = False            # Add captions
    caption_text: str = ""
    
    # Educational options
    show_steps: bool = False              # Show solving steps
    explanation_level: str = "basic"     # basic, intermediate, advanced
    
    # Compatibility
    mathjax_compatible: bool = True       # MathJAX compatible output
    katex_compatible: bool = True         # KaTeX compatible output


@dataclass
class ProcessedFormula:
    """Hasil processing untuk formula"""
    formula_id: str
    original_latex: str
    processed_content: str
    output_format: FormulaOutputFormat
    rendering_mode: FormulaRenderingMode
    
    # Metadata
    formula_type: str = ""                # equation, inequality, expression
    complexity_level: str = ""            # simple, moderate, complex
    variables: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    
    # Display info
    is_numbered: bool = False
    equation_number: str = ""
    caption: str = ""
    
    # Validation
    is_valid: bool = True
    validation_errors: List[str] = field(default_factory=list)
    
    # Processing metadata
    processing_time: float = 0.0
    simplified: bool = False
    expanded: bool = False


class FormulaProcessor:
    """
    Processor untuk extracted formulas
    
    Functionality:
    - LaTeX format conversion ke MathML, HTML, etc.
    - Formula simplification dan expansion
    - Mathematical expression manipulation
    - Educational format conversion
    - Validation dan error checking
    """
    
    def __init__(self, enable_simplify: bool = True):
        """
        Initialize Formula Processor
        
        Args:
            enable_simplify: Enable automatic formula simplification
        """
        self.enable_simplify = enable_simplify
        
        # Initialize regex patterns
        self._init_patterns()
        
        logger.info("FormulaProcessor initialized with mathematical formula conversion")
    
    def _init_patterns(self):
        """Initialize regex patterns untuk formula processing"""
        # Common LaTeX patterns
        self.latex_patterns = {
            'fraction': re.compile(r'\\frac\{([^}]+)\}\{([^}]+)\}'),
            'sqrt': re.compile(r'\\sqrt\{([^}]+)\}'),
            'power': re.compile(r'\^(\w+|\{[^}]+\})'),
            'subscript': re.compile(r'_(\w+|\{[^}]+\})'),
            'integral': re.compile(r'\\int[^{]*\{[^}]*\}'),
            'sum': re.compile(r'\\sum[^{]*\{[^}]*\}'),
            'limit': re.compile(r'\\lim[^{]*\{[^}]*\}'),
            'greek_letters': re.compile(r'\\[a-zA-Z]+'),
        }
    
    def process_formula(
        self,
        formula_data: Dict[str, Any],
        formula_id: str,
        options: Optional[FormulaProcessingOptions] = None
    ) -> ProcessedFormula:
        """
        Process extracted formula dengan format conversion
        
        Args:
            formula_data: Raw formula data dari extractor
            formula_id: Unique identifier untuk formula
            options: Processing options
        
        Returns:
            ProcessedFormula dengan converted content
        """
        if options is None:
            options = FormulaProcessingOptions()
        
        import time
        start_time = time.time()
        
        try:
            # Extract original LaTeX
            original_latex = formula_data.get('latex_representation', formula_data.get('formula_content', ''))
            
            if not original_latex:
                return ProcessedFormula(
                    formula_id=formula_id,
                    original_latex="",
                    processed_content="",
                    output_format=options.output_format,
                    rendering_mode=options.rendering_mode,
                    is_valid=False,
                    validation_errors=["No LaTeX content found"]
                )
            
            # Validate LaTeX syntax
            validation_result = self._validate_latex(original_latex)
            if not validation_result['is_valid']:
                return ProcessedFormula(
                    formula_id=formula_id,
                    original_latex=original_latex,
                    processed_content=original_latex,  # Return original if invalid
                    output_format=FormulaOutputFormat.LATEX,
                    rendering_mode=options.rendering_mode,
                    is_valid=False,
                    validation_errors=validation_result['errors']
                )
            
            # Simplify if requested
            processed_latex = original_latex
            if options.simplify and self.enable_simplify:
                simplified = self._simplify_latex(processed_latex)
                if simplified != processed_latex:
                    processed_latex = simplified
                    simplified_result = True
                else:
                    simplified_result = False
            else:
                simplified_result = False
            
            # Convert to requested format
            if options.output_format == FormulaOutputFormat.LATEX:
                processed_content = self._render_latex(processed_latex, options.rendering_mode)
            elif options.output_format == FormulaOutputFormat.MATHML:
                processed_content = self._convert_to_mathml(processed_latex)
            elif options.output_format == FormulaOutputFormat.HTML:
                processed_content = self._convert_to_html(processed_latex, options)
            elif options.output_format == FormulaOutputFormat.PLAIN_TEXT:
                processed_content = self._convert_to_plain_text(processed_latex)
            elif options.output_format == FormulaOutputFormat.UNICODE:
                processed_content = self._convert_to_unicode(processed_latex)
            elif options.output_format == FormulaOutputFormat.SYMPY:
                processed_content = self._convert_to_sympy(processed_latex)
            else:
                processed_content = self._render_latex(processed_latex, options.rendering_mode)
            
            # Extract components
            variables = self._extract_variables(processed_latex)
            functions = self._extract_functions(processed_latex)
            
            # Determine complexity
            complexity = self._determine_complexity(processed_latex)
            
            # Add numbering jika requested
            is_numbered = False
            equation_number = ""
            if options.add_numbering:
                is_numbered = True
                equation_number = str(formula_data.get('equation_number', '1'))
            
            # Add caption jika requested
            caption = ""
            if options.add_captions:
                caption = options.caption_text or formula_data.get('caption', '')
            
            result = ProcessedFormula(
                formula_id=formula_id,
                original_latex=original_latex,
                processed_content=processed_content,
                output_format=options.output_format,
                rendering_mode=options.rendering_mode,
                formula_type=formula_data.get('formula_type', 'unknown'),
                complexity_level=complexity,
                variables=variables,
                functions=functions,
                is_numbered=is_numbered,
                equation_number=equation_number,
                caption=caption,
                is_valid=True,
                processing_time=time.time() - start_time,
                simplified=simplified_result
            )
            
            logger.info(f"Processed formula {formula_id}: {options.output_format.value}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing formula {formula_id}: {e}")
            return ProcessedFormula(
                formula_id=formula_id,
                original_latex=formula_data.get('formula_content', ''),
                processed_content="",
                output_format=options.output_format,
                rendering_mode=options.rendering_mode,
                is_valid=False,
                validation_errors=[str(e)]
            )
    
    def _validate_latex(self, latex: str) -> Dict[str, Any]:
        """Validate LaTeX syntax"""
        errors = []
        
        # Check untuk balanced braces
        brace_count = latex.count('{') - latex.count('}')
        if brace_count != 0:
            errors.append(f"Unbalanced braces: {brace_count} unmatched")
        
        # Check untuk common syntax errors
        if '\\frac{' in latex and latex.count('}') < latex.count('{'):
            errors.append("Missing closing brace in fraction")
        
        if '\\sqrt{' in latex and latex.count('}') < latex.count('{'):
            errors.append("Missing closing brace in square root")
        
        # Check untuk invalid patterns
        invalid_patterns = ['\\\\\\', '\\\\{', '\\\\}']
        for pattern in invalid_patterns:
            if pattern in latex:
                errors.append(f"Invalid pattern detected: {pattern}")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def _simplify_latex(self, latex: str) -> str:
        """Simplify LaTeX expression (basic simplification)"""
        # Basic simplification rules
        simplified = latex
        
        # Remove redundant spaces
        simplified = re.sub(r'\s+', ' ', simplified)
        
        # Simplify common patterns
        simplified = re.sub(r'\{1\}', '', simplified)  # Remove {1}
        simplified = re.sub(r'\^{1}', '', simplified)  # Remove ^1
        simplified = re.sub(r'_{1}', '', simplified)  # Remove _1
        
        return simplified.strip()
    
    def _render_latex(self, latex: str, mode: FormulaRenderingMode) -> str:
        """Render LaTeX dalam appropriate mode"""
        if mode == FormulaRenderingMode.INLINE:
            return f'${latex}$'
        elif mode == FormulaRenderingMode.DISPLAY:
            return f'$${latex}$$'
        elif mode == FormulaRenderingMode.BLOCK:
            return f'\\[{latex}\\]'
        elif mode == FormulaRenderingMode.NUMBERED:
            return f'\\begin{{equation}}{latex}\\end{{equation}}'
        else:
            return f'$${latex}$$'
    
    def _convert_to_mathml(self, latex: str) -> str:
        """Convert LaTeX ke MathML"""
        # Basic LaTeX to MathML conversion
        # Note: Ini adalah simplified conversion - production would need proper MathML library
        
        mathml = '<math xmlns="http://www.w3.org/1998/Math/MathML">'
        mathml += '<mrow>'
        
        # Handle fractions
        if '\\frac' in latex:
            frac_match = self.latex_patterns['fraction'].search(latex)
            if frac_match:
                numerator = frac_match.group(1)
                denominator = frac_match.group(2)
                mathml += f'<mfrac><mrow>{self._convert_to_mathml_segment(numerator)}</mrow>'
                mathml += f'<mrow>{self._convert_to_mathml_segment(denominator)}</mrow></mfrac>'
        else:
            mathml += self._convert_to_mathml_segment(latex)
        
        mathml += '</mrow></math>'
        return mathml
    
    def _convert_to_mathml_segment(self, segment: str) -> str:
        """Convert LaTeX segment ke MathML segment"""
        # Remove LaTeX delimiters
        segment = segment.replace('{', '').replace('}', '')
        
        # Handle basic operators
        segment = segment.replace('\\times', '<mo>&times;</mo>')
        segment = segment.replace('\\div', '<mo>&div;</mo>')
        segment = segment.replace('\\pm', '<mo>&pm;</mo>')
        segment = segment.replace('\\mp', '<mo>&mp;</mo>')
        segment = segment.replace('\\le', '<mo>&le;</mo>')
        segment = segment.replace('\\ge', '<mo>&ge;</mo>')
        segment = segment.replace('\\ne', '<mo>&ne;</mo>')
        
        return segment
    
    def _convert_to_html(self, latex: str, options: FormulaProcessingOptions) -> str:
        """Convert LaTeX ke HTML dengan MathJax/KaTeX compatibility"""
        # For web display, we typically use MathJax atau KaTeX
        # Return LaTeX dalam appropriate delimiter
        
        if options.mathjax_compatible:
            if options.rendering_mode == FormulaRenderingMode.INLINE:
                return f'\\({latex}\\)'
            else:
                return f'\\[{latex}\\]'
        elif options.katex_compatible:
            if options.rendering_mode == FormulaRenderingMode.INLINE:
                return f'${latex}$'
            else:
                return f'$$latex\n{latex}\n$$'
        else:
            return self._render_latex(latex, options.rendering_mode)
    
    def _convert_to_plain_text(self, latex: str) -> str:
        """Convert LaTeX ke plain text representation"""
        plain = latex
        
        # Remove LaTeX commands
        plain = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1/\2', plain)
        plain = re.sub(r'\\sqrt\{([^}]+)\}', r'sqrt(\1)', plain)
        plain = re.sub(r'\\int', '∫', plain)
        plain = re.sub(r'\\sum', 'Σ', plain)
        plain = re.sub(r'\\lim', 'lim', plain)
        
        # Handle subscripts dan superscripts
        plain = re.sub(r'\^(\w+|\{([^}]+)\})', r'^\1' if not r'\2' else r'^\2', plain)
        plain = re.sub(r'_(\w+|\{([^}]+)\})', r'_\1' if not r'\2' else r'_\2', plain)
        
        # Remove braces
        plain = plain.replace('{', '').replace('}', '')
        
        return plain
    
    def _convert_to_unicode(self, latex: str) -> str:
        """Convert LaTeX ke Unicode mathematical symbols"""
        unicode_map = {
            '\\alpha': 'α',
            '\\beta': 'β',
            '\\gamma': 'γ',
            '\\delta': 'δ',
            '\\epsilon': 'ε',
            '\\theta': 'θ',
            '\\pi': 'π',
            '\\sigma': 'σ',
            '\\phi': 'φ',
            '\\omega': 'ω',
            '\\infty': '∞',
            '\\int': '∫',
            '\\sum': '∑',
            '\\prod': '∏',
            '\\sqrt': '√',
            '\\le': '≤',
            '\\ge': '≥',
            '\\ne': '≠',
            '\\pm': '±',
            '\\times': '×',
            '\\div': '÷'
        }
        
        unicode = latex
        for latex_cmd, unicode_char in unicode_map.items():
            unicode = unicode.replace(latex_cmd, unicode_char)
        
        # Remove remaining LaTeX commands
        unicode = re.sub(r'\\[a-zA-Z]+\{([^}]+)\}', r'\1', unicode)
        unicode = re.sub(r'\\[a-zA-Z]+', '', unicode)
        unicode = unicode.replace('{', '').replace('}', '')
        
        return unicode
    
    def _convert_to_sympy(self, latex: str) -> str:
        """Convert LaTeX ke SymPy-compatible format"""
        # SymPy uses specific syntax
        sympy = latex
        
        # Convert LaTeX fractions ke SymPy format
        sympy = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)', sympy)
        
        # Convert sqrt
        sympy = re.sub(r'\\sqrt\{([^}]+)\}', r'sqrt(\1)', sympy)
        
        # Remove LaTeX delimiters
        sympy = sympy.replace('$', '').replace('\\[', '').replace('\\]', '')
        
        return sympy
    
    def _extract_variables(self, latex: str) -> List[str]:
        """Extract variables dari LaTeX formula"""
        variables = []
        
        # Single letter variables (avoid LaTeX commands)
        var_pattern = re.compile(r'(?<!\\)\b([a-z])\b(?!\\w)')
        matches = var_pattern.findall(latex)
        
        for match in matches:
            if match not in variables and match not in ['e', 'i']:  # Exclude constants
                variables.append(match)
        
        return sorted(list(set(variables)))
    
    def _extract_functions(self, latex: str) -> List[str]:
        """Extract mathematical functions dari LaTeX formula"""
        functions = []
        
        function_patterns = [
            r'\\sin', r'\\cos', r'\\tan', r'\\cot',
            r'\\arcsin', r'\\arccos', r'\\arctan',
            r'\\sinh', r'\\cosh', r'\\tanh',
            r'\\log', r'\\ln', r'\\exp',
            r'\\sqrt', r'\\abs', r'\\max', r'\\min'
        ]
        
        for pattern in function_patterns:
            if re.search(pattern, latex):
                func_name = pattern.replace('\\', '')
                if func_name not in functions:
                    functions.append(func_name)
        
        return functions
    
    def _determine_complexity(self, latex: str) -> str:
        """Determine complexity level dari formula"""
        complexity_score = 0
        
        # Count operations
        if '+' in latex or '-' in latex:
            complexity_score += 1
        if '*' in latex or '/' in latex or '\\frac' in latex:
            complexity_score += 2
        if '^' in latex or '_ ' in latex:
            complexity_score += 2
        
        # Count functions
        function_count = len([f for f in ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt'] if f in latex])
        complexity_score += function_count
        
        # Count special operators
        special_count = len([s for s in ['\\int', '\\sum', '\\prod', '\\lim'] if s in latex])
        complexity_score += special_count * 3
        
        if complexity_score <= 2:
            return "simple"
        elif complexity_score <= 6:
            return "moderate"
        else:
            return "complex"
    
    def batch_process_formulas(
        self,
        formulas_data: List[Dict[str, Any]],
        options: Optional[FormulaProcessingOptions] = None
    ) -> List[ProcessedFormula]:
        """
        Process multiple formulas secara batch
        
        Args:
            formulas_data: List of formula data dictionaries
            options: Processing options (applied ke semua formulas)
        
        Returns:
            List of ProcessedFormula objects
        """
        results = []
        
        for idx, formula_data in enumerate(formulas_data):
            formula_id = formula_data.get('formula_id', f'formula_{idx}')
            try:
                processed_formula = self.process_formula(formula_data, formula_id, options)
                results.append(processed_formula)
            except Exception as e:
                logger.error(f"Error processing formula {formula_id}: {e}")
                continue
        
        logger.info(f"Batch processed {len(results)}/{len(formulas_data)} formulas")
        return results