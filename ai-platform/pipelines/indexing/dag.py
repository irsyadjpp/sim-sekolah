"""
Indexing DAG for document processing

This pipeline handles:
- Document chunking into manageable segments
- Vector storage for semantic search
- Graph edge creation for knowledge relationships
"""

from prefect import task, flow, get_run_logger
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

from shared.observability import get_tracer
from shared.logging import get_logger
from storage.abstractions import QdrantDB, Neo4jDB, StorageConfig

logger = get_logger(__name__)


@task(name="chunk_document")
async def chunk_document(
    document_id: str,
    content: str,
    metadata: Dict[str, Any],
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> List[Dict[str, Any]]:
    """
    Split document into chunks for processing.
    
    Args:
        document_id: Document identifier
        content: Document content text
        metadata: Document metadata
        chunk_size: Target chunk size in words
        chunk_overlap: Overlap between chunks in words
        
    Returns:
        List of document chunks
    """
    logger = get_run_logger()
    tracer = get_tracer("indexing")
    
    with tracer.span("chunk_document", kind="internal"):
        logger.info(f"Chunking document {document_id}")
        
        words = content.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - chunk_overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join chunk_words)
            
            if not chunk_text.strip():
                continue
            
            chunk = {
                "chunk_id": f"{document_id}_chunk_{len(chunks)}",
                "document_id": document_id,
                "chunk_index": len(chunks),
                "content": chunk_text,
                "word_count": len(chunk_words),
                "start_pos": i,
                "end_pos": min(i + chunk_size, len(words)),
                "metadata": {
                    **metadata,
                    "chunk_type": "semantic"
                }
            }
            
            chunks.append(chunk)
        
        logger.info(f"Document chunked into {len(chunks)} chunks")
        return chunks


@task(name="create_embeddings")
async def create_embeddings(
    chunks: List[Dict[str, Any]],
    model_name: str = "bge-m3",
    batch_size: int = 10
) -> List[Dict[str, Any]]:
    """
    Create embeddings for document chunks.
    
    Args:
        chunks: List of document chunks
        model_name: Embedding model name
        batch_size: Batch size for embedding generation
        
    Returns:
        List of embeddings with vector data
    """
    logger = get_run_logger()
    tracer = get_tracer("indexing")
    
    with tracer.span("create_embeddings", kind="internal"):
        logger.info(f"Creating embeddings for {len(chunks)} chunks using {model_name}")
        
        embeddings = []
        
        # Process in batches
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [chunk["content"] for chunk in batch]
            
            # In production, this would call the embedding service
            batch_embeddings = await _generate_embeddings_batch(texts, model_name)
            
            for j, embedding in enumerate(batch_embeddings):
                chunk = batch[j]
                embeddings.append({
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "embedding": embedding["vector"],
                    "model": model_name,
                    "dimension": len(embedding["vector"]),
                    "metadata": chunk["metadata"]
                })
        
        logger.info(f"Created {len(embeddings)} embeddings")
        return embeddings


@task(name="store_vectors")
async def store_vectors(
    embeddings: List[Dict[str, Any]],
    collection_name: str = "document_embeddings"
) -> Dict[str, Any]:
    """
    Store embeddings in vector database.
    
    Args:
        embeddings: List of embeddings with vector data
        collection_name: Vector collection name
        
    Returns:
        Storage result
    """
    logger = get_run_logger()
    tracer = get_tracer("indexing")
    
    with tracer.span("store_vectors", kind="internal"):
        logger.info(f"Storing {len(embeddings)} vectors in {collection_name}")
        
        # Get Qdrant client
        config = StorageConfig.from_env(prefix="QDRANT_")
        async with QdrantDB(config) as qdrant:
            # Ensure collection exists
            if not await qdrant.collection_exists(collection_name):
                logger.info(f"Creating collection {collection_name}")
                await qdrant.create_collection(
                    collection_name=collection_name,
                    vector_size=embeddings[0]["dimension"],
                    distance_metric="Cosine"
                )
            
            # Prepare vectors for insertion
            vectors = [emb["embedding"] for emb in embeddings]
            payloads = [
                {
                    "chunk_id": emb["chunk_id"],
                    "document_id": emb["document_id"],
                    "content": emb.get("content", ""),
                    **emb["metadata"]
                }
                for emb in embeddings
            ]
            ids = [emb["chunk_id"] for emb in embeddings]
            
            # Insert vectors
            vector_ids = await qdrant.insert_vectors(
                collection_name=collection_name,
                vectors=vectors,
                payloads=payloads,
                ids=ids
            )
            
            logger.info(f"Stored {len(vector_ids)} vectors in Qdrant")
            
            return {
                "collection_name": collection_name,
                "vector_count": len(vector_ids),
                "vector_ids": vector_ids,
                "stored_at": datetime.utcnow().isoformat()
            }


