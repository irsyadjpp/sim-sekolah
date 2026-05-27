"""
Ingestion Pipeline DAG - Document → Parsed → Chunked → Embedded

This Prefect flow orchestrates the complete document ingestion process.
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from prefect.context import get_run_context

from ..config import PipelineConfig, get_flow_run_id, get_flow_name
from shared.events import DocumentUploadedEvent, DocumentProcessedEvent, EventType
from shared.schemas import DocumentStatus


# Initialize configuration
config = PipelineConfig.from_env()


@task(
    name="validate_document",
    retries=3,
    retry_delay_seconds=5,
    cache_key_fn=task_input_hash,
)
async def validate_document(document_id: str, file_path: str) -> Dict[str, Any]:
    """
    Validate document before processing.
    
    Args:
        document_id: Document ID
        file_path: Path to document file
        
    Returns:
        Validation result with metadata
    """
    logger = get_run_logger()
    logger.info(f"Validating document {document_id}")
    
    # Check if file exists and is accessible
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Document file not found: {file_path}")
    
    # Get file metadata
    file_size = path.stat().st_size
    file_extension = path.suffix.lower()
    
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
    if file_extension not in allowed_extensions:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    # Validate file size (max 100MB)
    max_size = 100 * 1024 * 1024  # 100MB
    if file_size > max_size:
        raise ValueError(f"File too large: {file_size} bytes (max {max_size})")
    
    metadata = {
        "document_id": document_id,
        "file_path": file_path,
        "file_size": file_size,
        "file_extension": file_extension,
        "validated_at": datetime.utcnow().isoformat(),
    }
    
    logger.info(f"Document {document_id} validated successfully")
    return metadata


@task(
    name="parse_document",
    retries=3,
    retry_delay_seconds=10,
    timeout_seconds=300,
)
async def parse_document(document_id: str, file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse document using Parser Service.
    
    Args:
        document_id: Document ID
        file_path: Path to document file
        metadata: Document metadata
        
    Returns:
        Parsing result with extracted content
    """
    logger = get_run_logger()
    logger.info(f"Parsing document {document_id}")
    
    # Import here to avoid issues if service is not available
    import httpx
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        # Upload file to parser service
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = await client.post(
                f"{config.PARSER_SERVICE_URL}/parse",
                files=files,
                data={
                    "document_id": document_id,
                    "extract_images": "true",
                    "extract_tables": "true",
                }
            )
        
        response.raise_for_status()
        result = response.json()
        
    logger.info(f"Document {document_id} parsed successfully: {result.get('pages_count', 0)} pages")
    return result


@task(
    name="chunk_document",
    retries=3,
    retry_delay_seconds=5,
    timeout_seconds=180,
)
async def chunk_document(document_id: str, parsed_content: Dict[str, Any]) -> Dict[str, Any]:
    """
    Chunk parsed document using Semantic Chunk Service.
    
    Args:
        document_id: Document ID
        parsed_content: Parsed document content
        
    Returns:
        Chunking result with chunk IDs
    """
    logger = get_run_logger()
    logger.info(f"Chunking document {document_id}")
    
    import httpx
    
    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(
            f"{config.CHUNK_SERVICE_URL}/chunk",
            json={
                "document_id": document_id,
                "content": parsed_content.get("text_content", ""),
                "metadata": parsed_content.get("metadata", {}),
                "strategy": "semantic",
                "chunk_size": config.CHUNK_SIZE,
                "chunk_overlap": config.CHUNK_OVERLAP,
            }
        )
        
        response.raise_for_status()
        result = response.json()
        
    logger.info(f"Document {document_id} chunked successfully: {result.get('chunks_count', 0)} chunks")
    return result


