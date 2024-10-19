from datetime import date, datetime, timedelta
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.postgresql import insert

from src.infrastructure.models.recruiter import UserRecruiter
from src.infrastructure.repositories.base import SQLAlchemyRepo


class RecruiterRepo(SQLAlchemyRepo[UserRecruiter]):
    """User Recruiter repository implementation for SQLAlchemy ORM."""
    
    model = UserRecruiter
    
    async def upsert_user_recruiter(
        self,
        user_id: int,
        company_name: str | None,
    ) -> UserRecruiter:
        stmt = (
            insert(UserRecruiter)
            .values(dict(user_id=user_id, company_name=company_name))
            .on_conflict_do_update(constraint="user_recruiters_pkey", set_={"company_name": company_name})
            .returning(UserRecruiter)
        )
        result = await self._session.execute(stmt)
        return result.unique().scalar_one()
    
    async def get_recruiter_with_jobs(
        self,
        user_id: int,
    ) -> UserRecruiter | None:
        stmt = (
            select(UserRecruiter)
            .options(joinedload(UserRecruiter.jobs))
            .where(UserRecruiter.user_id == user_id)
        )
        resp = await self._session.execute(stmt)
        return resp.unique().scalar_one_or_none()
    
    