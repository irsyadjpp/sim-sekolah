# EDUCATIONAL METADATA STANDARD

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini mendefinisikan standar metadata pendidikan untuk seluruh Enterprise Educational AI Platform.

Metadata adalah:

```text id="metadata-definition"
educational intelligence layer
```

yang menentukan:

* retrieval quality,
* explainability,
* filtering,
* AI reasoning,
* governance,
* curriculum alignment.

---

# Why Metadata Matters

Pada enterprise educational AI systems:

```text id="metadata-core"
metadata > raw text
```

Karena AI retrieval modern membutuhkan:

* semantic filtering,
* educational hierarchy,
* pedagogical context,
* curriculum understanding.

---

# Core Objectives

---

# 1. Curriculum Alignment

Metadata harus memahami:

* CP,
* ATP,
* phase,
* grade,
* competency.

---

# 2. Pedagogical Intelligence

Metadata harus memahami:

* activity,
* reflection,
* inquiry,
* assessment.

---

# 3. Retrieval Optimization

Metadata harus:

* searchable,
* filterable,
* explainable.

---

# 4. AI Explainability

AI response harus dapat menjelaskan:

* source,
* competency,
* educational relevance.

---

# Core Metadata Principles

---

# 1. Metadata Must Be Structured

Metadata tidak boleh:

* random,
* inconsistent,
* untyped.

---

# GOOD

```json id="structured-metadata"
{
  "subject": "IPA",
  "grade": 4
}
```

---

# BAD

```json id="bad-metadata"
{
  "tag": "science maybe"
}
```

---

# 2. Metadata Must Be Consistent

Gunakan:

* controlled vocabulary,
* standardized taxonomy.

---

# 3. Metadata Must Be Queryable

Metadata harus compatible dengan:

* Qdrant filtering,
* retrieval pipelines,
* analytics.

---

# 4. Metadata Must Be Explainable

AI wajib dapat menjelaskan:

* kenapa chunk dipilih,
* competency terkait,
* educational relevance.

---

# Metadata Architecture

```text id="metadata-architecture"
Raw Content
     ↓
Structural Metadata
     ↓
Educational Metadata
     ↓
Pedagogical Metadata
     ↓
AI-Enriched Metadata
     ↓
Retrieval Metadata
```

---

# Metadata Categories

---

# 1. Document Metadata

## Purpose

Identitas dokumen.

---

# Required Fields

```json id="document-metadata"
{
  "document_id": "uuid",
  "document_type": "buku_guru",
  "source": "kemdikbud",
  "language": "id"
}
```

---

# Standard Fields

| Field         | Type     |
| ------------- | -------- |
| document_id   | string   |
| document_type | string   |
| source        | string   |
| language      | string   |
| upload_date   | datetime |

---

# Supported Document Types

```text id="document-types"
cp
atp
buku_guru
buku_siswa
modul_ajar
asesmen
p5
```

---

# 2. Curriculum Metadata

## Purpose

Representasi struktur kurikulum.

---

# Required Fields

```json id="curriculum-metadata"
{
  "subject": "IPA",
  "phase": "B",
  "grade": 4,
  "semester": 1
}
```

---

# Standard Fields

| Field              | Description     |
| ------------------ | --------------- |
| subject            | mata pelajaran  |
| phase              | fase kurikulum  |
| grade              | tingkat kelas   |
| semester           | semester        |
| curriculum_version | versi kurikulum |

---

# Subject Standardization

---

# Example

```text id="subject-standardization"
IPA
IPS
Matematika
Bahasa Indonesia
```

---

# Avoid

❌ science

❌ math

❌ bahasa indo

---

# 3. Competency Metadata

## Purpose

Representasi competency hierarchy.

---

# Required Fields

```json id="competency-metadata"
{
  "cp_code": "CP-IPA-B-01",
  "competency": "Memahami energi panas"
}
```

---

# Optional Fields

```json id="optional-competency"
{
  "learning_objective": "",
  "indicator": ""
}
```

---

# Competency Relationships

```text id="competency-relationships"
CP
 ↓
ATP
 ↓
Learning Objective
 ↓
Activity
 ↓
Assessment
```

---

# 4. Pedagogical Metadata

## Purpose

Memahami instructional design.

---

# Required Fields

```json id="pedagogical-metadata"
{
  "pedagogy_type": "inquiry",
  "learning_style": ["visual"]
}
```

---

# Supported Pedagogy Types

```text id="pedagogy-types"
inquiry
project-based
discussion
reflection
experiment
lecture
collaborative
```

---

# Learning Style Tags

```text id="learning-style-tags"
visual
auditory
kinesthetic
reading
```

---

# 5. Chunk Metadata

## Purpose

Representasi semantic chunk.

---

# Required Fields

```json id="chunk-metadata"
{
  "chunk_id": "uuid",
  "chunk_type": "activity",
  "sequence_order": 3
}
```

---

# Supported Chunk Types

```text id="chunk-types-list"
concept
activity
assessment
reflection
experiment
table
formula
diagram
```

---

# Chunk Hierarchy

```text id="chunk-hierarchy"
chapter
 └── topic
      └── chunk
```

---

# 6. Assessment Metadata

## Purpose

Representasi evaluasi pembelajaran.

---

# Required Fields

```json id="assessment-metadata"
{
  "assessment_type": "multiple_choice",
  "difficulty_level": "medium"
}
```

---

# Supported Assessment Types

