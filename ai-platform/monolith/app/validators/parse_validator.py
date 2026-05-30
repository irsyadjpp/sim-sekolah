"""
Parse Validator untuk Parser Service
Validasi kualitas dan integritas hasil parsing
Ensures output meets quality standards before downstream processing
"""
import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re

logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Severity level validation issues"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationCategory(Enum):
    """Category untuk validation checks"""
    STRUCTURE = "structure"           # Document structure integrity
    CONTENT = "content"               # Content quality dan completeness
    FORMATTING = "formatting"         # Formatting preservation
    METADATA = "metadata"             # Metadata completeness
    CONSISTENCY = "consistency"       # Consistency across elements
    ACCESSIBILITY = "accessibility"   # Accessibility compliance
    PERFORMANCE = "performance"       # Performance metrics


@dataclass
class ValidationIssue:
    """Individual validation issue"""
    category: ValidationCategory
    severity: ValidationSeverity
    element_id: str                   # ID of problematic element
    element_type: str                 # Type of element (text, table, image, etc.)
    issue_code: str                   # Unique code untuk issue
    description: str                  # Human-readable description
    suggestion: str = ""              # Suggested fix
    confidence: float = 0.0           # Confidence dalam issue detection
    context: Dict[str, Any] = field(default_factory=dict)  # Additional context


@dataclass
class ValidationResult:
    """Hasil validasi parsing result"""
    doc_id: str
    validation_passed: bool
    overall_quality_score: float      # 0.0 to 1.0
    issues: List[ValidationIssue] = field(default_factory=list)
    statistics: Dict[str, int] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    
    # Categorized issue counts
    critical_count: int = 0
    error_count: int = 0
    warning_count: int = 0
    info_count: int = 0
    
    # Element-specific quality scores
    text_quality_score: float = 0.0
    table_quality_score: float = 0.0
    image_quality_score: float = 0.0
    metadata_quality_score: float = 0.0
    
    # Validation metadata
    validation_timestamp: str = ""
    validation_method: str = "automated"
    
    def add_issue(self, issue: ValidationIssue):
        """Add validation issue ke result"""
        self.issues.append(issue)
        if issue.severity == ValidationSeverity.CRITICAL:
            self.critical_count += 1
        elif issue.severity == ValidationSeverity.ERROR:
            self.error_count += 1
        elif issue.severity == ValidationSeverity.WARNING:
            self.warning_count += 1
        elif issue.severity == ValidationSeverity.INFO:
            self.info_count += 1


