from pdf_reader import read_pdf
from utils import clean_text

path = input("Enter PDF path: ")

text = read_pdf(path)

if text is not None:
    text = clean_text(text)

    print("\nPDF loaded successfully!")
    print("Characters:", len(text))
    print("\nFirst 1000 characters:\n")
    print(text[:1000])