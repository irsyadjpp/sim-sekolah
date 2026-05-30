# PRD - Strategic Analysis Service

**Document Version:** 1.0  
**Date:** 2026-05-28  
**Module:** Strategic Analysis Service  
**Service Type:** AI-Powered Analysis Backend Service

---

## 1. Product Overview

The Strategic Analysis Service is an AI-powered backend microservice that provides intelligent analysis capabilities for educational institutions in Indonesia. It serves as the analytical engine within the SIM Sekolah Terpadu platform, enabling schools to perform strategic planning through multiple analytical frameworks:

- **SWOT Analysis**: Comprehensive Strengths, Weaknesses, Opportunities, and Threats analysis with strategic recommendations
- **Root Cause Analysis**: Deep problem analysis using 5-Whys methodology to identify fundamental causes
- **Fishbone Diagram**: Ishikawa diagram analysis across 6M categories (Man, Machine, Method, Material, Measurement, Environment)
- **KSP Generation**: Automated generation of Kurikulum Satuan Pendidikan (School Curriculum) documents based on integrated analysis data

The service leverages Large Language Models (LLMs) to generate contextual, Indonesian-language analysis tailored to the Indonesian education context and Kurikulum Merdeka framework. It operates as a stateless service with dual protocol support (REST and gRPC) and asynchronous processing capabilities via RabbitMQ.

**Primary Value Proposition**: Empower Indonesian schools with AI-driven strategic analysis tools that transform raw data into actionable insights for educational improvement and curriculum planning.

---

## 2. User Persona

### 2.1 School Administrators (Kepala Sekolah & Wakil Kepala Sekolah)
- **Role**: Decision-makers responsible for school strategic planning
- **Access Level**: Full access to all analysis features
- **Goals**: Generate comprehensive SWOT analysis, identify root causes of problems, create strategic plans

### 2.2 Curriculum Developers (Kurikulum Developer)
- **Role**: Responsible for developing and maintaining school curriculum (KSP)
- **Access Level**: KSP generation, integration of analysis data
- **Goals**: Generate KSP documents based on SWOT, root cause, and fishbone analysis

### 2.3 Quality Assurance Teams (Tim Mutu)
- **Role**: Monitor and improve school quality metrics
- **Access Level**: Root cause analysis, fishbone analysis, SWOT analysis
- **Goals**: Identify problems, analyze root causes, suggest improvements

### 2.4 System Integrators
- **Role**: Backend developers integrating with the service
- **Access Level**: API access (REST/gRPC), message queue integration
- **Goals**: Consume analysis services, integrate with frontend applications

---

## 3. User Story

### 3.1 SWOT Analysis
**As a School Administrator**, I want to generate a comprehensive SWOT analysis for my school, so that I can understand our internal strengths and weaknesses alongside external opportunities and threats to inform strategic planning.

### 3.2 Root Cause Analysis
**As a Quality Assurance Team Member**, I want to perform 5-Whys analysis on identified problems, so that I can uncover the fundamental causes and implement targeted interventions.

### 3.3 Fishbone Diagram
**As a Quality Assurance Team Member**, I want to analyze problems using the Fishbone (Ishikawa) method across 6M categories, so that I can systematically identify all potential contributing factors.

### 3.4 KSP Generation
**As a Curriculum Developer**, I want to generate Kurikulum Satuan Pendidikan documents based on integrated analysis data, so that I can create a curriculum that addresses identified needs and aligns with Kurikulum Merdeka.

### 3.5 Analysis Integration
**As a School Administrator**, I want to integrate SWOT, root cause, fishbone, and student needs data, so that I can gain cross-analysis insights and prioritize actions holistically.

---

## 4. Functional Requirement

### 4.1 SWOT Analysis Module

#### FR-SWOT-001: Comprehensive SWOT Analysis
- The system shall generate SWOT analysis with minimum 3 items per quadrant (Strengths, Weaknesses, Opportunities, Threats)
- The system shall assign priority scores (0.0-1.0) to each SWOT item
- The system shall categorize items into: akademik, sarana, sdm, keuangan, sosial
- The system shall generate strategic recommendations:
  - SO Strategies (Strengths-Opportunities): minimum 2 strategies
  - WO Strategies (Weaknesses-Opportunities): minimum 2 strategies
  - ST Strategies (Strengths-Threats): minimum 2 strategies
  - WT Strategies (Weaknesses-Threats): minimum 2 strategies
- The system shall provide an analysis confidence score (0.0-1.0)
- The system shall accept existing SWOT items as input for incremental analysis
- The system shall accept school context description for contextualization
- The system shall accept data sources list (e.g., "rapor_pendidikan", "survey")

#### FR-SWOT-002: SWOT Item Suggestions
- The system shall suggest SWOT items for specific quadrants
- The system shall limit suggestions to configurable maximum (default: 5)
- The system shall provide category and priority for each suggestion
- The system shall accept context parameter for relevance filtering

### 4.2 Root Cause Analysis Module

#### FR-RCA-001: Root Cause Analysis
- The system shall analyze root causes across three layers:
  - Immediate Causes (level 1)
  - Intermediate Causes (level 2)
  - Root Causes (fundamental level)
- The system shall provide confidence scores for each finding (0.0-1.0)
- The system shall include supporting evidence for each cause
- The system shall generate specific intervention recommendations
- The system shall provide intervention steps with timeframes:
  - Short-term (1 week)
  - Medium-term (1 month)
  - Long-term (3 months)
- The system shall accept existing causes as input
- The system shall accept problem description, category, and priority
- The system shall provide analysis summary (2-3 paragraphs)

