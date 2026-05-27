"""
Indexing Pipeline - Vector Store + Graph Edges
Indexes documents into vector store and creates graph edges for knowledge graph
"""
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import dataclass
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EnrichedDocument:
    """Enriched document to be indexed"""
    id: str
    content: str
    source: str
    enriched_metadata: Dict[str, Any]
    tags: List[str]
    difficulty: str
    taxonomies: List[str]
    competencies: List[str]


@dataclass
class VectorIndexResult:
    """Result of vector indexing"""
    document_id: str
    vector_id: str
    success: bool
    error: Optional[str] = None


@dataclass
class GraphEdge:
    """Graph edge for knowledge graph"""
    id: str
    source: str
    target: str
    relation: str
    weight: float
    metadata: Dict[str, Any]


class VectorIndexer:
    """Indexes documents into vector store"""
    
    def __init__(self):
        self.vector_store = {}  # In-memory vector store (in production, use Qdrant/Weaviate)
        self.indexed_count = 0
    
    def index_document(self, document: EnrichedDocument) -> VectorIndexResult:
        """Index a single document into vector store"""
        try:
            # Generate embedding (simplified - in production use embedding service)
            embedding = self._generate_embedding(document.content)
            
            # Store in vector store
            vector_id = f"vec_{document.id}"
            self.vector_store[vector_id] = {
                "id": vector_id,
                "document_id": document.id,
                "embedding": embedding,
                "metadata": document.enriched_metadata,
                "content": document.content
            }
            
            self.indexed_count += 1
            logger.info(f"Indexed document {document.id} as vector {vector_id}")
            
            return VectorIndexResult(
                document_id=document.id,
                vector_id=vector_id,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error indexing document {document.id}: {e}")
            return VectorIndexResult(
                document_id=document.id,
                vector_id="",
                success=False,
                error=str(e)
            )
    
    def index_batch(self, documents: List[EnrichedDocument]) -> List[VectorIndexResult]:
        """Index multiple documents"""
        results = []
        for doc in documents:
            result = self.index_document(doc)
            results.append(result)
        return results
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding (simplified)"""
        # In production, call embedding service
        # For now, generate a simple hash-based embedding
        import hashlib
        hash_obj = hashlib.md5(text.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Convert to float vector
        embedding = [float(int(hash_hex[i:i+2], 16) / 255.0) for i in range(0, min(len(hash_hex), 768), 2)]
        
        # Pad to 768 dimensions (common embedding size)
        while len(embedding) < 768:
            embedding.append(0.0)
        
        return embedding[:768]


class GraphEdgeBuilder:
    """Builds graph edges for knowledge graph"""
    
    def __init__(self):
        self.edges = []
        self.edge_count = 0
    
    def build_edges(self, document: EnrichedDocument) -> List[GraphEdge]:
        """Build graph edges from document metadata"""
        edges = []
        
        # Build competency edges
        for competency in document.competencies:
            edge = GraphEdge(
                id=f"edge_{uuid.uuid4().hex[:8]}",
                source=document.id,
                target=f"competency_{competency}",
                relation="has_competency",
                weight=1.0,
                metadata={
                    "document_source": document.source,
                    "difficulty": document.difficulty
                }
            )
            edges.append(edge)
        
        # Build taxonomy edges
        for taxonomy in document.taxonomies:
            edge = GraphEdge(
                id=f"edge_{uuid.uuid4().hex[:8]}",
                source=document.id,
                target=f"taxonomy_{taxonomy}",
                relation="belongs_to_taxonomy",
                weight=0.8,
                metadata={
                    "document_source": document.source
                }
            )
            edges.append(edge)
        
        # Build difficulty edges
        edge = GraphEdge(
            id=f"edge_{uuid.uuid4().hex[:8]}",
            source=document.id,
            target=f"difficulty_{document.difficulty}",
            relation="has_difficulty",
            weight=0.5,
            metadata={}
        )
        edges.append(edge)
        
        self.edges.extend(edges)
        self.edge_count += len(edges)
        
        logger.info(f"Built {len(edges)} edges for document {document.id}")
        
        return edges
    
    def build_batch_edges(self, documents: List[EnrichedDocument]) -> List[GraphEdge]:
        """Build edges for multiple documents"""
        all_edges = []
        for doc in documents:
            edges = self.build_edges(doc)
            all_edges.extend(edges)
        return all_edges
    
    def get_edges(self) -> List[GraphEdge]:
        """Get all built edges"""
        return self.edges


class IndexingPipeline:
    """Pipeline for indexing documents into vector store and building graph edges"""
    
    def __init__(self):
        self.vector_indexer = VectorIndexer()
        self.graph_builder = GraphEdgeBuilder()
        self.processed_count = 0
        self.failed_count = 0
    
    def run(self, documents: List[EnrichedDocument]) -> Tuple[List[VectorIndexResult], List[GraphEdge]]:
        """Run indexing pipeline"""
        logger.info(f"Starting indexing pipeline for {len(documents)} documents")
        
        # Index into vector store
        vector_results = self.vector_indexer.index_batch(documents)
        
        # Build graph edges
        graph_edges = self.graph_builder.build_batch_edges(documents)
        
        # Count successes/failures
        self.processed_count = sum(1 for r in vector_results if r.success)
        self.failed_count = sum(1 for r in vector_results if not r.success)
        
        logger.info(f"Indexing pipeline complete: {self.processed_count} indexed, {self.failed_count} failed")
        logger.info(f"Built {len(graph_edges)} graph edges")
        
        return vector_results, graph_edges
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        return {
            "vector_indexed": self.vector_indexer.indexed_count,
            "graph_edges": self.graph_builder.edge_count,
            "processed": self.processed_count,
            "failed": self.failed_count,
            "success_rate": self.processed_count / max(self.processed_count + self.failed_count, 1)
        }


# Example usage
if __name__ == "__main__":
    # Example enriched documents
    from pipelines.enrichment.metadata_tagging_pipeline import Document, MetadataTagger
    
    documents = [
        Document(
            id="doc1",
            content="This is a basic introduction to numbers and counting for beginners.",
            source="knowledge/cp",
            metadata={"grade": "1", "subject": "mathematics"}
        ),
        Document(
            id="doc2",
            content="Students will learn to apply algebraic concepts to solve complex problems.",
            source="knowledge/cp",
            metadata={"grade": "8", "subject": "mathematics"}
        )
    ]
    
    # Enrich documents first
    tagger = MetadataTagger()
    enriched = tagger.tag_batch(documents)
    
    # Index documents
    pipeline = IndexingPipeline()
    vector_results, graph_edges = pipeline.run(enriched)
    
    print(f"Vector indexing results:")
    for result in vector_results:
        print(f"  {result.document_id}: {'SUCCESS' if result.success else 'FAILED'}")
    
    print(f"\nGraph edges built: {len(graph_edges)}")
    for edge in graph_edges[:5]:  # Show first 5
        print(f"  {edge.source} --[{edge.relation}]--> {edge.target}")
    
    print(f"\nPipeline stats: {pipeline.get_stats()}")
