from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, insert, update, delete, text
from sqlalchemy.orm import selectinload
from app.repositories.interfaces.student_interface import StudentInterface
from app.models.exam_mark import ExamMark
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

import math


class StudentRepository(StudentInterface):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_students(
        self, page: int, limit: int, offset: int, params: dict
    ) -> dict:
        query = select(Student)

        for field, value in params.items():
            if field == "name":
                query = query.where(getattr(Student, field).ilike(f"%{value}%"))
            else:
                query = query.where(getattr(Student, field) == value)

        query = query.limit(limit).offset(offset)

        rows = await self.session.execute(query)
        rows = rows.scalars().all()

        query = select(func.count()).select_from(Student)

        for field, values in params.items():
            query = query.where(getattr(Student, field) == values)

        total_records = await self.session.execute(query)
        total_records = total_records.scalar()

        if not total_records:
            total_pages = 0
        else:
            total_pages = math.ceil(total_records / limit) or 1

        return {
            "students": rows,
            "total": total_records,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
        }

    async def get_student_by_id(self, student_id: int) -> Optional[Student]:
        row = await self.session.get(Student, student_id)
        return row

    """
    In the create_student , no need for connection.commit()/rollback()
    because the contextmanage will call rollback on exception
    and commit() on exit of the context

    """

    async def create_student(self, student: StudentCreate, user_id: int) -> Student:
        stmnt = (
            insert(Student)
            .values(**student.model_dump(), user_id=user_id)
            .returning(Student)
        )

        row = await self.session.execute(stmnt)
        row = row.scalar_one()

        return row

    async def update_student(
        self, student_id: int, student: StudentUpdate
    ) -> Optional[Student]:
        stmnt = (
            update(Student)
            .where(Student.id == student_id)
            .values(**student.model_dump())
            .returning(Student)
        )

        row = await self.session.execute(stmnt)
        row = row.scalar_one_or_none()

        return row

    async def delete_student(self, student_id: int) -> Optional[int]:
        stmnt = delete(Student).where(Student.id == student_id).returning(Student.id)

        row = await self.session.execute(stmnt)
        row = row.scalar_one_or_none()

        return row

    async def patch_student(self, student_id: int, payload: dict) -> Optional[Student]:
        stmnt = (
            update(Student)
            .where(Student.id == student_id)
            .values(**payload)
            .returning(Student)
        )

        row = await self.session.execute(stmnt)
        row = row.scalar_one_or_none()

        return row

    async def get_academic_summary(self, student_id) -> dict:
        result = await self.session.execute(
            text("""
            CALL academic_summary(
                :st_id, NULL, NULL
            )
        """),
            {"st_id": student_id},
        )

        row = result.fetchone()

        if not row:
            return None
        return {
            "total": row.total,
            "average": row.average,
        }

    async def get_student_marks(self, student_id: int) -> Optional[dict]:
        stmnt = (
            select(Student)
            .where(Student.id == student_id)
            .options(selectinload(Student.exam_marks).selectinload(ExamMark.subject))
        )

        row = await self.session.execute(stmnt)
        row = row.scalar_one_or_none()

        if not row:
            return None

        return {
            "name": row.name,
            "age": row.age,
            "gender": row.gender,
            "marks": {mark.subject.name: mark.mark for mark in row.exam_marks},
        }
