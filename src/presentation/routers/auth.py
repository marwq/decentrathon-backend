from typing import Annotated, List
import asyncio
from secrets import token_hex

from fastapi import APIRouter, Form, UploadFile, status, File, Depends, WebSocket, BackgroundTasks, Request
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from starlette.concurrency import run_in_threadpool
from pydantic import UUID4
from loguru import logger

from datetime import datetime, timedelta, timezone
import jwt

from aiogram import Bot
from aiogram.utils import web_app
from aiogram.utils.web_app import WebAppInitData

from src.infrastructure.uow import SQLAlchemyUoW
from src.presentation.di import get_uow, get_user_id
from ..schemas.auth import TelegramAuthSchema, TelegramAuthResponse
from ..schemas.user import UserResponse
from config import settings


router = APIRouter(prefix="/auth", tags=["auth"])


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/tg")
async def auth_tg_user(
        schema: TelegramAuthSchema,
        uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
) -> TelegramAuthResponse:
    """
    Authenticates user from Telegram MiniApp client.

    Expected data:
    - init_data: str - data from Telegram MiniApp client
    - role: str 
    """

    try:
        web_app_ini_data: WebAppInitData = web_app.safe_parse_webapp_init_data(
            settings.TELEGRAM_BOT_TOKEN, schema.init_data
        )
    except ValueError as exc:
        logger.info(exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.args[0],
            headers={"WWW-Authenticate": "Bearer"},
        )

    async with uow.db as uow:
        user = await uow.user_repo.get_item_by_id(web_app_ini_data.user.id)
        if user is None:
            user = await uow.user_repo.create_user(
                web_app_ini_data.user.id,
                web_app_ini_data.user.first_name,
                web_app_ini_data.user.last_name,
                web_app_ini_data.user.photo_url,
                web_app_ini_data.user.language_code,
                schema.role
            )
    
    # create token
    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": str(web_app_ini_data.user.id)}, expires_delta=access_token_expires
    )

    return TelegramAuthResponse(
        access_token=access_token, 
        user=user.as_dict()
    )


