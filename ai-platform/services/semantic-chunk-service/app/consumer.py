"""
RabbitMQ Consumer for Semantic Chunk Service
Handles async semantic chunking requests from Backend (Go)
"""
import sys
import os
sys.path.append('/app')

import logging
from typing import Dict, Any
from datetime import datetime

from shared.messaging.rabbitmq_consumer import BaseRabbitMQConsumer, AsyncRabbitMQConsumer, RabbitMQProducer
from shared.messaging.rabbitmq_messages import (
    ChunkCompetencyMessage,
    SuccessResponse,
    ErrorResponse
)
from shared.configs.settings import settings

# Import chunking components
from app.chunkers.competency_chunker import CompetencyChunker
from app.chunkers.activity_chunker import ActivityChunker
from app.chunkers.assessment_chunker import AssessmentChunker
from app.chunkers.inquiry_chunker import InquiryChunker
from app.chunkers.lesson_plan_chunker import LessonPlanChunker
from app.hierarchy.hierarchy_detector import HierarchyDetector
from app.pedagogy.pedagogy_classifier import PedagogyClassifier
from app.taxonomy.taxonomy_tagger import TaxonomyTagger
from app.builders.chunk_builder import ChunkBuilder
from app.enrichers.chunk_enricher import ChunkEnricher

logger = logging.getLogger(__name__)


