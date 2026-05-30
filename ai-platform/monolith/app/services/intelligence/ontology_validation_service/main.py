"""
Ontology Validation Service Main Application
Validates educational tags against Kurikulum Merdeka and other educational standards
"""
import sys
sys.path.append('/app')

import logging
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import validators
from app.validators.competency_validator import CompetencyValidator
from app.validators.pedagogy_validator import PedagogyValidator
from app.validators.taxonomy_validator import TaxonomyValidator

# Import shared components
from common.config.settings import settings
from common.logging.logger import setup_logging
from common.schemas.common import HealthResponse

# Setup logging
logger = setup_logging("ontology-validation-service")


# Request/Response Models
class CompetencyValidationRequest(BaseModel):
    """Request for competency code validation"""
    competency_code: str
    subject: Optional[str] = None
    grade_level: Optional[str] = None


class CompetencyBatchValidationRequest(BaseModel):
    """Request for batch competency validation"""
    competency_codes: List[str]
    context: Optional[Dict[str, Any]] = None


class PedagogyValidationRequest(BaseModel):
    """Request for pedagogy validation"""
    pedagogy_type: str
    teaching_method: Optional[str] = None


class PedagogyBatchValidationRequest(BaseModel):
    """Request for batch pedagogy validation"""
    pedagogy_list: List[Dict[str, Any]]


class TaxonomyValidationRequest(BaseModel):
    """Request for taxonomy validation"""
    taxonomy_type: str  # 'blooms', 'indonesian', 'competency_dimension'
    blooms_level: Optional[str] = None
    verb: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    phase: Optional[str] = None
    grade_level: Optional[int] = None


class TaxonomyBatchValidationRequest(BaseModel):
    """Request for batch taxonomy validation"""
    taxonomy_list: List[Dict[str, Any]]


class ComprehensiveValidationRequest(BaseModel):
    """Request for comprehensive validation of all tag types"""
    competency_codes: Optional[List[str]] = None
    pedagogy_tags: Optional[List[Dict[str, Any]]] = None
    taxonomy_tags: Optional[List[Dict[str, Any]]] = None
    context: Optional[Dict[str, Any]] = None


