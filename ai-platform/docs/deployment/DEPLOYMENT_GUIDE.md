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
* production hardening.

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
         │ MinIO                          │
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
* MinIO.

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
OCR workers
embedding workers
indexing workers
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
reranking-service
vision-service
embedding-service
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

# 3. MinIO

## Purpose

Object storage.

---

# Stores

* PDFs,
* OCR results,
* extracted images,
* embeddings artifacts.

---

# Production Requirements

* distributed storage,
* replication,
* lifecycle policies.

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

# MinIO

* object versioning,
* lifecycle backup.

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
