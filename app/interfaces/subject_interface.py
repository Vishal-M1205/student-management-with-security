from abc import ABC, abstractmethod
from app.schemas.subject import SubjectCreate, SubjectUpdate


class SubjectInterface(ABC):

    @abstractmethod
    async def get_all_subjects(self):
        pass

    @abstractmethod
    async def get_subject_by_id(self, subject_id: int):
        pass

    @abstractmethod
    async def create_subject(self, subject: SubjectCreate):
        pass

    @abstractmethod
    async def update_subject(self, subject_id: int, subject: SubjectUpdate):
        pass

    @abstractmethod
    async def patch_subject(self, subject_id: int, payload: dict):
        pass

    @abstractmethod
    async def delete_subject(self, subject_id: int):
        pass

