from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class SubjectResponse(BaseModel):

    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int = Field(description="ID is auto generated in postgres")
    name: str = Field(min_length=3)


class SubjectCreate(BaseModel):
    name: str = Field(min_length=3)


class SubjectUpdate(BaseModel):
    name: str = Field(min_length=3)


class SubjectPatch(BaseModel):
    name: Optional[str] = Field(min_length=3, default=None)
