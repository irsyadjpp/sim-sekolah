"""
Memory Manager Module

This module provides memory systems for AI agents to maintain context and learn from interactions:
- Vector memory for semantic similarity search
- Episodic memory for learning sequences
- Semantic memory for knowledge graph integration
"""

from .vector_memory import VectorMemory
from .episodic_memory import EpisodicMemory
from .semantic_memory import SemanticMemory

__all__ = [
    "MemoryManager",
    "VectorMemory",
    "EpisodicMemory",
    "SemanticMemory"
]

class MemoryManager:
    """Main class for memory management"""
    
    def __init__(self):
        self.vector_memory = VectorMemory()
        self.episodic_memory = EpisodicMemory()
        self.semantic_memory = SemanticMemory()
    
    def store(self, memory_type: str, data: dict) -> dict:
        """Store data in specified memory system"""
        if memory_type == "vector":
            return self.vector_memory.store(data)
        elif memory_type == "episodic":
            return self.episodic_memory.store(data)
        elif memory_type == "semantic":
            return self.semantic_memory.store(data)
        else:
            return {"error": f"Unknown memory type: {memory_type}"}
    
    def retrieve(self, memory_type: str, query: dict) -> dict:
        """Retrieve data from specified memory system"""
        if memory_type == "vector":
            return self.vector_memory.retrieve(query)
        elif memory_type == "episodic":
            return self.episodic_memory.retrieve(query)
        elif memory_type == "semantic":
            return self.semantic_memory.retrieve(query)
        else:
            return {"error": f"Unknown memory type: {memory_type}"}