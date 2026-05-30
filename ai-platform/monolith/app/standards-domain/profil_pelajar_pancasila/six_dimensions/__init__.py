"""
Six Dimensions of Profil Pelajar Pancasila

The 6 dimensions defined in Kurikulum Merdeka for character development:
1. Beriman, bertakwa kepada Tuhan YME, dan berakhlak mulia
2. Berkebinekaan global
3. Gotong royong
4. Mandiri
5. Bernalar kritis
6. Kreatif
"""

from enum import Enum
from typing import Dict, List


class ProfilPelajarPancasilaDimension(Enum):
    """The 6 dimensions of Profil Pelajar Pancasila"""
    BERIMAN = "Beriman, bertakwa kepada Tuhan YME, dan berakhlak mulia"
    BERKEBINEKAAN = "Berkebinekaan global"
    GOTONG_ROYONG = "Gotong royong"
    MANDIRI = "Mandiri"
    BERNALAR_KRITIS = "Bernalar kritis"
    KREATIF = "Kreatif"


class ProfilPelajarPancasilaDimensions:
    """Management of the 6 dimensions"""
    
    def __init__(self):
        self.dimension_descriptions = {
            ProfilPelajarPancasilaDimension.BERIMAN: {
                "focus": "Religious and moral development",
                "key_traits": ["faith", "moral integrity", "religious practice", "ethical behavior"],
                "development_areas": ["spiritual awareness", "moral reasoning", "character formation"]
            },
            ProfilPelajarPancasilaDimension.BERKEBINEKAAN: {
                "focus": "Global diversity and multicultural understanding",
                "key_traits": ["cultural awareness", "tolerance", "global perspective", "intercultural competence"],
                "development_areas": ["cultural understanding", "global citizenship", "multicultural competence"]
            },
            ProfilPelajarPancasilaDimension.GOTONG_ROYONG: {
                "focus": "Collaboration and community service",
                "key_traits": ["cooperation", "empathy", "community service", "social responsibility"],
                "development_areas": ["collaborative skills", "empathy development", "social responsibility"]
            },
            ProfilPelajarPancasilaDimension.MANDIRI: {
                "focus": "Independence and self-reliance",
                "key_traits": ["autonomy", "responsibility", "decision-making", "problem-solving"],
                "development_areas": ["self-management", "independence", "responsibility"]
            },
            ProfilPelajarPancasilaDimension.BERNALAR_KRITIS: {
                "focus": "Critical thinking and analytical skills",
                "key_traits": ["logical reasoning", "problem analysis", "evaluation", "reflective thinking"],
                "development_areas": ["critical thinking", "logical reasoning", "analytical skills"]
            },
            ProfilPelajarPancasilaDimension.KREATIF: {
                "focus": "Creativity and innovation",
                "key_traits": ["innovation", "creative expression", "problem-solving", "originality"],
                "development_areas": ["creative thinking", "innovation", "artistic expression"]
            }
        }
    
    def get_all_dimensions(self) -> List[Dict]:
        """Get all 6 dimensions with descriptions"""
        dimensions = []
        for dim_enum in ProfilPelajarPancasilaDimension:
            dimensions.append({
                "id": dim_enum.value,
                "name": dim_enum.name,
                "description": dim_enum.value,
                "focus": self.dimension_descriptions[dim_enum]["focus"],
                "key_traits": self.dimension_descriptions[dim_enum]["key_traits"],
                "development_areas": self.dimension_descriptions[dim_enum]["development_areas"]
            })
        return dimensions
    
    def get_dimension(self, dimension_id: str) -> Dict:
        """Get specific dimension by ID"""
        for dim_enum in ProfilPelajarPancasilaDimension:
            if dim_enum.value == dimension_id or dim_enum.name == dimension_id:
                return {
                    "id": dim_enum.value,
                    "name": dim_enum.name,
                    "description": dim_enum.value,
                    "focus": self.dimension_descriptions[dim_enum]["focus"],
                    "key_traits": self.dimension_descriptions[dim_enum]["key_traits"],
                    "development_areas": self.dimension_descriptions[dim_enum]["development_areas"]
                }
        return None
    
    def validate_dimension_integration(self, curriculum_data: Dict) -> Dict:
        """Validate if curriculum integrates all dimensions appropriately"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "dimension_coverage": {}
        }
        
        for dim_enum in ProfilPelajarPancasilaDimension:
            dimension_name = dim_enum.value
            # Check if dimension is mentioned in curriculum
            dimension_mentioned = dimension_name.lower() in str(curriculum_data).lower()
            validation_result["dimension_coverage"][dimension_name] = dimension_mentioned
            
            if not dimension_mentioned:
                validation_result["warnings"].append(f"Dimension {dimension_name} not explicitly integrated")
        
        # Check if at least 4 dimensions are integrated
        integrated_count = sum(1 for mentioned in validation_result["dimension_coverage"].values() if mentioned)
        if integrated_count < 4:
            validation_result["warnings"].append(f"Only {integrated_count}/6 dimensions integrated (recommended 4+)")
        
        return validation_result