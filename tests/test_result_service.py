from decimal import Decimal
from urllib.request import Request
import httpx
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.email_service import EmailService
from app.services.result_service import ExamResultService


@pytest.mark.asyncio
async def test_get_student_exam_result_success():
    mock_repo = AsyncMock()
    mock_session = MagicMock()

    mock_session.begin.return_value = AsyncMock()

    fake_data = {
        "student_id": 1,
        "name": "Alice",
        "subjects": [
            {"subject": "Math", "mark": 90},
            {"subject": "Science", "mark": 85},
            {"subject": "English", "mark": 95},
        ],
    }
    mock_repo.get_student_exam_result_by_id.return_value = fake_data

    result_service = ExamResultService(mock_repo, mock_session)

    result = await result_service.get_student_exam_result_by_id(1)

    assert result["total"] == 270
    mock_repo.get_student_exam_result_by_id.assert_awaited_once_with(1)


@pytest.mark.parametrize(
    "total_mark, expected_grade",
    [
        (Decimal("500.00"), "A"),
        (Decimal("450.50"), "A"),
        (Decimal("420.00"), "B"),
        (Decimal("375.00"), "C"),
        (Decimal("0.00"), "F"),
    ],
)
def test_calculate_grade_from_total(total_mark, expected_grade):
    result_service = ExamResultService(repository=None, session=None)
    result = result_service.calculate_grade_from_total(total_mark)

    assert result == expected_grade


@pytest.mark.asyncio
async def test_email_send_success():

    def handler(request: Request):
        assert request.url == "https://api.mailjet.com/v3.1/send"

        return httpx.Response(status_code=200, json={"status": "success"})

    mock_transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=mock_transport) as clinet:
        service = EmailService(clinet)

        await service.send_login_mail("vishal@example.com")


@pytest.mark.asyncio
async def test_email_send_retry():
    attempt = 0

    def handler(request: Request):
        assert request.url == "https://api.mailjet.com/v3.1/send"
        nonlocal attempt
        if attempt < 2:
            attempt += 1
            return httpx.Response(status_code=429)
        return httpx.Response(status_code=200)

    mock_transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=mock_transport) as clinet:
        service = EmailService(clinet)

        await service.send_login_mail("vishal@example.com")
    assert attempt == 2
