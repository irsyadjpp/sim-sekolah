"""
Knowledge Ingestion Pipeline
Loads knowledge/ data into vector store and knowledge graph
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import json
import os
from pathlib import Path
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class KnowledgeAsset:
    """Knowledge asset to be ingested"""
    id: str
    type: str  # cp, atp, buku_guru, buku_siswa, modul_ajar, asesmen, p5, media
    path: str
    metadata: Dict[str, Any]


@dataclass
class IngestionResult:
    """Result of knowledge ingestion"""
    asset_id: str
    success: bool
    vector_ids: List[str]
    graph_edge_ids: List[str]
    error: Optional[str] = None


class KnowledgeLoader:
    """Loads knowledge assets from filesystem"""
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.asset_types = ["cp", "atp", "buku_guru", "buku_siswa", "modul_ajar", "asesmen", "p5", "media"]
    
    def discover_assets(self) -> List[KnowledgeAsset]:
        """Discover all knowledge assets"""
        assets = []
        
        for asset_type in self.asset_types:
            type_path = self.knowledge_base_path / asset_type
            if type_path.exists():
                for file_path in type_path.glob("**/*"):
                    if file_path.is_file() and file_path.suffix in [".json", ".md", ".txt", ".csv"]:
                        asset = KnowledgeAsset(
                            id=f"{asset_type}_{file_path.stem}",
                            type=asset_type,
                            path=str(file_path),
                            metadata={
                                "file_name": file_path.name,
                                "file_size": file_path.stat().st_size,
                                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                            }
                        )
                        assets.append(asset)
        
        logger.info(f"Discovered {len(assets)} knowledge assets")
        return assets
    
    def load_asset(self, asset: KnowledgeAsset) -> Dict[str, Any]:
        """Load asset content"""
        file_path = Path(asset.path)
        
        if file_path.suffix == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)
        elif file_path.suffix in [".md", ".txt"]:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        elif file_path.suffix == ".csv":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = None
        
        return {
            "id": asset.id,
            "type": asset.type,
            "content": content,
            "metadata": asset.metadata
        }


class KnowledgeIngestionPipeline:
    """Pipeline for ingesting knowledge assets into vector store and knowledge graph"""
    
    def __init__(self, knowledge_base_path: str):
        self.loader = KnowledgeLoader(knowledge_base_path)
        self.ingested_count = 0
        self.failed_count = 0
    
    def run(self) -> List[IngestionResult]:
        """Run ingestion pipeline"""
        logger.info("Starting knowledge ingestion pipeline")
        
        # Discover assets
        assets = self.loader.discover_assets()
        
        results = []
        for asset in assets:
            try:
                result = self._ingest_asset(asset)
                results.append(result)
                self.ingested_count += 1
                logger.info(f"Ingested asset: {asset.id}")
            except Exception as e:
                logger.error(f"Failed to ingest asset {asset.id}: {e}")
                results.append(IngestionResult(
                    asset_id=asset.id,
                    success=False,
                    vector_ids=[],
                    graph_edge_ids=[],
                    error=str(e)
                ))
                self.failed_count += 1
        
        logger.info(f"Ingestion complete: {self.ingested_count} ingested, {self.failed_count} failed")
        
        return results
    
    def _ingest_asset(self, asset: KnowledgeAsset) -> IngestionResult:
        """Ingest a single asset"""
        # Load asset content
        loaded = self.loader.load_asset(asset)
        
        # Index into vector store (simplified)
        vector_ids = self._index_to_vector_store(loaded)
        
        # Create graph edges (simplified)
        graph_edge_ids = self._create_graph_edges(loaded)
        
        return IngestionResult(
            asset_id=asset.id,
            success=True,
            vector_ids=vector_ids,
            graph_edge_ids=graph_edge_ids
        )
    
    def _index_to_vector_store(self, loaded: Dict[str, Any]) -> List[str]:
        """Index content to vector store"""
        # Simplified - in production use actual vector store
        vector_id = f"vec_{loaded['id']}"
        logger.info(f"Indexed {loaded['id']} to vector store as {vector_id}")
        return [vector_id]
    
    def _create_graph_edges(self, loaded: Dict[str, Any]) -> List[str]:
        """Create graph edges for knowledge graph"""
        # Simplified - in production use actual graph database
        edge_id = f"edge_{loaded['id']}"
        logger.info(f"Created graph edge {edge_id} for {loaded['id']}")
        return [edge_id]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        return {
            "ingested": self.ingested_count,
            "failed": self.failed_count,
            "success_rate": self.ingested_count / max(self.ingested_count + self.failed_count, 1)
        }


# Example usage
if __name__ == "__main__":
    # Example usage with knowledge base path
    knowledge_path = "/home/upt-sdi-bonerate-no-85-kepulauan/Development/sim-sekolah/ai-platform/knowledge"
    
    pipeline = KnowledgeIngestionPipeline(knowledge_path)
    results = pipeline.run()
    
    print(f"Ingestion Results:")
    for result in results:
        status = "SUCCESS" if result.success else "FAILED"
        print(f"  {result.asset_id}: {status}")
        if result.success:
            print(f"    Vector IDs: {result.vector_ids}")
            print(f"    Graph Edge IDs: {result.graph_edge_ids}")
    
    print(f"\nPipeline stats: {pipeline.get_stats()}")
