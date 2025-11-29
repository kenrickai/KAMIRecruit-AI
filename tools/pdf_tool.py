import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract readable text from a PDF using pdfplumber.
    Returns an empty string if extraction fails.
    """
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
    except Exception as e:
        print(f"[pdf_tool] Failed to read PDF: {e}")
        return ""

    return text.strip()