#### FR-RCA-002: 5-Whys Analysis
- The system shall generate a structured 5-Whys chain
- The system shall allow configurable number of "why" levels (default: 5)
- The system shall provide:
  - Question for each level
  - Answer for each level
  - Rationale explaining the logical connection
- The system shall conclude with root cause identification
- The system shall provide corrective actions targeting the root cause
- The system shall accept problem statement and context

### 4.3 Fishbone Analysis Module

#### FR-FB-001: Fishbone Diagram Analysis
- The system shall analyze fishbone diagrams across 6M categories:
  - Man (Manusia/SDM)
  - Machine (Mesin/Peralatan)
  - Method (Metode/Prosedur)
  - Material (Material/Bahan)
  - Measurement (Pengukuran/Evaluasi)
  - Environment (Lingkungan)
- The system shall suggest causes with relevance scores (0.0-1.0)
- The system shall provide explanations for each suggested cause
- The system shall calculate completeness score (0.0-1.0) based on:
  - Minimum 2 causes per category required for full score
- The system shall identify priority causes requiring immediate attention
- The system shall accept existing fishbone nodes as input
- The system shall provide structured summary

#### FR-FB-002: Fishbone Category Suggestions
- The system shall suggest causes for all 6M categories
- The system shall limit suggestions per category (default: 3)
- The system shall ensure all 6M categories are represented
- The system shall provide concrete, verifiable suggestions

#### FR-FB-003: Fishbone Category Metadata
- The system shall provide list of available fishbone categories
- The system shall return category keys and Indonesian labels

### 4.4 KSP Generation Module

#### FR-KSP-001: Full KSP Document Generation
- The system shall generate KSP document sections from integrated analysis data
- The system shall support the following sections:
  - pendahuluan (Pendahuluan)
  - visi_misi (Visi dan Misi Sekolah)
  - tujuan_sekolah (Tujuan Sekolah)
  - pengorganisasian (Pengorganisasian Pembelajaran)
  - rencana_pembelajaran (Rencana Pembelajaran)
  - program_kerja (Program Kerja Sekolah)
  - evaluasi_pembelajaran (Evaluasi Pembelajaran)
  - rencana_tindak_lanjut (Rencana Tindak Lanjut)
  - penutup (Penutup)
- The system shall accept inputs from:
  - SWOT analysis data
  - Root cause analysis data
  - Fishbone analysis data
  - Student needs data
- The system shall allow selective section generation
- The system shall generate executive summary (3-4 paragraphs)
- The system shall support configurable tone (formal/semi_formal)
- The system shall ensure minimum 200 words per section
- The system shall include sub-sections for structured content

#### FR-KSP-002: Single KSP Section Generation
- The system shall generate individual KSP sections
- The system shall accept section key and title
- The system shall accept analysis context for the section
- The system shall accept school context
- The system shall allow configurable minimum word count (default: 300)
- The system shall return section content with sub-sections

#### FR-KSP-003: KSP Section Metadata
- The system shall provide list of available KSP sections
- The system shall return section keys and Indonesian titles

### 4.5 Analysis Integration Module

#### FR-INT-001: Cross-Analysis Integration
- The system shall integrate data from:
  - SWOT analysis
  - Root cause analysis
  - Fishbone analysis
  - Student needs
- The system shall identify:
  - Convergence: Areas where all analyses align
  - Gaps: Areas not covered by existing analyses
  - Priorities: Most urgent actions based on all data
- The system shall provide integrated insights with confidence scores
- The system shall include supporting evidence for each insight
- The system shall generate priority action list
- The system shall provide integrated summary (3-4 paragraphs)
- The system shall accept integration purpose parameter (e.g., "ksp_generation", "reporting", "dashboard")

### 4.6 Service Operations

#### FR-OPS-001: Health Check
- The system shall provide health check endpoint
- The system shall return service status
- The system shall return LLM provider type
- The system shall return LLM availability status

#### FR-OPS-002: Graceful Degradation
- The system shall fallback to rule-based responses when LLM is unavailable
- The system shall log warnings when using fallback mode
- The system shall maintain service availability during LLM outages
- The system shall provide placeholder responses indicating manual completion needed

---

## 5. Non-Functional Requirement

### 5.1 Performance Requirements

#### NFR-PER-001: Response Time
- REST API endpoints shall respond within 10 seconds for standard requests
- gRPC endpoints shall respond within 10 seconds for standard requests
- KSP full document generation may take up to 30 seconds
- Health check shall respond within 1 second

#### NFR-PER-002: Throughput
- Service shall handle minimum 50 concurrent requests
- Service shall support batch processing via message queue

### 5.2 Reliability Requirements

#### NFR-REL-001: Availability
- Service shall maintain 99% uptime during business hours
- Service shall support graceful restart without data loss (stateless design)

#### NFR-REL-002: Error Handling
- Service shall return HTTP 503 when engines not initialized
- Service shall log all errors with stack traces
- Service shall provide meaningful error messages in Indonesian

### 5.3 Security Requirements

#### NFR-SEC-001: API Key Protection
- LLM API keys shall be stored in environment variables
- API keys shall never be logged or exposed in responses
- Service shall support multiple LLM providers for redundancy

#### NFR-SEC-002: Input Validation
- All inputs shall be validated using Pydantic schemas
- String inputs shall have length limits
- Numeric inputs shall have range validation
- Invalid inputs shall return HTTP 422 with detailed error messages

### 5.4 Scalability Requirements

