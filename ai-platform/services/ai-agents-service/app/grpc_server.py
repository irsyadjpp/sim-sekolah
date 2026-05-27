"""
gRPC Server Implementation - AI Agents Service
This file contains the gRPC server implementation that wraps the existing engine classes.
"""

import grpc
from concurrent import futures
import asyncio
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import generated protobuf classes
try:
    import ai_agents_pb2 as pb2
    import ai_agents_pb2_grpc as pb2_grpc
except ImportError:
    print("Error: gRPC stub files not found. Please compile proto files first.")
    sys.exit(1)

from main import (
    AIAgentsEngine,
    LessonPlanningRequest,
    AssessmentCreationRequest,
    StudentProgressAnalysisRequest,
    TeachingStrategyRequest,
    PersonalizedGuidanceRequest,
    QuestionAnsweringRequest,
    LearningPathRecommendationRequest,
    AdaptiveInteractionRequest,
    CPGuidanceRequest,
    ATPGuidanceRequest,
    CurriculumAlignmentRequest,
    CurriculumRecommendationRequest,
    ExpertKnowledgeRequest,
    AssessmentGenerationRequest,
    RubricCreationRequest,
    AssessmentAnalyticsRequest,
    QualityValidationRequest
)

logger = logging.getLogger(__name__)


