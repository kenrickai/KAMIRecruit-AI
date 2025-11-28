# tools/actions.py

def action_search_projects(skill: str):
    """
    Dummy implementation.
    Later you can connect to real NGO directories.
    """
    return {
        "results": [
            {"project": "Data Cleanup for NGO X", "match_score": 0.88},
            {"project": "Impact Evaluation Dashboard", "match_score": 0.81},
        ],
        "used_skill": skill
    }


def action_update_user_skill(user, new_skill: str, session):
    skill_list = user.skills.split(",") if user.skills else []
    if new_skill not in skill_list:
        skill_list.append(new_skill)
        user.skills = ",".join(skill_list)
        session.commit()

    return {"updated_skills": skill_list}