#### NFR-SCL-001: Horizontal Scaling
- Service shall be stateless to support horizontal scaling
- Service shall support containerized deployment via Docker
- Service shall support multiple instances behind load balancer

#### NFR-SCL-002: Resource Management
- Service shall limit LLM token usage via max_tokens parameter
- Service shall use temperature parameter for response variability control

### 5.5 Maintainability Requirements

#### NFR-MAI-001: Code Organization
- Service shall follow modular architecture with separate engine modules
- Service shall use dependency injection for LLM providers
- Service shall implement abstract base classes for provider abstraction

#### NFR-MAI-002: Logging
- Service shall log at INFO level for normal operations
- Service shall log at WARNING level for fallback modes
- Service shall log at ERROR level for failures
- Logs shall include timestamps and component names

### 5.6 Interoperability Requirements

#### NFR-INT-001: Protocol Support
- Service shall support REST API via FastAPI
- Service shall support gRPC for high-performance scenarios
- Service shall support RabbitMQ for asynchronous processing

#### NFR-INT-002: Data Formats
- REST API shall use JSON for request/response
- gRPC shall use Protocol Buffers
- Message queue shall use JSON message format

---

## 6. API Requirement

### 6.1 REST API Endpoints

#### 6.1.1 Health Check
**Endpoint**: `GET /health`  
**Tags**: health  
**Response**:
```json
{
  "status": "healthy",
  "service": "strategic-analysis-service",
  "llm_provider": "OpenAIProvider",
  "llm_available": true
}
```

#### 6.1.2 SWOT Analysis
**Endpoint**: `POST /api/v1/swot/analyze`  
**Tags**: swot  
**Request Body**:
```json
{
  "school_context": "string (optional)",
  "data_sources": ["string"] (optional),
  "existing_items": [{"id": "string", "quadrant": "string", "content": "string", "category": "string", "priority": 0.8}] (optional),
  "include_recommendations": true (optional, default: true)
}
```
**Response**:
```json
{
  "success": true,
  "result": {
    "strengths": [{"id": "string", "quadrant": "strength", "content": "string", "category": "string", "priority": 0.8, "data_source": "ai_generated"}],
    "weaknesses": [...],
    "opportunities": [...],
    "threats": [...],
    "so_strategies": ["string"],
    "wo_strategies": ["string"],
    "st_strategies": ["string"],
    "wt_strategies": ["string"],
    "summary": "string",
    "analysis_confidence": 0.85
  }
}
```
**Validations**: 
- school_context: string, max length 5000
- data_sources: array of strings, max 10 items
- existing_items: array, max 50 items
- include_recommendations: boolean

#### 6.1.3 SWOT Item Suggestions
**Endpoint**: `POST /api/v1/swot/suggest`  
**Tags**: swot  
**Request Body**:
```json
{
  "quadrant": "strength|weakness|opportunity|threat",
  "context": "string (optional)",
  "max_suggestions": 5 (optional, default: 5)
}
```
**Response**:
```json
{
  "success": true,
  "suggestions": [
    {"content": "string", "category": "string", "priority": 0.8}
  ]
}
```
**Validations**:
- quadrant: required, enum ["strength", "weakness", "opportunity", "threat"]
- context: string, max length 2000
- max_suggestions: integer, range 1-20

#### 6.1.4 Root Cause Analysis
**Endpoint**: `POST /api/v1/root-cause/analyze`  
**Tags**: root_cause  
**Request Body**:
```json
{
  "root_cause": {
    "problem": "string",
    "description": "string",
    "category": "string",
    "priority": "string",
    "existing_causes": ["string"]
  },
  "school_context": "string (optional)",
  "include_solutions": true (optional, default: true)
}
```
**Response**:
```json
{
  "success": true,
  "result": {
    "findings": [
      {
        "layer": "immediate|intermediate|root",
        "cause": "string",
        "explanation": "string",
        "confidence": 0.85,
        "evidence": ["string"]
      }
    ],
    "recommendations": ["string"],
    "intervention_steps": ["string"],
    "summary": "string",
    "analysis_confidence": 0.8
  }
}
```

#### 6.1.5 5-Whys Analysis
**Endpoint**: `POST /api/v1/root-cause/five-whys`  
**Tags**: root_cause  
**Request Body**:
```json
{
  "problem_statement": "string",
  "context": "string (optional)",
  "num_whys": 5 (optional, default: 5)
}
```
**Response**:
```json
{
  "success": true,
  "result": {
    "why_chain": [
      {
        "level": 1,
        "question": "string",
        "answer": "string",
        "rationale": "string"
      }
    ],
    "root_cause_conclusion": "string",
    "corrective_actions": ["string"]
  }
}
```
**Validations**:
- problem_statement: required, string, max length 1000
- context: string, max length 2000
- num_whys: integer, range 1-10

#### 6.1.6 Fishbone Analysis
**Endpoint**: `POST /api/v1/fishbone/analyze`  
**Tags**: fishbone  
**Request Body**:
```json
{
  "problem_statement": "string",
  "existing_nodes": [{"id": "string", "label": "string", "category": "string", "parent_id": "string"}] (optional),
  "context": "string (optional)"
}
```
**Response**:
```json
{
  "success": true,
  "result": {
    "suggestions": [
      {
        "category": "man|machine|method|material|measurement|environment",
        "cause": "string",
        "explanation": "string",
        "relevance": 0.9
      }
    ],
    "priority_causes": ["string"],
    "structured_summary": "string",
    "completeness_score": 0.75
  }
}
```

