"""
Context builder for creating context from retrieved documents
Supports different strategies for organizing retrieved content
"""
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ContextBuilder:
    """Context builder for creating context from retrieved documents"""
    
    def __init__(self):
        """Initialize context builder"""
        logger.info("Initializing context builder")
    
    async def build(
        self,
        documents: List[Dict[str, Any]],
        max_tokens: int = 2000,
        strategy: str = "ranked"
    ) -> str:
        """
        Build context from retrieved documents
        
        Args:
            documents: List of retrieved documents
            max_tokens: Maximum tokens in context
            strategy: Context building strategy (concatenate, ranked, diverse, summarize)
        
        Returns:
            Built context string
        """
        try:
            if not documents:
                return ""
            
            if strategy == "concatenate":
                return self._concatenate_context(documents, max_tokens)
            elif strategy == "ranked":
                return self._ranked_context(documents, max_tokens)
            elif strategy == "diverse":
                return self._diverse_context(documents, max_tokens)
            elif strategy == "summarize":
                return self._summarized_context(documents, max_tokens)
            else:
                return self._ranked_context(documents, max_tokens)
                
        except Exception as e:
            logger.error(f"Error building context: {str(e)}")
            raise
    
    def _concatenate_context(self, documents: List[Dict[str, Any]], max_tokens: int) -> str:
        """
        Simple concatenation of documents
        
        Args:
            documents: List of documents
            max_tokens: Maximum tokens
        
        Returns:
            Concatenated context
        """
        context_parts = []
        current_tokens = 0
        
        for doc in documents:
            content = doc.get("content", "")
            tokens = self._estimate_tokens(content)
            
            if current_tokens + tokens > max_tokens:
                # Truncate to fit
                remaining = max_tokens - current_tokens
                content = content[:remaining * 4]  # Rough estimate: 1 token ≈ 4 chars
                context_parts.append(content)
                break
            
            context_parts.append(content)
            current_tokens += tokens
        
        return "\n\n".join(context_parts)
    
    def _ranked_context(self, documents: List[Dict[str, Any]], max_tokens: int) -> str:
        """
        Ranked context with scores and citations
        
        Args:
            documents: List of documents
            max_tokens: Maximum tokens
        
        Returns:
            Ranked context with citations
        """
        context_parts = []
        current_tokens = 0
        
        for i, doc in enumerate(documents):
            content = doc.get("content", "")
            score = doc.get("score", 0.0)
            doc_id = doc.get("id", str(i))
            
            # Add citation header
            header = f"[Source {i+1}] (Score: {score:.2f})\n"
            tokens = self._estimate_tokens(header + content)
            
            if current_tokens + tokens > max_tokens:
                # Truncate to fit
                remaining = max_tokens - current_tokens
                content = content[:remaining * 4]
                context_parts.append(header + content)
                break
            
            context_parts.append(header + content)
            current_tokens += tokens
        
        return "\n\n".join(context_parts)
    
    def _diverse_context(self, documents: List[Dict[str, Any]], max_tokens: int) -> str:
        """
        Diverse context selecting documents with different metadata
        
        Args:
            documents: List of documents
            max_tokens: Maximum tokens
        
        Returns:
            Diverse context
        """
        # Group documents by metadata to ensure diversity
        grouped = {}
        for doc in documents:
            metadata = doc.get("metadata", {})
            # Use competency type or subject as grouping key
            key = metadata.get("competency_type", metadata.get("subject", "general"))
            
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(doc)
        
        # Select documents from different groups
        diverse_docs = []
        groups = list(grouped.keys())
        
        # Round-robin selection from different groups
        i = 0
        while len(diverse_docs) < len(documents) and groups:
            for group in groups:
                if grouped[group]:
                    diverse_docs.append(grouped[group].pop(0))
                else:
                    groups.remove(group)
            
            i += 1
            if i > len(groups):
                break
        
        # Build context from diverse documents
        return self._ranked_context(diverse_docs, max_tokens)
    
    def _summarized_context(self, documents: List[Dict[str, Any]], max_tokens: int) -> str:
        """
        Summarized context (simplified - would use LLM in production)
        
        Args:
            documents: List of documents
            max_tokens: Maximum tokens
        
        Returns:
            Summarized context
        """
        # In production, this would use an LLM to summarize
        # For now, use ranked context as fallback
        
        context_parts = []
        current_tokens = 0
        
        for doc in documents:
            content = doc.get("content", "")
            
            # Simple summary: first and last sentences
            sentences = content.split(". ")
            if len(sentences) > 2:
                summary = f"{sentences[0]}. ... {sentences[-1]}."
            else:
                summary = content
            
            tokens = self._estimate_tokens(summary)
            
            if current_tokens + tokens > max_tokens:
                remaining = max_tokens - current_tokens
                summary = summary[:remaining * 4]
                context_parts.append(summary)
                break
            
            context_parts.append(summary)
            current_tokens += tokens
        
        return "\n\n".join(context_parts)
    
    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate token count (rough approximation)
        
        Args:
            text: Text to estimate
        
        Returns:
            Estimated token count
        """
        # Rough approximation: 1 token ≈ 4 characters
        return len(text) // 4
    
    async def build_with_citations(
        self,
        documents: List[Dict[str, Any]],
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Build context with citation metadata
        
        Args:
            documents: List of documents
            max_tokens: Maximum tokens
        
        Returns:
            Dictionary with context and citation information
        """
        context = await self.build(
            documents=documents,
            max_tokens=max_tokens,
            strategy="ranked"
        )
        
        citations = []
        for i, doc in enumerate(documents):
            citations.append({
                "id": doc.get("id", str(i)),
                "source": doc.get("metadata", {}).get("source", "unknown"),
                "score": doc.get("score", 0.0)
            })
        
        return {
            "context": context,
            "citations": citations,
            "citation_count": len(citations),
            "strategy": "ranked_with_citations"
        }