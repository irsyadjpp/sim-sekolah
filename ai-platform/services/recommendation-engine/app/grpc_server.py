"""
Recommendation Engine gRPC Server
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional

import grpc
from grpc.aio import ServicerContext

logger = logging.getLogger(__name__)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50068"))


class RecommendationServicer:
    """gRPC servicer for Recommendation Engine"""
    
    def __init__(self):
        from .main import RecommendationEngine, RecommendationRequest
        self.recommendation_engine = RecommendationEngine()
        self.RecommendationRequest = RecommendationRequest
    
    async def GenerateRecommendations(self, request, context: ServicerContext):
        """Generate content recommendations"""
        try:
            recommendation_request = self.RecommendationRequest(
                request_id=request.request_id,
                user_id=request.user_id,
                context=dict(request.context) if request.context else None,
                preferences=dict(request.preferences) if request.preferences else None,
                strategy=request.strategy
            )
            
            result = self.recommendation_engine.generate_recommendations(recommendation_request)
            
            # Return protobuf response
            # return recommendation_service_pb2.RecommendationResult(
            #     request_id=recommendation_request.request_id,
            #     user_id=recommendation_request.user_id,
            #     recommendations=[self._convert_recommendation_to_proto(r) for r in result["recommendations"]],
            #     strategy_used=result["strategy_used"],
            #     confidence_scores=result["confidence_scores"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error generating recommendations: {str(e)}")
            return None


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    servicer = RecommendationServicer()
    
    # Add servicer to server
    # recommendation_service_pb2_grpc.add_RecommendationServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info(f"Recommendation Engine gRPC server started on port {port}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        logger.info("Recommendation Engine gRPC server stopped")


if __name__ == "__main__":
    asyncio.run(serve(GRPC_PORT))
