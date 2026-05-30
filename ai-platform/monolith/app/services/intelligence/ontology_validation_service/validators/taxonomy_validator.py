"""
Taxonomy Validator
Validates taxonomy terms against Bloom's Taxonomy and Indonesian curriculum standards
"""
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class TaxonomyValidator:
    """Validates taxonomy terms against educational taxonomies"""
    
    # Bloom's Taxonomy (Revised) with cognitive levels
    BLOOMS_TAXONOMY = {
        "remember": {
            "level": 1,
            "verbs": ["identify", "list", "define", "name", "recall", "recognize", "state"],
            "description": "Recall facts and basic concepts"
        },
        "understand": {
            "level": 2,
            "verbs": ["explain", "describe", "summarize", "interpret", "classify", "compare"],
            "description": "Explain ideas or concepts"
        },
        "apply": {
            "level": 3,
            "verbs": ["apply", "demonstrate", "implement", "use", "execute", "solve"],
            "description": "Use information in new situations"
        },
        "analyze": {
            "level": 4,
            "verbs": ["analyze", "differentiate", "distinguish", "examine", "investigate", "compare"],
            "description": "Draw connections among ideas"
        },
        "evaluate": {
            "level": 5,
            "verbs": ["evaluate", "justify", "critique", "assess", "judge", "recommend"],
            "description": "Justify a stand or decision"
        },
        "create": {
            "level": 6,
            "verbs": ["create", "design", "construct", "produce", "develop", "formulate"],
            "description": "Produce new or original work"
        }
    }
    
    # Indonesian Curriculum (Kurikulum Merdeka) specific taxonomy
    INDONESIAN_CURRICULUM_TAXONOMY = {
        "literasi": {
            "subcategories": ["literasi_numerasi", "literasi_sains", "literasi_digital", "literasi_finansial"],
            "description": "Foundation literacy competencies"
        },
        "numerasi": {
            "subcategories": ["konsep_angka", "operasi_hitung", "pemecahan_masalah", "data_dan_penyajian"],
            "description": "Mathematical literacy and problem-solving"
        },
        "sains": {
            "subcategories": ["pengetahuan_konseptual", "penelitian_saintifik", "pemahaman_alam"],
            "description": "Scientific literacy and inquiry"
        },
        "profil_pelajar_pancasila": {
            "subcategories": ["beriman", "berkebinekaan_global", "gotong_royong", "mandiri", "bernalir_kritis", "kreatif"],
            "description": "Pancasila student profile dimensions"
        }
    }
    
    # Competency dimensions (Fase A-D for SD, SMP, SMA)
    COMPETENCY_DIMENSIONS = {
        "fase_a": {"grade_range": [1, 2], "description": "Kelas 1-2 SD"},
        "fase_b": {"grade_range": [3, 4], "description": "Kelas 3-4 SD"},
        "fase_c": {"grade_range": [5, 6], "description": "Kelas 5-6 SD"},
        "fase_d": {"grade_range": [7, 8, 9], "description": "Kelas 7-9 SMP"},
        "fase_e": {"grade_range": [10, 11, 12], "description": "Kelas 10-12 SMA"}
    }
    
    @classmethod
    def validate_blooms_level(cls, blooms_level: str, verb: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate Bloom's taxonomy level and verb
        
        Args:
            blooms_level: Bloom's taxonomy level to validate
            verb: Optional specific verb to validate against the level
            
        Returns:
            Validation result with validity flag and details
        """
        if not blooms_level or not isinstance(blooms_level, str):
            return {
                "valid": False,
                "error": "blooms_level must be a non-empty string",
                "blooms_level": blooms_level
            }
        
        blooms_level = blooms_level.strip().lower()
        
        # Check if Bloom's level exists
        if blooms_level not in cls.BLOOMS_TAXONOMY:
            return {
                "valid": False,
                "error": f"Unknown Bloom's taxonomy level: {blooms_level}",
                "blooms_level": blooms_level,
                "valid_levels": list(cls.BLOOMS_TAXONOMY.keys())
            }
        
        result = {
            "valid": True,
            "blooms_level": blooms_level,
            "cognitive_level": cls.BLOOMS_TAXONOMY[blooms_level]["level"],
            "description": cls.BLOOMS_TAXONOMY[blooms_level]["description"],
            "valid_verbs": cls.BLOOMS_TAXONOMY[blooms_level]["verbs"]
        }
        
        # Validate verb if provided
        if verb:
            verb = verb.strip().lower()
            if verb not in cls.BLOOMS_TAXONOMY[blooms_level]["verbs"]:
                return {
                    "valid": False,
                    "error": f"Verb '{verb}' not valid for Bloom's level '{blooms_level}'",
                    "blooms_level": blooms_level,
                    "verb": verb,
                    "valid_verbs": cls.BLOOMS_TAXONOMY[blooms_level]["verbs"]
                }
            result["verb"] = verb
            result["verb_valid"] = True
        
        return result
    
    @classmethod
    def validate_indonesian_taxonomy(cls, category: str, subcategory: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate Indonesian curriculum taxonomy
        
        Args:
            category: Indonesian curriculum category
            subcategory: Optional subcategory to validate
            
        Returns:
            Validation result with validity flag and details
        """
        if not category or not isinstance(category, str):
            return {
                "valid": False,
                "error": "category must be a non-empty string",
                "category": category
            }
        
        category = category.strip().lower()
        
        # Check if category exists
        if category not in cls.INDONESIAN_CURRICULUM_TAXONOMY:
            return {
                "valid": False,
                "error": f"Unknown Indonesian curriculum category: {category}",
                "category": category,
                "valid_categories": list(cls.INDONESIAN_CURRICULUM_TAXONOMY.keys())
            }
        
        result = {
            "valid": True,
            "category": category,
            "description": cls.INDONESIAN_CURRICULUM_TAXONOMY[category]["description"]
        }
        
        # Validate subcategory if provided
        if subcategory:
            subcategory = subcategory.strip().lower()
            valid_subcategories = cls.INDONESIAN_CURRICULUM_TAXONOMY[category]["subcategories"]
            if subcategory not in valid_subcategories:
                return {
                    "valid": False,
                    "error": f"Subcategory '{subcategory}' not valid for category '{category}'",
                    "category": category,
                    "subcategory": subcategory,
                    "valid_subcategories": valid_subcategories
                }
            result["subcategory"] = subcategory
            result["subcategory_valid"] = True
        
        return result
    
    @classmethod
    def validate_competency_dimension(cls, phase: str, grade_level: Optional[int] = None) -> Dict[str, Any]:
        """
        Validate competency phase/dimension against grade level
        
        Args:
            phase: Curriculum phase (fase_a, fase_b, etc.)
            grade_level: Optional grade level for validation
            
        Returns:
            Validation result with validity flag and details
        """
        if not phase or not isinstance(phase, str):
            return {
                "valid": False,
                "error": "phase must be a non-empty string",
                "phase": phase
            }
        
        phase = phase.strip().lower()
        
        # Check if phase exists
        if phase not in cls.COMPETENCY_DIMENSIONS:
            return {
                "valid": False,
                "error": f"Unknown competency phase: {phase}",
                "phase": phase,
                "valid_phases": list(cls.COMPETENCY_DIMENSIONS.keys())
            }
        
        result = {
            "valid": True,
            "phase": phase,
            "description": cls.COMPETENCY_DIMENSIONS[phase]["description"],
            "grade_range": cls.COMPETENCY_DIMENSIONS[phase]["grade_range"]
        }
        
        # Validate grade level if provided
        if grade_level is not None:
            grade_range = cls.COMPETENCY_DIMENSIONS[phase]["grade_range"]
            if grade_level not in grade_range:
                return {
                    "valid": False,
                    "error": f"Grade level {grade_level} not valid for phase '{phase}'",
                    "phase": phase,
                    "grade_level": grade_level,
                    "valid_grade_range": grade_range
                }
            result["grade_level"] = grade_level
            result["grade_level_valid"] = True
        
        return result
    
    @classmethod
    def validate_taxonomy_batch(cls, taxonomy_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate multiple taxonomy entries in batch
        
        Args:
            taxonomy_list: List of taxonomy dictionaries to validate
            
        Returns:
            Batch validation result with overall validity and individual results
        """
        if not taxonomy_list:
            return {
                "valid": True,
                "total_count": 0,
                "valid_count": 0,
                "invalid_count": 0,
                "results": []
            }
        
        results = []
        valid_count = 0
        
        for taxonomy_entry in taxonomy_list:
            taxonomy_type = taxonomy_entry.get("taxonomy_type")
            
            if taxonomy_type == "blooms":
                result = cls.validate_blooms_level(
                    taxonomy_entry.get("blooms_level"),
                    taxonomy_entry.get("verb")
                )
            elif taxonomy_type == "indonesian":
                result = cls.validate_indonesian_taxonomy(
                    taxonomy_entry.get("category"),
                    taxonomy_entry.get("subcategory")
                )
            elif taxonomy_type == "competency_dimension":
                result = cls.validate_competency_dimension(
                    taxonomy_entry.get("phase"),
                    taxonomy_entry.get("grade_level")
                )
            else:
                result = {
                    "valid": False,
                    "error": f"Unknown taxonomy type: {taxonomy_type}",
                    "taxonomy_type": taxonomy_type
                }
            
            results.append(result)
            if result["valid"]:
                valid_count += 1
        
        return {
            "valid": valid_count == len(taxonomy_list),
            "total_count": len(taxonomy_list),
            "valid_count": valid_count,
            "invalid_count": len(taxonomy_list) - valid_count,
            "results": results
        }
    
    @classmethod
    def get_taxonomy_standards(cls, framework: str = "both") -> Dict[str, Any]:
        """
        Get official taxonomy standards for reference
        
        Args:
            framework: Framework to retrieve ('blooms', 'indonesian', 'both')
            
        Returns:
            Taxonomy standards information
        """
        standards = {}
        
        if framework in ["blooms", "both"]:
            standards["blooms_taxonomy"] = cls.BLOOMS_TAXONOMY
        
        if framework in ["indonesian", "both"]:
            standards["indonesian_curriculum"] = cls.INDONESIAN_CURRICULUM_TAXONOMY
            standards["competency_dimensions"] = cls.COMPETENCY_DIMENSIONS
        
        return standards