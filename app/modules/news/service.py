from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.schemas import News


async def list_news(db: AsyncSession) -> list[News]:
    """List all news ordered by newest first with author loaded."""
    result = await db.execute(
        select(News)
        .options(selectinload(News.created_by))
        .order_by(News.created_at.desc())
    )
    return list(result.scalars().all())


async def get_news(db: AsyncSession, news_id: str) -> News | None:
    """Get single news by id with author loaded."""
    result = await db.execute(
        select(News).options(selectinload(News.created_by)).where(News.id == news_id)
    )
    return result.scalar_one_or_none()


async def create_news(
    db: AsyncSession,
    title: str,
    description: str,
    content: str,
    created_by_id: str,
) -> News:
    """Create news attributed to the given admin user."""
    news = News(
        title=title,
        description=description,
        content=content,
        viewed_count=0,
        created_by_id=created_by_id,
    )
    db.add(news)
    await db.commit()
    await db.refresh(news, attribute_names=["created_by"])
    return news


async def update_news(
    db: AsyncSession, news_id: str, data: dict[str, str]
) -> News | None:
    """Partial update of title/description/content. Returns None if not found."""
    result = await db.execute(
        select(News).options(selectinload(News.created_by)).where(News.id == news_id)
    )
    news = result.scalar_one_or_none()
    if not news:
        return None
    for key, value in data.items():
        setattr(news, key, value)
    await db.commit()
    await db.refresh(news, attribute_names=["created_by"])
    return news


async def delete_news(db: AsyncSession, news_id: str) -> bool:
    """Delete news by id. Returns False if not found."""
    result = await db.execute(select(News).where(News.id == news_id))
    news = result.scalar_one_or_none()
    if not news:
        return False
    await db.delete(news)
    await db.commit()
    return True


async def get_public_news(db: AsyncSession, news_id: str) -> News | None:
    """Get news for public detail view and increment viewed_count."""
    result = await db.execute(
        select(News).options(selectinload(News.created_by)).where(News.id == news_id)
    )
    news = result.scalar_one_or_none()
    if not news:
        return None
    news.viewed_count = (news.viewed_count or 0) + 1
    await db.commit()
    await db.refresh(news, attribute_names=["created_by"])
    return news
