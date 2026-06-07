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

### Day 4 — Gemini Integration & End-to-End RAG Pipeline

Integrated Gemini API and transformed the project from a document retrieval tool into a functional AI-powered study assistant.

Instead of simply returning the most relevant chunk from a PDF, the application now sends the retrieved context along with the user's question to Gemini and generates a natural language answer.

**Implemented:**

* Gemini API integration
* Secure API key management using `.env`
* Environment variable loading with `python-dotenv`
* Prompt construction using retrieved context and user questions
* LLM response generation
* Basic error handling for API requests
* Complete Retrieval-Augmented Generation (RAG) workflow

**Learned:**

* How LLM APIs work in real-world applications
* API key security best practices
* Environment variables and `.env` files
* Fundamentals of prompt engineering
* Difference between retrieval and generation
* How context improves answer quality in RAG systems
* Debugging AI pipelines and identifying retrieval bottlenecks

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
Retrieve Relevant Chunk
 ↓
Build Prompt
 ↓
Gemini API
 ↓
Generate Answer
```

### Key Insight

While testing with multiple PDFs, I discovered that poor answers were often caused by retrieving the wrong chunk rather than limitations of the LLM itself. This highlighted a critical lesson in RAG systems: answer quality depends heavily on retrieval quality. The AI model can only generate responses from the context it receives.

The project can now process documents, retrieve relevant information, and generate answers using Gemini, making it a complete end-to-end RAG application.

### Day 5 — Retrieval Optimization & RAG Improvement

After testing the Day 4 version, I discovered that answer quality was often limited by retrieval quality rather than the LLM itself.

The application was able to generate answers using Gemini, but sometimes retrieved irrelevant chunks because it relied on simple keyword matching. Day 5 focused on improving retrieval accuracy and providing better context to the model.

**Implemented:**

* Stop-word removal for cleaner search queries
* Question preprocessing and punctuation removal
* Refactored retrieval logic into reusable functions
* Set-based relevance scoring
* Top-K retrieval (Top 3 chunks)
* Context aggregation from multiple relevant chunks
* Retrieval quality debugging and testing

**Learned:**

* Why retrieval quality directly impacts answer quality in RAG systems
* Stop words and text normalization techniques
* Ranking and scoring strategies for information retrieval
* Set operations for relevance matching
* Top-K retrieval concepts used in production RAG systems
* Debugging retrieval pipelines before blaming the LLM
* Importance of context selection in AI applications

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
Clean Question
 ↓
Remove Stop Words
 ↓
Score Chunks
 ↓
Top-K Retrieval
 ↓
Build Context
 ↓
Gemini API
 ↓
Generate Answer
```

### Key Insight

The biggest lesson from this project was that better AI answers do not always require a better model. During testing, improving retrieval quality alone significantly improved answer quality without changing the LLM. This demonstrated a core principle of Retrieval-Augmented Generation: the model can only answer as well as the context it receives.

## Final Outcome

The AI Study Assistant is now a complete end-to-end RAG application capable of:

* Reading and processing PDF documents
* Cleaning and preparing text for retrieval
* Retrieving relevant information using Top-K search
* Generating answers using Gemini API
* Following a modular and maintainable architecture

This project provided hands-on experience with Python, APIs, prompt engineering, retrieval systems, and the core concepts behind modern GenAI applications.

