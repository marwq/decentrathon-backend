from pydantic import BaseModel

from src.application.user.enums import UserRole



class UserResponse(BaseModel):
    id: int
    avatar_url: str | None
    first_name: str
    last_name: str | None
    lang: str
    role: UserRole