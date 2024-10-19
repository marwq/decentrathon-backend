from datetime import datetime

from pydantic import BaseModel, UUID4

from src.application.user.enums import UserRole
from src.application.applicant.enums import WorkSearchingType



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
    
class EducationSchema(BaseModel):
    university: str
    title: str | None
    course: str | None
    end_at: datetime
    
class Education(EducationSchema):
    id: UUID4
    
class UserApplicantResponse(BaseModel):
    job_title: str | None
    job_salary: str | None
    work_searching_type: WorkSearchingType | None
    details: str | None
    experiences: list[Experience]
    skills: list[Skill]
    educations: list[Education]

class SetApplicantSchema(BaseModel):
    job_title: str
    job_salary: str
    work_searching_type: WorkSearchingType
    details: str
    experiences: list[ExperienceSchema]
    skills: list[SkillSchema]
    educations: list[EducationSchema]
