"""
Learning Graph Engine RabbitMQ Consumer
Consumes graph construction requests from RabbitMQ
"""
import os
import logging
from typing import Optional

from common.infrastructure.messaging.rabbitmq_consumer import AsyncRabbitMQConsumer
from common.infrastructure.messaging.rabbitmq_messages import BaseMessage

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


class LearningGraphEngineConsumer(AsyncRabbitMQConsumer):
    """Consumer for learning graph engine events"""
    
    def __init__(self):
        super().__init__(
            rabbitmq_url=RABBITMQ_URL,
            queue_name="graph.queue",
            exchange_name="graph.exchange",
            routing_key="graph.construct"
        )
        from .main import GraphConstructionRequest, GraphQueryRequest, graph_engine
        self.GraphConstructionRequest = GraphConstructionRequest
        self.GraphQueryRequest = GraphQueryRequest
        self.graph_engine = graph_engine
    
    async def process_message(self, message: BaseMessage) -> Optional[dict]:
        """Process graph message"""
        try:
            message_data = message.data
            request_type = message_data.get("request_type", "construct")
            
            if request_type == "construct":
                # Create graph construction request
                graph_request = self.GraphConstructionRequest(
                    request_id=message_data.get("request_id"),
                    graph_type=message_data.get("graph_type", "competency"),
                    nodes=message_data.get("nodes", []),
                    edges=message_data.get("edges", []),
                    context=message_data.get("context")
                )
                
                # Construct graph
                result = self.graph_engine.construct_graph(graph_request)
                
                logger.info(f"Processed graph construction request: {graph_request.request_id} - graph_id: {result['graph_id']}")
                
                return {
                    "request_id": graph_request.request_id,
                    "graph_id": result["graph_id"],
                    "graph_type": graph_request.graph_type,
                    "node_count": result["node_count"],
                    "edge_count": result["edge_count"],
                    "metadata": result["metadata"]
                }
            
            elif request_type == "query":
                # Create graph query request
                query_request = self.GraphQueryRequest(
                    request_id=message_data.get("request_id"),
                    graph_id=message_data.get("graph_id"),
                    query_type=message_data.get("query_type", "neighbors"),
                    start_node=message_data.get("start_node"),
                    end_node=message_data.get("end_node"),
                    depth=message_data.get("depth", 1)
                )
                
                # Query graph
                result = self.graph_engine.query_graph(query_request)
                
                logger.info(f"Processed graph query request: {query_request.request_id}")
                
                return {
                    "request_id": query_request.request_id,
                    "graph_id": query_request.graph_id,
                    "query_type": query_request.query_type,
                    "results": result["results"]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing graph message: {e}")
            raise


class AsyncLearningGraphEngineConsumer(LearningGraphEngineConsumer):
    """Async wrapper for learning graph engine consumer"""
    pass