class ChunkServiceConsumer(BaseRabbitMQConsumer):
    """RabbitMQ consumer for Semantic Chunk Service"""
    
    def __init__(self, rabbitmq_url: str = None):
        """
        Initialize chunk service consumer
        
        Args:
            rabbitmq_url: RabbitMQ connection URL (default from settings)
        """
        rabbitmq_url = rabbitmq_url or settings.rabbitmq_url
        
        super().__init__(
            rabbitmq_url=rabbitmq_url,
            queue_name="chunk.queue",
            exchange_name="ai.platform.exchange",
            routing_key="chunk.*",
            prefetch_count=10
        )
        
        # Initialize chunking components
        self.competency_chunker = CompetencyChunker()
        self.activity_chunker = ActivityChunker()
        self.assessment_chunker = AssessmentChunker()
        self.inquiry_chunker = InquiryChunker()
        self.lesson_plan_chunker = LessonPlanChunker()
        self.hierarchy_detector = HierarchyDetector()
        self.pedagogy_classifier = PedagogyClassifier()
        self.taxonomy_tagger = TaxonomyTagger()
        self.chunk_builder = ChunkBuilder()
        self.chunk_enricher = ChunkEnricher()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url)
        
        logger.info("ChunkServiceConsumer initialized")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming message
        
        Args:
            message: Message dictionary from RabbitMQ
            
        Returns:
            Response dictionary with result
        """
        message_type = message.get('message_type', 'unknown')
        logger.info(f"Processing message type: {message_type}")
        
        try:
            if message_type == "chunk_competency":
                return self._process_chunk_competency(message)
            elif message_type == "chunk_activity":
                return self._process_chunk_activity(message)
            elif message_type == "chunk_assessment":
                return self._process_chunk_assessment(message)
            elif message_type == "chunk_inquiry":
                return self._process_chunk_inquiry(message)
            elif message_type == "chunk_lesson_plan":
                return self._process_chunk_lesson_plan(message)
            elif message_type == "enrich_chunks":
                return self._process_enrich_chunks(message)
            else:
                raise ValueError(f"Unknown message type: {message_type}")
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    def _process_chunk_competency(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process competency-based chunking request
        
        Args:
            message: ChunkCompetencyMessage dictionary
            
        Returns:
            Chunking result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            competency_type = message.get('competency_type', 'KI-3')
            metadata = message.get('metadata', {})
            
            logger.info(f"Chunking competency content: {content_id}, type: {competency_type}")
            
            # Chunk content based on competency
            chunks = self.competency_chunker.chunk(
                content=content,
                competency_type=competency_type,
                metadata=metadata
            )
            
            # Enrich chunks
            enriched_chunks = self.chunk_enricher.enrich(chunks)
            
            result = {
                "content_id": content_id,
                "chunks": enriched_chunks,
                "chunk_count": len(enriched_chunks),
                "competency_type": competency_type,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="chunk_competency"
            )
            
            logger.info(f"Competency chunking completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "chunk_count": len(enriched_chunks),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error chunking competency: {str(e)}")
            raise
    
    def _process_chunk_activity(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process activity chunking request
        
        Args:
            message: Activity chunking message dictionary
            
        Returns:
            Chunking result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            activity_type = message.get('activity_type', 'general')
            metadata = message.get('metadata', {})
            
            logger.info(f"Chunking activity content: {content_id}")
            
            # Chunk activity content
            chunks = self.activity_chunker.chunk(
                content=content,
                activity_type=activity_type,
                metadata=metadata
            )
            
            # Enrich chunks
            enriched_chunks = self.chunk_enricher.enrich(chunks)
            
            result = {
                "content_id": content_id,
                "chunks": enriched_chunks,
                "chunk_count": len(enriched_chunks),
                "activity_type": activity_type,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="chunk_activity"
            )
            
            logger.info(f"Activity chunking completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "chunk_count": len(enriched_chunks),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error chunking activity: {str(e)}")
            raise
    
    def _process_chunk_assessment(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process assessment chunking request
        
        Args:
            message: Assessment chunking message dictionary
            
        Returns:
            Chunking result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            assessment_type = message.get('assessment_type', 'general')
            metadata = message.get('metadata', {})
            
            logger.info(f"Chunking assessment content: {content_id}")
            
            # Chunk assessment content
            chunks = self.assessment_chunker.chunk(
                content=content,
                assessment_type=assessment_type,
                metadata=metadata
            )
            
            # Enrich chunks
            enriched_chunks = self.chunk_enricher.enrich(chunks)
            
            result = {
                "content_id": content_id,
                "chunks": enriched_chunks,
                "chunk_count": len(enriched_chunks),
                "assessment_type": assessment_type,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="chunk_assessment"
            )
            
            logger.info(f"Assessment chunking completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "chunk_count": len(enriched_chunks),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error chunking assessment: {str(e)}")
            raise
    
    def _process_chunk_inquiry(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process inquiry-based chunking request
        
        Args:
            message: Inquiry chunking message dictionary
            
        Returns:
            Chunking result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            inquiry_type = message.get('inquiry_type', 'scientific')
            metadata = message.get('metadata', {})
            
            logger.info(f"Chunking inquiry content: {content_id}")
            
            # Chunk inquiry content
            chunks = self.inquiry_chunker.chunk(
                content=content,
                inquiry_type=inquiry_type,
                metadata=metadata
            )
            
            # Enrich chunks
            enriched_chunks = self.chunk_enricher.enrich(chunks)
            
            result = {
                "content_id": content_id,
                "chunks": enriched_chunks,
                "chunk_count": len(enriched_chunks),
                "inquiry_type": inquiry_type,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="chunk_inquiry"
            )
            
            logger.info(f"Inquiry chunking completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "chunk_count": len(enriched_chunks),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error chunking inquiry: {str(e)}")
            raise
    
    def _process_chunk_lesson_plan(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process lesson plan chunking request
        
        Args:
            message: Lesson plan chunking message dictionary
            
        Returns:
            Chunking result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            grade_level = message.get('grade_level', '10')
            subject = message.get('subject', 'general')
            metadata = message.get('metadata', {})
            
            logger.info(f"Chunking lesson plan: {content_id}")
            
            # Chunk lesson plan
            chunks = self.lesson_plan_chunker.chunk(
                content=content,
                grade_level=grade_level,
                subject=subject,
                metadata=metadata
            )
            
            # Enrich chunks
            enriched_chunks = self.chunk_enricher.enrich(chunks)
            
            result = {
                "content_id": content_id,
                "chunks": enriched_chunks,
                "chunk_count": len(enriched_chunks),
                "grade_level": grade_level,
                "subject": subject,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="chunk_lesson_plan"
            )
            
            logger.info(f"Lesson plan chunking completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "chunk_count": len(enriched_chunks),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error chunking lesson plan: {str(e)}")
            raise
    
    def _process_enrich_chunks(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process chunk enrichment request
        
        Args:
            message: Chunk enrichment message dictionary
            
        Returns:
            Enrichment result
        """
        try:
            content_id = message.get('content_id')
            chunks = message.get('chunks', [])
            enrichment_type = message.get('enrichment_type', 'full')
            metadata = message.get('metadata', {})
            
            logger.info(f"Enriching chunks for: {content_id}")
            
            # Enrich chunks
            enriched_chunks = self.chunk_enricher.enrich(
                chunks=chunks,
                enrichment_type=enrichment_type
            )
            
            result = {
                "content_id": content_id,
                "chunks": enriched_chunks,
                "chunk_count": len(enriched_chunks),
                "enrichment_type": enrichment_type,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="enrich_chunks"
            )
            
            logger.info(f"Chunk enrichment completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "chunk_count": len(enriched_chunks),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error enriching chunks: {str(e)}")
            raise
    
    def _publish_result(self, content_id: str, result: Dict[str, Any], message_type: str):
        """Publish chunking result to result queue"""
        try:
            response_message = SuccessResponse(
                message_id=content_id,
                message_type=f"{message_type}_result",
                timestamp=datetime.utcnow().isoformat(),
                priority="medium",
                success=True,
                result=result
            )
            
            self.result_producer.publish_message(
                exchange_name="ai.platform.exchange",
                routing_key=f"chunk.result.{content_id}",
                message=response_message.to_dict()
            )
            
            logger.info(f"Result published for {content_id}")
            
        except Exception as e:
            logger.error(f"Error publishing result: {str(e)}")


