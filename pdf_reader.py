import time
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from PyPDF2 import PdfReader
import pypdfium2 as pdfium
from rapidocr_onnxruntime import RapidOCR

MIN_NATIVE_CHARS = 50
LOW_CONFIDENCE_THRESHOLD = 0.70

_ocr_engine: Optional[RapidOCR] = None


def _get_ocr_engine() -> RapidOCR:
    global _ocr_engine
    if _ocr_engine is None:
        _ocr_engine = RapidOCR()
    return _ocr_engine


@dataclass
class PageExtractionLog:
    page_num: int
    method: str  # "native_text" or "ocr_fallback"
    char_count: int
    confidence: float  # 1.0 for native text, 0.0-1.0 for OCR
    needs_review: bool = False


@dataclass
class ExtractionReport:
    total_pages: int = 0
    native_pages: int = 0
    ocr_pages: int = 0
    avg_ocr_confidence: Optional[float] = None
    low_confidence_pages: List[int] = field(default_factory=list)
    latency_ms: float = 0.0
    page_logs: List[PageExtractionLog] = field(default_factory=list)


def _ocr_single_page(pdf_doc: pdfium.PdfDocument, page_index: int) -> Tuple[str, float]:
    """Renders a single PDF page to an image and extracts text + mean confidence via RapidOCR."""
    page = pdf_doc[page_index]
    # Render at 2x scale (~144 DPI) for clean OCR accuracy without heavy memory overhead
    bitmap = page.render(scale=2.0)
    pil_image = bitmap.to_pil()
    img_array = np.array(pil_image)

    ocr = _get_ocr_engine()
    result, _ = ocr(img_array)

    if not result:
        return "", 0.0

    lines = [item[1] for item in result]
    scores = [float(item[2]) for item in result]

    extracted_text = "\n".join(lines)
    avg_conf = sum(scores) / len(scores) if scores else 0.0
    return extracted_text, avg_conf


def read_pdf(path: str) -> Tuple[Optional[str], Optional[ExtractionReport]]:
    if not path.lower().endswith(".pdf"):
        print("Error: Please provide a PDF file.")
        return None, None

    start_time = time.perf_counter()

    try:
        reader = PdfReader(path)
        pdfium_doc = None  # Lazy-loaded only if at least one page needs OCR

        all_text_parts: List[str] = []
        report = ExtractionReport(total_pages=len(reader.pages))
        ocr_confidences: List[float] = []

        for idx, page in enumerate(reader.pages):
            page_num = idx + 1
            raw_text = (page.extract_text() or "").strip()

            if len(raw_text) >= MIN_NATIVE_CHARS:
                all_text_parts.append(raw_text)
                report.native_pages += 1
                report.page_logs.append(
                    PageExtractionLog(
                        page_num=page_num,
                        method="native_text",
                        char_count=len(raw_text),
                        confidence=1.0,
                        needs_review=False,
                    )
                )
            else:
                if pdfium_doc is None:
                    pdfium_doc = pdfium.PdfDocument(path)

                ocr_text, conf = _ocr_single_page(pdfium_doc, idx)
                needs_review = conf < LOW_CONFIDENCE_THRESHOLD

                all_text_parts.append(ocr_text)
                report.ocr_pages += 1
                ocr_confidences.append(conf)

                if needs_review:
                    report.low_confidence_pages.append(page_num)

                report.page_logs.append(
                    PageExtractionLog(
                        page_num=page_num,
                        method="ocr_fallback",
                        char_count=len(ocr_text),
                        confidence=round(conf, 3),
                        needs_review=needs_review,
                    )
                )

        if pdfium_doc is not None:
            pdfium_doc.close()

        if ocr_confidences:
            report.avg_ocr_confidence = round(sum(ocr_confidences) / len(ocr_confidences), 3)

        report.latency_ms = round((time.perf_counter() - start_time) * 1000, 1)
        return "\n".join(all_text_parts), report

    except FileNotFoundError:
        print("Error: File not found.")
        return None, None

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None, None
