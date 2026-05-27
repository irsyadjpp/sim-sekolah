# AI Platform — Implementation Plan (Outside `services/`)

> Status: Draft  
> Scope: What the `ai-platform/` root directory should contain, how each folder is used, and the phased rollout to get there.

---

## 1. Current Problem

The `ai-platform/` folder today is a mix of:
- **Over-declared domains**: `educational-intelligence/`, `ai-agents/`, `hallucination-guard/`, `educational-ontology/`, `retrieval-enhancement/`, `semantic-enrichment/` — most are empty directory trees that duplicate concepts already owned by the 13 microservices under `services/`.
- **Scattered infrastructure**: `infra/`, `k8s/`, `deployment/` each contain partial configs; no single source of truth for a local dev stack.
- **Missing platform contracts**: `shared/` exists but has no published package or versioned SDK; the Go backend and Python services consume definitions independently.
- **No clear boundary**: It is unclear what lives "in the platform" vs "in a service."

---

## 2. Design Principle

> **The platform root owns cross-cutting concerns. A service owns a bounded capability.**

If a piece of code is needed by **two or more services**, or by **the backend + a service**, it belongs in the platform root. Otherwise it stays inside the service that owns it.

---

## 3. Target Directory Structure

```text
ai-platform/
│
├── README.md                          # Platform overview, quickstart, architecture diagram
├── Makefile                           # One entrypoint: make dev, make test, make deploy
├── docker-compose.yml                 # Full local stack (infra + all services)
├── pyproject.toml                     # Python workspace (hatch/uv monorepo)
├── requirements.txt                   # Pinned production deps (generated)
├── .env.example                       # Required env vars for local development
│
├── proto/                             # Canonical proto definitions (source of truth)
│   ├── common/                        # Shared enums, types, errors
│   ├── embedding_service.proto
│   ├── generation_service.proto
│   ├── ... (all 13+ service contracts)
│   └── buf.yaml / buf.gen.yaml        # Buf workspace for lint + codegen
│
├── shared/                            # Published platform packages (cross-service)
│   ├── grpc/                          # Generated stubs + channel helpers
│   ├── schemas/                       # Pydantic / JSON-Schema contracts
│   ├── events/                        # Async event envelopes (RabbitMQ topics)
│   ├── security/                      # JWT validation, RBAC, audit context
│   ├── observability/                 # Shared logging, metrics, tracing helpers
│   └── pyproject.toml                 # pip-installable: pip install -e shared/
│
├── sdk/                               # Client SDKs for consumers
│   ├── python/                        # simsekolah-ai  (PyPI-ready)
│   └── go/                            # Go module (for backend integration)
│
├── services/                          # 13 microservices (already exists)
│   ├── gateway-service/
│   ├── parser-service/
│   ├── ... etc
│
├── pipelines/                         # Orchestrated processing DAGs
│   ├── ingestion/                     # Document → Parsed → Chunked → Embedded
│   ├── enrichment/                    # Metadata tagging (difficulty, taxonomy, competency)
│   ├── indexing/                      # Chunk → Vector store + Graph edges
│   └── generation/                    # Retrieval → Context building → LLM → Guard
│   # Each pipeline is a Prefect/Dagster/Airflow flow definition + unit tests
│
├── workers/                           # Background job templates + shared task code
│   ├── document_workers/
│   ├── embedding_workers/
│   └── cleanup_workers/
│   # Note: actual worker deployments live inside services; this is shared libs
│
├── knowledge/                         # Domain knowledge base (raw assets)
│   ├── cp/                            # Capaian Pembelajaran (JSON/CSV/MD)
│   ├── atp/                           # Alur Tujuan Pembelajaran
│   ├── buku_guru/
│   ├── buku_siswa/
│   ├── modul_ajar/
│   ├── asesmen/
│   ├── p5/
│   ├── media/
│   └── ontology/                      # RDF/OWL concept graphs for curriculum
│   # Stored as versioned data, not code. Services load them at runtime or ingest them.
│
├── models/                            # Model cards, configs, registry pointers
│   ├── embeddings/
│   ├── rerankers/
│   ├── classifiers/
│   ├── vision/
│   ├── ocr/
│   └── moderation/
│   # Each folder contains: config.yaml, README card, download script, benchmark results
│   # Actual weights live in S3/MinIO/Model Registry; never in git.
│
├── storage/                           # Storage layer abstractions (not data dumps)
│   ├── abstractions/                  # Unified storage interface (S3/MinIO, VectorDB, GraphDB)
│   ├── migrations/                    # Qdrant collection schemas, PG schema migrations
│   └── fixtures/                      # Small test datasets used in CI
│
├── infra/                             # Infrastructure-as-Code (local + cloud)
│   ├── docker/                        # Base images, Dockerfiles for services
│   ├── compose/                       # Per-environment compose overrides
│   │   ├── dev/
│   │   ├── staging/
│   │   └── production/
│   ├── kubernetes/                    # Helm charts or raw manifests
│   ├── terraform/                     # Cloud infra (optional)
│   └── scripts/                       # infra bootstrap, teardown, health checks
│
├── tests/                             # Platform-level integration + E2E tests
│   ├── integration/                   # Service-to-service contract tests
│   ├── e2e/                           # End-to-end RAG + generation flows
│   ├── load/                          # K6 / Locust load tests
│   └── fixtures/                      # Shared test documents, expected outputs
│
├── notebooks/                         # Research & experimentation (not production code)
│   ├── experiments/
│   ├── benchmarks/
│   └── model-benchmarks/
│
├── scripts/                           # Automation & ops scripts
│   ├── bootstrap/                     # One-command local setup
│   ├── ingest/                        # Bulk knowledge ingestion CLI
│   ├── benchmark/                     # Run benchmark suites
│   ├── deploy/                        # Deployment helpers
│   ├── maintenance/                   # Reindex, backup, cleanup
│   └── migrate/                       # DB/collection migration runners
│
└── docs/                              # Living documentation
    ├── architecture/                  # C4 diagrams, ADRs
    ├── runbooks/                    # Incident response, on-call playbooks
    ├── api/                         # OpenAPI / proto docs (generated)
    └── deployment/                  # Environment-specific deployment guides
```

