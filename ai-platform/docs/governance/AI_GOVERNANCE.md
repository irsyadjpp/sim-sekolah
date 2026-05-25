# AI GOVERNANCE

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini menjelaskan framework AI Governance untuk Enterprise Educational AI Platform.

AI Governance adalah:

```text id="ai-governance-definition"
operational control system
```

yang memastikan:

* AI aman,
* AI dapat diaudit,
* AI dapat dijelaskan,
* AI dapat dipercaya,
* AI compliant,
* AI reliable untuk pendidikan.

---

# Why AI Governance Matters

Enterprise educational AI systems tidak boleh:

* hallucinate tanpa kontrol,
* memberikan jawaban berbahaya,
* menghasilkan bias,
* kehilangan traceability.

---

# Core Principle

AI bukan sekadar:

* chatbot,
* LLM wrapper,
* prompt system.

AI adalah:

```text id="ai-system-definition"
decision-support infrastructure
```

untuk:

* guru,
* siswa,
* sekolah,
* kurikulum.

Karena itu:
AI wajib memiliki governance.

---

# Governance Objectives

---

# 1. Trustworthiness

AI harus:

* reliable,
* explainable,
* auditable.

---

# 2. Educational Safety

AI tidak boleh:

* memberi jawaban berbahaya,
* misleading,
* anti-pedagogical.

---

# 3. Traceability

Semua AI response harus:

* dapat ditelusuri,
* dapat direproduksi.

---

# 4. Compliance

AI harus compliant terhadap:

* kebijakan sekolah,
* data governance,
* educational standards.

---

# 5. Operational Reliability

AI harus:

* observable,
* measurable,
* monitorable.

---

# Governance Architecture

```text id="governance-architecture"
User Request
      ↓
Policy Validation
      ↓
Moderation Layer
      ↓
Retrieval Governance
      ↓
Prompt Governance
      ↓
LLM Generation
      ↓
Post-Generation Validation
      ↓
Audit Logging
      ↓
Response Delivery
```

---

# Core Governance Components

---

# 1. Policy Engine

## Purpose

Menentukan:

* allowed behavior,
* restricted behavior,
* model policy.

---

# Responsibilities

* access policy,
* AI usage policy,
* educational safety rules,
* moderation rules.

---

# Example Rules

```text id="policy-rules"
- siswa tidak boleh akses admin prompts
- AI tidak boleh membuat jawaban toxic
- AI tidak boleh memberi jawaban di luar kurikulum
```

---

# 2. Moderation Layer

## Purpose

Melindungi sistem dari:

* harmful prompts,
* toxic outputs,
* jailbreak attempts.

---

# Responsibilities

* input moderation,
* output moderation,
* jailbreak detection,
* prompt injection detection.

---

# Recommended Architecture

```text id="moderation-flow"
User Prompt
     ↓
Input Moderation
     ↓
Prompt Injection Detection
     ↓
LLM
     ↓
Output Moderation
```

---

# Moderation Categories

---

# Blocked Content

❌ hate speech

❌ explicit violence

❌ sexual exploitation

❌ self-harm instructions

❌ illegal activity

---

# Educational Restrictions

❌ unsafe experiments

❌ dangerous chemistry guidance

❌ misinformation

---

# 3. Retrieval Governance

## Purpose

Memastikan retrieval:

* valid,
* explainable,
* curriculum-aware.

---

# Responsibilities

* metadata filtering,
* curriculum filtering,
* source validation,
* confidence scoring.

---

# Retrieval Rules

AI wajib:

* menggunakan source terpercaya,
* menggunakan metadata filter,
* mencantumkan citation source.

---

# Example

```json id="retrieval-rule-example"
{
  "subject": "IPA",
  "grade": 4,
  "phase": "B"
}
```

---

# 4. Prompt Governance

## Purpose

Mengontrol:

* prompt quality,
* prompt consistency,
* prompt safety.

---

# Rules

## Prompts wajib:

✅ versioned

✅ reviewed

✅ auditable

---

# Prompt Storage

```text id="prompt-storage"
shared/prompts/
```

---

# Example

```text id="prompt-example"
retrieval_prompt_v1.txt
```

---

# Prompt Versioning

---

# Rules

Gunakan:

* semantic versioning,
* immutable prompts.

---

# Example

```text id="prompt-versioning-example"
teacher_assistant_v1
teacher_assistant_v2
```

---

# 5. Output Validation Layer

## Purpose

Memvalidasi:

* hallucination,
* unsupported claims,
* unsafe answers.

---

# Validation Checks

## Required

* source grounding,
* citation validation,
* confidence validation,
* policy validation.

---

# Hallucination Detection

---

# Rules

AI response harus:

* grounded ke retrieval,
* punya supporting context.

---

# Example

## BAD

AI menjawab tanpa source.

---

## GOOD

AI menjawab berdasarkan:

* CP,
* buku guru,
* asesmen.

---

# Confidence Scoring

---

# Purpose

Mengukur:

* retrieval confidence,
* generation confidence.

---

# Example

```json id="confidence-example"
{
  "retrieval_confidence": 0.92,
  "generation_confidence": 0.87
}
```

---

# Low Confidence Strategy

Jika confidence rendah:

## AI wajib:

* disclaimer,
* meminta klarifikasi,
* mengurangi assertiveness.

---

# Explainability Requirements

---

# Every AI Response Must Have

✅ source traceability

✅ retrieval trace

✅ model trace

✅ prompt version

---

# Example Audit Metadata

```json id="audit-metadata"
{
  "model": "gpt-4.1",
  "prompt_version": "teacher_assistant_v2",
  "retrieved_chunks": [
    "chunk_001",
    "chunk_002"
  ]
}
```

