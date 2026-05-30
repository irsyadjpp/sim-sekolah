"""
Learning Graph Engine gRPC Server
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional

import grpc
from grpc.aio import ServicerContext

logger = logging.getLogger(__name__)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50066"))


class LearningGraphServicer:
    """gRPC servicer for Learning Graph Engine"""
    
    def __init__(self):
        from .main import LearningGraphEngine, GraphConstructionRequest, GraphQueryRequest
        self.graph_engine = LearningGraphEngine()
        self.GraphConstructionRequest = GraphConstructionRequest
        self.GraphQueryRequest = GraphQueryRequest
    
    async def ConstructGraph(self, request, context: ServicerContext):
        """Construct knowledge graph"""
        try:
            graph_request = self.GraphConstructionRequest(
                request_id=request.request_id,
                graph_type=request.graph_type,
                nodes=[dict(node) for node in request.nodes],
                edges=[dict(edge) for edge in request.edges],
                context=dict(request.context) if request.context else None
            )
            
            result = self.graph_engine.construct_graph(graph_request)
            
            # Return protobuf response
            # return graph_service_pb2.GraphConstructionResult(
            #     request_id=graph_request.request_id,
            #     graph_id=result["graph_id"],
            #     graph_type=graph_request.graph_type,
            #     node_count=result["node_count"],
            #     edge_count=result["edge_count"],
            #     metadata=result["metadata"]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error constructing graph: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error constructing graph: {str(e)}")
            return None
    
    async def QueryGraph(self, request, context: ServicerContext):
        """Query knowledge graph"""
        try:
            query_request = self.GraphQueryRequest(
                request_id=request.request_id,
                graph_id=request.graph_id,
                query_type=request.query_type,
                start_node=request.start_node if request.start_node else None,
                end_node=request.end_node if request.end_node else None,
                depth=request.depth
            )
            
            result = self.graph_engine.query_graph(query_request)
            
            # Return protobuf response
            # return graph_service_pb2.GraphQueryResult(
            #     request_id=query_request.request_id,
            #     graph_id=query_request.graph_id,
            #     query_type=query_request.query_type,
            #     results=[self._convert_result_to_proto(r) for r in result["results"]]
            # )
            return result
            
        except Exception as e:
            logger.error(f"Error querying graph: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error querying graph: {str(e)}")
            return None


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    servicer = LearningGraphServicer()
    
    # Add servicer to server
    # graph_service_pb2_grpc.add_LearningGraphServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info(f"Learning Graph Engine gRPC server started on port {port}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        logger.info("Learning Graph Engine gRPC server stopped")


if __name__ == "__main__":
    asyncio.run(serve(GRPC_PORT))
