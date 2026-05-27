"""
Workflow helpers for end-to-end tests
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """
    Orchestrates complex end-to-end workflows for testing.
    
    This class provides methods to coordinate multiple service calls
    and verify the complete workflow execution.
    """
    
    def __init__(self, service_clients: Dict[str, Any], storage_clients: Dict[str, Any]):
        """
        Initialize workflow orchestrator.
        
        Args:
            service_clients: Dictionary of service clients
            storage_clients: Dictionary of storage clients
        """
        self.service_clients = service_clients
        self.storage_clients = storage_clients
        self.workflow_steps = []
    
    async def execute_step(self, step_name: str, coro):
        """
        Execute a workflow step with logging and error handling.
        
        Args:
            step_name: Name of the workflow step
            coro: Coroutine to execute
            
        Returns:
            Result of the coroutine
        """
        start_time = datetime.utcnow()
        logger.info(f"Starting step: {step_name}")
        
        try:
            result = await coro
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            self.workflow_steps.append({
                "name": step_name,
                "status": "success",
                "duration": duration,
                "timestamp": start_time.isoformat()
            })
            
            logger.info(f"Completed step: {step_name} in {duration:.2f}s")
            return result
            
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            self.workflow_steps.append({
                "name": step_name,
                "status": "failed",
                "duration": duration,
                "error": str(e),
                "timestamp": start_time.isoformat()
            })
            
            logger.error(f"Failed step: {step_name} after {duration:.2f}s: {e}")
            raise
    
    def get_workflow_summary(self) -> Dict[str, Any]:
        """
        Get summary of workflow execution.
        
        Returns:
            Workflow summary dictionary
        """
        total_duration = sum(step["duration"] for step in self.workflow_steps)
        failed_steps = [step for step in self.workflow_steps if step["status"] == "failed"]
        
        return {
            "total_steps": len(self.workflow_steps),
            "successful_steps": len(self.workflow_steps) - len(failed_steps),
            "failed_steps": len(failed_steps),
            "total_duration": total_duration,
            "status": "failed" if failed_steps else "success",
            "steps": self.workflow_steps
        }


async def ingest_document_workflow(
    document_client,
    embedding_client,
    qdrant_client,
    document_data: Dict[str, Any],
    orchestrator: Optional[WorkflowOrchestrator] = None
) -> Dict[str, Any]:
    """
    Execute complete document ingestion workflow.
    
    Args:
        document_client: Document service client
        embedding_client: Embedding service client
        qdrant_client: Qdrant client
        document_data: Document data to ingest
        orchestrator: Workflow orchestrator for tracking
        
    Returns:
        Workflow result dictionary
    """
    if orchestrator:
        # Step 1: Upload document
        upload_result = await orchestrator.execute_step(
            "upload_document",
            document_client.upload_document(
                title=document_data["title"],
                content=document_data["content"],
                metadata=document_data.get("metadata", {})
            )
        )
        document_id = upload_result["document_id"]
        
        # Step 2: Create embeddings
        embedding_result = await orchestrator.execute_step(
            "create_embeddings",
            embedding_client.batch_create_embeddings(
                texts=[document_data["content"]]
            )
        )
        
        # Step 3: Store vectors
        vector_result = await orchestrator.execute_step(
            "store_vectors",
            qdrant_client.insert_vectors(
                collection_name="document_embeddings",
                vectors=[emb["vector"] for emb in embedding_result["embeddings"]],
                payloads=[{
                    "document_id": document_id,
                    "content": document_data["content"],
                    **document_data.get("metadata", {})
                }],
                ids=[emb["embedding_id"] for emb in embedding_result["embeddings"]]
            )
        )
        
        return {
            "document_id": document_id,
            "embedding_ids": [emb["embedding_id"] for emb in embedding_result["embeddings"]],
            "status": "success"
        }
    else:
        # Simple execution without orchestrator
        upload_result = await document_client.upload_document(
            title=document_data["title"],
            content=document_data["content"],
            metadata=document_data.get("metadata", {})
        )
        
        embedding_result = await embedding_client.batch_create_embeddings(
            texts=[document_data["content"]]
        )
        
        await qdrant_client.insert_vectors(
            collection_name="document_embeddings",
            vectors=[emb["vector"] for emb in embedding_result["embeddings"]],
            payloads=[{
                "document_id": upload_result["document_id"],
                "content": document_data["content"],
                **document_data.get("metadata", {})
            }],
            ids=[emb["embedding_id"] for emb in embedding_result["embeddings"]]
        )
        
        return {
            "document_id": upload_result["document_id"],
            "embedding_ids": [emb["embedding_id"] for emb in embedding_result["embeddings"]],
            "status": "success"
        }


async def rag_workflow(
    retrieval_client,
    generation_client,
    guard_client,
    query: str,
    orchestrator: Optional[WorkflowOrchestrator] = None
) -> Dict[str, Any]:
    """
    Execute complete RAG (Retrieval-Augmented Generation) workflow.
    
    Args:
        retrieval_client: Retrieval service client
        generation_client: Generation service client
        guard_client: Guard service client
        query: User query
        orchestrator: Workflow orchestrator for tracking
        
    Returns:
        Workflow result dictionary
    """
    if orchestrator:
        # Step 1: Retrieve relevant documents
        retrieval_result = await orchestrator.execute_step(
            "retrieve_documents",
            retrieval_client.search(query=query, limit=5)
        )
        
        # Step 2: Generate response with context
        generation_result = await orchestrator.execute_step(
            "generate_response",
            generation_client.generate_with_rag(
                query=query,
                retrieved_docs=retrieval_result["results"]
            )
        )
        
        # Step 3: Apply guard rails
        guard_result = await orchestrator.execute_step(
            "apply_guards",
            guard_client.check_response(
                response=generation_result["response"],
                context=retrieval_result["results"]
            )
        )
        
        return {
            "query": query,
            "response": generation_result["response"],
            "sources": retrieval_result["results"],
            "guard_checks": guard_result,
            "status": "success" if guard_result["passed"] else "blocked"
        }
    else:
        # Simple execution without orchestrator
        retrieval_result = await retrieval_client.search(query=query, limit=5)
        
        generation_result = await generation_client.generate_with_rag(
            query=query,
            retrieved_docs=retrieval_result["results"]
        )
        
        guard_result = await guard_client.check_response(
            response=generation_result["response"],
            context=retrieval_result["results"]
        )
        
        return {
            "query": query,
            "response": generation_result["response"],
            "sources": retrieval_result["results"],
            "guard_checks": guard_result,
            "status": "success" if guard_result["passed"] else "blocked"
        }


async def conversation_workflow(
    document_client,
    retrieval_client,
    generation_client,
    guard_client,
    user_id: str,
    messages: List[Dict[str, str]],
    orchestrator: Optional[WorkflowOrchestrator] = None
) -> Dict[str, Any]:
    """
    Execute complete conversation workflow.
    
    Args:
        document_client: Document service client
        retrieval_client: Retrieval service client
        generation_client: Generation service client
        guard_client: Guard service client
        user_id: User ID
        messages: List of conversation messages
        orchestrator: Workflow orchestrator for tracking
        
    Returns:
        Workflow result dictionary
    """
    conversation_responses = []
    
    if orchestrator:
        # Create conversation
        conversation_result = await orchestrator.execute_step(
            "create_conversation",
            document_client.create_conversation(user_id=user_id)
        )
        conversation_id = conversation_result["conversation_id"]
        
        # Process each message
        for i, message in enumerate(messages):
            # Add user message
            await orchestrator.execute_step(
                f"add_message_{i}",
                document_client.add_message(
                    conversation_id=conversation_id,
                    role=message["role"],
                    content=message["content"]
                )
            )
            
            if message["role"] == "user":
                # Generate response
                rag_result = await rag_workflow(
                    retrieval_client,
                    generation_client,
                    guard_client,
                    message["content"],
                    orchestrator
                )
                
                conversation_responses.append(rag_result)
                
                # Add assistant response
                await orchestrator.execute_step(
                    f"add_response_{i}",
                    document_client.add_message(
                        conversation_id=conversation_id,
                        role="assistant",
                        content=rag_result["response"]
                    )
                )
        
        return {
            "conversation_id": conversation_id,
            "responses": conversation_responses,
            "status": "success"
        }
    else:
        # Simple execution without orchestrator
        conversation_result = await document_client.create_conversation(user_id=user_id)
        conversation_id = conversation_result["conversation_id"]
        
        for i, message in enumerate(messages):
            await document_client.add_message(
                conversation_id=conversation_id,
                role=message["role"],
                content=message["content"]
            )
            
            if message["role"] == "user":
                rag_result = await rag_workflow(
                    retrieval_client,
                    generation_client,
                    guard_client,
                    message["content"],
                    None
                )
                
                conversation_responses.append(rag_result)
                
                await document_client.add_message(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=rag_result["response"]
                )
        
        return {
            "conversation_id": conversation_id,
            "responses": conversation_responses,
            "status": "success"
        }


async def wait_for_condition(
    condition_check,
    timeout: int = 30,
    interval: float = 1.0,
    timeout_message: str = "Condition not met within timeout"
) -> Any:
    """
    Wait for a condition to be met with timeout.
    
    Args:
        condition_check: Async function that returns True when condition is met
        timeout: Maximum wait time in seconds
        interval: Check interval in seconds
        timeout_message: Message to use if timeout is reached
        
    Returns:
        Result from condition check
        
    Raises:
        TimeoutError: If condition is not met within timeout
    """
    start_time = asyncio.get_event_loop().time()
    
    while True:
        result = await condition_check()
        if result:
            return result
        
        if asyncio.get_event_loop().time() - start_time > timeout:
            raise TimeoutError(timeout_message)
        
        await asyncio.sleep(interval)