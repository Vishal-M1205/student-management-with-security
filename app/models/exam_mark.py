from app.models.base import Base
from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

"""Used TYPE_CHECKING because,
 subject.py import ExamMark from exam_mark.py, 
 exam_mark.py import Subject subject.py
  This creates a circular dependency 
but we need the class only for typehint """
if TYPE_CHECKING:
    from app.models.subject import Subject
    from app.models.student import Student


class ExamMark(Base):
    __tablename__ = "exam_marks"

    """all the field are not null because of the Mapped[datatype] didn't mention None, so it is inferred as NOT NULL """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("subjects.id", ondelete="CASCADE", name="fk_exam_mark_subject_id"),
    )
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE", name="fk_exam_mark_student_id"),
    )
    mark: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)

    subject: Mapped["Subject"] = relationship(back_populates="exam_marks")
    student: Mapped["Student"] = relationship(back_populates="exam_marks")
