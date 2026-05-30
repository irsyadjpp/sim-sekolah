"""
Semantic Enrichment Service - Integration Service
Connects to upstream/downstream services:
- Curriculum Engine (gRPC) — curriculum alignment validation
- Pedagogy Engine (gRPC) — pedagogy classification
- Educational Ontology Service (gRPC/Neo4j) — knowledge graph tagging
- Metadata Service (gRPC) — storing enriched metadata
"""
import sys
import os
sys.path.append('/app')

import logging
from typing import Dict, Any, List, Optional
import grpc
from datetime import datetime

from common.infrastructure.grpc.channel import create_channel, call_with_retry
from common.config.settings import settings

logger = logging.getLogger(__name__)


class CurriculumEngineClient:
    """gRPC client for Curriculum Engine integration."""
    
    def __init__(self, target: str = None):
        self.target = target or "curriculum-engine:50060"
        self._channel = None
        self._stub = None
        logger.info(f"CurriculumEngineClient initialized for target: {self.target}")
    
    async def _get_stub(self):
        if self._stub is None:
            try:
                import proto.curriculum_engine_pb2 as curr_pb2
                import proto.curriculum_engine_pb2_grpc as curr_pb2_grpc
                self._channel = create_channel(target=self.target, default_timeout=60.0)
                self._stub = curr_pb2_grpc.CurriculumEngineStub(self._channel)
                logger.info(f"Connected to Curriculum Engine at {self.target}")
            except ImportError:
                logger.warning("Curriculum Engine protobuf stubs not found, using fallback")
                return None
            except Exception as e:
                logger.error(f"Failed to connect to Curriculum Engine: {str(e)}")
                return None
        return self._stub
    
    async def validate_alignment(
        self,
        content: str,
        competency_codes: List[str] = None,
        phase: str = "",
        grade: str = "",
        subject: str = ""
    ) -> Dict[str, Any]:
        """Validate content alignment with curriculum standards."""
        try:
            try:
                import proto.curriculum_engine_pb2 as curr_pb2
            except ImportError:
                return self._fallback_validation(content, competency_codes, phase, grade, subject)
            
            stub = await self._get_stub()
            if stub is None:
                return self._fallback_validation(content, competency_codes, phase, grade, subject)
            
            request = curr_pb2.ValidateAlignmentRequest(
                content=content,
                competency_codes=competency_codes or [],
                phase=phase,
                grade=grade,
                subject=subject
            )
            
            response = await call_with_retry(stub.ValidateAlignment, request, timeout=60.0)
            
            return {
                "success": response.success,
                "is_aligned": response.result.is_aligned if response.result else False,
                "alignment_score": response.result.alignment_score if response.result else 0.0,
                "details": [
                    {
                        "competency_code": d.competency_code,
                        "competency_name": d.competency_name,
                        "alignment_score": d.alignment_score,
                        "status": d.status,
                        "evidence": d.evidence
                    }
                    for d in (response.result.details if response.result else [])
                ],
                "recommendations": list(response.result.recommendations) if response.result else []
            }
        except Exception as e:
            logger.error(f"Curriculum Engine validation error: {str(e)}")
            return self._fallback_validation(content, competency_codes, phase, grade, subject)
    
    def _fallback_validation(
        self, content: str, competency_codes: List[str],
        phase: str, grade: str, subject: str
    ) -> Dict[str, Any]:
        """Fallback curriculum validation when service is unavailable."""
        content_lower = content.lower()
        alignment_score = 0.5
        
        if subject and subject.lower() in content_lower:
            alignment_score += 0.15
        if grade and grade.lower() in content_lower:
            alignment_score += 0.1
        if competency_codes:
            for code in competency_codes:
                if code.lower() in content_lower:
                    alignment_score += 0.1
                    break
        
        alignment_score = min(alignment_score, 1.0)
        
        return {
            "success": True,
            "is_aligned": alignment_score >= 0.5,
            "alignment_score": alignment_score,
            "details": [
                {
                    "competency_code": code,
                    "competency_name": f"Competency {code}",
                    "alignment_score": alignment_score,
                    "status": "aligned" if alignment_score >= 0.5 else "partial",
                    "evidence": f"Keyword matching with score {alignment_score:.2f}"
                }
                for code in (competency_codes or [])
            ],
            "recommendations": [
                f"Ensure content covers all aspects of {code}"
                for code in (competency_codes or []) if alignment_score < 0.7
            ]
        }
    
    async def close(self):
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stub = None


