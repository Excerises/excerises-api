import asyncio

from app.database.connection import engine
from app.database.schemas import Base


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created")


if __name__ == "__main__":
    asyncio.run(main())
