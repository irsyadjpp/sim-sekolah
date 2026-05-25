# OCR FAILURE RUNBOOK

## Enterprise Educational AI Platform

---

# Purpose

Dokumen ini mendefinisikan prosedur recovery, diagnosis, mitigation, dan escalation untuk OCR failures pada Enterprise Educational AI Platform.

OCR Failure Runbook digunakan untuk:

* incident response,
* operational recovery,
* troubleshooting,
* observability,
* AI reliability.

---

# Why OCR Failure Matters

OCR adalah foundation dari:

* ingestion pipeline,
* retrieval quality,
* educational understanding,
* semantic chunking.

Jika OCR gagal:

* embeddings rusak,
* retrieval buruk,
* hallucination meningkat,
* AI grounding gagal.

---

# OCR Failure Definition

OCR failure adalah kondisi ketika:

* text extraction gagal,
* formula extraction rusak,
* layout detection gagal,
* image text tidak terbaca,
* OCR output corrupted.

---

# OCR Pipeline Overview

```text id="ocr-pipeline-overview"
PDF
 ↓
Document Analyzer
 ├── Text Extractor
 ├── OCR Engine
 ├── Layout Detector
 ├── Formula Extractor
 └── Image Processor
 ↓
OCR Validation
 ↓
Semantic Chunk Builder
```

---

# OCR Components

| Component         | Responsibility          |
| ----------------- | ----------------------- |
| OCR Engine        | text recognition        |
| Layout Detector   | structure understanding |
| Formula Extractor | formula parsing         |
| Image OCR         | embedded image text     |
| Validation Engine | OCR quality validation  |

---

# Supported OCR Engines

| Engine        | Use Case         |
| ------------- | ---------------- |
| Tesseract     | basic OCR        |
| PaddleOCR     | multilingual OCR |
| Nougat        | scientific OCR   |
| GPT-4o Vision | fallback OCR     |
| Qwen-VL       | multimodal OCR   |

---

# Failure Severity Levels

| Severity | Description           |
| -------- | --------------------- |
| SEV-1    | OCR pipeline outage   |
| SEV-2    | high OCR corruption   |
| SEV-3    | degraded OCR accuracy |
| SEV-4    | isolated OCR issue    |

---

# Common OCR Failure Types

```text id="ocr-failure-types"
text_missing
corrupted_text
formula_failure
table_corruption
layout_failure
language_detection_failure
image_ocr_failure
```

---

# 1. Missing Text

## Symptoms

* extracted text kosong,
* halaman hilang,
* chunk kosong.

---

# Example

```text id="missing-text-example"
Expected:
“Energi panas adalah…”

Actual:
“”
```

---

# Root Causes

| Cause                | Example          |
| -------------------- | ---------------- |
| scanned PDF          | image-only PDF   |
| OCR timeout          | worker overload  |
| unsupported encoding | malformed PDF    |
| corrupted file       | invalid document |

---

# Recovery Steps

## Step 1 — Validate PDF

Gunakan:

* PyMuPDF validation,
* PDF integrity check.

---

# Step 2 — Check OCR Logs

Cari:

* timeout,
* parser exception,
* memory issue.

---

# Step 3 — Retry OCR

Gunakan:

* retry queue,
* fallback OCR engine.

---

# Step 4 — Escalate to Vision OCR

Fallback:

* GPT-4o Vision,
* Qwen-VL.

---

# 2. Corrupted Text

## Symptoms

* karakter rusak,
* kata acak,
* spacing aneh.

---

# Example

```text id="corrupted-text-example"
Expected:
“Perpindahan panas”

Actual:
“P3rp1nd4han p4n45”
```

---

# Root Causes

| Cause                 | Example             |
| --------------------- | ------------------- |
| low-quality scan      | blurry PDF          |
| OCR language mismatch | wrong OCR model     |
| compression artifacts | scanned image issue |

---

# Recovery Steps

---

# Step 1 — Enable Image Preprocessing

Gunakan:

* denoise,
* contrast enhancement,
* sharpening.

---

# Step 2 — Validate OCR Language

Pastikan:

* Bahasa Indonesia model aktif.

---

# Step 3 — Reprocess with Better OCR

Gunakan:

* PaddleOCR,
* Vision OCR fallback.

---

# 3. Formula Extraction Failure

## Symptoms

* formula hilang,
* notation rusak,
* mathematical symbols incorrect.

---

# Example

```text id="formula-failure-example"
Expected:
F = m × a

Actual:
F = m x q
```

---

# Root Causes

| Cause                      | Example             |
| -------------------------- | ------------------- |
| OCR unsuitable for formula | generic OCR         |
| low resolution             | blurry formula      |
| unsupported notation       | scientific notation |

---

# Recovery Steps

---

# Step 1 — Route to Formula Pipeline

Gunakan:

* Nougat

---

# Step 2 — Validate Formula Confidence

Check:

* symbol confidence,
* notation consistency.

---

# Step 3 — Enable Formula Re-OCR

Retry:

* formula-only extraction.

---

# Step 4 — Human Review

Mandatory untuk:

* assessments,
* scientific materials.

---

# 4. Table Corruption

## Symptoms

* kolom hilang,
* row merge salah,
* rubric rusak.

---

# Example

```text id="table-corruption-example"
Expected:
| indikator | nilai |

Actual:
indikator nilai
```

---

# Root Causes

| Cause                    | Example               |
| ------------------------ | --------------------- |
| OCR flattening           | table jadi plain text |
| layout detection failure | row mismatch          |
| complex PDF structure    | nested tables         |

---

# Recovery Steps

---

# Step 1 — Route to Table Extractor

Gunakan:

* Camelot

---

# Step 2 — Validate Table Structure

Check:

