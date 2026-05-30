"""
Chunk Quality Calculator
Helper class for calculating chunk quality scores and educational values
"""
import logging
from typing import Dict, Any
from app.models.chunk_types import EducationalChunkType, BloomLevel

logger = logging.getLogger(__name__)


class ChunkQualityCalculator:
    """Helper class for calculating chunk quality metrics"""
    
    def calculate_quality_score(self, text: str, chunk_type: EducationalChunkType) -> float:
        """Calculate quality score based on text characteristics and chunk type"""
        quality_score = 0.5  # Base score
        
        # Length factor
        text_length = len(text)
        if 50 <= text_length <= 500:
            quality_score += 0.2
        elif 500 < text_length <= 1000:
            quality_score += 0.1
        elif text_length > 1000:
            quality_score -= 0.1
        
        # Chunk type factor
        if chunk_type in [EducationalChunkType.COMPETENCY, EducationalChunkType.ACTIVITY]:
            quality_score += 0.2
        elif chunk_type == EducationalChunkType.ASSESSMENT:
            quality_score += 0.15
        elif chunk_type == EducationalChunkType.LESSON_PLAN:
            quality_score += 0.1
        
        # Text completeness factor
        if text.strip() and len(text.split()) > 3:
            quality_score += 0.1
        
        return min(quality_score, 1.0)
    
    def calculate_educational_value(self, chunk_type: EducationalChunkType, 
                                   bloom_level: BloomLevel) -> float:
        """Calculate educational value based on chunk type and Bloom level"""
        base_value = 0.5
        
        # Chunk type contribution
        type_values = {
            EducationalChunkType.COMPETENCY: 0.9,
            EducationalChunkType.ACTIVITY: 0.8,
            EducationalChunkType.ASSESSMENT: 0.85,
            EducationalChunkType.LESSON_PLAN: 0.75,
            EducationalChunkType.INQUIRY: 0.7,
            EducationalChunkType.CONCEPT: 0.65,
            EducationalChunkType.EXAMPLE: 0.5,
            EducationalChunkType.REFERENCE: 0.3
        }
        
        base_value = type_values.get(chunk_type, 0.5)
        
        # Bloom level contribution (higher is better for educational value)
        bloom_values = {
            BloomLevel.C6_CREATE: 0.9,
            BloomLevel.C5_EVALUATE: 0.85,
            BloomLevel.C4_ANALYZE: 0.8,
            BloomLevel.C3_APPLY: 0.75,
            BloomLevel.C2_UNDERSTAND: 0.6,
            BloomLevel.C1_REMEMBER: 0.5,
            BloomLevel.UNKNOWN: 0.4
        }
        
        bloom_contribution = bloom_values.get(bloom_level, 0.5)
        
        return (base_value * 0.6) + (bloom_contribution * 0.4)