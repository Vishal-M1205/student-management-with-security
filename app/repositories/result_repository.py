from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces.result_interface import ExamResultInterface
from app.models.exam_mark import ExamMark
from app.models.student import Student


class ExamResultRepository(ExamResultInterface):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_student_exam_result_by_id(self, student_id: int):
        stmnt = (
            select(Student)
            .where(Student.id == student_id)
            .options(selectinload(Student.exam_marks).selectinload(ExamMark.subject))
        )

        row = await self.session.execute(stmnt)
        row = row.scalar_one_or_none()
        if row is not None:
            return {
                "student_id": student_id,
                "student_name": row.name,
                "subjects": [
                    {"subject_name": x.subject.name, "mark": x.mark}
                    for x in row.exam_marks
                ],
            }
