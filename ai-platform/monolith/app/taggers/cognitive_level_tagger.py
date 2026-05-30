"""
Cognitive Level Tagger - Bloom's Taxonomy Cognitive Levels
Tags content with cognitive difficulty levels based on Bloom's taxonomy with confidence scores
"""
import re
import logging
from typing import Dict, Any, List, Optional
import sys
sys.path.append('/app')

# from common.utils.confidence_scorer import confidence_scorer  # Commented out - legacy import

# Simple confidence scorer implementation for monolith
def confidence_scorer(text: str, pattern: str) -> float:
    """Simple confidence scorer for monolith architecture"""
    if not text or not pattern:
        return 0.0
    if re.search(pattern, text, re.IGNORECASE):
        return 0.8
    return 0.0

logger = logging.getLogger(__name__)


class CognitiveLevelTagger:
    """Tag educational content with cognitive levels (Bloom's taxonomy)"""
    
    def __init__(self):
        """Initialize cognitive level tagger with Bloom's taxonomy patterns"""
        # Bloom's Taxonomy cognitive levels
        self.bloom_levels = {
            "C1 (Remembering)": [
                r"mengingat", r"mengenal", r"menyebutkan", r"mengidentifikasi",
                r"mendefinisikan", r"menyusun", r"menuliskan", r"mencatat"
            ],
            "C2 (Understanding)": [
                r"memahami", r"menjelaskan", r"menginterpretasi", r"merangkum",
                r"menyimpulkan", r"mengilustrasikan", r"menggambarkan", r"menguraikan"
            ],
            "C3 (Applying)": [
                r"menerapkan", r"menggunakan", r"melaksanakan", r"mengimplementasikan",
                r"menyelesaikan", r"menghitung", r"mendemonstrasikan", r"mengoperasikan"
            ],
            "C4 (Analyzing)": [
                r"menganalisis", r"membedakan", r"mengorganisasi", r"menghubungkan",
                r"membandingkan", r"mengkontras", r"memilah", r"mengkategorikan"
            ],
            "C5 (Evaluating)": [
                r"mengevaluasi", r"mengkritik", r"menilai", r"memeriksa",
                r"menghakimi", r"memutuskan", r"merekomendasikan", r"mengargumentasi"
            ],
            "C6 (Creating)": [
                r"membuat", r"merancang", r"mengkonstruksi", r"merencanakan",
                r"menghasilkan", r"mengkomposisikan", r"memformulasikan", r"menginovasi"
            ]
        }
        
        # Cognitive complexity indicators
        self.complexity_indicators = {
            "low_complexity": [
                r"mengenal", r"mengingat", r"menyebutkan", r"mengidentifikasi",
                r"mencatat", r"mendaftar"
            ],
            "medium_complexity": [
                r"memahami", r"menjelaskan", r"menerapkan", r"menggunakan",
                r"menghitung", r"melaksanakan"
            ],
            "high_complexity": [
                r"menganalisis", r"mengevaluasi", r"membuat", r"merancang",
                r"mengkritik", r"menginovasi", r"mensintesis"
            ]
        }
        
        logger.info("CognitiveLevelTagger initialized with Bloom's taxonomy patterns")
    
    def tag(self, content: str, target_levels: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Tag content with cognitive level information with confidence scores
        
        Args:
            content: Text content to tag
            target_levels: Target cognitive levels (optional)
            
        Returns:
            List of cognitive level tags with confidence scores
        """
        try:
            tags = []
            content_lower = content.lower()
            
            # Tag cognitive levels
            for level, patterns in self.bloom_levels.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower):
                        # Calculate proper confidence score
                        confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                            pattern, content, len(content)
                        )
                        
                        tags.append({
                            "type": "cognitive_level",
                            "level": level,
                            "pattern_matched": pattern,
                            "confidence": confidence_obj.score,
                            "confidence_level": confidence_obj.confidence_level,
                            "confidence_method": confidence_obj.method,
                            "confidence_metadata": confidence_obj.metadata,
                            "context": "bloom_taxonomy"
                        })
            
            # Tag complexity level
            for complexity, patterns in self.complexity_indicators.items():
                for pattern in patterns:
                    if re.search(pattern, content_lower):
                        # Calculate proper confidence score
                        confidence_obj = confidence_scorer.calculate_pattern_match_confidence(
                            pattern, content, len(content)
                        )
                        
                        tags.append({
                            "type": "complexity_level",
                            "complexity": complexity,
                            "pattern_matched": pattern,
                            "confidence": confidence_obj.score,
                            "confidence_level": confidence_obj.confidence_level,
                            "confidence_method": confidence_obj.method,
                            "confidence_metadata": confidence_obj.metadata,
                            "context": "cognitive_demand"
                        })
            
            # Add target levels if provided
            if target_levels:
                confidence_obj = confidence_scorer.calculate_classifier_confidence(
                    prediction="target_levels",
                    probability=0.95,  # High confidence if explicitly provided
                    model_confidence=0.9
                )
                
                tags.append({
                    "type": "target_levels",
                    "target_levels": target_levels,
                    "confidence": confidence_obj.score,
                    "confidence_level": confidence_obj.confidence_level,
                    "confidence_method": confidence_obj.method,
                    "confidence_metadata": confidence_obj.metadata,
                    "context": "learning_objectives"
                })
            
            # Calculate dominant cognitive level
            if tags:
                cognitive_tags = [tag for tag in tags if tag["type"] == "cognitive_level"]
                if cognitive_tags:
                    # Count occurrences of each level
                    level_counts = {}
                    for tag in cognitive_tags:
                        level = tag["level"]
                        level_counts[level] = level_counts.get(level, 0) + 1
                    
                    # Find most frequent level
                    dominant_level = max(level_counts, key=level_counts.get)
                    
                    # Calculate ensemble confidence based on all cognitive level tags
                    confidence_scores = [tag["confidence"] for tag in cognitive_tags if tag["level"] == dominant_level]
                    if confidence_scores:
                        ensemble_confidence = confidence_scorer.calculate_ensemble_confidence(confidence_scores)
                        
                        tags.append({
                            "type": "dominant_cognitive_level",
                            "dominant_level": dominant_level,
                            "count": level_counts[dominant_level],
                            "confidence": ensemble_confidence.score,
                            "confidence_level": ensemble_confidence.confidence_level,
                            "confidence_method": ensemble_confidence.method,
                            "confidence_metadata": ensemble_confidence.metadata,
                            "context": "cognitive_analysis"
                        })
            
            logger.info(f"Tagged content with {len(tags)} cognitive level tags using confidence scoring")
            return tags
            
        except Exception as e:
            logger.error(f"Error in cognitive level tagging: {str(e)}")
            return []