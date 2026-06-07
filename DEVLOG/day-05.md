# Day 5 – Improving Retrieval Quality & Completing the RAG Pipeline

## Goal of Day 5

At the end of Day 4, the project was technically complete.

The system could:

✓ Read PDFs

✓ Extract text

✓ Clean text

✓ Split documents into chunks

✓ Retrieve information

✓ Send context to Gemini

✓ Generate answers

However, during testing I discovered a major problem.

The AI was working.

The retrieval was not.

---

## The Discovery

I tested the application using an Operating Systems PDF.

Question:

"What is an Operating System?"

The answer existed directly inside the PDF.

In fact, it appeared in the very first lecture.

However, the retriever selected a completely unrelated chunk discussing operating-system options and CPU scheduling.

Gemini then responded:

"The provided context does not define what an Operating System is."

At first this looked like an AI problem.

After inspecting the retrieved chunk, I realized something important:

Gemini was correct.

The retriever had given Gemini the wrong information.

This became the key lesson of Day 5:

Bad retrieval creates bad answers.

---

## Understanding the Real Bottleneck

The Day 4 retriever used a very simple approach.

It checked whether question words appeared inside a chunk.

Example:

Question:

"What is an Operating System?"

Words:

what
is
an
operating
system

The problem:

Words such as:

what
is
an

appear almost everywhere.

As a result, unrelated chunks could receive high scores and be selected.

The retriever was matching keywords.

It was not understanding importance.

---

## Improvement 1 – Stop Words

The first improvement was removing common words that provide little meaning.

Examples:

what
is
an
the
a
of
in
to
for

Instead of searching for:

what
is
an
operating
system

the retriever now searches for:

operating
system

This significantly improves retrieval accuracy because only meaningful terms contribute to scoring.

---

## Improvement 2 – Question Cleaning

Another issue appeared when users included punctuation.

Example:

"What is an Operating System?"

became:

what
is
an
operating
system?

Notice:

system?

is different from:

system

This can cause matches to fail.

To solve this, regular expressions were used to remove punctuation before processing the question.

The question is now normalized before retrieval.

---

## Improvement 3 – Refactoring Retrieval Logic

The retrieval code was broken into smaller functions.

Instead of one large function, the pipeline now includes:

clean_question()

Handles normalization and stop-word removal.

score_chunk()

Calculates how relevant a chunk is.

retrieve_relevant_chunks()

Ranks chunks and returns the most useful context.

This made the code significantly cleaner and easier to understand.

It also follows better software engineering practices by giving each function a single responsibility.

---

## Improvement 4 – Better Scoring

The original retriever counted simple matches.

The new version uses set intersections.

Example:

Question words:

{"operating", "system"}

Chunk words:

{"operating", "system", "kernel"}

Intersection:

{"operating", "system"}

Score:

2

This approach is cleaner, avoids duplicate counting, and produces more reliable relevance scores.

---

## Improvement 5 – Top-K Retrieval

This became the biggest improvement of the entire project.

Previously:

Question
↓
Best Chunk
↓
Gemini

Only one chunk was sent to the model.

The problem:

Answers are often spread across multiple chunks.

The new approach:

Question
↓
Score All Chunks
↓
Sort By Relevance
↓
Select Top 3 Chunks
↓
Combine Context
↓
Gemini

Now Gemini receives much richer context.

This dramatically improved answer quality.

---

## The Breakthrough Test

After implementing the improvements, I reran the Operating Systems PDF.

Question:

"What is an Operating System?"

Retrieved Context:

The system successfully retrieved the lecture section containing:

"A program that acts as an intermediary between a user and computer hardware."

For the first time, the retriever selected exactly the information needed.

Gemini then generated a correct answer.

This confirmed that the issue was never the model.

The issue was retrieval quality.

---

## Biggest Lesson Learned

The most important realization from this project:

Better retrieval leads to better AI answers.

I improved answer quality without changing:

* The model
* The API
* The prompt

The only thing that changed was retrieval.

This showed me why Retrieval-Augmented Generation systems depend heavily on the retrieval stage.

A powerful model cannot answer correctly if it receives the wrong context.

---

## Final Architecture

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

---

## What I Learned

* Stop words and why they matter
* Text normalization using regex
* Ranking and scoring systems
* Set intersections for relevance scoring
* Top-K retrieval techniques
* Debugging retrieval systems
* Importance of context quality in RAG
* Refactoring code into reusable functions
* Diagnosing bottlenecks in AI pipelines
* How retrieval directly impacts generation quality

---

## Project Completion 🎉

With Day 5 complete, the AI Study Assistant is now a functional Retrieval-Augmented Generation (RAG) application.

The system can:

✓ Read PDFs

✓ Process and clean text

✓ Retrieve relevant information

✓ Generate AI-powered answers

✓ Use Gemini for question answering

✓ Retrieve multiple relevant chunks for better context

This project started as a simple PDF reader and evolved into a complete end-to-end GenAI application.

Most importantly, I now understand not only how to use an LLM API, but also how retrieval systems work behind modern AI applications.
