from __future__ import annotations
from datetime import datetime

from sqlalchemy import BigInteger, String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from src.application.user.enums import UserRole
from .applicant import UserApplicant
from .recruiter import UserRecruiter


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(256))
    last_name: Mapped[str | None] = mapped_column(String(256))
    avatar_url: Mapped[str | None] = mapped_column(String(256))
    lang: Mapped[str] = mapped_column(String(2))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    
    applicant: Mapped[UserApplicant] = relationship("UserApplicant", back_populates="user", uselist=False, lazy="immediate")
    recruiter: Mapped[UserRecruiter] = relationship("UserRecruiter", back_populates="user", uselist=False, lazy="immediate")

    def as_dict_up(self):
        return dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            avatar_url=self.avatar_url,
            lang=self.lang,
            role=self.role,
        )

    def as_dict_down(self):
        applicant = self.applicant.as_dict_down() if self.applicant else None
        recruiter = self.recruiter.as_dict_down() if self.recruiter else None
        return dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            avatar_url=self.avatar_url,
            lang=self.lang,
            role=self.role,
            applicant=applicant,
            recruiter=recruiter,
        )