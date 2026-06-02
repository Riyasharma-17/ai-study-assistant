from PyPDF2 import PdfReader #-> PdfReader is the class responsible for opening and reading PDF files.

def read_pdf(path):
    reader = PdfReader(path)

    all_text = ""

    for page in reader.pages:
        page_text = page.extract_text() or ""
        all_text += page_text

    return all_text