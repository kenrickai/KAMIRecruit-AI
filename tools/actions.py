from sqlalchemy.orm import Session

from tools.database_tool import User
from tools.search_tool import search_projects_by_skills


def action_search_projects_for_user(user: User) -> dict:
    """
    Search projects based on user's skills.
    """
    skills = user.skills.split(",") if user.skills else []
    projects = search_projects_by_skills(skills)
    return {"user_id": user.id, "skills": skills, "projects": projects}


def action_update_user_skill(user: User, new_skill: str, session: Session) -> dict:
    """
    Add a new skill to the user's profile.
    """
    skill_list = user.skills.split(",") if user.skills else []
    new_skill_clean = new_skill.strip()
    if new_skill_clean and new_skill_clean.lower() not in [s.lower() for s in skill_list]:
        skill_list.append(new_skill_clean)
        user.skills = ",".join(skill_list)
        session.commit()

    return {"updated_skills": skill_list}


def action_search_projects(skill: str) -> dict:
    """
    Simple skill-based project search using a single skill.
    """
    projects = search_projects_by_skills([skill])
    return {"used_skill": skill, "projects": projects}
