from __future__ import annotations
from datetime import datetime
import uuid

from sqlalchemy import (
    BigInteger, String, Enum, UUID, ForeignKey, DateTime, Text,
    text as sqa_text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.applicant.enums import WorkSearchingType
from .application import Application
from .base import Base


class UserApplicant(Base):
    __tablename__ = "user_applicants"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    
    job_title: Mapped[str | None] = mapped_column(String(256))
    job_salary: Mapped[str | None] = mapped_column(String(256))
    details: Mapped[str | None] = mapped_column(Text())
    work_searching_type: Mapped[WorkSearchingType] = mapped_column(Enum(WorkSearchingType), default=WorkSearchingType.SEARCH)

    user = relationship("User", back_populates="applicant", uselist=False, lazy="immediate")
    experiences: Mapped[list[Experience]] = relationship("Experience", back_populates="user_applicant", lazy="immediate")
    skills: Mapped[list[Skill]] = relationship("Skill", back_populates="user_applicant", lazy="immediate")
    educations: Mapped[list[Education]] = relationship("Education", back_populates="user_applicant", lazy="immediate")
    applications: Mapped[list[Application]] = relationship("Application", back_populates="applicant", lazy="raise")
    
    def as_dict_up(self):
        try:
            user = self.user.as_dict_up()
        except:
            user = None
        return dict(
            user_id=self.user_id,
            job_title=self.job_title,
            job_salary=self.job_salary,
            details=self.details,
            work_searching_type=self.work_searching_type,
            user=user,
        )
        
    def as_dict_down(self):
        try:
            experiences = [i.as_dict_down() for i in self.experiences]
        except:
            experiences = None
        try:
            skills = [i.as_dict_down() for i in self.skills]
        except:
            skills = None
        try:
            applications = [i.as_dict_down() for i in self.applications]
        except:
            applications = None
        try:
            educations = [i.as_dict_down() for i in self.educations]
        except:
            educations = None
        return dict(
            user_id=self.user_id,
            job_title=self.job_title,
            job_salary=self.job_salary,
            details=self.details,
            work_searching_type=self.work_searching_type,
            experiences=experiences,
            skills=skills,
            applications=applications,
            educations=educations,
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
    
    user_applicant = relationship("UserApplicant", back_populates="experiences", lazy="raise")
    
    def as_dict_up(self):
        try:
            user_applicant = self.user_applicant.as_dict_up()
        except:
            user_applicant = None
        return dict(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            start_at=self.start_at,
            end_at=self.end_at,
            description=self.description,
            company_name=self.company_name,
            user_applicant=user_applicant,
        )
        
    def as_dict_down(self):
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
    
    user_applicant = relationship("UserApplicant", back_populates="skills", lazy="raise")
    
    def as_dict_up(self):
        try:
            user_applicant = self.user_applicant.as_dict_up()
        except:
            user_applicant = None
        return dict(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            user_applicant=user_applicant, 
        )
        
    def as_dict_down(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
        )
        
class Education(Base):
    __tablename__ = "educations"

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
    university: Mapped[str] = mapped_column(String(256))
    title: Mapped[str] = mapped_column(String(256))
    course: Mapped[str | None] = mapped_column(String(256))
    end_at: Mapped[datetime] = mapped_column(DateTime)
    
    user_applicant = relationship("UserApplicant", back_populates="educations", lazy="raise")
    
    def as_dict_up(self):
        try:
            user_applicant = self.user_applicant.as_dict_up()
        except:
            user_applicant = None
        return dict(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            university=self.university,
            end_at=self.end_at,
            course=self.course,
            user_applicant=user_applicant,
        )
        
    def as_dict_down(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            university=self.university,
            end_at=self.end_at,
            course=self.course,
        )
