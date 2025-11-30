import pdfplumber
import re

def extract_skills_from_pdf(pdf_path: str):
    """Extract skills by scanning text from PDF."""
    skills = []
    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        return [f"Error reading PDF: {str(e)}"]

    # simplified keyword-based extraction
    SKILL_KEYWORDS = [
        "python", "sql", "excel", "analysis", "research", "project",
        "communication", "leadership", "data", "marketing",
        "ai", "machine learning", "design", "javascript", "react",
    ]

    text_lower = text.lower()

    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            skills.append(skill.capitalize())

    return skills
