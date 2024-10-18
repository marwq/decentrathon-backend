from __future__ import annotations
from datetime import datetime
import uuid

from sqlalchemy import (
    BigInteger, String, Enum, UUID, ForeignKey, DateTime, Text,
    text as sqa_text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserApplicant(Base):
    __tablename__ = "user_applicants"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    
    job_title: Mapped[str | None] = mapped_column(String(256))
    job_salary: Mapped[str | None] = mapped_column(String(256))

    user = relationship("User", back_populates="applicant", uselist=False)
    experiences: Mapped[list[Experience]] = relationship("Experience", back_populates="user_applicant", lazy="joined")
    skills: Mapped[list[Skill]] = relationship("Skill", back_populates="user_applicant", lazy="joined")
    
    def as_dict(self):
        return dict(
            user_id=self.user_id,
            job_title=self.job_title,
            job_salary=self.job_salary,
            experiences=[i.as_dict() for i in self.experiences],
            skills=[i.as_dict() for i in self.skills],
        )

class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_applicants.user_id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(256))
    start_at: Mapped[datetime] = mapped_column(DateTime)
    end_at: Mapped[datetime | None] = mapped_column(DateTime)
    description: Mapped[str | None] = mapped_column(Text)
    company_name: Mapped[str | None] = mapped_column(String(256))
    
    user_applicant = relationship("UserApplicant", back_populates="experiences")
    
    def as_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            start_at=self.start_at,
            end_at=self.end_at,
            description=self.description,
            company_name=self.company_name,
        )

class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_applicants.user_id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(256))
    
    user_applicant = relationship("UserApplicant", back_populates="skills")
    
    def as_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
        )