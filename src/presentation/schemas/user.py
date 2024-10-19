from pydantic import BaseModel

from src.application.user.enums import UserRole
from .applicant import UserApplicantResponse



class UserRecruiterResponse(BaseModel):
    company_name: str | None

class SwitchUserRoleSchema(BaseModel):
    role: UserRole

class UserResponse(BaseModel):
    id: int
    avatar_url: str | None
    first_name: str
    last_name: str | None
    lang: str
    role: UserRole

class UserResponseRecruiterApplicant(UserResponse):
    recruiter: UserRecruiterResponse
    applicant: UserApplicantResponse
