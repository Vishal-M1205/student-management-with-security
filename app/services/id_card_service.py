import logging
from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.interfaces.id_card_interface import IdCardInterface
from app.schemas.id_card import IdCardCreate
from app.utils.path_utils import generate_file_path


class IdCardService:

    def __init__(self, repository: IdCardInterface, session: AsyncSession):
        self.logger = logging.getLogger(__name__)
        self.repository = repository
        self.session = session

    async def upload_student_id_card(self, student_id: int, file: UploadFile):
        if not file.size:
            raise ValueError("No file found")
        if not file.filename:
            raise ValueError("Uploaded file has no filename")
        if file.size > (1024 * 1024) * 10:
            raise HTTPException(status_code=status.HTTP_413_CONTENT_TOO_LARGE)

        supported_fileformat = [".png", ".jpg", ".jpeg"]

        if Path(file.filename).suffix not in supported_fileformat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file format, supported fileformats are {','.join(supported_fileformat)}",
            )

        id_card_file_path = generate_file_path(file, "uploads")
        stored_filename = Path(id_card_file_path).name

        try:
            file_content = await file.read()

            async with aiofiles.open(id_card_file_path, "wb") as id_card_file:
                await id_card_file.write(file_content)

            id_card_payload = IdCardCreate.model_validate(
                {
                    "student_id": student_id,
                    "original_filename": file.filename,
                    "stored_filename": stored_filename,
                    "file_path": str(id_card_file_path),
                }
            )

            async with self.session.begin():
                id_card = await self.repository.upload_student_id_card(id_card_payload)

                return id_card

        except IntegrityError:
            if Path(id_card_file_path).exists():
                Path(id_card_file_path).unlink()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="ID Card Already Exists",
            )
        except Exception:
            if Path(id_card_file_path).exists():
                Path(id_card_file_path).unlink()
            raise

    async def get_student_id_card(self, student_id: int):
        async with self.session.begin():
            id_card = await self.repository.get_student_id_card(student_id)

            if id_card is None:
                raise HTTPException(status_code=404, detail="ID Card Not Found")
            return id_card
