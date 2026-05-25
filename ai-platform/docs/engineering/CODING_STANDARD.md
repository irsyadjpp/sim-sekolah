# CODING STANDARD

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini mendefinisikan standar coding untuk seluruh Enterprise Educational AI Platform.

Tujuan:

* menjaga consistency,
* meningkatkan maintainability,
* mempermudah observability,
* meningkatkan reliability,
* mengurangi technical debt.

---

# Core Engineering Principles

---

# 1. Readability Over Cleverness

Kode harus:

* mudah dibaca,
* mudah dipahami,
* mudah di-debug.

---

# Avoid

❌ over-engineering

❌ overly clever abstractions

❌ magic behavior

---

# Prefer

✅ explicit code

✅ predictable flow

✅ maintainable architecture

---

# 2. Scalability First

Semua code harus mempertimbangkan:

* scaling,
* distributed systems,
* retries,
* observability.

---

# 3. Fail Safe

AI systems harus:

* resilient,
* retryable,
* observable,
* recoverable.

---

# 4. Traceability Everywhere

Semua request wajib:

* traceable,
* logged,
* correlated.

---

# General Naming Convention

---

# File Naming

## Python

Gunakan:

```text id="python-file-naming"
snake_case.py
```

---

# Examples

✅ Benar:

```text id="python-file-good"
embedding_service.py
semantic_chunk_builder.py
```

---

# Avoid

❌ CamelCase.py

❌ random naming

---

# Directory Naming

Gunakan:

```text id="dir-naming"
snake_case/
```

---

# Examples

```text id="dir-examples"
retrieval/
chunking/
metadata/
```

---

# Variable Naming

---

# Use Meaningful Names

✅ Benar:

```python
retrieved_chunks
embedding_vector
retrieval_latency
```

---

# Avoid

❌ Bad:

```python
x
tmp
data2
obj
```

---

# Function Naming

Gunakan:

```text id="function-naming"
verb_noun()
```

---

# Examples

```python
generate_embeddings()
build_semantic_chunks()
retrieve_documents()
```

---

# Class Naming

Gunakan:

```text id="class-naming"
PascalCase
```

---

# Examples

```python
SemanticChunkBuilder
EmbeddingGenerator
RetrievalService
```

---

# Constants Naming

Gunakan:

```text id="constants-naming"
UPPER_SNAKE_CASE
```

---

# Example

```python
MAX_RETRY_COUNT = 5
DEFAULT_TIMEOUT = 30
```

---

# Project Structure Standard

---

# Rules

## 1. One Responsibility Per Module

---

# GOOD

```text id="good-module-structure"
retrieval/
  hybrid_retriever.py
  reranker.py
  filters.py
```

---

# BAD

```text id="bad-module-structure"
utils.py
helpers.py
common.py
```

---

# 2. Avoid God Files

---

# BAD

```text id="god-file"
ai_service.py (5000+ lines)
```

---

# GOOD

Pisahkan berdasarkan domain.

---

# 3. Avoid Circular Dependency

---

# Rules

Dependency flow harus:

* jelas,
* satu arah.

---

# Layering Standard

```text id="layering-standard"
API
 ↓
Service
 ↓
Domain
 ↓
Repository
 ↓
Infrastructure
```

---

# Python Coding Standards

---

# Type Hinting Mandatory

## GOOD

```python
def generate_embeddings(text: str) -> list[float]:
    ...
```

---

# BAD

```python
def generate_embeddings(text):
    ...
```

---

# Dataclass / Pydantic Preferred

## Use

* dataclass,
* Pydantic models.

---

# Example

```python
from pydantic import BaseModel

class ChunkMetadata(BaseModel):
    subject: str
    grade: int
```

---

# Async Standards

---

# Use Async Only When Necessary

Gunakan async untuk:

* IO,
* HTTP,
* DB,
* queue.

---

# Avoid

❌ async everywhere

---

# Logging Standard

---

# Logging is Mandatory

Semua service wajib logging.

---

# Required Log Fields

```json id="required-log-fields"
{
  "trace_id": "",
  "request_id": "",
  "service": "",
  "event": ""
}
```

---

# Structured Logging Only

---

# GOOD

```python
logger.info(
    "retrieval_completed",
    extra={
        "trace_id": trace_id,
        "latency": latency
    }
)
```

---

# BAD

```python
print("done")
```

---

# Never Use

❌ print()

di production code.

---

# Error Handling Standard

---

# Never Swallow Errors

---

# BAD

```python
try:
    ...
except:
    pass
```

---

# GOOD

```python
try:
    ...
except Exception as e:
    logger.exception("embedding_failed")
    raise
```

---

# Error Classification

---

# Use Categories

```text id="error-categories"
ValidationError
RetrievalError
EmbeddingError
OCRFailure
GenerationError
```

---

# Retry Strategy

---

# Retry Only Safe Operations

## Retryable

✅ network timeout

✅ temporary queue failure

---

# Non-Retryable

❌ invalid schema

❌ corrupted PDF

---

# Timeout Standards

---

# All External Calls Must Have Timeout

---

# GOOD

```python
httpx.get(url, timeout=30)
```

---

# BAD

```python
httpx.get(url)
```

---

# API Standards

