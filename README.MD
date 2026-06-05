🚀 Building in Public | Learning GenAI, RAG, and LLM Applications through real projects

# AI Study Assistant

A Python-based AI Study Assistant that allows users to upload PDF documents, extract their contents, and eventually ask questions using an LLM-powered Retrieval-Augmented Generation (RAG) pipeline.

## Features

* PDF text extraction
* Text preprocessing and cleaning
* Question answering from uploaded documents (Coming Soon)
* Gemini API integration (Coming Soon)
* Retrieval-Augmented Generation (RAG) workflow

## Tech Stack

* Python
* PyPDF2
* Regular Expressions (re)
* Gemini API (Planned)

## Project Structure

```text
ai-study-assistant/
│
├── DEVLOG/
│   ├── day-01.md
│   └── day-02.md
│
├── documents/
├── main.py
├── pdf_reader.py
├── utils.py
├── retriever.py
├── llm.py
├── requirements.txt
└── README.md
```

## Development Log

### Day 1 — PDF Text Extraction

Implemented PDF text extraction using PyPDF2.

**Learned:**

* File handling
* Working with external libraries
* OOP objects in practice
* Reading and processing PDF documents

### Day 2 — Text Cleaning Pipeline

Built a reusable text-cleaning utility using regular expressions.

**Implemented:**

* Removal of extra spaces and blank lines
* Text normalization using regex
* Cleaner document processing pipeline

**Learned:**

* Practical use of regular expressions
* Importance of preprocessing before retrieval
* Single Responsibility Principle in project design

### Current Pipeline

```text
PDF
 ↓
Extract Text
 ↓
Clean Text
```

### Next Steps

* Build document retrieval logic
* Connect Gemini API
* Implement question answering
* Create a complete RAG workflow

```
```
### Day 3 — Building the Retrieval Pipeline

Implemented the first version of the document retrieval system.

Instead of sending the entire PDF to an LLM, the document is now split into smaller chunks and searched to find the most relevant information based on the user's question.

**Implemented:**

* Fixed-size document chunking
* Chunk generation using Python string slicing
* Keyword-based relevance scoring
* Retrieval of the most relevant document chunk
* Case-insensitive search improvements

**Learned:**

* Core concepts behind Retrieval-Augmented Generation (RAG)
* Why documents must be chunked before retrieval
* Python string slicing and chunking strategies
* Search and ranking using keyword matching
* Debugging data pipelines when preprocessing affects retrieval
* Building retrieval systems without external frameworks

### Current Pipeline

```text
PDF
 ↓
Extract Text
 ↓
Clean Text
 ↓
Split Into Chunks
 ↓
Retrieve Most Relevant Chunk
```

### Key Insight

While implementing chunking, I discovered that my text-cleaning step removed paragraph boundaries, causing the entire document to become a single chunk. This led me to redesign the chunking strategy using fixed-size character windows, an important lesson in how different stages of a data pipeline can affect each other.

The project now contains the core retrieval component required for a basic RAG system. The next step is connecting Gemini API and generating answers using the retrieved context.