class AIAgentsServicer(pb2_grpc.AIAgentsServiceServicer):
    """gRPC Servicer for AI Agents Service - wraps all 4 agents"""
    
    def __init__(self):
        self.engine = AIAgentsEngine()
        logger.info("AI Agents Servicer initialized with AIAgentsEngine")
    
    # Helper function to convert dict to protobuf map
    def _dict_to_map(self, data):
        """Convert dictionary to protobuf map"""
        return {str(k): str(v) for k, v in (data or {}).items()}
    
    # Helper function to convert list to protobuf repeated field
    def _list_to_repeated(self, data):
        """Convert list to protobuf repeated field"""
        return list(data or [])
    
    # ==================== Teacher Agent Methods ====================
    
    def LessonPlanningAssistant(self, request, context):
        """Lesson planning assistant"""
        logger.info(f"LessonPlanningAssistant called: {request.request_id}")
        
        try:
            internal_request = LessonPlanningRequest(
                request_id=request.request_id,
                topic=request.topic,
                grade=request.grade,
                subject=request.subject,
                duration_minutes=request.duration_minutes,
                learning_objectives=list(request.learning_objectives),
                pedagogy_type=request.pedagogy_type,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.lesson_planning_assistant(internal_request)
            
            return pb2.LessonPlanningResponse(
                request_id=request.request_id,
                success=True,
                message="Lesson planning completed successfully",
                lesson_plan=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in LessonPlanningAssistant: {e}")
            return pb2.LessonPlanningResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                lesson_plan={},
                metadata={}
            )
    
    def AssessmentCreationAssistant(self, request, context):
        """Assessment creation assistant"""
        logger.info(f"AssessmentCreationAssistant called: {request.request_id}")
        
        try:
            internal_request = AssessmentCreationRequest(
                request_id=request.request_id,
                topic=request.topic,
                competency=request.competency,
                grade=request.grade,
                assessment_type=request.assessment_type,
                question_count=request.question_count,
                difficulty=request.difficulty,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.assessment_creation_assistant(internal_request)
            
            return pb2.AssessmentCreationResponse(
                request_id=request.request_id,
                success=True,
                message="Assessment creation completed successfully",
                assessment=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in AssessmentCreationAssistant: {e}")
            return pb2.AssessmentCreationResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                assessment={},
                metadata={}
            )
    
    def StudentProgressAnalysis(self, request, context):
        """Student progress analysis"""
        logger.info(f"StudentProgressAnalysis called: {request.request_id}")
        
        try:
            internal_request = StudentProgressAnalysisRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                subject=request.subject,
                time_period=request.time_period,
                include_recommendations=request.include_recommendations
            )
            
            result = self.engine.student_progress_analysis(internal_request)
            
            return pb2.StudentProgressAnalysisResponse(
                request_id=request.request_id,
                success=True,
                message="Student progress analysis completed",
                progress_data=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in StudentProgressAnalysis: {e}")
            return pb2.StudentProgressAnalysisResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                progress_data={},
                metadata={}
            )
    
    def TeachingStrategyRecommendation(self, request, context):
        """Teaching strategy recommendation"""
        logger.info(f"TeachingStrategyRecommendation called: {request.request_id}")
        
        try:
            # Convert student profiles from protobuf to internal format
            student_profiles = []
            for sp in request.student_profiles:
                student_profiles.append({
                    "student_id": sp.student_id,
                    "profile_data": self._dict_to_map(sp.profile_data)
                })
            
            internal_request = TeachingStrategyRequest(
                request_id=request.request_id,
                topic=request.topic,
                grade=request.grade,
                subject=request.subject,
                class_size=request.class_size,
                available_resources=list(request.available_resources),
                student_profiles=student_profiles
            )
            
            result = self.engine.teaching_strategy_recommendation(internal_request)
            
            return pb2.TeachingStrategyResponse(
                request_id=request.request_id,
                success=True,
                message="Teaching strategy recommendation completed",
                strategy=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in TeachingStrategyRecommendation: {e}")
            return pb2.TeachingStrategyResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                strategy={},
                metadata={}
            )
    
    # ==================== Student Learning Agent Methods ====================
    
    def PersonalizedGuidance(self, request, context):
        """Personalized learning guidance"""
        logger.info(f"PersonalizedGuidance called: {request.request_id}")
        
        try:
            internal_request = PersonalizedGuidanceRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                subject=request.subject,
                current_topic=request.current_topic,
                learning_style=request.learning_style if request.learning_style else None,
                weak_areas=list(request.weak_areas),
                strong_areas=list(request.strong_areas)
            )
            
            result = self.engine.personal_guidance_assistant(internal_request)
            
            return pb2.PersonalizedGuidanceResponse(
                request_id=request.request_id,
                success=True,
                message="Personalized guidance completed",
                guidance=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in PersonalizedGuidance: {e}")
            return pb2.PersonalizedGuidanceResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                guidance={},
                metadata={}
            )
    
    def QuestionAnswering(self, request, context):
        """Question answering"""
        logger.info(f"QuestionAnswering called: {request.request_id}")
        
        try:
            # Convert conversation history from protobuf to internal format
            conversation_history = []
            for conv in request.conversation_history:
                conversation_history.append({
                    "role": conv.role,
                    "content": conv.content,
                    "timestamp": conv.timestamp
                })
            
            internal_request = QuestionAnsweringRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                question=request.question,
                subject=request.subject,
                context=self._dict_to_map(request.context) if request.context else None,
                conversation_history=conversation_history
            )
            
            result = self.engine.question_answering_assistant(internal_request)
            
            return pb2.QuestionAnsweringResponse(
                request_id=request.request_id,
                success=True,
                message="Question answering completed",
                answer=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in QuestionAnswering: {e}")
            return pb2.QuestionAnsweringResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                answer={},
                metadata={}
            )
    
    def LearningPathRecommendation(self, request, context):
        """Learning path recommendation"""
        logger.info(f"LearningPathRecommendation called: {request.request_id}")
        
        try:
            # Convert current_mastery from protobuf map to internal dict
            current_mastery = {k: float(v) for k, v in request.current_mastery.items()}
            
            internal_request = LearningPathRecommendationRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                target_competency=request.target_competency,
                current_mastery=current_mastery,
                learning_style=request.learning_style if request.learning_style else None,
                time_constraint=request.time_constraint if request.time_constraint else None
            )
            
            result = self.engine.learning_path_recommendation_assistant(internal_request)
            
            return pb2.LearningPathRecommendationResponse(
                request_id=request.request_id,
                success=True,
                message="Learning path recommendation completed",
                learning_path=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in LearningPathRecommendation: {e}")
            return pb2.LearningPathRecommendationResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                learning_path={},
                metadata={}
            )
    
    def AdaptiveInteraction(self, request, context):
        """Adaptive interaction"""
        logger.info(f"AdaptiveInteraction called: {request.request_id}")
        
        try:
            internal_request = AdaptiveInteractionRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                subject=request.subject,
                interaction_data=self._dict_to_map(request.interaction_data)
            )
            
            result = self.engine.adaptive_interaction(internal_request)
            
            return pb2.AdaptiveInteractionResponse(
                request_id=request.request_id,
                success=True,
                message="Adaptive interaction completed",
                adaptive_response=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in AdaptiveInteraction: {e}")
            return pb2.AdaptiveInteractionResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                adaptive_response={},
                metadata={}
            )
    
    # ==================== Curriculum Agent Methods ====================
    
    def CPGuidance(self, request, context):
        """CP guidance"""
        logger.info(f"CPGuidance called: {request.request_id}")
        
        try:
            internal_request = CPGuidanceRequest(
                request_id=request.request_id,
                phase=request.phase,
                grade=request.grade,
                subject=request.subject,
                current_cp=self._dict_to_map(request.current_cp) if request.current_cp else None
            )
            
            result = self.engine.cp_guidance_assistant(internal_request)
            
            return pb2.CPGuidanceResponse(
                request_id=request.request_id,
                success=True,
                message="CP guidance completed",
                guidance=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in CPGuidance: {e}")
            return pb2.CPGuidanceResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                guidance={},
                metadata={}
            )
    
    def ATPGuidance(self, request, context):
        """ATP guidance"""
        logger.info(f"ATPGuidance called: {request.request_id}")
        
        try:
            # Convert time_allocation from protobuf to internal format
            time_allocation = {k: int(v) for k, v in request.time_allocation.items()}
            
            internal_request = ATPGuidanceRequest(
                request_id=request.request_id,
                cp_id=request.cp_id,
                semester=request.semester,
                time_allocation=time_allocation
            )
            
            result = self.engine.atp_guidance_assistant(internal_request)
            
            return pb2.ATPGuidanceResponse(
                request_id=request.request_id,
                success=True,
                message="ATP guidance completed",
                guidance=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in ATPGuidance: {e}")
            return pb2.ATPGuidanceResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                guidance={},
                metadata={}
            )
    
    def CurriculumAlignmentChecking(self, request, context):
        """Curriculum alignment checking"""
        logger.info(f"CurriculumAlignmentChecking called: {request.request_id}")
        
        try:
            internal_request = CurriculumAlignmentRequest(
                request_id=request.request_id,
                teaching_material=self._dict_to_map(request.teaching_material),
                phase=request.phase,
                grade=request.grade,
                subject=request.subject
            )
            
            result = self.engine.curriculum_alignment_checking_assistant(internal_request)
            
            return pb2.CurriculumAlignmentResponse(
                request_id=request.request_id,
                success=True,
                message="Curriculum alignment checking completed",
                alignment_result=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in CurriculumAlignmentChecking: {e}")
            return pb2.CurriculumAlignmentResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                alignment_result={},
                metadata={}
            )
    
    def CurriculumRecommendation(self, request, context):
        """Curriculum recommendation"""
        logger.info(f"CurriculumRecommendation called: {request.request_id}")
        
        try:
            # Convert current_coverage from protobuf to internal format
            current_coverage = {k: float(v) for k, v in request.current_coverage.items()}
            
            internal_request = CurriculumRecommendationRequest(
                request_id=request.request_id,
                phase=request.phase,
                grade=request.grade,
                subject=request.subject,
                current_coverage=current_coverage
            )
            
            result = self.engine.curriculum_recommendation_assistant(internal_request)
            
            return pb2.CurriculumRecommendationResponse(
                request_id=request.request_id,
                success=True,
                message="Curriculum recommendation completed",
                recommendations=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in CurriculumRecommendation: {e}")
            return pb2.CurriculumRecommendationResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                recommendations={},
                metadata={}
            )
    
    def ExpertKnowledgeIntegration(self, request, context):
        """Expert knowledge integration"""
        logger.info(f"ExpertKnowledgeIntegration called: {request.request_id}")
        
        try:
            internal_request = ExpertKnowledgeRequest(
                request_id=request.request_id,
                query=request.query,
                context=self._dict_to_map(request.context)
            )
            
            result = self.engine.expert_knowledge_integration_assistant(internal_request)
            
            return pb2.ExpertKnowledgeResponse(
                request_id=request.request_id,
                success=True,
                message="Expert knowledge integration completed",
                expert_guidance=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in ExpertKnowledgeIntegration: {e}")
            return pb2.ExpertKnowledgeResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                expert_guidance={},
                metadata={}
            )
    
    # ==================== Assessment Agent Methods ====================
    
    def AssessmentGenerationAssistant(self, request, context):
        """Assessment generation assistant"""
        logger.info(f"AssessmentGenerationAssistant called: {request.request_id}")
        
        try:
            internal_request = AssessmentGenerationRequest(
                request_id=request.request_id,
                topic=request.topic,
                competency=request.competency,
                grade=request.grade,
                assessment_type=request.assessment_type,
                cognitive_levels=list(request.cognitive_levels),
                question_count=request.question_count
            )
            
            result = self.engine.assessment_generation_assistant(internal_request)
            
            return pb2.AssessmentGenerationResponse(
                request_id=request.request_id,
                success=True,
                message="Assessment generation completed",
                assessment=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in AssessmentGenerationAssistant: {e}")
            return pb2.AssessmentGenerationResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                assessment={},
                metadata={}
            )
    
    def RubricCreationAssistant(self, request, context):
        """Rubric creation assistant"""
        logger.info(f"RubricCreationAssistant called: {request.request_id}")
        
        try:
            internal_request = RubricCreationRequest(
                request_id=request.request_id,
                assessment_type=request.assessment_type,
                criteria=list(request.criteria),
                performance_levels=request.performance_levels,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.rubric_creation_assistant(internal_request)
            
            return pb2.RubricCreationResponse(
                request_id=request.request_id,
                success=True,
                message="Rubric creation completed",
                rubric=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in RubricCreationAssistant: {e}")
            return pb2.RubricCreationResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                rubric={},
                metadata={}
            )
    
    def AssessmentAnalytics(self, request, context):
        """Assessment analytics"""
        logger.info(f"AssessmentAnalytics called: {request.request_id}")
        
        try:
            internal_request = AssessmentAnalyticsRequest(
                request_id=request.request_id,
                assessment_id=request.assessment_id,
                class_id=request.class_id,
                analysis_type=request.analysis_type
            )
            
            result = self.engine.assessment_analytics_assistant(internal_request)
            
            return pb2.AssessmentAnalyticsResponse(
                request_id=request.request_id,
                success=True,
                message="Assessment analytics completed",
                analytics=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in AssessmentAnalytics: {e}")
            return pb2.AssessmentAnalyticsResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                analytics={},
                metadata={}
            )
    
    def QualityValidation(self, request, context):
        """Quality validation"""
        logger.info(f"QualityValidation called: {request.request_id}")
        
        try:
            internal_request = QualityValidationRequest(
                request_id=request.request_id,
                assessment_data=self._dict_to_map(request.assessment_data)
            )
            
            result = self.engine.quality_validation_assistant(internal_request)
            
            return pb2.QualityValidationResponse(
                request_id=request.request_id,
                success=True,
                message="Quality validation completed",
                validation_result=self._dict_to_map(result.get("result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in QualityValidation: {e}")
            return pb2.QualityValidationResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                validation_result={},
                metadata={}
            )


def serve(port: int = 50072):
    """Start the gRPC server"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting AI Agents gRPC Server on port {port}")
    
    # Create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer
    servicer = AIAgentsServicer()
    pb2_grpc.add_AIAgentsServiceServicer_to_server(servicer, server)
    
    # Start server
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"AI Agents gRPC Server started successfully on port {port}")
    logger.info("Available methods: 16 (4 per agent: Teacher, Student Learning, Curriculum, Assessment)")
    
    # Keep server running
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


if __name__ == "__main__":
    import os
    port = int(os.getenv("GRPC_PORT", "50072"))
    serve(port)
