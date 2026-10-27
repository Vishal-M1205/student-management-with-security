from fastapi import (
    APIRouter,
    Security,
    status,
    Header,
    Response,
    Request,
    Query,
    UploadFile,
    Depends,
)
from app.core.config import config
from app.core.types import StudentID
from app.schemas.result import ResultResponse, AcademicSummary
from app.schemas.student import (
    StudentIdCardResponse,
    StudentMarkResponse,
    StudentPatch,
    StudentResponse,
    StudentCreate,
    StudentUpdate,
    StudentListResponse,
)
from app.services.student_service import StudentService
from app.services.result_service import ExamResultService
from app.services.id_card_service import IdCardService
from app.dependencies import (
    get_exam_result_service,
    get_student_service,
    get_id_card_service,
)
from typing import Optional, Annotated
from app.dependencies import get_current_token_data

router = APIRouter(prefix="/students", tags=["Student Management"])
#! tags - groups the endpoints in the docs


#! As we are using dict_row now the value is validated with the Model and creates a object
#! If the validation passes then the object is deserialized to  a JSON data
# * That JSON is sent to the Client by FastAPI

#! For repeated type hits or dependencies we can write Annotated


@router.get("/", response_model=StudentListResponse, summary="Gets all the students")
async def get_all_students(
    request: Request,
    response: Response,
    service: Annotated[StudentService, Depends(get_student_service)],
    age: Optional[int] = None,
    gender: Optional[str] = None,
    name: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=5, le=10),
    user_agent: Optional[str] = Header(default=None),
):
    """
    Return all the students data,
    Explicitly mention the columns in the sql query,
    Uses context manager to close the connection and the cursor automatically,
    404 - for resource not found error,
    500 - for internal server error
    """
    print(
        user_agent
    )  #! getting the value from the headers - name should be same underscore converted to "-" and it is
    #! case-insensitive

    print(request.headers)  #! All the header value from the client
    print(request.cookies)

    response.headers["API-Name"] = config.app_name
    response.headers["API-Version"] = config.app_version

    #! Sending a header response

    return await service.get_all_students(
        page, limit, age=age, gender=gender, name=name
    )


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_by_id(
    student_id: StudentID,
    service: Annotated[StudentService, Depends(get_student_service)],
    token_data=Security(get_current_token_data, scopes=["student:read"]),
):
    """GET student data using id (path parameter)"""

    return await service.get_student_by_id(student_id)


"""
Here the response model is for, after creating the data the API need to 
send back the newly created data.

 student: StudentCreate -> this is for the data sent from JSON body,
 the data is validated/serialized to a StudentCreate object

 By default API sends 200 for the below POST method.
 201 need to be used , for that 
 status_code=status.HTTP_201_CREATED 

 status imported from FastAPI 
"""


# NOTE: Student creation is now handled through /auth/signup/student
# @router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
# async def create_student(
# student: StudentCreate,
# service: Annotated[StudentService, Depends(get_student_service)],
# ):
# """Creates a new Student Data"""
# return await service.create_student(student)


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: StudentID,
    student: StudentUpdate,
    service: Annotated[StudentService, Depends(get_student_service)],
):
    """Updates the exisitng Student data by Student ID"""
    return await service.update_student(student_id, student)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: StudentID,
    service: Annotated[StudentService, Depends(get_student_service)],
):
    """Deletes the Student data by Student ID , return no body"""
    await service.delete_student(student_id)


@router.patch("/{student_id}", response_model=StudentResponse)
async def patch_student(
    student_id: StudentID,
    student: StudentPatch,
    service: Annotated[StudentService, Depends(get_student_service)],
):
    """Modifies the data based on the field values"""
    return await service.patch_student(student_id, student)


@router.get("/{student_id}/results", response_model=ResultResponse)
async def get_student_exam_result_by_id(
    student_id: StudentID,
    service: Annotated[ExamResultService, Depends(get_exam_result_service)],
):
    """Returns the exam result consist of marks, total and grade"""
    return await service.get_student_exam_result_by_id(student_id)


@router.get("/{student_id}/academic-summary", response_model=AcademicSummary)
async def get_academic_summary(
    student_id: StudentID,
    service: Annotated[StudentService, Depends(get_student_service)],
):
    return await service.get_academic_summary(student_id)


@router.get("/{student_id}/marks", response_model=StudentMarkResponse)
async def get_student_marks(
    student_id: StudentID,
    service: Annotated[StudentService, Depends(get_student_service)],
):
    return await service.get_student_marks(student_id)


@router.post("/{student_id}/idcards")
async def upload_student_id_card(
    student_id: StudentID,
    file: UploadFile,
    service: Annotated[IdCardService, Depends(get_id_card_service)],
):
    return await service.upload_student_id_card(student_id, file)


@router.get("/{student_id}/idcards", response_model=StudentIdCardResponse)
async def get_student_id_card(
    student_id: StudentID,
    service: Annotated[IdCardService, Depends(get_id_card_service)],
):
    return await service.get_student_id_card(student_id)
