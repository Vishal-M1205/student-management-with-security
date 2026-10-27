from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String
from app.models.base import Base
from app.models.exam_mark import ExamMark
from app.models.id_card import IdCard
from app.models.user import User


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_student_user_id"),
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(1))

    exam_marks: Mapped[list["ExamMark"]] = relationship(back_populates="student")
    id_card: Mapped["IdCard"] = relationship()
    user: Mapped["User"] = relationship(back_populates="student_profile")
