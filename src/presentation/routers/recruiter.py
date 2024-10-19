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

from src.infrastructure.uow import SQLAlchemyUoW
from src.presentation.di import get_uow, get_user_id
from ..schemas.recruiter import UserRecruiterResposne, SetRecruiterSchema, RecruiterWithJobsResponse
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
    schema: SetRecruiterSchema,
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
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