@task(name="create_graph_nodes")
async def create_graph_nodes(
    document_id: str,
    metadata: Dict[str, Any]
) -> Dict[str, str]:
    """
    Create graph nodes for document entities.
    
    Args:
        document_id: Document identifier
        metadata: Document metadata
        
    Returns:
        Created node IDs
    """
    logger = get_run_logger()
    tracer = get_tracer("indexing")
    
    with tracer.span("create_graph_nodes", kind="internal"):
        logger.info(f"Creating graph nodes for document {document_id}")
        
        # Get Neo4j client
        config = StorageConfig.from_env(prefix="NEO4J_")
        async with Neo4jDB(config) as neo4j:
            # Create document node
            doc_node_id = await neo4j.create_node(
                label="Document",
                properties={
                    "document_id": document_id,
                    **metadata
                }
            )
            
            # Create concept nodes from document
            concept_nodes = {}
            for key, value in metadata.items():
                if key in ["subject", "topic", "difficulty"]:
                    node_id = await neo4j.create_node(
                        label="Concept",
                        properties={
                            "name": value,
                            "type": key,
                            "source_document": document_id
                        }
                    )
                    concept_nodes[key] = node_id
            
            logger.info(f"Created {1 + len(concept_nodes)} graph nodes")
            
            return {
                "document_node_id": doc_node_id,
                "concept_node_ids": concept_nodes
            }


@task(name="create_graph_edges")
async def create_graph_edges(
    document_node_id: str,
    concept_node_ids: Dict[str, str],
    document_id: str
) -> Dict[str, Any]:
    """
    Create graph edges between document and concepts.
    
    Args:
        document_node_id: Document node ID
        concept_node_ids: Concept node IDs
        document_id: Document identifier
        
    Returns:
        Edge creation result
    """
    logger = get_run_logger()
    tracer = get_tracer("indexing")
    
    with tracer.span("create_graph_edges", kind="internal"):
        logger.info(f"Creating graph edges for document {document_id}")
        
        # Get Neo4j client
        config = StorageConfig.from_env(prefix="NEO4J_")
        async with Neo4jDB(config) as neo4j:
            edge_ids = []
            
            # Create edges from document to concepts
            for concept_type, concept_node_id in concept_node_ids.items():
                edge_id = await neo4j.create_relationship(
                    from_node_id=document_node_id,
                    to_node_id=concept_node_id,
                    relationship_type="HAS_CONCEPT",
                    properties={
                        "strength": 1.0,
                        "created_at": datetime.utcnow().isoformat()
                    }
                )
                edge_ids.append(edge_id)
            
            # Create concept-to-concept relationships if applicable
            # In production, this would use ontology information
            if len(concept_node_ids) > 1:
                concepts = list(concept_node_ids.keys())
                for i in range(len(concepts) - 1):
                    edge_id = await neo4j.create_relationship(
                        from_node_id=concept_node_ids[concepts[i]],
                        to_node_id=concept_node_ids[concepts[i + 1]],
                        relationship_type="RELATED_TO",
                        properties={
                            "strength": 0.5,
                            "context": document_id
                        }
                    )
                    edge_ids.append(edge_id)
            
            logger.info(f"Created {len(edge_ids)} graph edges")
            
            return {
                "edge_count": len(edge_ids),
                "edge_ids": edge_ids,
                "created_at": datetime.utcnow().isoformat()
            }


