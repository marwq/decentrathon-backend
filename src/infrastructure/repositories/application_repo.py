from datetime import date, datetime, timedelta
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.postgresql import insert

from src.infrastructure.models import Application
from src.infrastructure.repositories.base import SQLAlchemyRepo
from src.application.application.enums import ApplicationStatus


class ApplicationRepo(SQLAlchemyRepo[Application]):
    """Application repository implementation for SQLAlchemy ORM."""
    
    model = Application
    
