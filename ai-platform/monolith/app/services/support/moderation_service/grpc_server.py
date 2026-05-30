"""
Moderation Service gRPC Server
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional

import grpc
from grpc.aio import ServicerContext

logger = logging.getLogger(__name__)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50060"))


class ModerationServicer:
    """gRPC servicer for Moderation Service"""
    
    def __init__(self):
        from .main import ModerationEngine, ModerationRequest
        self.moderation_engine = ModerationEngine()
        self.ModerationRequest = ModerationRequest
    
    async def ModerateContent(self, request, context: ServicerContext):
        """Moderate content"""
        try:
            moderation_request = self.ModerationRequest(
                request_id=request.request_id,
                content=request.content,
                content_type=request.content_type,
                user_id=request.user_id if request.user_id else None,
                context=dict(request.context) if request.context else None
            )
            
            result = self.moderation_engine.moderate(moderation_request)
            
            # Return protobuf response
            # return moderation_service_pb2.ModerationResult(
            #     request_id=result.request_id,
            #     is_safe=result.is_safe,
            #     toxicity_score=result.toxicity_score,
            #     bias_score=result.bias_score,
            #     categories=result.categories,
            #     flags=result.flags,
            #     confidence=result.confidence,
            #     timestamp=int(result.timestamp.timestamp())
            # )
            return result.dict()
            
        except Exception as e:
            logger.error(f"Error moderating content: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error moderating content: {str(e)}")
            return None
    
    async def ModerateBatch(self, request, context: ServicerContext):
        """Moderate multiple contents"""
        try:
            results = []
            for req in request.requests:
                moderation_request = self.ModerationRequest(
                    request_id=req.request_id,
                    content=req.content,
                    content_type=req.content_type,
                    user_id=req.user_id if req.user_id else None,
                    context=dict(req.context) if req.context else None
                )
                result = self.moderation_engine.moderate(moderation_request)
                results.append(result)
            
            # Return protobuf response
            # return moderation_service_pb2.ModerationBatchResponse(
            #     results=[self._convert_to_proto(r) for r in results]
            # )
            return {"results": [r.dict() for r in results]}
            
        except Exception as e:
            logger.error(f"Error moderating batch: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error moderating batch: {str(e)}")
            return None


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    servicer = ModerationServicer()
    
    # Add servicer to server
    # moderation_service_pb2_grpc.add_ModerationServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info(f"Moderation Service gRPC server started on port {port}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        logger.info("Moderation Service gRPC server stopped")


if __name__ == "__main__":
    asyncio.run(serve(GRPC_PORT))
