from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Login, StudentSignup, Token
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_hashed_password, create_access_token
from app.schemas.student import StudentCreate


class AuthService:

    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository,
        student_repository: StudentRepository,
    ):
        self.session = session
        self.user_repository = user_repository
        self.student_repository = student_repository

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

        token_payload = {"sub": user.email, "role": user.role}

        access_token = create_access_token(token_payload)

        return Token(access_token=access_token)
