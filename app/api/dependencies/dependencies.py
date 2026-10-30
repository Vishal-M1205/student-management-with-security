from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, SecurityScopes
import httpx
from app.database import get_db_connection
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import TokenData
from app.core.security import decode_access_token
import jwt

from app.repositories.interfaces.class_interface import ClassInterface
from app.repositories.interfaces.result_interface import ExamResultInterface
from app.repositories.interfaces.id_card_interface import IdCardInterface
from app.repositories.interfaces.subject_interface import SubjectInterface
from app.repositories.interfaces.student_interface import StudentInterface
from app.repositories.interfaces.user_interface import UserInterface
from app.repositories.interfaces.teacher_interface import TeacherInterface
from app.repositories.implementation.class_repository import ClassRepository
from app.repositories.implementation.student_repository import StudentRepository
from app.repositories.implementation.id_card_repository import IdCardRepository
from app.repositories.implementation.result_repository import ExamResultRepository
from app.repositories.implementation.subject_repository import SubjectRepository
from app.repositories.implementation.exam_mark_repository import ExamMarkRepository
from app.repositories.implementation.user_repository import UserRepository
from app.repositories.implementation.teacher_repository import TeacherRepository
from app.services.class_service import ClassService
from app.services.email_service import EmailService
from app.services.result_service import ExamResultService
from app.services.student_service import StudentService
from app.services.id_card_service import IdCardService
from app.services.subject_service import SubjectService
from app.services.exam_mark_service import ExamMarkService
from app.services.auth_service import AuthService

DB_Session = Annotated[AsyncSession, Depends(get_db_connection)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_exam_result_repository(
    session: DB_Session,
) -> ExamResultInterface:
    return ExamResultRepository(session)


def get_exam_result_service(
    repository: Annotated[ExamResultInterface, Depends(get_exam_result_repository)],
    session: DB_Session,
) -> ExamResultService:
    return ExamResultService(repository, session)


def get_student_repository(session: DB_Session) -> StudentInterface:
    return StudentRepository(session)


def get_student_service(
    repository: Annotated[StudentInterface, Depends(get_student_repository)],
    session: DB_Session,
) -> StudentService:
    return StudentService(repository, session)


def get_id_card_repository(
    session: DB_Session,
) -> IdCardInterface:
    return IdCardRepository(session)


def get_id_card_service(
    repository: Annotated[IdCardInterface, Depends(get_id_card_repository)],
    session: DB_Session,
) -> IdCardService:
    return IdCardService(repository, session)


def get_subject_repository(
    session: DB_Session,
) -> SubjectInterface:
    return SubjectRepository(session)


def get_subject_service(
    repository: Annotated[SubjectInterface, Depends(get_subject_repository)],
    session: DB_Session,
) -> SubjectService:
    return SubjectService(repository, session)


def get_exam_mark_repository(
    session: DB_Session,
) -> ExamMarkRepository:
    return ExamMarkRepository(session)


def get_exam_mark_service(
    repository: Annotated[ExamMarkRepository, Depends(get_exam_mark_repository)],
    session: DB_Session,
) -> ExamMarkService:
    return ExamMarkService(repository, session)


def get_class_repository(session: DB_Session) -> ClassInterface:
    return ClassRepository(session)


def get_class_service(
    session: DB_Session,
    repository: Annotated[ClassInterface, Depends(get_class_repository)],
) -> ClassService:
    return ClassService(repository, session)


def get_user_repository(session: DB_Session) -> UserInterface:
    return UserRepository(session)


def get_teacher_repository(session: DB_Session) -> TeacherInterface:
    return TeacherRepository(session)


def get_httpx_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.client


def get_email_service(client: Annotated[httpx.AsyncClient, Depends(get_httpx_client)]):
    return EmailService(client)


def get_auth_service(
    session: DB_Session,
    user_repository: Annotated[UserInterface, Depends(get_user_repository)],
    student_repository: Annotated[StudentInterface, Depends(get_student_repository)],
    teacher_repository: Annotated[TeacherInterface, Depends(get_teacher_repository)],
    email_service: Annotated[EmailService, Depends(get_email_service)],
) -> AuthService:
    return AuthService(
        session, user_repository, student_repository, teacher_repository, email_service
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    security_scopes: SecurityScopes,
    userrepository: Annotated[UserRepository, Depends(get_user_repository)],
    session: DB_Session,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = decode_access_token(token)

        if payload["sub"] is None or payload["role"] is None:
            raise credentials_exception

        token_data = TokenData(**payload)

        user = await userrepository.get_user_by_email(token_data.sub)

        await session.commit()

        if not user:
            raise credentials_exception

        for required_scopes in security_scopes.scopes:
            if required_scopes not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permission",
                )

        return user

    except (jwt.PyJWTError, Exception):

        raise