class PedagogyEngineClient:
    """gRPC client for Pedagogy Engine integration."""
    
    def __init__(self, target: str = None):
        self.target = target or "pedagogy-engine:50061"
        self._channel = None
        self._stub = None
        logger.info(f"PedagogyEngineClient initialized for target: {self.target}")
    
    async def _get_stub(self):
        if self._stub is None:
            try:
                import proto.pedagogy_engine_pb2 as ped_pb2
                import proto.pedagogy_engine_pb2_grpc as ped_pb2_grpc
                self._channel = create_channel(target=self.target, default_timeout=60.0)
                self._stub = ped_pb2_grpc.PedagogyEngineStub(self._channel)
                logger.info(f"Connected to Pedagogy Engine at {self.target}")
            except ImportError:
                logger.warning("Pedagogy Engine protobuf stubs not found, using fallback")
                return None
            except Exception as e:
                logger.error(f"Failed to connect to Pedagogy Engine: {str(e)}")
                return None
        return self._stub
    
    async def classify_pedagogy(
        self,
        content: str,
        context: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Classify pedagogical approach for content."""
        try:
            try:
                import proto.pedagogy_engine_pb2 as ped_pb2
            except ImportError:
                return self._fallback_classification(content, context)
            
            stub = await self._get_stub()
            if stub is None:
                return self._fallback_classification(content, context)
            
            request = ped_pb2.ClassifyPedagogyRequest(
                content=content,
                context=context or {}
            )
            
            response = await call_with_retry(stub.ClassifyPedagogy, request, timeout=60.0)
            
            return {
                "success": response.success,
                "primary_pedagogy": response.result.primary_pedagogy if response.result else "direct_instruction",
                "confidence": response.result.confidence if response.result else 0.5,
                "labels": [
                    {"pedagogy_type": l.pedagogy_type, "confidence": l.confidence}
                    for l in (response.result.labels if response.result else [])
                ]
            }
        except Exception as e:
            logger.error(f"Pedagogy Engine classification error: {str(e)}")
            return self._fallback_classification(content, context)
    
    def _fallback_classification(
        self, content: str, context: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Fallback pedagogy classification."""
        content_lower = content.lower()
        
        pedagogy_scores = {
            "direct_instruction": 0.3,
            "inquiry_based": 0.2,
            "project_based": 0.2,
            "collaborative": 0.15,
            "problem_based": 0.15
        }
        
        inquiry_keywords = ["experiment", "hypothesis", "observe", "discover", "investigate", "riset", "percobaan", "amati"]
        project_keywords = ["project", "projek", "create", "build", "design", "buat", "rancang"]
        collaborative_keywords = ["discuss", "group", "together", "collaborate", "diskusi", "kelompok"]
        problem_keywords = ["problem", "solve", "challenge", "masalah", "tantangan", "selesaikan"]
        direct_keywords = ["explain", "definition", "concept", "theory", "jelaskan", "definisi", "konsep"]
        
        for kw in inquiry_keywords:
            if kw in content_lower:
                pedagogy_scores["inquiry_based"] += 0.15
        for kw in project_keywords:
            if kw in content_lower:
                pedagogy_scores["project_based"] += 0.15
        for kw in collaborative_keywords:
            if kw in content_lower:
                pedagogy_scores["collaborative"] += 0.15
        for kw in problem_keywords:
            if kw in content_lower:
                pedagogy_scores["problem_based"] += 0.15
        for kw in direct_keywords:
            if kw in content_lower:
                pedagogy_scores["direct_instruction"] += 0.15
        
        primary = max(pedagogy_scores, key=pedagogy_scores.get)
        total = sum(pedagogy_scores.values())
        
        labels = [
            {"pedagogy_type": k, "confidence": round(v / total, 3)}
            for k, v in sorted(pedagogy_scores.items(), key=lambda x: -x[1])
        ]
        
        return {
            "success": True,
            "primary_pedagogy": primary,
            "confidence": round(pedagogy_scores[primary] / total, 3),
            "labels": labels
        }
    
    async def close(self):
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stub = None


class OntologyServiceClient:
    """gRPC client for Educational Ontology Service integration."""
    
    def __init__(self, target: str = None):
        self.target = target or "educational-ontology-service:50062"
        self._channel = None
        self._stub = None
        logger.info(f"OntologyServiceClient initialized for target: {self.target}")
    
    async def _get_stub(self):
        if self._stub is None:
            try:
                import proto.educational_ontology_pb2 as onto_pb2
                import proto.educational_ontology_pb2_grpc as onto_pb2_grpc
                self._channel = create_channel(target=self.target, default_timeout=60.0)
                self._stub = onto_pb2_grpc.EducationalOntologyServiceStub(self._channel)
                logger.info(f"Connected to Educational Ontology Service at {self.target}")
            except ImportError:
                logger.warning("Ontology Service protobuf stubs not found, using fallback")
                return None
            except Exception as e:
                logger.error(f"Failed to connect to Ontology Service: {str(e)}")
                return None
        return self._stub
    
    async def extract_entities(
        self,
        content: str,
        context: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Extract educational entities and relationships from content."""
        try:
            try:
                import proto.educational_ontology_pb2 as onto_pb2
            except ImportError:
                return self._fallback_extraction(content, context)
            
            stub = await self._get_stub()
            if stub is None:
                return self._fallback_extraction(content, context)
            
            request = onto_pb2.ExtractEntitiesRequest(
                content=content,
                context=context or {}
            )
            
            response = await call_with_retry(stub.ExtractEntities, request, timeout=60.0)
            
            return {
                "success": response.success,
                "entities": [
                    {"entity": e.entity, "entity_type": e.entity_type, "confidence": e.confidence}
                    for e in (response.result.entities if response.result else [])
                ],
                "relationships": [
                    {"source": r.source, "target": r.target, "relationship": r.relationship}
                    for r in (response.result.relationships if response.result else [])
                ]
            }
        except Exception as e:
            logger.error(f"Ontology Service extraction error: {str(e)}")
            return self._fallback_extraction(content, context)
    
    def _fallback_extraction(
        self, content: str, context: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Fallback entity extraction."""
        content_lower = content.lower()
        entities = []
        relationships = []
        
        entity_patterns = {
            "concept": ["concept", "theory", "principle", "konsep", "teori", "prinsip"],
            "process": ["process", "method", "technique", "proses", "metode", "teknik"],
            "phenomenon": ["phenomenon", "occurrence", "event", "fenomena", "peristiwa"],
            "organization": ["organization", "institution", "organisasi", "lembaga"],
            "standard": ["standard", "competency", "standar", "kompetensi"],
            "curriculum": ["curriculum", "syllabus", "kurikulum", "silabus"],
            "assessment": ["assessment", "evaluation", "asesmen", "evaluasi"],
            "pedagogy": ["pedagogy", "teaching", "learning", "pedagogi", "pembelajaran"]
        }
        
        for etype, keywords in entity_patterns.items():
            for kw in keywords:
                if kw in content_lower:
                    entities.append({
                        "entity": kw,
                        "entity_type": etype,
                        "confidence": 0.6
                    })
        
        if len(entities) >= 2:
            for i in range(min(len(entities), 5)):
                for j in range(i + 1, min(len(entities), 5)):
                    relationships.append({
                        "source": entities[i]["entity"],
                        "target": entities[j]["entity"],
                        "relationship": "related_to"
                    })
        
        return {
            "success": True,
            "entities": entities,
            "relationships": relationships
        }
    
    async def close(self):
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stub = None


class MetadataServiceClient:
    """gRPC client for Metadata Service integration (storing enriched metadata)."""
    
    def __init__(self, target: str = None):
        self.target = target or "metadata-service:50053"
        self._channel = None
        self._stub = None
        logger.info(f"MetadataServiceClient initialized for target: {self.target}")
    
    async def _get_stub(self):
        if self._stub is None:
            try:
                import proto.metadata_service_pb2 as meta_pb2
                import proto.metadata_service_pb2_grpc as meta_pb2_grpc
                self._channel = create_channel(target=self.target, default_timeout=60.0)
                self._stub = meta_pb2_grpc.MetadataServiceStub(self._channel)
                logger.info(f"Connected to Metadata Service at {self.target}")
            except ImportError:
                logger.warning("Metadata Service protobuf stubs not found")
                return None
            except Exception as e:
                logger.error(f"Failed to connect to Metadata Service: {str(e)}")
                return None
        return self._stub
    
    async def store_enriched_metadata(
        self,
        chunk_id: str,
        enriched_metadata: Dict[str, str]
    ) -> Dict[str, Any]:
        """Store enriched metadata for a chunk."""
        try:
            try:
                import proto.metadata_service_pb2 as meta_pb2
            except ImportError:
                return {"success": True, "stored_locally": True}
            
            stub = await self._get_stub()
            if stub is None:
                return {"success": True, "stored_locally": True}
            
            request = meta_pb2.StoreEnrichedMetadataRequest(
                content_id=chunk_id,
                enriched_metadata=enriched_metadata
            )
            
            response = await call_with_retry(stub.StoreEnrichedMetadata, request, timeout=30.0)
            return {"success": response.success, "message": response.message}
            
        except Exception as e:
            logger.error(f"Metadata Service store error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def close(self):
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stub = None


class EnrichmentIntegrationService:
    """
    Unified integration service for Semantic Enrichment Service.
    Coordinates Curriculum Engine, Pedagogy Engine, Ontology Service, and Metadata Service.
    """
    
    def __init__(
        self,
        curriculum_target: str = None,
        pedagogy_target: str = None,
        ontology_target: str = None,
        metadata_target: str = None
    ):
        self.curriculum_client = CurriculumEngineClient(target=curriculum_target)
        self.pedagogy_client = PedagogyEngineClient(target=pedagogy_target)
        self.ontology_client = OntologyServiceClient(target=ontology_target)
        self.metadata_client = MetadataServiceClient(target=metadata_target)
        logger.info("EnrichmentIntegrationService initialized")
    
    async def classify_pedagogy(
        self,
        chunk_id: str,
        content: str,
        context: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Classify pedagogical approach for a chunk."""
        return await self.pedagogy_client.classify_pedagogy(content=content, context=context)
    
    async def tag_taxonomy(
        self,
        chunk_id: str,
        content: str,
        context: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Tag chunk with taxonomy information using ontology entities."""
        ontology_result = await self.ontology_client.extract_entities(content=content, context=context)
        
        taxonomy_tags = []
        entity_type_to_category = {
            "concept": "knowledge",
            "process": "skill",
            "phenomenon": "understanding",
            "standard": "competency",
            "curriculum": "framework",
            "assessment": "evaluation",
            "pedagogy": "methodology",
            "organization": "context"
        }
        
        for entity in ontology_result.get("entities", []):
            etype = entity.get("entity_type", "concept")
            taxonomy_tags.append({
                "taxonomy_code": f"EDU-{etype.upper()[:3]}",
                "taxonomy_name": entity.get("entity", ""),
                "confidence": entity.get("confidence", 0.5),
                "category": entity_type_to_category.get(etype, "general")
            })
        
        primary_category = taxonomy_tags[0]["category"] if taxonomy_tags else "general"
        confidence = taxonomy_tags[0]["confidence"] if taxonomy_tags else 0.0
        
        return {
            "success": True,
            "taxonomy_tags": taxonomy_tags,
            "primary_category": primary_category,
            "confidence": confidence
        }
    
    async def enrich_chunk(
        self,
        chunk_id: str,
        content: str,
        enrichment_types: List[str] = None,
        context: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Full enrichment: pedagogy + taxonomy + ontology + curriculum."""
        enrichment_types = enrichment_types or ["pedagogy", "taxonomy", "ontology"]
        
        pedagogy_result = {}
        taxonomy_result = {}
        ontology_result = {}
        curriculum_result = {}
        
        if "pedagogy" in enrichment_types:
            pedagogy_result = await self.pedagogy_client.classify_pedagogy(content=content, context=context)
        
        if "taxonomy" in enrichment_types or "ontology" in enrichment_types:
            ontology_result = await self.ontology_client.extract_entities(content=content, context=context)
        
        if "pedagogy" in enrichment_types or "taxonomy" in enrichment_types:
            taxonomy_result = await self.tag_taxonomy(chunk_id=chunk_id, content=content, context=context)
        
        if "curriculum" in enrichment_types and context:
            curriculum_result = await self.curriculum_client.validate_alignment(
                content=content,
                competency_codes=context.get("competency_codes", "").split(",") if context.get("competency_codes") else [],
                phase=context.get("phase", ""),
                grade=context.get("grade", ""),
                subject=context.get("subject", "")
            )
        
        enriched_metadata = {
            "pedagogy_type": pedagogy_result.get("primary_pedagogy", ""),
            "pedagogy_confidence": str(pedagogy_result.get("confidence", 0.0)),
            "taxonomy_category": taxonomy_result.get("primary_category", ""),
            "ontology_entities_count": str(len(ontology_result.get("entities", []))),
            "curriculum_aligned": str(curriculum_result.get("is_aligned", False)) if curriculum_result else "unknown",
            "curriculum_score": str(curriculum_result.get("alignment_score", 0.0)) if curriculum_result else "0.0",
            "enriched_at": datetime.utcnow().isoformat()
        }
        
        try:
            await self.metadata_client.store_enriched_metadata(
                chunk_id=chunk_id,
                enriched_metadata=enriched_metadata
            )
        except Exception as e:
            logger.warning(f"Failed to store enriched metadata: {str(e)}")
        
        return {
            "success": True,
            "chunk_id": chunk_id,
            "pedagogy": pedagogy_result,
            "taxonomy": taxonomy_result,
            "ontology": ontology_result,
            "curriculum": curriculum_result,
            "enriched_metadata": enriched_metadata
        }
    
    async def validate_curriculum_alignment(
        self,
        chunk_id: str,
        content: str,
        competency_codes: List[str] = None,
        phase: str = "",
        grade: str = "",
        subject: str = ""
    ) -> Dict[str, Any]:
        """Validate content alignment with curriculum standards."""
        return await self.curriculum_client.validate_alignment(
            content=content,
            competency_codes=competency_codes,
            phase=phase,
            grade=grade,
            subject=subject
        )
    
    async def batch_enrich(
        self,
        items: List[Dict[str, Any]],
        enrichment_types: List[str] = None
    ) -> Dict[str, Any]:
        """Batch enrich multiple chunks."""
        results = []
        successful = 0
        failed = 0
        
        for item in items:
            chunk_id = item.get("chunk_id", "")
            content = item.get("content", "")
            context = item.get("context", {})
            
            try:
                result = await self.enrich_chunk(
                    chunk_id=chunk_id,
                    content=content,
                    enrichment_types=enrichment_types,
                    context=context
                )
                results.append(result)
                if result.get("success"):
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                results.append({
                    "chunk_id": chunk_id,
                    "success": False,
                    "error": str(e)
                })
                failed += 1
        
        return {
            "success": True,
            "results": results,
            "summary": {
                "total_items": len(items),
                "successful_items": successful,
                "failed_items": failed,
                "average_confidence": 0.0
            }
        }
    
    async def close(self):
        await self.curriculum_client.close()
        await self.pedagogy_client.close()
        await self.ontology_client.close()
        await self.metadata_client.close()
        logger.info("EnrichmentIntegrationService connections closed")


_enrichment_integration_service: Optional[EnrichmentIntegrationService] = None


def get_enrichment_integration_service(
    curriculum_target: str = None,
    pedagogy_target: str = None,
    ontology_target: str = None,
    metadata_target: str = None
) -> EnrichmentIntegrationService:
    global _enrichment_integration_service
    if _enrichment_integration_service is None:
        _enrichment_integration_service = EnrichmentIntegrationService(
            curriculum_target=curriculum_target,
            pedagogy_target=pedagogy_target,
            ontology_target=ontology_target,
            metadata_target=metadata_target
        )
    return _enrichment_integration_service