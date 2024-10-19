from pydantic import BaseModel, UUID4

from src.application.application.enums import ApplicationStatus

from .job import JobResponse


class ApplicationResponse(BaseModel):
    id: UUID4
    applicant_id: int
    job_id: int
    status: ApplicationStatus
    caption: str
    details: str
    salary_from: int
    salary_to: int
    job: JobResponse

class NewApplicationSchema(BaseModel):
    job_id: UUID4
    caption: str | None
