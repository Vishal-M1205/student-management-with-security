from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal


class ExamMarkResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="ID is auto generated in postgres")
    student_id: int
    subject_id: int
    mark: Decimal = Field(max_digits=5, decimal_places=2)


class ExamMarkCreate(BaseModel):
    student_id: int
    subject_id: int
    mark: Decimal = Field(max_digits=5, decimal_places=2)


class ExamMarkUpdate(BaseModel):
    student_id: int
    subject_id: int
    mark: Decimal = Field(max_digits=5, decimal_places=2)


class ExamMarkPatch(BaseModel):
    student_id: Optional[int] = Field(default=None)
    subject_id: Optional[int] = Field(default=None)
    mark: Optional[Decimal] = Field(max_digits=5, decimal_places=2, default=None)
