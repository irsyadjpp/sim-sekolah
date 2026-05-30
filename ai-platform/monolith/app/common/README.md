# common/ Directory Guidelines

**Purpose**: This document establishes clear guidelines for what belongs in the `common/` directory to prevent it from becoming a "God folder" and to maintain clean architecture.

**Last Updated**: 2026-05-30  
**Status**: Active

---

## Core Principles

The `common/` directory is for **cross-cutting utilities ONLY**. It must never contain:
- Business logic
- Domain-specific code
- AI components
- Domain models or schemas

---

## What Belongs in common/

### 1. Infrastructure Components
**Location**: `common/infrastructure/`

**Purpose**: Low-level infrastructure utilities used across all services

**Examples**:
- gRPC channel management (`infrastructure/grpc/`)
- Messaging/queue utilities (`infrastructure/messaging/`)
- Database connection pooling
- Cache management
- HTTP client utilities

**Criteria**:
- Pure infrastructure code with no business logic
- Used by 3+ domains/services
- No domain-specific knowledge

---

### 2. Logging & Observability
**Location**: `common/logging/`, `common/observability/`, `common/telemetry/`

**Purpose**: Cross-cutting logging, metrics, tracing, and monitoring

**Examples**:
- Logger configuration and formatters
- Metrics collectors
- Distributed tracing utilities
- Health check endpoints
- Performance monitoring

**Criteria**:
- Pure observability code
- No business logic embedded
- Used across all services

---

### 3. Configuration Management
**Location**: `common/config/`

**Purpose**: Application configuration and settings

**Examples**:
- Settings classes (Pydantic models)
- Environment variable parsing
- Configuration validation
- Secret management utilities

**Criteria**:
- Pure configuration code
- No business rules
- Used across all services

---

### 4. Security & Authentication
**Location**: `common/security/`

**Purpose**: Cross-cutting security utilities

**Examples**:
- JWT token handling
- Encryption/decryption utilities
- Authentication helpers
- Authorization utilities (generic)
- Security headers

**Criteria**:
- Generic security utilities only
- No domain-specific authorization rules
- No business logic

---

### 5. HTTP Middleware
**Location**: `common/middleware/`

**Purpose**: HTTP middleware for web frameworks

**Examples**:
- Authentication middleware
- CORS middleware
- Error handling middleware
- Logging middleware
- Rate limiting middleware

**Criteria**:
- Generic HTTP middleware
- No business logic
- Framework-agnostic where possible

---

### 6. Exception Handling
**Location**: `common/exceptions/`

**Purpose**: Base exception classes and common error handling

**Examples**:
- Base exception classes
- Common error types (ValidationError, NotFoundError, etc.)
- Error response formatting

**Criteria**:
- Generic exception classes only
- No domain-specific exceptions
- No business logic

---

### 7. Common Schemas
**Location**: `common/schemas/`

**Purpose**: Generic data schemas and models

**Examples**:
- Pagination schemas
- Common response formats
- Generic request/response models
- Standard error schemas

**Criteria**:
- Generic schemas only
- No domain-specific models
- Used across multiple domains

---

### 8. Event Definitions (Base)
**Location**: `common/events/`

**Purpose**: Base event classes and common event infrastructure

**Examples**:
- Base event classes (BaseEvent, EventType enums)
- Event metadata structures
- Event serialization/deserialization

**Criteria**:
- Base event infrastructure only
- Domain-specific events go in their respective domains
- No business logic

---

### 9. Utility Functions
**Location**: `common/utils/`

**Purpose**: Pure utility functions with no business logic

**Examples**:
- Date/time formatting
- String manipulation utilities
- File I/O helpers
- Validation helpers (generic)
- Data transformation utilities

**Criteria**:
- Pure functions with no side effects
- No business logic
- Used across multiple domains

---

## What Does NOT Belong in common/

### ❌ Business Logic
**Examples**:
- Curriculum validation logic
- Assessment generation logic
- Learning progress calculation
- Character development tracking

**Where it belongs**: Respective domain bounded contexts

---

### ❌ Domain-Specific Code
**Examples**:
- Kurikulum Merdeka-specific logic
- Profil Pelajar Pancasila assessment
- Teacher workflow logic
- Student dashboard logic

**Where it belongs**: Respective domain bounded contexts

---

