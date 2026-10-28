from typing import Annotated
from fastapi import APIRouter, status, Depends, Query
from app.schemas.exam_mark import (
    ExamMarkPatch,
    ExamMarkResponse,
    ExamMarkCreate,
    ExamMarkUpdate,
)
from app.services.exam_mark_service import ExamMarkService
from app.api.dependencies.dependencies import get_exam_mark_service
from typing import Optional

router = APIRouter(prefix="/exam-marks", tags=["Exam Mark Management"])


@router.get("/", response_model=list[ExamMarkResponse])
async def get_all_exam_marks(
    service: Annotated[ExamMarkService, Depends(get_exam_mark_service)],
    subject_id: Optional[int] = Query(default=None, gt=0),
    student_id: Optional[int] = Query(default=None, gt=0),
):
    return await service.get_all_exam_marks(
        subject_id=subject_id, student_id=student_id
    )


@router.get("/{exam_mark_id}", response_model=ExamMarkResponse)
async def get_exam_mark_by_id(
    exam_mark_id: int,
    service: Annotated[ExamMarkService, Depends(get_exam_mark_service)],
):
    return await service.get_exam_mark_by_id(exam_mark_id)


@router.post("/", response_model=ExamMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_mark(
    exam_mark: ExamMarkCreate,
    service: Annotated[ExamMarkService, Depends(get_exam_mark_service)],
):
    return await service.create_exam_mark(exam_mark)


@router.put("/{exam_mark_id}", response_model=ExamMarkResponse)
async def update_exam_mark(
    exam_mark_id: int,
    exam_mark: ExamMarkUpdate,
    service: Annotated[ExamMarkService, Depends(get_exam_mark_service)],
):
    return await service.update_exam_mark(exam_mark_id, exam_mark)


@router.delete("/{exam_mark_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exam_mark(
    exam_mark_id: int,
    service: Annotated[ExamMarkService, Depends(get_exam_mark_service)],
):
    await service.delete_exam_mark(exam_mark_id)


@router.patch("/{exam_mark_id}", response_model=ExamMarkResponse)
async def patch_exam_mark(
    exam_mark_id: int,
    exam_mark: ExamMarkPatch,
    service: Annotated[ExamMarkService, Depends(get_exam_mark_service)],
):
    return await service.patch_exam_mark(exam_mark_id, exam_mark)
