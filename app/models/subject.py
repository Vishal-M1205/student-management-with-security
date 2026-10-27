from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.models.base import Base
from app.models.exam_mark import ExamMark


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    exam_marks: Mapped[list["ExamMark"]] = relationship(back_populates="subject")
