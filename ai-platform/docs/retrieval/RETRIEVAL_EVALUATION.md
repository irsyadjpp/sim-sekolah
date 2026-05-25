# RETRIEVAL EVALUATION

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini mendefinisikan metodologi evaluasi retrieval untuk Enterprise Educational AI Platform.

Retrieval evaluation adalah:

```text id="retrieval-evaluation-definition"
systematic measurement of retrieval quality
```

untuk memastikan:

* retrieval relevan,
* retrieval akurat,
* hallucination rendah,
* curriculum alignment tinggi,
* AI grounding kuat.

---

# Why Retrieval Evaluation Matters

Dalam RAG systems:

```text id="retrieval-evaluation-core"
bad retrieval = bad AI
```

LLM terbaik sekalipun akan gagal jika:

* context salah,
* retrieval noisy,
* metadata mismatch,
* chunk tidak relevan.

---

# Core Objectives

---

# 1. Measure Retrieval Quality

Evaluasi:

* precision,
* recall,
* relevance.

---

# 2. Reduce Hallucination

Mengukur:

* unsupported generation,
* retrieval grounding quality.

---

# 3. Validate Curriculum Alignment

Memastikan:

* educational relevance,
* competency alignment.

---

# 4. Support Continuous Improvement

Evaluation harus:

* repeatable,
* benchmarkable,
* automatable.

---

# Evaluation Principles

---

# 1. Retrieval Must Be Measurable

Semua retrieval wajib:

* scored,
* benchmarked,
* monitored.

---

# 2. Evaluation Must Be Educationally Aware

Retrieval bukan sekadar:

* semantic similarity.

Tetapi:

* curriculum relevance,
* competency correctness,
* pedagogical fit.

---

# 3. Hallucination is a Retrieval Problem

Sebagian besar hallucination berasal dari:

* retrieval failure,
* grounding failure.

---

# 4. Human Evaluation Remains Important

Automated evaluation saja tidak cukup.

Karena educational systems membutuhkan:

* pedagogical review,
* curriculum validation.

---

# High-Level Evaluation Architecture

```text id="evaluation-architecture"
Benchmark Dataset
        ↓
Retrieval Pipeline
        ↓
Retrieved Candidates
        ↓
Evaluation Engine
 ├── Precision Metrics
 ├── Recall Metrics
 ├── Ranking Metrics
 ├── Hallucination Metrics
 └── Curriculum Metrics
        ↓
Evaluation Reports
```

---

# Evaluation Categories

```text id="evaluation-categories"
Recall Evaluation
Precision Evaluation
Ranking Evaluation
Hallucination Evaluation
Curriculum Evaluation
Human Evaluation
```

---

# 1. Recall Metrics

## Purpose

Mengukur:

* seberapa banyak relevant chunks berhasil ditemukan.

---

# Why Recall Matters

Jika retrieval gagal menemukan:

* competency,
* explanation,
* assessment,

maka AI tidak memiliki grounding yang cukup.

---

# Core Recall Metrics

| Metric         | Purpose                              |
| -------------- | ------------------------------------ |
| Recall@K       | relevant chunk ditemukan dalam top-K |
| Coverage Rate  | cakupan competency                   |
| Context Recall | retrieval completeness               |

---

# Recall@K

## Definition

Persentase query di mana relevant chunk ditemukan dalam top-K retrieval.

---

# Example

```text id="recall-example"
Top-5 retrieval:
4 relevant chunks ditemukan
```

---

# Formula

Recall@K = \frac{RelevantRetrieved}{TotalRelevant}

---

# Recommended Targets

| Metric    | Target |
| --------- | ------ |
| Recall@5  | > 85%  |
| Recall@10 | > 92%  |

---

# Educational Recall Example

## Query

```text id="educational-recall-query"
jelaskan perpindahan panas
```

Relevant chunks:

* concept,
* experiment,
* diagram,
* assessment.

---

# Retrieval dianggap gagal jika:

* concept ditemukan,
* tetapi experiment hilang.

---

# 2. Precision Metrics

## Purpose

Mengukur:

* seberapa relevan retrieval results.

---

# Why Precision Matters

High recall tanpa precision menghasilkan:

