from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.concurrency import run_in_threadpool
from pydantic import UUID4
from loguru import logger

from src.infrastructure.uow import SQLAlchemyUoW
from src.infrastructure.models import Job, UserApplicant
from src.infrastructure.repositories.job_repo import JobRepo
from src.application.job.enums import WorkType, EmploymentType
from src.application.user.enums import UserRole
from src.application.job.services import get_jobs_count, get_job_relevance
from src.presentation.di import get_user_id, get_uow
from ..schemas.job import JobsReponse, CreateJobSchema, JobResponse


router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/")
async def get_jobs_list(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
    skip: int = 0,
    limit: int = 10,
    q: str | None = None,
    work_type: WorkType | None = None,
    employment_type: EmploymentType | None = None,
) -> JobsReponse:
    async with uow:
        user = await uow.user_repo.get_item_by_id(user_id)
        jobs_list = await uow.job_repo.get_jobs(skip, limit, q, work_type, employment_type)
        jobs = [i.as_dict_up() | {"relevance": get_job_relevance(user.applicant, i)} for i in jobs_list]
        count = await get_jobs_count(uow)
        
    return JobsReponse(
        count=count,
        jobs=jobs,
    )

@router.post("/")
async def add_job(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
    schema: CreateJobSchema,
) -> JobResponse:
    async with uow:
        user = await uow.user_repo.get_item_by_id(user_id)
        if user.role != UserRole.RECRUITER is None:
            raise HTTPException(403, "You cannot create new job")
        job = await uow.job_repo.create_job(
            user_id, schema.title, schema.details, 
            schema.work_type, schema.employment_type,
            schema.salary_from, schema.salary_to,
            schema.experience,
        )
        job = await uow.job_repo.get_job_with_owner(job.id)
    a = job.as_dict_up()
    logger.info(a)
    return a