#### 6.1.7 Fishbone Category Suggestions
**Endpoint**: `POST /api/v1/fishbone/suggest-categories`  
**Tags**: fishbone  
**Request Body**:
```json
{
  "problem_statement": "string",
  "max_per_category": 3 (optional, default: 3)
}
```
**Response**:
```json
{
  "success": true,
  "categories": [
    {
      "category": "man",
      "suggestions": ["string", "string"]
    }
  ]
}
```

#### 6.1.8 Fishbone Categories List
**Endpoint**: `GET /api/v1/fishbone/categories`  
**Tags**: fishbone  
**Response**:
```json
{
  "categories": [
    {"key": "man", "label": "Manusia (SDM)"},
    {"key": "machine", "label": "Mesin/Peralatan"},
    {"key": "method", "label": "Metode/Prosedur"},
    {"key": "material", "label": "Material/Bahan"},
    {"key": "measurement", "label": "Pengukuran/Evaluasi"},
    {"key": "environment", "label": "Lingkungan"}
  ]
}
```

#### 6.1.9 KSP Full Generation
**Endpoint**: `POST /api/v1/ksp/generate`  
**Tags**: ksp  
**Request Body**:
```json
{
  "school_name": "string (optional)",
  "academic_year": "2024/2025" (optional, default: "2024/2025"),
  "swot_data": {} (optional),
  "root_cause_data": {} (optional),
  "fishbone_data": {} (optional),
  "student_needs_data": {} (optional),
  "sections_to_generate": ["string"] (optional, empty = all sections),
  "tone": "formal" (optional, default: "formal")
}
```
**Response**:
```json
{
  "success": true,
  "result": {
    "sections": [
      {
        "section_key": "visi_misi",
        "section_title": "Visi dan Misi Sekolah",
        "content": "string",
        "sub_sections": ["string"]
      }
    ],
    "executive_summary": "string"
  }
}
```

#### 6.1.10 KSP Section Generation
**Endpoint**: `POST /api/v1/ksp/section`  
**Tags**: ksp  
**Request Body**:
```json
{
  "section_key": "string",
  "section_title": "string (optional)",
  "analysis_context": "string (optional)",
  "school_context": "string (optional)",
  "max_words": 300 (optional, default: 300)
}
```
**Response**:
```json
{
  "success": true,
  "section": {
    "section_key": "string",
    "section_title": "string",
    "content": "string",
    "sub_sections": ["string"]
  }
}
```

#### 6.1.11 KSP Sections List
**Endpoint**: `GET /api/v1/ksp/sections`  
**Tags**: ksp  
**Response**:
```json
{
  "sections": [
    {"key": "pendahuluan", "title": "Pendahuluan"},
    {"key": "visi_misi", "title": "Visi dan Misi Sekolah"},
    {"key": "tujuan_sekolah", "title": "Tujuan Sekolah"},
    {"key": "pengorganisasian", "title": "Pengorganisasian Pembelajaran"},
    {"key": "rencana_pembelajaran", "title": "Rencana Pembelajaran"},
    {"key": "program_kerja", "title": "Program Kerja Sekolah"},
    {"key": "evaluasi_pembelajaran", "title": "Evaluasi Pembelajaran"},
    {"key": "rencana_tindak_lanjut", "title": "Rencana Tindak Lanjut"},
    {"key": "penutup", "title": "Penutup"}
  ]
}
```

#### 6.1.12 Analysis Integration
**Endpoint**: `POST /api/v1/analysis/integrate`  
**Tags**: integration  
**Request Body**:
```json
{
  "swot_data": {} (optional),
  "root_cause_data": {} (optional),
  "fishbone_data": {} (optional),
  "student_needs": {} (optional),
  "integration_purpose": "ksp_generation" (optional, default: "ksp_generation")
}
```
**Response**:
```json
{
  "success": true,
  "result": {
    "insights": [
      {
        "insight_type": "convergence|gap|priority",
        "description": "string",
        "confidence": 0.85,
        "supporting_evidence": ["string"]
      }
    ],
    "priority_actions": ["string"],
    "integrated_summary": "string"
  }
}
```

### 6.2 gRPC Service Methods

#### 6.2.1 AnalyzeSWOT
**Method**: `AnalyzeSWOT(AnalyzeSWOTRequest) returns (AnalyzeSWOTResponse)`  
**Request Fields**:
- school_context: string
- data_sources: repeated string
- existing_items: repeated SWOTItem
- include_recommendations: bool

**Response Fields**:
- success: bool
- message: string
- latency_ms: float
- result: SWOTAnalysisResult

#### 6.2.2 SuggestSWOTItems
**Method**: `SuggestSWOTItems(SuggestSWOTItemsRequest) returns (SuggestSWOTItemsResponse)`  
**Request Fields**:
- quadrant: string
- context: string
- max_suggestions: int32

#### 6.2.3 AnalyzeRootCause
**Method**: `AnalyzeRootCause(AnalyzeRootCauseRequest) returns (AnalyzeRootCauseResponse)`  
**Request Fields**:
- root_cause: RootCauseData
- school_context: string
- include_solutions: bool

#### 6.2.4 GenerateFiveWhys
**Method**: `GenerateFiveWhys(FiveWhysRequest) returns (FiveWhysResponse)`  
**Request Fields**:
- problem_statement: string
- context: string
- num_whys: int32

#### 6.2.5 AnalyzeFishbone
**Method**: `AnalyzeFishbone(AnalyzeFishboneRequest) returns (AnalyzeFishboneResponse)`  
**Request Fields**:
- problem_statement: string
- existing_nodes: repeated FishboneNode
- context: string

