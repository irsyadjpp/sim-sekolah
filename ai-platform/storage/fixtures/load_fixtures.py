"""
Fixture loading script for AI Platform storage backends

This script loads test fixtures into PostgreSQL, Qdrant, and Neo4j for testing and CI/CD.
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from storage.abstractions import PostgreSQL, QdrantDB, Neo4jDB, StorageConfig


def load_postgres_fixtures(config: StorageConfig, sql_file: str) -> bool:
    """
    Load SQL fixtures into PostgreSQL.
    
    Args:
        config: PostgreSQL configuration
        sql_file: Path to SQL file
        
    Returns:
        True if successful
    """
    import subprocess
    
    print(f"Loading PostgreSQL fixtures from {sql_file}...")
    
    try:
        # Use psql command line tool
        cmd = [
            "psql",
            "-h", config.host,
            "-p", str(config.port),
            "-U", config.username,
            "-d", config.database,
            "-f", sql_file
        ]
        
        # Set PGPASSWORD environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = config.password
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("PostgreSQL fixtures loaded successfully")
            return True
        else:
            print(f"Error loading PostgreSQL fixtures: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error loading PostgreSQL fixtures: {e}")
        return False


async def load_qdrant_fixtures(config: StorageConfig, vector_file: str) -> bool:
    """
    Load vector fixtures into Qdrant.
    
    Args:
        config: Qdrant configuration
        vector_file: Path to vector JSON file
        
    Returns:
        True if successful
    """
    print(f"Loading Qdrant fixtures from {vector_file}...")
    
    try:
        # Load vector data from JSON file
        with open(vector_file, 'r') as f:
            data = json.load(f)
        
        vectors = data.get("vectors", [])
        if not vectors:
            print("No vectors found in fixture file")
            return False
        
        # Connect to Qdrant
        async with QdrantDB(config) as qdrant:
            # Ensure collection exists
            collection_name = "document_embeddings"
            if not await qdrant.collection_exists(collection_name):
                print(f"Creating collection {collection_name}...")
                await qdrant.create_collection(
                    collection_name=collection_name,
                    vector_size=data["metadata"]["dimension"],
                    distance_metric="Cosine"
                )
            
            # Insert vectors
            vector_values = [v["values"] for v in vectors]
            payloads = [
                {
                    "chunk_id": v["chunk_id"],
                    "document_id": v["document_id"],
                    **v.get("metadata", {})
                }
                for v in vectors
            ]
            ids = [v["id"] for v in vectors]
            
            await qdrant.insert_vectors(
                collection_name=collection_name,
                vectors=vector_values,
                payloads=payloads,
                ids=ids
            )
            
            print(f"Loaded {len(vectors)} vectors into Qdrant")
            return True
            
    except Exception as e:
        print(f"Error loading Qdrant fixtures: {e}")
        return False


async def load_neo4j_fixtures(config: StorageConfig, nodes_file: str, edges_file: str) -> bool:
    """
    Load graph fixtures into Neo4j.
    
    Args:
        config: Neo4j configuration
        nodes_file: Path to nodes JSON file
        edges_file: Path to edges JSON file
        
    Returns:
        True if successful
    """
    print(f"Loading Neo4j fixtures...")
    
    try:
        # Load nodes data
        with open(nodes_file, 'r') as f:
            nodes_data = json.load(f)
        nodes = nodes_data.get("nodes", [])
        
        # Load edges data
        with open(edges_file, 'r') as f:
            edges_data = json.load(f)
        edges = edges_data.get("edges", [])
        
        # Connect to Neo4j
        async with Neo4jDB(config) as neo4j:
            # Create nodes
            node_id_map = {}
            for node in nodes:
                node_id = await neo4j.create_node(
                    label=node["label"],
                    properties=node["properties"]
                )
                node_id_map[node["id"]] = node_id
            
            print(f"Created {len(nodes)} nodes in Neo4j")
            
            # Create edges
            for edge in edges:
                from_id = node_id_map.get(edge["from"])
                to_id = node_id_map.get(edge["to"])
                
                if from_id and to_id:
                    await neo4j.create_relationship(
                        from_node_id=from_id,
                        to_node_id=to_id,
                        relationship_type=edge["type"],
                        properties=edge.get("properties", {})
                    )
            
            print(f"Created {len(edges)} edges in Neo4j")
            return True
            
    except Exception as e:
        print(f"Error loading Neo4j fixtures: {e}")
        return False


async def load_all_fixtures(
    postgres_config: StorageConfig,
    qdrant_config: StorageConfig,
    neo4j_config: StorageConfig,
    fixtures_dir: str,
) -> bool:
    """
    Load all fixtures for testing.
    
    Args:
        postgres_config: PostgreSQL configuration
        qdrant_config: Qdrant configuration
        neo4j_config: Neo4j configuration
        fixtures_dir: Base fixtures directory
        
    Returns:
        True if all fixtures loaded successfully
    """
    fixtures_path = Path(fixtures_dir)
    
    success = True
    
    # Load PostgreSQL fixtures
    sql_file = fixtures_path / "sql" / "seed.sql"
    if sql_file.exists():
        if not load_postgres_fixtures(postgres_config, str(sql_file)):
            success = False
    else:
        print(f"PostgreSQL fixture file not found: {sql_file}")
    
    # Load Qdrant fixtures
    vector_file = fixtures_path / "vectors" / "json" / "sample_vectors.json"
    if vector_file.exists():
        if not await load_qdrant_fixtures(qdrant_config, str(vector_file)):
            success = False
    else:
        print(f"Qdrant fixture file not found: {vector_file}")
    
    # Load Neo4j fixtures
    nodes_file = fixtures_path / "graphs" / "nodes" / "sample_nodes.json"
    edges_file = fixtures_path / "graphs" / "edges" / "sample_edges.json"
    if nodes_file.exists() and edges_file.exists():
        if not await load_neo4j_fixtures(neo4j_config, str(nodes_file), str(edges_file)):
            success = False
    else:
        print(f"Neo4j fixture files not found: {nodes_file}, {edges_file}")
    
    return success


def main():
    parser = argparse.ArgumentParser(description="Load test fixtures for AI Platform")
    parser.add_argument("--fixtures-dir", type=str, 
                       default="storage/fixtures",
                       help="Path to fixtures directory")
    parser.add_argument("--postgres", action="store_true", help="Load PostgreSQL fixtures")
    parser.add_argument("--qdrant", action="store_true", help="Load Qdrant fixtures")
    parser.add_argument("--neo4j", action="store_true", help="Load Neo4j fixtures")
    parser.add_argument("--all", action="store_true", help="Load all fixtures")
    
    args = parser.parse_args()
    
    # Load configurations from environment
    postgres_config = StorageConfig.from_env(prefix="POSTGRES_")
    qdrant_config = StorageConfig.from_env(prefix="QDRANT_")
    neo4j_config = StorageConfig.from_env(prefix="NEO4J_")
    
    # Default to loading all if no specific backend selected
    if not (args.postgres or args.qdrant or args.neo4j):
        args.all = True
    
    if args.all:
        success = asyncio.run(load_all_fixtures(
            postgres_config, qdrant_config, neo4j_config, args.fixtures_dir
        ))
    else:
        success = True
        if args.postgres:
            sql_file = Path(args.fixtures_dir) / "sql" / "seed.sql"
            success &= load_postgres_fixtures(postgres_config, str(sql_file))
        
        if args.qdrant:
            vector_file = Path(args.fixtures_dir) / "vectors" / "json" / "sample_vectors.json"
            success &= asyncio.run(load_qdrant_fixtures(qdrant_config, str(vector_file)))
        
        if args.neo4j:
            nodes_file = Path(args.fixtures_dir) / "graphs" / "nodes" / "sample_nodes.json"
            edges_file = Path(args.fixtures_dir) / "graphs" / "edges" / "sample_edges.json"
            success &= asyncio.run(load_neo4j_fixtures(neo4j_config, str(nodes_file), str(edges_file)))
    
    if success:
        print("\n✓ All fixtures loaded successfully")
        sys.exit(0)
    else:
        print("\n✗ Some fixtures failed to load")
        sys.exit(1)


if __name__ == "__main__":
    main()