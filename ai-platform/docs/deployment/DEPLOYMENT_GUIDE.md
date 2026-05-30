# DEPLOYMENT GUIDE

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini menjelaskan deployment strategy untuk Enterprise Educational AI Platform.

Dokumen ini mencakup:

* infrastructure deployment,
* container orchestration,
* Kubernetes architecture,
* CI/CD strategy,
* scaling strategy,
* GPU deployment,
* observability deployment,
* production hardening,
* integration dengan SIM Sekolah terpadu.

---

# Current Infrastructure Status

## Integration dengan SIM Sekolah

AI Platform saat ini terintegrasi dengan ekosistem SIM Sekolah yang memiliki:

### Existing Infrastructure (SIM Sekolah Utama)
- PostgreSQL 18.4-alpine (port 5432)
- Redis 7-alpine (port 11576)
- RabbitMQ 3-management-alpine (ports 5672, 15672)
- Qdrant latest (ports 6333-6334)
- RustFS (S3-compatible storage, ports 9000-9001) - akan diganti dengan SeaweedFS
- Backend Go Fiber (port 8080)
- OTEL Collector
- Neo4j (ports 7474, 7687)

### AI Platform Infrastructure (Stand-alone)
- PostgreSQL 15-alpine (port 5432)
- Redis 7-alpine (port 6379)
- RabbitMQ 3.12-management-alpine (ports 5672, 15672)
- Qdrant v1.7.0 (ports 6333-6334)
- MinIO (ports 9000-9001)
- Observability Stack (Prometheus, Grafana, Loki, Tempo)

### Integration Challenges
1. **Port Conflicts**: Beberapa service memiliki port yang sama (telah di-resolve)
2. **Version Differences**: PostgreSQL, Qdrant, RabbitMQ versions berbeda
3. **Storage Solutions**: RustFS vs MinIO vs SeaweedFS (telah di-resolve dengan SeaweedFS)
4. **Network Isolation**: Dua docker-compose networks terpisah

### Port Mapping Resolution
Berikut adalah port mapping yang telah di-adjust untuk menghindari konflik:

**SIM Sekolah Infrastructure:**
- Backend: 8080
- PostgreSQL: 5432
- Redis: 11576
- RabbitMQ: 5672, 15672
- Qdrant: 6333, 6334
- SeaweedFS Master: 9333, 19333
- SeaweedFS Volume: 8333, 18333 (container: 8080, 18080)
- SeaweedFS Filer: 8888, 18888
- SeaweedFS S3: 9555, 9556 (container: 8333, 8334)

**AI Platform Infrastructure (Default):**
- PostgreSQL: 5432 (shared dengan SIM Sekolah saat integrated)
- Redis: 6379
- RabbitMQ: 5672, 15672 (shared dengan SIM Sekolah saat integrated)
- Qdrant: 6333, 6334 (shared dengan SIM Sekolah saat integrated)
- MinIO: 9100, 9101 (diubah dari 9000, 9001 untuk menghindari konflik)
- Grafana: 3030 (diubah dari 3000 untuk menghindari konflik dengan frontend)
- Prometheus: 9090
- Loki: 3100
- Tempo: 3200, 4317, 4318
- AI Services: 8001-8012

### Recommended Integration Strategy
1. **Unified Infrastructure**: Gunakan satu infrastructure stack untuk kedua platform
2. **SeaweedFS Migration**: Ganti RustFS dengan SeaweedFS untuk object storage terpadu
3. **Service Discovery**: Implementasikan cross-platform service discovery
4. **Environment Configuration**: Standardize environment variables

---

# Deployment Philosophy

Platform ini dirancang sebagai:

```text id="deployment-philosophy"
enterprise-grade distributed AI infrastructure
```

Bukan:

* single VPS deployment,
* docker-compose production,
* monolith deployment.

---

# Core Deployment Principles

---

# 1. Everything Containerized

Semua service wajib:

* containerized,
* immutable,
* reproducible.

---

# 2. Stateless Services

Semua service harus:

* stateless,
* horizontally scalable.

---

# 3. Infrastructure as Code

Semua deployment harus:

* versioned,
* automated,
* reproducible.

---

# 4. GitOps-Based Deployment

Production deployment tidak boleh manual.

Gunakan:

* GitOps,
* CI/CD,
* automated rollout.

---

# High-Level Deployment Architecture

