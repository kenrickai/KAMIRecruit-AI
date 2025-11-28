
from tools.database_tool import get_db_session, Project

def search_projects_by_skills(skills:list[str]):
    s=get_db_session()
    projects = s.query(Project).all()
    out=[]
    for p in projects:
        req = p.required_skills.split(',') if p.required_skills else []
        if any(skill.strip().lower() in [r.strip().lower() for r in req] for skill in skills):
            out.append({'id':p.id,'title':p.title,'required_skills':req})
    s.close()
    return out
