# Day 2 — Cleaning the Chaos After PDF Extraction

## Goal

Build a text-cleaning utility that transforms messy PDF output into clean, searchable text.

---

## Why This Became Necessary

Yesterday, I successfully extracted text from PDFs using PyPDF2.

At first, I thought the problem was solved.

The PDF text was being extracted correctly, but when I looked at the output closely, I noticed something:

```text
Chapter 1


Introduction to Python



Python is a programming language.





Variables are used to store values.
```

Humans can still understand this.

Machines struggle more.

The extracted text contained:

* Multiple blank lines
* Extra spaces
* Inconsistent formatting
* Noise introduced during PDF extraction

This might seem harmless now, but the next stage of the project is retrieval.

If a user asks:

> What is Python?

the system must search through the document efficiently.

Messy text makes that process harder and less reliable.

Before building AI features, I needed cleaner data.

---

## The Realization

A PDF reader should only read PDFs.

It should not also clean text.

That would mix responsibilities.

So instead of modifying `pdf_reader.py`, I created a separate utility function dedicated to text cleaning.

This follows the idea of **single responsibility**:

* `pdf_reader.py` → extracts text
* `utils.py` → cleans text

Each module has one job.

---

## Solution

Created:

```python
import re

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()
```

---

## Understanding the Logic

### Step 1: Import Regex

```python
import re
```

Python's `re` module allows pattern-based text processing.

Instead of manually removing spaces and newlines, regex can handle them in one operation.

---

### Step 2: Replace Excessive Whitespace

```python
re.sub(r"\s+", " ", text)
```

#### What is `\s`?

Matches any whitespace character:

* Space
* Tab
* Newline

#### What does `+` mean?

One or more occurrences.

So:

```text
"Hello


World"
```

becomes:

```text
"Hello World"
```

All consecutive whitespace gets converted into a single space.

---

### Step 3: Remove Leading and Trailing Spaces

```python
text.strip()
```

Example:

```text
"   Python is awesome   "
```

becomes:

```text
"Python is awesome"
```

This ensures the final text starts and ends cleanly.

---

## Updating the Pipeline

Yesterday's flow:

```text
PDF
 ↓
Extract Text
```

Today's flow:

```text
PDF
 ↓
Extract Text
 ↓
Clean Text
```

The output is now much more structured and ready for retrieval.

---

## Changes in main.py

I connected the cleaning step directly after extraction.

```python
text = read_pdf(path)

if text is not None:
    text = clean_text(text)
```

Now every document is automatically cleaned before being used elsewhere.

---

## What I Learned

### Regex Solves Real Problems

Before today, regex felt like a confusing topic.

This is the first time I used it in a practical project to solve an actual issue.

---

### Data Quality Matters

AI systems are only as good as the data they receive.

Even before adding Gemini or building retrieval, I already needed preprocessing.

---

### Small Modules Scale Better

Instead of creating one giant file, I split responsibilities:

* Reading
* Cleaning

This makes the project easier to maintain and extend later.

---

## Challenges Faced

The biggest challenge wasn't coding.

It was understanding *why* cleaning was needed in the first place.

Initially, the extracted text looked acceptable.

Only after thinking about future search and retrieval did it become obvious that preprocessing was necessary.

---

## Result

Successfully built a reusable text-cleaning utility and integrated it into the PDF processing pipeline.

The project can now:

✅ Read PDFs

✅ Extract text

✅ Clean extracted text

✅ Display structured output

---

## Project Status

Current pipeline:

```text
PDF
 ↓
Extract Text
 ↓
Clean Text
 ↓
Ready for Retrieval
```

Next step:

Build a retrieval system that can find relevant sections of the document before sending them to the LLM.
