from __future__ import annotations
from datetime import datetime
import uuid

from sqlalchemy import (
    BigInteger, String, Enum, UUID, ForeignKey, DateTime, Text,
    text as sqa_text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.job.enums import WorkType, EmploymentType
from .base import Base


class Job(Base):
    __tablename__ = "jobs"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("user_recruiters.user_id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(256))
    details: Mapped[str] = mapped_column(Text())
    salary_from: Mapped[int] = mapped_column(BigInteger)
    salary_to: Mapped[int] = mapped_column(BigInteger)
    work_type: Mapped[WorkType] = mapped_column(Enum(WorkType))
    employment_type: Mapped[EmploymentType] = mapped_column(Enum(EmploymentType))
    experience: Mapped[str | None] = mapped_column(String(256))
    
    owner = relationship("UserRecruiter", back_populates="jobs", uselist=False, lazy="immediate")
    
    applications = relationship("Application", back_populates="applicant", lazy="raise")
    
    def as_dict_up(self):
        return dict(
            id=self.id,
            owner_id=self.owner_id,
            title=self.title,
            details=self.details,
            salary_from=self.salary_from,
            salary_to=self.salary_to,
            experience=self.experience,
            work_type=self.work_type,
            employment_type=self.employment_type,
            owner=self.owner.as_dict_up(),
        )
        
    def as_dict_down(self):
        try:
            applications = [i.as_dict_down() for i in self.applications]
        except:
            applications = None
        return dict(
            id=self.id,
            owner_id=self.owner_id,
            title=self.title,
            details=self.details,
            salary_from=self.salary_from,
            salary_to=self.salary_to,
            experience=self.experience,
            work_type=self.work_type,
            employment_type=self.employment_type,
            applications=applications,
        )