---

## 4. What Gets Removed or Merged

| Current Folder | Action | Reason |
|---|---|---|
| `educational-intelligence/` | **Delete** | Each "engine" is a module inside `generation-service` or `gateway-service`. No standalone deployment. |
| `ai-agents/` | **Delete** | Agent logic lives in `gateway-service` (orchestration) and `generation-service` (LLM reasoning). |
| `hallucination-guard/` | **Delete** | Guardrails are a module inside `moderation-service` and `generation-service`. |
| `educational-observability/` | **Delete** | Observability code is in `monitoring-service` and `shared/observability/`. |
| `educational-ontology/` | **Merge into** `knowledge/ontology/` | Ontology files are data assets, not code. |
| `retrieval-enhancement/` | **Delete** | Rerankers live in `reranking-service`; retrieval logic in `retrieval-service`. |
| `semantic-enrichment/` | **Delete** | Enrichment is a pipeline stage and a module inside `metadata-service`. |
| `k8s/` | **Merge into** `infra/kubernetes/` | Single infra source of truth. |
| `deployment/` | **Merge into** `infra/` + `scripts/deploy/` | Avoid split-brain between `deployment/` and `infra/`. |
| `storage/raw/`, `storage/parsed/`, etc. | **Delete** | These are runtime data paths, not repository contents. Use `storage/abstractions/` and `storage/fixtures/` instead. |

---

## 5. Rollout Phases

### Phase 1 — Foundation (Week 1–2)
**Goal**: A single command brings up the entire local platform.

1. Merge `infra/`, `k8s/`, `deployment/` into a clean `infra/` tree.
2. Rewrite `docker-compose.yml` to be the single source of truth for local dev.
3. Add `Makefile` targets:
   - `make dev` → docker compose up (infra + services)
   - `make test` → run unit + integration tests
   - `make proto` → generate Go + Python stubs from `proto/`
4. Move all proto files into `proto/` with a `buf.yaml` workspace.
5. Set up `shared/` as an installable Python package (`pip install -e shared/`).

### Phase 2 — Contracts & SDK (Week 3–4)
**Goal**: Backend and services speak the same types.

1. Establish `proto/` as the single source of truth.
2. Generate stubs into:
   - `shared/grpc/python/` (for Python services)
   - `sdk/go/` (for Go backend)
3. Publish a thin Python SDK (`sdk/python/`) that wraps gRPC + auth + retry.
4. Refactor `backend/internal/ai/grpc/` to consume `sdk/go/` instead of hand-written stubs.

### Phase 3 — Pipelines & Workers (Week 5–6)
**Goal**: Document ingestion is an observable DAG, not ad-hoc scripts.

1. Implement the `ingestion` pipeline (document → parsed → chunked → embedded).
2. Move reusable worker task code into `workers/`.
3. Add Prefect/Dagster flow definitions in `pipelines/`.
4. Seed `knowledge/` with the first batch of CP, ATP, and Modul Ajar data.

### Phase 4 — Knowledge & Models (Week 7–8)
**Goal**: Curriculum knowledge is versioned and queryable.

