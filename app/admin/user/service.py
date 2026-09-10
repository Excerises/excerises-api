from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth.service import hash_password
from app.users.model import User, UserRole
from app.users.profile_model import UserProfile


async def list_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    return list(result.scalars().all())


async def get_user_with_profile(db: AsyncSession, user_id: str) -> User | None:
    result = await db.execute(
        select(User).options(selectinload(User.profile)).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession, name: str, email: str, password: str, role: UserRole
) -> User:
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise ValueError("Email already taken")

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role=role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_password(
    db: AsyncSession, user_id: str, password: str
) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    user.hashed_password = hash_password(password)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_profile(
    db: AsyncSession, user_id: str, data: dict
) -> UserProfile | None:
    result = await db.execute(select(User).where(User.id == user_id))
    if not result.scalar_one_or_none():
        return None

    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)
        await db.flush()

    for key, value in data.items():
        if value is not None:
            setattr(profile, key, value)

    if profile.height and profile.weight:
        height_m = profile.height / 100
        profile.bmi = round(profile.weight / (height_m**2), 1)

    await db.commit()
    await db.refresh(profile)
    return profile


async def delete_user(db: AsyncSession, user_id: str) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return False

    await db.execute(delete(UserProfile).where(UserProfile.user_id == user_id))
    await db.delete(user)
    await db.commit()
    return True
