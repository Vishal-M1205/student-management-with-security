from pydantic import BaseModel, ConfigDict


class IdCardCreate(BaseModel):
    student_id: int
    original_filename: str
    stored_filename: str
    file_path: str


class IdCardResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    original_filename: str
    stored_filename: str
    file_path: str
