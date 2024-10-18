from datetime import datetime

from pydantic import BaseModel

from src.application.user.enums import UserRole



class Skill(BaseModel):
    title: str
    
class Experience(BaseModel):
    title: str
    start_at: datetime
    end_at: datetime
    description: str
    company_name: str
    
class UserApplicantResponse(BaseModel):
    job_title: str
    job_salary: str
    experiences: list[Experience]
    skills: list[Skill]

class SetApplicantSchema(BaseModel):
    job_title: str
    job_salary: str
    experiences: list[Experience]
    skills: list[Skill]