class ParseValidator:
    """
    Validator untuk parsing results
    
    Melakukan validasi pada:
    - Structure integrity (headers, hierarchy, page numbering)
    - Content quality (completeness, encoding, formatting)
    - Element-specific quality (tables, images, formulas)
    - Metadata completeness
    - Consistency across elements
    - Accessibility compliance
    """
    
    def __init__(
        self,
        strict_mode: bool = False,
        min_quality_threshold: float = 0.7,
        enable_accessibility_checks: bool = True
    ):
        """
        Initialize Parse Validator
        
        Args:
            strict_mode: Treat warnings sebagai errors
            min_quality_threshold: Minimum acceptable quality score
            enable_accessibility_checks: Enable accessibility compliance checks
        """
        self.strict_mode = strict_mode
        self.min_quality_threshold = min_quality_threshold
        self.enable_accessibility_checks = enable_accessibility_checks
        
        # Validation thresholds
        self.thresholds = {
            'min_text_length': 10,
            'max_text_length': 10000,
            'min_table_rows': 1,
            'min_table_cols': 1,
            'min_image_size': 100,  # bytes
            'min_caption_length': 5,
            'max_caption_length': 500,
            'required_metadata_fields': ['doc_id', 'title', 'author']
        }
        
        logger.info("ParseValidator initialized with quality validation")
    
    def validate_parse_result(
        self,
        parse_result: Dict[str, Any],
        doc_id: str
    ) -> ValidationResult:
        """
        Validate complete parsing result
        
        Args:
            parse_result: Complete parsing result dictionary
            doc_id: Document ID
        
        Returns:
            ValidationResult dengan all issues dan scores
        """
        result = ValidationResult(
            doc_id=doc_id,
            validation_passed=True,
            validation_method="automated"
        )
        
        try:
            # Validate structure
            self._validate_structure(parse_result, result)
            
            # Validate text content
            self._validate_text_content(parse_result, result)
            
            # Validate tables
            self._validate_tables(parse_result, result)
            
            # Validate images
            self._validate_images(parse_result, result)
            
            # Validate metadata
            self._validate_metadata(parse_result, result)
            
            # Validate consistency
            self._validate_consistency(parse_result, result)
            
            # Validate accessibility if enabled
            if self.enable_accessibility_checks:
                self._validate_accessibility(parse_result, result)
            
            # Calculate overall quality score
            result.overall_quality_score = self._calculate_overall_quality(result)
            
            # Determine if validation passed
            result.validation_passed = self._determine_validation_passed(result)
            
            # Generate recommendations
            result.recommendations = self._generate_recommendations(result)
            
            # Update statistics
            result.statistics = {
                'total_issues': len(result.issues),
                'critical': result.critical_count,
                'error': result.error_count,
                'warning': result.warning_count,
                'info': result.info_count
            }
            
            logger.info(
                f"Validation completed for {doc_id}: "
                f"passed={result.validation_passed}, "
                f"quality_score={result.overall_quality_score:.2f}, "
                f"issues={len(result.issues)}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error validating parse result for {doc_id}: {e}")
            result.add_issue(ValidationIssue(
                category=ValidationCategory.STRUCTURE,
                severity=ValidationSeverity.CRITICAL,
                element_id="system",
                element_type="system",
                issue_code="VALIDATION_ERROR",
                description=f"Validation system error: {str(e)}",
                confidence=1.0
            ))
            result.validation_passed = False
            return result
    
    def _validate_structure(self, parse_result: Dict[str, Any], result: ValidationResult):
        """Validate document structure"""
        # Check jika result has required keys
        required_keys = ['text_chunks', 'metadata']
        for key in required_keys:
            if key not in parse_result:
                result.add_issue(ValidationIssue(
                    category=ValidationCategory.STRUCTURE,
                    severity=ValidationSeverity.ERROR,
                    element_id="document",
                    element_type="structure",
                    issue_code="MISSING_KEY",
                    description=f"Required key '{key}' missing dari parse result",
                    suggestion="Ensure parser includes all required keys",
                    confidence=1.0
                ))
        
        # Validate page numbering
        if 'text_chunks' in parse_result:
            page_numbers = [chunk.get('page_number', 0) for chunk in parse_result['text_chunks']]
            if page_numbers and len(set(page_numbers)) < len(page_numbers) * 0.5:
                result.add_issue(ValidationIssue(
                    category=ValidationCategory.STRUCTURE,
                    severity=ValidationSeverity.WARNING,
                    element_id="document",
                    element_type="page_structure",
                    issue_code="DUPLICATE_PAGE_NUMBERS",
                    description="Many duplicate page numbers detected",
                    suggestion="Check page numbering logic in parser",
                    confidence=0.8
                ))
    
    def _validate_text_content(self, parse_result: Dict[str, Any], result: ValidationResult):
        """Validate text content quality"""
        if 'text_chunks' not in parse_result:
            return
        
        text_chunks = parse_result['text_chunks']
        total_text_length = 0
        empty_chunks = 0
        very_short_chunks = 0
        encoding_issues = 0
        
        for i, chunk in enumerate(text_chunks):
            content = chunk.get('content', '')
            chunk_id = chunk.get('chunk_id', f"text_{i}")
            
            total_text_length += len(content)
            
            # Check untuk empty chunks
            if not content or content.strip() == "":
                empty_chunks += 1
                result.add_issue(ValidationIssue(
                    category=ValidationCategory.CONTENT,
                    severity=ValidationSeverity.WARNING,
                    element_id=chunk_id,
                    element_type="text_chunk",
                    issue_code="EMPTY_CHUNK",
                    description="Text chunk is empty or whitespace only",
                    suggestion="Filter out empty chunks atau investigate parsing issue",
                    confidence=1.0
                ))
            
            # Check untuk very short chunks (might be noise)
            elif len(content) < self.thresholds['min_text_length']:
                very_short_chunks += 1
                result.add_issue(ValidationIssue(
                    category=ValidationCategory.CONTENT,
                    severity=ValidationSeverity.INFO,
                    element_id=chunk_id,
                    element_type="text_chunk",
                    issue_code="SHORT_CHUNK",
                    description=f"Text chunk is very short ({len(content)} chars)",
                    suggestion="Consider if this is intentional noise",
                    confidence=0.7
                ))
            
            # Check untuk encoding issues
            if self._has_encoding_issues(content):
                encoding_issues += 1
                result.add_issue(ValidationIssue(
                    category=ValidationCategory.CONTENT,
                    severity=ValidationSeverity.ERROR,
                    element_id=chunk_id,
                    element_type="text_chunk",
                    issue_code="ENCODING_ISSUE",
                    description="Text has potential encoding issues",
                    suggestion="Check character encoding in source document",
                    confidence=0.9
                ))
        
        # Calculate text quality score
        total_chunks = len(text_chunks)
        if total_chunks > 0:
            quality = 1.0 - (empty_chunks / total_chunks) - (encoding_issues / total_chunks) * 0.5
            result.text_quality_score = max(0.0, min(1.0, quality))
        else:
            result.text_quality_score = 0.0
    
    def _validate_tables(self, parse_result: Dict[str, Any], result: ValidationResult):
        """Validate table extraction quality"""
        if 'table_chunks' not in parse_result:
            return
        
        tables = parse_result['table_chunks']
        empty_tables = 0
        malformed_tables = 0
        
        for i, table in enumerate(tables):
            table_id = table.get('chunk_id', f"table_{i}")
            headers = table.get('headers', [])
            rows = table.get('rows', [])
            
            # Check untuk empty tables
            if not headers and not rows:
                empty_tables += 1
                result.add_issue(ValidationIssue(
                    category=ValidationCategory.CONTENT,
                    severity=ValidationSeverity.WARNING,
                    element_id=table_id,
                    element_type="table",
                    issue_code="EMPTY_TABLE",
                    description="Table has no headers or rows",
                    suggestion="Verify table extraction logic",
                    confidence=1.0
                ))
                continue
            
            # Check untuk inconsistent column counts
            if headers and rows:
                expected_cols = len(headers)
                inconsistent_rows = 0
                for row in rows:
                    if len(row) != expected_cols:
                        inconsistent_rows += 1
                
                if inconsistent_rows > len(rows) * 0.3:
                    malformed_tables += 1
                    result.add_issue(ValidationIssue(
                        category=ValidationCategory.STRUCTURE,
                        severity=ValidationSeverity.WARNING,
                        element_id=table_id,
                        element_type="table",
                        issue_code="INCONSISTENT_COLS",
                        description=f"Many rows ({inconsistent_rows}/{len(rows)}) have wrong column count",
                        suggestion="Check table parsing for merged cells or complex structures",
                        confidence=0.8
                    ))
        
        # Calculate table quality score
        total_tables = len(tables)
        if total_tables > 0:
            quality = 1.0 - (empty_tables / total_tables) - (malformed_tables / total_tables) * 0.3
            result.table_quality_score = max(0.0, min(1.0, quality))
        else:
            result.table_quality_score = 1.0  # No tables is OK
    
    def _validate_images(self, parse_result: Dict[str, Any], result: ValidationResult):
        """Validate image extraction quality"""
        if 'image_chunks' not in parse_result:
            return
        
        images = parse_result['image_chunks']
        missing_data = 0
        missing_type = 0
        missing_caption = 0
        
        for i, image in enumerate(images):
            image_id = image.get('chunk_id', f"image_{i}")
            image_data = image.get('image_data')
            image_type = image.get('image_type')
            
            # Check untuk missing image data
            if not image_data:
                missing_data += 1
                result.add_issue(ValidationIssue(
                    category=ValidationCategory.CONTENT,
                    severity=ValidationSeverity.ERROR,
                    element_id=image_id,
                    element_type="image",
                    issue_code="MISSING_IMAGE_DATA",
                    description="Image chunk has no binary data",
                    suggestion="Check image extraction logic",
                    confidence=1.0
                ))
            
            # Check untuk missing image type
            if not image_type:
                missing_type += 1
                result.add_issue(ValidationIssue(
                    category=ValidationCategory.METADATA,
                    severity=ValidationSeverity.WARNING,
                    element_id=image_id,
                    element_type="image",
                    issue_code="MISSING_IMAGE_TYPE",
                    description="Image chunk has no type specified",
                    suggestion="Include image type metadata",
                    confidence=0.8
                ))
        
        # Calculate image quality score
        total_images = len(images)
        if total_images > 0:
            quality = 1.0 - (missing_data / total_images) - (missing_type / total_images) * 0.2
            result.image_quality_score = max(0.0, min(1.0, quality))
        else:
            result.image_quality_score = 1.0  # No images is OK
    
    def _validate_metadata(self, parse_result: Dict[str, Any], result: ValidationResult):
        """Validate metadata completeness"""
        if 'metadata' not in parse_result:
            result.add_issue(ValidationIssue(
                category=ValidationCategory.METADATA,
                severity=ValidationSeverity.ERROR,
                element_id="document",
                element_type="metadata",
                issue_code="MISSING_METADATA",
                description="No metadata found in parse result",
                suggestion="Include basic document metadata",
                confidence=1.0
            ))
            result.metadata_quality_score = 0.0
            return
        
        metadata = parse_result['metadata']
        missing_fields = []
        
        # Check untuk required metadata fields
        for field in self.thresholds['required_metadata_fields']:
            if field not in metadata or not metadata[field]:
                missing_fields.append(field)
                result.add_issue(ValidationIssue(
                    category=ValidationCategory.METADATA,
                    severity=ValidationSeverity.WARNING,
                    element_id="document",
                    element_type="metadata",
                    issue_code="MISSING_METADATA_FIELD",
                    description=f"Required metadata field '{field}' is missing or empty",
                    suggestion=f"Include {field} dalam document metadata",
                    confidence=0.9
                ))
        
        # Calculate metadata quality score
        total_required = len(self.thresholds['required_metadata_fields'])
        if total_required > 0:
            quality = 1.0 - (len(missing_fields) / total_required)
            result.metadata_quality_score = max(0.0, min(1.0, quality))
        else:
            result.metadata_quality_score = 1.0
    
    def _validate_consistency(self, parse_result: Dict[str, Any], result: ValidationResult):
        """Validate consistency across elements"""
        # Check page number consistency
        all_elements = []
        
        if 'text_chunks' in parse_result:
            all_elements.extend(parse_result['text_chunks'])
        if 'table_chunks' in parse_result:
            all_elements.extend(parse_result['table_chunks'])
        if 'image_chunks' in parse_result:
            all_elements.extend(parse_result['image_chunks'])
        
        page_numbers = [elem.get('page_number', 0) for elem in all_elements]
        if page_numbers:
            min_page = min(page_numbers)
            max_page = max(page_numbers)
            
            if min_page < 0 or max_page < 0:
                result.add_issue(ValidationIssue(
                    category=ValidationCategory.CONSISTENCY,
                    severity=ValidationSeverity.ERROR,
                    element_id="document",
                    element_type="page_structure",
                    issue_code="INVALID_PAGE_NUMBERS",
                    description=f"Invalid page numbers detected (min: {min_page}, max: {max_page})",
                    suggestion="Check page numbering logic",
                    confidence=1.0
                ))
    
    def _validate_accessibility(self, parse_result: Dict[str, Any], result: ValidationResult):
        """Validate accessibility compliance"""
        # Check untuk image alt text
        if 'image_chunks' in parse_result:
            for image in parse_result['image_chunks']:
                image_id = image.get('chunk_id', 'unknown')
                metadata = image.get('metadata', {})
                
                if not metadata.get('alt_text'):
                    result.add_issue(ValidationIssue(
                        category=ValidationCategory.ACCESSIBILITY,
                        severity=ValidationSeverity.WARNING,
                        element_id=image_id,
                        element_type="image",
                        issue_code="MISSING_ALT_TEXT",
                        description="Image is missing alt text for accessibility",
                        suggestion="Include descriptive alt text untuk images",
                        confidence=0.8
                    ))
        
        # Check untuk proper heading structure
        if 'text_chunks' in parse_result:
            for chunk in parse_result['text_chunks']:
                content = chunk.get('content', '')
                if content.startswith('#'):
                    # Check heading hierarchy
                    heading_level = len(re.match(r'^#+', content).group())
                    if heading_level > 6:
                        result.add_issue(ValidationIssue(
                            category=ValidationCategory.ACCESSIBILITY,
                            severity=ValidationSeverity.INFO,
                            element_id=chunk.get('chunk_id', 'unknown'),
                            element_type="text",
                            issue_code="INVALID_HEADING_LEVEL",
                            description=f"Heading level {heading_level} exceeds HTML standard (max 6)",
                            suggestion="Use heading levels 1-6 for proper hierarchy",
                            confidence=0.9
                        ))
    
    def _calculate_overall_quality(self, result: ValidationResult) -> float:
        """Calculate overall quality score from component scores"""
        weights = {
            'text': 0.4,
            'table': 0.2,
            'image': 0.2,
            'metadata': 0.2
        }
        
        overall_score = (
            result.text_quality_score * weights['text'] +
            result.table_quality_score * weights['table'] +
            result.image_quality_score * weights['image'] +
            result.metadata_quality_score * weights['metadata']
        )
        
        # Penalize untuk critical dan error issues
        severity_penalty = (result.critical_count * 0.3) + (result.error_count * 0.1)
        overall_score = max(0.0, overall_score - severity_penalty)
        
        return overall_score
    
    def _determine_validation_passed(self, result: ValidationResult) -> bool:
        """Determine jika validation passed based on criteria"""
        if result.critical_count > 0:
            return False
        
        if self.strict_mode and result.error_count > 0:
            return False
        
        if result.overall_quality_score < self.min_quality_threshold:
            return False
        
        return True
    
    def _generate_recommendations(self, result: ValidationResult) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        if result.text_quality_score < 0.8:
            recommendations.append("Review text extraction untuk encoding issues dan empty chunks")
        
        if result.table_quality_score < 0.8:
            recommendations.append("Improve table extraction untuk better column consistency")
        
        if result.image_quality_score < 0.8:
            recommendations.append("Verify image extraction untuk missing data and metadata")
        
        if result.metadata_quality_score < 0.8:
            recommendations.append("Ensure complete metadata extraction dengan required fields")
        
        if result.critical_count > 0:
            recommendations.append("Address critical validation issues before proceeding")
        
        if result.error_count > 5:
            recommendations.append("Multiple errors detected - consider reviewing parser configuration")
        
        if not recommendations:
            recommendations.append("Parsing quality is acceptable - no major issues detected")
        
        return recommendations
    
    def _has_encoding_issues(self, text: str) -> bool:
        """Check jika text has encoding issues"""
        # Check untuk common encoding problem characters
        encoding_indicators = ['\ufffd', '\u0000', '\u0001', '\u0002']
        return any(char in text for char in encoding_indicators)