"""
Assessment Engine gRPC Server
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional

import grpc
from grpc.aio import ServicerContext

logger = logging.getLogger(__name__)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50064"))


class AssessmentServicer:
    """gRPC servicer for Assessment Engine"""
    
    def __init__(self):
        from .main import AssessmentEngine, AssessmentGenerationRequest, HOTSQuestionRequest, RubricGenerationRequest
        self.assessment_engine = AssessmentEngine()
        self.AssessmentGenerationRequest = AssessmentGenerationRequest
        self.HOTSQuestionRequest = HOTSQuestionRequest
        self.RubricGenerationRequest = RubricGenerationRequest
    
    async def GenerateAssessment(self, request, context: ServicerContext):
        """Generate assessment questions"""
        try:
            assessment_request = self.AssessmentGenerationRequest(
                request_id=request.request_id,
                topic=request.topic,
                competency=request.competency,
                grade=request.grade,
                assessment_type=request.assessment_type,
                question_count=request.question_count,
                difficulty=request.difficulty,
                context=dict(request.context) if request.context else None
            )
            
            result = self.assessment_engine.generate_assessment(assessment_request)
            
            # Return protobuf response
            # return assessment_service_pb2.AssessmentGenerationResult(
            #     request_id=assessment_request.request_id,
            #     questions=[self._convert_question_to_proto(q) for q in result["questions"]],
            #     rubric=self._convert_rubric_to_proto(result["rubric"]) if result["rubric"] else None,
            #     metadata=result["metadata"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error generating assessment: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error generating assessment: {str(e)}")
            return None
    
    async def GenerateHOTSQuestions(self, request, context: ServicerContext):
        """Generate HOTS questions"""
        try:
            hots_request = self.HOTSQuestionRequest(
                request_id=request.request_id,
                topic=request.topic,
                competency=request.competency,
                cognitive_level=request.cognitive_level,
                question_count=request.question_count,
                context=dict(request.context) if request.context else None
            )
            
            result = self.assessment_engine.generate_hots_questions(hots_request)
            
            # Return protobuf response
            # return assessment_service_pb2.HOTSQuestionResult(
            #     questions=[self._convert_question_to_proto(q) for q in result["questions"]],
            #     metadata=result["metadata"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error generating HOTS questions: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error generating HOTS questions: {str(e)}")
            return None
    
    async def GenerateRubric(self, request, context: ServicerContext):
        """Generate assessment rubric"""
        try:
            rubric_request = self.RubricGenerationRequest(
                request_id=request.request_id,
                assessment_type=request.assessment_type,
                criteria=list(request.criteria),
                performance_levels=request.performance_levels,
                context=dict(request.context) if request.context else None
            )
            
            result = self.assessment_engine.generate_rubric(rubric_request)
            
            # Return protobuf response
            # return assessment_service_pb2.RubricGenerationResult(
            #     rubric=self._convert_rubric_to_proto(result["rubric"]),
            #     metadata=result["metadata"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error generating rubric: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error generating rubric: {str(e)}")
            return None


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    servicer = AssessmentServicer()
    
    # Add servicer to server
    # assessment_service_pb2_grpc.add_AssessmentServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info(f"Assessment Engine gRPC server started on port {port}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        logger.info("Assessment Engine gRPC server stopped")


if __name__ == "__main__":
    asyncio.run(serve(GRPC_PORT))
