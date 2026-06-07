# AI Study Assistant

> A lightweight RAG system built from scratch — no LangChain, no vector databases, just Python and a clear understanding of how retrieval-augmented generation actually works.

---

## What This Is

Most tutorials hand you a framework and call it "building a RAG app." This project does the opposite.

The AI Study Assistant is a document question-answering system that lets users upload a PDF and ask natural language questions about its contents. Under the hood, it implements a complete RAG pipeline — chunking, retrieval, context aggregation, and LLM generation — written from scratch to understand what frameworks like LangChain are actually doing.

Built over 5 days as a learning project. The goal was not to ship a product. The goal was to understand the engineering.

---

## The Problem

LLMs have a context window limit. You cannot feed an entire textbook to Gemini and ask questions. You need to:

1. Break the document into manageable pieces
2. Find the pieces most relevant to the question
3. Send only those pieces to the LLM
4. Generate a grounded, accurate answer

That's RAG. This project builds it piece by piece.

---

## How It Works

```
Input PDF
    │
    ▼
┌─────────────────┐
│  PDF Extraction │  ← PyPDF2 reads raw text page by page
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Cleaning  │  ← Regex pipeline: removes noise, normalises whitespace
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Chunking     │  ← Fixed-size character windows with overlap
└────────┬────────┘
         │
    User Question
         │
         ▼
┌──────────────────────┐
│  Question Cleaning   │  ← Punctuation removal, lowercasing
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stop Word Removal   │  ← Filters "the", "is", "a" — keeps signal words
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Relevance Scoring   │  ← Set-based keyword overlap between query and chunks
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Top-K Retrieval    │  ← Returns top 3 most relevant chunks
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Context Aggregation │  ← Combines chunks into a single context block
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Prompt Assembly    │  ← Injects context + question into structured prompt
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│     Gemini API       │  ← Generates a grounded natural language answer
└──────────────────────┘
```

---

## Project Structure

```
ai-study-assistant/
│
├── main.py           # Entry point — orchestrates the full pipeline
├── pdf_reader.py     # PDF extraction logic
├── utils.py          # Text cleaning and preprocessing utilities
├── retriever.py      # Chunking, scoring, and Top-K retrieval
├── llm.py            # Gemini API integration and prompt construction
│
├── documents/        # Drop PDFs here
├── DEVLOG/           # Day-by-day engineering notes
│   ├── day-01.md
│   ├── day-02.md
│   └── ...
│
├── .env              # API key (not committed)
├── requirements.txt
└── README.md
```

Each module has a single responsibility. `retriever.py` does not know about Gemini. `llm.py` does not know about PDFs. This separation made debugging significantly easier — when answers were wrong, the problem could be isolated to retrieval or generation independently.

---

## Tech Stack

| Component | Choice | Why |
|---|---|---|
| PDF extraction | PyPDF2 | Lightweight, no heavy dependencies |
| Text processing | Python `re` (regex) | Sufficient for cleaning at this scale; no overhead of NLP libraries |
| Retrieval | Custom keyword scoring | Forces understanding of the mechanism before using embeddings |
| LLM | Gemini API | Free tier suitable for development; straightforward REST interface |
| Env management | `python-dotenv` | Standard practice for API key security |

Notably absent: LangChain, vector databases, embeddings. This was intentional. The goal was to implement the concepts, not abstract over them.

---

## Key Engineering Decisions

### Fixed-Size Chunking Over Paragraph Splitting

Early versions tried to split text by paragraph boundaries. This broke during the cleaning phase — the regex pipeline removed the blank lines that marked paragraph separations, collapsing the entire document into one chunk.

Fixed-size character windows with overlap solved this. Less elegant than semantic chunking, but reliable and predictable.

### Set-Based Scoring Over String Matching

Initial retrieval used substring matching — check if the keyword appears in the chunk. This was noisy and slow. Replacing it with set intersection (query keywords ∩ chunk keywords) made scoring cleaner and more accurate, and made stop word removal meaningful.

### Top-K Over Single Chunk Retrieval

Retrieving only the single best chunk caused failures when the relevant information spanned multiple sections. Top-3 retrieval with context aggregation improved answer coverage without significantly inflating the prompt size.

---

## Challenges

**Retrieval quality, not model quality, was the bottleneck.**

This was the central engineering insight of the project. Early poor answers felt like an LLM problem. After investigation, the issue was consistently that the wrong chunks were being retrieved — the LLM was generating coherent but irrelevant answers because the context it received was irrelevant.

Improving the retrieval logic (stop word removal, set scoring, Top-K) produced noticeably better answers without touching the model or the prompt.

This mirrors a known pattern in production RAG systems: optimise retrieval before optimising generation.

---

## What I Learned

- **RAG is a data pipeline problem as much as an AI problem.** Each stage — extraction, cleaning, chunking, retrieval — compounds into final answer quality.
- **Preprocessing decisions have downstream effects.** Removing paragraph breaks in cleaning broke chunking. Modules need to be designed with awareness of what comes after them.
- **Single Responsibility Principle is worth the effort.** Isolating modules made bugs easier to find and fixes easier to test.
- **API key security from day one.** `.env` and `.gitignore` set up before any API key was generated.
- **Debugging a pipeline means isolating stages.** Print the chunks. Check the scores. Verify context before blaming the LLM.

---

## Limitations

This is a learning project. Production use would require:

- **Semantic retrieval** — Keyword matching cannot capture meaning. Embedding-based retrieval (FAISS, ChromaDB, or similar) would be the next step.
- **Persistent storage** — Chunks are rebuilt on every run. A vector store would cache them.
- **Chunking improvements** — Sentence-aware or semantic chunking would reduce the chance of splitting mid-thought.
- **Evaluation** — No formal metrics (precision, recall, faithfulness) were measured. A real system needs these.
- **UI** — Currently terminal-based. A web interface would be the practical next step.

---

## Future Improvements

- [ ] Replace keyword scoring with embedding-based retrieval (sentence-transformers + FAISS)
- [ ] Add a simple Streamlit or Flask interface
- [ ] Implement chunk overlap to avoid splitting relevant context at boundaries
- [ ] Add retrieval evaluation using RAGAS or a custom scoring script
- [ ] Support multiple PDFs with a persistent index
- [ ] Add source attribution — show which chunk the answer came from

---

## Running Locally

```bash
git clone https://github.com/Riyasharma-17/ai-study-assistant
cd ai-study-assistant
pip install -r requirements.txt
```

Create a `.env` file:
```
GEMINI_API_KEY=your_key_here
```

Drop a PDF into `documents/`, then:
```bash
python main.py
```

---

## Development Log

Day-by-day engineering notes are in the [`DEVLOG/`](./DEVLOG/) folder. They cover implementation decisions, bugs encountered, and what changed between versions — written while building, not reconstructed afterward.

---

*Built as part of a personal GenAI engineering learning track. Focused on understanding core RAG concepts before working with frameworks like LangChain or LlamaIndex.*