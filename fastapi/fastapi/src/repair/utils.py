from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.repair.models import Repair_list

async def insert_repair_list(session: AsyncSession, entity: Repair_list):
    session.add(entity)
    await session.commit()


async def read_repair_list_by_room(session: AsyncSession, room_id: int) -> List[Repair_list]:
    statement = select(Repair_list).where(Repair_list.room_id == room_id)
    statement = await session.execute(statement)
    return statement.scalars().all()


async def read_repair_list_by_id(session: AsyncSession, claim_id: int) -> Repair_list:
    statement = select(Repair_list).where(Repair_list.id == claim_id)
    statement = await session.execute(statement)
    return statement.scalars().first()


async def delete_repair_list(session: AsyncSession, entity: Repair_list):
    print("print")
    print(entity)
    await session.delete(entity)
    await session.commit()