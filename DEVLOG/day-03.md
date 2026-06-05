# Day 3 – Building the Retrieval System

## Goal of Day 3

After Day 2, the project could:

1. Read a PDF
2. Extract text
3. Clean the extracted text

The problem was that the entire document existed as one large string.

For example:

PDF
↓
Extract Text
↓
Clean Text
↓
One Huge String

This creates a major problem for AI applications.

Suppose a user uploads a 200-page textbook and asks:

"What is Machine Learning?"

Should we send the entire textbook to Gemini?

No.

That would be inefficient, expensive, and unnecessary.

Instead, we first need a way to find the most relevant part of the document before sending anything to an AI model.

This is the core idea behind Retrieval-Augmented Generation (RAG):

Retrieve Relevant Information
↓
Provide Context
↓
Generate Answer

The objective of Day 3 was to build the "Retrieve" part ourselves using only Python.

---

## Initial Idea: Paragraph-Based Chunking

The first approach was simple.

I thought about splitting the document into paragraphs.

Example:

Python is great.

Lists store values.

Dictionaries store key-value pairs.

This could become:

[
"Python is great.",
"Lists store values.",
"Dictionaries store key-value pairs."
]

To achieve this, I created:

split_into_chunks(text)

and initially used:

text.split("\n\n")

because paragraphs are often separated by two newline characters.

---

## Unexpected Problem

After testing the implementation, I discovered a problem.

My text cleaning function from Day 2 used:

re.sub(r"\s+", " ", text)

The pattern:

\s+

matches all whitespace characters:

* spaces
* tabs
* newlines

and replaces them with a single space.

This meant:

Before cleaning:

Paragraph 1

Paragraph 2

Paragraph 3

After cleaning:

Paragraph 1 Paragraph 2 Paragraph 3

All paragraph boundaries disappeared.

As a result:

text.split("\n\n")

returned only one chunk.

Output:

Chunks: 1

The chunking strategy failed.

---

## Debugging the Issue

Instead of blindly changing code, I traced the flow:

PDF
↓
Extract Text
↓
Clean Text
↓
Chunk Text

I realized that the cleaning step was removing the exact separators that chunking depended on.

This was an important lesson:

A preprocessing step can unintentionally break a later component in the pipeline.

---

## New Approach: Fixed-Size Chunking

Instead of relying on paragraph breaks, I switched to a more reliable strategy.

The idea:

Split the document every 500 characters.

Example:

Document Length = 2000 characters

Chunk 1 = text[0:500]
Chunk 2 = text[500:1000]
Chunk 3 = text[1000:1500]
Chunk 4 = text[1500:2000]

This method works regardless of formatting issues inside the PDF.

---

## Understanding Python Slicing

Before implementing chunking, I reviewed Python string slicing.

Example:

text = "abcdefghij"

To get:

abcde

I used:

text[0:5]

To get:

fghij

I used:

text[5:10]

Important concept:

start index = included
end index = excluded

---

## Building split_into_chunks()

The final logic:

1. Create an empty list
2. Loop through the document in steps of chunk_size
3. Extract a slice of text
4. Store it inside the list
5. Return all chunks

Implementation:

def split_into_chunks(text, chunk_size=500):
chunks = []

```
for i in range(0, len(text), chunk_size):
    chunk = text[i:i + chunk_size]
    chunks.append(chunk)

return chunks
```

---

## Testing Chunking

The extracted document contained:

8486 characters

Using:

chunk_size = 500

Expected:

8486 ÷ 500 ≈ 17 chunks

Actual Result:

Number of chunks: 17

The chunking system worked successfully.

---

# Building the Retriever

After chunking was complete, the next goal was:

Given a user's question, find the most relevant chunk.

Example:

Question:
"What is GSoC?"

Chunks:

[
"Python is a programming language.",
"I got a GSoC internship in Sugar Labs.",
"Lists store multiple values."
]

Desired Output:

"I got a GSoC internship in Sugar Labs."

---

## Retrieval Strategy

Instead of using embeddings or vector databases, I implemented a simple keyword matching approach.

The logic:

1. Split the user's question into words
2. Check each chunk
3. Count matching words
4. Assign a score
5. Return the chunk with the highest score

This allowed me to understand the core retrieval concept before introducing AI frameworks.

---

## Converting Question into Words

Question:

"What is GSoC"

Using:

question.split()

Result:

["What", "is", "GSoC"]

This created a list of searchable keywords.

---

## Scoring Chunks

For each chunk:

score = 0

For every word in the question:

If the word exists inside the chunk:

score += 1

Higher score means greater relevance.

Example:

Question:

"What is GSoC"

Chunk:

"I got a GSoC internship in Sugar Labs."

Match:

"GSoC"

Score:

1

---

## Tracking the Best Chunk

Two variables were introduced:

best_score = 0
best_chunk = ""

Every time a chunk achieved a higher score:

best_score = score
best_chunk = chunk

At the end of the search:

return best_chunk

This returned the most relevant chunk found in the document.

---

## Additional Improvement

After testing, I noticed another issue.

Example:

Question:

"what is gsoc"

Chunk:

"GSoC internship"

Python treats:

"gsoc"

and

"GSoC"

as different strings.

To solve this, I made the search case-insensitive by converting text to lowercase before comparison.

This improved retrieval accuracy significantly.

---

## Final Outcome of Day 3

The application can now:

✓ Extract PDF text
✓ Clean extracted text
✓ Split text into chunks
✓ Accept a user question
✓ Search through all chunks
✓ Find the most relevant chunk
✓ Return context for future AI processing

Current Pipeline:

PDF
↓
Read PDF
↓
Clean Text
↓
Split into Chunks
↓
Retrieve Best Chunk
↓
(Next Step: Gemini API)

Day 3 transformed the project from a document reader into the foundation of a real Retrieval-Augmented Generation (RAG) system.
