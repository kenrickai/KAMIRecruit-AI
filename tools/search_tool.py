from typing import List, Dict

from sqlalchemy.orm import Session

from tools.database_tool import get_db, Project


def search_projects_by_skills(skills: List[str]) -> list[Dict]:
    """
    Simple matching: returns projects where any required_skill
    intersects with provided skills.
    """
    session: Session = get_db()
    try:
        projects = session.query(Project).all()
        results: list[Dict] = []

        normalized_skills = [s.strip().lower() for s in skills]

        for p in projects:
            req = p.required_skills.split(",") if p.required_skills else []
            req_norm = [r.strip().lower() for r in req]
            if any(s in req_norm for s in normalized_skills):
                results.append(
                    {
                        "id": p.id,
                        "title": p.title,
                        "required_skills": req,
                    }
                )
        return results
    finally:
        session.close()
