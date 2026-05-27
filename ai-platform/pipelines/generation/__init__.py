"""
Generation pipeline module

This module provides Prefect-based DAGs for AI response generation:
- Complete RAG pipeline (retrieval → context → LLM → guard)
- Batch generation for multiple queries
- Guard rail validation (safety, quality, accuracy, policy)
"""

from pipelines.generation.dag import (
    retrieve_documents,
    assemble_context,
    generate_response,
    guard_rails,
    generation_pipeline,
    batch_generation_pipeline
)

__all__ = [
    "retrieve_documents",
    "assemble_context",
    "generate_response",
    "guard_rails",
    "generation_pipeline",
    "batch_generation_pipeline"
]