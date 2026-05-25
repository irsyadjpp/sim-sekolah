# PARSER FAILURE RUNBOOK

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini mendefinisikan prosedur recovery, diagnosis, mitigation, dan escalation untuk parser failures pada Enterprise Educational AI Platform.

Parser Failure Runbook digunakan untuk:

* incident response,
* operational troubleshooting,
* pipeline recovery,
* semantic integrity protection,
* ingestion reliability.

---

# Why Parser Failures Matter

Parser adalah foundation dari:

* document understanding,
* semantic chunking,
* metadata extraction,
* educational structure analysis.

Jika parser gagal:

* chunks rusak,
* metadata salah,
* retrieval quality turun,
* hallucination meningkat.

---

# Parser Pipeline Overview

```text id="parser-pipeline-overview"
PDF
 ↓
Raw Extraction
 ↓
Document Analyzer
 ├── Text Parser
 ├── Layout Parser
 ├── Table Parser
 ├── Formula Parser
 └── Metadata Parser
 ↓
Semantic Chunk Builder
 ↓
Embedding Pipeline
```

---

# Supported Parser Components

| Component           | Responsibility       |
| ------------------- | -------------------- |
| PyMuPDF Parser      | raw extraction       |
| Unstructured Parser | semantic layout      |
| Camelot Parser      | table extraction     |
| Nougat Parser       | formula parsing      |
| Metadata Parser     | educational metadata |

---

# Parser Failure Severity Levels

| Severity | Description               |
| -------- | ------------------------- |
| SEV-1    | parser pipeline outage    |
| SEV-2    | high parser corruption    |
| SEV-3    | degraded parsing accuracy |
| SEV-4    | isolated parsing issue    |

---

# Common Parser Failure Types

```text id="parser-failure-types"
document_parse_failure
layout_parse_failure
table_parse_failure
formula_parse_failure
metadata_parse_failure
chunk_boundary_failure
encoding_failure
memory_failure
```

---

# 1. Document Parse Failure

## Symptoms

* parser crash,
* empty extraction,
* unreadable output.

---

# Example

```text id="document-parse-failure-example"
Expected:
Educational content extracted

Actual:
null
```

---

# Root Causes

| Cause                   | Example            |
| ----------------------- | ------------------ |
| corrupted PDF           | malformed document |
| unsupported PDF version | encrypted file     |
| parser exception        | library crash      |
| memory exhaustion       | huge PDF           |

---

# Recovery Steps

---

# Step 1 — Validate PDF Integrity

Gunakan:

* PyMuPDF validation,
* PDF structure inspection.

---

# Step 2 — Check Parser Logs

Cari:

* segmentation fault,
* parser exception,
* timeout.

---

# Step 3 — Retry Parsing

Gunakan:

* retry queue,
* isolated worker.

---

# Step 4 — Fallback Parser

Fallback:

* alternate extraction pipeline,
* OCR-first parsing.

---

# Step 5 — Escalate

Jika:

* repeated crash,
* parser corruption persists.

---

# 2. Layout Parse Failure

## Symptoms

* heading tidak dikenali,
* paragraph merge salah,
* educational structure hilang.

---

# Example

```text id="layout-parse-example"
Title:
“Energi Panas”

Merged incorrectly with paragraph.
```

---

# Root Causes

| Cause                   | Example       |
| ----------------------- | ------------- |
| weak layout detection   | missing title |
| scanned distortion      | rotated pages |
| inconsistent formatting | mixed layouts |

---

# Recovery Steps

---

# Step 1 — Re-run Layout Detection

Gunakan:

* Unstructured parser.

---

# Step 2 — Validate Bounding Boxes

Check:

* overlap,
* spacing,
* coordinate integrity.

---

# Step 3 — Apply Heuristics

Gunakan:

* font-size heuristics,
* indentation rules,
* spacing analysis.

---

# Step 4 — Fallback to OCR Layout

Gunakan:

* vision-based segmentation.

---

# 3. Table Parse Failure

## Symptoms

* missing rows,
* merged columns,
* rubric corruption.

---

# Example

```text id="table-parse-example"
Expected:
| indikator | nilai |

Actual:
indikatornilai
```

---

