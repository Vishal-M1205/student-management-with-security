from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile


def generate_file_path(file: UploadFile, dir: str):
    directory = Path(dir)

    #! parents = True means - if the path contains parent folder and not existed then python creates it     
    Path.mkdir(directory, parents=True, exist_ok=True)

    if not file.filename:
        raise ValueError("Uploaded file has no file name")
    extension = Path(file.filename).suffix

    return directory / f"{uuid4()}.{extension}"
