from pydantic import BaseModel, UUID4

from src.application.job.enums import WorkType, EmploymentType
from .recruiter import UserRecruiterResposne


class JobResponse(BaseModel):
    id: UUID4
    owner: UserRecruiterResposne
    title: str
    details: str
    salary_from: int
    salary_to: int
    work_type: WorkType
    employment_type: EmploymentType
    experience: str | None
    
class JobWithRelevance(JobResponse):
    relevance: list[str] | None = None

class JobsReponse(BaseModel):
    count: int
    jobs: list[JobWithRelevance]

class CreateJobSchema(BaseModel):
    title: str
    details: str
    work_type: WorkType
    salary_from: int
    salary_to: int
    employment_type: EmploymentType
    experience: str | None = None

