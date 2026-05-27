"""
Enrichment DAG for metadata tagging

This pipeline handles automatic metadata enrichment for documents including:
- Difficulty assessment (easy, medium, hard)
- Taxonomy classification (subject, topic, grade level)
- Competency mapping (educational standards alignment)
"""

from prefect import task, flow, get_run_logger
from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime

from shared.observability import get_tracer, trace_function
from shared.logging import get_logger

logger = get_logger(__name__)


@task(name="analyze_difficulty")
async def analyze_difficulty(
    document_id: str,
    content: str,
    metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze document difficulty level.
    
    Args:
        document_id: Document identifier
        content: Document content text
        metadata: Existing document metadata
        
    Returns:
        Difficulty analysis result
    """
    logger = get_run_logger()
    tracer = get_tracer("enrichment")
    
    with tracer.span("analyze_difficulty", kind="internal"):
        logger.info(f"Analyzing difficulty for document {document_id}")
        
        # Extract text features for difficulty analysis
        text_features = _extract_text_features(content)
        
        # Analyze vocabulary complexity
        vocabulary_score = _analyze_vocabulary_complexity(content)
        
        # Analyze sentence structure
        structure_score = _analyze_sentence_structure(content)
        
        # Analyze concept density
        concept_density = _analyze_concept_density(content)
        
        # Determine difficulty level
        difficulty_level = _determine_difficulty_level(
            vocabulary_score,
            structure_score,
            concept_density
        )
        
        result = {
            "document_id": document_id,
            "difficulty": difficulty_level,
            "vocabulary_score": vocabulary_score,
            "structure_score": structure_score,
            "concept_density": concept_density,
            "analyzed_at": datetime.utcnow().isoformat(),
            "confidence": _calculate_confidence(
                vocabulary_score,
                structure_score,
                concept_density
            )
        }
        
        logger.info(f"Difficulty analysis completed: {difficulty_level}")
        return result


@task(name="classify_taxonomy")
async def classify_taxonomy(
    document_id: str,
    content: str,
    metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Classify document taxonomy (subject, topic, grade level).
    
    Args:
        document_id: Document identifier
        content: Document content text
        metadata: Existing document metadata
        
    Returns:
        Taxonomy classification result
    """
    logger = get_run_logger()
    tracer = get_tracer("enrichment")
    
    with tracer.span("classify_taxonomy", kind="internal"):
        logger.info(f"Classifying taxonomy for document {document_id}")
        
        # Extract subject keywords
        subject_keywords = _extract_subject_keywords(content)
        
        # Classify subject
        subject = _classify_subject(subject_keywords, metadata)
        
        # Extract topic
        topic = _extract_topic(content, subject)
        
        # Determine grade level
        grade_level = _determine_grade_level(content, metadata)
        
        # Extract subtopics
        subtopics = _extract_subtopics(content, subject)
        
        # Get taxonomy path
        taxonomy_path = _build_taxonomy_path(subject, topic, grade_level)
        
        result = {
            "document_id": document_id,
            "subject": subject,
            "topic": topic,
            "subtopics": subtopics,
            "grade_level": grade_level,
            "taxonomy_path": taxonomy_path,
            "subject_confidence": _calculate_subject_confidence(subject_keywords),
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Taxonomy classification completed: {taxonomy_path}")
        return result


@task(name="map_competencies")
async def map_competencies(
    document_id: str,
    content: str,
    taxonomy_result: Dict[str, Any],
    metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Map document content to educational competencies.
    
    Args:
        document_id: Document identifier
        content: Document content text
        taxonomy_result: Result from taxonomy classification
        metadata: Existing document metadata
        
    Returns:
        Competency mapping result
    """
    logger = get_run_logger()
    tracer = get_tracer("enrichment")
    
    with tracer.span("map_competencies", kind="internal"):
        logger.info(f"Mapping competencies for document {document_id}")
        
        # Get educational standards
        standards = _load_educational_standards()
        
        # Extract skill tags
        skill_tags = _extract_skill_tags(content, taxonomy_result)
        
        # Map to competencies
        mapped_competencies = _map_to_competencies(
            skill_tags,
            taxonomy_result,
            standards
        )
        
        # Determine competency levels
        competency_levels = _determine_competency_levels(
            mapped_competencies,
            taxonomy_result["grade_level"]
        )
        
        # Calculate alignment scores
        alignment_scores = _calculate_alignment_scores(
            mapped_competencies,
            standards
        )
        
        result = {
            "document_id": document_id,
            "competencies": mapped_competencies,
            "competency_levels": competency_levels,
            "alignment_scores": alignment_scores,
            "standards_aligned": _get_aligned_standards(mapped_competencies),
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Competency mapping completed: {len(mapped_competencies)} competencies")
        return result


@task(name="update_document_metadata")
async def update_document_metadata(
    document_id: str,
    enrichment_results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update document with enriched metadata.
    
    Args:
        document_id: Document identifier
        enrichment_results: Combined enrichment results
        
    Returns:
        Update result
    """
    logger = get_run_logger()
    tracer = get_tracer("enrichment")
    
    with tracer.span("update_document_metadata", kind="internal"):
        logger.info(f"Updating metadata for document {document_id}")
        
        # Combine all enrichment results
        enriched_metadata = {
            "difficulty": enrichment_results.get("difficulty"),
            "vocabulary_score": enrichment_results.get("vocabulary_score"),
            "structure_score": enrichment_results.get("structure_score"),
            "subject": enrichment_results.get("subject"),
            "topic": enrichment_results.get("topic"),
            "subtopics": enrichment_results.get("subtopics"),
            "grade_level": enrichment_results.get("grade_level"),
            "taxonomy_path": enrichment_results.get("taxonomy_path"),
            "competencies": enrichment_results.get("competencies"),
            "competency_levels": enrichment_results.get("competency_levels"),
            "alignment_scores": enrichment_results.get("alignment_scores"),
            "enriched_at": datetime.utcnow().isoformat()
        }
        
        # Update in database (placeholder for actual implementation)
        # In production, this would call the document service
        update_result = await _update_document_in_db(document_id, enriched_metadata)
        
        result = {
            "document_id": document_id,
            "status": "enriched",
            "metadata": enriched_metadata,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Document metadata updated successfully")
        return result


@flow(name="enrichment_pipeline")
async def enrichment_pipeline(
    document_id: str,
    content: str,
    metadata: Dict[str, Any],
    skip_difficulty: bool = False,
    skip_taxonomy: bool = False,
    skip_competencies: bool = False
) -> Dict[str, Any]:
    """
    Complete enrichment pipeline for document metadata.
    
    Args:
        document_id: Document identifier
        content: Document content text
        metadata: Existing document metadata
        skip_difficulty: Skip difficulty analysis
        skip_taxonomy: Skip taxonomy classification
        skip_competencies: Skip competency mapping
        
    Returns:
        Combined enrichment results
    """
    logger = get_run_logger()
    logger.info(f"Starting enrichment pipeline for document {document_id}")
    
    enrichment_results = {}
    
    # Analyze difficulty
    if not skip_difficulty:
        difficulty_result = await analyze_difficulty(
            document_id=document_id,
            content=content,
            metadata=metadata
        )
        enrichment_results.update(difficulty_result)
    else:
        logger.info("Skipping difficulty analysis")
    
    # Classify taxonomy
    if not skip_taxonomy:
        taxonomy_result = await classify_taxonomy(
            document_id=document_id,
            content=content,
            metadata=metadata
        )
        enrichment_results.update(taxonomy_result)
    else:
        logger.info("Skipping taxonomy classification")
    
    # Map competencies
    if not skip_competencies:
        competency_result = await map_competencies(
            document_id=document_id,
            content=content,
            taxonomy_result=taxonomy_result,
            metadata=metadata
        )
        enrichment_results.update(competency_result)
    else:
        logger.info("Skipping competency mapping")
    
    # Update document metadata
    update_result = await update_document_metadata(
        document_id=document_id,
        enrichment_results=enrichment_results
    )
    
    logger.info(f"Enrichment pipeline completed for document {document_id}")
    return {
        "document_id": document_id,
        "enrichment_results": enrichment_results,
        "update_result": update_result,
        "pipeline_status": "completed"
    }


# Helper functions
def _extract_text_features(content: str) -> Dict[str, Any]:
    """Extract text features for analysis."""
    words = content.split()
    sentences = [s.strip() for s in content.split('.') if s.strip()]
    
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
        "avg_sentence_length": sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    }


def _analyze_vocabulary_complexity(content: str) -> float:
    """Analyze vocabulary complexity (0-1 scale)."""
    import re
    
    words = re.findall(r'\b[a-zA-Z]+\b', content.lower())
    if not words:
        return 0.0
    
    # Simple complexity score based on word length and diversity
    avg_length = sum(len(w) for w in words) / len(words)
    unique_words = len(set(words))
    total_words = len(words)
    
    # Normalize to 0-1 scale
    length_score = min(avg_length / 8.0, 1.0)  # 8 letters is considered complex
    diversity_score = unique_words / total_words if total_words > 0 else 0
    
    return (length_score + diversity_score) / 2


def _analyze_sentence_structure(content: str) -> float:
    """Analyze sentence structure complexity (0-1 scale)."""
    import re
    
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 0.0
    
    # Analyze sentence length variation
    sentence_lengths = [len(s.split()) for s in sentences]
    avg_length = sum(sentence_lengths) / len(sentence_lengths)
    
    # Normalize to 0-1 scale (15 words avg is medium complexity)
    complexity_score = min(avg_length / 20.0, 1.0)
    
    return complexity_score


def _analyze_concept_density(content: str) -> float:
    """Analyze concept density (0-1 scale)."""
    # Simple heuristic: count technical/academic terms
    technical_terms = [
        "algorithm", "function", "variable", "equation", "formula",
        "theory", "concept", "principle", "process", "mechanism"
    ]
    
    words = content.lower().split()
    technical_count = sum(1 for word in words if word in technical_terms)
    density = technical_count / len(words) if words else 0
    
    # Normalize to 0-1 scale (10% technical terms is high density)
    return min(density / 0.1, 1.0)


def _determine_difficulty_level(vocab_score: float, structure_score: float, concept_density: float) -> str:
    """Determine difficulty level from analysis scores."""
    avg_score = (vocab_score + structure_score + concept_density) / 3
    
    if avg_score < 0.3:
        return "easy"
    elif avg_score < 0.6:
        return "medium"
    else:
        return "hard"


def _calculate_confidence(vocab_score: float, structure_score: float, concept_density: float) -> float:
    """Calculate confidence in difficulty classification."""
    scores = [vocab_score, structure_score, concept_density]
    variance = sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)
    
    # Lower variance = higher confidence
    confidence = max(0.0, 1.0 - variance)
    return confidence


def _extract_subject_keywords(content: str) -> Dict[str, int]:
    """Extract subject-specific keywords from content."""
    subject_keywords = {
        "mathematics": ["number", "equation", "formula", "calculate", "algebra", "geometry"],
        "science": ["experiment", "hypothesis", "observation", "biology", "chemistry", "physics"],
        "history": ["war", "revolution", "century", "ancient", "modern", "timeline"],
        "language": ["grammar", "vocabulary", "literature", "poem", "novel", "essay"],
        "geography": ["country", "capital", "border", "climate", "population", "region"]
    }
    
    content_lower = content.lower()
    keyword_counts = {}
    
    for subject, keywords in subject_keywords.items():
        count = sum(1 for keyword in keywords if keyword in content_lower)
        if count > 0:
            keyword_counts[subject] = count
    
    return keyword_counts


def _classify_subject(keyword_counts: Dict[str, int], metadata: Dict[str, Any]) -> str:
    """Classify document subject."""
    if keyword_counts:
        # Return subject with highest keyword count
        return max(keyword_counts, key=keyword_counts.get)
    
    # Check metadata
    if "subject" in metadata:
        return metadata["subject"]
    
    return "general"


def _extract_topic(content: str, subject: str) -> str:
    """Extract main topic from content."""
    # Simple heuristic: extract most frequent noun phrase
    # In production, this would use NLP models
    words = content.split()
    if len(words) > 0:
        return words[0].capitalize()
    return subject.capitalize()


def _determine_grade_level(content: str, metadata: Dict[str, Any]) -> str:
    """Determine appropriate grade level."""
    # Check metadata first
    if "grade_level" in metadata:
        return metadata["grade_level"]
    
    # Analyze complexity to estimate grade level
    vocab_score = _analyze_vocabulary_complexity(content)
    
    if vocab_score < 0.3:
        return "elementary"
    elif vocab_score < 0.5:
        return "middle"
    elif vocab_score < 0.7:
        return "high"
    else:
        return "advanced"


def _extract_subtopics(content: str, subject: str) -> List[str]:
    """Extract subtopics from content."""
    # Simple extraction based on section headers
    # In production, this would use topic modeling
    lines = content.split('\n')
    subtopics = []
    
    for line in lines:
        if line.strip().endswith(':') and len(line.strip()) < 50:
            potential_topic = line.strip().rstrip(':')
            if potential_topic and len(potential_topic.split()) <= 5:
                subtopics.append(potential_topic.capitalize())
    
    return subtopics[:5]  # Return top 5 subtopics


def _build_taxonomy_path(subject: str, topic: str, grade_level: str) -> str:
    """Build taxonomy path."""
    parts = [grade_level, subject, topic]
    return "/".join(parts)


def _calculate_subject_confidence(keyword_counts: Dict[str, int]) -> float:
    """Calculate confidence in subject classification."""
    if not keyword_counts:
        return 0.0
    
    total_count = sum(keyword_counts.values())
    max_count = max(keyword_counts.values())
    
    return max_count / total_count if total_count > 0 else 0.0


def _load_educational_standards() -> Dict[str, Any]:
    """Load educational standards (placeholder)."""
    # In production, this would load from database or file
    return {
        "indonesia": {
            "mathematics": ["bilangan", "aljabar", "geometri", "statistika"],
            "science": ["biologi", "fisika", "kimia"],
            "language": ["bahasa", "literasi", "sastra"]
        },
        "international": {
            "mathematics": ["number_sense", "algebra", "geometry", "measurement"],
            "science": ["life_science", "physical_science", "earth_science"],
            "language": ["reading", "writing", "listening", "speaking"]
        }
    }


def _extract_skill_tags(content: str, taxonomy_result: Dict[str, Any]) -> List[str]:
    """Extract skill tags from content."""
    # Simple keyword extraction
    # In production, this would use skill extraction models
    skill_keywords = [
        "problem_solving", "critical_thinking", "analysis",
        "calculation", "measurement", "observation",
        "comparison", "classification", "synthesis"
    ]
    
    content_lower = content.lower()
    found_skills = [skill for skill in skill_keywords if skill in content_lower]
    
    return found_skills


def _map_to_competencies(
    skill_tags: List[str],
    taxonomy_result: Dict[str, Any],
    standards: Dict[str, Any]
) -> List[str]:
    """Map skill tags to educational competencies."""
    subject = taxonomy_result.get("subject", "general")
    grade_level = taxonomy_result.get("grade_level", "elementary")
    
    # Map to standard competencies
    # In production, this would use more sophisticated mapping
    competencies = []
    
    for skill in skill_tags:
        competency = f"{grade_level}_{subject}_{skill}"
        competencies.append(competency)
    
    return competencies


def _determine_competency_levels(competencies: List[str], grade_level: str) -> Dict[str, str]:
    """Determine competency levels for each competency."""
    levels = {}
    
    for competency in competencies:
        # Simple heuristic: assign based on grade level
        if grade_level in ["elementary", "middle"]:
            levels[competency] = "developing"
        else:
            levels[competency] = "proficient"
    
    return levels


def _calculate_alignment_scores(competencies: List[str], standards: Dict[str, Any]) -> Dict[str, float]:
    """Calculate alignment scores with educational standards."""
    # Simple placeholder implementation
    # In production, this would use actual standard matching
    scores = {}
    
    for competency in competencies:
        # Check if competency matches any standard
        for standard_name, standard_competencies in standards.items():
            for std_comp in standard_competencies:
                if std_comp in competency.lower():
                    scores[standard_name] = 0.8  # Placeholder score
                    break
    
    return scores


def _get_aligned_standards(competencies: List[str]) -> List[str]:
    """Get list of aligned educational standards."""
    # Placeholder implementation
    return ["indonesia"] if competencies else []


async def _update_document_in_db(document_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Update document in database (placeholder)."""
    # In production, this would call the document service
    logger.info(f"Updating document {document_id} in database")
    
    return {
        "document_id": document_id,
        "success": True
    }