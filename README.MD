
# AI Study Assistant

A modular RAG pipeline built from scratch in Python—featuring hybrid native + OCR PDF extraction, page-level confidence scoring, and extraction telemetry—without hiding behind heavy frameworks like LangChain or vector databases.

## Why This Project Exists (TL;DR for Reviewers)

Most RAG tutorials assume every PDF has clean, selectable digital text and wrap everything in black-box abstractions. Real-world documents don't work like that—they mix digital text with scanned pages, low-resolution images, and noisy formatting.

I built AI Study Assistant from scratch across 5 independent modules to understand and debug every stage of a document Q&A pipeline:

- **Hybrid Ingestion (`pdf_reader.py`):** Evaluates every page individually—extracting native text via PyPDF2 when available, and automatically falling back to pypdfium2 + RapidOCR when a page is scanned or image-only.
- **Confidence & Observability Telemetry:** Logs per-page extraction method (`native_text` vs. `ocr_fallback`), character count, mean OCR confidence score, end-to-end latency (ms), and flags pages below 0.70 confidence for human review.
- **Zero-Framework RAG Core (`retriever.py` & `llm.py`):** Implements text normalization, overlapping fixed-size chunking, stop-word-filtered set-intersection scoring, Top-K context aggregation, and grounded Gemini generation cleanly separated from ingestion.

## Sample Telemetry Output

When ingesting a mixed or scanned document, `main.py` prints page-level extraction diagnostics before running retrieval:

```text
--- Extraction Telemetry ---
Pages: 2 total | 1 native | 1 OCR fallback | Avg OCR Conf: 91.4% | Latency: 384.2ms
  Page 1: native_text (1420 chars, conf=1.00)
  Page 2: ocr_fallback (412 chars, conf=0.91)
```

If an OCR page drops below 0.70 confidence, it logs `[WARN: Low confidence - flag for human review]` so downstream answers aren't trusted blindly.

## Architecture & Data Flow

```text
Input PDF
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│                 Hybrid PDF Extraction                    │
│  Per-page check: native text >= 50 chars?                │
│   ├── YES → PyPDF2 native extraction (conf = 1.00)       │
│   └── NO  → pypdfium2 render (2x) → RapidOCR fallback    │
│             + page confidence & latency telemetry        │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│                     Text Cleaning                        │
│  Regex pipeline: removes noise, normalizes whitespace    │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│                       Chunking                           │
│  Fixed-size character windows with overlap               │
└────────────────────────────┬─────────────────────────────┘
                             │
                       User Question
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│               Query Cleaning & Stop Words                │
│  Lowercasing, punctuation strip, signal-word filtering   │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│             Relevance Scoring & Top-K Retrieval          │
│  Set-based keyword overlap → Top 3 chunks aggregated     │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│              Prompt Assembly & Gemini API                │
│  Grounded answer generation from retrieved context       │
└──────────────────────────────────────────────────────────┘
```

## Project Structure

```text
ai-study-assistant/
│
├── main.py             # Entry point — prints extraction telemetry & orchestrates RAG
├── pdf_reader.py       # Hybrid PDF extraction (PyPDF2 + pypdfium2/RapidOCR + confidence logs)
├── utils.py            # Regex text cleaning and preprocessing utilities
├── retriever.py        # Chunking, set-overlap scoring, and Top-K retrieval
├── llm.py              # Gemini API integration and grounded prompt construction
├── make_test_pdf.py    # Generates synthetic scanned/image-only PDFs for OCR testing
│
├── documents/          # Drop digital or scanned PDFs here
├── DEVLOG/             # Day-by-day engineering notes and trade-offs
├── requirements.txt
└── README.md
```

Each module follows the Single Responsibility Principle: `retriever.py` has no knowledge of OCR or Gemini, and `llm.py` has no knowledge of PDFs. Upgrading ingestion from PyPDF2-only to hybrid OCR required zero changes to cleaning, chunking, retrieval, or generation.

## Tech Stack

| Component | Choice | Engineering Rationale |
|---|---|---|
| Native PDF Parsing | PyPDF2 | Fast, zero-overhead extraction for clean digital pages |
| Scanned Page Rendering | pypdfium2 | Pure-Python wheel; avoids OS-level poppler binary/PATH issues across machines |
| OCR Engine | rapidocr-onnxruntime | Lightweight ONNX runtime with per-line confidence scores and no external Tesseract install |
| Text Processing | Python re | Deterministic regex normalization without heavy NLP dependencies |
| Retrieval | Custom Set-Overlap Scoring | Transparent baseline to benchmark retrieval quality before introducing embeddings |
| LLM Generation | Gemini API | Straightforward REST interface for grounded Q&A |

## Key Engineering Decisions

### 1. Hybrid Per-Page Routing Over Blanket OCR

Running OCR on every page is slow and introduces character recognition noise onto clean digital text. Checking `len(raw_text) >= 50` per page routes digital pages through fast native extraction (~5ms) while triggering pypdfium2 + RapidOCR strictly on scanned/image pages—and lazy-loading the OCR engine only when needed.

### 2. Confidence Thresholding (< 0.70) for Human Review

OCR errors silently corrupt RAG answers if downstream chunks look plausible to an LLM. Tracking per-page mean confidence and surfacing low-confidence warnings makes failure modes explicit at ingestion time rather than hidden in hallucinated outputs.

### 3. Fixed-Size Overlapping Windows Over Paragraph Splitting

Early versions split text on blank lines, which broke when regex whitespace normalization collapsed paragraph breaks into a single block. Fixed-size character windows with overlap proved predictable across both native PDF text and noisy OCR line breaks.

### 4. Set-Based Intersection Over Substring Matching

Replacing raw substring checks with set intersection (`query_tokens ∩ chunk_tokens`) after stop-word removal eliminated noisy partial matches and paired naturally with Top-3 chunk aggregation for multi-section answers.

## What I Learned

- **Ingestion quality sets the ceiling for RAG:** Early wrong answers looked like LLM failures, but inspecting retrieved chunks showed extraction and retrieval were the real bottlenecks.
- **Module boundaries pay off during upgrades:** Keeping `pdf_reader.py` decoupled allowed adding OCR fallback, dataclasses for telemetry, and latency tracking without touching downstream modules.
- **Zero-dependency portability matters:** Choosing pypdfium2 + rapidocr-onnxruntime over pdf2image + pytesseract ensures anyone cloning the repo can run `pip install -r requirements.txt` without OS binary setup.

## Current Limitations & Next Steps

- **Semantic Retrieval:** Replace keyword overlap with dense embeddings (sentence-transformers + FAISS) behind the existing `retriever.py` interface.
- **Retrieval Evaluation:** Add a small benchmark set measuring recall@K and answer faithfulness on mixed native/scanned PDFs.
- **Chunk-Level Source Citations:** Propagate `page_num` and `extraction_method` metadata from `pdf_reader.py` into final answers.
- **API / Web Layer:** Wrap `main.py` in a FastAPI endpoint with file upload and JSON telemetry responses.

## Running Locally

Clone the repository:

```bash
git clone https://github.com/Riyasharma-17/ai-study-assistant
cd ai-study-assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_key_here
```

(Optional) Generate a sample scanned/image-only PDF to test the OCR fallback:

```bash
python make_test_pdf.py
```

Run the assistant:

```bash
python main.py
```
