"""
RabbitMQ Consumer for Metadata Service
Handles async metadata enrichment requests from Backend (Go)
"""
import sys
import os
sys.path.append('/app')

import logging
from typing import Dict, Any
from datetime import datetime

from common.infrastructure.messaging.rabbitmq_consumer import BaseRabbitMQConsumer, AsyncRabbitMQConsumer, RabbitMQProducer
from common.infrastructure.messaging.rabbitmq_messages import (
    SuccessResponse,
    ErrorResponse
)
from common.config.settings import settings

# Import metadata components
from app.enrichers.difficulty_classifier import DifficultyClassifier
from app.enrichers.taxonomy_classifier import TaxonomyClassifier
from app.enrichers.learning_style_detector import LearningStyleDetector
from app.enrichers.competency_tagger import CompetencyTagger
from app.enrichers.pedagogy_tagger import PedagogyTagger
from app.enrichers.assessment_tagger import AssessmentTagger

logger = logging.getLogger(__name__)


class MetadataServiceConsumer(BaseRabbitMQConsumer):
    """RabbitMQ consumer for Metadata Service"""
    
    def __init__(self, rabbitmq_url: str = None):
        """
        Initialize metadata service consumer
        
        Args:
            rabbitmq_url: RabbitMQ connection URL (default from settings)
        """
        rabbitmq_url = rabbitmq_url or settings.rabbitmq_url
        
        super().__init__(
            rabbitmq_url=rabbitmq_url,
            queue_name="metadata.queue",
            exchange_name="ai.platform.exchange",
            routing_key="metadata.*",
            prefetch_count=10
        )
        
        # Initialize metadata components
        self.difficulty_classifier = DifficultyClassifier()
        self.taxonomy_classifier = TaxonomyClassifier()
        self.learning_style_detector = LearningStyleDetector()
        self.competency_tagger = CompetencyTagger()
        self.pedagogy_tagger = PedagogyTagger()
        self.assessment_tagger = AssessmentTagger()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url)
        
        logger.info("MetadataServiceConsumer initialized")
    
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
            if message_type == "enrich_difficulty":
                return self._process_enrich_difficulty(message)
            elif message_type == "enrich_taxonomy":
                return self._process_enrich_taxonomy(message)
            elif message_type == "enrich_competency":
                return self._process_enrich_competency(message)
            elif message_type == "enrich_pedagogy":
                return self._process_enrich_pedagogy(message)
            elif message_type == "detect_learning_style":
                return self._process_detect_learning_style(message)
            elif message_type == "tag_assessment":
                return self._process_tag_assessment(message)
            elif message_type == "batch_enrich":
                return self._process_batch_enrich(message)
            else:
                raise ValueError(f"Unknown message type: {message_type}")
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    def _process_enrich_difficulty(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process difficulty enrichment request
        
        Args:
            message: Difficulty enrichment message dictionary
            
        Returns:
            Enrichment result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            content_type = message.get('content_type', 'text')
            metadata = message.get('metadata', {})
            
            logger.info(f"Enriching difficulty for: {content_id}")
            
            # Classify difficulty
            difficulty_result = self.difficulty_classifier.classify(
                content=content,
                content_type=content_type
            )
            
            result = {
                "content_id": content_id,
                "difficulty": difficulty_result,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="enrich_difficulty"
            )
            
            logger.info(f"Difficulty enrichment completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error enriching difficulty: {str(e)}")
            raise
    
    def _process_enrich_taxonomy(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process taxonomy enrichment request
        
        Args:
            message: Taxonomy enrichment message dictionary
            
        Returns:
            Enrichment result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            taxonomy_type = message.get('taxonomy_type', 'bloom')
            metadata = message.get('metadata', {})
            
            logger.info(f"Enriching taxonomy for: {content_id}")
            
            # Classify taxonomy
            taxonomy_result = self.taxonomy_classifier.classify(
                content=content,
                taxonomy_type=taxonomy_type
            )
            
            result = {
                "content_id": content_id,
                "taxonomy": taxonomy_result,
                "taxonomy_type": taxonomy_type,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="enrich_taxonomy"
            )
            
            logger.info(f"Taxonomy enrichment completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error enriching taxonomy: {str(e)}")
            raise
    
    def _process_enrich_competency(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process competency enrichment request
        
        Args:
            message: Competency enrichment message dictionary
            
        Returns:
            Enrichment result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            competency_framework = message.get('competency_framework', 'kurikulum_merdeka')
            metadata = message.get('metadata', {})
            
            logger.info(f"Enriching competency for: {content_id}")
            
            # Tag competency
            competency_result = self.competency_tagger.tag(
                content=content,
                framework=competency_framework
            )
            
            result = {
                "content_id": content_id,
                "competency": competency_result,
                "competency_framework": competency_framework,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="enrich_competency"
            )
            
            logger.info(f"Competency enrichment completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error enriching competency: {str(e)}")
            raise
    
    def _process_enrich_pedagogy(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process pedagogy enrichment request
        
        Args:
            message: Pedagogy enrichment message dictionary
            
        Returns:
            Enrichment result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            pedagogy_type = message.get('pedagogy_type', 'general')
            metadata = message.get('metadata', {})
            
            logger.info(f"Enriching pedagogy for: {content_id}")
            
            # Tag pedagogy
            pedagogy_result = self.pedagogy_tagger.tag(
                content=content,
                pedagogy_type=pedagogy_type
            )
            
            result = {
                "content_id": content_id,
                "pedagogy": pedagogy_result,
                "pedagogy_type": pedagogy_type,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="enrich_pedagogy"
            )
            
            logger.info(f"Pedagogy enrichment completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error enriching pedagogy: {str(e)}")
            raise
    
    def _process_detect_learning_style(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process learning style detection request
        
        Args:
            message: Learning style detection message dictionary
            
        Returns:
            Detection result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            metadata = message.get('metadata', {})
            
            logger.info(f"Detecting learning style for: {content_id}")
            
            # Detect learning style
            learning_style_result = self.learning_style_detector.detect(content=content)
            
            result = {
                "content_id": content_id,
                "learning_style": learning_style_result,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="detect_learning_style"
            )
            
            logger.info(f"Learning style detection completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error detecting learning style: {str(e)}")
            raise
    
    def _process_tag_assessment(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process assessment tagging request
        
        Args:
            message: Assessment tagging message dictionary
            
        Returns:
            Tagging result
        """
        try:
            content_id = message.get('content_id')
            content = message.get('content')
            assessment_type = message.get('assessment_type', 'general')
            metadata = message.get('metadata', {})
            
            logger.info(f"Tagging assessment for: {content_id}")
            
            # Tag assessment
            assessment_result = self.assessment_tagger.tag(
                content=content,
                assessment_type=assessment_type
            )
            
            result = {
                "content_id": content_id,
                "assessment": assessment_result,
                "assessment_type": assessment_type,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=content_id,
                result=result,
                message_type="tag_assessment"
            )
            
            logger.info(f"Assessment tagging completed for: {content_id}")
            
            return {
                "success": True,
                "content_id": content_id,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error tagging assessment: {str(e)}")
            raise
    
    def _process_batch_enrich(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process batch enrichment request
        
        Args:
            message: Batch enrichment message dictionary
            
        Returns:
            Batch enrichment result
        """
        try:
            content_ids = message.get('content_ids', [])
            contents = message.get('contents', [])
            enrichment_types = message.get('enrichment_types', ['difficulty', 'taxonomy'])
            metadata = message.get('metadata', {})
            
            logger.info(f"Batch enriching {len(contents)} contents")
            
            results = []
            for content_id, content in zip(content_ids, contents):
                content_result = {
                    "content_id": content_id,
                    "enrichments": {}
                }
                
                # Apply each enrichment type
                for enrichment_type in enrichment_types:
                    if enrichment_type == "difficulty":
                        content_result["enrichments"]["difficulty"] = self.difficulty_classifier.classify(content)
                    elif enrichment_type == "taxonomy":
                        content_result["enrichments"]["taxonomy"] = self.taxonomy_classifier.classify(content)
                    elif enrichment_type == "competency":
                        content_result["enrichments"]["competency"] = self.competency_tagger.tag(content)
                    elif enrichment_type == "pedagogy":
                        content_result["enrichments"]["pedagogy"] = self.pedagogy_tagger.tag(content)
                    elif enrichment_type == "learning_style":
                        content_result["enrichments"]["learning_style"] = self.learning_style_detector.detect(content)
                
                results.append(content_result)
            
            result = {
                "content_ids": content_ids,
                "results": results,
                "enrichment_types": enrichment_types,
                "count": len(results),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                content_id=f"batch_{len(contents)}",
                result=result,
                message_type="batch_enrich"
            )
            
            logger.info(f"Batch enrichment completed for {len(contents)} contents")
            
            return {
                "success": True,
                "count": len(results),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error batch enriching: {str(e)}")
            raise
    
    def _publish_result(self, content_id: str, result: Dict[str, Any], message_type: str):
        """Publish enrichment result to result queue"""
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
                routing_key=f"metadata.result.{content_id}",
                message=response_message.to_dict()
            )
            
            logger.info(f"Result published for {content_id}")
            
        except Exception as e:
            logger.error(f"Error publishing result: {str(e)}")


class AsyncMetadataServiceConsumer(AsyncRabbitMQConsumer):
    """Async version of metadata service consumer with threading support"""
    
    def __init__(self, rabbitmq_url: str = None):
        super().__init__(rabbitmq_url or settings.rabbitmq_url,
                       queue_name="metadata.queue",
                       exchange_name="ai.platform.exchange",
                       routing_key="metadata.*",
                       prefetch_count=10)
        
        # Initialize metadata components
        self.difficulty_classifier = DifficultyClassifier()
        self.taxonomy_classifier = TaxonomyClassifier()
        self.learning_style_detector = LearningStyleDetector()
        self.competency_tagger = CompetencyTagger()
        self.pedagogy_tagger = PedagogyTagger()
        self.assessment_tagger = AssessmentTagger()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url or settings.rabbitmq_url)
        
        logger.info("AsyncMetadataServiceConsumer initialized")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate to sync consumer's process_message"""
        sync_consumer = MetadataServiceConsumer(self.rabbitmq_url)
        return sync_consumer.process_message(message)


def start_consumer():
    """Start the metadata service consumer"""
    logger.info("Starting Metadata Service RabbitMQ Consumer")
    
    try:
        consumer = AsyncMetadataServiceConsumer()
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
