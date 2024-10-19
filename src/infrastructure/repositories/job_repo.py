from datetime import date, datetime, timedelta
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.postgresql import insert

from src.infrastructure.models import Job, UserRecruiter
from src.infrastructure.repositories.base import SQLAlchemyRepo
from src.application.job.enums import WorkType, EmploymentType


class JobRepo(SQLAlchemyRepo[Job]):
    """Job repository implementation for SQLAlchemy ORM."""
    
    model = Job
    
    async def create_job(
        self,
        owner_id: int,
        title: str,
        details: str,
        work_type: WorkType,
        employment_type: EmploymentType,
        salary_from: int,
        salary_to: int,
        experience: str | None = None,
    ) -> Job:
        job = Job(
            owner_id=owner_id, title=title, details=details,
            work_type=work_type, employment_type=employment_type,
            experience=experience, salary_from=salary_from,
            salary_to=salary_to,
        )
        self._session.add(job)
        await self._session.commit()
        await self._session.refresh(job)
        return job

    async def get_jobs(
        self,
        skip: int = 0,
        limit: int = 10,
        q: str | None = None,
        work_type: WorkType | None = None,
        employment_type: EmploymentType | None = None,
    ) -> list[Job]:
        stmt = (
            select(Job)
            .offset(skip)
            .limit(limit)
        )
        if q is not None:
            stmt = stmt.where(
                Job.title.ilike(f"%{q}%") | Job.details.ilike(f"%{q}%")
            )
        if work_type is not None:
            stmt = stmt.where(Job.work_type == work_type)
        if employment_type is not None:
            stmt = stmt.where(Job.employment_type == employment_type)
        resp = await self._session.execute(stmt)
        return resp.scalars().all()

    async def get_job_with_owner(self, id: str) -> Job | None:
        stmt = (
            select(Job)
            .options(joinedload(Job.owner).joinedload(UserRecruiter.user))
            .where(Job.id==id)
        )
        resp = await self._session.execute(stmt)
        return resp.unique().scalar_one_or_none()
