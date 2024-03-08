from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.laundry.models import Washer, Washer_Queue
from src.auth.models import AuthUser

async def read_washers(session: AsyncSession) -> List[Washer]:
    statement = select(Washer)
    result = await session.execute(statement)
    return result.scalars().all()

async def read_washer(session: AsyncSession, washer_id: int) -> Washer:
    statement = select(Washer).where(Washer.id == washer_id)
    result = await session.execute(statement)
    return result.scalars().first()

async def check_user_in_queue(session, user) -> Washer_Queue:
    user_proccess = select(Washer_Queue).where(Washer_Queue.user_id == user.id)
    user_proccess = await session.execute(user_proccess)
    return user_proccess.scalars().first()


async def read_queue_position(session: AsyncSession, user: AuthUser) -> int:
    waiters  = select(Washer_Queue.user_id).where(Washer_Queue.washer_id == None)
    waiters = await session.execute(waiters)
    waiters = waiters.scalars().all()

    user_proccess = await check_user_in_queue(session, user)
    if (user_proccess and user_proccess.washer_id != None):
        return 0

    if (user.id in waiters):
        return waiters.index(user.id) + 1
    else:
        return -1
    

async def read_occupied_by_user_washer(session: AsyncSession, user: AuthUser) -> int:
    washer_id = select(Washer_Queue.washer_id).where(Washer_Queue.user_id == user.id)
    washer_id = await session.execute(washer_id)
    washer_id = washer_id.scalars().first()

    if (not washer_id):
        return -1
    return washer_id


async def insert_washer_queue(session: AsyncSession, user: AuthUser):
    washers = await read_washers(session)
    statuses = list(w.status for w in washers)
    choosed_washer = None

    if (1 in statuses):
        choosed_washer = washers[statuses.index(1)]

    if not choosed_washer:
        inserted = Washer_Queue(user_id = user.id, washer_id = None)
    else:
        inserted = Washer_Queue(user_id = user.id, washer_id = choosed_washer.id)
        await update_washer_status(session, choosed_washer, 2)

    session.add(inserted)
    await session.commit()


async def delete_washer_queue(session: AsyncSession, washing: Washer_Queue):
    await session.delete(washing)
    if (washing.washer_id != None):
        await update_washer_status(session, await read_washer(session, washing.washer_id), 1)
    await session.commit()


async def update_washer_status(session: AsyncSession, washer: Washer, status: int):
    washer.status = status
    session.add(washer)
    await session.commit()


async def start_washing(session: AsyncSession, washer_id: int):
    proccess = select(Washer_Queue).where(Washer_Queue.washer_id == None)
    proccess = await session.execute(proccess)
    proccess = proccess.scalars().first()

    if (not proccess):
        return

    washer = select(Washer).where(Washer.id == washer_id)
    washer = await session.execute(washer)
    washer = washer.scalars().first()
    
    await update_washer_status(session, washer, 2)
    
    proccess.washer_id = washer_id
    session.add(proccess)
    await session.commit()
