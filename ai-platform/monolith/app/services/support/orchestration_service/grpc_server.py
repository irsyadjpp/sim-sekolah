"""
Orchestration Service gRPC Server
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional

import grpc
from grpc.aio import ServicerContext

logger = logging.getLogger(__name__)

GRPC_PORT = int(os.getenv("GRPC_PORT", "50061"))


class OrchestrationServicer:
    """gRPC servicer for Orchestration Service"""
    
    def __init__(self):
        from .main import WorkflowEngine, WorkflowRequest
        self.workflow_engine = WorkflowEngine()
        self.WorkflowRequest = WorkflowRequest
    
    async def ExecuteWorkflow(self, request, context: ServicerContext):
        """Execute workflow orchestration"""
        try:
            workflow_request = self.WorkflowRequest(
                request_id=request.request_id,
                user_id=request.user_id if request.user_id else None,
                session_id=request.session_id if request.session_id else None,
                query=request.query,
                context=dict(request.context) if request.context else None,
                preferences=dict(request.preferences) if request.preferences else None
            )
            
            result = self.workflow_engine.execute_workflow(workflow_request)
            
            # Return protobuf response
            # return orchestration_service_pb2.WorkflowResponse(
            #     request_id=result.request_id,
            #     intent=result.intent,
            #     retrieval_strategy=result.retrieval_strategy,
            #     generation_strategy=result.generation_strategy,
            #     steps=[self._convert_step_to_proto(s) for s in result.steps],
            #     timestamp=int(result.timestamp.timestamp())
            # )
            return result.dict()
            
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error executing workflow: {str(e)}")
            return None
    
    async def DetectIntent(self, request, context: ServicerContext):
        """Detect user intent"""
        try:
            intent_result = self.workflow_engine.detect_intent(request.query, dict(request.context) if request.context else None)
            
            # Return protobuf response
            # return orchestration_service_pb2.IntentDetectionResponse(
            #     intent=intent_result["intent"],
            #     confidence=intent_result["confidence"],
            #     categories=intent_result["categories"]
            # )
            return intent_result
            
        except Exception as e:
            logger.error(f"Error detecting intent: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error detecting intent: {str(e)}")
            return None
    
    async def GetStrategies(self, request, context: ServicerContext):
        """Get available strategies"""
        try:
            strategies = {
                "retrieval_strategies": [
                    "semantic_search",
                    "hybrid_search",
                    "curriculum_aware",
                    "pedagogy_aware",
                    "competency_aware"
                ],
                "generation_strategies": [
                    "standard_generation",
                    "step_by_step",
                    "reasoning_chain",
                    "structured_comparison",
                    "template_based"
                ]
            }
            
            # Return protobuf response
            # return orchestration_service_pb2.StrategiesResponse(**strategies)
            return strategies
            
        except Exception as e:
            logger.error(f"Error getting strategies: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error getting strategies: {str(e)}")
            return None


async def serve(port: int):
    """Start gRPC server"""
    server = grpc.aio.server()
    
    servicer = OrchestrationServicer()
    
    # Add servicer to server
    # orchestration_service_pb2_grpc.add_OrchestrationServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    logger.info(f"Orchestration Service gRPC server started on port {port}")
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)
        logger.info("Orchestration Service gRPC server stopped")


if __name__ == "__main__":
    asyncio.run(serve(GRPC_PORT))