```text id="deployment-architecture"
                    ┌────────────────────┐
                    │   React Frontend   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Golang Backend API │
                    └─────────┬──────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │  Python AI Platform     │
                 └─────────┬───────────────┘
                           │
         ┌─────────────────┼──────────────────┐
         ▼                 ▼                  ▼
   AI Services        Worker Pool        GPU Workers

                           │
                           ▼
         ┌─────────────────────────────────┐
         │ Infrastructure Layer            │
         ├─────────────────────────────────┤
         │ PostgreSQL                     │
         │ Qdrant                         │
         │ RabbitMQ / Kafka               │
         │ SeaweedFS (Object Storage)     │
         │ Redis (Cache)                  │
         │ Prometheus                     │
         │ Grafana                        │
         └─────────────────────────────────┘
```

---

# Deployment Environments

---

# 1. Development

## Purpose

Local development environment.

---

# Characteristics

* lightweight,
* fast iteration,
* minimal infra.

---

# Recommended

```text id="dev-stack"
docker-compose
```

---

# Port Configuration Reference

## SIM Sekolah Port Mapping
| Service | External Port | Container Port | Notes |
|---------|---------------|----------------|-------|
| PostgreSQL | 5432 | 5432 | Database |
| Redis | 11576 | 11576 | Cache |
| RabbitMQ | 5672, 15672 | 5672, 15672 | Message Queue |
| Qdrant | 6333, 6334 | 6333, 6334 | Vector Database |
| Backend | 8080 | 8080 | Go Fiber API |
| SeaweedFS Master | 9333, 19333 | 9333, 19333 | Storage Master |
| SeaweedFS Volume | 8333, 18333 | 8080, 18080 | Storage Volume |
| SeaweedFS Filer | 8888, 18888 | 8888, 18888 | File Management |
| SeaweedFS S3 | 9555, 9556 | 8333, 8334 | S3 Gateway |
| Frontend | 3000 | 80 | React Frontend |

## AI Platform Port Mapping (Default)
| Service | External Port | Container Port | Notes |
|---------|---------------|----------------|-------|
| PostgreSQL | 5432 | 5432 | Shared dengan SIM Sekolah |
| Redis | 6379 | 6379 | Cache |
| RabbitMQ | 5672, 15672 | 5672, 15672 | Shared dengan SIM Sekolah |
| Qdrant | 6333, 6334 | 6333, 6334 | Shared dengan SIM Sekolah |
| MinIO | 9100, 9101 | 9000, 9101 | Object Storage (conflict resolved) |
| Grafana | 3030 | 3000 | Observability (conflict resolved) |
| Prometheus | 9090 | 9090 | Metrics |
| Loki | 3100 | 3100 | Log Aggregation |
| Tempo | 3200, 4317, 4318 | 3200, 4317, 4318 | Distributed Tracing |
| Gateway Service | 8002 | 8002 | API Gateway |
| Parser Service | 8001 | 8001 | Document Processing |
| Semantic Chunk Service | 8003 | 8003 | Text Chunking |
| Metadata Service | 8004 | 8004 | Document Metadata |
| Embedding Service | 8005 | 8005 | Vector Generation |
| Retrieval Service | 8006 | 8006 | Semantic Retrieval |
| Generation Service | 8007 | 8007 | AI Generation |
| Audit Service | 8008 | 8008 | Audit Logging |
| Moderation Service | 8009 | 8009 | Content Moderation |
| Reranking Service | 8010 | 8010 | Result Reranking |
| Vision Service | 8011 | 8011 | Image Processing |
| Monitoring Service | 8012 | 8012 | Service Monitoring |

## Conflict Resolution Summary
1. **Port 8080**: SeaweedFS Volume moved to 8333 (external) to avoid Backend conflict
2. **Port 9000, 9001**: AI Platform MinIO moved to 9100, 9101 to avoid SeaweedFS S3 conflict
3. **Port 3000**: AI Platform Grafana moved to 3030 to avoid Frontend conflict
4. **Port 9443**: SeaweedFS S3 moved to 9555 to avoid Portainer conflict
5. **Infrastructure Ports**: PostgreSQL, RabbitMQ, Qdrant intentionally shared for integrated deployment

---

# Current Deployment Options

## Option A: Stand-alone AI Platform (Current Default)

Jalankan AI Platform secara terpisah dengan infrastructure sendiri:

```bash
cd ai-platform
cp .env.example .env
docker-compose up -d
```

**Pros**:
- Tidak ada konflik dengan SIM Sekolah
- Development yang lebih cepat
- Dependency yang lebih terkontrol