# Root Causes

| Cause                   | Example            |
| ----------------------- | ------------------ |
| complex table structure | nested table       |
| OCR flattening          | no cell boundaries |
| parser limitation       | unsupported table  |

---

# Recovery Steps

---

# Step 1 — Route to Table Parser

Gunakan:

* Camelot

---

# Step 2 — Validate Structure

Check:

* column count,
* row alignment,
* headers.

---

# Step 3 — Reconstruct Table

Gunakan:

* coordinate-based rebuilding.

---

# Step 4 — Human Validation

Mandatory untuk:

* assessment rubrics,
* competency matrices.

---

# 4. Formula Parse Failure

## Symptoms

* broken equations,
* incorrect notation,
* missing symbols.

---

# Example

```text id="formula-parse-example"
Expected:
E = mc²

Actual:
E = mcz
```

---

# Root Causes

| Cause             | Example            |
| ----------------- | ------------------ |
| generic parser    | no formula support |
| OCR confusion     | superscript loss   |
| low image quality | blurry notation    |

---

# Recovery Steps

---

# Step 1 — Route to Formula Parser

Gunakan:

* Nougat

---

# Step 2 — Validate Formula Syntax

Check:

* symbol validity,
* notation consistency.

---

# Step 3 — Formula Re-Parsing

Gunakan:

* isolated formula extraction.

---

# Step 4 — Human Verification

Mandatory untuk:

* scientific documents,
* mathematics materials.

---

# 5. Metadata Parse Failure

## Symptoms

* wrong subject,
* incorrect grade,
* missing competency tags.

---

# Example

```json id="metadata-failure-example"
{
  "grade": 8
}
```

Padahal seharusnya:

* grade 4.

---

# Root Causes

| Cause              | Example             |
| ------------------ | ------------------- |
| weak classifier    | wrong subject       |
| missing ontology   | competency mismatch |
| malformed metadata | extraction issue    |

---

# Recovery Steps

---

# Step 1 — Re-run Metadata Extraction

Gunakan:

* metadata enrichment pipeline.

---

# Step 2 — Validate Ontology Mapping

Check:

* subject hierarchy,
* competency relationships.

---

# Step 3 — Cross-Validate Metadata

Bandingkan:

* filename,
* curriculum structure,
* document source.

---

# Step 4 — Human Review

Mandatory untuk:

* official curriculum docs.

---

# 6. Chunk Boundary Failure

## Symptoms

* chunk terlalu panjang,
* chunk memotong konteks,
* educational semantics hilang.

---

# Example

```text id="chunk-boundary-example"
Activity instructions merged with assessment.
```

---

# Root Causes

| Cause            | Example                |
| ---------------- | ---------------------- |
| fixed chunking   | no semantic awareness  |
| layout failure   | incorrect segmentation |
| missing ontology | context mismatch       |

---

# Recovery Steps

---

# Step 1 — Re-run Semantic Chunking

Gunakan:

* curriculum-aware chunking.

---

# Step 2 — Validate Chunk Semantics

Check:

* chunk_type,
* topic integrity,
* competency coherence.

---

# Step 3 — Chunk Boundary Heuristics

Gunakan:

* heading boundaries,
* activity markers,
* assessment separators.

---

# 7. Encoding Failure

## Symptoms

* invalid characters,
* unicode corruption,
* unreadable text.

---

# Example

```text id="encoding-failure-example"
“kalor”
→
“kal�r”
```

---

# Root Causes

| Cause            | Example             |
| ---------------- | ------------------- |
| invalid encoding | malformed UTF       |
| parser mismatch  | unsupported charset |
| OCR corruption   | invalid symbols     |

---

# Recovery Steps

---

# Step 1 — Detect Encoding

Gunakan:

* UTF validation.

---

# Step 2 — Normalize Text

Gunakan:

* Unicode normalization,
* symbol repair.

---

# Step 3 — Reparse Source

Gunakan:

* original binary extraction.

---

# 8. Memory Failure

## Symptoms

* worker killed,
* OOM crash,
* parser timeout.

---

# Root Causes

| Cause                | Example              |
| -------------------- | -------------------- |
| huge PDF             | >1000 pages          |
| image-heavy document | excessive RAM        |
| parser leak          | memory fragmentation |

