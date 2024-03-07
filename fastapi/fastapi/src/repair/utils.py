from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from datetime import datetime

from src.repair.models import Repair_list
from src.lodgers.models import Room

from src.repair.schemas import ClaimScheme


def create_get_repair_schemas(repairs: List[Repair_list]):
    def prepair_claim(c: Repair_list):
        return ClaimScheme(
            id = c.id,
            room_id = c.room_id,
            description = c.description,
            open_date = c.open_date,
            close_date = c.close_date
        )

    return list(map(prepair_claim, repairs))


async def insert_repair_list(session: AsyncSession, entity: Repair_list):
    session.add(entity)
    await session.commit()


async def read_opened_claims_by_room(session: AsyncSession, room_id: int) -> List[Repair_list]:
    statement = select(Repair_list).where((Repair_list.close_date == None) & (Repair_list.room_id == room_id))
    statement = await session.execute(statement)

    val = statement.scalars().all()


    return val


async def read_repair_list_by_id(session: AsyncSession, claim_id: int) -> Repair_list:
    statement = select(Repair_list).where(Repair_list.id == claim_id)
    statement = await session.execute(statement)
    return statement.scalars().first()


async def delete_repair_list(session: AsyncSession, entity: Repair_list):
    await session.delete(entity)
    await session.commit()
    

async def finish_repair_list(session: AsyncSession, entity: Repair_list):
    entity.close_date = datetime.utcnow()
    session.add(entity)
    await session.commit()
    

async def read_repair_list(session: AsyncSession) -> List[Repair_list]:
    statement = select(Repair_list)
    statement = await session.execute(statement)
    return statement.scalars().all()
    

async def read_opened_claims_by_floor(session: AsyncSession, floor: int) -> List[Repair_list]:
    statement = select(Repair_list).join(Room).where((Repair_list.close_date == None) & (Room.floor == floor))
    statement = await session.execute(statement)
    return statement.scalars().all()