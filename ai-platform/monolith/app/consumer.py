"""
RabbitMQ Consumer for Parser Service
Handles async document parsing requests from Backend (Go)
"""
import sys
import os
sys.path.append('/app')
sys.path.append('/shared')

import logging
from typing import Dict, Any
from pathlib import Path
import tempfile
from datetime import datetime

from common.infrastructure.messaging.rabbitmq_consumer import BaseRabbitMQConsumer, AsyncRabbitMQConsumer, RabbitMQProducer
from common.infrastructure.messaging.rabbitmq_messages import (
    ParseDocumentMessage, 
    ProcessOCRMessage,
    SuccessResponse, 
    ErrorResponse
)
from common.config.settings import settings
from common.infrastructure.messaging.dlq_config import DLQConfiguration

# Import parser components
from app.extractors.text_extractor import TextExtractor
from app.extractors.table_extractor import TableExtractor
from app.extractors.image_extractor import ImageExtractor
from app.extractors.ocr_extractor import OCRExtractor
from app.extractors.layout_detector import LayoutDetector
from app.extractors.enhanced_layout_detector import EnhancedLayoutDetector
from app.extractors.formula_extractor import FormulaExtractor
from app.extractors.figure_extractor import FigureExtractor
from app.pipelines.modern_document_pipeline import ModernDocumentPipeline
from app.pipelines.reading_order_resolver import ReadingOrderResolver
from app.pipelines.semantic_chunker import SemanticChunker
from app.pipelines.region_classifier import RegionClassifier
from app.pipelines.semantic_services_integration import SemanticServicesIntegration
from app.normalizers.content_normalizer import ContentNormalizer

logger = logging.getLogger(__name__)

# Temporary storage for processing documents
TEMP_DIR = Path(tempfile.gettempdir()) / "parser-service"
TEMP_DIR.mkdir(exist_ok=True)


