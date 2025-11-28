import PyPDF2


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def extract_skills(text: str) -> list[str]:
    keywords = ["python", "sql", "excel", "machine learning", "data", "analysis", "ai"]
    text_lower = text.lower()
    return [k for k in keywords if k in text_lower]
