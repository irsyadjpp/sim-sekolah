"""
gRPC Server Implementation - Educational Observability Service
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
    import educational_observability_pb2 as pb2
    import educational_observability_pb2_grpc as pb2_grpc
except ImportError:
    print("Error: gRPC stub files not found. Please compile proto files first.")
    sys.exit(1)

from main import (
    EducationalObservabilityEngine,
    LearningAnalyticsRequest,
    CompetencyAnalyticsRequest,
    AssessmentQualityMonitoringRequest,
    RetrievalQualityMonitoringRequest,
    PedagogyEffectivenessMonitoringRequest,
    HallucinationMonitoringRequest
)

logger = logging.getLogger(__name__)


class EducationalObservabilityServicer(pb2_grpc.EducationalObservabilityServiceServicer):
    """gRPC Servicer for Educational Observability Service - wraps 6 monitoring dashboards"""
    
    def __init__(self):
        self.engine = EducationalObservabilityEngine()
        logger.info("Educational Observability Servicer initialized with EducationalObservabilityEngine")
    
    # Helper function to convert dict to protobuf map
    def _dict_to_map(self, data):
        """Convert dictionary to protobuf map"""
        return {str(k): str(v) for k, v in (data or {}).items()}
    
    # Helper function to convert list to protobuf repeated field
    def _list_to_repeated(self, data):
        """Convert list to protobuf repeated field"""
        return list(data or [])
    
    # Helper function to convert analytics result to protobuf
    def _convert_analytics_result(self, result):
        """Convert internal analytics result to protobuf format"""
        return pb2.AnalyticsResult(
            data=self._dict_to_map(result.get("data", {})),
            insights=self._list_to_repeated(result.get("insights", [])),
            recommendations=self._list_to_repeated(result.get("recommendations", []))
        )
    
    # ==================== Monitoring Dashboard Methods ====================
    
    def LearningAnalytics(self, request, context):
        """Learning analytics dashboard"""
        logger.info(f"LearningAnalytics called: {request.request_id}")
        
        try:
            internal_request = LearningAnalyticsRequest(
                request_id=request.request_id,
                student_id=request.student_id if request.student_id else None,
                class_id=request.class_id if request.class_id else None,
                subject=request.subject if request.subject else None,
                time_period=request.time_period,
                metrics=list(request.metrics),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.learning_analytics(internal_request)
            
            return pb2.LearningAnalyticsResponse(
                request_id=request.request_id,
                success=True,
                message="Learning analytics completed",
                result=self._convert_analytics_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in LearningAnalytics: {e}")
            return pb2.LearningAnalyticsResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.AnalyticsResult(),
                metadata={}
            )
    
    def CompetencyAnalytics(self, request, context):
        """Competency analytics dashboard"""
        logger.info(f"CompetencyAnalytics called: {request.request_id}")
        
        try:
            internal_request = CompetencyAnalyticsRequest(
                request_id=request.request_id,
                competency_framework=request.competency_framework,
                subject=request.subject if request.subject else None,
                grade=request.grade if request.grade else None,
                time_period=request.time_period,
                analysis_type=request.analysis_type,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.competency_analytics(internal_request)
            
            return pb2.CompetencyAnalyticsResponse(
                request_id=request.request_id,
                success=True,
                message="Competency analytics completed",
                result=self._convert_analytics_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in CompetencyAnalytics: {e}")
            return pb2.CompetencyAnalyticsResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.AnalyticsResult(),
                metadata={}
            )
    
    def AssessmentQualityMonitoring(self, request, context):
        """Assessment quality monitoring dashboard"""
        logger.info(f"AssessmentQualityMonitoring called: {request.request_id}")
        
        try:
            internal_request = AssessmentQualityMonitoringRequest(
                request_id=request.request_id,
                assessment_id=request.assessment_id if request.assessment_id else None,
                subject=request.subject if request.subject else None,
                assessment_type=request.assessment_type if request.assessment_type else None,
                time_period=request.time_period,
                quality_dimensions=list(request.quality_dimensions),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.assessment_quality_monitoring(internal_request)
            
            return pb2.AssessmentQualityMonitoringResponse(
                request_id=request.request_id,
                success=True,
                message="Assessment quality monitoring completed",
                result=self._convert_analytics_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in AssessmentQualityMonitoring: {e}")
            return pb2.AssessmentQualityMonitoringResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.AnalyticsResult(),
                metadata={}
            )
    
    def RetrievalQualityMonitoring(self, request, context):
        """Retrieval quality monitoring dashboard"""
        logger.info(f"RetrievalQualityMonitoring called: {request.request_id}")
        
        try:
            internal_request = RetrievalQualityMonitoringRequest(
                request_id=request.request_id,
                query_type=request.query_type if request.query_type else None,
                subject=request.subject if request.subject else None,
                time_period=request.time_period,
                quality_metrics=list(request.quality_metrics),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.retrieval_quality_monitoring(internal_request)
            
            return pb2.RetrievalQualityMonitoringResponse(
                request_id=request.request_id,
                success=True,
                message="Retrieval quality monitoring completed",
                result=self._convert_analytics_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in RetrievalQualityMonitoring: {e}")
            return pb2.RetrievalQualityMonitoringResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.AnalyticsResult(),
                metadata={}
            )
    
    def PedagogyEffectivenessMonitoring(self, request, context):
        """Pedagogy effectiveness monitoring dashboard"""
        logger.info(f"PedagogyEffectivenessMonitoring called: {request.request_id}")
        
        try:
            internal_request = PedagogyEffectivenessMonitoringRequest(
                request_id=request.request_id,
                pedagogy_type=request.pedagogy_type if request.pedagogy_type else None,
                subject=request.subject if request.subject else None,
                grade=request.grade if request.grade else None,
                time_period=request.time_period,
                effectiveness_metrics=list(request.effectiveness_metrics),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.pedagogy_effectiveness_monitoring(internal_request)
            
            return pb2.PedagogyEffectivenessMonitoringResponse(
                request_id=request.request_id,
                success=True,
                message="Pedagogy effectiveness monitoring completed",
                result=self._convert_analytics_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in PedagogyEffectivenessMonitoring: {e}")
            return pb2.PedagogyEffectivenessMonitoringResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.AnalyticsResult(),
                metadata={}
            )
    
    def HallucinationMonitoring(self, request, context):
        """Hallucination monitoring dashboard"""
        logger.info(f"HallucinationMonitoring called: {request.request_id}")
        
        try:
            internal_request = HallucinationMonitoringRequest(
                request_id=request.request_id,
                content_type=request.content_type if request.content_type else None,
                service=request.service if request.service else None,
                time_period=request.time_period,
                monitoring_dimensions=list(request.monitoring_dimensions),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.hallucination_monitoring(internal_request)
            
            return pb2.HallucinationMonitoringResponse(
                request_id=request.request_id,
                success=True,
                message="Hallucination monitoring completed",
                result=self._convert_analytics_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in HallucinationMonitoring: {e}")
            return pb2.HallucinationMonitoringResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.AnalyticsResult(),
                metadata={}
            )


def serve(port: int = 50074):
    """Start the gRPC server"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Educational Observability gRPC Server on port {port}")
    
    # Create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer
    servicer = EducationalObservabilityServicer()
    pb2_grpc.add_EducationalObservabilityServiceServicer_to_server(servicer, server)
    
    # Start server
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Educational Observability gRPC Server started successfully on port {port}")
    logger.info("Available methods: 6 (Learning, Competency, Assessment Quality, Retrieval Quality, Pedagogy Effectiveness, Hallucination)")
    
    # Keep server running
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


if __name__ == "__main__":
    import os
    port = int(os.getenv("GRPC_PORT", "50074"))
    serve(port)
