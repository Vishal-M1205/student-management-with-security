from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces.class_interface import ClassInterface
from app.models.exam_mark import ExamMark
from app.models.student import Student


class ClassRepository(ClassInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_top_five_students(self):
        stmnt = (
            select(Student.id, Student.name, func.sum(ExamMark.mark).label("total"))
            .join(ExamMark, Student.id == ExamMark.student_id)
            .group_by(Student.id, Student.name)
            .order_by(func.sum(ExamMark.mark).desc())
            .limit(5)
        )

        rows = await self.session.execute(stmnt)

        return {"students": rows.mappings().all()}

    async def get_top_five_average(self):
        class_average_stmnt = select(func.avg(ExamMark.mark)).scalar_subquery()

        stmnt = (
            select(Student.id, Student.name, func.avg(ExamMark.mark).label("average"))
            .join(ExamMark)
            .group_by(Student.id, Student.name)
            .having(func.avg(ExamMark.mark) >= class_average_stmnt)
            .order_by(func.avg(ExamMark.mark).desc())
            .limit(5)
        )

        rows = await self.session.execute(stmnt)

        return {"students": rows.mappings().all()}
