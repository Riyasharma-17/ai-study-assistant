from pdf_reader import read_pdf
from utils import clean_text
from retriever import split_into_chunks
from retriever import retrieve_relevant_chunk

path = input("Enter PDF path: ").strip()

text = read_pdf(path)

if text is not None:

    question = input("Ask a question: ").lower()

    text = clean_text(text)

    print("\nPDF loaded successfully!")
    print("Characters:", len(text))
    print("\nFirst 1000 characters:\n")
    print(text[:1000])

    chunks = split_into_chunks(text)

    print("\nNumber of chunks:", len(chunks))

    best_chunk = retrieve_relevant_chunk(question, chunks)

    print("\nMost Relevant Chunk:\n")
    print(best_chunk)