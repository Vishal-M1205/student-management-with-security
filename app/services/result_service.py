from decimal import Decimal
import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces.result_interface import ExamResultInterface


class ExamResultService:

    def __init__(self, repository: ExamResultInterface, session: AsyncSession):
        self.logger = logging.getLogger(__name__)
        self.repository = repository
        self.session = session

    async def get_student_exam_result_by_id(self, student_id: int) -> dict:
        async with self.session.begin():
            data = await self.repository.get_student_exam_result_by_id(student_id)
            if not data:
                raise HTTPException(
                    status_code=404,
                    detail=f"No Result Found for the Student ID : {student_id} ",
                )
            total = sum(x["mark"] for x in data["subjects"])
            grade = self.calculate_grade_from_total(total)
            data.update(
                {
                    "total": total,
                    "grade": grade,
                }
            )

            return data

    def calculate_grade_from_total(self, total: int) -> str:
        match total:
            case total if total > 450:
                return "A"
            case total if total > 400:
                return "B"
            case total if total > 350:
                return "C"
            case _:
                return "F"
