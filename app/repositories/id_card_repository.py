from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload
from app.repositories.interfaces.id_card_interface import IdCardInterface
from app.models.id_card import IdCard
from app.models.student import Student
from app.schemas.id_card import IdCardCreate


class IdCardRepository(IdCardInterface):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def upload_student_id_card(self, id_card: IdCardCreate):
        stmnt = insert(IdCard).values(**id_card.model_dump()).returning(IdCard)

        row = await self.session.execute(stmnt)
        row = row.scalar_one()

        return row

    async def get_student_id_card(self, student_id: int):
        stmnt = (
            select(Student)
            .options(joinedload(Student.id_card))
            .where(Student.id == student_id)
        )

        row = await self.session.execute(stmnt)

        row = row.scalar_one_or_none()

        if row is not None:
            return {
                "student_id": row.id,
                "student_name": row.name,
                "id_card_id": row.id_card.id,
                "original_filename": row.id_card.original_filename,
                "stored_filename": row.id_card.stored_filename,
                "file_path": row.id_card.file_path,
            }