### ❌ AI Components
**Examples**:
- LLM providers
- Embedding models
- AI agents
- Prompt templates
- Reranking logic

**Where it belongs**: `ai_core/` bounded context

---

### ❌ Domain Models
**Examples**:
- Curriculum models
- Assessment models
- Student models
- Teacher models

**Where it belongs**: Respective domain bounded contexts

---

### ❌ Domain Events
**Examples**:
- DocumentUploaded event
- CurriculumCreated event
- AssessmentCompleted event

**Where it belongs**: Respective domain bounded contexts under `events/`

---

## Approval Process for Adding to common/

### Step 1: Self-Assessment
Before adding code to `common/`, ask:
1. Is this cross-cutting infrastructure/utility?
2. Is it used by 3+ domains/services?
3. Does it contain any business logic?
4. Is it domain-specific?
5. Is it an AI component?

If answer to 3, 4, or 5 is "yes", it does NOT belong in common/.

### Step 2: Team Review
All additions to `common/` require:
- Code review by at least 2 senior engineers
- Architecture review if adding new subdirectory
- Documentation update

### Step 3: Documentation
All additions must include:
- Purpose statement
- Usage examples
- Criteria for why it belongs in common/
- Maintenance guidelines

---

## Regular Audit Schedule

### Monthly Audits
- Review all files in `common/`
- Identify any code that should be moved to domains
- Remove unused code
- Update documentation

### Quarterly Deep Dive
- Comprehensive review of `common/` structure
- Identify potential refactoring opportunities
- Assess if any components should be extracted to separate packages
- Update guidelines based on learnings

---

## Automated Checks

### Pre-Commit Hooks
- Check for business logic in `common/`
- Validate that new files have documentation
- Ensure imports don't create circular dependencies

### CI/CD Pipeline
- Run automated tests for all `common/` code
- Check for code coverage (target: 90%+)
- Validate no domain-specific imports in `common/`

---

## Governance

### Code Review Enforcement
- All PRs adding to `common/` require architecture review
- PR template includes checklist for common/ additions
- Blocking criteria if guidelines not followed

### Team Education
- Onboarding includes common/ guidelines training
- Quarterly refresher sessions
- Examples of good vs bad common/ code

### Ownership
- Architecture team owns `common/` directory
- Domain teams can propose additions
- Final approval by architecture team

---

## Migration Path

If you find code in `common/` that shouldn't be there:

1. Identify the appropriate domain
2. Create issue for migration
3. Update imports in consuming code
4. Move code to domain
5. Remove from `common/`
6. Update documentation
7. Notify team of breaking changes

---

## Examples

### ✅ Good: Common Utility
```python
# common/utils/date_helpers.py
from datetime import datetime, timedelta

def format_date_iso(date: datetime) -> str:
    """Format datetime to ISO 8601 string."""
    return date.isoformat()

def add_days(date: datetime, days: int) -> datetime:
    """Add days to datetime."""
    return date + timedelta(days)
```
**Why**: Pure utility function, no business logic, used across domains

---

### ❌ Bad: Business Logic in Common
```python
# common/utils/curriculum_validator.py
def validate_curriculum_alignment(cp: Curriculum) -> bool:
    """Validate CP aligns with Kurikulum Merdeka."""
    # Business logic for curriculum validation
    return check_national_standards(cp)
```
**Why**: Contains business logic, domain-specific, belongs in `curriculum-domain/`

---

### ✅ Good: Common Middleware
```python
# common/middleware/logging.py
from fastapi import Request
import logging

async def log_requests(request: Request, call_next):
    """Log all HTTP requests."""
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    return response
```
**Why**: Generic HTTP middleware, no business logic

---

### ❌ Bad: Domain-Specific Middleware
```python
# common/middleware/teacher_auth.py
async def validate_teacher_access(request: Request):
    """Validate teacher has access to curriculum."""
    # Domain-specific authorization logic
    if not is_teacher(request.user):
        raise Forbidden()
```
**Why**: Domain-specific authorization, belongs in `teacher-domain/`

---

## Contact & Questions

**Architecture Team**: architecture-team@example.com  
**Common/ Owners**: See CODEOWNERS file  
**Issue Tracker**: Create issue with label `common/`

---

## Version History

- **2026-05-30**: Initial guidelines established as part of Phase 3 cleanup
- **Future**: Quarterly reviews and updates
