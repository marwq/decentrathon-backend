from __future__ import annotations
from datetime import datetime
import uuid

from sqlalchemy import (
    BigInteger, String, Enum, UUID, ForeignKey, DateTime, Text, Integer,
    text as sqa_text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.transaction.enums import TransactionType, TransactionIncomeType, TransactionOutcomeType
from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    transaction_income_type: Mapped[TransactionIncomeType | None] = mapped_column(Enum(TransactionIncomeType))
    transaction_outcome_type: Mapped[TransactionOutcomeType | None] = mapped_column(Enum(TransactionOutcomeType))
    amount: Mapped[int] = mapped_column(Integer)
    