---

# Audit Logging

---

# Mandatory Logs

## 1. Prompt Log

Menyimpan:

* input prompt,
* system prompt,
* prompt version.

---

# 2. Retrieval Log

Menyimpan:

* retrieved chunks,
* retrieval score,
* filters.

---

# 3. Generation Log

Menyimpan:

* generated output,
* model version,
* latency.

---

# 4. Moderation Log

Menyimpan:

* blocked requests,
* flagged outputs,
* safety violations.

---

# Audit Storage Rules

---

# Logs Must Be

✅ immutable

✅ searchable

✅ traceable

---

# Recommended Storage

* PostgreSQL
* object storage archive

---

# AI Identity & Versioning

---

# Every AI Response Must Include

```json id="identity-versioning"
{
  "model": "gpt-4.1",
  "model_provider": "OpenAI",
  "model_version": "2026-05"
}
```

---

# Model Governance

---

# Rules

## Semua model wajib:

✅ versioned

✅ benchmarked

✅ monitored

✅ approved sebelum production

---

# Local Model Governance

---

# Approved Local Models

Contoh:

* Mistral
* Qwen
* Llama

---

# Governance Requirements

Local models wajib:

* benchmark evaluation,
* hallucination evaluation,
* toxicity evaluation.

---

# Educational Safety Policy

---

# AI Must Avoid

❌ fabricated curriculum

❌ fake references

❌ unsupported educational claims

❌ unsafe educational guidance

---

# Required Behavior

✅ explain concept safely

✅ cite learning sources

✅ encourage critical thinking

---

# Bias Governance

---

# Risks

AI dapat menghasilkan:

* gender bias,
* cultural bias,
* socio-economic bias.

---

# Required Mitigation

✅ diverse evaluation dataset

✅ moderation review

✅ output auditing

---

# Privacy & Data Governance

---

# Rules

AI tidak boleh:

* expose sensitive data,
* leak student data,
* expose internal prompts.

---

# Sensitive Data Categories

❌ student PII

❌ teacher credentials

❌ internal tokens

---

# Required Protections

✅ encryption

✅ RBAC

✅ audit trail

✅ secure storage

---

# Access Governance

---

# Role-Based Access Control (RBAC)

## Example Roles

| Role       | Access               |
| ---------- | -------------------- |
| Student    | limited AI access    |
| Teacher    | educational AI       |
| Admin      | governance dashboard |
| AI Auditor | audit access         |

---

# AI Rate Limiting

---

# Purpose

Melindungi:

* infrastructure,
* model usage,
* abuse prevention.

---

# Example Limits

```text id="rate-limit-example"
student → 20 requests/minute
teacher → 100 requests/minute
```

---

# Human-in-the-Loop Governance

---

# Required for Critical Workflows

Contoh:

* curriculum generation,
* grading recommendation,
* assessment generation.

---

# Rules

AI tidak boleh menjadi:

* final authority,
* autonomous decision maker.

---

# AI Evaluation Framework

---

# Required Evaluation Categories

| Category              | Purpose             |
| --------------------- | ------------------- |
| Hallucination         | factual accuracy    |
| Retrieval Quality     | retrieval relevance |
| Toxicity              | harmful content     |
| Bias                  | fairness            |
| Educational Alignment | curriculum fit      |

---

# AI Benchmarking

---

# Evaluation Dataset

Wajib memiliki:

* Indonesian educational dataset,
* curriculum dataset,
* assessment dataset.

---

# Observability Requirements

---

# AI Metrics

## Required

```text id="ai-metrics"
hallucination_rate
retrieval_accuracy
response_latency
token_usage
moderation_block_rate
```

---

# OpenTelemetry Integration

Semua AI workflows wajib:

* traceable,
* correlated,
* observable.

---

# Incident Management

---

# AI Incident Categories

## Severity 1

* dangerous output,
* data leak,
* severe hallucination.

---

# Severity 2

* retrieval failure,
* model degradation.

---

# Severity 3

* latency issue,
* retry failure.

---

# AI Kill Switch

---

# Mandatory

Production AI wajib memiliki:

```text id="kill-switch"
AI emergency shutdown mechanism
```

---

# Use Cases

* dangerous output spike,
* prompt injection attack,
* hallucination outbreak.

---

# Governance Dashboard

---

# Features

✅ audit search

✅ prompt trace

✅ retrieval trace

✅ moderation logs

✅ AI metrics

---

# Recommended Stack

* Grafana
* OpenTelemetry

---

# Compliance Requirements

---

# Logs Must Store

✅ timestamps

✅ trace_id

✅ model version

✅ prompt version

✅ retrieval references

---

# Governance Anti-Patterns

---

# DO NOT

❌ hidden prompts

❌ unlogged AI responses

❌ retrieval without source

❌ AI without moderation

❌ direct LLM access from frontend

❌ non-versioned prompts

---

# Production Governance Checklist

---

# Mandatory

✅ moderation layer

✅ audit logs

✅ retrieval trace

✅ prompt versioning

✅ model versioning

✅ observability

✅ RBAC

✅ rate limiting

---

# Most Important Insight

Enterprise AI governance bukan tentang:

* compliance document,
* checkbox security,
* moderation semata.

Tetapi tentang:

```text id="governance-core"
trustworthy AI operations
```

Karena:
AI tanpa governance akan menjadi:

* tidak dapat dipercaya,
* tidak dapat diaudit,
* tidak dapat dioperasikan secara enterprise,

terutama untuk sistem pendidikan.