class AsyncChunkServiceConsumer(AsyncRabbitMQConsumer):
    """Async version of chunk service consumer with threading support"""
    
    def __init__(self, rabbitmq_url: str = None):
        super().__init__(rabbitmq_url or settings.rabbitmq_url,
                       queue_name="chunk.queue",
                       exchange_name="ai.platform.exchange",
                       routing_key="chunk.*",
                       prefetch_count=10)
        
        # Initialize chunking components
        self.competency_chunker = CompetencyChunker()
        self.activity_chunker = ActivityChunker()
        self.assessment_chunker = AssessmentChunker()
        self.inquiry_chunker = InquiryChunker()
        self.lesson_plan_chunker = LessonPlanChunker()
        self.hierarchy_detector = HierarchyDetector()
        self.pedagogy_classifier = PedagogyClassifier()
        self.taxonomy_tagger = TaxonomyTagger()
        self.chunk_builder = ChunkBuilder()
        self.chunk_enricher = ChunkEnricher()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url or settings.rabbitmq_url)
        
        logger.info("AsyncChunkServiceConsumer initialized")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate to sync consumer's process_message"""
        sync_consumer = ChunkServiceConsumer(self.rabbitmq_url)
        return sync_consumer.process_message(message)


def start_consumer():
    """Start the chunk service consumer"""
    logger.info("Starting Semantic Chunk Service RabbitMQ Consumer")
    
    try:
        consumer = AsyncChunkServiceConsumer()
        consumer.start_consuming_async()
        
        # Keep main thread alive
        import time
        while consumer.is_alive():
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Stopping consumer")
        consumer.stop_consuming_async()
    except Exception as e:
        logger.error(f"Consumer error: {str(e)}")
        consumer.stop_consuming_async()


if __name__ == "__main__":
    start_consumer()
