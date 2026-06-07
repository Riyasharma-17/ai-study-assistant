import re

def split_into_chunks(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


import re

# Common words that don't help retrieval
stop_words = {
    "what", "is", "an", "the", "a",
    "of", "in", "to", "for", "and",
    "on", "at", "by"
}


def clean_question(question):
    # Convert to lowercase
    question = question.lower()

    # Remove punctuation
    question = re.sub(r"[^\w\s]", "", question)

    # Split into words
    words = question.split()

    # Remove stop words
    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    return filtered_words


def score_chunk(chunk, question_words):
    chunk_words = set(chunk.lower().split())

    # Count matching words
    score = len(set(question_words) & chunk_words)

    return score


def retrieve_relevant_chunks(question, chunks, top_k=3):

    # Clean and process question
    question_words = clean_question(question)

    results = []

    # Score every chunk
    for chunk in chunks:
        score = score_chunk(chunk, question_words)
        results.append((score, chunk))

    # Sort by score (highest first)
    results.sort(key=lambda x: x[0], reverse=True)

    # Take top k chunks
    top_chunks = results[:top_k]

    # Extract chunk text only
    chunk_texts = [
        chunk for score, chunk in top_chunks
        if score > 0
    ]

    # Combine into one context string
    context = "\n\n".join(chunk_texts)

    return context