"""
Base Document Worker Template
Reusable worker code for document processing with observability
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from abc import ABC, abstractmethod
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseWorker(ABC):
    """Base worker class with observability"""
    
    def __init__(self, worker_name: str):
        self.worker_name = worker_name
        self.processed_count = 0
        self.failed_count = 0
        self.total_latency_ms = 0
        self.start_time = None
    
    @abstractmethod
    def process(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single item"""
        pass
    
    def process_with_observability(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Process item with observability metrics"""
        start_time = time.time()
        
        try:
            result = self.process(item)
            
            # Record metrics
            latency_ms = (time.time() - start_time) * 1000
            self.total_latency_ms += latency_ms
            self.processed_count += 1
            
            # Log with metrics
            logger.info(
                f"Worker {self.worker_name} processed item {item.get('id', 'unknown')} "
                f"in {latency_ms:.2f}ms"
            )
            
            # Add metrics to result
            result["_metrics"] = {
                "worker": self.worker_name,
                "latency_ms": latency_ms,
                "processed_at": datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            self.failed_count += 1
            latency_ms = (time.time() - start_time) * 1000
            logger.error(f"Worker {self.worker_name} failed to process item: {e}")
            
            return {
                "error": str(e),
                "_metrics": {
                    "worker": self.worker_name,
                    "latency_ms": latency_ms,
                    "processed_at": datetime.utcnow().isoformat(),
                    "failed": True
                }
            }
    
    def process_batch(self, items: list) -> list:
        """Process multiple items"""
        results = []
        for item in items:
            result = self.process_with_observability(item)
            results.append(result)
        return results
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get worker metrics"""
        avg_latency = self.total_latency_ms / max(self.processed_count, 1)
        success_rate = self.processed_count / max(self.processed_count + self.failed_count, 1)
        
        return {
            "worker_name": self.worker_name,
            "processed_count": self.processed_count,
            "failed_count": self.failed_count,
            "success_rate": success_rate,
            "average_latency_ms": avg_latency,
            "total_latency_ms": self.total_latency_ms
        }
    
    def reset_metrics(self):
        """Reset worker metrics"""
        self.processed_count = 0
        self.failed_count = 0
        self.total_latency_ms = 0


class DocumentParsingWorker(BaseWorker):
    """Worker for parsing documents"""
    
    def __init__(self):
        super().__init__("document_parsing_worker")
    
    def process(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Parse document"""
        content = item.get("content", "")
        source = item.get("source", "")
        
        # Simulate parsing
        parsed = {
            "id": item.get("id"),
            "content": content,
            "source": source,
            "parsed": True,
            "sections": self._extract_sections(content),
            "metadata": {
                "word_count": len(content.split()),
                "char_count": len(content)
            }
        }
        
        return parsed
    
    def _extract_sections(self, content: str) -> list:
        """Extract sections from content"""
        # Simplified section extraction
        sections = []
        lines = content.split("\n")
        current_section = "Introduction"
        section_content = []
        
        for line in lines:
            if line.strip().startswith("#"):
                if section_content:
                    sections.append({
                        "title": current_section,
                        "content": "\n".join(section_content)
                    })
                current_section = line.strip("#").strip()
                section_content = []
            else:
                section_content.append(line)
        
        if section_content:
            sections.append({
                "title": current_section,
                "content": "\n".join(section_content)
            })
        
        return sections


class DocumentChunkingWorker(BaseWorker):
    """Worker for chunking documents"""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        super().__init__("document_chunking_worker")
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def process(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Chunk document"""
        content = item.get("content", "")
        
        chunks = self._chunk_text(content)
        
        return {
            "id": item.get("id"),
            "chunks": chunks,
            "chunk_count": len(chunks),
            "chunk_size": self.chunk_size,
            "overlap": self.overlap
        }
    
    def _chunk_text(self, text: str) -> list:
        """Chunk text into segments"""
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size):
            chunk_words = words[i:i + self.chunk_size + self.overlap]
            chunk = " ".join(chunk_words)
            chunks.append(chunk)
        
        return chunks


# Example usage
if __name__ == "__main__":
    # Example document
    document = {
        "id": "doc_001",
        "content": "# Introduction\nThis is the introduction.\n\n# Section 1\nThis is section 1 content.",
        "source": "knowledge/cp"
    }
    
    # Parse document
    parsing_worker = DocumentParsingWorker()
    parsed = parsing_worker.process_with_observability(document)
    print(f"Parsed: {parsed}")
    print(f"Metrics: {parsing_worker.get_metrics()}")
    
    # Chunk document
    chunking_worker = DocumentChunkingWorker(chunk_size=10, overlap=2)
    chunked = chunking_worker.process_with_observability(document)
    print(f"\nChunked: {chunked}")
    print(f"Metrics: {chunking_worker.get_metrics()}")
