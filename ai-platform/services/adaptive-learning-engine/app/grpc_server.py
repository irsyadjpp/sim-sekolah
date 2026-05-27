"""
Adaptive Learning Engine gRPC Server
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional

import grpc
from grpc.aio import ServicerContext

logger = logging.getLogger(__name__)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50067"))


class AdaptiveLearningServicer:
    """gRPC servicer for Adaptive Learning Engine"""
    
    def __init__(self):
        from .main import AdaptiveLearningEngine, PersonalizedPathRequest, ContentSelectionRequest
        self.adaptive_engine = AdaptiveLearningEngine()
        self.PersonalizedPathRequest = PersonalizedPathRequest
        self.ContentSelectionRequest = ContentSelectionRequest
    
    async def GeneratePersonalizedPath(self, request, context: ServicerContext):
        """Generate personalized learning path"""
        try:
            path_request = self.PersonalizedPathRequest(
                request_id=request.request_id,
                user_id=request.user_id,
                target_competency=request.target_competency,
                current_mastery=dict(request.current_mastery),
                learning_style=request.learning_style if request.learning_style else None,
                preferences=dict(request.preferences) if request.preferences else None,
                context=dict(request.context) if request.context else None
            )
            
            result = self.adaptive_engine.generate_personalized_path(path_request)
            
            # Return protobuf response
            # return adaptive_service_pb2.PersonalizedPathResult(
            #     request_id=path_request.request_id,
            #     user_id=path_request.user_id,
            #     target_competency=path_request.target_competency,
            #     learning_path=[self._convert_step_to_proto(s) for s in result["learning_path"]],
            #     estimated_duration=result["estimated_duration"],
            #     adaptation_notes=result["adaptation_notes"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error generating personalized path: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error generating personalized path: {str(e)}")
            return None
    
    async def SelectAdaptiveContent(self, request, context: ServicerContext):
        """Select adaptive content"""
        try:
            content_request = self.ContentSelectionRequest(
                request_id=request.request_id,
                user_id=request.user_id,
                competency=request.competency,
                current_level=request.current_level,
                learning_style=request.learning_style if request.learning_style else None,
                context=dict(request.context) if request.context else None
            )
            
            result = self.adaptive_engine.select_content(content_request)
            
            # Return protobuf response
            # return adaptive_service_pb2.ContentSelectionResult(
            #     request_id=content_request.request_id,
            #     user_id=content_request.user_id,
            #     competency=content_request.competency,
            #     recommended_content=[self._convert_content_to_proto(c) for c in result["recommended_content"]],
            #     adaptation_reason=result["adaptation_reason"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error selecting adaptive content: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error selecting adaptive content: {str(e)}")
            return None


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    servicer = AdaptiveLearningServicer()
    
    # Add servicer to server
    # adaptive_service_pb2_grpc.add_AdaptiveLearningServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info(f"Adaptive Learning Engine gRPC server started on port {port}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        logger.info("Adaptive Learning Engine gRPC server stopped")


if __name__ == "__main__":
    asyncio.run(serve(GRPC_PORT))