* row count,
* column count,
* header consistency.

---

# Step 3 — Rebuild Table Structure

Gunakan:

* layout-aware reconstruction.

---

# 5. Layout Detection Failure

## Symptoms

* heading tidak terdeteksi,
* paragraph merge,
* chunk boundaries salah.

---

# Example

```text id="layout-failure-example"
Title + body merged incorrectly.
```

---

# Root Causes

| Cause                    | Example           |
| ------------------------ | ----------------- |
| poor layout model        | weak segmentation |
| scanned image distortion | rotated scan      |
| mixed formatting         | inconsistent PDF  |

---

# Recovery Steps

---

# Step 1 — Re-run Layout Analysis

Gunakan:

* Unstructured layout detection.

---

# Step 2 — Enable Coordinate Validation

Check:

* bounding boxes,
* block overlap.

---

# Step 3 — Apply Layout Heuristics

Gunakan:

* font-size rules,
* spacing heuristics.

---

# 6. Language Detection Failure

## Symptoms

* OCR menghasilkan bahasa salah,
* transliteration rusak.

---

# Example

```text id="language-failure-example"
“kalor”
→
“kator”
```

---

# Root Causes

| Cause                  | Example          |
| ---------------------- | ---------------- |
| multilingual mismatch  | OCR English-only |
| scientific terminology | domain confusion |

---

# Recovery Steps

---

# Step 1 — Enable Indonesian OCR

Gunakan:

* Indonesian OCR model.

---

# Step 2 — Enable Dictionary Validation

Check:

* curriculum vocabulary,
* educational terminology.

---

# Step 3 — Post-OCR Correction

Gunakan:

* spelling normalization,
* curriculum ontology matching.

---

# OCR Validation Strategy

---

# Validation Categories

```text id="ocr-validation-categories"
text_validation
formula_validation
table_validation
layout_validation
language_validation
```

---

# OCR Confidence Thresholds

| OCR Type    | Threshold |
| ----------- | --------- |
| text OCR    | > 90%     |
| formula OCR | > 95%     |
| table OCR   | > 92%     |

---

# OCR Validation Rules

---

# Reject OCR Output If

❌ empty content

❌ confidence too low

❌ corrupted symbols

❌ invalid formula structure

---

# Example Validation Metadata

```json id="ocr-validation-metadata"
{
  "ocr_confidence": 0.91,
  "language": "id"
}
```

---

# OCR Retry Strategy

---

# Retry Levels

| Retry   | Action                 |
| ------- | ---------------------- |
| Retry-1 | same OCR engine        |
| Retry-2 | alternative OCR engine |
| Retry-3 | vision OCR             |
| Retry-4 | manual review          |

---

# OCR Retry Flow

```text id="ocr-retry-flow"
OCR Failure
    ↓
Retry Queue
    ↓
Fallback OCR
    ↓
Validation
    ↓
Success / Escalation
```

---

# OCR Escalation Policy

---

# Escalate When

✅ repeated OCR failure

✅ scientific notation corrupted

✅ educational content unreadable

✅ retrieval grounding affected

---

# Escalation Targets

| Issue            | Team                |
| ---------------- | ------------------- |
| OCR engine crash | AI Platform Team    |
| corrupted PDF    | Ingestion Team      |
| formula failure  | Scientific OCR Team |

---

# OCR Observability

---

# Required Metrics

```text id="ocr-observability"
ocr_success_rate
ocr_failure_rate
ocr_retry_rate
ocr_confidence_average
```

---

# Additional Metrics

```text id="ocr-additional-metrics"
formula_ocr_accuracy
table_extraction_accuracy
layout_detection_accuracy
```

---

# Required Logs

* OCR logs,
* retry logs,
* validation logs,
* OCR confidence logs.

---

# OCR Alerts

---

# Critical Alerts

```text id="ocr-critical-alerts"
OCR success rate < 80%
formula OCR failure spike
OCR queue backlog
```

---

# Warning Alerts

```text id="ocr-warning-alerts"
OCR latency increase
confidence degradation
retry spike
```

---

# OCR Queue Recovery

---

# Symptoms

* OCR backlog,
* stuck jobs,
* retry storms.

---

# Recovery Steps

---

# Step 1 — Inspect Queue

Check:

* queue lag,
* DLQ growth.

---

# Step 2 — Scale OCR Workers

Increase:

* OCR worker replicas.

---

# Step 3 — Prioritize Critical Documents

Prioritize:

* assessments,
* curriculum documents.

---

# OCR Quality Assurance

---

# Mandatory QA

✅ sample validation

✅ educational terminology validation

✅ formula validation

✅ table validation

---

# Human Review Rules

Mandatory untuk:

* national curriculum,
* assessments,
* scientific materials.

---

# OCR Security Considerations

---

# Validate

✅ malicious PDFs

✅ oversized documents

✅ malformed images

---

# Reject

❌ executable content

❌ suspicious embedded objects

---

# Production Recovery Checklist

---

# Mandatory

✅ OCR retry queue

✅ fallback OCR engines

✅ OCR observability

✅ validation engine

✅ escalation workflow

✅ confidence thresholds

---

# Anti-Patterns

---

# DO NOT

❌ trust OCR blindly

❌ flatten tables into text

❌ use generic OCR for formulas

❌ skip validation

❌ ignore low-confidence OCR

---

# Most Important Insight

Enterprise OCR engineering bukan tentang:

```text id="wrong-ocr-thinking"
extracting text from PDFs
```

Tetapi tentang:

```text id="correct-ocr-thinking"
preserving educational semantic integrity
```

Karena:
OCR quality menentukan:

* chunk quality,
* retrieval quality,
* AI grounding,
* hallucination rate,
* educational correctness.
