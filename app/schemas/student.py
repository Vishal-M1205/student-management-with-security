from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional

"""
Models describe your application's/database data.
Schemas describe the data entering and leaving your API.

As of now, No Model is required because in the database already a Table is created.
Model is used to implement ORM (Object Relational Model) , used to create table in the 
databse using a python / (pydantic) Model.
No need now , beacuse already table is created in the postgres 

"""


class StudentResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="ID is auto generated in postgres")
    name: str = Field(min_length=3)
    age: int = Field(ge=17, le=35)
    gender: str = Field(max_length=1, examples=["M", "F"])


class StudentListResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    students: list[StudentResponse]
    total: int = Field(description="Total Student Records in the Database")
    page: int = Field(description="Current Page")
    limit: int = Field(description="Maximum Records requested")
    total_pages: int = Field(description="Total available pages")


class StudentCreate(BaseModel):
    name: str = Field(min_length=3, pattern=r"^[A-Za-z\s]+$")
    age: int = Field(ge=17, le=35)
    gender: str = Field(max_length=1, examples=["M", "F"])

    @field_validator("name")
    @classmethod
    def validate_name_format(cls, name: str):
        return name.strip().title()


"""
Botht the models StudentCreate and StudentUpdate are same.
But for a clear meaning in API and seperate Responsibility, need to create these models
"""


class StudentUpdate(BaseModel):
    name: str = Field(min_length=3, pattern=r"^[A-Za-z\s]+$")
    age: int = Field(ge=17, le=35)
    gender: str = Field(max_length=1, examples=["M", "F"])

    @field_validator("name")
    @classmethod
    def validate_name_format(cls, name: str):
        return name.strip().title()


class StudentPatch(BaseModel):
    name: Optional[str] = Field(min_length=3, pattern=r"^[A-Za-z\s]+$", default=None)
    age: Optional[int] = Field(ge=17, le=35, default=None)
    gender: Optional[str] = Field(max_length=1, examples=["M", "F"], default=None)

    @field_validator("name")
    @classmethod
    def validate_name_format(cls, name: Optional[str]):
        if name is None:
            return
        return name.strip().title()


class StudentMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=3)
    age: int = Field(ge=17, le=35)
    gender: str = Field(max_length=1, examples=["M", "F"])

    marks: dict[str, int]


class StudentIdCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    student_id: int
    student_name: str
    id_card_id: int
    original_filename: str
    stored_filename: str
    file_path: str