---

# Recovery Steps

---

# Step 1 — Split Document

Gunakan:

* page batching.

---

# Step 2 — Scale Workers

Increase:

* memory limits,
* worker replicas.

---

# Step 3 — Enable Streaming Parse

Gunakan:

* page-by-page parsing.

---

# Validation Strategy

---

# Validation Categories

```text id="parser-validation-categories"
structure_validation
metadata_validation
semantic_validation
formula_validation
table_validation
```

---

# Required Validation Rules

---

# Reject Parse Output If

❌ empty chunks

❌ invalid metadata

❌ corrupted formulas

❌ malformed tables

❌ broken educational structure

---

# Example Validation Metadata

```json id="parser-validation-metadata"
{
  "parser_version": "v2",
  "validation_status": "passed"
}
```

---

# Retry Strategy

---

# Retry Levels

| Retry   | Action               |
| ------- | -------------------- |
| Retry-1 | same parser          |
| Retry-2 | alternate parser     |
| Retry-3 | OCR-assisted parsing |
| Retry-4 | manual review        |

---

# Retry Flow

```text id="parser-retry-flow"
Parser Failure
      ↓
Retry Queue
      ↓
Fallback Parser
      ↓
Validation
      ↓
Success / Escalation
```

---

# Escalation Policy

---

# Escalate When

✅ parser repeatedly crashes

✅ metadata corruption detected

✅ semantic chunking invalid

✅ curriculum structure damaged

---

# Escalation Targets

| Issue               | Team                       |
| ------------------- | -------------------------- |
| parser crash        | AI Platform Team           |
| malformed document  | Ingestion Team             |
| metadata corruption | Knowledge Engineering Team |

---

# Parser Observability

---

# Required Metrics

```text id="parser-observability"
parse_success_rate
parse_failure_rate
parse_retry_rate
chunk_validation_failure
```

---

# Additional Metrics

```text id="parser-additional-metrics"
metadata_accuracy
table_parse_accuracy
formula_parse_accuracy
```

---

# Required Logs

* parser logs,
* chunk logs,
* metadata logs,
* retry logs.

---

# Parser Alerts

---

# Critical Alerts

```text id="parser-critical-alerts"
parser crash spike
chunk validation failure spike
metadata corruption detected
```

---

# Warning Alerts

```text id="parser-warning-alerts"
parsing latency increase
retry spike
layout parse degradation
```

---

# Queue Recovery

---

# Symptoms

* parser queue backlog,
* stuck parsing jobs,
* retry storms.

---

# Recovery Steps

---

# Step 1 — Inspect Queue

Check:

* queue lag,
* dead-letter queue,
* worker health.

---

# Step 2 — Scale Parser Workers

Increase:

* parsing worker replicas.

---

# Step 3 — Prioritize Critical Documents

Prioritize:

* curriculum docs,
* assessments,
* active ingestion requests.

---

# Parser Quality Assurance

---

# Mandatory QA

✅ chunk validation

✅ metadata validation

✅ formula validation

✅ educational structure validation

---

# Human Review Mandatory For

* national curriculum,
* scientific documents,
* official assessments.

---

# Parser Security Considerations

---

# Validate

✅ malformed PDFs

✅ parser exploit attempts

✅ oversized files

---

# Reject

❌ suspicious embedded objects

❌ executable payloads

❌ invalid document structures

---

# Production Recovery Checklist

---

# Mandatory

✅ parser retry queue

✅ fallback parsers

✅ validation engine

✅ parser observability

✅ escalation workflow

✅ semantic validation

---

# Anti-Patterns

---

# DO NOT

❌ trust parser blindly

❌ use fixed chunking only

❌ ignore metadata validation

❌ flatten educational structure

❌ skip semantic validation

---

# Most Important Insight

Enterprise parser engineering bukan tentang:

```text id="wrong-parser-thinking"
extracting document text
```

Tetapi tentang:

```text id="correct-parser-thinking"
preserving educational semantic structure
```

Karena:
parser quality menentukan:

* semantic chunk quality,
* retrieval precision,
* metadata integrity,
* curriculum alignment,
* AI grounding reliability.
