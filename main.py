from pdf_reader import read_pdf
from utils import clean_text
from retriever import split_into_chunks, retrieve_relevant_chunks
from llm import generate_answer

path = input("Enter PDF path: ").strip()

text, report = read_pdf(path)

if text is not None and report is not None:
    print("\n--- Extraction Telemetry ---")
    conf_str = (
        f"{report.avg_ocr_confidence * 100:.1f}%"
        if report.avg_ocr_confidence is not None
        else "N/A (100% native)"
    )
    print(
        f"Pages: {report.total_pages} total | "
        f"{report.native_pages} native | "
        f"{report.ocr_pages} OCR fallback | "
        f"Avg OCR Conf: {conf_str} | "
        f"Latency: {report.latency_ms}ms"
    )

    for log in report.page_logs:
        flag = " [WARN: Low confidence - flag for human review]" if log.needs_review else ""
        print(
            f"  Page {log.page_num}: {log.method} "
            f"({log.char_count} chars, conf={log.confidence:.2f}){flag}"
        )

    if not text.strip():
        print("\nError: No readable text extracted from document.")
    else:
        question = input("\nAsk a question: ").strip()

        text = clean_text(text)

        print("\nPDF loaded successfully!")
        print("Characters:", len(text))

        chunks = split_into_chunks(text)
        print("Number of chunks:", len(chunks))

        context = retrieve_relevant_chunks(question, chunks)
        answer = generate_answer(question, context)

        print("\nRetrieved Context:\n")
        print(context[:1500])
        print("\nAnswer:\n")
        print(answer)
