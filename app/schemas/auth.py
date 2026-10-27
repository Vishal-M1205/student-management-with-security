import re
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class StudentSignup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, description="Strong user password")
    age: int = Field(ge=17, le=35)
    gender: str = Field(max_length=1, examples=["M", "F"])

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not re.match(r"^[A-Za-z\s]+$", value):
            raise ValueError("Name can only contain alphabetic characters and spaces")
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long after trimming")
        return value.title()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if " " in value:
            raise ValueError("Password cannot contain spaces")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one numeric digit")
        if not re.search(r"[@$!%*?&#^()_+=\-\[\]{}|;:<>./~`]", value):
            raise ValueError("Password must contain at least one special character")
        return value


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Login(BaseModel):
    email: EmailStr
    password: str
