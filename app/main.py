import time
from typing import Annotated
import httpx
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Response, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.api.dependencies.dependencies import get_email_service, get_httpx_client
from app.exceptions.email_exception import EmailException
from app.services.email_service import EmailService
from app.utils.log import setup_logging
from app.api.routes.student_routes import router as student_router
from app.api.routes.subject_routes import router as subject_router
from app.api.routes.exam_mark_routes import router as exam_mark_router
from app.api.routes.class_routes import router as class_router
from app.api.routes.auth_routes import router as auth_router
from app.core.config import config
from uuid import uuid4
import app.models

import logging

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    timeout = httpx.Timeout(connect=5, pool=5, read=10, write=10)
    limits = httpx.Limits(
        max_connections=10, max_keepalive_connections=5, keepalive_expiry=30
    )
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
    }
    #! Above code configure the connection pool
    async with httpx.AsyncClient(
        limits=limits,
        timeout=timeout,
        headers=headers,
        auth=(config.mailjet_api_key, config.mailjet_secret_key),
    ) as client:
        app.state.client = client
        yield


"""Using the lifespan to reuse the httpx connection"""

app = FastAPI(
    title=config.app_name,
    description="Connected with Postgres and handles CRUD operations",
    version=config.app_version,
    lifespan=lifespan,
)
# ! returns a FastAPI object to initiate the application


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    correlation_id = str(uuid4())
    request.state.correlation_id = correlation_id

    start_time = time.perf_counter()

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start_time) * 1000

    response.headers["Correlation-ID"] = correlation_id

    logger.info(
        f"Request completed - correlation_id {correlation_id} - method {request.method} - path {request.url.path} - status_code {response.status_code} - duration_ms {round(duration_ms, 2)}",
    )

    return response


app.include_router(student_router)
app.include_router(subject_router)
app.include_router(exam_mark_router)
app.include_router(class_router)
app.include_router(auth_router)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.error(
        "Database integrity error on %s %s: %s", request.method, request.url.path, exc
    )
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Database conflict or constraint violation occurred."},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled error processing %s %s: %s", request.method, request.url.path, exc
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )


@app.exception_handler(EmailException)
async def email_exception_handler(request: Request, exc: EmailException):
    logger.exception(
        "Email Service Error %s %s: %s", request.method, request.url.path, exc
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Email Service Error"},
    )


@app.get("/", tags=["Home Page"])
def home(response: Response):
    """Root endpoint value is returned"""
    response.set_cookie(key="theme", value="dark", secure=False, httponly=True)
    #! If the secure is true the browser send the cookie data in HTTPS , for False -> HTTP
    #! For preventing JS API like cookie to access the data
    return {"title": config.app_name}


"""Creating a /students end point of GET to take data from the db"""


# @app.get("/external-api")
# async def external_api(service: Annotated[EmailService, Depends(get_email_service)]):
#     return await service.send_login_mail("vishalmanivannan1205@gmail.com")
