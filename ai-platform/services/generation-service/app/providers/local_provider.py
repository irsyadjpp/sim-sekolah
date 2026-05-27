"""
Local LLM provider for text generation
Supports local models like Qwen, Mistral, and LLaMA
"""
import time
from typing import Dict, Any, Optional
import logging

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("Transformers library not available")

logger = logging.getLogger(__name__)


class LocalProvider:
    """Local LLM provider for text generation"""
    
    def __init__(self, device: str = "cuda"):
        """
        Initialize local provider
        
        Args:
            device: Device to use (cuda/cpu)
        """
        self.device = device if torch.cuda.is_available() else "cpu"
        self.models = {}
        self.tokenizers = {}
        
        logger.info(f"Initializing local provider on device: {self.device}")
        
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers library not available, using fallback")
    
    async def generate(
        self,
        prompt: str,
        model: str = "default",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Generate text using local LLM
        
        Args:
            prompt: Input prompt
            model: Model name or identifier
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        
        Returns:
            Dictionary with generated text and metadata
        """
        try:
            if not TRANSFORMERS_AVAILABLE:
                return self._fallback_generation(prompt, temperature, max_tokens)
            
            start_time = time.time()
            
            # Load model if not already loaded
            if model not in self.models:
                await self._load_model(model)
            
            # Tokenize input
            tokenizer = self.tokenizers[model]
            model_instance = self.models[model]
            
            inputs = tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = model_instance.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Decode output
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove input prompt from output
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            result = {
                "text": generated_text,
                "model": model,
                "tokens_used": len(outputs[0]),
                "latency_ms": latency_ms
            }
            
            logger.info(f"Local generation completed. Model: {model}, Latency: {latency_ms}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in local generation: {str(e)}")
            # Fallback to simple generation
            return self._fallback_generation(prompt, temperature, max_tokens)
    
    async def _load_model(self, model_name: str):
        """
        Load a local model
        
        Args:
            model_name: Name of the model to load
        """
        try:
            # Model mapping (simplified)
            model_map = {
                "default": "Qwen/Qwen2.5-0.5B-Instruct",
                "qwen": "Qwen/Qwen2.5-0.5B-Instruct",
                "mistral": "mistralai/Mistral-7B-Instruct-v0.2",
                "llama": "meta-llama/Llama-2-7b-chat-hf"
            }
            
            actual_model = model_map.get(model_name, model_name)
            
            logger.info(f"Loading model: {actual_model}")
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(actual_model)
            model = AutoModelForCausalLM.from_pretrained(
                actual_model,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            if self.device == "cpu":
                model = model.to(self.device)
            
            self.tokenizers[model_name] = tokenizer
            self.models[model_name] = model
            
            logger.info(f"Model {model_name} loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            raise
    
    def _fallback_generation(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> Dict[str, Any]:
        """
        Fallback generation when transformers is not available
        
        Args:
            prompt: Input prompt
            temperature: Temperature (ignored in fallback)
            max_tokens: Maximum tokens (ignored in fallback)
        
        Returns:
            Dictionary with generated text and metadata
        """
        start_time = time.time()
        
        # Simple rule-based fallback
        generated_text = f"Based on the prompt: {prompt}\n\nThis is a fallback response as the local LLM is not properly configured."
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        return {
            "text": generated_text,
            "model": "fallback",
            "tokens_used": len(generated_text.split()),
            "latency_ms": latency_ms
        }
    
    async def generate_with_system_prompt(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "default",
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
        # Combine prompts
        combined_prompt = f"{system_prompt}\n\n{user_prompt}"
        return await self.generate(combined_prompt, model, temperature, max_tokens)
    
    def get_available_models(self) -> list:
        """Get list of available local models"""
        return [
            "default",
            "qwen",
            "mistral",
            "llama"
        ]