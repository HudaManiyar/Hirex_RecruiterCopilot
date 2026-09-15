import fitz  # PyMuPDF
from pathlib import Path


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF using PyMuPDF.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text as a single string.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"{pdf_path} does not exist.")

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text("text")

    document.close()

    return text.strip()