from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.interfaces.subject_interface import SubjectInterface
from app.schemas.subject import SubjectCreate, SubjectUpdate
from app.models.subject import Subject


class SubjectRepository(SubjectInterface):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_subjects(self):
        result = await self.session.execute(
            select(Subject)
        )  #! returns a ResultObject which is a Iterator
        return result.scalars().all()  #! list of ORM Object

    async def get_subject_by_id(self, subject_id: int):

        row = await self.session.get(Subject, subject_id)

        return row

    async def create_subject(self, subject: SubjectCreate):
        row = Subject(**subject.model_dump())

        self.session.add(row)
        await self.session.flush()
        await self.session.refresh(row)

        return row

    async def update_subject(self, subject_id: int, subject: SubjectUpdate):
        row = await self.session.get(Subject, subject_id)

        if row:
            data = subject.model_dump(exclude_unset=True)
            for field, value in data.items():
                setattr(row, field, value)

        return row

    async def patch_subject(self, subject_id: int, payload: dict):
        row = await self.session.get(Subject, subject_id)

        if row:
            for field, value in payload.items():
                setattr(row, field, value)

        return row

    async def delete_subject(self, subject_id: int):
        row = await self.session.get(Subject, subject_id)

        if row:
            await self.session.delete(row)

        return row
