"""
Graph database abstraction (Neo4j)
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from .base import StorageBackend, StorageConfig


class GraphDB(StorageBackend):
    """
    Abstract graph database backend.
    
    Provides unified interface for graph operations and queries.
    """
    
    @abstractmethod
    async def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query.
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            
        Returns:
            Query results as list of dictionaries
        """
        pass
    
    @abstractmethod
    async def create_node(
        self,
        label: str,
        properties: Dict[str, Any],
    ) -> str:
        """
        Create a node in the graph.
        
        Args:
            label: Node label
            properties: Node properties
            
        Returns:
            Node ID
        """
        pass
    
    @abstractmethod
    async def create_relationship(
        self,
        from_node_id: str,
        to_node_id: str,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create a relationship between nodes.
        
        Args:
            from_node_id: Source node ID
            to_node_id: Target node ID
            relationship_type: Relationship type
            properties: Relationship properties
            
        Returns:
            Relationship ID
        """
        pass
    
    @abstractmethod
    async def get_node(
        self,
        node_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a node by ID.
        
        Args:
            node_id: Node ID
            
        Returns:
            Node data or None if not found
        """
        pass
    
    @abstractmethod
    async def get_relationship(
        self,
        relationship_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a relationship by ID.
        
        Args:
            relationship_id: Relationship ID
            
        Returns:
            Relationship data or None if not found
        """
        pass
    
    @abstractmethod
    async def update_node(
        self,
        node_id: str,
        properties: Dict[str, Any],
    ) -> bool:
        """
        Update node properties.
        
        Args:
            node_id: Node ID
            properties: Properties to update
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def update_relationship(
        self,
        relationship_id: str,
        properties: Dict[str, Any],
    ) -> bool:
        """
        Update relationship properties.
        
        Args:
            relationship_id: Relationship ID
            properties: Properties to update
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def delete_node(self, node_id: str) -> bool:
        """
        Delete a node by ID.
        
        Args:
            node_id: Node ID
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def delete_relationship(self, relationship_id: str) -> bool:
        """
        Delete a relationship by ID.
        
        Args:
            relationship_id: Relationship ID
            
        Returns:
            True if successful
        """
        pass
    
    @abstractmethod
    async def find_nodes(
        self,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Find nodes matching criteria.
        
        Args:
            label: Node label filter
            properties: Property filters
            limit: Maximum number of results
            
        Returns:
            List of matching nodes
        """
        pass
    
    @abstractmethod
    async def find_relationships(
        self,
        relationship_type: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Find relationships matching criteria.
        
        Args:
            relationship_type: Relationship type filter
            properties: Property filters
            limit: Maximum number of results
            
        Returns:
            List of matching relationships
        """
        pass
    
    @abstractmethod
    async def get_neighbors(
        self,
        node_id: str,
        relationship_type: Optional[str] = None,
        direction: str = "outgoing",
    ) -> List[Dict[str, Any]]:
        """
        Get neighboring nodes.
        
        Args:
            node_id: Node ID
            relationship_type: Filter by relationship type
            direction: "incoming", "outgoing", or "both"
            
        Returns:
            List of neighboring nodes with relationship info
        """
        pass
    
    @abstractmethod
    async def get_path(
        self,
        from_node_id: str,
        to_node_id: str,
        relationship_types: Optional[List[str]] = None,
        max_depth: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Find path between two nodes.
        
        Args:
            from_node_id: Source node ID
            to_node_id: Target node ID
            relationship_types: Filter by relationship types
            max_depth: Maximum path length
            
        Returns:
            List of nodes and relationships in the path
        """
        pass


class Neo4jDB(GraphDB):
    """
    Neo4j graph database implementation.
    
    Provides graph database operations using Neo4j driver.
    """
    
    def __init__(self, config: StorageConfig):
        """
        Initialize Neo4j backend.
        
        Args:
            config: Storage configuration
        """
        super().__init__(config)
        self._driver = None
    
    async def connect(self) -> None:
        """Establish Neo4j connection."""
        from neo4j import GraphDatabase
        
        uri = f"{'neo4j+s' if self.config.use_ssl else 'neo4j'}://{self.config.host}:{self.config.port}"
        
        self._driver = GraphDatabase.driver(
            uri,
            auth=(self.config.username, self.config.password),
            max_connection_pool_size=self.config.pool_size,
            connection_acquisition_timeout=self.config.pool_timeout
        )
        
        # Verify connection
        self._driver.verify_connectivity()
        self._is_connected = True
    
    async def disconnect(self) -> None:
        """Close Neo4j connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
        self._is_connected = False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Neo4j health."""
        try:
            result = await self.execute_query("RETURN 1 as status")
            if result:
                return {
                    "status": "healthy",
                    "backend": "neo4j",
                    "details": {
                        "endpoint": f"{self.config.host}:{self.config.port}",
                        "database": self.config.database or "neo4j"
                    }
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": "neo4j",
                "error": str(e)
            }
    
    async def ping(self) -> bool:
        """Ping Neo4j backend."""
        try:
            result = await self.execute_query("RETURN 1 as status")
            return len(result) > 0
        except:
            return False
    
    async def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Execute Cypher query."""
        parameters = parameters or {}
        
        with self._driver.session(database=self.config.database) as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]
    
    async def create_node(
        self,
        label: str,
        properties: Dict[str, Any],
    ) -> str:
        """Create node in Neo4j."""
        query = f"""
        CREATE (n:{label} $properties)
        RETURN elementId(n) as id
        """
        
        result = await self.execute_query(query, {"properties": properties})
        return result[0]["id"]
    
    async def create_relationship(
        self,
        from_node_id: str,
        to_node_id: str,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create relationship in Neo4j."""
        properties = properties or {}
        
        query = f"""
        MATCH (a), (b)
        WHERE elementId(a) = $from_id AND elementId(b) = $to_id
        CREATE (a)-[r:{relationship_type} $properties]->(b)
        RETURN elementId(r) as id
        """
        
        result = await self.execute_query(
            query,
            {
                "from_id": from_node_id,
                "to_id": to_node_id,
                "properties": properties
            }
        )
        return result[0]["id"]
    
    async def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve node from Neo4j."""
        query = """
        MATCH (n)
        WHERE elementId(n) = $node_id
        RETURN n
        """
        
        result = await self.execute_query(query, {"node_id": node_id})
        if result:
            node = result[0]["n"]
            return {
                "id": node.element_id,
                "labels": list(node.labels),
                "properties": dict(node)
            }
        return None
    
    async def get_relationship(self, relationship_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve relationship from Neo4j."""
        query = """
        MATCH ()-[r]->()
        WHERE elementId(r) = $relationship_id
        RETURN r
        """
        
        result = await self.execute_query(query, {"relationship_id": relationship_id})
        if result:
            rel = result[0]["r"]
            return {
                "id": rel.element_id,
                "type": rel.type,
                "properties": dict(rel),
                "start_node": rel.start_node.element_id,
                "end_node": rel.end_node.element_id
            }
        return None
    
    async def update_node(
        self,
        node_id: str,
        properties: Dict[str, Any],
    ) -> bool:
        """Update node in Neo4j."""
        query = """
        MATCH (n)
        WHERE elementId(n) = $node_id
        SET n += $properties
        RETURN elementId(n) as id
        """
        
        result = await self.execute_query(
            query,
            {"node_id": node_id, "properties": properties}
        )
        return len(result) > 0
    
    async def update_relationship(
        self,
        relationship_id: str,
        properties: Dict[str, Any],
    ) -> bool:
        """Update relationship in Neo4j."""
        query = """
        MATCH ()-[r]->()
        WHERE elementId(r) = $relationship_id
        SET r += $properties
        RETURN elementId(r) as id
        """
        
        result = await self.execute_query(
            query,
            {"relationship_id": relationship_id, "properties": properties}
        )
        return len(result) > 0
    
    async def delete_node(self, node_id: str) -> bool:
        """Delete node from Neo4j."""
        query = """
        MATCH (n)
        WHERE elementId(n) = $node_id
        DETACH DELETE n
        """
        
        await self.execute_query(query, {"node_id": node_id})
        return True
    
    async def delete_relationship(self, relationship_id: str) -> bool:
        """Delete relationship from Neo4j."""
        query = """
        MATCH ()-[r]->()
        WHERE elementId(r) = $relationship_id
        DELETE r
        """
        
        await self.execute_query(query, {"relationship_id": relationship_id})
        return True
    
    async def find_nodes(
        self,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Find nodes in Neo4j."""
        label_part = f":{label}" if label else ""
        properties_part = ""
        params = {"limit": limit}
        
        if properties:
            property_conditions = []
            for key, value in properties.items():
                param_key = f"prop_{key}"
                property_conditions.append(f"n.{key} = ${param_key}")
                params[param_key] = value
            properties_part = " AND " + " AND ".join(property_conditions)
        
        query = f"""
        MATCH (n{label_part})
        WHERE true {properties_part}
        RETURN n
        LIMIT $limit
        """
        
        result = await self.execute_query(query, params)
        return [
            {
                "id": node["n"].element_id,
                "labels": list(node["n"].labels),
                "properties": dict(node["n"])
            }
            for node in result
        ]
    
    async def find_relationships(
        self,
        relationship_type: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Find relationships in Neo4j."""
        type_part = f":{relationship_type}" if relationship_type else ""
        properties_part = ""
        params = {"limit": limit}
        
        if properties:
            property_conditions = []
            for key, value in properties.items():
                param_key = f"prop_{key}"
                property_conditions.append(f"r.{key} = ${param_key}")
                params[param_key] = value
            properties_part = " AND " + " AND ".join(property_conditions)
        
        query = f"""
        MATCH ()-[r{type_part}]->()
        WHERE true {properties_part}
        RETURN r
        LIMIT $limit
        """
        
        result = await self.execute_query(query, params)
        return [
            {
                "id": rel["r"].element_id,
                "type": rel["r"].type,
                "properties": dict(rel["r"]),
                "start_node": rel["r"].start_node.element_id,
                "end_node": rel["r"].end_node.element_id
            }
            for rel in result
        ]
    
    async def get_neighbors(
        self,
        node_id: str,
        relationship_type: Optional[str] = None,
        direction: str = "outgoing",
    ) -> List[Dict[str, Any]]:
        """Get neighboring nodes in Neo4j."""
        if direction == "incoming":
            arrow = "<-"
        elif direction == "outgoing":
            arrow = "-"
        else:
            arrow = "-"
        
        type_part = f":{relationship_type}" if relationship_type else ""
        
        query = f"""
        MATCH (a)-[r{type_part}]{arrow}(b)
        WHERE elementId(a) = $node_id
        RETURN b, r
        """
        
        result = await self.execute_query(query, {"node_id": node_id})
        return [
            {
                "node": {
                    "id": item["b"].element_id,
                    "labels": list(item["b"].labels),
                    "properties": dict(item["b"])
                },
                "relationship": {
                    "id": item["r"].element_id,
                    "type": item["r"].type,
                    "properties": dict(item["r"])
                }
            }
            for item in result
        ]
    
    async def get_path(
        self,
        from_node_id: str,
        to_node_id: str,
        relationship_types: Optional[List[str]] = None,
        max_depth: int = 5,
    ) -> List[Dict[str, Any]]:
        """Find path between nodes in Neo4j."""
        type_part = "|".join(relationship_types) if relationship_types else ""
        
        query = f"""
        MATCH path = shortestPath((a)-[:{type_part}*1..{max_depth}]->(b))
        WHERE elementId(a) = $from_id AND elementId(b) = $to_id
        RETURN [node in nodes(path) | {{
            id: elementId(node),
            labels: labels(node),
            properties: properties(node)
        }}] as nodes,
        [rel in relationships(path) | {{
            id: elementId(rel),
            type: type(rel),
            properties: properties(rel)
        }}] as relationships
        """
        
        result = await self.execute_query(
            query,
            {
                "from_id": from_node_id,
                "to_id": to_node_id
            }
        )
        
        if result:
            return {
                "nodes": result[0]["nodes"],
                "relationships": result[0]["relationships"]
            }
        return []