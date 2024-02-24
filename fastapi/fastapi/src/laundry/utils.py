from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from src.laundry.models import Washer, Washer_Queue
from src.auth.models import AuthUser

async def read_washers(session: AsyncSession) -> List[Washer]:
    statement = select(Washer)
    result = await session.execute(statement)
    return result.scalars().all()

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
    w_id = None

    print(statuses)
    if (1 in statuses):
        w_id = washers[statuses.index(1)]
    
    inserted = Washer_Queue(user_id = user.id, washer_id = w_id)
    session.add(inserted)
    await session.commit()


async def delete_washer_queue(session: AsyncSession, washing: Washer_Queue):
    print(washing)
    await session.delete(washing)
    await session.commit()