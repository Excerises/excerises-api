import uuid
from datetime import datetime

from sqlalchemy import JSON, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.users.model import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    body_part: Mapped[str | None] = mapped_column(String(100), nullable=True)
    equipment: Mapped[str | None] = mapped_column(String(100), nullable=True)
    target: Mapped[str | None] = mapped_column(String(100), nullable=True)
    secondary_muscles: Mapped[list | None] = mapped_column(JSON, nullable=True)
    instructions: Mapped[list | None] = mapped_column(JSON, nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(50), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