class OntologyValidationService:
    """Main ontology validation service"""
    
    def validate_competency(self, competency_code: str, subject: Optional[str] = None, 
                          grade_level: Optional[str] = None) -> Dict[str, Any]:
        """Validate a single competency code"""
        return CompetencyValidator.validate_competency_code(competency_code, subject, grade_level)
    
    def validate_competency_batch(self, competency_codes: List[str], 
                                 context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Validate multiple competency codes"""
        return CompetencyValidator.validate_competency_batch(competency_codes, context)
    
    def validate_pedagogy(self, pedagogy_type: str, teaching_method: Optional[str] = None) -> Dict[str, Any]:
        """Validate a pedagogy type and teaching method"""
        return PedagogyValidator.validate_pedagogy_type(pedagogy_type, teaching_method)
    
    def validate_pedagogy_batch(self, pedagogy_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate multiple pedagogy entries"""
        return PedagogyValidator.validate_pedagogy_batch(pedagogy_list)
    
    def validate_taxonomy(self, taxonomy_type: str, **kwargs) -> Dict[str, Any]:
        """Validate taxonomy based on type"""
        if taxonomy_type == "blooms":
            blooms_level = kwargs.get("blooms_level")
            verb = kwargs.get("verb")
            return TaxonomyValidator.validate_blooms_level(blooms_level, verb)
        elif taxonomy_type == "indonesian":
            category = kwargs.get("category")
            subcategory = kwargs.get("subcategory")
            return TaxonomyValidator.validate_indonesian_taxonomy(category, subcategory)
        elif taxonomy_type == "competency_dimension":
            phase = kwargs.get("phase")
            grade_level = kwargs.get("grade_level")
            return TaxonomyValidator.validate_competency_dimension(phase, grade_level)
        else:
            return {
                "valid": False,
                "error": f"Unknown taxonomy type: {taxonomy_type}"
            }
    
    def validate_taxonomy_batch(self, taxonomy_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate multiple taxonomy entries"""
        return TaxonomyValidator.validate_taxonomy_batch(taxonomy_list)
    
    def validate_comprehensive(self, competency_codes: Optional[List[str]] = None,
                             pedagogy_tags: Optional[List[Dict[str, Any]]] = None,
                             taxonomy_tags: Optional[List[Dict[str, Any]]] = None,
                             context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Validate all tag types comprehensively"""
        results = {
            "overall_valid": True,
            "competency_validation": None,
            "pedagogy_validation": None,
            "taxonomy_validation": None
        }
        
        if competency_codes:
            competency_result = self.validate_competency_batch(competency_codes, context)
            results["competency_validation"] = competency_result
            if not competency_result["valid"]:
                results["overall_valid"] = False
        
        if pedagogy_tags:
            pedagogy_result = self.validate_pedagogy_batch(pedagogy_tags)
            results["pedagogy_validation"] = pedagogy_result
            if not pedagogy_result["valid"]:
                results["overall_valid"] = False
        
        if taxonomy_tags:
            taxonomy_result = self.validate_taxonomy_batch(taxonomy_tags)
            results["taxonomy_validation"] = taxonomy_result
            if not taxonomy_result["valid"]:
                results["overall_valid"] = False
        
        return results


ontology_service = OntologyValidationService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    logger.info("Starting Ontology Validation Service")
    yield
    logger.info("Shutting down Ontology Validation Service")


# Initialize FastAPI app
app = FastAPI(
    title="AI Platform Ontology Validation Service",
    description="Validates educational tags against Kurikulum Merdeka and educational standards",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers
)


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        environment=settings.environment,
        services={
            "ontology_validation": "available"
        }
    )


# Competency validation endpoints
@app.post("/api/v1/validate/competency")
async def validate_competency(request: CompetencyValidationRequest):
    """Validate a single competency code"""
    try:
        result = ontology_service.validate_competency(
            request.competency_code,
            request.subject,
            request.grade_level
        )
        return result
    except Exception as e:
        logger.error(f"Error validating competency: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/validate/competency/batch")
async def validate_competency_batch(request: CompetencyBatchValidationRequest):
    """Validate multiple competency codes in batch"""
    try:
        result = ontology_service.validate_competency_batch(
            request.competency_codes,
            request.context
        )
        return result
    except Exception as e:
        logger.error(f"Error validating competency batch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Pedagogy validation endpoints
@app.post("/api/v1/validate/pedagogy")
async def validate_pedagogy(request: PedagogyValidationRequest):
    """Validate a pedagogy type and teaching method"""
    try:
        result = ontology_service.validate_pedagogy(
            request.pedagogy_type,
            request.teaching_method
        )
        return result
    except Exception as e:
        logger.error(f"Error validating pedagogy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/validate/pedagogy/batch")
async def validate_pedagogy_batch(request: PedagogyBatchValidationRequest):
    """Validate multiple pedagogy entries in batch"""
    try:
        result = ontology_service.validate_pedagogy_batch(request.pedagogy_list)
        return result
    except Exception as e:
        logger.error(f"Error validating pedagogy batch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Taxonomy validation endpoints
@app.post("/api/v1/validate/taxonomy")
async def validate_taxonomy(request: TaxonomyValidationRequest):
    """Validate taxonomy based on type"""
    try:
        result = ontology_service.validate_taxonomy(
            request.taxonomy_type,
            blooms_level=request.blooms_level,
            verb=request.verb,
            category=request.category,
            subcategory=request.subcategory,
            phase=request.phase,
            grade_level=request.grade_level
        )
        return result
    except Exception as e:
        logger.error(f"Error validating taxonomy: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/validate/taxonomy/batch")
async def validate_taxonomy_batch(request: TaxonomyBatchValidationRequest):
    """Validate multiple taxonomy entries in batch"""
    try:
        result = ontology_service.validate_taxonomy_batch(request.taxonomy_list)
        return result
    except Exception as e:
        logger.error(f"Error validating taxonomy batch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Comprehensive validation endpoint
@app.post("/api/v1/validate/comprehensive")
async def validate_comprehensive(request: ComprehensiveValidationRequest):
    """Validate all tag types comprehensively"""
    try:
        result = ontology_service.validate_comprehensive(
            request.competency_codes,
            request.pedagogy_tags,
            request.taxonomy_tags,
            request.context
        )
        return result
    except Exception as e:
        logger.error(f"Error validating comprehensive: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Standards reference endpoints
@app.get("/api/v1/standards/competency")
async def get_competency_standards(subject: Optional[str] = None):
    """Get official competency standards"""
    try:
        return CompetencyValidator.get_competency_standards(subject)
    except Exception as e:
        logger.error(f"Error getting competency standards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/standards/pedagogy")
async def get_pedagogy_standards(framework: str = "kurikulum_merdeka"):
    """Get official pedagogy standards"""
    try:
        return PedagogyValidator.get_pedagogy_standards(framework)
    except Exception as e:
        logger.error(f"Error getting pedagogy standards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/standards/taxonomy")
async def get_taxonomy_standards(framework: str = "both"):
    """Get official taxonomy standards"""
    try:
        return TaxonomyValidator.get_taxonomy_standards(framework)
    except Exception as e:
        logger.error(f"Error getting taxonomy standards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)