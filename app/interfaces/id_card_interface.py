from abc import ABC, abstractmethod
from app.schemas.id_card import IdCardCreate


class IdCardInterface(ABC):

    @abstractmethod
    async def upload_student_id_card(self, id_card: IdCardCreate):
        pass

    @abstractmethod
    async def get_student_id_card(self, student_id: int):
        pass
