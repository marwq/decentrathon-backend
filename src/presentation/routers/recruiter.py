from typing import Annotated, List
import asyncio
from secrets import token_hex
from datetime import datetime

from fastapi import APIRouter, Depends, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.concurrency import run_in_threadpool
from pydantic import UUID4
from loguru import logger

from src.application.application.enums import ApplicationStatus
from src.infrastructure.uow import SQLAlchemyUoW
from src.presentation.di import get_uow, get_user_id
from ..schemas.recruiter import (
    UserRecruiterResposne, SetRecruiterSchema, 
    RecruiterWithJobsResponse, HandleApplicationSchema,
)
from ..schemas.application import ApplicationResponse
from config import settings


router = APIRouter(prefix="/recruiter", tags=["recruiter"])

@router.get("/me")
async def get_my_recruiter(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
) -> UserRecruiterResposne:
    async with uow:
        user = await uow.user_repo.get_item_by_id(user_id)
        recruiter = user.recruiter
    return recruiter.as_dict_up()

@router.post("/")
async def set_my_recruiter(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
    schema: SetRecruiterSchema,
):
    async with uow:
        await uow.recruiter_repo.upsert_user_recruiter(
            user_id, 
            schema.company_name
        )
        await uow.session.commit()
    return JSONResponse({"status": "ok"})

@router.get("/jobs")
async def get_my_jobs(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
) -> RecruiterWithJobsResponse:
    async with uow:
        user_recruiter = await uow.recruiter_repo.get_recruiter_with_jobs(user_id)
    return user_recruiter.as_dict_both()

@router.get("/appications")
async def get_incoming_applications(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
    status: ApplicationStatus | None = None,
) -> list[ApplicationResponse]:
    if status is not None:
        kwargs = dict(status=status)
    else:
        kwargs = dict()
    async with uow:
        jobs = await uow.job_repo.list(owner_id=user_id)
        applications = []
        for job in jobs:
            applications.extend(await uow.application_repo.list(job_id=job.id, **kwargs))
    return [i.as_dict_down() for i in applications]

@router.post("/handle-application")
async def handle_application(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
    schema: HandleApplicationSchema
) -> ApplicationResponse:
    async with uow:
        application = await uow.application_repo.get_item_by_id(schema.application_id)
        if application.job.owner.user_id != user_id:
            raise HTTPException(403, "Not yours")
        application.status = schema.status
        await uow.session.commit()
    return application.as_dict_down()