---

# API Must Be Versioned

---

# GOOD

```text id="api-versioning-good"
v1/retrieval/query
```

---

# BAD

```text id="api-versioning-bad"
query
```

---

# Request Validation Mandatory

Gunakan:

* Pydantic,
* schema validation.

---

# Response Standard

## Standard Response Format

```json id="response-standard"
{
  "success": true,
  "data": {},
  "error": null
}
```

---

# gRPC Standards

---

# Proto Naming

Gunakan:

```text id="proto-naming"
snake_case.proto
```

---

# Service Naming

Gunakan:

```text id="grpc-service-naming"
RetrievalService
EmbeddingService
```

---

# Event Standards

---

# Event Naming

Gunakan:

```text id="event-standard"
DOMAIN.ACTION.STATUS
```

---

# Example

```text id="event-example"
DOCUMENT.PARSE.COMPLETED
```

---

# Queue Consumer Standards

---

# Consumers Must Be

✅ idempotent

✅ retry-safe

✅ observable

---

# AI Standards

---

# Never Hardcode Prompts

---

# GOOD

```text id="prompt-good"
shared/prompts/
```

---

# BAD

Prompt tersebar di codebase.

---

# Prompt Versioning Mandatory

---

# Example

```text id="prompt-versioning"
retrieval_prompt_v1.txt
```

---

# Embedding Standards

---

# Embedding Metadata Mandatory

Semua embedding wajib memiliki:

* source document,
* chunk ID,
* embedding model,
* timestamp.

---

# Chunk Standards

---

# Chunk Must Be

✅ semantic

✅ self-contained

✅ metadata-rich

---

# Never Use

❌ fixed character chunking

---

# Security Standards

---

# Never Hardcode

❌ API keys

❌ secrets

❌ credentials

---

# Use

✅ environment variables

✅ secret manager

---

# Dependency Standards

---

# Dependency Rules

## Allowed

* explicit dependency,
* versioned dependency.

---

# Avoid

❌ unused libraries

❌ experimental packages in production

---

# Pin Versions

---

# GOOD

```text id="pin-version-good"
pydantic==2.7.0
```

---

# BAD

```text id="pin-version-bad"
pydantic
```

---

# Testing Standards

---

# Test Categories

## Mandatory

* unit tests,
* integration tests,
* retrieval tests.

---

# AI Evaluation Tests

---

# Required

* hallucination test,
* retrieval relevance test,
* chunk quality test.

---

# Coverage Goal

```text id="coverage-goal"
minimum 80%
```

---

# Observability Standards

---

# Every Service Must Have

✅ metrics

✅ tracing

✅ structured logs

---

# OpenTelemetry Mandatory

---

# Required Trace Fields

```text id="trace-fields"
trace_id
request_id
user_id
document_id
```

---

# Performance Standards

---

# Avoid

❌ blocking operations in async flow

❌ loading huge files into memory

---

# Prefer

✅ streaming

✅ batching

✅ async workers

---

# Database Standards

---

# Never Query Without Filter

---

# BAD

```sql
SELECT * FROM chunks;
```

---

# GOOD

```sql
SELECT * FROM chunks
WHERE document_id = ?;
```

---

# Migration Standards

---

# Rules

* migrations immutable,
* backward compatible,
* reversible.

---

# Git Standards

---

# Branch Naming

```text id="branch-naming"
feature/
bugfix/
hotfix/
```

---

# Commit Naming

Gunakan:

```text id="commit-format"
feat:
fix:
refactor:
docs:
test:
```

---

# Example

```text id="commit-example"
feat: add semantic chunk builder
```

---

# Pull Request Standards

---

# PR Must Include

✅ description

✅ testing result

✅ rollback impact

✅ screenshots/logs if needed

---

# AI Service Standards

---

# Services Must Be

✅ stateless

✅ scalable

✅ retry-safe

✅ observable

---

# Never

❌ store state in memory

❌ share mutable global state

---

# Anti-Patterns

---

# DO NOT

❌ massive utils.py

❌ business logic in controller

❌ hidden side effects

❌ huge functions

❌ magic numbers

❌ silent failures

❌ print debugging

---

# Recommended Function Size

---

# Target

```text id="function-size"
20–50 lines
```

---

# Recommended File Size

---

# Target

```text id="file-size"
< 500 lines
```

---

# Documentation Standards

---

# Every Module Must Have

✅ README

✅ architecture notes

✅ usage examples

---

# Public APIs Must Have

✅ request examples

✅ response examples

✅ error examples

---

# Production Readiness Checklist

---

# Before Merge

✅ tests pass

✅ logging exists

✅ tracing exists

✅ metrics added

✅ retry strategy reviewed

✅ timeout exists

---

# Before Production

✅ observability validated

✅ scaling validated

✅ rollback validated

✅ security reviewed

---

# Most Important Engineering Insight

Enterprise AI systems gagal biasanya bukan karena:

* model,
* framework,
* GPU.

Tetapi karena:

* inconsistent code,
* poor observability,
* weak retry strategy,
* hidden side effects,
* technical debt chaos.

Karena itu:
coding standard adalah:

* operational foundation,
* scalability foundation,
* maintainability foundation,

untuk enterprise AI platform.
