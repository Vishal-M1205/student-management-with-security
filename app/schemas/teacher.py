import re
from pydantic import BaseModel, ConfigDict, Field, field_validator


class TeacherCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    department: str = Field(min_length=2, max_length=100)
    designation: str = Field(default="Teacher", max_length=50)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not re.match(r"^[A-Za-z\s]+$", value):
            raise ValueError("Name can only contain alphabetic characters and spaces")
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long after trimming")
        return value.title()


class TeacherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    department: str
    designation: str
