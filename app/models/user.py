from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Index, Integer, String, UniqueConstraint, func

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.teacher import Teacher


class User(Base):
    __tablename__ = "users"

    __table_args__ = (Index("ix_users_email", "email", unique=True),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    student_profile: Mapped[Optional["Student"]] = relationship(back_populates="user")
    teacher_profile: Mapped[Optional["Teacher"]] = relationship(back_populates="user")
