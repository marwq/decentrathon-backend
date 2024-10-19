from datetime import datetime

from pydantic import BaseModel, UUID4

from src.application.user.enums import UserRole


class SkillSchema(BaseModel):
    title: str

class Skill(SkillSchema):
    id: UUID4
    
class ExperienceSchema(BaseModel):
    title: str
    start_at: datetime
    end_at: datetime
    description: str
    company_name: str
class Experience(ExperienceSchema):
    id: UUID4
    
class UserApplicantResponse(BaseModel):
    job_title: str | None
    job_salary: str | None
    experiences: list[Experience]
    skills: list[Skill]

class SetApplicantSchema(BaseModel):
    job_title: str
    job_salary: str
    experiences: list[ExperienceSchema]
    skills: list[SkillSchema]
