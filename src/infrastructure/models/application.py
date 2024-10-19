from __future__ import annotations
from datetime import datetime
import uuid

from sqlalchemy import (
    BigInteger, String, Enum, UUID, ForeignKey, DateTime, Text,
    text as sqa_text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.application.enums import ApplicationStatus
from .base import Base


class Application(Base):
    __tablename__ = "applications"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    applicant_id: Mapped[int] = mapped_column(
        ForeignKey("user_applicants.user_id"), nullable=False, index=True
    )
    job_id: Mapped[UUID] = mapped_column(
        ForeignKey("jobs.id"), nullable=False, index=True
    )
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus), default=ApplicationStatus.WAITING
    )
    caption: Mapped[str | None] = mapped_column(Text())
    
    applicant = relationship("UserApplicant", back_populates="applications", uselist=False, lazy="immediate")
    job = relationship("Job", back_populates="applications", uselist=False, lazy="immediate")
    
    def as_dict_up(self):
        return dict(
            id=self.id,
            applicant_id=self.applicant_id,
            job_id=self.job_id,
            status=self.status,
            caption=self.caption,
            applicant=self.applicant.as_dict_up(),
            job=self.job.as_dict_up(),
        )
        
    def as_dict_down(self):
        return dict(
            id=self.id,
            applicant_id=self.applicant_id,
            job_id=self.job_id,
            status=self.status,
            caption=self.caption,
        )
