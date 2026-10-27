from decimal import Decimal
import pytest
from app.services.result_service import ExamResultService


@pytest.fixture
def result_service():
    return ExamResultService(repository=None, session=None)


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
def test_calculate_grade_from_total(total_mark, expected_grade, result_service):
    result = result_service.calculate_grade_from_total(total_mark)

    assert result == expected_grade