#### 6.2.6 SuggestFishboneCategories
**Method**: `SuggestFishboneCategories(SuggestFishboneCategoriesRequest) returns (SuggestFishboneCategoriesResponse)`  
**Request Fields**:
- problem_statement: string
- max_per_category: int32

#### 6.2.7 GenerateKSPContent
**Method**: `GenerateKSPContent(GenerateKSPContentRequest) returns (GenerateKSPContentResponse)`  
**Request Fields**:
- school_name: string
- academic_year: string
- swot_data: SWOTData
- root_cause_data: RootCauseData
- fishbone_data: FishboneData
- student_needs_data: StudentNeedsData
- sections_to_generate: repeated string
- tone: string

#### 6.2.8 GenerateKSPSection
**Method**: `GenerateKSPSection(GenerateKSPSectionRequest) returns (GenerateKSPSectionResponse)`  
**Request Fields**:
- section_key: string
- section_title: string
- analysis_context: string
- school_context: string
- max_words: int32

#### 6.2.9 IntegrateAnalysisData
**Method**: `IntegrateAnalysisData(IntegrateAnalysisDataRequest) returns (IntegrateAnalysisDataResponse)`  
**Request Fields**:
- swot_data: SWOTData
- root_cause_data: RootCauseData
- fishbone_data: FishboneData
- student_needs: StudentNeeds
- integration_purpose: string

#### 6.2.10 HealthCheck
**Method**: `HealthCheck(HealthCheckRequest) returns (HealthCheckResponse)`  
**Response Fields**:
- healthy: bool
- status: string
- version: string
- components: map<string, string>

### 6.3 RabbitMQ Message Types

#### 6.3.1 Message Queue Configuration
- **Queue**: `strategic_analysis.queue`
- **Exchange**: `ai.platform.exchange`
- **Routing Key**: `strategic_analysis.*`
- **Prefetch Count**: 3

#### 6.3.2 Supported Message Types
- `analyze_swot`
- `suggest_swot_items`
- `analyze_root_cause`
- `generate_five_whys`
- `analyze_fishbone`
- `suggest_fishbone_categories`
- `generate_ksp_content`
- `generate_ksp_section`
- `integrate_analysis_data`

#### 6.3.3 Message Format
All messages follow JSON format with:
- `message_type`: string (required)
- Payload fields matching REST API request bodies
- Response includes `success` boolean and corresponding result field

---

## 7. UI/UX Requirement

### 7.1 UI Scope
**Note**: This is a backend service with no direct UI components. The following requirements apply to consuming frontend applications.

### 7.2 Frontend Integration Guidelines

#### UX-INT-001: Loading States
- Frontend shall display loading indicators for requests > 2 seconds
- KSP generation shall show progress indicator (may take 20-30 seconds)
- Frontend shall implement timeout handling (30 second default)

#### UX-INT-002: Error Display
- Frontend shall display error messages in Indonesian
- Frontend shall provide fallback UI when LLM unavailable
- Frontend shall guide users to manual completion when in fallback mode

#### UX-INT-003: Data Visualization
- SWOT analysis shall display in 4-quadrant grid
- Fishbone diagram shall display as interactive tree structure
- 5-Whys shall display as numbered chain
- KSP document shall display as structured sections with expandable sub-sections

#### UX-INT-004: Form Validation
- Frontend shall validate quadrant selection (strength/weakness/opportunity/threat)
- Frontend shall validate fishbone category selection (6M categories)
- Frontend shall validate numeric ranges (num_whys: 1-10, max_suggestions: 1-20)
- Frontend shall provide real-time validation feedback

#### UX-INT-005: Contextual Help
- Frontend shall provide tooltips for SWOT quadrants
- Frontend shall provide explanations for 6M fishbone categories
- Frontend shall provide examples for each analysis type

---

## 8. Data Requirement

### 8.1 Data Entities

### 8.1.1 SWOT Item
**Fields**:
- id: string (UUID, auto-generated)
- quadrant: enum ["strength", "weakness", "opportunity", "threat"]
- content: string (max 500 chars)
- category: enum ["akademik", "sarana", "sdm", "keuangan", "sosial"]
- priority: float (0.0-1.0)
- data_source: string ("ai_generated" or "manual")

**State Transitions**: None (immutable once created)

### 8.1.2 Root Cause Finding
**Fields**:
- layer: enum ["immediate", "intermediate", "root"]
- cause: string (max 500 chars)
- explanation: string (max 1000 chars)
- confidence: float (0.0-1.0)
- evidence: array of strings

**State Transitions**: None (immutable once created)

### 8.1.3 Fishbone Suggestion
**Fields**:
- category: enum ["man", "machine", "method", "material", "measurement", "environment"]
- cause: string (max 500 chars)
- explanation: string (max 1000 chars)
- relevance: float (0.0-1.0)

**State Transitions**: None (immutable once created)

### 8.1.4 KSP Section
**Fields**:
- section_key: string (enum of 9 section keys)
- section_title: string (Indonesian label)
- content: string (min 200 words, no max limit)
- sub_sections: array of strings

**State Transitions**: None (immutable once generated)

### 8.1.5 Integration Insight
**Fields**:
- insight_type: enum ["convergence", "gap", "priority"]
- description: string (max 1000 chars)
- confidence: float (0.0-1.0)
- supporting_evidence: array of strings

**State Transitions**: None (immutable once created)

### 8.2 Data Dictionary

