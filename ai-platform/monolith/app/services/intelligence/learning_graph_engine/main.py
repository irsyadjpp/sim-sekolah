"""
Learning Graph Engine - Fase 5.5
Educational Intelligence Layer - Knowledge graph construction and competency mapping
"""
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
ENABLE_GRPC_SERVER = os.getenv("ENABLE_GRPC_SERVER", "false").lower() == "true"
ENABLE_RABBITMQ_CONSUMER = os.getenv("ENABLE_RABBITMQ_CONSUMER", "false").lower() == "true"
GRPC_PORT = int(os.getenv("GRPC_PORT", "50066"))


# Pydantic models
class GraphConstructionRequest(BaseModel):
    """Graph construction request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    graph_type: str  # competency, prerequisite, concept
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    context: Optional[Dict[str, Any]] = None


class GraphConstructionResult(BaseModel):
    """Graph construction result"""
    request_id: str
    graph_id: str
    graph_type: str
    node_count: int
    edge_count: int
    metadata: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class GraphQueryRequest(BaseModel):
    """Graph query request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    graph_id: str
    query_type: str  # path, neighbors, ancestors, descendants
    start_node: Optional[str] = None
    end_node: Optional[str] = None
    depth: int = Field(default=1, ge=1, le=5)


class GraphQueryResult(BaseModel):
    """Graph query result"""
    request_id: str
    graph_id: str
    query_type: str
    results: List[Dict[str, Any]]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Learning graph engine
