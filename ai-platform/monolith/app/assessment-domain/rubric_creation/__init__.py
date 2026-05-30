"""
Rubric Creation

This service provides comprehensive rubric creation capabilities aligned with
Kurikulum Merdeka authentic assessment principles, supporting various assessment
types and proficiency levels.
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class ProficiencyLevel(Enum):
    """Proficiency levels for assessment rubrics"""
    EXCEEDS = "exceeds"  # Demonstrates understanding beyond expectations
    MEETS = "meets"  # Meets expectations
    APPROACHING = "approaching"  # Developing understanding
    EMERGING = "emerging"  # Beginning understanding


class RubricCreation:
    """Rubric creation service for Kurikulum Merdeka assessment"""
    
    def __init__(self):
        self.rubric_database = {}
        self.rubric_templates = self._initialize_rubric_templates()
        self.criteria_library = self._initialize_criteria_library()
    
    def create(self, learning_objectives: List[str], criteria: Dict) -> Dict:
        """Create assessment rubric based on learning objectives and criteria"""
        rubric_id = f"rubric_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Determine rubric type
        rubric_type = self._determine_rubric_type(criteria)
        
        # Generate rubric criteria from learning objectives
        rubric_criteria = self._generate_rubric_criteria(learning_objectives, criteria)
        
        # Create proficiency level descriptors
        proficiency_descriptors = self._create_proficiency_descriptors(
            rubric_criteria,
            rubric_type
        )
        
        # Set scoring system
        scoring_system = self._set_scoring_system(criteria)
        
        # Add authentic assessment elements if needed
        authentic_elements = self._add_authentic_elements(rubric_type, criteria)
        
        rubric = {
            "rubric_id": rubric_id,
            "rubric_type": rubric_type,
            "learning_objectives": learning_objectives,
            "rubric_criteria": rubric_criteria,
            "proficiency_descriptors": proficiency_descriptors,
            "scoring_system": scoring_system,
            "authentic_elements": authentic_elements,
            "created_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        self.rubric_database[rubric_id] = rubric
        
        return rubric
    
    def create_authentic_rubric(self, task_type: str, deliverables: List[Dict], context: Dict) -> Dict:
        """Create rubric for authentic assessment task"""
        authentic_rubric_id = f"authentic_rubric_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate authentic assessment criteria
        authentic_criteria = self._generate_authentic_criteria(
            task_type,
            deliverables,
            context
        )
        
        # Create proficiency level descriptions for authentic assessment
        authentic_descriptors = self._create_authentic_descriptors(
            authentic_criteria,
            task_type
        )
        
        # Set authentic assessment scoring
        authentic_scoring = self._set_authentic_scoring(authentic_criteria)
        
        # Add performance indicators
        performance_indicators = self._add_performance_indicators(
            authentic_criteria,
            task_type
        )
        
        authentic_rubric = {
            "authentic_rubric_id": authentic_rubric_id,
            "task_type": task_type,
            "deliverables": deliverables,
            "authentic_criteria": authentic_criteria,
            "authentic_descriptors": authentic_descriptors,
            "authentic_scoring": authentic_scoring,
            "performance_indicators": performance_indicators,
            "context": context,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.rubric_database[authentic_rubric_id] = authentic_rubric
        
        return authentic_rubric
    
    def create_performance_rubric(self, performance_task: Dict, skill_areas: List[str]) -> Dict:
        """Create rubric for performance-based assessment"""
        performance_rubric_id = f"perf_rubric_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate performance criteria
        performance_criteria = self._generate_performance_criteria(
            performance_task,
            skill_areas
        )
        
        # Create performance level descriptions
        performance_descriptors = self._create_performance_descriptors(
            performance_criteria,
            performance_task
        )
        
        # Set performance scoring system
        performance_scoring = self._set_performance_scoring(performance_criteria)
        
        # Add observation checklist
        observation_checklist = self._create_observation_checklist(
            performance_criteria
        )
        
        performance_rubric = {
            "performance_rubric_id": performance_rubric_id,
            "performance_task": performance_task,
            "skill_areas": skill_areas,
            "performance_criteria": performance_criteria,
            "performance_descriptors": performance_descriptors,
            "performance_scoring": performance_scoring,
            "observation_checklist": observation_checklist,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.rubric_database[performance_rubric_id] = performance_rubric
        
        return performance_rubric
    
    def create_analytic_rubric(self, dimensions: List[str], performance_levels: List[str]) -> Dict:
        """Create analytic rubric with multiple dimensions and performance levels"""
        analytic_rubric_id = f"analytic_rubric_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Create analytic criteria for each dimension
        analytic_criteria = self._create_analytic_criteria(dimensions)
        
        # Create performance level descriptions for each criterion
        analytic_descriptors = self._create_analytic_descriptors(
            analytic_criteria,
            performance_levels
        )
        
        # Set analytic scoring system
        analytic_scoring = self._set_analytic_scoring(analytic_criteria, performance_levels)
        
        analytic_rubric = {
            "analytic_rubric_id": analytic_rubric_id,
            "dimensions": dimensions,
            "performance_levels": performance_levels,
            "analytic_criteria": analytic_criteria,
            "analytic_descriptors": analytic_descriptors,
            "analytic_scoring": analytic_scoring,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.rubric_database[analytic_rubric_id] = analytic_rubric
        
        return analytic_rubric
    
    def customize_rubric(self, rubric_id: str, customization: Dict) -> Dict:
        """Customize existing rubric"""
        if rubric_id not in self.rubric_database:
            return {"error": "Rubric not found"}
        
        rubric = self.rubric_database[rubric_id]
        
        # Apply customization
        if "criteria_modifications" in customization:
            self._apply_criteria_modifications(rubric, customization["criteria_modifications"])
        
        if "proficiency_adjustments" in customization:
            self._apply_proficiency_adjustments(rubric, customization["proficiency_adjustments"])
        
        if "scoring_changes" in customization:
            self._apply_scoring_changes(rubric, customization["scoring_changes"])
        
        rubric["customized"] = True
        rubric["customized_at"] = datetime.utcnow().isoformat()
        
        return {
            "rubric_id": rubric_id,
            "status": "customized",
            "rubric": rubric
        }
    
    def _determine_rubric_type(self, criteria: Dict) -> str:
        """Determine appropriate rubric type based on criteria"""
        assessment_type = criteria.get("assessment_type", "general")
        
        if assessment_type == "authentic":
            return "authentic"
        elif assessment_type == "performance":
            return "performance"
        elif criteria.get("analytic_required", False):
            return "analytic"
        else:
            return "general"
    
    def _generate_rubric_criteria(self, learning_objectives: List[str], criteria: Dict) -> List[Dict]:
        """Generate rubric criteria from learning objectives"""
        rubric_criteria = []
        
        for i, objective in enumerate(learning_objectives):
            criterion = {
                "criterion_id": f"crit_{i+1}",
                "criterion_name": f"Criterion {i+1}",
                "objective_aligned": objective,
                "description": self._generate_criterion_description(objective),
                "weight": 1.0 / len(learning_objectives)
            }
            rubric_criteria.append(criterion)
        
        return rubric_criteria
    
    def _generate_criterion_description(self, objective: str) -> str:
        """Generate description for criterion based on objective"""
        return f"Student demonstrates understanding of {objective}"
    
    def _create_proficiency_descriptors(self, rubric_criteria: List[Dict], rubric_type: str) -> Dict:
        """Create proficiency level descriptors for each criterion"""
        proficiency_descriptors = {}
        
        for criterion in rubric_criteria:
            criterion_id = criterion["criterion_id"]
            
            proficiency_descriptors[criterion_id] = {
                ProficiencyLevel.EXCEEDS.value: self._generate_exceeds_descriptor(criterion),
                ProficiencyLevel.MEETS.value: self._generate_meets_descriptor(criterion),
                ProficiencyLevel.APPROACHING.value: self._generate_approaching_descriptor(criterion),
                ProficiencyLevel.EMERGING.value: self._generate_emerging_descriptor(criterion)
            }
        
        return proficiency_descriptors
    
    def _generate_exceeds_descriptor(self, criterion: Dict) -> str:
        """Generate descriptor for exceeds level"""
        objective = criterion.get("objective_aligned", "the concept")
        return f"Demonstrates deep understanding of {objective} with sophisticated application"
    
    def _generate_meets_descriptor(self, criterion: Dict) -> str:
        """Generate descriptor for meets level"""
        objective = criterion.get("objective_aligned", "the concept")
        return f"Demonstrates solid understanding of {objective} with competent application"
    
    def _generate_approaching_descriptor(self, criterion: Dict) -> str:
        """Generate descriptor for approaching level"""
        objective = criterion.get("objective_aligned", "the concept")
        return f"Demonstrates developing understanding of {objective} with partial application"
    
    def _generate_emerging_descriptor(self, criterion: Dict) -> str:
        """Generate descriptor for emerging level"""
        objective = criterion.get("objective_aligned", "the concept")
        return f"Beginning to understand {objective} with limited application"
    
    def _set_scoring_system(self, criteria: Dict) -> Dict:
        """Set scoring system for rubric"""
        return {
            "scoring_type": criteria.get("scoring_type", "point_based"),
            "point_range": criteria.get("point_range", [0, 100]),
            "proficiency_conversion": {
                ProficiencyLevel.EXCEEDS.value: "90-100",
                ProficiencyLevel.MEETS.value: "70-89",
                ProficiencyLevel.APPROACHING.value: "55-69",
                ProficiencyLevel.EMERGING.value: "0-54"
            },
            "partial_credit": criteria.get("partial_credit", True)
        }
    
    def _add_authentic_elements(self, rubric_type: str, criteria: Dict) -> Dict:
        """Add authentic assessment elements to rubric"""
        if rubric_type == "authentic":
            return {
                "real_world_relevance": True,
                "student_choice": True,
                "collaboration_criteria": criteria.get("collaboration_required", False),
                "reflection_criteria": True,
                "audience_criteria": True
            }
        else:
            return {}
    
    def _generate_authentic_criteria(self, task_type: str, deliverables: List[Dict], context: Dict) -> List[Dict]:
        """Generate criteria for authentic assessment rubric"""
        authentic_criteria = []
        
        # Content quality criterion
        authentic_criteria.append({
            "criterion_id": "auth_content",
            "criterion_name": "Content Quality",
            "description": "Depth, accuracy, and relevance of content",
            "weight": 0.35
        })
        
        # Application criterion
        authentic_criteria.append({
            "criterion_id": "auth_application",
            "criterion_name": "Application",
            "description": "Application of knowledge in authentic context",
            "weight": 0.30
        })
        
        # Communication criterion
        authentic_criteria.append({
            "criterion_id": "auth_communication",
            "criterion_name": "Communication",
            "description": "Clarity and effectiveness of communication",
            "weight": 0.20
        })
        
        # Process criterion
        authentic_criteria.append({
            "criterion_id": "auth_process",
            "criterion_name": "Process",
            "description": "Quality of learning process and reflection",
            "weight": 0.15
        })
        
        return authentic_criteria
    
    def _create_authentic_descriptors(self, authentic_criteria: List[Dict], task_type: str) -> Dict:
        """Create descriptors for authentic assessment rubric"""
        descriptors = {}
        
        for criterion in authentic_criteria:
            criterion_id = criterion["criterion_id"]
            
            descriptors[criterion_id] = {
                ProficiencyLevel.EXCEEDS.value: self._generate_authentic_exceeds(criterion, task_type),
                ProficiencyLevel.MEETS.value: self._generate_authentic_meets(criterion, task_type),
                ProficiencyLevel.APPROACHING.value: self._generate_authentic_approaching(criterion, task_type),
                ProficiencyLevel.EMERGING.value: self._generate_authentic_emerging(criterion, task_type)
            }
        
        return descriptors
    
    def _generate_authentic_exceeds(self, criterion: Dict, task_type: str) -> str:
        """Generate authentic exceeds descriptor"""
        criterion_name = criterion["criterion_name"]
        return f"Exceptional {criterion_name.lower()} with sophisticated {task_type} application"
    
    def _generate_authentic_meets(self, criterion: Dict, task_type: str) -> str:
        """Generate authentic meets descriptor"""
        criterion_name = criterion["criterion_name"]
        return f"Solid {criterion_name.lower()} with competent {task_type} application"
    
    def _generate_authentic_approaching(self, criterion: Dict, task_type: str) -> str:
        """Generate authentic approaching descriptor"""
        criterion_name = criterion["criterion_name"]
        return f"Developing {criterion_name.lower()} with basic {task_type} application"
    
    def _generate_authentic_emerging(self, criterion: Dict, task_type: str) -> str:
        """Generate authentic emerging descriptor"""
        criterion_name = criterion["criterion_name"]
        return f"Beginning {criterion_name.lower()} with limited {task_type} application"
    
    def _set_authentic_scoring(self, authentic_criteria: List[Dict]) -> Dict:
        """Set scoring for authentic assessment rubric"""
        return {
            "scoring_type": "weight_based",
            "total_points": 100,
            "criteria_weights": {criterion["criterion_id"]: criterion["weight"] for criterion in authentic_criteria},
            "proficiency_benchmarks": {
                ProficiencyLevel.EXCEEDS.value: 90,
                ProficiencyLevel.MEETS.value: 75,
                ProficiencyLevel.APPROACHING.value: 60,
                ProficiencyLevel.EMERGING.value: 0
            }
        }
    
    def _add_performance_indicators(self, authentic_criteria: List[Dict], task_type: str) -> List[str]:
        """Add performance indicators for authentic assessment"""
        return [
            "Demonstrates understanding in authentic context",
            "Applies knowledge to real-world situations",
            "Communicates findings effectively",
            "Reflects on learning process"
        ]
    
    def _generate_performance_criteria(self, performance_task: Dict, skill_areas: List[str]) -> List[Dict]:
        """Generate criteria for performance-based assessment"""
        performance_criteria = []
        
        for i, skill_area in enumerate(skill_areas):
            performance_criteria.append({
                "criterion_id": f"perf_crit_{i+1}",
                "criterion_name": skill_area,
                "description": f"Demonstration of {skill_area} in performance",
                "observable_behaviors": self._generate_observable_behaviors(skill_area),
                "weight": 1.0 / len(skill_areas)
            })
        
        return performance_criteria
    
    def _generate_observable_behaviors(self, skill_area: str) -> List[str]:
        """Generate observable behaviors for skill area"""
        return [
            f"Demonstrates {skill_area} in performance",
            f"Applies {skill_area} consistently",
            f"Shows understanding of {skill_area} through action"
        ]
    
    def _create_performance_descriptors(self, performance_criteria: List[Dict], performance_task: Dict) -> Dict:
        """Create descriptors for performance-based assessment"""
        descriptors = {}
        
        for criterion in performance_criteria:
            criterion_id = criterion["criterion_id"]
            
            descriptors[criterion_id] = {
                ProficiencyLevel.EXCEEDS.value: f"Exceptional demonstration with {criterion['criterion_name']}",
                ProficiencyLevel.MEETS.value: f"Competent demonstration of {criterion['criterion_name']}",
                ProficiencyLevel.APPROACHING.value: f"Developing demonstration of {criterion['criterion_name']}",
                ProficiencyLevel.EMERGING.value: f"Beginning demonstration of {criterion['criterion_name']}"
            }
        
        return descriptors
    
    def _set_performance_scoring(self, performance_criteria: List[Dict]) -> Dict:
        """Set scoring for performance-based assessment"""
        return {
            "scoring_type": "observation_based",
            "total_points": 100,
            "criteria_points": {criterion["criterion_id"]: int(criterion["weight"] * 100) for criterion in performance_criteria},
            "proficiency_levels": {
                ProficiencyLevel.EXCEEDS.value: 90,
                ProficiencyLevel.MEETS.value: 75,
                ProficiencyLevel.APPROACHING.value: 60,
                ProficiencyLevel.EMERGING.value: 0
            }
        }
    
    def _create_observation_checklist(self, performance_criteria: List[Dict]) -> List[str]:
        """Create observation checklist for performance assessment"""
        checklist = []
        
        for criterion in performance_criteria:
            for behavior in criterion.get("observable_behaviors", []):
                checklist.append(behavior)
        
        return checklist
    
    def _create_analytic_criteria(self, dimensions: List[str]) -> List[Dict]:
        """Create criteria for analytic rubric"""
        analytic_criteria = []
        
        for i, dimension in enumerate(dimensions):
            analytic_criteria.append({
                "criterion_id": f"an_crit_{i+1}",
                "criterion_name": dimension,
                "description": f"Assessment of {dimension}",
                "indicators": self._generate_dimension_indicators(dimension),
                "weight": 1.0 / len(dimensions)
            })
        
        return analytic_criteria
    
    def _generate_dimension_indicators(self, dimension: str) -> List[str]:
        """Generate indicators for specific dimension"""
        return [
            f"Demonstrates {dimension}",
            f"Applies {dimension} effectively",
            f"Shows mastery of {dimension}"
        ]
    
    def _create_analytic_descriptors(self, analytic_criteria: List[Dict], performance_levels: List[str]) -> Dict:
        """Create descriptors for analytic rubric"""
        descriptors = {}
        
        for criterion in analytic_criteria:
            criterion_id = criterion["criterion_id"]
            
            descriptors[criterion_id] = {}
            for level in performance_levels:
                descriptors[criterion_id][level] = f"Student {criterion['criterion_name']} at {level} level"
        
        return descriptors
    
    def _set_analytic_scoring(self, analytic_criteria: List[Dict], performance_levels: List[str]) -> Dict:
        """Set scoring for analytic rubric"""
        return {
            "scoring_type": "level_based",
            "performance_levels": performance_levels,
            "level_values": {level: idx + 1 for idx, level in enumerate(performance_levels)},
            "criteria_weights": {criterion["criterion_id"]: criterion["weight"] for criterion in analytic_criteria}
        }
    
    def _apply_criteria_modifications(self, rubric: Dict, modifications: List[Dict]) -> None:
        """Apply criteria modifications to rubric"""
        for modification in modifications:
            criterion_id = modification.get("criterion_id")
            modification_type = modification.get("modification_type")
            
            if modification_type == "add":
                rubric["rubric_criteria"].append(modification.get("new_criterion"))
            elif modification_type == "remove":
                rubric["rubric_criteria"] = [c for c in rubric["rubric_criteria"] if c["criterion_id"] != criterion_id]
            elif modification_type == "modify":
                for criterion in rubric["rubric_criteria"]:
                    if criterion["criterion_id"] == criterion_id:
                        criterion.update(modification.get("updates", {}))
    
    def _apply_proficiency_adjustments(self, rubric: Dict, adjustments: Dict) -> None:
        """Apply proficiency level adjustments"""
        for criterion_id, adjustments_list in adjustments.items():
            if criterion_id in rubric["proficiency_descriptors"]:
                for adjustment in adjustments_list:
                    level = adjustment.get("level")
                    new_descriptor = adjustment.get("new_descriptor")
                    if level and new_descriptor:
                        rubric["proficiency_descriptors"][criterion_id][level] = new_descriptor
    
    def _apply_scoring_changes(self, rubric: Dict, changes: Dict) -> None:
        """Apply scoring system changes"""
        rubric["scoring_system"].update(changes)
    
    def _initialize_rubric_templates(self) -> Dict:
        """Initialize rubric templates"""
        return {
            "authentic_IPA": {
                "template_id": "authentic_IPA",
                "rubric_type": "authentic",
                "subject": "IPA",
                "criteria": ["content_quality", "scientific_process", "communication", "application"]
            },
            "performance_Matematika": {
                "template_id": "performance_Matematika",
                "rubric_type": "performance",
                "subject": "Matematika",
                "skill_areas": ["problem_solving", "reasoning", "communication"]
            },
            "analytic_Bahasa": {
                "template_id": "analytic_Bahasa",
                "rubric_type": "analytic",
                "subject": "Bahasa Indonesia",
                "dimensions": ["reading_comprehension", "writing_quality", "oral_communication"]
            }
        }
    
    def _initialize_criteria_library(self) -> Dict:
        """Initialize criteria library for rubric creation"""
        return {
            "content_mastery": {
                "description": "Demonstrates understanding of content",
                "indicators": ["accuracy", "depth", "completeness"]
            },
            "application_skill": {
                "description": "Applies knowledge in context",
                "indicators": ["transfer", "adaptation", "innovation"]
            },
            "critical_thinking": {
                "description": "Demonstrates critical thinking",
                "indicators": ["analysis", "evaluation", "synthesis"]
            },
            "communication": {
                "description": "Communicates effectively",
                "indicators": ["clarity", "organization", "audience_awareness"]
            },
            "collaboration": {
                "description": "Collaborates effectively",
                "indicators": ["participation", "contribution", "teamwork"]
            }
        }