from pydantic import BaseModel

from src.application.user.enums import UserRole
from .user import UserResponse


class TelegramAuthSchema(BaseModel):
    role: UserRole
    init_data: str

class TelegramAuthResponse(BaseModel):
    access_token: str
    user: UserResponse