**Cons**:
- Duplikasi infrastructure resources
- Integrasi lebih kompleks
- Resource usage lebih tinggi

## Option B: Integrated Deployment (Recommended for Production)

Integrasikan AI Platform dengan existing SIM Sekolah infrastructure:

**Langkah-langkah**:
1. Gunakan existing PostgreSQL, Redis, RabbitMQ, Qdrant dari SIM Sekolah
2. Tambahkan SeaweedFS untuk menggantikan RustFS
3. Deploy hanya AI Platform services (tanpa infrastructure duplikat)
4. Konfigurasikan environment variables untuk menggunakan existing services

**Configuration Changes Needed**:
- Port mapping untuk menghindari conflicts
- Environment variables untuk cross-network communication
- Service discovery configuration
- Shared network setup

## Option C: Hybrid Deployment

Gunakan sebagian infrastructure, deploy sebagian:

```bash
# Gunakan existing SIM Sekolah infrastructure
# Deploy hanya AI Platform services
cd ai-platform
docker-compose -f docker-compose.yml --profile services-only up -d
```

---

# 2. Staging

## Purpose

Pre-production validation.

---

# Characteristics

* mirrors production,
* full observability,
* integration testing.

---

# 3. Production

## Purpose

Enterprise production workloads.

---

# Characteristics

* high availability,
* autoscaling,
* observability,
* disaster recovery.

---

# Recommended Infrastructure

---

# Container Runtime

## Recommended

* Docker

---

# Container Orchestration

## Recommended

* Kubernetes

---

# Why Kubernetes

Karena AI platform membutuhkan:

* autoscaling,
* worker orchestration,
* GPU scheduling,
* rolling deployment,
* service discovery.

---

# Recommended Kubernetes Architecture

```text id="k8s-architecture"
Kubernetes Cluster
├── frontend namespace
├── backend namespace
├── ai-platform namespace
├── monitoring namespace
└── infra namespace
```

---

# Namespace Strategy

---

# frontend

Berisi:

* React app,
* CDN layer.

---

# backend

Berisi:

* Golang services,
* business APIs.

---

# ai-platform

Berisi:

* AI services,
* workers,
* orchestration.

---

# monitoring

Berisi:

* Prometheus,
* Grafana,
* Loki,
* Tempo.

---

# infra

Berisi:

* PostgreSQL,
* RabbitMQ,
* Qdrant,
* SeaweedFS (Object Storage),
* Redis.

---

# AI Platform Deployment Strategy

---

# Service Categories

## 1. API Services

Characteristics:

* low latency,
* synchronous,
* autoscale by request.

---

# Examples

```text id="api-services"
gateway-service
retrieval-service
generation-service
parser-service
semantic-chunk-service
metadata-service
monitoring-service
strategic-analysis-service
```

---

# Deployment Type

```text id="deployment-api"
Kubernetes Deployment
```

---

# 2. Worker Services

Characteristics:

* asynchronous,
* queue-driven,
* scalable.

---

# Examples

```text id="worker-services"
parser-service (document processing)
semantic-chunk-service (text chunking)
embedding-service (vector generation)
metadata-service (document metadata)
vision-service (image processing)
reranking-service (result optimization)
```

---

# Deployment Type

```text id="deployment-workers"
Kubernetes Worker Deployment
```

---

# 3. GPU Services

Characteristics:

* GPU intensive,
* isolated nodes,
* expensive resources.

---

# Examples

```text id="gpu-services"
embedding-service (vector generation)
reranking-service (result optimization)
vision-service (image processing)
generation-service (AI response generation)
```

---

# Deployment Type

```text id="gpu-deployment"
Dedicated GPU Node Pool
```

---

# Kubernetes Node Strategy

---

# CPU Node Pool

## Purpose

Menjalankan:

* API services,
* lightweight workers.

---

# GPU Node Pool

## Purpose

Menjalankan:

* embeddings,
* reranking,
* VLM inference.

---

# Infra Node Pool

## Purpose

Menjalankan:

* databases,
* queue systems,
* observability stack.

---

# Suggested Cluster Layout

```text id="cluster-layout"
Node Pool
├── cpu-general
├── cpu-workers
├── gpu-ai
└── infra-storage
```

---

# Service Deployment Guidelines

---

# 1. One Service = One Container

Jangan gabungkan multiple services dalam satu container.

---

# 2. Stateless API

API services:

* tidak menyimpan state,
* tidak menyimpan session.

