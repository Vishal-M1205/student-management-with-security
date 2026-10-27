from abc import ABC, abstractmethod
from app.schemas.student import StudentCreate, StudentUpdate


class StudentInterface(ABC):

    @abstractmethod
    async def get_all_students(self, page: int, limit: int, offset: int, params: dict):
        pass

    @abstractmethod
    async def get_student_by_id(self, student_id: int):
        pass

    @abstractmethod
    async def create_student(self, student: StudentCreate, user_id: int):
        pass

    @abstractmethod
    async def update_student(self, student_id: int, student: StudentUpdate):
        pass

    @abstractmethod
    async def delete_student(self, student_id: int):
        pass

    @abstractmethod
    async def patch_student(self, student_id: int, payload: dict):
        pass

    @abstractmethod
    async def get_academic_summary(self, student_id: int):
        pass

    @abstractmethod
    async def get_student_marks(self, student_id: int):
        pass

