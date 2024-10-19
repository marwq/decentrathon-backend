from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.concurrency import run_in_threadpool
from pydantic import UUID4
from loguru import logger

from src.infrastructure.uow import SQLAlchemyUoW
from src.infrastructure.models import Application
from src.presentation.di import get_user_id, get_uow
from ..schemas.application import ApplicationResponse, NewApplicationSchema


router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("/")
async def get_my_applications(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
) -> list[ApplicationResponse]:
    async with uow:
        user_applicant = await uow.applicant_repo.get_with_applications(user_id)
        
    return user_applicant.applications

@router.post("/")
async def add_new_application(
    user_id: Annotated[int, Depends(get_user_id)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
    schema: NewApplicationSchema,
) -> ApplicationResponse:
    async with uow:
        application = Application(
            applicant_id=user_id,
            job_id=schema.job_id,
            caption=schema.caption,
        )
        uow.session.add(application)
        uow.session.commit()
        uow.session.refresh(application)
            
    return application
