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
