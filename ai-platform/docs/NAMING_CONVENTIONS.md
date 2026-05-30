# Naming Conventions

**Purpose**: This document establishes clear naming conventions for all components in the AI Platform to ensure consistency, readability, and maintainability.

**Last Updated**: 2026-05-30  
**Status**: Active

---

## Core Principles

1. **Consistency**: Use consistent naming patterns across the codebase
2. **Clarity**: Names should clearly indicate purpose and functionality
3. **Domain-Driven**: Names should reflect domain language and bounded contexts
4. **Simplicity**: Avoid unnecessary complexity in naming
5. **Pythonic**: Follow PEP 8 guidelines for Python code

---

## General Naming Rules

### File Names
- Use **snake_case** for all Python files
- Use **kebab-case** for configuration files (except Python)
- Use **PascalCase** for class files in other languages

**Examples**:
- ✅ `workflow_orchestrator.py`
- ✅ `assessment-integration.yaml`
- ✅ `WorkflowOrchestrator.ts`

### Directory Names
- Use **snake_case** for directories
- Domain directories should end with `-domain` suffix

**Examples**:
- ✅ `teacher-domain/`
- ✅ `student-domain/`
- ✅ `curriculum-domain/`

### Variable Names
- Use **snake_case** for variables and functions
- Use **PascalCase** for classes
- Use **UPPER_CASE** for constants

**Examples**:
- ✅ `workflow_id`
- ✅ `get_workflow_definition()`
- ✅ `WorkflowOrchestrator`
- ✅ `MAX_RETRIES`

---

## Component-Specific Conventions

### Services

**Pattern**: `{domain}_{service_type}_service`

**Rules**:
- Domain prefix indicates bounded context
- Service type indicates primary function
- Always end with `_service` suffix
- Use descriptive, domain-specific names

**Examples**:
- ✅ `teacher_workflow_service`
- ✅ `student_progress_service`
- ✅ `curriculum_management_service`
- ✅ `assessment_generation_service`

**Anti-patterns**:
- ❌ `workflow_service` (missing domain)
- ❌ `teacherService` (not snake_case)
- ❌ `teacher_workflow` (missing _service suffix)

---

### Engines

**Pattern**: `{domain}_{functionality}_engine`

**Rules**:
- Domain prefix indicates bounded context
- Functionality indicates what the engine processes
- Always end with `_engine` suffix
- Use for AI/ML processing, computation, or transformation

**Examples**:
- ✅ `adaptive_learning_engine`
- ✅ `assessment_engine`
- ✅ `curriculum_engine`
- ✅ `learning_graph_engine`
- ✅ `semantic_enrichment_engine`

**Anti-patterns**:
- ❌ `learning_engine` (too generic)
- ❌ `adaptiveEngine` (not snake_case)
- ❌ `adaptive_learning` (missing _engine suffix)

---

### Pipelines

**Pattern**: `{domain}_{process}_pipeline`

**Rules**:
- Domain prefix indicates bounded context
- Process indicates what the pipeline handles
- Always end with `_pipeline` suffix
- Use for multi-step data processing workflows

**Examples**:
- ✅ `document_ingestion_pipeline`
- ✅ `content_processing_pipeline`
- ✅ `assessment_scoring_pipeline`
- ✅ `student_analytics_pipeline`

**Anti-patterns**:
- ❌ `ingestion_pipeline` (missing domain)
- ❌ `documentPipeline` (not snake_case)
- ❌ `document_ingestion` (missing _pipeline suffix)

---

### Providers

**Pattern**: `{resource}_{provider}_provider`

**Rules**:
- Resource indicates what is being provided
- Provider indicates the source or type
- Always end with `_provider` suffix
- Use for external service integrations, AI models, or data sources

**Examples**:
- ✅ `llm_openai_provider`
- ✅ `embedding_qdrant_provider`
- ✅ `storage_seaweed_provider`
- ✅ `auth_jwt_provider`
- ✅ `cache_redis_provider`

**Anti-patterns**:
- ❌ `openai_provider` (missing resource)
- ❌ `llmProvider` (not snake_case)
- ❌ `llm_openai` (missing _provider suffix)

---

### Repositories

**Pattern**: `{entity}_repository`

**Rules**:
- Entity indicates what data is being managed
- Always end with `_repository` suffix
- Use for data access layer
- Follow Domain-Driven Design repository pattern

**Examples**:
- ✅ `student_repository`
- ✅ `teacher_repository`
- ✅ `curriculum_repository`
- ✅ `assessment_repository`
- ✅ `learning_objective_repository`

**Anti-patterns**:
- ❌ `student_repo` (use full word)
- ❌ `StudentRepository` (not snake_case)
- ❌ `student_data_repository` (redundant "data")

---

## Domain-Specific Conventions

### Teacher Domain

**Services**:
- `teacher_workflow_service`
- `teacher_planning_service`
- `teacher_assessment_service`

**Engines**:
- `pedagogy_engine`
- `recommendation_engine`

**Pipelines**:
- `lesson_planning_pipeline`
- `assessment_creation_pipeline`

---

### Student Domain

**Services**:
- `student_progress_service`
- `student_reflection_service`
- `student_analytics_service`

**Engines**:
- `adaptive_learning_engine`
- `learning_progression_engine`

**Pipelines**:
- `student_analytics_pipeline`
- `reflection_processing_pipeline`

---

### Curriculum Domain

**Services**:
- `curriculum_management_service`
- `standards_alignment_service`

**Engines**:
- `curriculum_engine`
- `ontology_validation_engine`