```text id="assessment-types"
multiple_choice
essay
rubric
performance
observation
quiz
```

---

# Difficulty Levels

```text id="difficulty-levels"
easy
medium
hard
```

---

# 7. Bloom Taxonomy Metadata

## Purpose

Representasi cognitive level.

---

# Required Fields

```json id="taxonomy-metadata"
{
  "taxonomy_level": "analyze"
}
```

---

# Supported Levels

```text id="taxonomy-levels"
remember
understand
apply
analyze
evaluate
create
```

---

# 8. Multi-Modal Metadata

## Purpose

Representasi content multimodal.

---

# Image Metadata

```json id="image-metadata-standard"
{
  "image_type": "diagram",
  "caption": "Perpindahan panas"
}
```

---

# Formula Metadata

```json id="formula-metadata"
{
  "formula_type": "physics",
  "formula_topic": "force"
}
```

---

# Table Metadata

```json id="table-metadata"
{
  "table_type": "rubric",
  "row_count": 5
}
```

---

# 9. AI-Enriched Metadata

## Purpose

AI-generated educational intelligence.

---

# Example

```json id="ai-enriched-metadata"
{
  "semantic_topic": "Energi Panas",
  "retrieval_priority": "high",
  "confidence_score": 0.92
}
```

---

# AI Metadata Fields

| Field              | Purpose               |
| ------------------ | --------------------- |
| semantic_topic     | topic grouping        |
| confidence_score   | extraction confidence |
| retrieval_priority | retrieval weighting   |
| semantic_density   | information density   |

---

# 10. Governance Metadata

## Purpose

Auditability & traceability.

---

# Required Fields

```json id="governance-metadata"
{
  "pipeline_version": "v2",
  "embedding_model": "bge-m3"
}
```

---

# Additional Fields

```json id="governance-extra"
{
  "trace_id": "uuid",
  "processing_timestamp": "ISO8601"
}
```

---

# Metadata Schema Standard

---

# Recommended Structure

```json id="recommended-metadata-schema"
{
  "document": {},
  "curriculum": {},
  "pedagogical": {},
  "chunk": {},
  "assessment": {},
  "AI": {},
  "governance": {}
}
```

---

# Qdrant Metadata Strategy

## Purpose

Optimized filtering & retrieval.

---

# Example

```json id="qdrant-filter-example"
{
  "subject": "IPA",
  "grade": 4,
  "chunk_type": "activity"
}
```

---

# Required Filter Fields

## Mandatory

```text id="required-filter-fields"
subject
grade
phase
chunk_type
document_type
```

---

# Metadata Validation Rules

---

# Rules

## Metadata wajib:

✅ typed

✅ validated

✅ normalized

✅ versioned

---

# Validation Example

## GOOD

```json id="validation-good"
{
  "grade": 4
}
```

---

# BAD

```json id="validation-bad"
{
  "grade": "empat"
}
```

---

# Metadata Versioning

---

# Purpose

Schema evolution.

---

# Example

```json id="metadata-versioning"
{
  "metadata_version": "v2"
}
```

---

# Metadata Relationships

---

# Purpose

Educational graph construction.

---

# Example

```text id="metadata-relationships"
activity → competency
assessment → learning objective
diagram → concept
```

---

# Metadata Enrichment Pipeline

```text id="metadata-enrichment-pipeline"
Raw Chunk
     ↓
Curriculum Detection
     ↓
Pedagogical Classification
     ↓
Difficulty Classification
     ↓
Taxonomy Classification
     ↓
Metadata Validation
```

---

# Metadata Quality Metrics

---

# Required Metrics

| Metric                | Purpose                     |
| --------------------- | --------------------------- |
| metadata_accuracy     | extraction accuracy         |
| metadata_completeness | field completeness          |
| filter_precision      | retrieval filtering quality |
| semantic_alignment    | educational consistency     |

---

# Observability Requirements

---

# Required Logs

* metadata extraction logs,
* classification logs,
* enrichment logs.

---

# Required Metrics

```text id="metadata-metrics"
metadata_failure_rate
taxonomy_accuracy
classification_latency
```

---

# Security Requirements

---

# Metadata Must Not Contain

❌ secrets

❌ raw credentials

❌ sensitive PII

---

# Access Rules

Metadata filtering harus:

* RBAC-aware,
* tenant-aware.

---

# Governance Requirements

---

# Metadata Must Be

✅ explainable

✅ traceable

✅ reproducible

---

# AI Explainability Example

```json id="ai-explainability-example"
{
  "reason_selected": [
    "subject match",
    "grade match",
    "taxonomy relevance"
  ]
}
```

---

# Anti-Patterns

---

# DO NOT

❌ inconsistent subject naming

❌ free-text metadata chaos

❌ metadata without schema

❌ missing chunk type

❌ mixing business metadata & AI metadata

---

# Production Readiness Checklist

---

# Mandatory

✅ metadata schema

✅ metadata validation

✅ metadata versioning

✅ Qdrant filtering support

✅ educational taxonomy

✅ audit metadata

---

# Most Important Insight

Enterprise educational AI retrieval bukan tentang:

```text id="wrong-retrieval-focus"
semantic search only
```

Tetapi tentang:

```text id="correct-retrieval-focus"
metadata-driven educational intelligence
```

Karena:
metadata menentukan:

* retrieval precision,
* explainability,
* curriculum alignment,
* AI reasoning quality.
