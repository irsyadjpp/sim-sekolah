"""
Learning Progression Engine gRPC Server
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional

import grpc
from grpc.aio import ServicerContext

logger = logging.getLogger(__name__)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50065"))


class LearningProgressionServicer:
    """gRPC servicer for Learning Progression Engine"""
    
    def __init__(self):
        from .main import LearningProgressionEngine, MasteryTrackingRequest, GapDetectionRequest
        self.progression_engine = LearningProgressionEngine()
        self.MasteryTrackingRequest = MasteryTrackingRequest
        self.GapDetectionRequest = GapDetectionRequest
    
    async def TrackMastery(self, request, context: ServicerContext):
        """Track mastery progression"""
        try:
            mastery_request = self.MasteryTrackingRequest(
                request_id=request.request_id,
                user_id=request.user_id,
                competency=request.competency,
                performance_data=[dict(perf) for perf in request.performance_data],
                context=dict(request.context) if request.context else None
            )
            
            result = self.progression_engine.track_mastery(mastery_request)
            
            # Return protobuf response
            # return progression_service_pb2.MasteryTrackingResult(
            #     request_id=mastery_request.request_id,
            #     user_id=mastery_request.user_id,
            #     competency=mastery_request.competency,
            #     mastery_level=result["mastery_level"],
            #     mastery_score=result["mastery_score"],
            #     progression_trend=result["progression_trend"],
            #     recommendations=result["recommendations"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error tracking mastery: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error tracking mastery: {str(e)}")
            return None
    
    async def DetectGaps(self, request, context: ServicerContext):
        """Detect prerequisite gaps"""
        try:
            gap_request = self.GapDetectionRequest(
                request_id=request.request_id,
                user_id=request.user_id,
                target_competency=request.target_competency,
                current_mastery=dict(request.current_mastery),
                prerequisite_map={k: list(v) for k, v in request.prerequisite_map.items()},
                context=dict(request.context) if request.context else None
            )
            
            result = self.progression_engine.detect_gaps(gap_request)
            
            # Return protobuf response
            # return progression_service_pb2.GapDetectionResult(
            #     request_id=gap_request.request_id,
            #     user_id=gap_request.user_id,
            #     target_competency=gap_request.target_competency,
            #     has_gaps=result["has_gaps"],
            #     missing_prerequisites=result["missing_prerequisites"],
            #     weak_prerequisites=result["weak_prerequisites"],
            #     recommended_path=result["recommended_path"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error detecting gaps: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error detecting gaps: {str(e)}")
            return None


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    servicer = LearningProgressionServicer()
    
    # Add servicer to server
    # progression_service_pb2_grpc.add_LearningProgressionServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info(f"Learning Progression Engine gRPC server started on port {port}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        logger.info("Learning Progression Engine gRPC server stopped")


if __name__ == "__main__":
    asyncio.run(serve(GRPC_PORT))
