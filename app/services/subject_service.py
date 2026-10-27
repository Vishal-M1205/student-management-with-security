import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.subject_interface import SubjectInterface
from app.schemas.subject import SubjectCreate, SubjectPatch, SubjectUpdate


class SubjectService:

    def __init__(self, repository: SubjectInterface, session: AsyncSession):
        self.logger = logging.getLogger(__name__)
        self.repository = repository
        self.session = session

    async def get_all_subjects(self):
        async with self.session.begin():
            return await self.repository.get_all_subjects()

    async def get_subject_by_id(self, subject_id: int):
        async with self.session.begin():
            subject = await self.repository.get_subject_by_id(subject_id)
            if subject is None:
                raise HTTPException(status_code=404, detail="Subject Not Found")
            return subject

    async def create_subject(self, subject: SubjectCreate):
        async with self.session.begin():
            return await self.repository.create_subject(subject)

    async def update_subject(self, subject_id: int, subject: SubjectUpdate):
        async with self.session.begin():
            row = await self.repository.update_subject(subject_id, subject)
            if row is None:
                raise HTTPException(status_code=404, detail="No Subject Found")
            return row

    async def delete_subject(self, subject_id: int):
        async with self.session.begin():
            row = await self.repository.delete_subject(subject_id)
            if row is None:
                raise HTTPException(status_code=404, detail="No Subject Found")
            return row

    async def patch_subject(self, subject_id: int, subject: SubjectPatch):
        async with self.session.begin():
            payload = subject.model_dump(exclude_unset=True)
            if not payload:
                raise HTTPException(
                    status_code=400,
                    detail="Bad Request : No fields provided for update",
                )
            row = await self.repository.patch_subject(subject_id, payload)
            if row is None:
                raise HTTPException(status_code=404, detail="No Subject Found")
            return row
