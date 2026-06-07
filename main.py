from pdf_reader import read_pdf
from utils import clean_text
from retriever import split_into_chunks
from retriever import retrieve_relevant_chunks
from llm import generate_answer

path = input("Enter PDF path: ").strip()

text = read_pdf(path)

if text is not None:

    question = input("Ask a question: ").strip()

    text = clean_text(text)

    print("\nPDF loaded successfully!")
    print("Characters:", len(text))

    chunks = split_into_chunks(text)

    print("\nNumber of chunks:", len(chunks))

    context = retrieve_relevant_chunks(question, chunks)

    answer = generate_answer(question, context)
    
    print("\nRetrieved Context:\n")
    print(context[:1500])
    print("\nAnswer:\n")
    print(answer)