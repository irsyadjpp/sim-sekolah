"""
Test fixtures for integration tests
"""

import asyncio
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime


def generate_test_document_id() -> str:
    """Generate a test document ID."""
    return f"test-doc-{uuid.uuid4().hex[:8]}"


def generate_test_user_id() -> str:
    """Generate a test user ID."""
    return f"test-user-{uuid.uuid4().hex[:8]}"


def generate_test_conversation_id() -> str:
    """Generate a test conversation ID."""
    return f"test-conv-{uuid.uuid4().hex[:8]}"


def create_test_document(
    title: str = "Test Document",
    content: str = "This is a test document for integration testing.",
    file_type: str = "txt",
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a test document.
    
    Args:
        title: Document title
        content: Document content
        file_type: File type
        metadata: Additional metadata
        
    Returns:
        Document dictionary
    """
    return {
        "document_id": generate_test_document_id(),
        "title": title,
        "content": content,
        "file_type": file_type,
        "file_size": len(content.encode('utf-8')),
        "status": "pending",
        "source": "test_fixture",
        "metadata": metadata or {
            "test": True,
            "created_by": "integration_test"
        },
        "created_at": datetime.utcnow().isoformat()
    }


def create_test_user(
    email: str = "test@example.com",
    username: str = "testuser",
    full_name: str = "Test User",
    role: str = "user",
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a test user.
    
    Args:
        email: User email
        username: Username
        full_name: Full name
        role: User role
        metadata: Additional metadata
        
    Returns:
        User dictionary
    """
    return {
        "user_id": generate_test_user_id(),
        "email": email,
        "username": username,
        "full_name": full_name,
        "role": role,
        "metadata": metadata or {
            "test": True,
            "created_by": "integration_test"
        },
        "created_at": datetime.utcnow().isoformat()
    }


def create_test_conversation(
    user_id: str,
    title: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a test conversation.
    
    Args:
        user_id: User ID
        title: Conversation title
        context: Conversation context
        
    Returns:
        Conversation dictionary
    """
    return {
        "conversation_id": generate_test_conversation_id(),
        "user_id": user_id,
        "title": title or "Test Conversation",
        "context": context or {},
        "metadata": {
            "test": True,
            "created_by": "integration_test"
        },
        "created_at": datetime.utcnow().isoformat()
    }


def create_test_message(
    conversation_id: str,
    role: str = "user",
    content: str = "Test message",
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a test message.
    
    Args:
        conversation_id: Conversation ID
        role: Message role (user/assistant/system)
        content: Message content
        metadata: Additional metadata
        
    Returns:
        Message dictionary
    """
    return {
        "message_id": f"test-msg-{uuid.uuid4().hex[:8]}",
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "metadata": metadata or {
            "test": True
        },
        "created_at": datetime.utcnow().isoformat()
    }


def create_test_embedding(
    text: str,
    model: str = "bge-m3",
    dimension: int = 1024
) -> Dict[str, Any]:
    """
    Create a test embedding.
    
    Args:
        text: Text that was embedded
        model: Embedding model name
        dimension: Embedding dimension
        
    Returns:
        Embedding dictionary
    """
    import random
    
    return {
        "embedding_id": f"test-emb-{uuid.uuid4().hex[:8]}",
        "text": text,
        "vector": [random.random() for _ in range(dimension)],
        "model": model,
        "dimension": dimension,
        "created_at": datetime.utcnow().isoformat()
    }


def create_test_search_result(
    document_id: str,
    score: float,
    content: str = "Sample content"
) -> Dict[str, Any]:
    """
    Create a test search result.
    
    Args:
        document_id: Document ID
        score: Similarity score
        content: Content snippet
        
    Returns:
        Search result dictionary
    """
    return {
        "document_id": document_id,
        "chunk_id": f"test-chunk-{uuid.uuid4().hex[:8]}",
        "score": score,
        "content": content,
        "metadata": {
            "test": True
        }
    }


def create_test_graph_node(
    label: str = "Concept",
    properties: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a test graph node.
    
    Args:
        label: Node label
        properties: Node properties
        
    Returns:
        Node dictionary
    """
    return {
        "id": f"test-node-{uuid.uuid4().hex[:8]}",
        "label": label,
        "properties": properties or {
            "name": "Test Concept",
            "test": True
        }
    }


def create_test_graph_edge(
    from_node: str,
    to_node: str,
    edge_type: str = "RELATED_TO",
    properties: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a test graph edge.
    
    Args:
        from_node: Source node ID
        to_node: Target node ID
        edge_type: Edge type
        properties: Edge properties
        
    Returns:
        Edge dictionary
    """
    return {
        "id": f"test-edge-{uuid.uuid4().hex[:8]}",
        "from": from_node,
        "to": to_node,
        "type": edge_type,
        "properties": properties or {
            "strength": 0.8,
            "test": True
        }
    }


def create_test_batch_documents(count: int = 5) -> List[Dict[str, Any]]:
    """
    Create a batch of test documents.
    
    Args:
        count: Number of documents to create
        
    Returns:
        List of document dictionaries
    """
    return [
        create_test_document(
            title=f"Test Document {i}",
            content=f"This is test document {i} for batch processing."
        )
        for i in range(count)
    ]


def create_test_pagination_response(
    data: List[Any],
    page: int = 1,
    page_size: int = 10,
    total: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a test paginated response.
    
    Args:
        data: Data items
        page: Current page
        page_size: Page size
        total: Total items (defaults to len(data))
        
    Returns:
        Paginated response dictionary
    """
    total = total or len(data)
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "data": data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages
        }
    }


def create_test_error_response(
    message: str,
    code: int = 500,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a test error response.
    
    Args:
        message: Error message
        code: Error code
        details: Additional error details
        
    Returns:
        Error response dictionary
    """
    return {
        "error": True,
        "message": message,
        "code": code,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat()
    }


async def cleanup_test_document(document_id: str, document_client):
    """
    Cleanup test document after test.
    
    Args:
        document_id: Document ID to cleanup
        document_client: Document service client
    """
    try:
        await document_client.delete_document(document_id)
    except Exception as e:
        print(f"Warning: Failed to cleanup document {document_id}: {e}")


async def cleanup_test_user(user_id: str, user_client):
    """
    Cleanup test user after test.
    
    Args:
        user_id: User ID to cleanup
        user_client: User service client
    """
    try:
        await user_client.delete_user(user_id)
    except Exception as e:
        print(f"Warning: Failed to cleanup user {user_id}: {e}")


# Context manager for test cleanup
class TestCleanup:
    """Context manager for test resource cleanup."""
    
    def __init__(self):
        self.cleanup_tasks = []
    
    def add_cleanup(self, coro):
        """Add a cleanup coroutine to be executed on exit."""
        self.cleanup_tasks.append(coro)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Execute all cleanup tasks."""
        for task in self.cleanup_tasks:
            try:
                await task
            except Exception as e:
                print(f"Warning: Cleanup task failed: {e}")
        self.cleanup_tasks.clear()
        return False