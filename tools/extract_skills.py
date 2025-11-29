import spacy

# Try to load spaCy model; fall back gracefully if missing
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    print("[extract_skills] spaCy model not found. Keyword-only mode.")
    nlp = None

SKILL_KEYWORDS = [
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust",
    "sql", "mysql", "postgresql", "mongodb", "redis",
    "fastapi", "django", "flask", "react", "node", "express",
    "aws", "azure", "gcp", "docker", "kubernetes",
    "machine learning", "nlp", "pytorch", "tensorflow", "sklearn",
    "html", "css", "tailwind", "vue", "angular",
    "git", "linux",
]


def extract_skills(text: str) -> list[str]:
    """
    Extracts skills from text using simple keyword matching.
    If spaCy is available, lightly enhances detection.
    """
    text_lower = text.lower()
    found = set()

    # Keyword search
    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            found.add(skill)

    # Optional spaCy enhancement
    if nlp:
        doc = nlp(text)
        for token in doc:
            if token.text.lower() in SKILL_KEYWORDS:
                found.add(token.text.lower())

    return sorted(found)
