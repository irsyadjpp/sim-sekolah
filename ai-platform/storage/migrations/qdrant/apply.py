"""
Qdrant collection management script

This script applies collection schemas to Qdrant vector database.
"""

import argparse
import asyncio
import sys
import os
from typing import List

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PayloadSchema

# Import collection definitions
from collections.document_embeddings import (
    COLLECTION_NAME as DOC_EMBEDDINGS,
    get_collection_config as get_doc_config,
    get_vector_params as get_doc_params,
    PAYLOAD_INDEXES as DOC_INDEXES,
)
from collections.knowledge_embeddings import (
    COLLECTION_NAME as KNOWLEDGE_EMBEDDINGS,
    get_collection_config as get_knowledge_config,
    get_vector_params as get_knowledge_params,
    PAYLOAD_INDEXES as KNOWLEDGE_INDEXES,
)
from collections.conversation_embeddings import (
    COLLECTION_NAME as CONV_EMBEDDINGS,
    get_collection_config as get_conv_config,
    get_vector_params as get_conv_params,
    PAYLOAD_INDEXES as CONV_INDEXES,
)


# Collection registry
COLLECTIONS = {
    "document_embeddings": {
        "name": DOC_EMBEDDINGS,
        "config": get_doc_config,
        "params": get_doc_params,
        "indexes": DOC_INDEXES,
    },
    "knowledge_embeddings": {
        "name": KNOWLEDGE_EMBEDDINGS,
        "config": get_knowledge_config,
        "params": get_knowledge_params,
        "indexes": KNOWLEDGE_INDEXES,
    },
    "conversation_embeddings": {
        "name": CONV_EMBEDDINGS,
        "config": get_conv_config,
        "params": get_conv_params,
        "indexes": CONV_INDEXES,
    },
}


def get_qdrant_client() -> QdrantClient:
    """
    Get Qdrant client from environment variables.
    
    Returns:
        QdrantClient instance
    """
    host = os.getenv("QDRANT_HOST", "localhost")
    port = int(os.getenv("QDRANT_PORT", "6333"))
    
    return QdrantClient(url=f"http://{host}:{port}", prefer_grpc=False)


def list_collections(client: QdrantClient) -> List[str]:
    """
    List all collections in Qdrant.
    
    Args:
        client: Qdrant client
        
    Returns:
        List of collection names
    """
    collections = client.get_collections()
    return [c.name for c in collections]


def collection_exists(client: QdrantClient, collection_name: str) -> bool:
    """
    Check if collection exists.
    
    Args:
        client: Qdrant client
        collection_name: Collection name
        
    Returns:
        True if collection exists
    """
    collections = list_collections(client)
    return collection_name in collections


def create_collection(
    client: QdrantClient,
    collection_key: str,
    vector_size: int = 1024,
    recreate: bool = False,
) -> bool:
    """
    Create a Qdrant collection from schema.
    
    Args:
        client: Qdrant client
        collection_key: Key from COLLECTIONS registry
        vector_size: Vector dimension size
        recreate: Drop and recreate if exists
        
    Returns:
        True if successful
    """
    if collection_key not in COLLECTIONS:
        print(f"Error: Unknown collection '{collection_key}'")
        return False
    
    collection_info = COLLECTIONS[collection_key]
    collection_name = collection_info["name"]
    
    # Check if collection exists
    if collection_exists(client, collection_name):
        if recreate:
            print(f"Dropping existing collection '{collection_name}'...")
            client.delete_collection(collection_name)
        else:
            print(f"Collection '{collection_name}' already exists. Use --recreate to overwrite.")
            return True
    
    # Create collection
    print(f"Creating collection '{collection_name}'...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=collection_info["params"](vector_size),
        optimizers_config=collection_info["config"]()["optimizers_config"],
        replication_factor=collection_info["config"]()["replication_factor"],
        write_consistency_factor=collection_info["config"]()["write_consistency_factor"],
        on_disk=collection_info["config"]()["on_disk"],
    )
    
    # Create payload indexes
    for index_config in collection_info["indexes"]:
        try:
            client.create_payload_index(
                collection_name=collection_name,
                field_name=index_config["field_name"],
                field_schema=index_config["field_schema"],
            )
            print(f"Created index on field '{index_config['field_name']}'")
        except Exception as e:
            print(f"Warning: Could not create index on '{index_config['field_name']}': {e}")
    
    print(f"Collection '{collection_name}' created successfully")
    return True


def delete_collection(client: QdrantClient, collection_name: str) -> bool:
    """
    Delete a Qdrant collection.
    
    Args:
        client: Qdrant client
        collection_name: Collection name
        
    Returns:
        True if successful
    """
    if not collection_exists(client, collection_name):
        print(f"Collection '{collection_name}' does not exist")
        return False
    
    print(f"Deleting collection '{collection_name}'...")
    client.delete_collection(collection_name)
    print(f"Collection '{collection_name}' deleted successfully")
    return True


def get_collection_info(client: QdrantClient, collection_name: str) -> dict:
    """
    Get information about a collection.
    
    Args:
        client: Qdrant client
        collection_name: Collection name
        
    Returns:
        Collection information dictionary
    """
    if not collection_exists(client, collection_name):
        print(f"Collection '{collection_name}' does not exist")
        return {}
    
    info = client.get_collection(collection_name)
    return {
        "name": info.name,
        "vector_size": info.config.params.vectors.size,
        "distance": str(info.config.params.distance),
        "vectors_count": info.points_count,
        "status": info.status,
    }


def main():
    parser = argparse.ArgumentParser(description="Qdrant collection management")
    parser.add_argument("--list", action="store_true", help="List all collections")
    parser.add_argument("--collection", type=str, help="Collection name to operate on")
    parser.add_argument("--create", action="store_true", help="Create collection")
    parser.add_argument("--delete", action="store_true", help="Delete collection")
    parser.add_argument("--info", action="store_true", help="Get collection info")
    parser.add_argument("--all", action="store_true", help="Operate on all collections")
    parser.add_argument("--recreate", action="store_true", help="Drop and recreate collection")
    parser.add_argument("--vector-size", type=int, default=1024, help="Vector dimension size")
    
    args = parser.parse_args()
    
    # Get Qdrant client
    client = get_qdrant_client()
    
    try:
        # List collections
        if args.list:
            collections = list_collections(client)
            print("Existing collections:")
            for col in collections:
                print(f"  - {col}")
            return
        
        # Create collections
        if args.create:
            if args.all:
                for collection_key in COLLECTIONS:
                    create_collection(client, collection_key, args.vector_size, args.recreate)
            elif args.collection:
                create_collection(client, args.collection, args.vector_size, args.recreate)
            else:
                print("Error: Specify --collection or --all")
                parser.print_help()
            return
        
        # Delete collections
        if args.delete:
            if args.collection:
                delete_collection(client, args.collection)
            else:
                print("Error: Specify --collection")
                parser.print_help()
            return
        
        # Get collection info
        if args.info:
            if args.collection:
                info = get_collection_info(client, args.collection)
                if info:
                    print("Collection info:")
                    for key, value in info.items():
                        print(f"  {key}: {value}")
            else:
                print("Error: Specify --collection")
                parser.print_help()
            return
        
        # No action specified
        parser.print_help()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()