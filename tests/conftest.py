import psycopg
import pytest
from fastapi.testclient import TestClient
from collections.abc import AsyncGenerator

from sqlalchemy import NullPool
from app.core.config import config
from app.main import app
from app.database import conn_url, get_db_connection
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

test_conn_url = conn_url.set(database="student_db_test")
test_engine = create_async_engine(url=test_conn_url, poolclass=NullPool)
TestSession = async_sessionmaker(bind=test_engine, expire_on_commit=False)


async def get_test_session():
    async with TestSession() as session:
        yield session


@pytest.fixture
def client():
    app.dependency_overrides[get_db_connection] = get_test_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def db_cleanup():
    yield
    connection = psycopg.connect(
        host=config.database_host,
        port=config.database_port,
        user=config.database_user,
        password=config.database_password,
        dbname="student_db_test",
    )
    with connection.cursor() as cursor:
        cursor.execute(
            "TRUNCATE TABLE students, subjects, exam_marks,id_cards RESTART IDENTITY CASCADE;"
        )
    connection.commit()