---

# 3. Queue-Based Workers

Workers harus:

* consume queue,
* retry-safe,
* idempotent.

---

# 4. GPU Isolation

GPU workloads wajib:

* isolated,
* resource-limited.

---

# Recommended Scaling Strategy

---

# Horizontal Pod Autoscaler (HPA)

## Use Cases

* retrieval-service,
* generation-service,
* workers.

---

# Metrics

```text id="hpa-metrics"
CPU
memory
queue lag
GPU utilization
```

---

# Queue-Based Scaling

Workers autoscale berdasarkan:

* queue depth,
* processing latency.

---

# Example

```text id="worker-autoscale"
queue > 1000
→ scale workers
```

---

# Current Service Implementation

## Active Services (docker-compose.yml)

Services yang saat ini sudah terintegrasi dalam docker-compose.yml:

1. **gateway-service** (port 8002) - API Gateway
2. **parser-service** (port 8001) - Document parsing
3. **semantic-chunk-service** (port 8003) - Semantic text chunking
4. **metadata-service** (port 8004) - Document metadata extraction
5. **embedding-service** (port 8005) - Vector embedding generation
6. **retrieval-service** (port 8006) - Semantic retrieval
7. **generation-service** (port 8007) - AI content generation
8. **audit-service** (port 8008) - Audit logging
9. **moderation-service** (port 8009) - Content moderation
10. **reranking-service** (port 8010) - Result reranking
11. **vision-service** (port 8011) - Image/vision processing
12. **monitoring-service** (port 8012) - Service monitoring
13. **strategic-analysis-service** - Educational analysis

## Additional Services (Development Phase)

Services yang ada dalam direktori tetapi belum fully integrated:

- adaptive-learning-engine
- advanced-enhancement-service
- ai-agents-service
- assessment-engine
- curriculum-engine
- educational-intelligence-service
- educational-observability-service
- educational-ontology-service
- hallucination-guard-service
- learning-graph-engine
- learning-progression-engine
- notification-service
- orchestration-service
- pedagogy-engine
- recommendation-engine
- retrieval-enhancement-service
- semantic-enrichment-service

---

# Storage Deployment

---

# 1. PostgreSQL

## Purpose

Relational database.

---

# Recommendation

Gunakan:

* managed PostgreSQL,
  atau
* HA PostgreSQL cluster.

---

# Production Requirements

* replication,
* backup,
* WAL archiving.

---

# 2. Qdrant

## Purpose

Vector database.

---

# Deployment

Gunakan:

* distributed cluster,
* persistent volume.

---

# Production Requirements

* replication,
* snapshot backup,
* SSD storage.

---

# 3. Redis

## Purpose

Caching layer untuk performance optimization.

---

# Uses

* retrieval caching,
* metadata caching,
* prompt caching,
* session management,
* rate limiting.

---

# Production Requirements

* persistence,
* replication,
* memory optimization,
- eviction policies.

---

# 4. SeaweedFS

## Purpose

Distributed object storage system untuk menggantikan RustFS dan MinIO.

---

# Migration Path

**From RustFS (SIM Sekolah)**:
- RustFS saat ini digunakan di SIM Sekolah utama
- Akan diganti dengan SeaweedFS untuk integrasi yang lebih baik

**From MinIO (AI Platform)**:
- AI Platform saat ini menggunakan MinIO
- Akan bermigrasi ke SeaweedFS untuk统一 storage solution

---

# Stores

* PDFs,
* OCR results,
* extracted images,
* embeddings artifacts,
* model checkpoints,
* curriculum documents,
* assessment materials.

---

# SeaweedFS Advantages

- **Better Performance**: Higher throughput than MinIO/RustFS
- **S3 Compatible**: Full S3 API compatibility
- **Distributed Architecture**: Better scaling capabilities
- **Filer Support**: Better file management
- **Active Development**: More active community than RustFS

---

# Production Requirements

* distributed storage cluster,
* replication across multiple nodes,
* lifecycle policies,
- S3 gateway layer,
- Filer server for metadata management.

---

# Queue System Deployment

---

# Recommended

* RabbitMQ
  atau
* Apache Kafka

---

# Queue Architecture

```text id="queue-architecture"
document.queue
OCR.queue
embedding.queue
retrieval.queue
generation.queue
```

---

# GPU Deployment Strategy

---

# GPU Workloads

* embeddings,
* reranking,
* VLM,
* OCR acceleration.

---

