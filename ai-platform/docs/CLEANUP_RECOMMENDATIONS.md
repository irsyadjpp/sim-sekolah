# AI Platform Cleanup Recommendations
## Folder and File Analysis

**Date:** 2026-05-29  
**Purpose:** Analyze ai-platform folders (excluding monolith) and provide cleanup recommendations

---

## Current Structure Analysis

### ✅ **KEEP - Essential Folders**

#### **Configuration Files**
- `.env` - Environment configuration (keep)
- `.env.example` - Environment template (keep)
- `.gitignore` - Git ignore rules (keep)
- `.python-version` - Python version specification (keep)
- `pyproject.toml` - Python project configuration (keep)
- `requirements.txt` - Python dependencies (keep)
- `Makefile` - Build automation (keep)
- `docker-compose.yml` - Docker compose configuration (keep)

#### **Documentation**
- `README.md` - Project documentation (keep)
- `ARCHITECTURE_REVIEW.md` - Architecture review document (keep)
- `PRODUCTION_READINESS_PLAN.md` - Production readiness plan (keep)
- `docs/` - Complete documentation (31 items) - **KEEP**
  - API documentation
  - Architecture documentation
  - Deployment guides
  - User guides

#### **Infrastructure**
- `infra/` - Infrastructure configurations (37 items) - **KEEP**
  - Docker configurations
  - Kubernetes configurations
  - Monitoring setup (Grafana, Prometheus)
  - Infrastructure as code

#### **Shared Code**
- `shared/` - Shared utilities (50 items) - **KEEP**
  - Common configurations
  - Shared schemas
  - Utilities used across services
  - Middleware components

#### **Data & Knowledge**
- `knowledge/` - Knowledge base (9 items) - **KEEP**
  - Curriculum data (asesmen, buku_guru, buku_siswa, etc.)
  - MinIO migration scripts
  - Metadata templates
  - Educational content

#### **Development Tools**
- `scripts/` - Automation scripts (41 items) - **KEEP**
  - Deployment scripts
  - Maintenance scripts
  - Backup/recovery scripts
  - Testing scripts

- `tests/` - Test files (23 items) - **KEEP**
  - Unit tests
  - Integration tests
  - Test fixtures

#### **SDK & Integration**
- `sdk/` - Client SDKs (24 items) - **KEEP**
  - Python SDK
  - Go SDK
  - Client libraries for external integration

#### **Data Processing**
- `pipelines/` - Data pipelines (22 items) - **KEEP**
  - Data ingestion pipelines
  - Embedding pipelines
  - Indexing pipelines
  - Prefect workflow configurations

#### **Storage**
- `storage/` - Storage configurations (27 items) - **KEEP**
  - Database migrations
  - Storage abstractions
  - OCR configurations
  - Data fixtures

#### **Models**
- `models/` - ML models (5 items) - **KEEP**
  - Trained models
  - Model configurations
  - Model utilities

#### **Workers**
- `workers/` - Background workers (1 item) - **KEEP**
  - Background job processing
  - Async task handlers

---

### ⚠️ **MOVE TO LEGACY - Old Microservices Artifacts**

#### **Kubernetes Deployments**
- `k8s/` - Kubernetes deployments (7 items) - **MOVE TO LEGACY**
  - `adaptive-learning-engine-deployment.yaml`
  - `assessment-engine-deployment.yaml`
  - `curriculum-engine-deployment.yaml`
  - `learning-graph-engine-deployment.yaml`
  - `learning-progression-engine-deployment.yaml`
  - `pedagogy-engine-deployment.yaml`
  - `recommendation-engine-deployment.yaml`
  
  **Reason:** These are old microservice deployments for individual engines. Since we've moved to monolith architecture, these are no longer needed but should be preserved for reference.

#### **Protocol Buffers**
- `proto/` - gRPC protocol definitions (18 items) - **MOVE TO LEGACY**
  - `audit_service.proto`
  - `embedding_service.proto`
  - `generation_service.proto`
  - `parser_service.proto`
  - `retrieval_service.proto`
  - `semantic_chunk_service.proto`
  - And other service proto files
  
  **Reason:** gRPC definitions for old microservices. Monolith uses REST API, so these are no longer needed but should be preserved for reference.

---

### ❌ **DELETE - Unnecessary Items**

#### **Empty Directories**
- `notebooks/` - Jupyter notebooks (0 items) - **DELETE**
  - Empty directory, no notebooks present
  
