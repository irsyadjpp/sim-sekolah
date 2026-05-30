"""
Text Extraction Helper
Helper class for extracting text content from parsed documents
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class TextExtractionHelper:
    """Helper class for text extraction operations"""
    
    def extract_text_content(self, parsed_document: Dict[str, Any]) -> str:
        """Extract text content from parsed document"""
        # Handle different document structures
        if 'text_content' in parsed_document:
            content = parsed_document['text_content']
            # If it's a list of page objects, join them
            if isinstance(content, list):
                text_parts = []
                for item in content:
                    if isinstance(item, dict) and 'text' in item:
                        text_parts.append(item['text'])
                    elif isinstance(item, str):
                        text_parts.append(item)
                return ' '.join(text_parts)
            # If it's already a string, return it
            elif isinstance(content, str):
                return content
            # Otherwise convert to string
            else:
                return str(content)
        elif 'pages' in parsed_document:
            # Extract text from pages
            text_parts = []
            for page in parsed_document['pages']:
                if isinstance(page, dict) and 'text' in page:
                    text_parts.append(page['text'])
                elif isinstance(page, dict) and 'regions' in page:
                    # Extract from regions
                    for region in page['regions']:
                        if isinstance(region, dict) and 'content' in region:
                            text_parts.append(region['content'])
            return ' '.join(text_parts)
        elif 'content' in parsed_document:
            content = parsed_document['content']
            if isinstance(content, list):
                return ' '.join([str(item) for item in content])
            return str(content)
        else:
            return ""