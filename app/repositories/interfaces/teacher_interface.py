from abc import ABC, abstractmethod
from typing import Optional
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate


class TeacherInterface(ABC):

    @abstractmethod
    async def create_teacher(self, teacher: TeacherCreate, user_id: int) -> Teacher:
        pass

    @abstractmethod
    async def get_teacher_by_id(self, teacher_id: int) -> Optional[Teacher]:
        pass

    @abstractmethod
    async def get_teacher_by_user_id(self, user_id: int) -> Optional[Teacher]:
        pass
