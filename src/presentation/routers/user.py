from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.concurrency import run_in_threadpool
from pydantic import UUID4
from loguru import logger

from src.infrastructure.uow import SQLAlchemyUoW
from src.application.user.enums import UserRole
from src.application.job.services import get_jobs_count, get_job_relevance
from src.presentation.di import get_user_id, get_uow
from ..schemas.user import SwitchUserRoleSchema, UserResponseRecruiterApplicant


router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me")
async def get_me(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
) -> UserResponseRecruiterApplicant:
    async with uow:
        user = await uow.user_repo.get_item_by_id(user_id)
    return user.as_dict_down()

@router.post("/switch_role")
async def switch_role(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
    schema: SwitchUserRoleSchema,
):
    async with uow:
        await uow.user_repo.update(user_id, role=schema.role)
        await uow.commit()
    return {"status": "ok"}
