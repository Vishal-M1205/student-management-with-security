from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from app.models.exam_mark import ExamMark
from app.schemas.exam_mark import ExamMarkCreate, ExamMarkUpdate


class ExamMarkRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_exam_marks(self, params: dict):
        stmnt = select(ExamMark)

        for field, value in params.items():
            stmnt = stmnt.where(getattr(ExamMark, field) == value)

        rows = await self.session.execute(stmnt)
        rows = rows.scalars().all()
        return rows

    async def get_exam_mark_by_id(self, exam_mark_id: int):
        row = await self.session.get(ExamMark, exam_mark_id)
        return row

    async def create_exam_mark(self, exam_mark: ExamMarkCreate):
        stmnt = insert(ExamMark).values(**exam_mark.model_dump()).returning(ExamMark)

        row = await self.session.execute(stmnt)
        row = row.scalar_one()

        return row

    async def update_exam_mark(self, exam_mark_id: int, exam_mark: ExamMarkUpdate):
        stmnt = (
            update(ExamMark)
            .where(ExamMark.id == exam_mark_id)
            .values(**exam_mark.model_dump())
            .returning(ExamMark)
        )

        row = await self.session.execute(stmnt)
        row = row.scalar_one_or_none()

        return row

    async def delete_exam_mark(self, exam_mark_id: int):
        stmnt = (
            delete(ExamMark)
            .where(ExamMark.id == exam_mark_id)
            .returning(ExamMark.id)
        )

        row = await self.session.execute(stmnt)
        row = row.scalar_one_or_none()

        return row

    async def patch_exam_mark(self, exam_mark_id: int, payload: dict):
        stmnt = (
            update(ExamMark)
            .where(ExamMark.id == exam_mark_id)
            .values(**payload)
            .returning(ExamMark)
        )

        row = await self.session.execute(stmnt)
        row = row.scalar_one_or_none()

        return row
