"""
RabbitMQ Consumer for Vision Service
Handles async vision processing requests from Backend (Go)
"""
import sys
import os
sys.path.append('/app')

import logging
from typing import Dict, Any
from pathlib import Path
import tempfile
from datetime import datetime
import base64

from shared.messaging.rabbitmq_consumer import BaseRabbitMQConsumer, AsyncRabbitMQConsumer, RabbitMQProducer
from shared.messaging.rabbitmq_messages import (
    ProcessOCRMessage,
    SuccessResponse,
    ErrorResponse
)
from shared.configs.settings import settings

# Import vision components
from app.OCR.ocr_processor import OCRProcessor
from app.VLM.image_classifier import ImageClassifier
from app.captioning.image_captioning import ImageCaptioning
from app.diagram_analysis.diagram_analyzer import DiagramAnalyzer
from app.embeddings.image_embeddings import ImageEmbeddings

logger = logging.getLogger(__name__)

# Temporary storage for processing images
TEMP_DIR = Path(tempfile.gettempdir()) / "vision-service"
TEMP_DIR.mkdir(exist_ok=True)


class VisionServiceConsumer(BaseRabbitMQConsumer):
    """RabbitMQ consumer for Vision Service"""
    
    def __init__(self, rabbitmq_url: str = None):
        """
        Initialize vision consumer
        
        Args:
            rabbitmq_url: RabbitMQ connection URL (default from settings)
        """
        rabbitmq_url = rabbitmq_url or settings.rabbitmq_url
        
        super().__init__(
            rabbitmq_url=rabbitmq_url,
            queue_name="vision.queue",
            exchange_name="ai.platform.exchange",
            routing_key="vision.*",
            prefetch_count=5
        )
        
        # Initialize vision components
        self.ocr_processor = OCRProcessor()
        self.image_classifier = ImageClassifier()
        self.image_captioning = ImageCaptioning()
        self.diagram_analyzer = DiagramAnalyzer()
        self.image_embeddings = ImageEmbeddings()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url)
        
        logger.info("VisionServiceConsumer initialized")
    
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
            if message_type == "process_ocr":
                return self._process_ocr(message)
            elif message_type == "classify_image":
                return self._process_image_classification(message)
            elif message_type == "caption_image":
                return self._process_image_captioning(message)
            elif message_type == "analyze_diagram":
                return self._process_diagram_analysis(message)
            elif message_type == "generate_image_embedding":
                return self._process_image_embedding(message)
            else:
                raise ValueError(f"Unknown message type: {message_type}")
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
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
                    decoded_data = base64.b64decode(image_data)
                    temp_file.write(decoded_data)
                else:
                    temp_file.write(image_data)
            
            # Process OCR
            ocr_result = self.ocr_processor.process(str(temp_file_path), language=language)
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Publish result
            self._publish_result(
                image_id=image_id,
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
    
    def _process_image_classification(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process image classification request
        
        Args:
            message: Image classification message dictionary
            
        Returns:
            Classification result
        """
        try:
            image_id = message.get('image_id')
            image_data = message.get('image_data')
            classes = message.get('classes', [])
            
            logger.info(f"Classifying image: {image_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{image_id}.png"
            
            # Write image data to file
            with open(temp_file_path, "wb") as temp_file:
                if isinstance(image_data, str):
                    decoded_data = base64.b64decode(image_data)
                    temp_file.write(decoded_data)
                else:
                    temp_file.write(image_data)
            
            # Classify image
            classification_result = self.image_classifier.classify(
                str(temp_file_path),
                classes=classes
            )
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Publish result
            self._publish_result(
                image_id=image_id,
                result=classification_result,
                message_type="classify_image"
            )
            
            logger.info(f"Image classification completed for: {image_id}")
            
            return {
                "success": True,
                "image_id": image_id,
                "result": classification_result
            }
            
        except Exception as e:
            logger.error(f"Error classifying image: {str(e)}")
            raise
    
    def _process_image_captioning(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process image captioning request
        
        Args:
            message: Image captioning message dictionary
            
        Returns:
            Captioning result
        """
        try:
            image_id = message.get('image_id')
            image_data = message.get('image_data')
            
            logger.info(f"Generating caption for image: {image_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{image_id}.png"
            
            # Write image data to file
            with open(temp_file_path, "wb") as temp_file:
                if isinstance(image_data, str):
                    decoded_data = base64.b64decode(image_data)
                    temp_file.write(decoded_data)
                else:
                    temp_file.write(image_data)
            
            # Generate caption
            caption_result = self.image_captioning.generate_caption(str(temp_file_path))
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Publish result
            self._publish_result(
                image_id=image_id,
                result=caption_result,
                message_type="caption_image"
            )
            
            logger.info(f"Image captioning completed for: {image_id}")
            
            return {
                "success": True,
                "image_id": image_id,
                "result": caption_result
            }
            
        except Exception as e:
            logger.error(f"Error generating caption: {str(e)}")
            raise
    
    def _process_diagram_analysis(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process diagram analysis request
        
        Args:
            message: Diagram analysis message dictionary
            
        Returns:
            Diagram analysis result
        """
        try:
            image_id = message.get('image_id')
            image_data = message.get('image_data')
            diagram_type = message.get('diagram_type', 'auto')
            
            logger.info(f"Analyzing diagram: {image_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{image_id}.png"
            
            # Write image data to file
            with open(temp_file_path, "wb") as temp_file:
                if isinstance(image_data, str):
                    decoded_data = base64.b64decode(image_data)
                    temp_file.write(decoded_data)
                else:
                    temp_file.write(image_data)
            
            # Analyze diagram
            analysis_result = self.diagram_analyzer.analyze(
                str(temp_file_path),
                diagram_type=diagram_type
            )
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Publish result
            self._publish_result(
                image_id=image_id,
                result=analysis_result,
                message_type="analyze_diagram"
            )
            
            logger.info(f"Diagram analysis completed for: {image_id}")
            
            return {
                "success": True,
                "image_id": image_id,
                "result": analysis_result
            }
            
        except Exception as e:
            logger.error(f"Error analyzing diagram: {str(e)}")
            raise
    
    def _process_image_embedding(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process image embedding generation request
        
        Args:
            message: Image embedding message dictionary
            
        Returns:
            Image embedding result
        """
        try:
            image_id = message.get('image_id')
            image_data = message.get('image_data')
            model = message.get('model', 'openai/clip-vit-base-patch32')
            
            logger.info(f"Generating embedding for image: {image_id}")
            
            # Create temporary image file
            temp_file_path = TEMP_DIR / f"{image_id}.png"
            
            # Write image data to file
            with open(temp_file_path, "wb") as temp_file:
                if isinstance(image_data, str):
                    decoded_data = base64.b64decode(image_data)
                    temp_file.write(decoded_data)
                else:
                    temp_file.write(image_data)
            
            # Generate embedding
            embedding_result = self.image_embeddings.generate_embedding(
                str(temp_file_path),
                model=model
            )
            
            # Clean up temp file
            if temp_file_path.exists():
                temp_file_path.unlink()
            
            # Publish result
            self._publish_result(
                image_id=image_id,
                result=embedding_result,
                message_type="generate_image_embedding"
            )
            
            logger.info(f"Image embedding generated for: {image_id}")
            
            return {
                "success": True,
                "image_id": image_id,
                "result": embedding_result
            }
            
        except Exception as e:
            logger.error(f"Error generating image embedding: {str(e)}")
            raise
    
    def _publish_result(self, image_id: str, result: Dict[str, Any], message_type: str):
        """Publish processing result to result queue"""
        try:
            response_message = SuccessResponse(
                message_id=image_id,
                message_type=f"{message_type}_result",
                timestamp=datetime.utcnow().isoformat(),
                priority="medium",
                success=True,
                result=result
            )
            
            self.result_producer.publish_message(
                exchange_name="ai.platform.exchange",
                routing_key=f"vision.result.{image_id}",
                message=response_message.to_dict()
            )
            
            logger.info(f"Result published for {image_id}")
            
        except Exception as e:
            logger.error(f"Error publishing result: {str(e)}")


class AsyncVisionServiceConsumer(AsyncRabbitMQConsumer):
    """Async version of vision consumer with threading support"""
    
    def __init__(self, rabbitmq_url: str = None):
        super().__init__(rabbitmq_url or settings.rabbitmq_url,
                       queue_name="vision.queue",
                       exchange_name="ai.platform.exchange",
                       routing_key="vision.*",
                       prefetch_count=5)
        
        # Initialize vision components
        self.ocr_processor = OCRProcessor()
        self.image_classifier = ImageClassifier()
        self.image_captioning = ImageCaptioning()
        self.diagram_analyzer = DiagramAnalyzer()
        self.image_embeddings = ImageEmbeddings()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url or settings.rabbitmq_url)
        
        logger.info("AsyncVisionServiceConsumer initialized")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate to sync consumer's process_message"""
        sync_consumer = VisionServiceConsumer(self.rabbitmq_url)
        return sync_consumer.process_message(message)


def start_consumer():
    """Start the vision service consumer"""
    logger.info("Starting Vision Service RabbitMQ Consumer")
    
    try:
        consumer = AsyncVisionServiceConsumer()
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
