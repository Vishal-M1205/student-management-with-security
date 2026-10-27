from pydantic import BaseModel, Field
from decimal import Decimal


class StudentTotal(BaseModel):
    id: int
    name: str = Field(min_length=3)
    total: Decimal = Field(max_digits=5, decimal_places=2)


class StudentAverage(BaseModel):
    id: int
    name: str = Field(min_length=3)
    average: Decimal = Field(max_digits=5, decimal_places=2)


class TopFiveStudents(BaseModel):
    students: list[StudentTotal | StudentAverage] = Field(max_length=5)