class ParserServiceConsumer(BaseRabbitMQConsumer):
    """RabbitMQ consumer for Parser Service"""
    
    def __init__(self, rabbitmq_url: str = None):
        """
        Initialize parser consumer
        
        Args:
            rabbitmq_url: RabbitMQ connection URL (default from settings)
        """
        rabbitmq_url = rabbitmq_url or settings.rabbitmq_url
        
        super().__init__(
            rabbitmq_url=rabbitmq_url,
            queue_name="parser.queue",
            exchange_name="ai.platform.exchange",
            routing_key="parser.*",
            prefetch_count=5
        )
        
        # Initialize parser components
        self.text_extractor = TextExtractor()
        self.table_extractor = TableExtractor()
        self.image_extractor = ImageExtractor()
        self.ocr_extractor = OCRExtractor()
        self.layout_detector = LayoutDetector()
        self.content_normalizer = ContentNormalizer()
        self.document_pipeline = DocumentPipeline(
            text_extractor=self.text_extractor,
            table_extractor=self.table_extractor,
            image_extractor=self.image_extractor,
            ocr_extractor=self.ocr_extractor,
            layout_detector=self.layout_detector,
            content_normalizer=self.content_normalizer
        )
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url)
        
        # DLQ configuration
        self.service_name = "parser_service"
        self.dlq_config = DLQConfiguration.get_config(self.service_name)
        self.max_retries = self.dlq_config.get("retry_policy", {}).get("max_retries", 3)
        
        logger.info("ParserServiceConsumer initialized with DLQ support")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming message with DLQ support
        
        Args:
            message: Message dictionary from RabbitMQ
            
        Returns:
            Response dictionary with result
        """
        message_type = message.get('message_type', 'unknown')
        logger.info(f"Processing message type: {message_type}")
        
        retry_count = message.get('x-retry-count', 0)
        
        try:
            if message_type == "parse_document":
                result = self._process_parse_document(message)
                return result
            elif message_type == "process_ocr":
                result = self._process_ocr(message)
                return result
            else:
                raise ValueError(f"Unknown message type: {message_type}")
                
        except ValueError as e:
            # Validation error - fatal, send to DLQ immediately
            error_info = {
                "error_type": "schema_validation_error",
                "error_message": str(e),
                "exception": e,
                "retry_count": retry_count,
                "service_name": self.service_name,
                "failed_at": datetime.utcnow().isoformat(),
                "original_queue": "parser.queue",
                "max_retries_exceeded": True
            }
            self._send_to_dlq(message, error_info)
            raise
            
        except Exception as e:
            # Other errors - check if should send to DLQ or retry
            error_type = self._classify_error(e)
            
            if DLQConfiguration.should_send_to_dlq(error_type, retry_count, self.max_retries):
                error_info = {
                    "error_type": error_type,
                    "error_message": str(e),
                    "exception": e,
                    "retry_count": retry_count,
                    "service_name": self.service_name,
                    "failed_at": datetime.utcnow().isoformat(),
                    "original_queue": "parser.queue",
                    "max_retries_exceeded": retry_count >= self.max_retries
                }
                self._send_to_dlq(message, error_info)
                raise
            else:
                # Should retry - increment retry count and re-raise
                logger.warning(f"Retryable error {error_type}, will retry (attempt {retry_count + 1}/{self.max_retries})")
                raise
    
    def _classify_error(self, exception: Exception) -> str:
        """Classify error type for DLQ decision"""
        error_message = str(exception).lower()
        
        if "timeout" in error_message or "timed out" in error_message:
            return "timeout_error"
        elif "database" in error_message or "connection" in error_message:
            return "database_connection_error"
        elif "rate limit" in error_message or "too many requests" in error_message:
            return "rate_limit_exceeded"
        elif "validation" in error_message or "invalid" in error_message:
            return "schema_validation_error"
        elif "authentication" in error_message or "unauthorized" in error_message:
            return "authentication_error"
        else:
            return "unknown_error"
    
    def _send_to_dlq(self, message: Dict[str, Any], error_info: Dict[str, Any]):
        """Send failed message to DLQ"""
        try:
            dlq_exchange = f"{self.dlq_config.get('exchange')}.dlq"
            dlq_routing_key = f"{self.service_name}.dlq"
            
            # Format DLQ message
            dlq_message = DLQConfiguration.format_dlq_message(message, error_info)
            
            # Send to DLQ via result producer
            self.result_producer.exchange_name = dlq_exchange
            self.result_producer.routing_key = dlq_routing_key
            self.result_producer.publish(dlq_message)
            
            logger.warning(f"Sent message to DLQ {dlq_routing_key} due to: {error_info['error_type']}")
            
        except Exception as e:
            logger.error(f"Failed to send message to DLQ: {str(e)}")
    
    def _process_parse_document(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process document parsing request
        
        Args:
            message: ParseDocumentMessage dictionary
            
        Returns:
            Parsing result
        """
        try:
            document_id = message.get('document_id')
            document_data = message.get('document_data')
            document_type = message.get('document_type')
            metadata = message.get('metadata', {})
            
            logger.info(f"Parsing document: {document_id}, type: {document_type}")
            
            # Create temporary file from document data
            # Assuming document_data is base64 encoded content
            file_extension = self._get_file_extension(document_type)
            temp_file_path = TEMP_DIR / f"{document_id}{file_extension}"
            
            # Write document data to file
            # In production, handle base64 decoding if needed
            with open(temp_file_path, "wb") as temp_file:
                if isinstance(document_data, str):
                    # Assume base64 encoded
                    import base64
                    decoded_data = base64.b64decode(document_data)
                    temp_file.write(decoded_data)
                else:
                    temp_file.write(document_data)
            
            # Process document
            result = self.document_pipeline.process(
                file_path=str(temp_file_path),
                options=metadata
            )
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Publish result to result queue
            self._publish_result(
                document_id=document_id,
                result=result,
                message_type="parse_document"
            )
            
            logger.info(f"Document {document_id} parsed successfully")
            
            return {
                "success": True,
                "document_id": document_id,
                "processing_time_ms": result.get("processing_time_ms", 0),
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error parsing document: {str(e)}")
            raise
    
    def _process_ocr(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process OCR request
        
        Args:
            message: ProcessOCRMessage dictionary
            
        Returns:
            OCR result
        """
        try:
            image_id = message.get('image_id')
            image_data = message.get('image_data')
            language = message.get('language', 'ind')
            
            logger.info(f"Processing OCR for image: {image_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{image_id}.png"
            
            # Write image data to file
            with open(temp_file_path, "wb") as temp_file:
                if isinstance(image_data, str):
                    import base64
                    decoded_data = base64.b64decode(image_data)
                    temp_file.write(decoded_data)
                else:
                    temp_file.write(image_data)
            
            # Process OCR
            ocr_result = self.ocr_extractor.extract(str(temp_file_path), language=language)
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Publish result
            self._publish_result(
                document_id=image_id,
                result=ocr_result,
                message_type="process_ocr"
            )
            
            logger.info(f"OCR processing completed for image: {image_id}")
            
            return {
                "success": True,
                "image_id": image_id,
                "result": ocr_result
            }
            
        except Exception as e:
            logger.error(f"Error processing OCR: {str(e)}")
            raise
    
    def _publish_result(self, document_id: str, result: Dict[str, Any], message_type: str):
        """Publish processing result to result queue"""
        try:
            response_message = SuccessResponse(
                message_id=document_id,
                message_type=f"{message_type}_result",
                timestamp=datetime.utcnow().isoformat(),
                priority="medium",
                success=True,
                result=result
            )
            
            self.result_producer.publish_message(
                exchange_name="ai.platform.exchange",
                routing_key=f"parser.result.{document_id}",
                message=response_message.to_dict()
            )
            
            logger.info(f"Result published for {document_id}")
            
        except Exception as e:
            logger.error(f"Error publishing result: {str(e)}")
    
    def _get_file_extension(self, document_type: str) -> str:
        """Get file extension from document type"""
        extension_map = {
            'pdf': '.pdf',
            'doc': '.doc',
            'docx': '.docx',
            'txt': '.txt',
            'png': '.png',
            'jpg': '.jpg',
            'jpeg': '.jpeg'
        }
        return extension_map.get(document_type.lower(), '.txt')


class AsyncParserServiceConsumer(AsyncRabbitMQConsumer):
    """Async version of parser consumer with threading support"""
    
    def __init__(self, rabbitmq_url: str = None):
        super().__init__(rabbitmq_url or settings.rabbitmq_url, 
                       queue_name="parser.queue",
                       exchange_name="ai.platform.exchange",
                       routing_key="parser.*",
                       prefetch_count=5)
        
        # Initialize parser components
        self.text_extractor = TextExtractor()
        self.table_extractor = TableExtractor()
        self.image_extractor = ImageExtractor()
        self.ocr_extractor = OCRExtractor()
        self.layout_detector = LayoutDetector()
        self.content_normalizer = ContentNormalizer()
        self.document_pipeline = DocumentPipeline(
            text_extractor=self.text_extractor,
            table_extractor=self.table_extractor,
            image_extractor=self.image_extractor,
            ocr_extractor=self.ocr_extractor,
            layout_detector=self.layout_detector,
            content_normalizer=self.content_normalizer
        )
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url or settings.rabbitmq_url)
        
        logger.info("AsyncParserServiceConsumer initialized")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate to sync consumer's process_message"""
        # Create temporary sync consumer for processing
        sync_consumer = ParserServiceConsumer(self.rabbitmq_url)
        return sync_consumer.process_message(message)


def start_consumer():
    """Start the parser service consumer"""
    logger.info("Starting Parser Service RabbitMQ Consumer")
    
    try:
        consumer = AsyncParserServiceConsumer()
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