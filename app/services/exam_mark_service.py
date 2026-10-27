import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.exam_mark_repository import ExamMarkRepository
from app.schemas.exam_mark import ExamMarkCreate, ExamMarkPatch, ExamMarkUpdate


class ExamMarkService:

    def __init__(self, repository: ExamMarkRepository, session: AsyncSession):
        self.logger = logging.getLogger(__name__)
        self.repository = repository
        self.session = session

    async def get_all_exam_marks(self, **kwargs):
        async with self.session.begin():
            params = {
                key: value for key, value in kwargs.items() if value is not None
            }
            return await self.repository.get_all_exam_marks(params)

    async def get_exam_mark_by_id(self, exam_mark_id: int):
        async with self.session.begin():
            exam_mark = await self.repository.get_exam_mark_by_id(exam_mark_id)
            if exam_mark is None:
                raise HTTPException(status_code=404, detail="Exam Mark Not Found")
            return exam_mark

    async def create_exam_mark(self, exam_mark: ExamMarkCreate):
        async with self.session.begin():
            return await self.repository.create_exam_mark(exam_mark)

    async def update_exam_mark(self, exam_mark_id: int, exam_mark: ExamMarkUpdate):
        async with self.session.begin():
            row = await self.repository.update_exam_mark(exam_mark_id, exam_mark)
            if row is None:
                raise HTTPException(status_code=404, detail="No Exam Mark Found")
            return row

    async def delete_exam_mark(self, exam_mark_id: int):
        async with self.session.begin():
            row = await self.repository.delete_exam_mark(exam_mark_id)
            if row is None:
                raise HTTPException(status_code=404, detail="No Exam Mark Found")
            return row

    async def patch_exam_mark(self, exam_mark_id: int, exam_mark: ExamMarkPatch):
        async with self.session.begin():
            payload = exam_mark.model_dump(exclude_unset=True)
            if not payload:
                raise HTTPException(
                    status_code=400,
                    detail="Bad Request : No fields provided for update",
                )
            row = await self.repository.patch_exam_mark(exam_mark_id, payload)
            if row is None:
                raise HTTPException(status_code=404, detail="No Exam Mark Found")
            return row

