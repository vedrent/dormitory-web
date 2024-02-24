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


async def insert_washer_queue(session: AsyncSession, user: AuthUser):
    washers = await read_washers(session)
    statuses = list(w.status for w in washers)
    choosed_washer = None

    if (1 in statuses):
        choosed_washer = washers[statuses.index(1)]
    
    inserted = Washer_Queue(user_id = user.id, washer_id = choosed_washer.id)
    session.add(inserted)
    await session.commit()
    await update_washer_status(session, choosed_washer, 2)


async def delete_washer_queue(session: AsyncSession, washing: Washer_Queue):
    await session.delete(washing)
    if (washing.washer_id != None):
        await update_washer_status(session, await read_washer(session, washing.washer_id), 1)
    await session.commit()

async def update_washer_status(session: AsyncSession, washer: Washer, status: int):
    washer.status = status
    session.add(washer)
    await session.commit()