* noisy context,
* hallucination risk,
* context pollution.

---

# Core Precision Metrics

| Metric             | Purpose          |
| ------------------ | ---------------- |
| Precision@K        | relevansi top-K  |
| Context Precision  | kualitas context |
| Metadata Precision | filter accuracy  |

---

# Formula

Precision@K = \frac{RelevantRetrieved}{TotalRetrieved}

---

# Example

```text id="precision-example"
Top-5 chunks:
4 relevant
1 unrelated

Precision@5 = 0.8
```

---

# Recommended Targets

| Metric       | Target |
| ------------ | ------ |
| Precision@5  | > 80%  |
| Precision@10 | > 70%  |

---

# Educational Precision Rules

Relevant chunks harus:

* sesuai subject,
* sesuai grade,
* sesuai competency.

---

# BAD Example

## Query

```text id="bad-precision-query"
IPA kelas 4 energi panas
```

Retrieval:

* IPA kelas 8.

→ precision failure.

---

# 3. Ranking Metrics

## Purpose

Mengukur:

* kualitas reranking.

---

# Why Ranking Matters

Relevant chunk harus:

* muncul lebih awal,
* diprioritaskan.

---

# Core Ranking Metrics

| Metric         | Purpose                |
| -------------- | ---------------------- |
| MRR            | Mean Reciprocal Rank   |
| NDCG           | ranking quality        |
| Top-1 Accuracy | best chunk correctness |

---

# Mean Reciprocal Rank (MRR)

## Formula

MRR = \frac{1}{|Q|}\sum_{i=1}^{|Q|}\frac{1}{rank_i}

---

# NDCG

## Purpose

Mengukur:

* ranking usefulness,
* graded relevance.

---

# Why Important

Karena:
beberapa chunks:

* lebih penting,
* lebih educationally relevant.

---

# Example

```text id="ranking-example"
Chunk A:
exact competency match

Chunk B:
general explanation

Chunk A harus lebih tinggi.
```

---

# 4. Hallucination Scoring

## Purpose

Mengukur:

* unsupported generation,
* grounding quality.

---

# Hallucination Definition

```text id="hallucination-definition"
generated content unsupported by retrieved evidence
```

---

# Hallucination Categories

| Type                  | Example         |
| --------------------- | --------------- |
| fabricated competency | CP palsu        |
| unsupported fact      | fakta tidak ada |
| invented citation     | sumber palsu    |
| curriculum mismatch   | grade salah     |

---

# Hallucination Scoring Formula

HallucinationRate = \frac{UnsupportedClaims}{TotalClaims}

---

# Example

## AI Output

```text id="hallucination-example"
“Kurikulum menyatakan energi panas diajarkan di kelas 2.”
```

Padahal tidak ada retrieval evidence.

→ hallucination.

---

# Recommended Target

| Metric             | Target |
| ------------------ | ------ |
| Hallucination Rate | < 3%   |

---

# Hallucination Detection Strategy

---

# Automated Detection

Gunakan:

* claim verification,
* retrieval overlap checking.

---

# Human Validation

Mandatory untuk:

* curriculum outputs,
* assessments,
* educational recommendations.

---

# Groundedness Evaluation

## Purpose

Mengukur:

* seberapa grounded AI terhadap retrieval context.

---

# Formula

Groundedness = \frac{SupportedClaims}{TotalClaims}

---

# Recommended Target

| Metric       | Target |
| ------------ | ------ |
| Groundedness | > 95%  |

---

# 5. Benchmark Dataset

## Purpose

Dataset standar untuk evaluasi retrieval.

---

# Benchmark Dataset Components

```text id="benchmark-components"
queries
golden chunks
expected metadata
expected citations
```

---

# Benchmark Query Categories

| Category   | Example                     |
| ---------- | --------------------------- |
| factual    | “apa itu kalor”             |
| retrieval  | “materi sebelum kalor”      |
| assessment | “buat soal energi panas”    |
| diagram    | “diagram perpindahan panas” |

---

# Golden Dataset Example

```json id="golden-dataset-example"
{
  "query": "energi panas",
  "expected_chunks": [
    "chunk_001",
    "chunk_002"
  ]
}
```

---

