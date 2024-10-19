from __future__ import annotations

from pydantic import BaseModel, UUID4

from src.application.job.enums import WorkType, EmploymentType
from src.application.application.enums import ApplicationStatus
from .user import UserResponse



class JobResponse(BaseModel):
    id: UUID4
    title: str
    details: str
    salary_from: int
    salary_to: int
    work_type: WorkType
    employment_type: EmploymentType
    experience: str | None

class UserRecruiterResposne(BaseModel):
    company_name: str | None
    user: UserResponse

class SetRecruiterSchema(BaseModel):
    company_name: str | None

class RecruiterWithJobsResponse(UserRecruiterResposne):
    jobs: list[JobResponse]
    
class HandleApplicationSchema(BaseModel):
    application_id: UUID4
    status: ApplicationStatus

