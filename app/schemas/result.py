from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal


class SubjectMark(BaseModel):
    subject_name: str
    mark: Decimal = Field(max_digits=5, decimal_places=2, le=100.00)


class ResultResponse(BaseModel):

    model_config = ConfigDict(extra="forbid")

    student_id: int
    student_name: str
    subjects: list[SubjectMark]
    total: Decimal = Field(max_digits=5, decimal_places=2, le=500.00)
    grade: str = Field(max_length=1)


class AcademicSummary(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    total: Optional[Decimal] = Field(max_digits=5, decimal_places=2, le=500.00)
    average: Optional[Decimal] = Field(max_digits=5, decimal_places=2, le=100.00)
