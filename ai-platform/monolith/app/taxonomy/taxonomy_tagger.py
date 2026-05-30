import re
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class TaxonomyTagger:
    """
    Tag text with Indonesian curriculum taxonomy and Bloom's taxonomy cognitive levels
    Updated to match legacy API signature for compatibility
    """
    
    def __init__(self):
        """Initialize taxonomy tagger with Indonesian curriculum taxonomy"""
        
        # Indonesian Kurikulum Merdeka taxonomy
        self.curriculum_taxonomy = {
            "CP": {  # Capaian Pembelajaran
                "patterns": [r"capaian pembelajaran", r"cp", r"capaian"],
                "description": "Learning Achievement"
            },
            "TP": {  # Tujuan Pembelajaran  
                "patterns": [r"tujuan pembelajaran", r"tp", r"tujuan"],
                "description": "Learning Objectives"
            },
            "ATP": {  # Alur Tujuan Pembelajaran
                "patterns": [r"alur tujuan pembelajaran", r"atp", r"alur"],
                "description": "Learning Objectives Flow"
            },
            "AKM": {  # Asesmen Kompetensi Minimum
                "patterns": [r"asesmen kompetensi minimum", r"akm", r"kompetensi minimum"],
                "description": "Minimum Competency Assessment"
            }
        }
        
        # Subject taxonomy (canonical forms)
        self.subject_taxonomy = {
            "Matematika": {
                "canonical": "Matematika",
                "aliases": ["Math", "Matematik", "Mtk", "Mathematics"],
                "code": "SUBJ-MAT"
            },
            "Bahasa Indonesia": {
                "canonical": "Bahasa Indonesia",
                "aliases": ["Indonesian", "Bahasa", "BI"],
                "code": "SUBJ-BIN"
            },
            "IPA": {
                "canonical": "Ilmu Pengetahuan Alam",
                "aliases": ["Science", "Sains", "IPA"],
                "code": "SUBJ-IPA"
            },
            "IPS": {
                "canonical": "Ilmu Pengetahuan Sosial",
                "aliases": ["Social Studies", "IPS", "Sosial"],
                "code": "SUBJ-IPS"
            },
            "PJOK": {
                "canonical": "Pendidikan Jasmani, Olahraga, dan Kesehatan",
                "aliases": ["Physical Education", "PJOK", "Olahraga"],
                "code": "SUBJ-PJOK"
            },
            "Seni Budaya": {
                "canonical": "Seni Budaya",
                "aliases": ["Arts", "Seni", "Culture"],
                "code": "SUBJ-SBU"
            },
            "Bahasa Inggris": {
                "canonical": "Bahasa Inggris",
                "aliases": ["English", "Inggris"],
                "code": "SUBJ-BIG"
            }
        }
        
        # Bloom's taxonomy cognitive levels
        self.bloom_taxonomy = {
            'remembering': [
                'mengingat', 'menyebut', 'mengenali', 'menyebut', 'menghafal',
                'recall', 'define', 'identify', 'list', 'state'
            ],
            'understanding': [
                'memahami', 'menjelaskan', 'menguraikan', 'menginterpretasi',
                'understand', 'explain', 'describe', 'discuss', 'interpret'
            ],
            'applying': [
                'menerapkan', 'menggunakan', 'mengaplikasikan', 'menjalankan',
                'apply', 'use', 'implement', 'execute', 'operate'
            ],
            'analyzing': [
                'menganalisis', 'membandingkan', 'mengorganisir', 'menghubungkan',
                'analyze', 'compare', 'organize', 'connect', 'differentiate'
            ],
            'evaluating': [
                'menilai', 'memeriksa', 'mengkaji', 'menganggap',
                'evaluate', 'assess', 'examine', 'critique', 'judge'
            ],
            'creating': [
                'membuat', 'mencipta', 'merancang', 'mengkonstruksi',
                'create', 'design', 'construct', 'produce', 'develop'
            ]
        }
        
        logger.info("TaxonomyTagger initialized with Indonesian curriculum taxonomy and Bloom's taxonomy")
    
    def tag(self, content: str, subject: str = 'general', grade: str = 'unknown') -> Dict[str, Any]:
        """
        Tag content with taxonomy information (updated API signature)
        
        Args:
            content: Text content to tag
            subject: Subject (for canonical normalization)
            grade: Grade level
            
        Returns:
            List of taxonomy tags with canonical forms
        """
        try:
            tags = []
            content_lower = content.lower()
            
            # Tag curriculum standards
            curriculum_tags = self._tag_curriculum_standards(content_lower)
            tags.extend(curriculum_tags)
            
            # Tag subjects (with canonical normalization)
            subject_tags = self._tag_subjects(content_lower, subject)
            tags.extend(subject_tags)
            
            # Tag grade levels
            grade_tags = self._tag_grade_levels(content_lower, grade)
            tags.extend(grade_tags)
            
            # Tag Bloom's cognitive levels
            bloom_tags = self._tag_bloom_taxonomy(content_lower)
            tags.extend(bloom_tags)
            
            logger.info(f"Taxonomy tagging completed: {len(tags)} tags")
            return tags
            
        except Exception as e:
            logger.error(f"Error in taxonomy tagging: {str(e)}")
            return []
    
    def _tag_curriculum_standards(self, content_lower: str) -> List[Dict[str, Any]]:
        """Tag content with curriculum standards"""
        tags = []
        
        for standard_name, standard_info in self.curriculum_taxonomy.items():
            for pattern in standard_info["patterns"]:
                if re.search(pattern, content_lower):
                    tags.append({
                        "type": "curriculum_standard",
                        "canonical": standard_name,
                        "description": standard_info["description"],
                        "confidence": 0.85,
                        "pattern_matched": pattern
                    })
                    break  # Only tag once per standard
        
        return tags
    
    def _tag_subjects(self, content_lower: str, subject: str) -> List[Dict[str, Any]]:
        """Tag content with subject taxonomy (with canonical normalization)"""
        tags = []
        
        # First, use provided subject if available
        if subject and subject != 'general':
            canonical_subject = self._normalize_subject(subject)
            if canonical_subject:
                tags.append({
                    "type": "subject",
                    "canonical": canonical_subject,
                    "original": subject,
                    "confidence": 0.95,
                    "source": "context"
                })
                return tags  # Trust context over content analysis
        
        # Otherwise, analyze content
        for canonical_name, subject_info in self.subject_taxonomy.items():
            for alias in subject_info["aliases"]:
                if alias.lower() in content_lower:
                    tags.append({
                        "type": "subject",
                        "canonical": canonical_name,
                        "original": alias,
                        "confidence": 0.75,
                        "source": "content_analysis"
                    })
                    break  # Only tag once per subject
        
        return tags
    
    def _tag_grade_levels(self, content_lower: str, grade: str) -> List[Dict[str, Any]]:
        """Tag content with grade levels"""
        tags = []
        
        # First, use provided grade if available
        if grade and grade != 'unknown':
            tags.append({
                "type": "grade_level",
                "canonical": f"Kelas {grade}",
                "original": grade,
                "confidence": 0.95,
                "source": "context"
            })
            return tags
        
        # Otherwise, analyze content for grade patterns
        grade_patterns = {
            "Kelas 1": r'\bkelas\s*1\b',
            "Kelas 2": r'\bkelas\s*2\b',
            "Kelas 3": r'\bkelas\s*3\b',
            "Kelas 4": r'\bkelas\s*4\b',
            "Kelas 5": r'\bkelas\s*5\b',
            "Kelas 6": r'\bkelas\s*6\b',
            "SD": r'\bsd\b',
            "SMP": r'\bsmp\b',
            "SMA": r'\bsma\b'
        }
        
        for grade_name, pattern in grade_patterns.items():
            if re.search(pattern, content_lower, re.IGNORECASE):
                tags.append({
                    "type": "grade_level",
                    "canonical": grade_name,
                    "confidence": 0.7,
                    "source": "content_analysis"
                })
        
        return tags
    
    def _tag_bloom_taxonomy(self, content_lower: str) -> List[Dict[str, Any]]:
        """Tag content with Bloom's taxonomy cognitive levels"""
        tags = []
        
        # Score each cognitive level
        level_scores = {}
        for level, verbs in self.bloom_taxonomy.items():
            score = sum(1 for verb in verbs if verb in content_lower)
            level_scores[level] = score
        
        # Find dominant level
        if level_scores:
            dominant_level = max(level_scores, key=level_scores.get)
            confidence = level_scores[dominant_level] / len(content_lower.split()) if content_lower.split() else 0
        else:
            dominant_level = 'understanding'  # Default level
            confidence = 0.5
        
        # Get all detected levels
        detected_levels = [
            level for level, score in level_scores.items() if score > 0
        ]
        
        if detected_levels:
            tags.append({
                "type": "bloom_taxonomy",
                "levels": detected_levels,
                "dominant_level": dominant_level,
                "confidence": min(confidence, 1.0),
                "level_scores": level_scores
            })
        
        return tags
    
    def _normalize_subject(self, subject: str) -> Optional[str]:
        """Normalize subject to canonical form"""
        subject_lower = subject.lower().strip()
        
        for canonical_name, subject_info in self.subject_taxonomy.items():
            if canonical_name.lower() == subject_lower:
                return canonical_name
            
            for alias in subject_info["aliases"]:
                if alias.lower() == subject_lower:
                    return canonical_name
        
        return None
    
    # Maintain backward compatibility with old method
    def classify_question(self, question: str) -> str:
        """Classify a question into Bloom's taxonomy level (deprecated, kept for compatibility)"""
        try:
            content_lower = question.lower()
            
            level_scores = {}
            for level, verbs in self.bloom_taxonomy.items():
                score = sum(1 for verb in verbs if verb in content_lower)
                level_scores[level] = score
            
            if level_scores:
                return max(level_scores, key=level_scores.get)
            return 'understanding'
        except Exception as e:
            logger.error(f"Error classifying question: {str(e)}")
            return 'understanding'