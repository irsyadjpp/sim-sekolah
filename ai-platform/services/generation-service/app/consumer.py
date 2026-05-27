"""
RabbitMQ Consumer for Generation Service
Handles async LLM generation requests from Backend (Go)
"""
import sys
import os
sys.path.append('/app')

import logging
from typing import Dict, Any
from datetime import datetime

from shared.messaging.rabbitmq_consumer import BaseRabbitMQConsumer, AsyncRabbitMQConsumer, RabbitMQProducer
from shared.messaging.rabbitmq_messages import (
    GenerateTextMessage,
    GenerateWithCitationsMessage,
    SuccessResponse,
    ErrorResponse
)
from shared.configs.settings import settings

# Import generation components
from app.providers.openai_provider import OpenAIProvider
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.local_provider import LocalProvider
from app.citations.citation_system import CitationSystem
from app.validators.response_validator import ResponseValidator
from app.prompts.prompt_manager import PromptManager

logger = logging.getLogger(__name__)


class GenerationServiceConsumer(BaseRabbitMQConsumer):
    """RabbitMQ consumer for Generation Service"""
    
    def __init__(self, rabbitmq_url: str = None):
        """
        Initialize generation consumer
        
        Args:
            rabbitmq_url: RabbitMQ connection URL (default from settings)
        """
        rabbitmq_url = rabbitmq_url or settings.rabbitmq_url
        
        super().__init__(
            rabbitmq_url=rabbitmq_url,
            queue_name="generation.queue",
            exchange_name="ai.platform.exchange",
            routing_key="generation.*",
            prefetch_count=5  # Lower prefetch for long-running generation tasks
        )
        
        # Initialize providers
        self.openai_provider = OpenAIProvider()
        self.anthropic_provider = AnthropicProvider()
        self.local_provider = LocalProvider()
        self.citation_system = CitationSystem()
        self.response_validator = ResponseValidator()
        self.prompt_manager = PromptManager()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url)
        
        logger.info("GenerationServiceConsumer initialized")
    
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
            if message_type == "generate_text":
                return self._process_generate_text(message)
            elif message_type == "generate_with_citations":
                return self._process_generate_with_citations(message)
            elif message_type == "validate_response":
                return self._process_validate_response(message)
            elif message_type == "generate_from_template":
                return self._process_generate_from_template(message)
            else:
                raise ValueError(f"Unknown message type: {message_type}")
                
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    def _get_provider(self, provider_name: str):
        """Get provider instance by name"""
        providers = {
            'openai': self.openai_provider,
            'anthropic': self.anthropic_provider,
            'local': self.local_provider
        }
        return providers.get(provider_name.lower(), self.openai_provider)
    
    def _process_generate_text(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process text generation request
        
        Args:
            message: GenerateTextMessage dictionary
            
        Returns:
            Generated text result
        """
        try:
            prompt = message.get('prompt')
            provider = message.get('provider', 'openai')
            model = message.get('model', 'gpt-4')
            temperature = message.get('temperature', 0.7)
            max_tokens = message.get('max_tokens', 1000)
            metadata = message.get('metadata', {})
            
            logger.info(f"Generating text with provider: {provider}, model: {model}")
            
            # Get provider
            provider_instance = self._get_provider(provider)
            
            # Generate text
            result = provider_instance.generate(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            generation_result = {
                "prompt": prompt,
                "generated_text": result,
                "provider": provider,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "tokens_used": len(result.split()),  # Approximate
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                generation_id=f"gen_{len(prompt)}",
                result=generation_result,
                message_type="generate_text"
            )
            
            logger.info(f"Text generation completed: {len(result)} characters")
            
            return {
                "success": True,
                "generated_text": result,
                "tokens_used": len(result.split()),
                "result": generation_result
            }
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise
    
    def _process_generate_with_citations(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process text generation with citations request
        
        Args:
            message: GenerateWithCitationsMessage dictionary
            
        Returns:
            Generated text with citations
        """
        try:
            prompt = message.get('prompt')
            context = message.get('context', '')
            documents = message.get('documents', [])
            provider = message.get('provider', 'openai')
            model = message.get('model', 'gpt-4')
            temperature = message.get('temperature', 0.7)
            max_tokens = message.get('max_tokens', 1000)
            metadata = message.get('metadata', {})
            
            logger.info(f"Generating text with citations: {len(documents)} documents")
            
            # Get provider
            provider_instance = self._get_provider(provider)
            
            # Generate text with context
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nGenerate answer with citations."
            generated_text = provider_instance.generate(
                prompt=full_prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract citations
            citations = self.citation_system.extract_citations(
                generated_text=generated_text,
                documents=documents
            )
            
            # Validate response
            validation_result = self.response_validator.validate(
                response=generated_text,
                context=context,
                documents=documents
            )
            
            generation_result = {
                "prompt": prompt,
                "context": context,
                "generated_text": generated_text,
                "citations": citations,
                "validation": validation_result,
                "provider": provider,
                "model": model,
                "documents_used": len(documents),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                generation_id=f"cit_{len(documents)}",
                result=generation_result,
                message_type="generate_with_citations"
            )
            
            logger.info(f"Generation with citations completed: {len(citations)} citations")
            
            return {
                "success": True,
                "generated_text": generated_text,
                "citations": citations,
                "validation": validation_result,
                "result": generation_result
            }
            
        except Exception as e:
            logger.error(f"Error generating with citations: {str(e)}")
            raise
    
    def _process_validate_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process response validation request
        
        Args:
            message: Validation request dictionary
            
        Returns:
            Validation result
        """
        try:
            response = message.get('response')
            context = message.get('context', '')
            documents = message.get('documents', [])
            metadata = message.get('metadata', {})
            
            logger.info("Validating response")
            
            # Validate response
            validation_result = self.response_validator.validate(
                response=response,
                context=context,
                documents=documents
            )
            
            result = {
                "response": response,
                "validation": validation_result,
                "is_valid": validation_result.get('is_valid', False),
                "confidence": validation_result.get('confidence', 0.0),
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                generation_id=f"val_{len(response)}",
                result=result,
                message_type="validate_response"
            )
            
            logger.info(f"Response validation completed: valid={result['is_valid']}")
            
            return {
                "success": True,
                "is_valid": result['is_valid'],
                "confidence": result['confidence'],
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error validating response: {str(e)}")
            raise
    
    def _process_generate_from_template(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process generation from template request
        
        Args:
            message: Template generation request dictionary
            
        Returns:
            Generated text from template
        """
        try:
            template_name = message.get('template_name')
            template_vars = message.get('template_vars', {})
            provider = message.get('provider', 'openai')
            model = message.get('model', 'gpt-4')
            metadata = message.get('metadata', {})
            
            logger.info(f"Generating from template: {template_name}")
            
            # Get prompt from template
            prompt = self.prompt_manager.render_template(
                template_name=template_name,
                variables=template_vars
            )
            
            # Get provider
            provider_instance = self._get_provider(provider)
            
            # Generate text
            generated_text = provider_instance.generate(
                prompt=prompt,
                model=model
            )
            
            result = {
                "template_name": template_name,
                "template_vars": template_vars,
                "prompt": prompt,
                "generated_text": generated_text,
                "provider": provider,
                "model": model,
                "metadata": metadata
            }
            
            # Publish result
            self._publish_result(
                generation_id=f"tmpl_{template_name}",
                result=result,
                message_type="generate_from_template"
            )
            
            logger.info(f"Template generation completed: {template_name}")
            
            return {
                "success": True,
                "generated_text": generated_text,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error generating from template: {str(e)}")
            raise
    
    def _publish_result(self, generation_id: str, result: Dict[str, Any], message_type: str):
        """Publish generation result to result queue"""
        try:
            response_message = SuccessResponse(
                message_id=generation_id,
                message_type=f"{message_type}_result",
                timestamp=datetime.utcnow().isoformat(),
                priority="medium",
                success=True,
                result=result
            )
            
            self.result_producer.publish_message(
                exchange_name="ai.platform.exchange",
                routing_key=f"generation.result.{generation_id}",
                message=response_message.to_dict()
            )
            
            logger.info(f"Result published for {generation_id}")
            
        except Exception as e:
            logger.error(f"Error publishing result: {str(e)}")


class AsyncGenerationServiceConsumer(AsyncRabbitMQConsumer):
    """Async version of generation consumer with threading support"""
    
    def __init__(self, rabbitmq_url: str = None):
        super().__init__(rabbitmq_url or settings.rabbitmq_url,
                       queue_name="generation.queue",
                       exchange_name="ai.platform.exchange",
                       routing_key="generation.*",
                       prefetch_count=5)
        
        # Initialize providers
        self.openai_provider = OpenAIProvider()
        self.anthropic_provider = AnthropicProvider()
        self.local_provider = LocalProvider()
        self.citation_system = CitationSystem()
        self.response_validator = ResponseValidator()
        self.prompt_manager = PromptManager()
        
        # Result producer
        self.result_producer = RabbitMQProducer(rabbitmq_url or settings.rabbitmq_url)
        
        logger.info("AsyncGenerationServiceConsumer initialized")
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Delegate to sync consumer's process_message"""
        sync_consumer = GenerationServiceConsumer(self.rabbitmq_url)
        return sync_consumer.process_message(message)


def start_consumer():
    """Start the generation service consumer"""
    logger.info("Starting Generation Service RabbitMQ Consumer")
    
    try:
        consumer = AsyncGenerationServiceConsumer()
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