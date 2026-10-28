from abc import ABC, abstractmethod


class ExamResultInterface(ABC):

    @abstractmethod
    async def get_student_exam_result_by_id(self, student_id: int):
        pass
