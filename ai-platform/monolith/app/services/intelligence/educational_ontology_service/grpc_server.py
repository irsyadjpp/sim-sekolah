"""
gRPC Server for Educational Ontology Service
"""
import os
import logging
import grpc
from concurrent import futures
import asyncio

logger = logging.getLogger(__name__)

class EducationalOntologyService:
    """gRPC service for educational ontology"""
    
    def __init__(self):
        self.port = int(os.getenv("GRPC_PORT", "50071"))
    
    async def QueryOntology(self, request, context):
        """Handle ontology query via gRPC"""
        logger.info(f"gRPC: QueryOntology request: {request.request_id}")
        return request
    
    async def AddOntologyNode(self, request, context):
        """Handle adding ontology node via gRPC"""
        logger.info(f"gRPC: AddOntologyNode request: {request.request_id}")
        return request
    
    async def UpdateOntologyNode(self, request, context):
        """Handle updating ontology node via gRPC"""
        logger.info(f"gRPC: UpdateOntologyNode request: {request.request_id}")
        return request
    
    async def DeleteOntologyNode(self, request, context):
        """Handle deleting ontology node via gRPC"""
        logger.info(f"gRPC: DeleteOntologyNode request: {request.request_id}")
        return request


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    server.add_insecure_port(f'[::]:{port}')
    logger.info(f"Educational Ontology gRPC server started on port {port}")
    
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    port = int(os.getenv("GRPC_PORT", "50071"))
    asyncio.run(serve(port))