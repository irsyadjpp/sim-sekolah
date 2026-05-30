"""
Assessment Generation

This service provides comprehensive assessment generation capabilities aligned with
Kurikulum Merdeka standards, including authentic assessment, formative assessment,
and summative assessment types.
"""

from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class AssessmentType(Enum):
    """Types of assessments supported"""
    AUTHENTIC = "authentic"  # Real-world application
    FORMATIVE = "formative"  # Ongoing assessment during learning
    SUMMATIVE = "summative"  # End of unit assessment
    DIAGNOSTIC = "diagnostic"  # Pre-assessment
    PERFORMANCE = "performance"  # Performance-based assessment


class AssessmentGeneration:
    """Assessment generation service for Kurikulum Merdeka alignment"""
    
    def __init__(self):
        self.assessment_database = {}
        self.assessment_templates = self._initialize_assessment_templates()
        self.authentic_task_library = self._initialize_authentic_tasks()
    
    def generate(self, context: Dict) -> Dict:
        """Generate assessment based on learning context"""
        assessment_id = f"assess_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Determine appropriate assessment type
        assessment_type = self._determine_assessment_type(context)
        
        # Select assessment template
        template = self._select_assessment_template(assessment_type, context)
        
        # Generate assessment content
        assessment_content = self._generate_assessment_content(
            template,
            context,
            assessment_type
        )
        
        # Align with learning objectives
        aligned_objectives = self._align_with_learning_objectives(
            context.get("learning_objectives", []),
            assessment_content
        )
        
        # Add Kurikulum Merdeka authentic assessment elements
        authentic_elements = self._add_authentic_elements(
            assessment_type,
            context
        )
        
        # Generate assessment criteria
        criteria = self._generate_assessment_criteria(
            assessment_type,
            aligned_objectives
        )
        
        assessment = {
            "assessment_id": assessment_id,
            "assessment_type": assessment_type.value,
            "template": template,
            "context": context,
            "assessment_content": assessment_content,
            "aligned_objectives": aligned_objectives,
            "authentic_elements": authentic_elements,
            "criteria": criteria,
            "estimated_duration": self._estimate_duration(assessment_content),
            "generated_at": datetime.utcnow().isoformat(),
            "kurikulum_merdeka_aligned": True
        }
        
        self.assessment_database[assessment_id] = assessment
        
        return assessment
    
    def generate_authentic_assessment(self, learning_objectives: List[str], context: Dict) -> Dict:
        """Generate authentic assessment based on learning objectives"""
        authentic_id = f"authentic_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Select authentic task type
        task_type = self._select_authentic_task_type(context)
        
        # Generate authentic task scenario
        scenario = self._generate_authentic_scenario(task_type, context)
        
        # Create task requirements
        requirements = self._create_task_requirements(
            task_type,
            scenario,
            learning_objectives
        )
        
        # Define deliverables
        deliverables = self._define_deliverables(task_type, learning_objectives)
        
        # Create authentic assessment rubric criteria
        authentic_criteria = self._create_authentic_criteria(
            task_type,
            deliverables
        )
        
        authentic_assessment = {
            "authentic_id": authentic_id,
            "task_type": task_type,
            "learning_objectives": learning_objectives,
            "scenario": scenario,
            "requirements": requirements,
            "deliverables": deliverables,
            "authentic_criteria": authentic_criteria,
            "context": context,
            "estimated_duration_weeks": self._estimate_authentic_duration(task_type),
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.assessment_database[authentic_id] = authentic_assessment
        
        return authentic_assessment
    
    def generate_formative_assessment(self, lesson_context: Dict) -> Dict:
        """Generate formative assessment for ongoing learning monitoring"""
        formative_id = f"formative_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Determine formative assessment strategies
        strategies = self._select_formative_strategies(lesson_context)
        
        # Generate formative activities
        formative_activities = self._generate_formative_activities(
            strategies,
            lesson_context
        )
        
        # Create formative feedback mechanisms
        feedback_mechanisms = self._create_feedback_mechanisms(strategies)
        
        # Set formative assessment timeline
        timeline = self._set_formative_timeline(lesson_context)
        
        formative_assessment = {
            "formative_id": formative_id,
            "strategies": strategies,
            "formative_activities": formative_activities,
            "feedback_mechanisms": feedback_mechanisms,
            "timeline": timeline,
            "lesson_context": lesson_context,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.assessment_database[formative_id] = formative_assessment
        
        return formative_assessment
    
    def generate_summative_assessment(self, unit_context: Dict) -> Dict:
        """Generate summative assessment for end of unit evaluation"""
        summative_id = f"summative_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Determine summative assessment structure
        structure = self._determine_summative_structure(unit_context)
        
        # Generate summative sections
        sections = self._generate_summative_sections(
            structure,
            unit_context
        )
        
        # Create summative scoring guidelines
        scoring_guidelines = self._create_scoring_guidelines(
            structure,
            sections
        )
        
        # Set summative assessment logistics
        logistics = self._set_summative_logistics(unit_context)
        
        summative_assessment = {
            "summative_id": summative_id,
            "structure": structure,
            "sections": sections,
            "scoring_guidelines": scoring_guidelines,
            "logistics": logistics,
            "unit_context": unit_context,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.assessment_database[summative_id] = summative_assessment
        
        return summative_assessment
    
    def _determine_assessment_type(self, context: Dict) -> AssessmentType:
        """Determine appropriate assessment type based on context"""
        assessment_purpose = context.get("assessment_purpose", "evaluation")
        learning_phase = context.get("learning_phase", "ongoing")
        
        if assessment_purpose == "pre_assessment":
            return AssessmentType.DIAGNOSTIC
        elif learning_phase == "ongoing" and assessment_purpose == "monitoring":
            return AssessmentType.FORMATIVE
        elif learning_phase == "complete" and assessment_purpose == "evaluation":
            return AssessmentType.SUMMATIVE
        elif context.get("authentic_required", False):
            return AssessmentType.AUTHENTIC
        else:
            return AssessmentType.PERFORMANCE
    
    def _select_assessment_template(self, assessment_type: AssessmentType, context: Dict) -> Dict:
        """Select appropriate assessment template"""
        subject = context.get("subject", "general")
        grade = context.get("grade", "1")
        
        template_key = f"{assessment_type.value}_{subject}_{grade}"
        
        if template_key in self.assessment_templates:
            return self.assessment_templates[template_key]
        else:
            # Return default template
            return {
                "template_id": f"default_{assessment_type.value}",
                "type": assessment_type.value,
                "subject": subject,
                "grade": grade,
                "sections": self._get_default_sections(assessment_type)
            }
    
    def _get_default_sections(self, assessment_type: AssessmentType) -> List[str]:
        """Get default sections for assessment type"""
        sections_map = {
            AssessmentType.AUTHENTIC: ["scenario", "task", "deliverables", "criteria"],
            AssessmentType.FORMATIVE: ["check_in", "quick_assessment", "feedback"],
            AssessmentType.SUMMATIVE: ["knowledge", "application", "analysis", "evaluation"],
            AssessmentType.DIAGNOSTIC: ["pre_concept_check", "skill_pre_assessment"],
            AssessmentType.PERFORMANCE: ["task_description", "performance_criteria", "demonstration"]
        }
        
        return sections_map.get(assessment_type, ["general_assessment"])
    
    def _generate_assessment_content(self, template: Dict, context: Dict, assessment_type: AssessmentType) -> Dict:
        """Generate assessment content based on template"""
        sections = template.get("sections", [])
        content = {}
        
        for section in sections:
            content[section] = self._generate_section_content(
                section,
                context,
                assessment_type
            )
        
        return content
    
    def _generate_section_content(self, section: str, context: Dict, assessment_type: AssessmentType) -> Dict:
        """Generate content for specific section"""
        subject = context.get("subject", "subject")
        
        if section == "scenario":
            return {
                "description": f"Authentic scenario for {subject}",
                "context": "Real-world application context",
                "relevance": "Connects to student experience"
            }
        elif section == "task":
            return {
                "task_description": f"{subject} application task",
                "requirements": ["Task requirement 1", "Task requirement 2"],
                "complexity": "moderate"
            }
        elif section == "deliverables":
            return {
                "deliverable_1": "Written response",
                "deliverable_2": "Practical demonstration",
                "deliverable_3": "Reflection"
            }
        elif section == "criteria":
            return {
                "criterion_1": {"description": "Content mastery", "weight": 0.4},
                "criterion_2": {"description": "Application skill", "weight": 0.3},
                "criterion_3": {"description": "Communication", "weight": 0.3}
            }
        else:
            return {
                "section_name": section,
                "content": f"Content for {section} in {subject}"
            }
    
    def _align_with_learning_objectives(self, learning_objectives: List[str], assessment_content: Dict) -> List[Dict]:
        """Align assessment content with learning objectives"""
        aligned = []
        
        for i, objective in enumerate(learning_objectives):
            aligned.append({
                "objective_id": f"obj_{i+1}",
                "objective_text": objective,
                "assessment_items": self._generate_assessment_items_for_objective(objective),
                "alignment_score": 0.85
            })
        
        return aligned
    
    def _generate_assessment_items_for_objective(self, objective: str) -> List[str]:
        """Generate assessment items for specific learning objective"""
        return [
            f"Item 1: Assess {objective}",
            f"Item 2: Apply {objective}",
            f"Item 3: Evaluate {objective}"
        ]
    
    def _add_authentic_elements(self, assessment_type: AssessmentType, context: Dict) -> Dict:
        """Add authentic assessment elements"""
        if assessment_type == AssessmentType.AUTHENTIC:
            return {
                "real_world_context": True,
                "student_choice": True,
                "collaboration": context.get("collaboration_required", False),
                "reflection_component": True,
                "audience_beyond_teacher": True
            }
        else:
            return {
                "real_world_context": False,
                "student_choice": False,
                "collaboration": False,
                "reflection_component": False,
                "audience_beyond_teacher": False
            }
    
    def _generate_assessment_criteria(self, assessment_type: AssessmentType, aligned_objectives: List[Dict]) -> List[Dict]:
        """Generate assessment criteria based on aligned objectives"""
        criteria = []
        
        for objective in aligned_objectives:
            criteria.append({
                "criterion_id": f"crit_{objective['objective_id']}",
                "description": f"Mastery of {objective['objective_text']}",
                "weight": 1.0 / len(aligned_objectives),
                "proficiency_levels": {
                    "exceeds": "Demonstrates deep understanding and application",
                    "meets": "Demonstrates solid understanding and application",
                    "approaching": "Demonstrates developing understanding",
                    "below": "Needs additional support"
                }
            })
        
        return criteria
    
    def _estimate_duration(self, assessment_content: Dict) -> str:
        """Estimate assessment duration based on content"""
        num_sections = len(assessment_content)
        
        if num_sections <= 2:
            return "30-45 minutes"
        elif num_sections <= 4:
            return "45-60 minutes"
        else:
            return "60-90 minutes"
    
    def _select_authentic_task_type(self, context: Dict) -> str:
        """Select authentic task type based on context"""
        subject = context.get("subject", "general")
        
        task_types = {
            "IPA": ["investigation", "experiment", "research_project"],
            "Matematika": ["problem_solving", "data_analysis", "real_world_application"],
            "Bahasa Indonesia": ["writing_project", "presentation", "debate"],
            "IPS": ["case_study", "research_project", "simulation"],
            "Seni Budaya": ["creative_project", "performance", "exhibition"]
        }
        
        available_tasks = task_types.get(subject, ["project_based"])
        return available_tasks[0] if available_tasks else "project_based"
    
    def _generate_authentic_scenario(self, task_type: str, context: Dict) -> Dict:
        """Generate authentic scenario for task"""
        subject = context.get("subject", "subject")
        grade = context.get("grade", "1")
        
        return {
            "scenario_type": task_type,
            "real_world_context": f"Real-world application of {subject} for grade {grade}",
            "stakeholders": ["students", "teachers", "community"],
            "constraints": ["time_limit", "resource_availability"],
            "opportunities": ["student_choice", "creative_solution"]
        }
    
    def _create_task_requirements(self, task_type: str, scenario: Dict, learning_objectives: List[str]) -> List[str]:
        """Create task requirements based on scenario and objectives"""
        return [
            f"Apply {objective} in {task_type} context"
            for objective in learning_objectives
        ]
    
    def _define_deliverables(self, task_type: str, learning_objectives: List[str]) -> List[Dict]:
        """Define deliverables for authentic task"""
        deliverables = []
        
        if task_type in ["investigation", "research_project"]:
            deliverables.append({
                "deliverable": "Research Report",
                "format": "Written document",
                "length": "3-5 pages"
            })
            deliverables.append({
                "deliverable": "Presentation",
                "format": "Oral presentation",
                "duration": "10-15 minutes"
            })
        
        deliverables.append({
            "deliverable": "Reflection",
            "format": "Written reflection",
            "length": "1-2 pages"
        })
        
        return deliverables
    
    def _create_authentic_criteria(self, task_type: str, deliverables: List[Dict]) -> Dict:
        """Create authentic assessment criteria"""
        return {
            "content_quality": {
                "exceeds": "Exceptional depth and insight",
                "meets": "Solid content and understanding",
                "approaching": "Developing content quality",
                "below": "Needs significant improvement"
            },
            "application": {
                "exceeds": "Sophisticated application in context",
                "meets": "Competent application",
                "approaching": "Basic application",
                "below": "Limited application"
            },
            "communication": {
                "exceeds": "Clear, engaging, professional",
                "meets": "Clear and appropriate",
                "approaching": "Somewhat unclear",
                "below": "Difficult to follow"
            }
        }
    
    def _estimate_authentic_duration(self, task_type: str) -> str:
        """Estimate duration for authentic assessment"""
        duration_map = {
            "investigation": "2-3 weeks",
            "experiment": "1-2 weeks",
            "research_project": "3-4 weeks",
            "problem_solving": "1-2 weeks",
            "creative_project": "2-3 weeks"
        }
        
        return duration_map.get(task_type, "2-3 weeks")
    
    def _select_formative_strategies(self, lesson_context: Dict) -> List[str]:
        """Select formative assessment strategies"""
        return [
            "exit_tickets",
            "think_pair_share",
            "quick_writes",
            "classroom_discussions",
            "observation_checklists"
        ]
    
    def _generate_formative_activities(self, strategies: List[str], lesson_context: Dict) -> List[Dict]:
        """Generate formative assessment activities"""
        activities = []
        
        for strategy in strategies:
            activities.append({
                "strategy": strategy,
                "activity_description": f"Formative activity using {strategy}",
                "timing": "during_lesson",
                "format": "individual_or_group"
            })
        
        return activities
    
    def _create_feedback_mechanisms(self, strategies: List[str]) -> Dict:
        """Create feedback mechanisms for formative assessment"""
        return {
            "immediate_feedback": True,
            "peer_feedback": "discussion" in strategies,
            "self_assessment": "reflection" in strategies,
            "teacher_feedback": True
        }
    
    def _set_formative_timeline(self, lesson_context: Dict) -> Dict:
        """Set timeline for formative assessment"""
        return {
            "frequency": "ongoing_during_lesson",
            "check_points": ["lesson_start", "mid_lesson", "lesson_end"],
            "immediate_action": True
        }
    
    def _determine_summative_structure(self, unit_context: Dict) -> Dict:
        """Determine structure for summative assessment"""
        return {
            "format": "mixed_format",
            "sections": ["multiple_choice", "short_answer", "extended_response"],
            "time_limit": "60-90 minutes",
            "total_points": 100
        }
    
    def _generate_summative_sections(self, structure: Dict, unit_context: Dict) -> List[Dict]:
        """Generate sections for summative assessment"""
        sections = []
        
        sections.append({
            "section": "multiple_choice",
            "item_count": 20,
            "points_per_item": 2,
            "total_points": 40
        })
        
        sections.append({
            "section": "short_answer",
            "item_count": 5,
            "points_per_item": 8,
            "total_points": 40
        })
        
        sections.append({
            "section": "extended_response",
            "item_count": 2,
            "points_per_item": 10,
            "total_points": 20
        })
        
        return sections
    
    def _create_scoring_guidelines(self, structure: Dict, sections: List[Dict]) -> Dict:
        """Create scoring guidelines for summative assessment"""
        return {
            "scoring_method": "point_based",
            "rubric_required": ["extended_response"],
            "partial_credit": True,
            "proficiency_levels": {
                "advanced": "85-100%",
                "proficient": "70-84%",
                "developing": "55-69%",
                "emerging": "0-54%"
            }
        }
    
    def _set_summative_logistics(self, unit_context: Dict) -> Dict:
        """Set logistics for summative assessment"""
        return {
            "administration": "teacher_supervised",
            "materials_needed": ["assessment_paper", "writing_implements"],
            "accommodations": "available_as_needed",
            "review_process": "teacher_grading"
        }
    
    def _initialize_assessment_templates(self) -> Dict:
        """Initialize assessment templates"""
        return {
            "authentic_IPA_1": {
                "template_id": "authentic_IPA_1",
                "type": "authentic",
                "subject": "IPA",
                "grade": "1",
                "sections": ["scenario", "investigation", "report", "presentation"]
            },
            "formative_Matematika_3": {
                "template_id": "formative_Matematika_3",
                "type": "formative",
                "subject": "Matematika",
                "grade": "3",
                "sections": ["check_in", "problem_solving", "reflection"]
            },
            "summative_Bahasa_5": {
                "template_id": "summative_Bahasa_5",
                "type": "summative",
                "subject": "Bahasa Indonesia",
                "grade": "5",
                "sections": ["reading_comprehension", "writing", "listening", "speaking"]
            }
        }
    
    def _initialize_authentic_tasks(self) -> Dict:
        """Initialize authentic task library"""
        return {
            "investigation": {
                "task_type": "investigation",
                "description": "Scientific investigation with inquiry process",
                "typical_duration": "2-3 weeks"
            },
            "project_based": {
                "task_type": "project_based",
                "description": "Project-based learning with real application",
                "typical_duration": "3-4 weeks"
            },
            "case_study": {
                "task_type": "case_study",
                "description": "Analysis of real-world case",
                "typical_duration": "1-2 weeks"
            },
            "simulation": {
                "task_type": "simulation",
                "description": "Simulation of real-world scenario",
                "typical_duration": "1-2 weeks"
            }
        }