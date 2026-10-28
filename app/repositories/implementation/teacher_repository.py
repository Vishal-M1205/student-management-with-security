from typing import Optional
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces.teacher_interface import TeacherInterface
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate


class TeacherRepository(TeacherInterface):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_teacher(self, teacher: TeacherCreate, user_id: int) -> Teacher:
        stmnt = (
            insert(Teacher)
            .values(**teacher.model_dump(), user_id=user_id)
            .returning(Teacher)
        )
        result = await self.session.execute(stmnt)
        return result.scalar_one()

    async def get_teacher_by_id(self, teacher_id: int) -> Optional[Teacher]:
        return await self.session.get(Teacher, teacher_id)

    async def get_teacher_by_user_id(self, user_id: int) -> Optional[Teacher]:
        query = select(Teacher).where(Teacher.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
