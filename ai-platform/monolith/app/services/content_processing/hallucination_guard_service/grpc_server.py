"""
gRPC Server Implementation - Hallucination Guard Service
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
    import hallucination_guard_pb2 as pb2
    import hallucination_guard_pb2_grpc as pb2_grpc
except ImportError:
    print("Error: gRPC stub files not found. Please compile proto files first.")
    sys.exit(1)

from main import (
    HallucinationGuardEngine,
    CurriculumValidationRequest,
    PedagogyValidationRequest,
    CompetencyValidationRequest,
    AssessmentValidationRequest,
    PhaseValidationRequest,
    RetrievalGroundingValidationRequest,
    HallucinationDetectionRequest
)

logger = logging.getLogger(__name__)


class HallucinationGuardServicer(pb2_grpc.HallucinationGuardServiceServicer):
    """gRPC Servicer for Hallucination Guard Service - wraps validators and detection system"""
    
    def __init__(self):
        self.engine = HallucinationGuardEngine()
        logger.info("Hallucination Guard Servicer initialized with HallucinationGuardEngine")
    
    # Helper function to convert dict to protobuf map
    def _dict_to_map(self, data):
        """Convert dictionary to protobuf map"""
        return {str(k): str(v) for k, v in (data or {}).items()}
    
    # Helper function to convert list to protobuf repeated field
    def _list_to_repeated(self, data):
        """Convert list to protobuf repeated field"""
        return list(data or [])
    
    # Helper function to convert validation result to protobuf
    def _convert_validation_result(self, result):
        """Convert internal validation result to protobuf format"""
        return pb2.ValidationResult(
            is_valid=result.get("is_valid", False),
            confidence_score=float(result.get("confidence_score", 0.0)),
            issues=self._list_to_repeated(result.get("issues", [])),
            suggestions=self._list_to_repeated(result.get("suggestions", [])),
            validation_details=self._dict_to_map(result.get("validation_details", {}))
        )
    
    # ==================== Validator Methods ====================
    
    def CurriculumValidator(self, request, context):
        """Curriculum content validator"""
        logger.info(f"CurriculumValidator called: {request.request_id}")
        
        try:
            internal_request = CurriculumValidationRequest(
                request_id=request.request_id,
                content=request.content,
                phase=request.phase,
                grade=request.grade,
                subject=request.subject,
                expected_outcomes=list(request.expected_outcomes),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.curriculum_validator(internal_request)
            
            return pb2.CurriculumValidatorResponse(
                request_id=request.request_id,
                success=True,
                message="Curriculum validation completed",
                result=self._convert_validation_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in CurriculumValidator: {e}")
            return pb2.CurriculumValidatorResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.ValidationResult(),
                metadata={}
            )
    
    def PedagogyValidator(self, request, context):
        """Pedagogy validator"""
        logger.info(f"PedagogyValidator called: {request.request_id}")
        
        try:
            internal_request = PedagogyValidationRequest(
                request_id=request.request_id,
                content=request.content,
                pedagogy_type=request.pedagogy_type,
                target_grade=request.target_grade,
                learning_objectives=list(request.learning_objectives),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.pedagogy_validator(internal_request)
            
            return pb2.PedagogyValidatorResponse(
                request_id=request.request_id,
                success=True,
                message="Pedagogy validation completed",
                result=self._convert_validation_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in PedagogyValidator: {e}")
            return pb2.PedagogyValidatorResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.ValidationResult(),
                metadata={}
            )
    
    def CompetencyValidator(self, request, context):
        """Competency validator"""
        logger.info(f"CompetencyValidator called: {request.request_id}")
        
        try:
            internal_request = CompetencyValidationRequest(
                request_id=request.request_id,
                content=request.content,
                competency_framework=request.competency_framework,
                competency_level=request.competency_level,
                subject=request.subject,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.competency_validator(internal_request)
            
            return pb2.CompetencyValidatorResponse(
                request_id=request.request_id,
                success=True,
                message="Competency validation completed",
                result=self._convert_validation_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in CompetencyValidator: {e}")
            return pb2.CompetencyValidatorResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.ValidationResult(),
                metadata={}
            )
    
    def AssessmentValidator(self, request, context):
        """Assessment validator"""
        logger.info(f"AssessmentValidator called: {request.request_id}")
        
        try:
            internal_request = AssessmentValidationRequest(
                request_id=request.request_id,
                assessment_content=request.assessment_content,
                assessment_type=request.assessment_type,
                cognitive_levels=list(request.cognitive_levels),
                subject=request.subject,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.assessment_validator(internal_request)
            
            return pb2.AssessmentValidatorResponse(
                request_id=request.request_id,
                success=True,
                message="Assessment validation completed",
                result=self._convert_validation_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in AssessmentValidator: {e}")
            return pb2.AssessmentValidatorResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.ValidationResult(),
                metadata={}
            )
    
    def PhaseValidator(self, request, context):
        """Phase validator"""
        logger.info(f"PhaseValidator called: {request.request_id}")
        
        try:
            internal_request = PhaseValidationRequest(
                request_id=request.request_id,
                content=request.content,
                target_phase=request.target_phase,
                developmental_stage=request.developmental_stage,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.phase_validator(internal_request)
            
            return pb2.PhaseValidatorResponse(
                request_id=request.request_id,
                success=True,
                message="Phase validation completed",
                result=self._convert_validation_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in PhaseValidator: {e}")
            return pb2.PhaseValidatorResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.ValidationResult(),
                metadata={}
            )
    
    def RetrievalGroundingValidator(self, request, context):
        """Retrieval grounding validator"""
        logger.info(f"RetrievalGroundingValidator called: {request.request_id}")
        
        try:
            internal_request = RetrievalGroundingValidationRequest(
                request_id=request.request_id,
                generated_answer=request.generated_answer,
                retrieved_context=list(request.retrieved_context),
                query=request.query,
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.retrieval_grounding_validator(internal_request)
            
            return pb2.RetrievalGroundingValidatorResponse(
                request_id=request.request_id,
                success=True,
                message="Retrieval grounding validation completed",
                result=self._convert_validation_result(result),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in RetrievalGroundingValidator: {e}")
            return pb2.RetrievalGroundingValidatorResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                result=pb2.ValidationResult(),
                metadata={}
            )
    
    # ==================== Hallucination Detection Methods ====================
    
    def HallucinationDetection(self, request, context):
        """Hallucination detection"""
        logger.info(f"HallucinationDetection called: {request.request_id}")
        
        try:
            internal_request = HallucinationDetectionRequest(
                request_id=request.request_id,
                content=request.content,
                content_type=request.content_type,
                reference_materials=list(request.reference_materials),
                context=self._dict_to_map(request.context) if request.context else None
            )
            
            result = self.engine.hallucination_detection(internal_request)
            
            return pb2.HallucinationDetectionResponse(
                request_id=request.request_id,
                success=True,
                message="Hallucination detection completed",
                is_hallucination=result.get("is_hallucination", False),
                hallucination_probability=float(result.get("hallucination_probability", 0.0)),
                detected_issues=self._list_to_repeated(result.get("detected_issues", [])),
                grounded_facts=self._list_to_repeated(result.get("grounded_facts", [])),
                ungrounded_claims=self._list_to_repeated(result.get("ungrounded_claims", [])),
                confidence_score=float(result.get("confidence_score", 0.0)),
                detection_details=self._dict_to_map(result.get("detection_details", {})),
                metadata=self._dict_to_map(result.get("metadata", {}))
            )
        except Exception as e:
            logger.error(f"Error in HallucinationDetection: {e}")
            return pb2.HallucinationDetectionResponse(
                request_id=request.request_id,
                success=False,
                message=f"Error: {str(e)}",
                is_hallucination=False,
                hallucination_probability=0.0,
                detected_issues=[],
                grounded_facts=[],
                ungrounded_claims=[],
                confidence_score=0.0,
                detection_details={},
                metadata={}
            )


def serve(port: int = 50073):
    """Start the gRPC server"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info(f"Starting Hallucination Guard gRPC Server on port {port}")
    
    # Create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add servicer
    servicer = HallucinationGuardServicer()
    pb2_grpc.add_HallucinationGuardServiceServicer_to_server(servicer, server)
    
    # Start server
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"Hallucination Guard gRPC Server started successfully on port {port}")
    logger.info("Available methods: 7 (6 validators + 1 hallucination detection)")
    
    # Keep server running
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.stop(0)


if __name__ == "__main__":
    import os
    port = int(os.getenv("GRPC_PORT", "50073"))
    serve(port)
