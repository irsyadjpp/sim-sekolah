"""
gRPC Server Implementation - Educational Intelligence Service
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
    import educational_intelligence_pb2 as pb2
    import educational_intelligence_pb2_grpc as pb2_grpc
except ImportError:
    print("Error: gRPC stub files not found. Please compile proto files first.")
    sys.exit(1)

from main import (
    EducationalIntelligenceEngine,
    PersonalizedLearningRequest,
    LearningPatternRequest,
    AdaptiveAssessmentRequest,
    AssessmentAnalysisRequest,
    CurriculumPlanRequest,
    ContentAlignmentRequest,
    LearningGraphRequest,
    LearningPathAnalysisRequest,
    ProgressionTrackingRequest,
    LearningOutcomesRequest,
    PedagogyRequest,
    EffectivenessEvaluationRequest,
    ContentRecommendationRequest,
    ActivityRecommendationRequest
)

logger = logging.getLogger(__name__)


class EducationalIntelligenceServicer:
    """gRPC Servicer for Educational Intelligence Service - wraps 7 engines"""
    
    def __init__(self):
        self.engine = EducationalIntelligenceEngine()
        logger.info("Educational Intelligence Servicer initialized with EducationalIntelligenceEngine")
    
    # Helper function to convert dict to protobuf map
    def _dict_to_map(self, data):
        """Convert dictionary to protobuf map"""
        return {str(k): str(v) for k, v in (data or {}).items()}
    
    # Helper function to convert list to protobuf repeated field
    def _list_to_repeated(self, data):
        """Convert list to protobuf repeated field"""
        return list(data or [])
    
    # ==================== Adaptive Learning Engine Methods ====================
    
    def GeneratePersonalizedLearningPath(self, request, context):
        """Generate personalized learning path"""
        logger.info(f"GeneratePersonalizedLearningPath called: {request.request_id}")
        
        try:
            internal_request = PersonalizedLearningRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                subject=request.subject,
                current_competencies=list(request.current_competencies),
                learning_objectives=list(request.learning_objectives),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.adaptive_learning_engine.generate_personalized_learning_path(internal_request)
            
            return pb2.LearningPathResponse(
                request_id=request.request_id,
                success=True,
                message="Personalized learning path generated successfully",
                learning_path=self._dict_to_map(result.get("learning_path", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in GeneratePersonalizedLearningPath: {e}")
            return pb2.LearningPathResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                learning_path={},
                metadata={}
            )
    
    def AnalyzeStudentLearningPattern(self, request, context):
        """Analyze student learning patterns"""
        logger.info(f"AnalyzeStudentLearningPattern called: {request.request_id}")
        
        try:
            internal_request = LearningPatternRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                subject=request.subject,
                time_period_days=request.time_period_days
            )
            
            result = self.engine.adaptive_learning_engine.analyze_student_learning_pattern(internal_request)
            
            return pb2.PatternAnalysisResponse(
                request_id=request.request_id,
                success=True,
                message="Learning pattern analysis completed",
                pattern_analysis=self._dict_to_map(result.get("pattern_analysis", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in AnalyzeStudentLearningPattern: {e}")
            return pb2.PatternAnalysisResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                pattern_analysis={},
                metadata={}
            )
    
    # ==================== Assessment Engine Methods ====================
    
    def GenerateAdaptiveAssessment(self, request, context):
        """Generate adaptive assessment"""
        logger.info(f"GenerateAdaptiveAssessment called: {request.request_id}")
        
        try:
            internal_request = AdaptiveAssessmentRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                topic=request.topic,
                competency=request.competency,
                difficulty_level=request.difficulty_level,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.assessment_engine.generate_adaptive_assessment(internal_request)
            
            return pb2.AdaptiveAssessmentResponse(
                request_id=request.request_id,
                success=True,
                message="Adaptive assessment generated successfully",
                assessment=self._dict_to_map(result.get("assessment", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in GenerateAdaptiveAssessment: {e}")
            return pb2.AdaptiveAssessmentResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                assessment={},
                metadata={}
            )
    
    def AnalyzeAssessmentResults(self, request, context):
        """Analyze assessment results"""
        logger.info(f"AnalyzeAssessmentResults called: {request.request_id}")
        
        try:
            # Convert student assessment results from protobuf
            results = []
            for result in request.results:
                results.append({
                    "student_id": result.student_id,
                    "scores": dict(result.scores)
                })
            
            internal_request = AssessmentAnalysisRequest(
                request_id=request.request_id,
                assessment_id=request.assessment_id,
                results=results
            )
            
            result = self.engine.assessment_engine.analyze_assessment_results(internal_request)
            
            return pb2.AssessmentAnalysisResponse(
                request_id=request.request_id,
                success=True,
                message="Assessment analysis completed",
                analysis=self._dict_to_map(result.get("analysis", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in AnalyzeAssessmentResults: {e}")
            return pb2.AssessmentAnalysisResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                analysis={},
                metadata={}
            )
    
    # ==================== Curriculum Engine Methods ====================
    
    def GenerateCurriculumPlan(self, request, context):
        """Generate curriculum plan"""
        logger.info(f"GenerateCurriculumPlan called: {request.request_id}")
        
        try:
            internal_request = CurriculumPlanRequest(
                request_id=request.request_id,
                phase=request.phase,
                grade=request.grade,
                subject=request.subject,
                competencies=list(request.competencies),
                time_allocation_weeks=request.time_allocation_weeks
            )
            
            result = self.engine.curriculum_engine.generate_curriculum_plan(internal_request)
            
            return pb2.CurriculumPlanResponse(
                request_id=request.request_id,
                success=True,
                message="Curriculum plan generated successfully",
                curriculum_plan=self._dict_to_map(result.get("curriculum_plan", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in GenerateCurriculumPlan: {e}")
            return pb2.CurriculumPlanResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                curriculum_plan={},
                metadata={}
            )
    
    def AlignContentWithStandards(self, request, context):
        """Align content with educational standards"""
        logger.info(f"AlignContentWithStandards called: {request.request_id}")
        
        try:
            internal_request = ContentAlignmentRequest(
                request_id=request.request_id,
                content=self._dict_to_map(request.content),
                framework=request.framework,
                grade=request.grade,
                subject=request.subject
            )
            
            result = self.engine.curriculum_engine.align_content_with_standards(internal_request)
            
            return pb2.AlignmentResponse(
                request_id=request.request_id,
                success=True,
                message="Content alignment completed",
                alignment_result=self._dict_to_map(result.get("alignment_result", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in AlignContentWithStandards: {e}")
            return pb2.AlignmentResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                alignment_result={},
                metadata={}
            )
    
    # ==================== Learning Graph Engine Methods ====================
    
    def BuildLearningGraph(self, request, context):
        """Build learning graph"""
        logger.info(f"BuildLearningGraph called: {request.request_id}")
        
        try:
            internal_request = LearningGraphRequest(
                request_id=request.request_id,
                subject=request.subject,
                phase=request.phase,
                competencies=list(request.competencies),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.learning_graph_engine.build_learning_graph(internal_request)
            
            return pb2.LearningGraphResponse(
                request_id=request.request_id,
                success=True,
                message="Learning graph built successfully",
                learning_graph=self._dict_to_map(result.get("learning_graph", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in BuildLearningGraph: {e}")
            return pb2.LearningGraphResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                learning_graph={},
                metadata={}
            )
    
    def AnalyzeLearningPath(self, request, context):
        """Analyze learning path"""
        logger.info(f"AnalyzeLearningPath called: {request.request_id}")
        
        try:
            internal_request = LearningPathAnalysisRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                subject=request.subject,
                target_competency=request.target_competency
            )
            
            result = self.engine.learning_graph_engine.analyze_learning_path(internal_request)
            
            return pb2.PathAnalysisResponse(
                request_id=request.request_id,
                success=True,
                message="Learning path analysis completed",
                path_analysis=self._dict_to_map(result.get("path_analysis", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in AnalyzeLearningPath: {e}")
            return pb2.PathAnalysisResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                path_analysis={},
                metadata={}
            )
    
    # ==================== Learning Progression Engine Methods ====================
    
    def TrackStudentProgression(self, request, context):
        """Track student progression"""
        logger.info(f"TrackStudentProgression called: {request.request_id}")
        
        try:
            internal_request = ProgressionTrackingRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                subject=request.subject,
                competencies=list(request.competencies)
            )
            
            result = self.engine.learning_progression_engine.track_student_progression(internal_request)
            
            return pb2.ProgressionResponse(
                request_id=request.request_id,
                success=True,
                message="Student progression tracked successfully",
                progression_data=self._dict_to_map(result.get("progression_data", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in TrackStudentProgression: {e}")
            return pb2.ProgressionResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                progression_data={},
                metadata={}
            )
    
    def PredictLearningOutcomes(self, request, context):
        """Predict learning outcomes"""
        logger.info(f"PredictLearningOutcomes called: {request.request_id}")
        
        try:
            internal_request = LearningOutcomesRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                subject=request.subject,
                current_progress=list(request.current_progress)
            )
            
            result = self.engine.learning_progression_engine.predict_learning_outcomes(internal_request)
            
            return pb2.OutcomesResponse(
                request_id=request.request_id,
                success=True,
                message="Learning outcomes predicted successfully",
                predicted_outcomes=self._dict_to_map(result.get("predicted_outcomes", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in PredictLearningOutcomes: {e}")
            return pb2.OutcomesResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                predicted_outcomes={},
                metadata={}
            )
    
    # ==================== Pedagogy Engine Methods ====================
    
    def RecommendPedagogyStrategy(self, request, context):
        """Recommend pedagogy strategy"""
        logger.info(f"RecommendPedagogyStrategy called: {request.request_id}")
        
        try:
            internal_request = PedagogyRequest(
                request_id=request.request_id,
                topic=request.topic,
                grade=request.grade,
                subject=request.subject,
                class_size=request.class_size,
                learning_objectives=list(request.learning_objectives),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.pedagogy_engine.recommend_pedagogy_strategy(internal_request)
            
            return pb2.PedagogyResponse(
                request_id=request.request_id,
                success=True,
                message="Pedagogy strategy recommendation completed",
                pedagogy_recommendations=self._dict_to_map(result.get("pedagogy_recommendations", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in RecommendPedagogyStrategy: {e}")
            return pb2.PedagogyResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                pedagogy_recommendations={},
                metadata={}
            )
    
    def EvaluateTeachingEffectiveness(self, request, context):
        """Evaluate teaching effectiveness"""
        logger.info(f"EvaluateTeachingEffectiveness called: {request.request_id}")
        
        try:
            internal_request = EffectivenessEvaluationRequest(
                request_id=request.request_id,
                pedagogy_type=request.pedagogy_type,
                subject=request.subject,
                grade=request.grade,
                assessment_data=list(request.assessment_data)
            )
            
            result = self.engine.pedagogy_engine.evaluate_teaching_effectiveness(internal_request)
            
            return pb2.EffectivenessResponse(
                request_id=request.request_id,
                success=True,
                message="Teaching effectiveness evaluation completed",
                effectiveness_data=self._dict_to_map(result.get("effectiveness_data", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in EvaluateTeachingEffectiveness: {e}")
            return pb2.EffectivenessResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                effectiveness_data={},
                metadata={}
            )
    
    # ==================== Recommendation Engine Methods ====================
    
    def GenerateContentRecommendations(self, request, context):
        """Generate content recommendations"""
        logger.info(f"GenerateContentRecommendations called: {request.request_id}")
        
        try:
            internal_request = ContentRecommendationRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                subject=request.subject,
                current_competencies=list(request.current_competencies),
                weak_areas=list(request.weak_areas)
            )
            
            result = self.engine.recommendation_engine.generate_content_recommendations(internal_request)
            
            # Convert recommendations to protobuf format
            recommendations = []
            for rec in result.get("recommendations", []):
                recommendations.append(pb2.Recommendation(
                    content_id=rec.get("content_id", ""),
                    content_type=rec.get("content_type", ""),
                    title=rec.get("title", ""),
                    relevance_score=rec.get("relevance_score", 0.0),
                    rationale=rec.get("rationale", "")
                ))
            
            return pb2.RecommendationsResponse(
                request_id=request.request_id,
                success=True,
                message="Content recommendations generated successfully",
                recommendations=recommendations,
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in GenerateContentRecommendations: {e}")
            return pb2.RecommendationsResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                recommendations=[],
                metadata={}
            )
    
    def GenerateActivityRecommendations(self, request, context):
        """Generate activity recommendations"""
        logger.info(f"GenerateActivityRecommendations called: {request.request_id}")
        
        try:
            internal_request = ActivityRecommendationRequest(
                request_id=request.request_id,
                student_id=request.student_id,
                subject=request.subject,
                topic=request.topic,
                learning_objectives=list(request.learning_objectives)
            )
            
            result = self.engine.recommendation_engine.generate_activity_recommendations(internal_request)
            
            # Convert recommendations to protobuf format
            recommendations = []
            for rec in result.get("recommendations", []):
                recommendations.append(pb2.Recommendation(
                    content_id=rec.get("content_id", ""),
                    content_type=rec.get("content_type", ""),
                    title=rec.get("title", ""),
                    relevance_score=rec.get("relevance_score", 0.0),
                    rationale=rec.get("rationale", "")
                ))
            
            return pb2.RecommendationsResponse(
                request_id=request.request_id,
                success=True,
                message="Activity recommendations generated successfully",
                recommendations=recommendations,
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in GenerateActivityRecommendations: {e}")
            return pb2.RecommendationsResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                recommendations=[],
                metadata={}
            )


def serve_adaptive_learning(port: int = 50075):
    """Start the Adaptive Learning Engine gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Adaptive Learning Engine gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = EducationalIntelligenceServicer()
    pb2_grpc.add_AdaptiveLearningEngineServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Adaptive Learning Engine gRPC Server started successfully on port {port}")
    logger.info("Available methods: 2 (GeneratePersonalizedLearningPath, AnalyzeStudentLearningPattern)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


def serve_assessment(port: int = 50076):
    """Start the Assessment Engine gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Assessment Engine gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = EducationalIntelligenceServicer()
    pb2_grpc.add_AssessmentEngineServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Assessment Engine gRPC Server started successfully on port {port}")
    logger.info("Available methods: 2 (GenerateAdaptiveAssessment, AnalyzeAssessmentResults)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


def serve_curriculum(port: int = 50077):
    """Start the Curriculum Engine gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Curriculum Engine gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = EducationalIntelligenceServicer()
    pb2_grpc.add_CurriculumEngineServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Curriculum Engine gRPC Server started successfully on port {port}")
    logger.info("Available methods: 2 (GenerateCurriculumPlan, AlignContentWithStandards)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


def serve_learning_graph(port: int = 50078):
    """Start the Learning Graph Engine gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Learning Graph Engine gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = EducationalIntelligenceServicer()
    pb2_grpc.add_LearningGraphEngineServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Learning Graph Engine gRPC Server started successfully on port {port}")
    logger.info("Available methods: 2 (BuildLearningGraph, AnalyzeLearningPath)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


def serve_learning_progression(port: int = 50079):
    """Start the Learning Progression Engine gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Learning Progression Engine gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = EducationalIntelligenceServicer()
    pb2_grpc.add_LearningProgressionEngineServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Learning Progression Engine gRPC Server started successfully on port {port}")
    logger.info("Available methods: 2 (TrackStudentProgression, PredictLearningOutcomes)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


def serve_pedagogy(port: int = 50080):
    """Start the Pedagogy Engine gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Pedagogy Engine gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = EducationalIntelligenceServicer()
    pb2_grpc.add_PedagogyEngineServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Pedagogy Engine gRPC Server started successfully on port {port}")
    logger.info("Available methods: 2 (RecommendPedagogyStrategy, EvaluateTeachingEffectiveness)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


def serve_recommendation(port: int = 50081):
    """Start the Recommendation Engine gRPC server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Recommendation Engine gRPC Server on port {port}")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    servicer = EducationalIntelligenceServicer()
    pb2_grpc.add_RecommendationEngineServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Recommendation Engine gRPC Server started successfully on port {port}")
    logger.info("Available methods: 2 (GenerateContentRecommendations, GenerateActivityRecommendations)")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


if __name__ == "__main__":
    import sys
    
    # Determine which engine to start based on command line argument
    if len(sys.argv) > 1:
        engine = sys.argv[1]
        port = int(os.getenv("GRPC_PORT", "50075"))
        
        if engine == "adaptive-learning":
            serve_adaptive_learning(port)
        elif engine == "assessment":
            serve_assessment(port + 1)
        elif engine == "curriculum":
            serve_curriculum(port + 2)
        elif engine == "learning-graph":
            serve_learning_graph(port + 3)
        elif engine == "learning-progression":
            serve_learning_progression(port + 4)
        elif engine == "pedagogy":
            serve_pedagogy(port + 5)
        elif engine == "recommendation":
            serve_recommendation(port + 6)
        else:
            print(f"Unknown engine: {engine}")
            print("Available engines: adaptive-learning, assessment, curriculum, learning-graph, learning-progression, pedagogy, recommendation")
    else:
        print("Usage: python grpc_server.py <engine_name>")
        print("Available engines: adaptive-learning, assessment, curriculum, learning-graph, learning-progression, pedagogy, recommendation")
