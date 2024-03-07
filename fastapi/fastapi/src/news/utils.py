from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from datetime import datetime

from src.news.models import New


async def insert_new(new: New, session: AsyncSession):
    session.add(new)
    await session.commit()


async def read_news(session: AsyncSession) -> List[New]:
    news = select(New)
    news = await session.execute(news)
    return news.scalars().all()


async def read_new_by_id(new_id: int, session: AsyncSession) -> New:
    news = select(New).where(New.id == new_id)
    news = await session.execute(news)
    return news.scalars().first()


async def delete_new(new: New, session: AsyncSession):
    await session.delete(new)
    await session.commit()


async def update_new(new: New, date: datetime, session: AsyncSession):
    new.date = date
    session.add(new)
    await session.commit()