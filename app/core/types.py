from typing import Annotated
from fastapi import Path

#! Type annotation uses a Path parameter from FastAPI
StudentID = Annotated[int, Path(gt=0, description="The ID of the student")]