@task(
    name="embed_chunks",
    retries=3,
    retry_delay_seconds=10,
    timeout_seconds=600,
)
async def embed_chunks(document_id: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate embeddings for document chunks using Embedding Service.
    
    Args:
        document_id: Document ID
        chunks: List of document chunks
        
    Returns:
        Embedding result with vector IDs
    """
    logger = get_run_logger()
    logger.info(f"Generating embeddings for {len(chunks)} chunks of document {document_id}")
    
    import httpx
    
    async with httpx.AsyncClient(timeout=600.0) as client:
        # Process in batches
        batch_size = config.EMBEDDING_BATCH_SIZE
        all_results = []
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            
            response = await client.post(
                f"{config.EMBEDDING_SERVICE_URL}/batch",
                json={
                    "texts": [chunk.get("content", "") for chunk in batch],
                    "model": config.EMBEDDING_MODEL,
                    "document_id": document_id,
                    "chunk_ids": [chunk.get("chunk_id") for chunk in batch],
                }
            )
            
            response.raise_for_status()
            batch_result = response.json()
            all_results.extend(batch_result.get("embeddings", []))
            
            logger.info(f"Processed batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size}")
        
    logger.info(f"Generated {len(all_results)} embeddings for document {document_id}")
    return {"embeddings": all_results, "count": len(all_results)}


@task(
    name="index_vectors",
    retries=3,
    retry_delay_seconds=5,
    timeout_seconds=120,
)
async def index_vectors(document_id: str, embeddings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Index document vectors in Qdrant using Retrieval Service.
    
    Args:
        document_id: Document ID
        embeddings: Embedding data with vectors
        
    Returns:
        Indexing result
    """
    logger = get_run_logger()
    logger.info(f"Indexing vectors for document {document_id}")
    
    import httpx
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{config.RETRIEVAL_SERVICE_URL}/index",
            json={
                "document_id": document_id,
                "embeddings": embeddings.get("embeddings", []),
            }
        )
        
        response.raise_for_status()
        result = response.json()
        
    logger.info(f"Document {document_id} indexed successfully")
    return result