@task(name="update_indexing_status")
async def update_indexing_status(
    document_id: str,
    indexing_results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update document indexing status.
    
    Args:
        document_id: Document identifier
        indexing_results: Combined indexing results
        
    Returns:
        Update result
    """
    logger = get_run_logger()
    tracer = get_tracer("indexing")
    
    with tracer.span("update_indexing_status", kind="internal"):
        logger.info(f"Updating indexing status for document {document_id}")
        
        # Update in database (placeholder)
        update_result = await _update_document_status_in_db(
            document_id,
            "indexed",
            indexing_results
        )
        
        result = {
            "document_id": document_id,
            "status": "indexed",
            "chunk_count": indexing_results.get("chunk_count"),
            "vector_count": indexing_results.get("vector_count"),
            "graph_nodes": indexing_results.get("graph_nodes"),
            "graph_edges": indexing_results.get("graph_edges"),
            "indexed_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Indexing status updated for document {document_id}")
        return result


@flow(name="indexing_pipeline")
async def indexing_pipeline(
    document_id: str,
    content: str,
    metadata: Dict[str, Any],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    model_name: str = "bge-m3",
    skip_graph: bool = False
) -> Dict[str, Any]:
    """
    Complete indexing pipeline for document.
    
    Args:
        document_id: Document identifier
        content: Document content text
        metadata: Document metadata
        chunk_size: Target chunk size in words
        chunk_overlap: Overlap between chunks in words
        model_name: Embedding model name
        skip_graph: Skip graph creation
        
    Returns:
        Combined indexing results
    """
    logger = get_run_logger()
    logger.info(f"Starting indexing pipeline for document {document_id}")
    
    indexing_results = {}
    
    # Chunk document
    chunks = await chunk_document(
        document_id=document_id,
        content=content,
        metadata=metadata,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    indexing_results["chunk_count"] = len(chunks)
    
    # Create embeddings
    embeddings = await create_embeddings(
        chunks=chunks,
        model_name=model_name
    )
    indexing_results["embedding_count"] = len(embeddings)
    
    # Store vectors
    vector_result = await store_vectors(
        embeddings=embeddings
    )
    indexing_results["vector_storage"] = vector_result
    
    # Create graph nodes and edges
    if not skip_graph:
        graph_nodes = await create_graph_nodes(
            document_id=document_id,
            metadata=metadata
        )
        indexing_results["graph_nodes"] = graph_nodes
        
        graph_edges = await create_graph_edges(
            document_node_id=graph_nodes["document_node_id"],
            concept_node_ids=graph_nodes["concept_node_ids"],
            document_id=document_id
        )
        indexing_results["graph_edges"] = graph_edges
    
    # Update indexing status
    status_result = await update_indexing_status(
        document_id=document_id,
        indexing_results=indexing_results
    )
    indexing_results["status_update"] = status_result
    
    logger.info(f"Indexing pipeline completed for document {document_id}")
    return {
        "document_id": document_id,
        "indexing_results": indexing_results,
        "pipeline_status": "completed"
    }


@flow(name="batch_indexing_pipeline")
async def batch_indexing_pipeline(
    documents: List[Dict[str, Any]],
    batch_size: int = 5
) -> Dict[str, Any]:
    """
    Batch indexing pipeline for multiple documents.
    
    Args:
        documents: List of documents with content and metadata
        batch_size: Number of documents to process in parallel
        
    Returns:
        Combined indexing results for all documents
    """
    logger = get_run_logger()
    logger.info(f"Starting batch indexing for {len(documents)} documents")
    
    results = []
    
    # Process documents in batches
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        
        # Process batch in parallel
        tasks = [
            indexing_pipeline(
                document_id=doc["document_id"],
                content=doc["content"],
                metadata=doc.get("metadata", {}),
                chunk_size=doc.get("chunk_size", 500),
                chunk_overlap=doc.get("chunk_overlap", 50),
                model_name=doc.get("model_name", "bge-m3"),
                skip_graph=doc.get("skip_graph", False)
            )
            for doc in batch
        ]
        
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
    
    logger.info(f"Batch indexing completed for {len(results)} documents")
    
    return {
        "total_documents": len(documents),
        "successful_indexing": len(results),
        "results": results
    }


# Helper functions
async def _generate_embeddings_batch(texts: List[str], model_name: str) -> List[Dict[str, Any]]:
    """Generate embeddings for a batch of texts (placeholder)."""
    # In production, this would call the embedding service
    # For now, return mock embeddings
    import numpy as np
    
    embeddings = []
    for text in texts:
        # Mock embedding generation
        vector = np.random.rand(1024).tolist()
        embeddings.append({
            "vector": vector,
            "model": model_name,
            "dimension": 1024,
            "text_preview": text[:100]  # Preview for debugging
        })
    
    return embeddings


async def _update_document_status_in_db(
    document_id: str,
    status: str,
    results: Dict[str, Any]
) -> Dict[str, Any]:
    """Update document status in database (placeholder)."""
    # In production, this would call the document service
    logger.info(f"Updating document {document_id} status to {status}")
    
    return {
        "document_id": document_id,
        "status": status,
        "results": results,
        "success": True
    }