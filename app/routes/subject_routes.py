from typing import Annotated
from fastapi import APIRouter, status, Depends
from app.schemas.subject import (
    SubjectPatch,
    SubjectResponse,
    SubjectCreate,
    SubjectUpdate,
)
from app.services.subject_service import SubjectService
from app.dependencies import get_subject_service

router = APIRouter(prefix="/subjects", tags=["Subject Management"])


@router.get("/", response_model=list[SubjectResponse])
async def get_all_subjects(
    service: Annotated[SubjectService, Depends(get_subject_service)],
):
    """Return all the subjects data"""
    return await service.get_all_subjects()


@router.get("/{subject_id}", response_model=SubjectResponse)
async def get_subject_by_id(
    subject_id: int,
    service: Annotated[SubjectService, Depends(get_subject_service)],
):
    """GET subject data using id (path parameter)"""
    return await service.get_subject_by_id(subject_id)


@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(
    subject: SubjectCreate,
    service: Annotated[SubjectService, Depends(get_subject_service)],
):
    """Creates a new Subject Data"""
    return await service.create_subject(subject)


@router.put("/{subject_id}", response_model=SubjectResponse)
async def update_subject(
    subject_id: int,
    subject: SubjectUpdate,
    service: Annotated[SubjectService, Depends(get_subject_service)],
):
    """Updates the existing Subject data by Subject ID"""
    return await service.update_subject(subject_id, subject)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(
    subject_id: int,
    service: Annotated[SubjectService, Depends(get_subject_service)],
):
    """Deletes the Subject data by Subject ID, return no body"""
    await service.delete_subject(subject_id)


@router.patch("/{subject_id}", response_model=SubjectResponse)
async def patch_subject(
    subject_id: int,
    subject: SubjectPatch,
    service: Annotated[SubjectService, Depends(get_subject_service)],
):
    """Partially updates the Subject data by Subject ID"""
    return await service.patch_subject(subject_id, subject)