@task(
    name="update_document_status",
    retries=3,
    retry_delay_seconds=5,
)
async def update_document_status(document_id: str, status: DocumentStatus, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update document status in database.
    
    Args:
        document_id: Document ID
        status: New document status
        metadata: Additional metadata
        
    Returns:
        Update result
    """
    logger = get_run_logger()
    logger.info(f"Updating document {document_id} status to {status}")
    
    # This would typically update a database
    # For now, we'll just log the update
    result = {
        "document_id": document_id,
        "status": status,
        "updated_at": datetime.utcnow().isoformat(),
        "metadata": metadata,
    }
    
    logger.info(f"Document {document_id} status updated to {status}")
    return result


@task(
    name="emit_event",
    retries=3,
    retry_delay_seconds=5,
)
async def emit_event(event_type: EventType, event_data: Dict[str, Any]):
    """
    Emit event to message queue for other services.
    
    Args:
        event_type: Type of event to emit
        event_data: Event data payload
    """
    logger = get_run_logger()
    logger.info(f"Emitting event: {event_type}")
    
    # This would typically publish to RabbitMQ
    # For now, we'll just log the event
    logger.info(f"Event emitted: {event_type} - {event_data}")


@flow(
    name="document_ingestion_flow",
    description="Complete document ingestion pipeline: Document → Parsed → Chunked → Embedded → Indexed",
    timeout_seconds=1800,  # 30 minutes
)
async def document_ingestion_flow(
    document_id: str,
    file_path: str,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main ingestion flow for document processing.
    
    This flow orchestrates the complete document ingestion process:
    1. Validate document
    2. Parse document content
    3. Chunk document into semantic units
    4. Generate embeddings for chunks
    5. Index vectors in vector database
    6. Update document status
    7. Emit completion events
    
    Args:
        document_id: Document ID
        file_path: Path to document file
        user_id: Optional user ID who uploaded the document
        
    Returns:
        Processing result with summary
    """
    logger = get_run_logger()
    flow_run_id = get_flow_run_id()
    
    logger.info(f"Starting document ingestion flow for {document_id}")
    logger.info(f"Flow run ID: {flow_run_id}")
    
    try:
        # Step 1: Validate document
        validation_result = await validate_document(document_id, file_path)
        await update_document_status(document_id, DocumentStatus.PROCESSING, validation_result)
        
        # Step 2: Parse document
        parse_result = await parse_document(document_id, file_path, validation_result)
        
        # Step 3: Chunk document
        chunk_result = await chunk_document(document_id, parse_result)
        
        # Step 4: Generate embeddings
        embedding_result = await embed_chunks(document_id, chunk_result.get("chunks", []))
        
        # Step 5: Index vectors
        index_result = await index_vectors(document_id, embedding_result)
        
        # Step 6: Update document status to completed
        final_metadata = {
            "pages_count": parse_result.get("pages_count", 0),
            "chunks_count": chunk_result.get("chunks_count", 0),
            "embeddings_count": embedding_result.get("count", 0),
            "processing_time_seconds": 0,  # Would calculate actual time
        }
        await update_document_status(document_id, DocumentStatus.COMPLETED, final_metadata)
        
        # Step 7: Emit completion event
        await emit_event(
            EventType.DOCUMENT_PROCESSED,
            {
                "document_id": document_id,
                "user_id": user_id,
                "flow_run_id": flow_run_id,
                "metadata": final_metadata,
            }
        )
        
        result = {
            "document_id": document_id,
            "status": "completed",
            "pages_count": parse_result.get("pages_count", 0),
            "chunks_count": chunk_result.get("chunks_count", 0),
            "embeddings_count": embedding_result.get("count", 0),
            "flow_run_id": flow_run_id,
        }
        
        logger.info(f"Document ingestion flow completed successfully for {document_id}")
        return result
        
    except Exception as e:
        logger.error(f"Document ingestion flow failed for {document_id}: {str(e)}")
        
        # Update status to failed
        await update_document_status(
            document_id,
            DocumentStatus.FAILED,
            {"error": str(e), "flow_run_id": flow_run_id}
        )
        
        # Emit failure event
        await emit_event(
            EventType.DOCUMENT_FAILED,
            {
                "document_id": document_id,
                "user_id": user_id,
                "flow_run_id": flow_run_id,
                "error": str(e),
            }
        )
        
        raise


@flow(
    name="batch_document_ingestion_flow",
    description="Batch document ingestion for multiple documents",
    timeout_seconds=3600,  # 60 minutes
)
async def batch_document_ingestion_flow(
    documents: List[Dict[str, Any]],
    max_concurrent: int = 4,
) -> Dict[str, Any]:
    """
    Batch ingestion flow for processing multiple documents concurrently.
    
    Args:
        documents: List of document dictionaries with 'document_id' and 'file_path'
        max_concurrent: Maximum number of concurrent document ingestions
        
    Returns:
        Batch processing result with summary
    """
    logger = get_run_logger()
    logger.info(f"Starting batch document ingestion for {len(documents)} documents")
    
    # Process documents concurrently with limit
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_with_semaphore(doc: Dict[str, Any]) -> Dict[str, Any]:
        async with semaphore:
            try:
                return await document_ingestion_flow(
                    document_id=doc["document_id"],
                    file_path=doc["file_path"],
                    user_id=doc.get("user_id"),
                )
            except Exception as e:
                logger.error(f"Failed to process document {doc['document_id']}: {str(e)}")
                return {
                    "document_id": doc["document_id"],
                    "status": "failed",
                    "error": str(e),
                }
    
    results = await asyncio.gather(
        *[process_with_semaphore(doc) for doc in documents],
        return_exceptions=True
    )
    
    # Count successes and failures
    successful = sum(1 for r in results if isinstance(r, dict) and r.get("status") == "completed")
    failed = len(results) - successful
    
    summary = {
        "total_documents": len(documents),
        "successful": successful,
        "failed": failed,
        "results": results,
    }
    
    logger.info(f"Batch ingestion completed: {successful} successful, {failed} failed")
    return summary