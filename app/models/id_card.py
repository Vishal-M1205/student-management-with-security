from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from app.models.base import Base


class IdCard(Base):
    __tablename__ = "id_cards"

    __table_args__ = (UniqueConstraint("student_id", name="ud_id_card_student_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE", name="fk_id_cards_student_id"),
        nullable=False,
    )
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    stored_filename: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
