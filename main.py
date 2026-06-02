from pdf_reader import read_pdf

path = r"C:\Users\riyas\OneDrive\Desktop\ai-study-assistant\documents\gsoc sugarlabs.pdf"

text = read_pdf(path)

print("PDF loaded successfully!")
print("Characters:", len(text))
print(text[:1000])