class LearningGraphEngine:
    """Knowledge graph construction and query engine"""
    
    def __init__(self):
        self.graphs = {}  # In-memory graph storage
        self.graph_counter = 0
        self.neo4j_client = None  # Neo4j client (lazy initialization)
        self.neo4j_enabled = os.getenv("NEO4J_ENABLED", "false").lower() == "true"
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
    
    def _get_neo4j_client(self):
        """Get or create Neo4j client"""
        if self.neo4j_enabled and self.neo4j_client is None:
            try:
                from neo4j import GraphDatabase
                self.neo4j_client = GraphDatabase.driver(
                    self.neo4j_uri,
                    auth=(self.neo4j_user, self.neo4j_password)
                )
                logger.info("Neo4j client initialized successfully")
            except ImportError:
                logger.warning("Neo4j driver not installed, using in-memory storage only")
                self.neo4j_enabled = False
            except Exception as e:
                logger.error(f"Failed to initialize Neo4j client: {e}")
                self.neo4j_enabled = False
        
        return self.neo4j_client
    
    def construct_graph_with_neo4j(self, request: GraphConstructionRequest) -> Dict:
        """Construct knowledge graph with Neo4j backend"""
        if not self.neo4j_enabled:
            # Fallback to in-memory storage
            return self.construct_graph(request)
        
        client = self._get_neo4j_client()
        if not client:
            return self.construct_graph(request)
        
        graph_id = f"graph_{self.graph_counter}"
        self.graph_counter += 1
        
        try:
            with client.session() as session:
                # Create nodes
                for node in request.nodes:
                    session.run(
                        "CREATE (n:Node $props)",
                        props={"id": node.get("id"), **node}
                    )
                
                # Create edges
                for edge in request.edges:
                    session.run(
                        """
                        MATCH (source:Node {id: $source_id})
                        MATCH (target:Node {id: $target_id})
                        CREATE (source)-[r:CONNECTED $props]->(target)
                        """,
                        source_id=edge.get("source"),
                        target_id=edge.get("target"),
                        props=edge
                    )
                
                # Store metadata
                self.graphs[graph_id] = {
                    "id": graph_id,
                    "type": request.graph_type,
                    "nodes": request.nodes,
                    "edges": request.edges,
                    "metadata": {
                        "node_count": len(request.nodes),
                        "edge_count": len(request.edges),
                        "created_at": datetime.utcnow().isoformat(),
                        "backend": "neo4j"
                    }
                }
                
                return {
                    "graph_id": graph_id,
                    "node_count": len(request.nodes),
                    "edge_count": len(request.edges),
                    "metadata": self.graphs[graph_id]["metadata"],
                    "backend": "neo4j"
                }
        except Exception as e:
            logger.error(f"Neo4j graph construction failed: {e}")
            # Fallback to in-memory
            return self.construct_graph(request)
    
    def visualize_graph(self, graph_id: str) -> Dict:
        """Generate graph visualization data"""
        graph = self.graphs.get(graph_id)
        
        if not graph:
            raise HTTPException(status_code=404, detail="Graph not found")
        
        # Generate visualization data in format suitable for frontend libraries
        visualization_data = {
            "nodes": [
                {
                    "id": node.get("id"),
                    "label": node.get("label", node.get("id")),
                    "data": node
                }
                for node in graph["nodes"]
            ],
            "edges": [
                {
                    "source": edge.get("source"),
                    "target": edge.get("target"),
                    "label": edge.get("relation", "connected"),
                    "data": edge
                }
                for edge in graph["edges"]
            ],
            "layout": self._generate_layout_suggestions(graph["nodes"], graph["edges"]),
            "style": self._generate_style_suggestions(graph["type"])
        }
        
        return {
            "graph_id": graph_id,
            "visualization_data": visualization_data,
            "metadata": graph["metadata"]
        }
    
    def _generate_layout_suggestions(self, nodes: List[Dict], edges: List[Dict]) -> Dict:
        """Generate layout suggestions for graph visualization"""
        node_count = len(nodes)
        edge_count = len(edges)
        
        # Determine appropriate layout based on graph characteristics
        if node_count < 10:
            layout_type = "circular"
        elif node_count < 50:
            layout_type = "force_directed"
        elif edge_count > node_count * 2:
            layout_type = "hierarchical"
        else:
            layout_type = "force_directed"
        
        return {
            "type": layout_type,
            "suggestions": {
                "node_size": min(max(5000 // node_count, 200), 800),
                "edge_width": min(max(3000 // edge_count, 1), 5),
                "label_size": max(12, 20 - node_count // 10)
            }
        }
    
    def _generate_style_suggestions(self, graph_type: str) -> Dict:
        """Generate style suggestions based on graph type"""
        style_map = {
            "competency": {
                "color_scheme": "categorical",
                "node_colors": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
                "edge_color": "#7f7f7f"
            },
            "prerequisite": {
                "color_scheme": "sequential",
                "node_colors": ["#ffffcc", "#c2e699", "#78c679", "#31a354", "#006837"],
                "edge_color": "#666666",
                "arrow": True
            },
            "concept": {
                "color_scheme": "diverging",
                "node_colors": ["#e0f3f8", "#abd9e9", "#74add1", "#4575b4", "#313695"],
                "edge_color": "#999999"
            }
        }
        
        return style_map.get(graph_type, style_map["competency"])
    
    def export_graph(self, graph_id: str, format: str = "json") -> Dict:
        """Export graph in specified format"""
        graph = self.graphs.get(graph_id)
        
        if not graph:
            raise HTTPException(status_code=404, detail="Graph not found")
        
        if format == "json":
            return graph
        elif format == "gexf":
            return self._export_gexf(graph)
        elif format == "graphml":
            return self._export_graphml(graph)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")
    
    def _export_gexf(self, graph: Dict) -> Dict:
        """Export graph in GEXF format (simplified)"""
        # Simplified GEXF export
        gexf_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
    <graph mode="static" defaultedgetype="directed">
        <nodes>
            {"".join(f'<node id="{node.get("id")}" label="{node.get("label", node.get("id"))}"/>' for node in graph["nodes"])}
        </nodes>
        <edges>
            {"".join(f'<edge source="{edge.get("source")}" target="{edge.get("target")}" label="{edge.get("relation", "connected")}"/>' for edge in graph["edges"])}
        </edges>
    </graph>
</gexf>"""
        
        return {
            "format": "gexf",
            "data": gexf_data
        }
    
    def _export_graphml(self, graph: Dict) -> Dict:
        """Export graph in GraphML format (simplified)"""
        # Simplified GraphML export
        graphml_data = f"""<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
    <graph id="G" edgedefault="directed">
        {"".join(f'<node id="{node.get("id")}"/>' for node in graph["nodes"])}
        {"".join(f'<edge source="{edge.get("source")}" target="{edge.get("target")}"/>' for edge in graph["edges"])}
    </graph>
</graphml>"""
        
        return {
            "format": "graphml",
            "data": graphml_data
        }
    
    def construct_graph(self, request: GraphConstructionRequest) -> Dict:
        """Construct knowledge graph"""
        self.graph_counter += 1
        graph_id = f"graph_{self.graph_counter}"
        
        # Validate graph structure
        validation = self._validate_graph(request.nodes, request.edges)
        
        if not validation["is_valid"]:
            raise HTTPException(status_code=400, detail=validation["errors"])
        
        # Store graph
        graph = {
            "id": graph_id,
            "type": request.graph_type,
            "nodes": request.nodes,
            "edges": request.edges,
            "metadata": {
                "node_count": len(request.nodes),
                "edge_count": len(request.edges),
                "created_at": datetime.utcnow().isoformat()
            }
        }
        
        self.graphs[graph_id] = graph
        
        return {
            "graph_id": graph_id,
            "node_count": len(request.nodes),
            "edge_count": len(request.edges),
            "metadata": graph["metadata"]
        }
    
    def query_graph(self, request: GraphQueryRequest) -> Dict:
        """Query knowledge graph"""
        graph = self.graphs.get(request.graph_id)
        
        if not graph:
            raise HTTPException(status_code=404, detail="Graph not found")
        
        results = []
        
        if request.query_type == "neighbors":
            results = self._get_neighbors(graph, request.start_node, request.depth)
        elif request.query_type == "path":
            results = self._find_path(graph, request.start_node, request.end_node)
        elif request.query_type == "ancestors":
            results = self._get_ancestors(graph, request.start_node, request.depth)
        elif request.query_type == "descendants":
            results = self._get_descendants(graph, request.start_node, request.depth)
        
        return {
            "results": results
        }
    
    def _validate_graph(self, nodes: List[Dict], edges: List[Dict]) -> Dict:
        """Validate graph structure"""
        errors = []
        
        # Check for duplicate node IDs
        node_ids = [node.get("id") for node in nodes]
        if len(node_ids) != len(set(node_ids)):
            errors.append("Duplicate node IDs found")
        
        # Check edge references
        node_id_set = set(node_ids)
        for edge in edges:
            source = edge.get("source")
            target = edge.get("target")
            
            if source not in node_id_set:
                errors.append(f"Edge references non-existent source node: {source}")
            if target not in node_id_set:
                errors.append(f"Edge references non-existent target node: {target}")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    def _get_neighbors(self, graph: Dict, node_id: str, depth: int) -> List[Dict]:
        """Get neighboring nodes"""
        neighbors = []
        visited = set()
        queue = [(node_id, 0)]
        
        while queue:
            current, current_depth = queue.pop(0)
            
            if current_depth > depth:
                continue
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Find connected nodes
            for edge in graph["edges"]:
                if edge["source"] == current and edge["target"] not in visited:
                    neighbors.append({
                        "node": edge["target"],
                        "relation": edge.get("relation", "connected"),
                        "depth": current_depth + 1
                    })
                    queue.append((edge["target"], current_depth + 1))
        
        return neighbors
    
    def _find_path(self, graph: Dict, start: str, end: str) -> List[Dict]:
        """Find path between nodes"""
        if not start or not end:
            return []
        
        # Simple BFS path finding
        queue = [(start, [start])]
        visited = set()
        
        while queue:
            current, path = queue.pop(0)
            
            if current == end:
                return [{"path": path}]
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for edge in graph["edges"]:
                if edge["source"] == current:
                    queue.append((edge["target"], path + [edge["target"]]))
        
        return []
    
    def _get_ancestors(self, graph: Dict, node_id: str, depth: int) -> List[Dict]:
        """Get ancestor nodes"""
        ancestors = []
        visited = set()
        queue = [(node_id, 0)]
        
        while queue:
            current, current_depth = queue.pop(0)
            
            if current_depth > depth:
                continue
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Find parent nodes (edges where current is target)
            for edge in graph["edges"]:
                if edge["target"] == current and edge["source"] not in visited:
                    ancestors.append({
                        "node": edge["source"],
                        "relation": edge.get("relation", "parent"),
                        "depth": current_depth + 1
                    })
                    queue.append((edge["source"], current_depth + 1))
        
        return ancestors
    
    def _get_descendants(self, graph: Dict, node_id: str, depth: int) -> List[Dict]:
        """Get descendant nodes"""
        descendants = []
        visited = set()
        queue = [(node_id, 0)]
        
        while queue:
            current, current_depth = queue.pop(0)
            
            if current_depth > depth:
                continue
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Find child nodes (edges where current is source)
            for edge in graph["edges"]:
                if edge["source"] == current and edge["target"] not in visited:
                    descendants.append({
                        "node": edge["target"],
                        "relation": edge.get("relation", "child"),
                        "depth": current_depth + 1
                    })
                    queue.append((edge["target"], current_depth + 1))
        
        return descendants


# Initialize learning graph engine
graph_engine = LearningGraphEngine()


# FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    # Import and start gRPC server if enabled
    if ENABLE_GRPC_SERVER:
        from .grpc_server import serve
        import asyncio
        asyncio.create_task(serve(GRPC_PORT))
    
    # Import and start RabbitMQ consumer if enabled
    if ENABLE_RABBITMQ_CONSUMER:
        from .consumer import AsyncLearningGraphEngineConsumer
        consumer = AsyncLearningGraphEngineConsumer()
        import asyncio
        asyncio.create_task(consumer.start())
    
    yield


app = FastAPI(
    title="Learning Graph Engine",
    description="Educational Intelligence Layer - Knowledge graph construction and competency mapping",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "service": "learning-graph-engine",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Graph endpoints
@app.post("/graph/construct")
async def construct_graph(request: GraphConstructionRequest):
    """Construct knowledge graph"""
    result = graph_engine.construct_graph(request)
    return GraphConstructionResult(
        request_id=request.request_id,
        graph_id=result["graph_id"],
        graph_type=request.graph_type,
        node_count=result["node_count"],
        edge_count=result["edge_count"],
        metadata=result["metadata"]
    )


@app.post("/graph/query")
async def query_graph(request: GraphQueryRequest):
    """Query knowledge graph"""
    result = graph_engine.query_graph(request)
    return GraphQueryResult(
        request_id=request.request_id,
        graph_id=request.graph_id,
        query_type=request.query_type,
        results=result["results"]
    )


@app.get("/graph/{graph_id}")
async def get_graph(graph_id: str):
    """Get graph by ID"""
    graph = graph_engine.graphs.get(graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="Graph not found")
    return graph


@app.get("/graphs")
async def list_graphs():
    """List all graphs"""
    return {
        "graphs": list(graph_engine.graphs.keys()),
        "count": len(graph_engine.graphs)
    }


# Neo4j integration endpoints
@app.post("/graph/construct-neo4j")
async def construct_graph_neo4j(request: GraphConstructionRequest):
    """Construct knowledge graph with Neo4j backend"""
    result = graph_engine.construct_graph_with_neo4j(request)
    return GraphConstructionResult(
        request_id=request.request_id,
        graph_id=result["graph_id"],
        graph_type=request.graph_type,
        node_count=result["node_count"],
        edge_count=result["edge_count"],
        metadata=result["metadata"]
    )


# Visualization endpoints
@app.get("/graph/{graph_id}/visualize")
async def visualize_graph(graph_id: str):
    """Generate graph visualization data"""
    result = graph_engine.visualize_graph(graph_id)
    return result


# Export endpoints
@app.get("/graph/{graph_id}/export")
async def export_graph(graph_id: str, format: str = "json"):
    """Export graph in specified format"""
    result = graph_engine.export_graph(graph_id, format)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8017)
