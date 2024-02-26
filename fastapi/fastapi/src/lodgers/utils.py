from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.lodgers.models import Room, Lodger, Passport

async def check_room_exists(room: Room, session: AsyncSession) -> bool:
    statement = select(Room).where(Room.number == room.number and Room.floor == room.floor)
    check = await session.execute(statement)
    return check.scalars().first() != None


async def insert_room(room: Room, session: AsyncSession):
    session.add(room)
    await session.commit()
    

async def read_room_id(number: str, floor: int, session: AsyncSession) -> int:
    id = select(Room.id).where(Room.number == number and Room.floor == floor)
    id = await session.execute(id)
    id = id.scalars().first()

    return id


async def insert_passport(passport: Passport, session: AsyncSession) -> int:
    id = session.add(passport)
    await session.commit()
    
    id = select(Passport.id).where(Passport.serias == passport.serias and Passport.number == passport.number)
    id = await session.execute(id)

    return id.scalars().first()


async def insert_lodger(lodger: Lodger, session: AsyncSession):
    session.add(lodger)
    await session.commit()


async def read_lodger_by_user_id(id: int, session: AsyncSession) -> Lodger:
    lodger = select(Lodger).where(Lodger.user_id == id)
    lodger = await session.execute(lodger)
    return lodger.scalars().first()
