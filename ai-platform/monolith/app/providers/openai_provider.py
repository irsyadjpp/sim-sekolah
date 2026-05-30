"""
OpenAI provider for text generation
Supports GPT-4, GPT-4 Turbo, and GPT-3.5 Turbo
"""
import os
import time
from typing import Dict, Any, Optional
import logging

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library not available")

logger = logging.getLogger(__name__)


class OpenAIProvider:
    """OpenAI provider for text generation"""
    
    def __init__(self, api_key: str):
        """
        Initialize OpenAI provider
        
        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key
        self.client = None
        
        logger.info("Initializing OpenAI provider")
        
        if not OPENAI_AVAILABLE:
            logger.error("OpenAI library not available")
            raise ImportError("OpenAI library is required but not installed")
        
        try:
            self.client = openai.OpenAI(api_key=api_key)
            logger.info("OpenAI provider initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI provider: {str(e)}")
            raise
    
    async def generate(
        self,
        prompt: str,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Generate text using OpenAI
        
        Args:
            prompt: Input prompt
            model: Model name (gpt-4, gpt-4-turbo, gpt-3.5-turbo)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        
        Returns:
            Dictionary with generated text and metadata
        """
        try:
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            result = {
                "text": response.choices[0].message.content,
                "model": model,
                "tokens_used": response.usage.total_tokens,
                "latency_ms": latency_ms,
                "finish_reason": response.choices[0].finish_reason
            }
            
            logger.info(f"OpenAI generation completed. Model: {model}, Tokens: {result['tokens_used']}, Latency: {latency_ms}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in OpenAI generation: {str(e)}")
            raise
    
    async def generate_with_system_prompt(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "gpt-4",
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
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "text": response.choices[0].message.content,
                "model": model,
                "tokens_used": response.usage.total_tokens,
                "latency_ms": latency_ms,
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            logger.error(f"Error in OpenAI generation with system prompt: {str(e)}")
            raise
    
    async def generate_streaming(
        self,
        prompt: str,
        model: str = "gpt-4",
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
            stream = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error in OpenAI streaming generation: {str(e)}")
            raise
    
    def get_available_models(self) -> list:
        """Get list of available models"""
        return [
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-4-1106-preview",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-1106"
        ]