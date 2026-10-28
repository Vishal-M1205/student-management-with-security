import logging
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.types import StudentID
from app.repositories.interfaces.student_interface import StudentInterface
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentPatch, StudentUpdate


class StudentService:
    def __init__(self, repository: StudentInterface, session: AsyncSession):
        self.logger = logging.getLogger(__name__)
        self.repository = repository
        self.session = session

    async def get_all_students(self, page: int, limit: int, **kwargs) -> dict:
        async with self.session.begin():
            query_params = {
                key: value for key, value in kwargs.items() if value is not None
            }
            offset = (page - 1) * limit
            return await self.repository.get_all_students(
                page, limit, offset, query_params
            )

    async def get_student_by_id(self, student_id: StudentID) -> Student:
        async with self.session.begin():
            student = await self.repository.get_student_by_id(student_id)
            if student is None:
                raise HTTPException(status_code=404, detail="Student Not Found")
            return student

    async def create_student(self, student: StudentCreate):
        async with self.session.begin():
            return await self.repository.create_student(student)

    async def update_student(self, student_id: int, student: StudentUpdate):
        async with self.session.begin():
            row = await self.repository.update_student(student_id, student)
            if row is None:
                raise HTTPException(status_code=404, detail="No Student Found")
            return row

    async def delete_student(self, student_id: int):
        async with self.session.begin():
            row = await self.repository.delete_student(student_id)
            if row is None:
                raise HTTPException(status_code=404, detail="No Student Found")
            return row

    async def patch_student(self, student_id: int, student: StudentPatch):
        async with self.session.begin():
            payload = student.model_dump(exclude_unset=True)
            if not payload:
                raise HTTPException(
                    status_code=400,
                    detail="Bad Request : No fields provided for update",
                )
            row = await self.repository.patch_student(student_id, payload)
            if row is None:
                raise HTTPException(status_code=404, detail="No Student Found")
            return row

    async def get_academic_summary(self, student_id):
        async with self.session.begin():
            row = await self.repository.get_academic_summary(student_id)
            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No Student Found"
                )
            return row

    async def get_student_marks(self, student_id: int):
        async with self.session.begin():
            row = await self.repository.get_student_marks(student_id)

            if row is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No Student Found"
                )
            return row
