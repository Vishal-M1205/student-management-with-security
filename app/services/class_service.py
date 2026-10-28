from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status

from app.repositories.interfaces.class_interface import ClassInterface


class ClassService:
    def __init__(self, repository: ClassInterface, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def get_top_five_students(self):
        async with self.session.begin():
            rows = await self.repository.get_top_five_students()
            if rows is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No Student Found"
                )

            return rows

    async def get_top_five_average(self):
        async with self.session.begin():
            rows = await self.repository.get_top_five_average()
            if rows is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No Student Found"
                )

            return rows
