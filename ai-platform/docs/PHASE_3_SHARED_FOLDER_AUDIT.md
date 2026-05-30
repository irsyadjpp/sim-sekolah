# Phase 3: shared/ Folder Audit Report

**Date**: 2026-05-30  
**Action Item**: 3.4.1 - Audit and Decompose shared/ Folder  
**Status**: In Progress

---

## Executive Summary

The `shared/` folder at `ai-platform/shared/` contains cross-cutting utilities and infrastructure code that should be properly organized. This audit categorizes all contents and provides a migration plan to prevent it from becoming a "God folder".

---

## Current Structure

```
ai-platform/shared/
├── __init__.py
├── pyproject.toml
├── app_logging/              # Logging utilities
├── configs/                 # Configuration management
├── constants/               # (empty)
├── contracts/               # (empty)
├── enums/                   # (empty)
├── events/                  # Event definitions
├── exceptions/              # Custom exceptions
├── grpc/                    # gRPC utilities
│   ├── clients/
│   ├── generated/
│   ├── interceptors/
│   ├── proto/
│   └── python/
├── messaging/               # Messaging (RabbitMQ)
├── middleware/              # HTTP middleware
├── models/                  # (empty)
├── observability/           # Observability (metrics, tracing)
├── prompts/                 # (empty)
├── schemas/                 # Common schemas
├── security/                # Security utilities
├── telemetry/               # Telemetry (health, performance)
└── utils/                   # General utilities
```

---

## Categorization Analysis

### Category 1: True Cross-Cutting Utilities (Keep in common/)
These are genuine cross-cutting concerns used across all domains:

- **app_logging/** - Centralized logging configuration
- **configs/** - Application settings and configuration
- **exceptions/** - Custom exception classes
- **middleware/** - HTTP middleware (auth, CORS, error, logging)
- **observability/** - Metrics, tracing, logging
- **schemas/** - Common data schemas
- **security/** - Authentication, authorization, encryption, JWT
- **telemetry/** - Health checks, performance monitoring
- **utils/** - General utility functions

### Category 2: Infrastructure/Communication (Keep in common/)
These are infrastructure components used across services:

- **grpc/** - gRPC channel management, clients, interceptors
- **messaging/** - RabbitMQ consumer, DLQ config, message definitions

### Category 3: Domain-Specific Events (Move to appropriate domains)
These should be moved to domain-specific locations:

- **events/** - Event definitions should be in each domain that owns them
  - `document_events.py` → Move to appropriate domain (e.g., curriculum-domain or new document-domain)

### Category 4: Empty Directories (Remove)
These are empty and should be removed:

- **constants/** - Empty
- **contracts/** - Empty
- **enums/** - Empty
- **models/** - Empty
- **prompts/** - Empty

---

## Migration Plan

### Step 1: Create common/ Directory Structure
```
ai-platform/monolith/app/common/
├── __init__.py
├── logging/                 # From shared/app_logging
├── config/                  # From shared/configs
├── exceptions/              # From shared/exceptions
├── middleware/              # From shared/middleware
├── observability/           # From shared/observability
├── schemas/                 # From shared/schemas
├── security/                # From shared/security
├── telemetry/               # From shared/telemetry
├── infrastructure/          # From shared/grpc and shared/messaging
│   ├── grpc/
│   └── messaging/
└── utils/                   # From shared/utils
```

### Step 2: Move Cross-Cutting Utilities
- Move `shared/app_logging/` → `monolith/app/common/logging/`
- Move `shared/configs/` → `monolith/app/common/config/`
- Move `shared/exceptions/` → `monolith/app/common/exceptions/`
- Move `shared/middleware/` → `monolith/app/common/middleware/`
- Move `shared/observability/` → `monolith/app/common/observability/`
- Move `shared/schemas/` → `monolith/app/common/schemas/`
- Move `shared/security/` → `monolith/app/common/security/`
- Move `shared/telemetry/` → `monolith/app/common/telemetry/`
- Move `shared/utils/` → `monolith/app/common/utils/`

### Step 3: Move Infrastructure Components
- Move `shared/grpc/` → `monolith/app/common/infrastructure/grpc/`
- Move `shared/messaging/` → `monolith/app/common/infrastructure/messaging/`

### Step 4: Move Domain-Specific Events
- Move `shared/events/document_events.py` → `monolith/app/curriculum-domain/events/` (or appropriate domain)
- Keep `shared/events/base.py` in `monolith/app/common/events/` as base event definitions

### Step 5: Remove Empty Directories
- Remove `shared/constants/`
- Remove `shared/contracts/`
- Remove `shared/enums/`
- Remove `shared/models/`
- Remove `shared/prompts/`

### Step 6: Update All Imports
- Update imports across the codebase from `shared.*` to `common.*`
- Update imports from `shared.events.*` to appropriate domain events

### Step 7: Delete shared/ Folder
- Verify all code moved
- Update all references
- Remove `ai-platform/shared/` directory

---

## Import Impact Analysis

### Files Using shared/ Imports
Need to search for all files importing from `shared`:
```bash
grep -r "from shared" ai-platform/
grep -r "import shared" ai-platform/
```

### Expected Import Changes
- `from shared.app_logging.logger import setup_logging` → `from common.logging.logger import setup_logging`
- `from shared.configs.settings import settings` → `from common.config.settings import settings`
- `from shared.exceptions.exceptions import BaseException` → `from common.exceptions.exceptions import BaseException`
- `from shared.grpc.channel import create_channel` → `from common.infrastructure.grpc.channel import create_channel`
- `from shared.events.base import BaseEvent` → `from common.events.base import BaseEvent`
- `from shared.events.document_events import DocumentEvent` → `from curriculum_domain.events.document_events import DocumentEvent`

---

## Risk Assessment

### Low Risk
- Moving logging, config, exceptions, middleware, observability, schemas, security, telemetry, utils
- These are pure utilities with no business logic

### Medium Risk
- Moving grpc and messaging infrastructure
- Need to ensure all service connections still work

### High Risk
- Moving events to domain-specific locations
- Need to ensure event-driven communication still works
- Need to identify which domain owns each event type

---

## Success Criteria

✅ All cross-cutting utilities moved to `monolith/app/common/`  
✅ Infrastructure components moved to `monolith/app/common/infrastructure/`  
✅ Domain-specific events moved to appropriate domains  
✅ Empty directories removed  
✅ All imports updated across codebase  
✅ `shared/` folder completely removed  
✅ No functionality lost  
✅ All tests passing  

---

## Next Steps

1. Create `monolith/app/common/` directory structure
2. Begin migration with low-risk components (logging, config, exceptions)
3. Move infrastructure components (grpc, messaging)
4. Move domain-specific events after identifying owning domains
5. Update all imports
6. Remove empty directories
7. Delete shared/ folder
8. Run comprehensive tests
9. Update documentation

---

## Timeline Estimate

- **Step 1-2**: 1 day (Create structure, move low-risk components)
- **Step 3**: 1 day (Move infrastructure components)
- **Step 4**: 1 day (Move events, identify domains)
- **Step 5-6**: 1 day (Remove empty dirs, update imports)
- **Step 7-9**: 1 day (Delete shared/, test, document)

**Total**: 5 days
