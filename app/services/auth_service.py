from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.implementation.student_repository import StudentRepository
from app.repositories.implementation.user_repository import UserRepository
from app.repositories.implementation.teacher_repository import TeacherRepository
from app.schemas.auth import Login, StudentSignup, TeacherSignup, Token
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_refresh_token,
    hash_password,
    verify_hashed_password,
    create_access_token,
    decode_access_token,
)
from app.schemas.student import StudentCreate
from app.schemas.teacher import TeacherCreate
from app.services.email_service import EmailService


class AuthService:

    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository,
        student_repository: StudentRepository,
        teacher_repository: TeacherRepository,
        email_service: EmailService,
    ):
        self.session = session
        self.user_repository = user_repository
        self.student_repository = student_repository
        self.teacher_repository = teacher_repository
        self.email_service = email_service

    async def student_signup(self, student_data: StudentSignup):
        async with self.session.begin():
            existing_user = await self.user_repository.get_user_by_email(
                student_data.email
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already found"
                )
            hashed_password = hash_password(student_data.password)
            new_user = User(
                email=student_data.email,
                hashed_password=hashed_password,
                role="student",
                is_active=True,
            )

            created_user = await self.user_repository.create_user(new_user)

            new_student_data = StudentCreate(
                **student_data.model_dump(include={"name", "age", "gender"})
            )

            created_student = await self.student_repository.create_student(
                new_student_data, user_id=created_user.id
            )

            return created_student

    async def teacher_signup(self, teacher_data: TeacherSignup):
        async with self.session.begin():
            existing_user = await self.user_repository.get_user_by_email(
                teacher_data.email
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already found"
                )
            hashed_password = hash_password(teacher_data.password)
            new_user = User(
                email=teacher_data.email,
                hashed_password=hashed_password,
                role="teacher",
                is_active=True,
            )

            created_user = await self.user_repository.create_user(new_user)

            new_teacher_data = TeacherCreate(
                **teacher_data.model_dump(include={"name", "department", "designation"})
            )

            created_teacher = await self.teacher_repository.create_teacher(
                new_teacher_data, user_id=created_user.id
            )

            return created_teacher

    async def login(self, user_data: Login):
        user = await self.user_repository.get_user_by_email(user_data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No such user found"
            )

        if not verify_hashed_password(
            hashed_password=user.hashed_password, password=user_data.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
            )

        access_token_payload = {"sub": user.email, "role": user.role}
        refresh_token_payload = {"sub": user.email}

        access_token = create_access_token(access_token_payload)
        refresh_token = create_refresh_token(refresh_token_payload)

        await self.email_service.send_login_mail(user.email)

        return Token(access_token=access_token, refresh_token=refresh_token)

    async def refresh_access_token(self, refresh_token: str):
        payload = decode_access_token(refresh_token)

        credential_error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

        if payload.get("type") != "refresh":
            raise credential_error

        user = await self.user_repository.get_user_by_email(payload.get("sub"))

        if not user or user.is_active == False:
            raise credential_error

        token_data = {"sub": user.email, "role": user.role}

        access_token = create_access_token(token_data)

        return Token(access_token=access_token, refresh_token=refresh_token)