# Benchmark Dataset Rules

Dataset wajib:

* manually validated,
* curriculum-aligned,
* versioned.

---

# Benchmark Coverage

---

# Must Cover

✅ all subjects

✅ all grades

✅ all chunk types

✅ multimodal retrieval

---

# Evaluation Dataset Types

---

# 1. Public Dataset

Untuk:

* generic retrieval benchmarking.

---

# 2. Internal Dataset

Untuk:

* curriculum evaluation,
* production testing.

---

# 3. Adversarial Dataset

Untuk:

* prompt injection,
* retrieval poisoning,
* hallucination testing.

---

# Educational Evaluation Strategy

---

# Educational Metrics

| Metric               | Purpose                |
| -------------------- | ---------------------- |
| curriculum_alignment | competency correctness |
| pedagogy_alignment   | teaching relevance     |
| grade_alignment      | age appropriateness    |

---

# Example

## Query

```text id="educational-evaluation-example"
jelaskan gaya untuk kelas 4
```

Failure jika:

* explanation terlalu advanced.

---

# Metadata Evaluation

## Purpose

Mengukur:

* metadata filter quality.

---

# Metrics

```text id="metadata-evaluation-metrics"
metadata_precision
filter_accuracy
taxonomy_alignment
```

---

# Multi-Modal Evaluation

---

# Evaluate

✅ image retrieval

✅ formula retrieval

✅ table retrieval

---

# Example

```text id="multimodal-evaluation"
diagram konduksi
```

Harus menemukan:

* relevant image chunks.

---

# Reranker Evaluation

## Purpose

Mengukur:

* reranking quality.

---

# Metrics

```text id="reranker-metrics"
reranker_accuracy
top1_accuracy
ranking_consistency
```

---

# Latency Evaluation

## Purpose

Mengukur retrieval performance.

---

# Required Metrics

| Metric            | Target  |
| ----------------- | ------- |
| retrieval_latency | < 500ms |
| reranking_latency | < 200ms |

---

# Cost Evaluation

---

# Evaluate

✅ token usage

✅ reranker inference cost

✅ GPU utilization

---

# Observability Requirements

---

# Required Metrics

```text id="evaluation-observability"
retrieval_precision
retrieval_recall
hallucination_rate
groundedness_score
```

---

# Required Logs

* retrieval evaluation logs,
* reranking logs,
* hallucination detection logs.

---

# Human Evaluation Workflow

```text id="human-evaluation-workflow"
AI Output
   ↓
Curriculum Reviewer
   ↓
Pedagogical Validation
   ↓
Evaluation Score
```

---

# Governance Requirements

---

# Evaluation Must Be

✅ reproducible

✅ traceable

✅ benchmarked

---

# Required Metadata

```json id="evaluation-governance"
{
  "evaluation_version": "v1",
  "benchmark_dataset": "edu_retrieval_v2"
}
```

---

# Continuous Evaluation Strategy

---

# Evaluate

✅ before deployment

✅ after model change

✅ after chunking change

✅ after embedding change

---

# Regression Testing

Mandatory ketika:

* retrieval pipeline berubah,
* reranker berubah,
* metadata schema berubah.

---

# Security Evaluation

---

# Evaluate

✅ prompt injection resistance

✅ retrieval poisoning resistance

✅ tenant isolation

---

# Anti-Patterns

---

# DO NOT

❌ evaluate only semantic similarity

❌ ignore curriculum alignment

❌ ignore hallucination metrics

❌ benchmark only on generic datasets

❌ deploy retrieval changes without regression testing

---

# Production Readiness Checklist

---

# Mandatory

✅ recall metrics

✅ precision metrics

✅ ranking metrics

✅ hallucination scoring

✅ benchmark dataset

✅ human evaluation

✅ regression testing

---

# Most Important Insight

Enterprise retrieval evaluation bukan tentang:

```text id="wrong-evaluation-focus"
did the vector search work?
```

Tetapi tentang:

```text id="correct-evaluation-focus"
did the AI retrieve the correct educational knowledge reliably?
```

Karena:
AI quality ditentukan oleh:

* retrieval grounding,
* curriculum relevance,
* educational precision,
* hallucination control.
