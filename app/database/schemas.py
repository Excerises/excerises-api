import enum
import uuid
from datetime import date, datetime, time

from sqlalchemy import JSON, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        String(10), nullable=False, default=UserRole.USER
    )
    profile: Mapped["UserProfile | None"] = relationship(
        back_populates="user", uselist=False
    )
    news: Mapped[list["News"]] = relationship(back_populates="created_by")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user")
    login_logs: Mapped[list["UserLoginLog"]] = relationship(back_populates="user")
    sessions: Mapped[list["Session"]] = relationship(back_populates="user")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), unique=True, nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="profile")
    birth_date: Mapped[date] = mapped_column(nullable=True)
    height: Mapped[float] = mapped_column(Float, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    bmi: Mapped[float] = mapped_column(Float, nullable=True)
    workout_freq_per_week: Mapped[int] = mapped_column(Integer, nullable=True)
    fitness_level: Mapped[str] = mapped_column(String(50), nullable=True)
    reminder_days: Mapped[list] = mapped_column(JSON, nullable=True)
    reminder_time: Mapped[time] = mapped_column(nullable=True)
    workout_duration_per_day: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


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
    session_exercises: Mapped[list["SessionExercise"]] = relationship(
        back_populates="exercise"
    )


class News(Base):
    __tablename__ = "news"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(LONGTEXT)
    viewed_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=lambda: 0
    )
    created_by_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    created_by: Mapped["User"] = relationship(back_populates="news")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(36), nullable=False, primary_key=True, default=lambda: uuid.uuid4()
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="sessions")
    duration: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    feedback: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    exercises: Mapped[list["SessionExercise"]] = relationship(back_populates="session")


class SessionExercise(Base):
    __tablename__ = "session_exercises"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, nullable=False, primary_key=True
    )
    session_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sessions.id"), nullable=False
    )
    session: Mapped["Session"] = relationship(back_populates="exercises")
    exercise_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("exercises.id"), nullable=False
    )
    exercise: Mapped["Exercise"] = relationship(back_populates="session_exercises")
    repetition: Mapped[int] = mapped_column(Integer, nullable=True)
    duration: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, nullable=False, primary_key=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="notifications")
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text)
    readed_at: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class UserLoginLog(Base):
    __tablename__ = "user_login_logs"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, nullable=False, primary_key=True
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="login_logs")
    ip_address: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    device: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
