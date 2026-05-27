"""
Enrichment Pipeline - Metadata Tagging
Tags documents with educational metadata: difficulty, taxonomy, competency
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Document:
    """Document to be enriched"""
    id: str
    content: str
    source: str
    metadata: Dict[str, Any]


@dataclass
class EnrichedDocument:
    """Document with enriched metadata"""
    id: str
    content: str
    source: str
    base_metadata: Dict[str, Any]
    enriched_metadata: Dict[str, Any]
    tags: List[str]
    difficulty: str
    taxonomies: List[str]
    competencies: List[str]
    processed_at: datetime


class MetadataTagger:
    """Tags documents with educational metadata"""
    
    def __init__(self):
        self.difficulty_keywords = {
            "easy": ["basic", "introduction", "fundamental", "simple", "beginner"],
            "medium": ["intermediate", "practice", "apply", "develop", "build"],
            "hard": ["advanced", "complex", "analyze", "evaluate", "create", "synthesize"]
        }
        
        self.taxonomy_keywords = {
            "mathematics": ["number", "algebra", "geometry", "measurement", "statistics"],
            "science": ["biology", "physics", "chemistry", "earth", "space"],
            "language": ["reading", "writing", "grammar", "vocabulary", "literature"],
            "social": ["history", "geography", "civics", "culture", "society"]
        }
    
    def tag_document(self, document: Document) -> EnrichedDocument:
        """Tag a single document with metadata"""
        content_lower = document.content.lower()
        
        # Determine difficulty
        difficulty = self._determine_difficulty(content_lower)
        
        # Determine taxonomies
        taxonomies = self._determine_taxonomies(content_lower)
        
        # Extract competencies (simplified)
        competencies = self._extract_competencies(content_lower)
        
        # Generate tags
        tags = self._generate_tags(difficulty, taxonomies, competencies)
        
        # Build enriched metadata
        enriched_metadata = {
            **document.metadata,
            "difficulty": difficulty,
            "taxonomies": taxonomies,
            "competencies": competencies,
            "tags": tags,
            "enriched_at": datetime.utcnow().isoformat()
        }
        
        return EnrichedDocument(
            id=document.id,
            content=document.content,
            source=document.source,
            base_metadata=document.metadata,
            enriched_metadata=enriched_metadata,
            tags=tags,
            difficulty=difficulty,
            taxonomies=taxonomies,
            competencies=competencies,
            processed_at=datetime.utcnow()
        )
    
    def tag_batch(self, documents: List[Document]) -> List[EnrichedDocument]:
        """Tag multiple documents"""
        enriched = []
        for doc in documents:
            try:
                enriched_doc = self.tag_document(doc)
                enriched.append(enriched_doc)
                logger.info(f"Tagged document: {doc.id}")
            except Exception as e:
                logger.error(f"Error tagging document {doc.id}: {e}")
        
        return enriched
    
    def _determine_difficulty(self, content: str) -> str:
        """Determine document difficulty"""
        scores = {
            "easy": sum(1 for kw in self.difficulty_keywords["easy"] if kw in content),
            "medium": sum(1 for kw in self.difficulty_keywords["medium"] if kw in content),
            "hard": sum(1 for kw in self.difficulty_keywords["hard"] if kw in content)
        }
        
        return max(scores, key=scores.get)
    
    def _determine_taxonomies(self, content: str) -> List[str]:
        """Determine document taxonomies"""
        taxonomies = []
        for taxonomy, keywords in self.taxonomy_keywords.items():
            if any(kw in content for kw in keywords):
                taxonomies.append(taxonomy)
        return taxonomies
    
    def _extract_competencies(self, content: str) -> List[str]:
        """Extract competencies from content"""
        # Simplified competency extraction
        # In production, use NLP models or knowledge graph
        competencies = []
        
        # Look for competency indicators
        if "understand" in content or "explain" in content:
            competencies.append("understanding")
        if "apply" in content or "use" in content:
            competencies.append("application")
        if "analyze" in content or "examine" in content:
            competencies.append("analysis")
        if "create" in content or "design" in content:
            competencies.append("creation")
        
        return competencies
    
    def _generate_tags(self, difficulty: str, taxonomies: List[str], competencies: List[str]) -> List[str]:
        """Generate tags from metadata"""
        tags = [difficulty]
        tags.extend(taxonomies)
        tags.extend(competencies)
        return tags


class EnrichmentPipeline:
    """Pipeline for enriching documents with metadata"""
    
    def __init__(self):
        self.tagger = MetadataTagger()
        self.processed_count = 0
        self.failed_count = 0
    
    def run(self, documents: List[Document]) -> List[EnrichedDocument]:
        """Run enrichment pipeline"""
        logger.info(f"Starting enrichment pipeline for {len(documents)} documents")
        
        enriched = self.tagger.tag_batch(documents)
        
        self.processed_count = len(enriched)
        self.failed_count = len(documents) - len(enriched)
        
        logger.info(f"Enrichment pipeline complete: {self.processed_count} processed, {self.failed_count} failed")
        
        return enriched
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics"""
        return {
            "processed": self.processed_count,
            "failed": self.failed_count,
            "success_rate": self.processed_count / max(self.processed_count + self.failed_count, 1)
        }


# Example usage
if __name__ == "__main__":
    # Example documents
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
    
    pipeline = EnrichmentPipeline()
    enriched = pipeline.run(documents)
    
    for doc in enriched:
        print(f"Document: {doc.id}")
        print(f"Difficulty: {doc.difficulty}")
        print(f"Taxonomies: {doc.taxonomies}")
        print(f"Competencies: {doc.competencies}")
        print(f"Tags: {doc.tags}")
        print("---")
    
    print(f"Pipeline stats: {pipeline.get_stats()}")
