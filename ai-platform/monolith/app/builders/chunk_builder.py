import logging
from typing import Dict, Any, List, Optional
import time

logger = logging.getLogger(__name__)


class ChunkBuilder:
    """
    Main chunk builder that orchestrates all chunking components
    
    This is the CORE component that builds educational semantic chunks
    """
    
    def __init__(
        self,
        competency_chunker,
        activity_chunker,
        assessment_chunker,
        inquiry_chunker,
        lesson_plan_chunker,
        hierarchy_detector,
        pedagogy_classifier,
        taxonomy_tagger,
        chunk_enricher
    ):
        """Initialize chunk builder with all chunking components"""
        self.competency_chunker = competency_chunker
        self.activity_chunker = activity_chunker
        self.assessment_chunker = assessment_chunker
        self.inquiry_chunker = inquiry_chunker
        self.lesson_plan_chunker = lesson_plan_chunker
        self.hierarchy_detector = hierarchy_detector
        self.pedagogy_classifier = pedagogy_classifier
        self.taxonomy_tagger = taxonomy_tagger
        self.chunk_enricher = chunk_enricher
        
        logger.info("Chunk builder initialized with all components")
    
    def build_chunks(
        self,
        text: str,
        options: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build semantic chunks based on strategy
        
        Args:
            text: Text to chunk
            options: Chunking options
            metadata: Document metadata
            
        Returns:
            Chunking result with chunks and statistics
        """
        start_time = time.time()
        
        try:
            logger.info(f"Building chunks with strategy: {options.get('chunking_strategy', 'semantic')}")
            
            # Select chunking strategy
            chunking_strategy = options.get('chunking_strategy', 'semantic')
            
            # Build chunks based on strategy
            if chunking_strategy == 'competency_based':
                chunks = self.competency_chunker.chunk(text, metadata)
            elif chunking_strategy == 'activity_based':
                chunks = self.activity_chunker.chunk(text, metadata)
            elif chunking_strategy == 'assessment_based':
                chunks = self.assessment_chunker.chunk(text, metadata)
            elif chunking_strategy == 'inquiry_based':
                chunks = self.inquiry_chunker.chunk(text, metadata)
            elif chunking_strategy == 'lesson_plan_based':
                chunks = self.lesson_plan_chunker.chunk(text, metadata)
            else:  # semantic (default)
                chunks = self._build_semantic_chunks(text, options, metadata)
            
            # Enrich chunks if requested
            if options.get('enrich_chunks', True):
                chunks = self._enrich_chunks(chunks, metadata)
            
            # Calculate statistics
            statistics = self._calculate_statistics(chunks)
            
            processing_time = time.time() - start_time
            
            result = {
                'chunks': chunks,
                'processing_time': processing_time,
                'statistics': statistics
            }
            
            logger.info(f"Built {len(chunks)} chunks in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Error building chunks: {str(e)}")
            raise
    
    def _build_semantic_chunks(self, text: str, options: Dict[str, Any], metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build semantic chunks using multiple strategies"""
        try:
            # Detect hierarchy first
            hierarchy = None
            if options.get('detect_hierarchy', True):
                hierarchy = self.hierarchy_detector.detect(text)
            
            # Try competency chunking first (most important)
            chunks = self.competency_chunker.chunk(text, metadata)
            
            # If competency chunking didn't work well, try other strategies
            if len(chunks) < 2:
                logger.info("Competency chunking produced few chunks, trying activity chunking")
                chunks = self.activity_chunker.chunk(text, metadata)
            
            # If still few chunks, use fallback
            if len(chunks) < 2:
                logger.info("Still few chunks, using semantic chunking fallback")
                chunks = self._semantic_fallback_chunking(text, options, metadata)
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error building semantic chunks: {str(e)}")
            return self._semantic_fallback_chunking(text, options, metadata)
    
    def _semantic_fallback_chunking(self, text: str, options: Dict[str, Any], metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fallback semantic chunking"""
        # Simple semantic chunking based on paragraphs
        paragraphs = text.split('\n\n')
        chunks = []
        
        chunk_size = options.get('chunk_size', 500)
        current_chunk = []
        current_size = 0
        
        import uuid
        
        for i, para in enumerate(paragraphs):
            para_size = len(para)
            
            if current_size + para_size > chunk_size and current_chunk:
                chunk_id = str(uuid.uuid4())
                chunk_text = ' '.join(current_chunk)
                
                chunks.append({
                    'chunk_id': chunk_id,
                    'text': chunk_text,
                    'metadata': {
                        'chunk_id': chunk_id,
                        'chunk_type': 'semantic',
                        'subject': metadata.get('subject'),
                        'grade': metadata.get('grade'),
                        'phase': metadata.get('phase'),
                        'document_position': i,
                        'chunk_quality_score': 0.6,
                        'educational_value_score': 0.65
                    },
                    'character_count': len(chunk_text),
                    'word_count': len(chunk_text.split()),
                    'position': i,
                    'confidence': 0.6
                })
                
                current_chunk = [para]
                current_size = para_size
            else:
                current_chunk.append(para)
                current_size += para_size
        
        # Don't forget the last chunk
        if current_chunk:
            chunk_id = str(uuid.uuid4())
            chunk_text = ' '.join(current_chunk)
            
            chunks.append({
                'chunk_id': chunk_id,
                'text': chunk_text,
                'metadata': {
                    'chunk_id': chunk_id,
                    'chunk_type': 'semantic',
                    'subject': metadata.get('subject'),
                    'grade': metadata.get('grade'),
                    'phase': metadata.get('phase'),
                    'document_position': len(paragraphs),
                    'chunk_quality_score': 0.6,
                    'educational_value_score': 0.65
                },
                'character_count': len(chunk_text),
                'word_count': len(chunk_text.split()),
                'position': len(paragraphs),
                'confidence': 0.6
            })
        
        return chunks
    
    def _enrich_chunks(self, chunks: List[Dict[str, Any]], metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Enrich chunks with additional educational metadata"""
        try:
            enriched_chunks = []
            
            for chunk in chunks:
                # Get chunk text
                chunk_text = chunk['text']
                
                # Classify pedagogy if requested
                pedagogy_result = self.pedagogy_classifier.classify(chunk_text)
                
                # Tag taxonomy if requested
                taxonomy_result = self.taxonomy_tagger.tag(chunk_text)
                
                # Update chunk metadata
                enriched_metadata = chunk['metadata'].copy()
                enriched_metadata.update({
                    'pedagogy_type': pedagogy_result.get('pedagogy_type'),
                    'cognitive_level': taxonomy_result.get('dominant_level'),
                    'pedagogy_confidence': pedagogy_result.get('confidence', 0.0),
                    'taxonomy_confidence': taxonomy_result.get('confidence', 0.0)
                })
                
                # Update chunk
                enriched_chunk = chunk.copy()
                enriched_chunk['metadata'] = enriched_metadata
                
                enriched_chunks.append(enriched_chunk)
            
            return enriched_chunks
            
        except Exception as e:
            logger.error(f"Error enriching chunks: {str(e)}")
            return chunks
    
    def _calculate_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics about the chunks"""
        try:
            if not chunks:
                return {}
            
            # Basic statistics
            total_chunks = len(chunks)
            sizes = [chunk['character_count'] for chunk in chunks]
            words = [chunk['word_count'] for chunk in chunks]
            
            avg_chunk_length = sum(sizes) / total_chunks
            min_chunk_length = min(sizes)
            max_chunk_length = max(sizes)
            avg_word_count = sum(words) / total_chunks
            
            # Type distribution
            chunk_types = {}
            for chunk in chunks:
                chunk_type = chunk['metadata'].get('chunk_type', 'unknown')
                chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
            
            # Pedagogy distribution
            pedagogy_distribution = {}
            for chunk in chunks:
                pedagogy = chunk['metadata'].get('pedagogy_type', 'unknown')
                if pedagogy:
                    pedagogy_distribution[pedagogy] = pedagogy_distribution.get(pedagogy, 0) + 1
            
            # Cognitive level distribution
            cognitive_distribution = {}
            for chunk in chunks:
                cognitive = chunk['metadata'].get('cognitive_level', 'unknown')
                if cognitive:
                    cognitive_distribution[cognitive] = cognitive_distribution.get(cognitive, 0) + 1
            
            # Quality metrics
            quality_scores = [chunk['metadata'].get('chunk_quality_score', 0.5) for chunk in chunks]
            avg_quality = sum(quality_scores) / total_chunks
            
            return {
                'total_chunks': total_chunks,
                'average_chunk_length': avg_chunk_length,
                'min_chunk_length': min_chunk_length,
                'max_chunk_length': max_chunk_length,
                'average_word_count': avg_word_count,
                'chunk_types_distribution': chunk_types,
                'pedagogy_distribution': pedagogy_distribution,
                'cognitive_level_distribution': cognitive_distribution,
                'quality_metrics': {
                    'average_quality_score': avg_quality,
                    'min_quality': min(quality_scores),
                    'max_quality': max(quality_scores)
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating statistics: {str(e)}")
            return {}