
from tools.database_tool import get_db_session, Certificate
def issue_certificate(candidate_id:int, project_id:int):
    s=get_db_session()
    cert=Certificate(candidate_id=candidate_id, project_id=project_id)
    s.add(cert)
    s.commit()
    s.refresh(cert)
    s.close()
    return {'certificate_id':cert.id, 'issued_date':str(cert.issued_date)}
