def split_into_chunks(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
        

    return chunks


def retrieve_relevant_chunk(question, chunks):
    question = question.lower()
    question_words = question.split()
    best_score = 0
    best_chunk = ""

    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = 0

        for question_word in question_words:
            if question_word in chunk:
                score += 1
            
        if score > best_score:
            best_score = score
            best_chunk = chunk

    return best_chunk
