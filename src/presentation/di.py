"""Provide project the API layer dependencies."""

import asyncio
from typing import Annotated, Optional
from datetime import datetime, timedelta, timezone

from loguru import logger
import jwt
from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infrastructure.models import User
from src.infrastructure.uow import SQLAlchemyUoW
from config import settings


engine = create_async_engine(
    "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
        settings.DB_USER,
        settings.DB_PASS,
        settings.DB_HOST,
        settings.DB_PORT,
        settings.DB_NAME,
    ),
    future=True,
)

session_pool = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)

async def get_uow() -> SQLAlchemyUoW:
    """
    Create a new Unit of Work instance.

    Returns:
        UnitOfWork: The new Unit of Work instance.
    """
    return SQLAlchemyUoW(session_pool)

auth_scheme = HTTPBearer()

async def get_user_id(
    request: Request,
    creds: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)],
    uow: Annotated[SQLAlchemyUoW, Depends(get_uow)],
) -> str:
    user_id = None
    if creds.credentials:
        try:
            payload = jwt.decode(
                creds.credentials.encode(), settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")
        except InvalidTokenError as e:
            logger.error(e)
    if user_id is None:
        raise HTTPException(401, "user_id is None")
    return int(user_id)
