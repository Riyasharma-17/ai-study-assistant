### Day 4 — Connecting Gemini and Building the First End-to-End AI Pipeline

After Day 3, the project could successfully:

✓ Extract text from PDFs

✓ Clean extracted text

✓ Split documents into chunks

✓ Retrieve the most relevant chunk based on a user's question

However, there was still a major limitation.

The application could only return raw document chunks.

Example:

Question:

"What is GSoC?"

Output:

"I got a GSoC internship in Sugar Labs..."

While retrieval was working, the application was not actually answering questions.

The goal of Day 4 was to transform the project from a document search tool into an AI-powered assistant capable of generating answers from retrieved context.

---

## Understanding the Problem

At the beginning of Day 4, I asked an important question:

What is missing from the current pipeline?

Current Pipeline:

PDF
↓
Extract Text
↓
Clean Text
↓
Split Into Chunks
↓
Retrieve Relevant Chunk

The missing component was an LLM (Large Language Model).

Without an LLM, the application could only retrieve information.

It could not explain, summarize, or answer questions.

This led to the next architecture:

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
Gemini
↓
Generate Answer

---

## Learning About APIs

Before writing code, I first understood what an API actually is.

The key realization:

My Python application cannot run Gemini locally.

Instead, Gemini runs on Google's servers.

The communication flow is:

My Application
↓
API Request
↓
Google Gemini
↓
Response

This was my first practical experience interacting with an LLM through an API rather than using ChatGPT through a browser.

---

## Generating a Gemini API Key

To communicate with Gemini, I needed an API key.

I created a free API key through Google AI Studio.

Important lesson:

API keys should never be hardcoded inside source code.

Bad:

api_key = "AIza..."

Good:

Store inside a .env file

This introduced a very important software engineering concept:

Environment Variables

which are commonly used in professional applications to protect secrets and credentials.

---

## Using Environment Variables

I created:

.env

and stored:

GEMINI_API_KEY=your_api_key

Then I learned how Python loads environment variables using:

python-dotenv

and accesses them through:

os.getenv()

This allowed the project to securely load credentials without exposing them in GitHub repositories.

---

## Creating llm.py

A new module was added:

llm.py

The purpose of this file:

Handle all communication with Gemini.

This follows a clean software design principle:

Single Responsibility Principle

Each file should have one clear purpose.

Current structure:

pdf_reader.py → PDF extraction

utils.py → Text cleaning

retriever.py → Retrieval logic

llm.py → LLM communication

main.py → Application workflow

This separation makes future maintenance significantly easier.

---

## Understanding Prompt Engineering

The next challenge was understanding how to communicate with Gemini.

Initially, I thought:

Should I send only the question?

Example:

"What is GSoC?"

The problem:

Gemini would answer using its own knowledge rather than the uploaded document.

Then I considered sending only the retrieved chunk.

The problem:

Gemini would not know what the user is asking.

This led to the core RAG insight:

Send BOTH context and question.

Example:

Context:
I got a GSoC internship in Sugar Labs...

Question:
What is GSoC?

Answer the question using only the provided context.

This became my first manually designed prompt.

---

## Why Context + Question Matters

This was one of the biggest conceptual lessons of the project.

The retriever's job:

Find relevant information.

The LLM's job:

Generate a useful answer from that information.

Together they form:

Retrieval-Augmented Generation (RAG)

Retrieve
↓
Augment Prompt
↓
Generate Answer

This was the first time I fully understood why RAG systems exist.

---

## Building generate_answer()

The core function created was:

generate_answer(question, context)

Its responsibilities:

1. Build a prompt
2. Send the prompt to Gemini
3. Receive the response
4. Return the answer

Instead of printing directly, the function returns:

response.text

This follows good software engineering practices because returned values can be reused elsewhere in the application.

---

## Adding Error Handling

To make the project more robust, Gemini calls were wrapped in:

try:
...
except:
...

This prevents the application from crashing if:

* API requests fail
* Invalid credentials are used
* Network issues occur

This was my first experience adding defensive programming around an AI API.

---

## Integrating Gemini into main.py

The final integration step connected retrieval and generation.

Previous flow:

Question
↓
Retrieve Chunk
↓
Print Chunk

New flow:

Question
↓
Retrieve Chunk
↓
Gemini
↓
Generate Answer
↓
Print Answer

For the first time, the application became a complete AI workflow.

---

## First Real Test

I tested the system using multiple PDFs.

The Gemini integration worked successfully.

The model received context, generated responses, and returned answers.

However, something interesting happened.

When asking:

"What is an Operating System?"

the answer returned by Gemini was poor even though the PDF contained the correct definition.

At first this looked like a Gemini problem.

After investigation, I discovered the real issue:

Retrieval selected the wrong chunk.

Gemini simply answered based on the context it received.

This taught an important lesson:

A weak answer does not necessarily mean the LLM failed.

Sometimes retrieval fails before the model even gets the correct information.

---

## Biggest Insight of Day 4

The most important realization was:

The AI model was not the bottleneck.

Retrieval quality was.

The system worked exactly as designed:

Question
↓
Retriever
↓
Wrong Chunk
↓
Gemini
↓
Wrong Answer

This highlighted why retrieval quality is one of the most important components of a RAG system.

---

## Current Pipeline

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

---

## What I Learned

* How APIs allow applications to communicate with LLMs
* Why API keys should be stored in environment variables
* How .env files work
* Using python-dotenv and os.getenv()
* Configuring Gemini inside a Python application
* Fundamentals of prompt engineering
* Why context and question must be combined in RAG
* Error handling for external APIs
* Difference between retrieval and generation
* Diagnosing failures in AI pipelines
* Understanding where bottlenecks actually occur

---

## Outcome of Day 4

The AI Study Assistant can now:

✓ Read PDFs

✓ Clean text

✓ Split documents into chunks

✓ Retrieve relevant information

✓ Connect to Gemini

✓ Generate answers from retrieved context

✓ Operate as a complete end-to-end RAG application

The project is now a functional AI application rather than a document-processing tool.

The next step is improving retrieval quality so the system consistently provides Gemini with the most relevant context.
