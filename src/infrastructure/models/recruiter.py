from __future__ import annotations
from datetime import datetime
import uuid

from sqlalchemy import (
    BigInteger, String, Enum, UUID, ForeignKey, DateTime, Text,
    text as sqa_text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserRecruiter(Base):
    __tablename__ = "user_recruiters"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    company_name: Mapped[str | None] = mapped_column(String(256))
    
    user = relationship("User", back_populates="recruiter", uselist=False, lazy="immediate")
    jobs = relationship("Job", back_populates="owner", uselist=True, lazy="raise")
    
    def as_dict_up(self):
        return dict(
            user_id=self.user_id,
            company_name=self.company_name,
            user=self.user.as_dict_up(),
        )
        
    def as_dict_down(self):
        try:
            jobs = [i.as_dict_down() for i in self.jobs]
        except:
            jobs = None
        return dict(
            user_id=self.user_id,
            company_name=self.company_name,
            jobs=jobs,
        )
        
    def as_dict_both(self):
        return self.as_dict_down() | self.as_dict_up()