- `venv/` - Virtual environment (0 items) - **DELETE**
  - Empty directory, virtual environment should be created locally or via Docker

---

### 🔄 **REORGANIZE - Better Organization**

#### **Sample Files**
- `sample/` - Sample PDF files (4 items) - **MOVE TO knowledge/sample/**
  - `BUKUSAKUAIMURID.pdf`
  - `Matematika-BG-KLS-IV.pdf`
  - `bkb10.pdf`
  - `siklus-air.pdf`
  
  **Reason:** These are sample educational documents that belong in the knowledge base structure, not as a separate folder at root level.

---

## Recommended Actions

### Priority 1: Immediate Cleanup
1. **Delete empty directories:**
   ```bash
   rm -rf notebooks/ venv/
   ```

2. **Move old microservices artifacts to legacy:**
   ```bash
   mv k8s/ legacy/k8s_microservices_deployments/
   mv proto/ legacy/proto_microservices_definitions/
   ```

3. **Reorganize sample files:**
   ```bash
   mkdir -p knowledge/sample
   mv sample/* knowledge/sample/
   rmdir sample/
   ```

### Priority 2: Documentation Updates
1. Update `README.md` to reflect new structure
2. Update deployment documentation to reference monolith instead of microservices
3. Create migration guide for future reference

### Priority 3: Infrastructure Updates
1. Review `infra/` configurations for monolith compatibility
2. Update monitoring configurations for monolith architecture
3. Clean up any microservice-specific infrastructure code

---

## Final Recommended Structure

```
ai-platform/
├── Configuration Files
│   ├── .env, .env.example
│   ├── .gitignore, .python-version
│   ├── pyproject.toml, requirements.txt
│   ├── Makefile, docker-compose.yml
│
├── Documentation
│   ├── README.md
│   ├── ARCHITECTURE_REVIEW.md
│   ├── PRODUCTION_READINESS_PLAN.md
│   └── docs/ (complete documentation)
│
├── Main Application
│   └── monolith/ (clean modular monolith)
│
├── Legacy Code
│   └── legacy/
│       ├── services/ (old microservices)
│       ├── monolith_app_backup/ (removed nested structure)
│       ├── k8s_microservices_deployments/ (old K8s configs)
│       └── proto_microservices_definitions/ (old gRPC defs)
│
├── Infrastructure
│   ├── infra/ (infrastructure configurations)
│   └── scripts/ (automation scripts)
│
├── Shared Code
│   └── shared/ (shared utilities and components)
│
├── Data & Knowledge
│   ├── knowledge/ (educational content and data)
│   │   └── sample/ (sample documents)
│   ├── storage/ (storage configurations)
│   └── models/ (ML models)
│
├── Development Tools
│   ├── pipelines/ (data processing pipelines)
│   ├── sdk/ (client SDKs)
│   ├── tests/ (test files)
│   └── workers/ (background workers)
│
└── GitHub
    └── .github/ (CI/CD workflows)
```

---

## Summary of Changes

### Files to Delete: 8 directories
- `notebooks/` (empty)
- `venv/` (empty)
- `scripts/deploy/` (empty)
- `workers/embedding_workers/` (empty)
- `workers/cleanup_workers/` (empty)
- `monolith/app/models/` (empty)
- `monolith/app/utils/` (empty)
- `tests/e2e/scenarios/` (empty)
- `tests/integration/contracts/` (empty)

### Files to Move to Legacy: 2 directories
- `k8s/` → `legacy/k8s_microservices_deployments/`
- `proto/` → `legacy/proto_microservices_definitions/`

### Files to Reorganize: 1 directory
- `sample/` → `knowledge/sample/`

### Total Impact: 11 directories affected

---

## Benefits of Cleanup

1. **Clearer Structure:** Easier to understand and navigate
2. **Reduced Confusion:** No ambiguity about what code is active
3. **Better Maintenance:** Less clutter to maintain
4. **Improved Onboarding:** New developers can understand structure faster
5. **Cleaner Git History:** Less noise in version control
6. **Focused Development:** Clear separation between active and legacy code

---

## Post-Cleanup Validation

After cleanup, verify:
- [ ] All tests still pass
- [ ] Documentation is updated
- [ ] CI/CD pipelines work correctly
- [ ] Development environment setup works
- [ ] No broken imports or references
- [ ] Docker builds successfully
- [ ] Application starts correctly

---

**Recommendation Status:** ✅ **READY FOR IMPLEMENTATION**
