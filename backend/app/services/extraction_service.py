"""Module 2: Content Extraction — OCR for images/scanned PDFs, direct
text pull for text-based PDFs via PyMuPDF."""
import os


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return _extract_pdf(file_path)
    if ext in (".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp"):
        return _extract_image(file_path)
    if ext in (".txt", ".md"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    raise ValueError(f"Unsupported file type for extraction: {ext}")


def _extract_pdf(file_path: str) -> str:
    import fitz  # PyMuPDF

    doc = fitz.open(file_path)
    text_parts = []
    for page in doc:
        page_text = page.get_text().strip()
        if page_text:
            text_parts.append(page_text)
        else:
            # Scanned page with no extractable text layer -> OCR the rendered image
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")
            text_parts.append(_ocr_image_bytes(img_bytes))
    doc.close()
    return "\n\n".join(text_parts).strip()


def _extract_image(file_path: str) -> str:
    from PIL import Image
    import pytesseract

    img = Image.open(file_path)
    return pytesseract.image_to_string(img).strip()


def _ocr_image_bytes(img_bytes: bytes) -> str:
    import io
    from PIL import Image
    import pytesseract

    img = Image.open(io.BytesIO(img_bytes))
    return pytesseract.image_to_string(img).strip()
