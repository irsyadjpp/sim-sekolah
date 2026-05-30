"""
MinIO AIStor Integration for Semantic Chunk Service
Implementation untuk menggunakan MinIO AIStor sebagai source untuk knowledge assets
"""

from typing import Optional, List, Dict, Any
import tempfile
import os
from pathlib import Path
from app.schemas.chunking_schemas import (
    ChunkRequest, 
    ChunkResponse, 
    ChunkInfo, 
    ChunkMetadata,
    DocumentMetadata
)
from app.config.minio_config import get_minio_client


class MinIOChunkingService:
    """
    Semantic chunking service dengan MinIO AIStor integration.
    Membaca knowledge assets dari MinIO AIStor dan melakukan semantic chunking.
    """
    
    def __init__(self):
        """Initialize service dengan MinIO AIStor client."""
        self.minio_client = get_minio_client()
    
    def chunk_from_minio(
        self, 
        document_path: str,
        options: 'ChunkingOptions',
        metadata: Optional[DocumentMetadata] = None
    ) -> ChunkResponse:
        """
        Chunk document yang disimpan di MinIO AIStor.
        
        Args:
            document_path: Path ke document di MinIO AIStor (relatif terhadap knowledge prefix)
                        Contoh: "cp/matematika/kelas-10/v1.0.0/cp.json"
            options: Chunking options
            metadata: Optional document metadata (akan di-enrich dengan metadata dari MinIO)
            
        Returns:
            ChunkResponse dengan hasil chunking
        """
        try:
            import time
            start_time = time.time()
            
            # 1. Get document dengan metadata dari MinIO AIStor
            content, minio_metadata = self.minio_client.get_object_with_metadata(document_path)
            
            if content is None:
                return ChunkResponse(
                    success=False,
                    document_id=document_path,
                    status="failed",
                    message=f"Document not found in MinIO AIStor: {document_path}"
                )
            
            # 2. Extract educational metadata dari MinIO AIStor metadata
            enriched_metadata = self._enrich_metadata_from_minio(
                metadata, 
                minio_metadata
            )
            
            # 3. Decode content berdasarkan file type
            text = self._decode_content(content, minio_metadata)
            
            # 4. Perform semantic chunking
            chunks = self._perform_chunking(text, options, enriched_metadata)
            
            # 5. Calculate processing time
            processing_time = time.time() - start_time
            
            # 6. Generate statistics
            statistics = self._calculate_statistics(chunks, minio_metadata)
            
            return ChunkResponse(
                success=True,
                document_id=document_path,
                status="completed",
                chunks=chunks,
                chunk_count=len(chunks),
                processing_time=processing_time,
                statistics=statistics,
                message=f"Successfully chunked document from MinIO AIStor in {processing_time:.2f}s"
            )
            
        except Exception as e:
            return ChunkResponse(
                success=False,
                document_id=document_path,
                status="failed",
                message=f"Error chunking from MinIO AIStor: {str(e)}"
            )
    
    def batch_chunk_from_minio(
        self,
        document_paths: List[str],
        options: 'ChunkingOptions'
    ) -> Dict[str, Any]:
        """
        Batch chunk multiple documents dari MinIO AIStor.
        
        Args:
            document_paths: List of document paths di MinIO AIStor
            options: Chunking options (applied ke semua documents)
            
        Returns:
            Dictionary dengan batch results
        """
        import concurrent.futures
        from datetime import datetime
        
        results = []
        completed = 0
        failed = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit semua chunking tasks
            future_to_path = {
                executor.submit(self.chunk_from_minio, path, options): path 
                for path in document_paths
            }
            
            # Collect results
            for future in concurrent.futures.as_completed(future_to_path):
                document_path = future_to_path[future]
                try:
                    result = future.result()
                    if result.success:
                        completed += 1
                    else:
                        failed += 1
                    results.append({
                        'document_path': document_path,
                        'success': result.success,
                        'status': result.status,
                        'chunk_count': result.chunk_count,
                        'processing_time': result.processing_time,
                        'message': result.message
                    })
                except Exception as e:
                    failed += 1
                    results.append({
                        'document_path': document_path,
                        'success': False,
                        'status': 'failed',
                        'message': f"Exception: {str(e)}"
                    })
        
        return {
            'success': failed == 0,
            'total_documents': len(document_paths),
            'completed': completed,
            'failed': failed,
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _enrich_metadata_from_minio(
        self,
        user_metadata: Optional[DocumentMetadata],
        minio_metadata: Dict[str, Any]
    ) -> DocumentMetadata:
        """
        Enrich user metadata dengan metadata dari MinIO AIStor.
        
        Args:
            user_metadata: Metadata yang disediakan user
            minio_metadata: Metadata yang tersimpan di MinIO AIStor
            
        Returns:
            Enriched DocumentMetadata
        """
        # Start dengan user metadata atau empty
        enriched = user_metadata if user_metadata else DocumentMetadata()
        
        # Enrich dengan MinIO AIStor metadata jika tersedia
        if minio_metadata:
            # Map common fields
            if not enriched.title and minio_metadata.get('title'):
                enriched.title = minio_metadata['title']
            
            if not enriched.subject and minio_metadata.get('subject'):
                enriched.subject = minio_metadata['subject']
            
            if not enriched.grade and minio_metadata.get('grade_level'):
                enriched.grade = minio_metadata['grade_level']
            
            if not enriched.phase and minio_metadata.get('phase'):
                enriched.phase = minio_metadata['phase']
            
            if not enriched.language and minio_metadata.get('language'):
                enriched.language = minio_metadata['language']
            
            # Extract curriculum source dari path structure
            if not enriched.curriculum_source:
                original_path = minio_metadata.get('original_path', '')
                if 'cp/' in original_path:
                    enriched.curriculum_source = 'CP'
                elif 'atp/' in original_path:
                    enriched.curriculum_source = 'ATP'
                elif 'buku_guru/' in original_path:
                    enriched.curriculum_source = 'buku_guru'
                elif 'buku_siswa/' in original_path:
                    enriched.curriculum_source = 'buku_siswa'
                elif 'modul_ajar/' in original_path:
                    enriched.curriculum_source = 'modul_ajar'
                elif 'asesmen/' in original_path:
                    enriched.curriculum_source = 'asesmen'
        
        return enriched
    
    def _decode_content(
        self, 
        content: bytes, 
        minio_metadata: Dict[str, Any]
    ) -> str:
        """
        Decode content berdasarkan file type.
        
        Args:
            content: Raw content bytes
            minio_metadata: File metadata
            
        Returns:
            Decoded text content
        """
        file_type = minio_metadata.get('file_type', '').lower()
        
        # JSON files
        if file_type == '.json':
            try:
                import json
                data = json.loads(content.decode('utf-8'))
                
                # Extract text dari JSON structure
                if isinstance(data, dict):
                    # Coba extract dari common JSON structure
                    if 'content' in data:
                        return data['content']
                    elif 'text' in data:
                        return data['text']
                    elif 'description' in data:
                        return data['description']
                    else:
                        # Convert seluruh JSON ke string representation
                        return json.dumps(data, indent=2)
                elif isinstance(data, list):
                    return json.dumps(data, indent=2)
                
            except json.JSONDecodeError:
                # Fallback ke raw text
                return content.decode('utf-8')
        
        # PDF files (akan perlu PDF parser)
        elif file_type == '.pdf':
            # Untuk sekarang return placeholder, but seharusnya
            # menggunakan PDF parser service
            return f"[PDF Content - Size: {len(content)} bytes]"
        
        # Text files
        elif file_type in ['.txt', '.md']:
            return content.decode('utf-8')
        
        # Default: try UTF-8 decode
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            return f"[Binary Content - Size: {len(content)} bytes]"
    
    def _perform_chunking(
        self,
        text: str,
        options: 'ChunkingOptions',
        metadata: DocumentMetadata
    ) -> List[ChunkInfo]:
        """
        Perform semantic chunking berdasarkan options.
        
        Args:
            text: Text content to chunk
            options: Chunking options
            metadata: Document metadata
            
        Returns:
            List of ChunkInfo
        """
        chunks = []
        
        # Implement semantic chunking logic
        # Ini adalah simplified version, actual implementation
        # akan lebih sophisticated dengan NLP models
        
        if options.chunking_strategy.value == "competency_based":
            chunks = self._competency_based_chunking(text, metadata)
        elif options.chunking_strategy.value == "activity_based":
            chunks = self._activity_based_chunking(text, metadata)
        elif options.chunking_strategy.value == "assessment_based":
            chunks = self._assessment_based_chunking(text, metadata)
        elif options.chunking_strategy.value == "inquiry_based":
            chunks = self._inquiry_based_chunking(text, metadata)
        else:
            chunks = self._semantic_based_chunking(text, options, metadata)
        
        return chunks
    
    def _semantic_based_chunking(
        self,
        text: str,
        options: 'ChunkingOptions',
        metadata: DocumentMetadata
    ) -> List[ChunkInfo]:
        """
        Basic semantic chunking implementation.
        
        Args:
            text: Text content
            options: Chunking options
            metadata: Document metadata
            
        Returns:
            List of chunks
        """
        chunks = []
        
        # Simple chunking by size (actual implementation akan lebih sophisticated)
        chunk_size = options.chunk_size
        overlap = options.chunk_overlap
        
        # Split text into chunks
        for i in range(0, len(text), chunk_size - overlap):
            chunk_text = text[i:i + chunk_size]
            
            if len(chunk_text) < 50:  # Skip terlalu short chunks
                continue
            
            chunk_id = f"{metadata.document_type or 'doc'}_{i // (chunk_size - overlap)}"
            
            chunk_info = ChunkInfo(
                chunk_id=chunk_id,
                text=chunk_text,
                metadata=ChunkMetadata(
                    chunk_id=chunk_id,
                    chunk_type="semantic",
                    subject=metadata.subject,
                    grade=metadata.grade,
                    phase=metadata.phase,
                    document_position=i,
                    confidence=0.8  # Placeholder confidence score
                ),
                character_count=len(chunk_text),
                word_count=len(chunk_text.split()),
                position=i // (chunk_size - overlap),
                confidence=0.8
            )
            
            chunks.append(chunk_info)
        
        return chunks
    
    def _competency_based_chunking(
        self,
        text: str,
        metadata: DocumentMetadata
    ) -> List[ChunkInfo]:
        """Chunk by competency (KI-1, KI-2, KI-3, KI-4)."""
        # Implement competency-based chunking logic
        chunks = []
        
        # Pattern matching untuk competency indicators
        competency_patterns = [
            r"KI-1[\s:]",  # Kompetensi Inti 1
            r"KI-2[\s:]",  # Kompetensi Inti 2
            r"KI-3[\s:]",  # Kompetensi Inti 3
            r"KI-4[\s:]",  # Kompetensi Inti 4
        ]
        
        import re
        for pattern in competency_patterns:
            matches = list(re.finditer(pattern, text))
            for i, match in enumerate(matches):
                start = match.start()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                chunk_text = text[start:end].strip()
                
                if len(chunk_text) > 50:
                    chunk_id = f"competency_{pattern}_{i}"
                    chunks.append(ChunkInfo(
                        chunk_id=chunk_id,
                        text=chunk_text,
                        metadata=ChunkMetadata(
                            chunk_id=chunk_id,
                            chunk_type="competency",
                            competency=pattern,
                            subject=metadata.subject,
                            grade=metadata.grade,
                            document_position=start,
                            confidence=0.9
                        ),
                        character_count=len(chunk_text),
                        word_count=len(chunk_text.split()),
                        position=i,
                        confidence=0.9
                    ))
        
        return chunks if chunks else self._semantic_based_chunking(text, None, metadata)
    
    def _activity_based_chunking(self, text: str, metadata: DocumentMetadata) -> List[ChunkInfo]:
        """Chunk by learning activities."""
        # Implement activity-based chunking
        return self._semantic_based_chunking(text, None, metadata)
    
    def _assessment_based_chunking(self, text: str, metadata: DocumentMetadata) -> List[ChunkInfo]:
        """Chunk by assessment items."""
        # Implement assessment-based chunking
        return self._semantic_based_chunking(text, None, metadata)
    
    def _inquiry_based_chunking(self, text: str, metadata: DocumentMetadata) -> List[ChunkInfo]:
        """Chunk for inquiry learning."""
        # Implement inquiry-based chunking
        return self._semantic_based_chunking(text, None, metadata)
    
    def _calculate_statistics(
        self,
        chunks: List[ChunkInfo],
        seaweedfs_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate statistics tentang chunking results.
        
        Args:
            chunks: List of chunks
            seaweedfs_metadata: SeaweedFS metadata
            
        Returns:
            Statistics dictionary
        """
        if not chunks:
            return {}
        
        total_chars = sum(chunk.character_count for chunk in chunks)
        total_words = sum(chunk.word_count for chunk in chunks)
        avg_chunk_size = total_chars / len(chunks)
        
        # Calculate size variance
        chunk_sizes = [chunk.character_count for chunk in chunks]
        variance = sum((size - avg_chunk_size) ** 2 for size in chunk_sizes) / len(chunk_sizes)
        
        # Chunk type distribution
        chunk_type_dist = {}
        for chunk in chunks:
            chunk_type = chunk.metadata.chunk_type
            chunk_type_dist[chunk_type] = chunk_type_dist.get(chunk_type, 0) + 1
        
        # Pedagogy distribution
        pedagogy_dist = {}
        for chunk in chunks:
            pedagogy = chunk.metadata.pedagogy_type
            if pedagogy:
                pedagogy_dist[pedagogy] = pedagogy_dist.get(pedagogy, 0) + 1
        
        # Cognitive level distribution
        cognitive_dist = {}
        for chunk in chunks:
            level = chunk.metadata.cognitive_level
            if level:
                cognitive_dist[level] = cognitive_dist.get(level, 0) + 1
        
        return {
            'total_chunks': len(chunks),
            'total_characters': total_chars,
            'total_words': total_words,
            'average_chunk_length': avg_chunk_size,
            'min_chunk_length': min(chunk_sizes),
            'max_chunk_length': max(chunk_sizes),
            'size_variance': variance,
            'chunk_types_distribution': chunk_type_dist,
            'pedagogy_distribution': pedagogy_dist,
            'cognitive_level_distribution': cognitive_dist,
            'source': 'seaweedfs',
            'file_hash': seaweedfs_metadata.get('file_hash'),
            'upload_timestamp': seaweedfs_metadata.get('upload_timestamp'),
            'metadata_coverage': self._calculate_metadata_coverage(chunks)
        }
    
    def _calculate_metadata_coverage(self, chunks: List[ChunkInfo]) -> float:
        """Calculate percentage of chunks dengan complete metadata."""
        complete_chunks = 0
        for chunk in chunks:
            metadata = chunk.metadata
            if (metadata.subject and metadata.grade and 
                metadata.chunk_type and metadata.competency):
                complete_chunks += 1
        
        return (complete_chunks / len(chunks)) * 100 if chunks else 0


# Factory function untuk service creation
# Note: SeaweedFSChunkingService not implemented, commenting out
# def create_seaweedfs_chunking_service() -> SeaweedFSChunkingService:
#     """
#     Factory function untuk create SeaweedFS chunking service.
#     
#     Returns:
#         SeaweedFSChunkingService instance
#     """
#     return SeaweedFSChunkingService()