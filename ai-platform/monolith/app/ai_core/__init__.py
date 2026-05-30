"""
AI Core - AI Layer Separation Domain

This domain provides clear separation for all AI capabilities, making them reusable,
maintainable, and upgradeable independently from business logic.

Components:
- LLM providers and management
- Embedding systems
- Reranking strategies
- AI agents for different domains
- Reasoning chains
- Memory systems (vector, episodic, semantic)
- Orchestration frameworks
"""

from .llm import LLMManager
from .embeddings import EmbeddingManager
from .reranking import RerankingEngine
from .agents import AgentManager
from .reasoning import ReasoningEngine
from .memory import MemoryManager
from .orchestration import OrchestrationEngine

__all__ = [
    "AICore",
    "LLMManager",
    "EmbeddingManager",
    "RerankingEngine",
    "AgentManager",
    "ReasoningEngine",
    "MemoryManager",
    "OrchestrationEngine"
]

class AICore:
    """Main class for AI Core domain operations"""
    
    def __init__(self):
        self.llm_manager = LLMManager()
        self.embedding_manager = EmbeddingManager()
        self.reranking_engine = RerankingEngine()
        self.agent_manager = AgentManager()
        self.reasoning_engine = ReasoningEngine()
        self.memory_manager = MemoryManager()
        self.orchestration_engine = OrchestrationEngine()
    
    def get_llm_provider(self, provider_name: str):
        """Get specific LLM provider"""
        return self.llm_manager.get_provider(provider_name)
    
    def get_embedding_model(self, model_name: str):
        """Get specific embedding model"""
        return self.embedding_manager.get_model(model_name)
    
    def get_agent(self, agent_type: str):
        """Get specific AI agent"""
        return self.agent_manager.get_agent(agent_type)
    
    def orchestrate_agents(self, task: str, agents: list):
        """Orchestrate multiple agents for a task"""
        return self.orchestration_engine.orchestrate_agents(task, agents)
    
    def reason(self, context: dict, reasoning_type: str):
        """Perform reasoning on context"""
        return self.reasoning_engine.reason(context, reasoning_type)
    
    def store_memory(self, memory_type: str, data: dict):
        """Store data in memory system"""
        return self.memory_manager.store(memory_type, data)
    
    def retrieve_memory(self, memory_type: str, query: dict):
        """Retrieve data from memory system"""
        return self.memory_manager.retrieve(memory_type, query)