"""
Pedagogy Engine gRPC Server
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional

import grpc
from grpc.aio import ServicerContext

logger = logging.getLogger(__name__)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50063"))


class PedagogyServicer:
    """gRPC servicer for Pedagogy Engine"""
    
    def __init__(self):
        from .main import PedagogyEngine
        self.pedagogy_engine = PedagogyEngine()
    
    async def AnalyzePedagogy(self, request, context: ServicerContext):
        """Analyze pedagogy from content"""
        try:
            result = self.pedagogy_engine.detect_pedagogy(
                request.content,
                dict(request.context) if request.context else None
            )
            
            # Return protobuf response
            # return pedagogy_service_pb2.PedagogyAnalysisResult(
            #     pedagogy_type=result["pedagogy_type"],
            #     confidence=result["confidence"],
            #     characteristics=result["characteristics"],
            #     teaching_methods=result["teaching_methods"],
            #     recommendations=result["recommendations"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing pedagogy: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error analyzing pedagogy: {str(e)}")
            return None
    
    async def DetectPedagogyType(self, request, context: ServicerContext):
        """Detect pedagogy type"""
        try:
            result = self.pedagogy_engine.detect_pedagogy(
                request.content,
                dict(request.context) if request.context else None
            )
            
            # Return protobuf response
            # return pedagogy_service_pb2.PedagogyDetectionResult(
            #     pedagogy_type=result["pedagogy_type"],
            #     confidence=result["confidence"],
            #     scores=result["scores"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error detecting pedagogy type: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error detecting pedagogy type: {str(e)}")
            return None


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    servicer = PedagogyServicer()
    
    # Add servicer to server
    # pedagogy_service_pb2_grpc.add_PedagogyServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info(f"Pedagogy Engine gRPC server started on port {port}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        logger.info("Pedagogy Engine gRPC server stopped")


if __name__ == "__main__":
    asyncio.run(serve(GRPC_PORT))
