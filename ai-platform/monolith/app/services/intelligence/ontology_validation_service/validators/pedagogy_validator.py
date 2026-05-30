"""
Pedagogy Validator
Validates pedagogy types and teaching methods against educational standards
"""
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class PedagogyValidator:
    """Validates pedagogy types and teaching methods against educational standards"""
    
    # Official pedagogy types for Kurikulum Merdeka
    PEDAGOGY_TYPES = {
        "student_centered": {
            "methods": [
                "inquiry_based_learning",
                "project_based_learning", 
                "problem_based_learning",
                "collaborative_learning",
                "discovery_learning",
                "experiential_learning"
            ],
            "description": "Learning approaches that focus on student needs and interests"
        },
        "differentiated": {
            "methods": [
                "differentiated_instruction",
                "scaffolding",
                "tiered_activities",
                "flexible_grouping"
            ],
            "description": "Tailored instruction to meet diverse student needs"
        },
        "assessment_for_learning": {
            "methods": [
                "formative_assessment",
                "peer_assessment",
                "self_assessment",
                "authentic_assessment"
            ],
            "description": "Assessment methods that support learning"
        },
        "technology_enhanced": {
            "methods": [
                "blended_learning",
                "flipped_classroom",
                "gamification",
                "digital_storytelling"
            ],
            "description": "Integration of technology in teaching and learning"
        },
        "kurikulum_merdeka_specific": {
            "methods": [
                "p5_project",  # Project-based learning for Pancasila Student Profile
                "project_based",
                "inquiry_based",
                "reflection",
                "contextual_learning"
            ],
            "description": "Specific pedagogy methods from Kurikulum Merdeka"
        }
    }
    
    # Teaching strategies aligned with Profil Pelajar Pancasila
    PROFIL_PELAJAR_PANCASILA_STRATEGIES = {
        "faithful": ["value_based_learning", "character_education", "religious_integration"],
        "diverse": ["multicultural_education", "global_citizenship", "intercultural_learning"],
        "collaborative": ["group_projects", "peer_tutoring", "team_based_learning"],
        "independent": ["self_directed_learning", "metacognition", "autonomous_learning"],
        "critical": ["critical_thinking", "problem_solving", "debate", "analysis"],
        "creative": ["creative_thinking", "innovation", "design_thinking", "artistic_expression"]
    }
    
    @classmethod
    def validate_pedagogy_type(cls, pedagogy_type: str, teaching_method: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a pedagogy type and teaching method
        
        Args:
            pedagogy_type: The pedagogy type to validate
            teaching_method: Optional specific teaching method to validate
            
        Returns:
            Validation result with validity flag and details
        """
        if not pedagogy_type or not isinstance(pedagogy_type, str):
            return {
                "valid": False,
                "error": "pedagogy_type must be a non-empty string",
                "pedagogy_type": pedagogy_type
            }
        
        pedagogy_type = pedagogy_type.strip().lower()
        
        # Check if pedagogy type exists
        if pedagogy_type not in cls.PEDAGOGY_TYPES:
            return {
                "valid": False,
                "error": f"Unknown pedagogy type: {pedagogy_type}",
                "pedagogy_type": pedagogy_type,
                "valid_types": list(cls.PEDAGOGY_TYPES.keys())
            }
        
        result = {
            "valid": True,
            "pedagogy_type": pedagogy_type,
            "description": cls.PEDAGOGY_TYPES[pedagogy_type]["description"]
        }
        
        # Validate teaching method if provided
        if teaching_method:
            method_validation = cls._validate_teaching_method(pedagogy_type, teaching_method)
            if not method_validation["valid"]:
                return method_validation
            result["teaching_method"] = teaching_method
            result["teaching_method_valid"] = True
        
        return result
    
    @classmethod
    def _validate_teaching_method(cls, pedagogy_type: str, teaching_method: str) -> Dict[str, Any]:
        """Validate teaching method within pedagogy type context"""
        teaching_method = teaching_method.strip().lower()
        
        valid_methods = cls.PEDAGOGY_TYPES[pedagogy_type]["methods"]
        
        if teaching_method not in valid_methods:
            return {
                "valid": False,
                "error": f"Invalid teaching method '{teaching_method}' for pedagogy type '{pedagogy_type}'",
                "pedagogy_type": pedagogy_type,
                "teaching_method": teaching_method,
                "valid_methods": valid_methods
            }
        
        return {
            "valid": True,
            "teaching_method": teaching_method
        }
    
    @classmethod
    def validate_profil_pelajar_pancasila(cls, strategy: str) -> Dict[str, Any]:
        """
        Validate strategy against Profil Pelajar Pancasila principles
        
        Args:
            strategy: Teaching strategy to validate
            
        Returns:
            Validation result with mapped principles
        """
        if not strategy or not isinstance(strategy, str):
            return {
                "valid": False,
                "error": "strategy must be a non-empty string",
                "strategy": strategy
            }
        
        strategy = strategy.strip().lower()
        
        # Find which principles this strategy aligns with
        matched_principles = []
        for principle, strategies in cls.PROFIL_PELAJAR_PANCASILA_STRATEGIES.items():
            if strategy in strategies:
                matched_principles.append(principle)
        
        if not matched_principles:
            return {
                "valid": False,
                "error": f"Strategy '{strategy}' not aligned with Profil Pelajar Pancasila principles",
                "strategy": strategy,
                "valid_strategies": [s for strategies in cls.PROFIL_PELAJAR_PANCASILA_STRATEGIES.values() for s in strategies]
            }
        
        return {
            "valid": True,
            "strategy": strategy,
            "aligned_principles": matched_principles,
            "framework": "Profil Pelajar Pancasila"
        }
    
    @classmethod
    def validate_pedagogy_batch(cls, pedagogy_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate multiple pedagogy entries in batch
        
        Args:
            pedagogy_list: List of pedagogy dictionaries to validate
            
        Returns:
            Batch validation result with overall validity and individual results
        """
        if not pedagogy_list:
            return {
                "valid": True,
                "total_count": 0,
                "valid_count": 0,
                "invalid_count": 0,
                "results": []
            }
        
        results = []
        valid_count = 0
        
        for pedagogy_entry in pedagogy_list:
            pedagogy_type = pedagogy_entry.get("pedagogy_type")
            teaching_method = pedagogy_entry.get("teaching_method")
            
            result = cls.validate_pedagogy_type(pedagogy_type, teaching_method)
            results.append(result)
            if result["valid"]:
                valid_count += 1
        
        return {
            "valid": valid_count == len(pedagogy_list),
            "total_count": len(pedagogy_list),
            "valid_count": valid_count,
            "invalid_count": len(pedagogy_list) - valid_count,
            "results": results
        }
    
    @classmethod
    def get_pedagogy_standards(cls, framework: str = "kurikulum_merdeka") -> Dict[str, Any]:
        """
        Get official pedagogy standards for reference
        
        Args:
            framework: Educational framework (default: kurikulum_merdeka)
            
        Returns:
            Pedagogy standards information
        """
        if framework == "kurikulum_merdeka":
            return {
                "framework": "Kurikulum Merdeka",
                "pedagogy_types": cls.PEDAGOGY_TYPES,
                "profil_pelajar_pancasila": cls.PROFIL_PELAJAR_PANCASILA_STRATEGIES
            }
        else:
            return {
                "framework": framework,
                "error": f"Framework {framework} not yet implemented"
            }