**Pipelines**:
- `curriculum_import_pipeline`
- `standards_alignment_pipeline`

---

### Assessment Domain

**Services**:
- `assessment_generation_service`
- `assessment_scoring_service`
- `rubric_service`

**Engines**:
- `assessment_engine`
- `reranking_engine`

**Pipelines**:
- `assessment_scoring_pipeline`
- `rubric_generation_pipeline`

---

## AI Core Domain

**Services**:
- `llm_service`
- `embedding_service`
- `retrieval_service`

**Engines**:
- `semantic_enrichment_engine`
- `strategic_analysis_engine`

**Pipelines**:
- `document_processing_pipeline`
- `rag_pipeline`

**Providers**:
- `llm_openai_provider`
- `llm_anthropic_provider`
- `embedding_openai_provider`
- `embedding_qdrant_provider`

---

## Database Naming Conventions

### Tables
- Use **snake_case**
- Use plural form for table names
- Prefix with domain if needed for clarity

**Examples**:
- ✅ `students`
- ✅ `teachers`
- ✅ `learning_objectives`
- ✅ `assessment_results`

### Columns
- Use **snake_case**
- Use descriptive names
- Foreign keys should reference table name with `_id` suffix

**Examples**:
- ✅ `student_id`
- ✅ `teacher_id`
- ✅ `created_at`
- ✅ `updated_at`

---

## API Endpoint Conventions

### REST API
- Use **kebab-case** for URL paths
- Use plural nouns for collections
- Use HTTP verbs appropriately

**Examples**:
- ✅ `GET /api/students`
- ✅ `POST /api/students`
- ✅ `GET /api/students/{student_id}`
- ✅ `PUT /api/students/{student_id}`
- ✅ `DELETE /api/students/{student_id}`

### gRPC Services
- Use **PascalCase** for service names
- Use **PascalCase** for method names
- Use **snake_case** for message fields

**Examples**:
- ✅ `service TeacherService`
- ✅ `rpc GetStudent(StudentRequest) returns (StudentResponse)`
- ✅ `message StudentRequest { string student_id = 1; }`

---

## Configuration Naming Conventions

### Environment Variables
- Use **UPPER_CASE**
- Use underscores to separate words
- Prefix with application or domain name

**Examples**:
- ✅ `AI_PLATFORM_DATABASE_URL`
- ✅ `TEACHER_SERVICE_PORT`
- ✅ `STUDENT_DASHBOARD_ENABLED`

### Configuration Keys
- Use **snake_case**
- Use hierarchical structure with dots

**Examples**:
- ✅ `database.url`
- ✅ `teacher_service.port`
- ✅ `student_dashboard.features.enabled`

---

## Test Naming Conventions

### Test Files
- Use **snake_case**
- End with `_test.py` suffix
- Name should indicate what is being tested

**Examples**:
- ✅ `workflow_orchestrator_test.py`
- ✅ `assessment_integration_test.py`
- ✅ `student_dashboard_test.py`

### Test Functions
- Use **snake_case**
- Start with `test_` prefix
- Name should indicate scenario being tested

**Examples**:
- ✅ `test_workflow_orchestrator_starts_workflow()`
- ✅ `test_assessment_integration_generates_rubric()`
- ✅ `test_student_dashboard_shows_progress()`

---

## Migration Plan

### Step 1: Audit Current Names
- List all services, engines, pipelines, providers, repositories
- Identify violations of naming conventions
- Prioritize high-impact components

### Step 2: Rename Components
- Update file names
- Update class names
- Update imports
- Update configuration

### Step 3: Update References
- Update API endpoints
- Update database references
- Update documentation
- Update tests

### Step 4: Verify
- Run all tests
- Verify no broken imports
- Verify functionality preserved

---

## Enforcement

### Code Review Checklist
- [ ] Service names follow `{domain}_{service_type}_service` pattern
- [ ] Engine names follow `{domain}_{functionality}_engine` pattern
- [ ] Pipeline names follow `{domain}_{process}_pipeline` pattern
- [ ] Provider names follow `{resource}_{provider}_provider` pattern
- [ ] Repository names follow `{entity}_repository` pattern
- [ ] File names use snake_case
- [ ] Variable names use snake_case
- [ ] Class names use PascalCase
- [ ] Constants use UPPER_CASE

### Automated Checks
- Pre-commit hooks for naming convention validation
- CI/CD pipeline checks for naming violations
- Linting rules for naming conventions

---

## Examples of Correct Naming

### Complete Example: Teacher Workflow Service

**File**: `teacher-domain/teacher_workflow_service/workflow_orchestrator.py`

```python
class WorkflowOrchestrator:
    """Orchestrates teacher workflows"""
    
    def __init__(self):
        self.workflow_service = TeacherWorkflowService()
        self.assessment_engine = AssessmentEngine()
        self.lesson_planning_pipeline = LessonPlanningPipeline()
    
    def start_workflow(self, workflow_type: str) -> dict:
        """Start a teacher workflow"""
        pass
```

**File**: `teacher-domain/teacher_workflow_service/__init__.py`

```python
from .workflow_orchestrator import WorkflowOrchestrator
from .workflow_intelligence import WorkflowIntelligenceService
from .workflow_analytics import WorkflowAnalyticsService
```

---

## Contact & Questions

**Architecture Team**: architecture-team@example.com  
**Naming Convention Owners**: See CODEOWNERS file  
**Issue Tracker**: Create issue with label `naming-convention`

---

## Version History

- **2026-05-30**: Initial naming conventions established as part of Phase 3 cleanup
- **Future**: Quarterly reviews and updates based on team feedback
