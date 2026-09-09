import uuid
from datetime import date, datetime, time

from sqlalchemy import Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.users.model import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=True)
    height: Mapped[float] = mapped_column(Float, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    bmi: Mapped[float] = mapped_column(Float, nullable=True)
    workout_freq_per_week: Mapped[int] = mapped_column(Integer, nullable=True)
    fitness_level: Mapped[str] = mapped_column(String(50), nullable=True)
    reminder_days: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)
    reminder_time: Mapped[time] = mapped_column(nullable=True)
    workout_duration_per_day: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
