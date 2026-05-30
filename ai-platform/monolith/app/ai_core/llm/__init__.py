"""
LLM Manager Module

This module provides LLM provider management, prompt engineering, and model management
for all AI operations in the platform.
"""

from .providers import LLMProviderFactory
from .prompt_engineering import PromptManager
from .model_management import ModelManager

__all__ = [
    "LLMManager",
    "LLMProviderFactory",
    "PromptManager", 
    "ModelManager"
]

class LLMManager:
    """Main class for LLM management"""
    
    def __init__(self):
        self.provider_factory = LLMProviderFactory()
        self.prompt_manager = PromptManager()
        self.model_manager = ModelManager()
    
    def get_provider(self, provider_name: str):
        """Get specific LLM provider"""
        return self.provider_factory.get_provider(provider_name)
    
    def get_prompt_template(self, template_name: str):
        """Get prompt template"""
        return self.prompt_manager.get_template(template_name)
    
    def select_model(self, task_type: str, requirements: dict):
        """Select appropriate model for task"""
        return self.model_manager.select_model(task_type, requirements)