"""This module contains the implementation of the user repository."""
from datetime import date, datetime, timedelta
from typing import Sequence

from src.application.user.enums import UserRole
from src.infrastructure.models.user import User
from src.infrastructure.repositories.base import SQLAlchemyRepo


class UserRepo(SQLAlchemyRepo[User]):
    """User repository implementation for SQLAlchemy ORM."""
    
    model = User
    
    async def create_user(
        self,
        id: int,
        first_name: str,
        last_name: str | None,
        avatar_url: str | None,
        lang: str,
        role: UserRole
) -> User:
        user = User(
            id=id,
            first_name=first_name,
            last_name=last_name,
            avatar_url=avatar_url,
            lang=lang,
            role=role,
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
