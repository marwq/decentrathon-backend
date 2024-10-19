from pydantic import BaseModel, UUID4

from src.application.application.enums import ApplicationStatus

from .job import JobResponse



class ApplicationResponse(BaseModel):
    id: UUID4
    applicant_id: int
    job_id: UUID4
    status: ApplicationStatus
    caption: str

class ApplicationWithJobResponse(ApplicationResponse):
    job: JobResponse

class NewApplicationSchema(BaseModel):
    job_id: UUID4
    caption: str | None