#### 8.2.1 SWOT Categories
- **akademik**: Academic performance, curriculum, teaching quality
- **sarana**: Facilities, infrastructure, equipment
- **sdm**: Human resources, staff competence
- **keuangan**: Budget, funding, financial management
- **sosial**: Community relations, partnerships, reputation

#### 8.2.2 Fishbone 6M Categories
- **man**: Human factors (teachers, students, parents, principal)
- **machine**: Equipment/technology factors (computers, projectors, labs, library)
- **method**: Method/procedure factors (teaching methods, curriculum, evaluation procedures)
- **material**: Material factors (textbooks, modules, worksheets, learning media)
- **measurement**: Measurement factors (assessment, report cards, competency standards)
- **environment**: Environmental factors (classroom, school, family, community)

#### 8.2.3 Root Cause Layers
- **immediate**: Direct, observable causes (first-level)
- **intermediate**: Contributing factors (second-level)
- **root**: Fundamental, systemic causes (third-level)

#### 8.2.4 KSP Sections
- **pendahuluan**: Introduction/background
- **visi_misi**: School vision and mission
- **tujuan_sekolah**: School objectives
- **pengorganisasian**: Learning organization structure
- **rencana_pembelajaran**: Learning plan
- **program_kerja**: School work program
- **evaluasi_pembelajaran**: Learning evaluation
- **rencana_tindak_lanjut**: Follow-up action plan
- **penutup**: Closing/conclusion

### 8.3 Data Flow

#### 8.3.1 SWOT Analysis Flow
1. User provides school context and optional existing items
2. Service sends prompt to LLM with context
3. LLM generates SWOT items in JSON format
4. Service parses JSON, enriches with IDs and metadata
5. Service returns structured SWOT result

#### 8.3.2 KSP Generation Flow
1. User provides integrated analysis data (SWOT, RCA, Fishbone, Student Needs)
2. Service summarizes each data source
3. Service sends integrated prompt to LLM
4. LLM generates KSP sections in JSON format
5. Service validates all requested sections present
6. Service returns KSP document with executive summary

#### 8.3.3 Integration Flow
1. User provides multiple analysis data sources
2. Service summarizes each source
3. Service sends integration prompt to LLM
4. LLM identifies convergences, gaps, and priorities
5. Service returns integrated insights with confidence scores

### 8.4 Data Persistence
**Note**: This service is stateless and does not persist data. Data persistence is handled by calling services or frontend applications.

---

## 9. Acceptance Criteria

### 9.1 SWOT Analysis Acceptance Criteria

#### AC-SWOT-001
**Given**: School administrator provides school context  
**When**: They request SWOT analysis  
**Then**: System shall return minimum 3 items per quadrant  
**And**: Each item shall have content, category, and priority  
**And**: System shall generate 8 strategic recommendations (2 per SO/WO/ST/WT)  
**And**: System shall provide analysis confidence score  
**And**: Response time shall be < 10 seconds

#### AC-SWOT-002
**Given**: School administrator provides existing SWOT items  
**When**: They request SWOT analysis with existing items  
**Then**: System shall incorporate existing items into analysis  
**And**: System shall generate additional items to reach minimum 3 per quadrant  
**And**: Existing items shall retain their original IDs and data_source

#### AC-SWOT-003
**Given**: LLM provider is not configured  
**When**: Any SWOT request is made  
**Then**: System shall return fallback response with placeholder data  
**And**: System shall log warning about fallback mode  
**And**: Response shall indicate manual completion needed

### 9.2 Root Cause Analysis Acceptance Criteria

#### AC-RCA-001
**Given**: Quality team provides problem statement  
**When**: They request 5-Whys analysis with 5 levels  
**Then**: System shall return 5 why levels  
**And**: Each level shall have question, answer, and rationale  
**And**: System shall identify root cause conclusion  
**And**: System shall provide corrective actions  
**And**: Response time shall be < 10 seconds

#### AC-RCA-002
**Given**: Quality team provides problem with existing causes  
**When**: They request root cause analysis  
**Then**: System shall analyze across immediate, intermediate, and root layers  
**And**: System shall provide confidence scores for each finding  
**And**: System shall include supporting evidence  
**And**: System shall generate intervention steps with timeframes

#### AC-RCA-003
**Given**: User requests num_whys outside range 1-10  
**When**: Request is validated  
**Then**: System shall return validation error  
**And**: Error message shall specify valid range

### 9.3 Fishbone Analysis Acceptance Criteria

#### AC-FB-001
**Given**: Quality team provides problem statement  
**When**: They request fishbone category suggestions  
**Then**: System shall return suggestions for all 6M categories  
**And**: Each category shall have minimum 2 suggestions  
**And**: Each suggestion shall be concrete and verifiable  
**And**: Response time shall be < 10 seconds

#### AC-FB-002
**Given**: Quality team provides existing fishbone nodes  
**When**: They request fishbone analysis  
**Then**: System shall calculate completeness score  
**And**: Score shall be 1.0 if all categories have >= 2 items  
**And**: System shall identify priority causes  
**And**: System shall provide structured summary

#### AC-FB-003
**Given**: User requests fishbone categories list  
**When**: Request is made  
**Then**: System shall return all 6 categories  
**And**: Each category shall have key and Indonesian label  
**And**: Response time shall be < 1 second

### 9.4 KSP Generation Acceptance Criteria

#### AC-KSP-001
**Given**: Curriculum developer provides integrated analysis data  
**When**: They request full KSP generation for all sections  
**Then**: System shall generate all 9 KSP sections  
**And**: Each section shall have minimum 200 words  
**And**: Each section shall have sub-sections  
**And**: System shall provide executive summary  
**And**: Response time shall be < 30 seconds

