from sqlalchemy import ForeignKey, Integer, String

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.user import User


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_teacher_user_id"),
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    designation: Mapped[str] = mapped_column(String(50), default="Teacher")
    user: Mapped["User"] = relationship(back_populates="teacher_profile")