# GPU Recommendations

| Workload      | GPU        |
| ------------- | ---------- |
| Embeddings    | T4 / L4    |
| Reranking     | L4         |
| Vision Models | A100 / L40 |
| OCR           | T4         |

---

# GPU Isolation Rules

GPU workloads:

* tidak boleh share dengan infra,
* harus punya node affinity.

---

# CI/CD Strategy

---

# Recommended Tools

* [GitHub Actions](https://github.com/features/actions?utm_source=chatgpt.com)
* [Argo CD](https://argo-cd.readthedocs.io/?utm_source=chatgpt.com)

---

# CI Pipeline

```text id="ci-pipeline"
Lint
↓
Test
↓
Build Docker Image
↓
Security Scan
↓
Push Registry
```

---

# CD Pipeline

```text id="cd-pipeline"
Git Push
↓
Argo CD Sync
↓
Rolling Deployment
↓
Health Check
↓
Production Rollout
```

---

# Deployment Strategy

---

# Recommended

## Rolling Update

Karena:

* zero downtime,
* safer deployment.

---

# Avoid

❌ recreate deployment

---

# Blue-Green Deployment

Recommended untuk:

* generation-service,
* retrieval-service.

---

# Canary Deployment

Recommended untuk:

* new models,
* retrieval algorithm updates.

---

# Observability Deployment

---

# Stack

* Prometheus
* Grafana
* OpenTelemetry
* Loki

---

# Required Metrics

```text id="required-metrics"
retrieval_latency
OCR_failure_rate
queue_lag
embedding_duration
GPU_utilization
hallucination_rate
```

---

# Required Logs

* AI logs,
* retrieval logs,
* audit logs,
* worker logs,
* queue logs.

---

# Security Deployment

---

# Secrets Management

## Recommended

* Kubernetes Secrets,
* HashiCorp Vault.

---

# Never Store

❌ API keys in code

❌ secrets in Git

---

# Network Security

Gunakan:

* internal service mesh,
* private networking,
* ingress protection.

---

# TLS Requirements

Semua traffic wajib:

* HTTPS,
* TLS encrypted.

---

# Backup Strategy

---

# PostgreSQL

* daily backup,
* PITR,
* WAL archive.

---

# Qdrant

* snapshot backup,
* replication.

---

# SeaweedFS

* volume replication,
- snapshot backup,
- lifecycle policies.

---

# Disaster Recovery

---

# Recovery Objectives

| Objective | Target       |
| --------- | ------------ |
| RPO       | < 15 minutes |
| RTO       | < 1 hour     |

---

# Required DR Features

* backup automation,
* multi-zone deployment,
* infra reproducibility.

---

# Production Readiness Checklist

---

# Infrastructure

✅ Kubernetes

✅ autoscaling

✅ monitoring

✅ tracing

✅ backups

---

# Security

✅ TLS

✅ RBAC

✅ secret management

---

# AI Governance

✅ audit logs

✅ retrieval logs

✅ prompt logs

---

# Reliability

✅ retry policy

✅ DLQ

✅ health checks

✅ readiness probes

---

# Performance Optimization

---

# Recommended

## Redis Cache

Untuk:

* retrieval caching,
* metadata caching,
* prompt caching.

---

# Batch Processing

Untuk:

* embeddings,
* OCR,
* indexing.

---

# Async Processing

Untuk:

* heavy AI workloads.

---

# Deployment Anti-Patterns

---

# DO NOT

❌ deploy AI services on single VPS

❌ store embeddings in app memory

❌ run GPU workloads on shared infra nodes

❌ deploy without observability

❌ skip tracing

❌ deploy without queue

---

# Recommended Production Topology

```text id="production-topology"
Internet
   ↓
Ingress
   ↓
Frontend
   ↓
Golang Backend
   ↓
AI Gateway
   ↓
AI Platform Cluster
   ├── API Services
   ├── Workers
   ├── GPU Workers
   └── Monitoring
```

---

# Final Recommendations

---

# Prioritize First

## 1. Observability

## 2. Queue reliability

## 3. Retrieval latency

## 4. GPU isolation

## 5. Backup strategy

---

# Most Important Insight

Enterprise AI deployment bukan tentang:

```text id="wrong-focus"
deploying GPT
```

Tetapi tentang:

* orchestration,
* scaling,
* observability,
* reproducibility,
* governance,
* fault tolerance.

Karena:
AI systems jauh lebih sulit di-operasikan dibanding backend biasa.