#### AC-KSP-002
**Given**: Curriculum developer requests specific sections  
**When**: They provide sections_to_generate list  
**Then**: System shall generate only requested sections  
**And**: System shall ensure all requested sections are present  
**And**: System shall fallback to placeholder if section generation fails

#### AC-KSP-003
**Given**: Curriculum developer sets tone to "formal"  
**When**: KSP is generated  
**Then**: Content shall use formal Indonesian language  
**And**: Content shall align with government document standards

### 9.5 Integration Acceptance Criteria

#### AC-INT-001
**Given**: Administrator provides SWOT, RCA, Fishbone, and Student Needs data  
**When**: They request analysis integration  
**Then**: System shall identify convergences across analyses  
**And**: System shall identify gaps in coverage  
**And**: System shall prioritize actions based on all data  
**And**: Each insight shall have confidence score and supporting evidence  
**And**: Response time shall be < 15 seconds

### 9.6 Service Operations Acceptance Criteria

#### AC-OPS-001
**Given**: Service is running  
**When**: Health check is requested  
**Then**: System shall return healthy status  
**And**: System shall return LLM provider type  
**And**: System shall return LLM availability  
**And**: Response time shall be < 1 second

#### AC-OPS-002
**Given**: Service receives invalid input (e.g., invalid quadrant)  
**When**: Request is processed  
**Then**: System shall return HTTP 422  
**And**: Error message shall detail validation failure  
**And**: Error message shall be in Indonesian

#### AC-OPS-003
**Given**: Service engines are not initialized  
**When**: Any analysis request is made  
**Then**: System shall return HTTP 503  
**And**: Error message shall indicate service not ready

### 9.7 Edge Cases

#### AC-EDGE-001
**Given**: LLM API call times out  
**When**: Analysis request is made  
**Then**: System shall return fallback response  
**And**: System shall log timeout error  
**And**: User shall be informed of manual completion needed

#### AC-EDGE-002
**Given**: LLM returns malformed JSON  
**When**: Response is parsed  
**Then**: System shall attempt to extract JSON from markdown code blocks  
**And**: If parsing fails, system shall return fallback response  
**And**: System shall log JSON parse warning

#### AC-EDGE-003
**Given**: User provides empty school_context  
**When**: SWOT analysis is requested  
**Then**: System shall use default context "Sekolah di Indonesia"  
**And**: Analysis shall proceed with generic recommendations

#### AC-EDGE-004
**Given**: RabbitMQ message has unknown message_type  
**When**: Message is processed  
**Then**: System shall raise ValueError  
**And** System shall log error with message type  
**And** Message shall be rejected

---

## 10. Technical Constraint

### 10.1 Infrastructure Constraints

#### TC-INF-001: LLM Provider Dependency
- Service requires external LLM provider (OpenAI, Anthropic, or Google)
- Service must handle provider unavailability gracefully
- API keys must be configured via environment variables
- No local LLM inference capability (requires cloud API)

#### TC-INF-002: Network Requirements
- Service requires outbound internet access for LLM API calls
- Service requires inbound access for REST (port 8020) and gRPC (port 50063)
- Service requires RabbitMQ connectivity if consumer enabled
- Latency to LLM APIs affects overall response time

#### TC-INF-003: Resource Constraints
- Service runs in Docker container with Python 3.11
- Memory usage depends on LLM response size (typically < 500MB)
- CPU usage minimal (I/O bound to LLM APIs)
- No GPU requirements

### 10.2 Integration Dependencies

#### TC-INT-001: Shared Libraries
- Service depends on `ai-platform-shared` package
- Service depends on `ai-platform-shared-grpc` for gRPC stubs
- Service depends on `ai-platform-shared-schemas` for common schemas
- Service depends on `ai-platform-shared-events` for event handling
- Service depends on `ai-platform-shared-observability` for logging/metrics
- If shared libraries unavailable, RabbitMQ consumer is disabled

#### TC-INT-002: Protocol Buffer Compilation
- gRPC stubs must be compiled via grpc_tools.protoc
- Proto file location: `../../proto/strategic_analysis_service.proto`
- If stubs not compiled, gRPC server runs in dict-passthrough mode
- Compilation command:
  ```bash
  python -m grpc_tools.protoc -I ../../proto \
    --python_out=. --grpc_python_out=. \
    ../../proto/strategic_analysis_service.proto
  ```

#### TC-INT-003: Message Queue Integration
- RabbitMQ consumer is optional (controlled by ENABLE_RABBITMQ_CONSUMER env var)
- If shared messaging library unavailable, consumer cannot start
- Consumer uses BaseRabbitMQConsumer from shared library
- Queue configuration: strategic_analysis.queue, ai.platform.exchange

### 10.3 Configuration Constraints

#### TC-CONF-001: Environment Variables
Required/Optional Environment Variables:
- `STRATEGIC_ANALYSIS_LLM_PROVIDER`: Optional, explicit provider selection ("openai", "anthropic", "google")
- `OPENAI_API_KEY`: Optional, for OpenAI provider
- `ANTHROPIC_API_KEY`: Optional, for Anthropic provider
- `GOOGLE_API_KEY` or `GEMINI_API_KEY`: Optional, for Google provider
- `OPENAI_MODEL`: Optional, default "gpt-4o-mini"
- `ANTHROPIC_MODEL`: Optional, default "claude-3-haiku-20240307"
- `GOOGLE_MODEL`: Optional, default "gemini-1.5-flash"
- `REST_PORT`: Optional, default 8020
- `GRPC_PORT`: Optional, default 50063
- `ENABLE_GRPC`: Optional, default "true"
- `ENABLE_RABBITMQ_CONSUMER`: Optional, default "false"
- `RABBITMQ_URL`: Optional, default "amqp://guest:guest@rabbitmq:5672/"
- `RUN_MODE`: Optional, "rest" or empty (default)

