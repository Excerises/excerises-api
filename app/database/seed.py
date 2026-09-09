import asyncio

from sqlalchemy import select

from app.database.connection import async_session, engine
from app.users.model import User, UserRole
from app.auth.service import hash_password


async def seed_admin():
    try:
        async with async_session() as db:
            existing = await db.execute(select(User).where(User.email == "admin@demo.com"))
            if existing.scalar_one_or_none():
                print("Admin already exists, skipping.")
                return

            admin = User(
                name="Admin",
                email="admin@demo.com",
                hashed_password=hash_password("akuadmin"),
                role=UserRole.ADMIN,
            )
            db.add(admin)
            await db.commit()
            print("Admin seeded: admin@demo.com")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_admin())
