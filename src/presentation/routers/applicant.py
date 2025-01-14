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
from ..schemas.applicant import UserApplicantResponse, SetApplicantSchema
from config import settings


router = APIRouter(prefix="/applicant", tags=["applicant"])

@router.get("/me")
async def get_my_applicant(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
) -> UserApplicantResponse:
    async with uow:
        user = await uow.user_repo.get_item_by_id(user_id)
    return user.applicant.as_dict_down()

@router.post("/")
async def set_my_applicant(
    schema: SetApplicantSchema,
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
):
    async with uow:
        await uow.applicant_repo.upsert_user_applicant(
            user_id, 
            schema.job_title,
            schema.job_salary,
            experiences_data=[i.model_dump() for i in schema.experiences],
            skills_data=[i.model_dump() for i in schema.skills],
        )
        await uow.session.commit()
    return JSONResponse({"status": "ok"})