#### TC-CONF-002: Provider Selection Priority
1. Explicit STRATEGIC_ANALYSIS_LLM_PROVIDER if set and API key available
2. Auto-detect by API key availability: Google → OpenAI → Anthropic
3. StubProvider (no LLM, returns placeholders)

### 10.4 Deployment Constraints

#### TC-DEP-001: Container Deployment
- Service must be deployed as Docker container
- Base image: python:3.11-slim
- Exposed ports: 8020 (REST), 50063 (gRPC)
- Default command: gRPC server; set RUN_MODE=rest for FastAPI

#### TC-DEP-002: Scaling Constraints
- Service is stateless, supports horizontal scaling
- No session state or in-memory data persistence
- Multiple instances can run behind load balancer
- No shared storage requirements

#### TC-DEP-003: Monitoring Constraints
- Service uses standard Python logging
- No built-in metrics collection (relies on shared observability)
- Health check endpoint available for monitoring
- Logs include timestamps, component names, and log levels

### 10.5 Development Constraints

#### TC-DEV-001: Python Version
- Requires Python >= 3.11
- Uses type hints (from __future__ import annotations)
- Uses modern Python features (f-strings, match statement if needed)

#### TC-DEV-002: Dependency Management
- Uses pyproject.toml for dependencies
- Requires hatchling for build backend
- Dependencies include: fastapi, uvicorn, grpcio, protobuf, aio-pika, openai, anthropic, google-generativeai

#### TC-DEV-003: Code Organization
- Modular architecture with separate engine modules
- Abstract base class for LLM provider abstraction
- Dependency injection pattern for provider selection
- Clear separation between API layer (main.py, grpc_server.py) and business logic (engine/)

### 10.6 Security Constraints

#### TC-SEC-001: API Key Management
- API keys must never be hardcoded
- API keys must be stored in environment variables
- API keys must not be logged or exposed in error messages
- No API key rotation mechanism built-in (external rotation required)

#### TC-SEC-002: Input Sanitization
- All inputs validated via Pydantic schemas
- No SQL injection risk (no database)
- No command injection risk (no shell command execution)
- LLM prompts are constructed from validated inputs only

#### TC-SEC-003: CORS Configuration
- CORS allows all origins (*) in current configuration
- This must be restricted in production deployments
- Credentials allowed in CORS configuration

### 10.7 Limitations

#### TC-LIM-001: No Persistence
- Service does not persist any data
- All data is transient (request-response cycle)
- Calling services must handle persistence
- No audit trail built-in

#### TC-LIM-002: No Authentication/Authorization
- No built-in authentication mechanism
- No RBAC enforcement at service level
- Security must be handled at API gateway or reverse proxy
- All endpoints are publicly accessible by default

#### TC-LIM-003: No Rate Limiting
- No built-in rate limiting
- No request throttling
- Must be implemented at API gateway or infrastructure level
- Vulnerable to abuse if not protected externally

#### TC-LIM-004: No Retry Logic
- No automatic retry for LLM API failures
- No exponential backoff
- Single attempt per request
- Reliability depends on LLM provider uptime

#### TC-LIM-005: No Caching
- No response caching mechanism
- No memoization of LLM responses
- Identical requests will trigger new LLM calls
- Cost and latency implications for repeated requests

#### TC-LIM-006: Language Constraint
- Prompts and responses hardcoded for Indonesian language
- No multi-language support
- Not suitable for non-Indonesian educational contexts
- Localization would require prompt engineering changes

---

## Appendix A: Configuration Examples

### A.1 Docker Compose Example
```yaml
services:
  strategic-analysis:
    image: strategic-analysis-service:latest
    environment:
      - STRATEGIC_ANALYSIS_LLM_PROVIDER=openai
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=gpt-4o-mini
      - ENABLE_GRPC=true
      - ENABLE_RABBITMQ_CONSUMER=true
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
    ports:
      - "8020:8020"
      - "50063:50063"
```

### A.2 Environment File Example
```bash
STRATEGIC_ANALYSIS_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
REST_PORT=8020
GRPC_PORT=50063
ENABLE_GRPC=true
ENABLE_RABBITMQ_CONSUMER=false
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
```

---

## Appendix B: Error Response Examples

### B.1 Service Unavailable (503)
```json
{
  "detail": "Service not ready"
}
```

### B.2 Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "quadrant"],
      "msg": "value is not a valid enumeration member; permitted: 'strength', 'weakness', 'opportunity', 'threat'",
      "type": "value_error.enum"
    }
  ]
}
```

### B.3 Fallback Response (LLM Unavailable)
```json
{
  "success": true,
  "result": {
    "strengths": [
      {
        "id": "s1",
        "quadrant": "strength",
        "content": "Tenaga pendidik yang berdedikasi",
        "category": "sdm",
        "priority": 0.8,
        "data_source": "manual"
      }
    ],
    "summary": "Analisis SWOT perlu dilengkapi secara manual. Hubungi administrator AI platform.",
    "analysis_confidence": 0.0
  }
}
```

---

**Document End**
