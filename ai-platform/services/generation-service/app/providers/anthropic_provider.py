"""
Anthropic provider for text generation
Supports Claude 3 Opus, Claude 3 Sonnet, and Claude 3 Haiku
"""
import os
import time
from typing import Dict, Any, Optional
import logging

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logging.warning("Anthropic library not available")

logger = logging.getLogger(__name__)


class AnthropicProvider:
    """Anthropic provider for text generation"""
    
    def __init__(self, api_key: str):
        """
        Initialize Anthropic provider
        
        Args:
            api_key: Anthropic API key
        """
        self.api_key = api_key
        self.client = None
        
        logger.info("Initializing Anthropic provider")
        
        if not ANTHROPIC_AVAILABLE:
            logger.error("Anthropic library not available")
            raise ImportError("Anthropic library is required but not installed")
        
        try:
            self.client = anthropic.Anthropic(api_key=api_key)
            logger.info("Anthropic provider initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic provider: {str(e)}")
            raise
    
    async def generate(
        self,
        prompt: str,
        model: str = "claude-3-opus-20240229",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Generate text using Anthropic Claude
        
        Args:
            prompt: Input prompt
            model: Model name (claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        
        Returns:
            Dictionary with generated text and metadata
        """
        try:
            start_time = time.time()
            
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            result = {
                "text": response.content[0].text,
                "model": model,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "latency_ms": latency_ms,
                "stop_reason": response.stop_reason
            }
            
            logger.info(f"Anthropic generation completed. Model: {model}, Tokens: {result['tokens_used']}, Latency: {latency_ms}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in Anthropic generation: {str(e)}")
            raise
    
    async def generate_with_system_prompt(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "claude-3-opus-20240229",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Generate text with system prompt
        
        Args:
            system_prompt: System prompt for context
            user_prompt: User prompt
            model: Model name
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        
        Returns:
            Dictionary with generated text and metadata
        """
        try:
            start_time = time.time()
            
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "text": response.content[0].text,
                "model": model,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "latency_ms": latency_ms,
                "stop_reason": response.stop_reason
            }
            
        except Exception as e:
            logger.error(f"Error in Anthropic generation with system prompt: {str(e)}")
            raise
    
    async def generate_streaming(
        self,
        prompt: str,
        model: str = "claude-3-opus-20240229",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        Generate text with streaming
        
        Args:
            prompt: Input prompt
            model: Model name
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        
        Yields:
            Streaming text chunks
        """
        try:
            with self.client.messages.stream(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            ) as stream:
                for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            logger.error(f"Error in Anthropic streaming generation: {str(e)}")
            raise
    
    def get_available_models(self) -> list:
        """Get list of available models"""
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1",
            "claude-2.0",
            "claude-instant-1.2"
        ]