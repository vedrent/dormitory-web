from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.lodgers.models import Room

async def check_room_exists(room: Room, session: AsyncSession) -> bool:
    statement = select(Room).where(Room.number == room.number and Room.floor == room.floor)
    check = await session.execute(statement)
    return check.scalars().first() != None

async def insert_room(room: Room, session: AsyncSession):
    session.add(room)
    await session.commit()