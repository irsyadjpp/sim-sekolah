import re
import logging
from typing import Dict, Any, List
import uuid

logger = logging.getLogger(__name__)


class HierarchyDetector:
    """Detect document hierarchy structure (headings, sections, subsections)"""
    
    def __init__(self):
        """Initialize hierarchy detector"""
        self.heading_patterns = [
            r'^(#{1,6})\s+(.+)$',  # Markdown headings
            r'^([A-Z][A-Z\s]+)\s*$',  # ALL CAPS headings
            r'^[IVX]+\.\s+(.+)$',  # Roman numeral headings
            r'^\d+\.\s+(.+)$',  # Numbered headings
        ]
        logger.info("Hierarchy detector initialized")
    
    def detect(self, text: str) -> Dict[str, Any]:
        """Detect hierarchy structure in text"""
        try:
            lines = text.split('\n')
            
            structure = {
                'levels': [],
                'sections': [],
                'depth': 0
            }
            
            current_level = 0
            current_sections = []
            
            for line_num, line in enumerate(lines):
                heading_info = self._detect_heading(line)
                
                if heading_info:
                    structure['sections'].append({
                        'level': heading_info['level'],
                        'title': heading_info['title'],
                        'line_number': line_num,
                        'content': ''
                    })
                    
                    structure['depth'] = max(structure['depth'], heading_info['level'])
            
            logger.info(f"Detected hierarchy with {structure['depth']} levels, {len(structure['sections'])} sections")
            
            return structure
            
        except Exception as e:
            logger.error(f"Error detecting hierarchy: {str(e)}")
            return {'levels': [], 'sections': [], 'depth': 0, 'error': str(e)}
    
    def _detect_heading(self, line: str) -> Dict[str, Any]:
        """Detect if line is a heading and extract level"""
        # Check for markdown headings
        markdown_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if markdown_match:
            return {
                'level': len(markdown_match.group(1)),
                'title': markdown_match.group(2).strip()
            }
        
        # Check for ALL CAPS heading
        if line.isupper() and len(line) < 100 and len(line.split()) <= 5:
            return {
                'level': 1,
                'title': line.strip()
            }
        
        # Check for numbered heading
        numbered_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if numbered_match and len(numbered_match.group(2).split()) <= 10:
            return {
                'level': 2,
                'title': numbered_match.group(2).strip()
            }
        
        return None