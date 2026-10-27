from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_auth_service
from app.schemas.auth import Login, StudentSignup, Token
from app.schemas.student import StudentResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup/student",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new student",
)
async def student_signup(
    student_data: StudentSignup,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await service.student_signup(student_data)


@router.post("/login", response_model=Token)
async def login(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_auth_service)],
):

    return await service.login(
        Login(email=user_data.username, password=user_data.password)
    )