1. Load `knowledge/` into the vector store and knowledge graph.
2. Add model cards in `models/` for every model used in production.
3. Create `storage/migrations/` for Qdrant collection schemas and PG migrations.

### Phase 5 — Observability & Hardening (Week 9–10)
**Goal**: The platform is debuggable and tested in CI.

1. Add integration tests in `tests/integration/` (contract tests between services).
2. Add E2E tests in `tests/e2e/` (full RAG → generation → guard flow).
3. Wire `shared/observability/` into every service.
4. Add load tests in `tests/load/`.

### Phase 6 — SDK & Integration (Week 11–12)
**Goal**: Backend and external consumers have official SDKs.

1. Move reusable code to `shared/` - Extract logging, telemetry, security, middleware from services.
2. Create Go SDK - Build Go SDK for backend integration.
3. Refactor backend gRPC - Update backend to use Go SDK instead of hand-written stubs.
4. Publish Python SDK - Publish to internal registry or PyPI.
5. Add SDK documentation and examples.

---

## 6. Ownership & Conventions

| Folder | Owner | Change Policy |
|---|---|---|
| `proto/` | Platform / Architecture | Any breaking change requires a RFC and version bump. |
| `shared/` | Platform / Platform Team | PR review by at least one service owner. |
| `sdk/` | Platform / Platform Team | Breaking changes require version bump and migration guide. |
| `services/*` | Service Owner | Independent deploy; must not depend on unmerged shared changes. |
| `knowledge/` | Curriculum / Content Team | Data PRs; validated by ingestion pipeline tests. |
| `models/` | ML Engineer | Model changes require benchmark validation before promotion. |
| `storage/` | Data Engineer | Schema changes require migration script and rollback plan. |
| `infra/` | DevOps / SRE | Infrastructure changes require plan review. |
| `pipelines/` | Data / ML Engineer | Flow changes tested in staging before prod. |
| `workers/` | Platform / Platform Team | Worker changes require observability integration. |
| `tests/` | QA / Platform Team | Test changes must maintain coverage thresholds. |
| `scripts/` | DevOps / SRE | Script changes require safety review for production use. |
| `docs/` | Technical Writer | Documentation changes require accuracy validation. |
| `notebooks/` | Research | No production dependencies; weekly cleanup of stale experiments. |

---

## 7. Quick-Start (Target State)

```bash
# 1. Clone and enter
cd ai-platform/

# 2. One-command local stack
make dev

# 3. Run contract tests
make test

# 4. Regenerate proto stubs after changing .proto
make proto

# 5. Ingest the first curriculum document
python scripts/ingest/ingest_document.py \
  --source knowledge/cp/SD_Kelas_1_CP.json \
  --pipeline ingestion

# 6. Check platform health
curl http://localhost:8080/health
```

---

## 8. Summary

The `ai-platform/` root should be a **lean platform layer**: proto contracts, shared libraries, infrastructure definitions, knowledge assets, and cross-service pipelines. Domain logic (agents, guards, engines, enhancers) belongs **inside the services that own them**, not as peer directories that create the illusion of modularity without actual deployment boundaries.

This plan turns `ai-platform/` from a sprawling design document into a working system.

## Remaining Tasks:
- [ ] Move reusable code to shared/ - Extract logging, telemetry, security, middleware from services
- [ ] Create Go SDK - Build Go SDK for backend integration
- [ ] Refactor backend gRPC - Update backend to use Go SDK instead of hand-written stubs
- [ ] Publish Python SDK - Publish to internal registry or PyPI

## Remaining Phase 6 Tasks:
- [ ] Move reusable code to shared/ - Extract logging, telemetry, security, middleware from services
- [ ] Create Go SDK - Build Go SDK for backend integration
- [ ] Refactor backend gRPC - Update backend to use Go SDK instead of hand-written stubs
- [ ] Publish Python SDK - Publish to internal registry or PyPI
- [ ] Add SDK documentation and examples

## Remaining Phase 3 Tasks:
- [x] Implement enrichment pipeline (metadata tagging)
- [x] Implement indexing pipeline (vector store + graph edges)
- [x] Implement generation pipeline (retrieval → context → LLM → guard)
- [x] Write unit tests for pipeline stages
- [x] Move reusable worker code to workers/ directory
- [x] Setup worker template with observability

## Remaining Phase 4 Tasks:
- [x] Load knowledge/ to vector store and knowledge graph via ingestion pipeline
- [x] Setup knowledge/ontology/ from merged educational-ontology/

Phase 3: 100% (7/7 tasks) ✅
Phase 4: 100% (6/6 tasks) ✅
Phase 5: 100% (9/9 tasks) ✅
Phase 6: 0% (0/5 tasks) ← Current focus