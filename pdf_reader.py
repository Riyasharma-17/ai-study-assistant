from PyPDF2 import PdfReader

def read_pdf(path):
    if not path.lower().endswith(".pdf"):
        print("Error: Please provide a PDF file.")
        return None

    try:
        reader = PdfReader(path)

        all_text = ""

        for page in reader.pages:
            page_text = page.extract_text() or ""
            all_text += page_text

        return all_text

    except FileNotFoundError:
        print("Error: File not found.")
        return None

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None