from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException

from src.database import get_session
from src.laundry.utils import read_washers, read_queue_position, insert_washer_queue, check_user_in_queue, delete_washer_queue

from src.auth.models import AuthUser, Role
from src.auth.dependencies import get_current_user
from src.laundry.schemas import LaundryGetScheme

from sqlmodel.ext.asyncio.session import AsyncSession
laundry_router = APIRouter(tags=["laundry"])


@laundry_router.get("/laundry", response_model=LaundryGetScheme)
async def check_washer(user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    washers = await read_washers(session)
    pos = await read_queue_position(session, user)
    
    return LaundryGetScheme(washers = washers, queue_position = pos)

@laundry_router.post("/laundry")
async def post_washer(user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    user_proccess = await check_user_in_queue(session, user)
    if (user_proccess):
        raise HTTPException(status_code=400, detail="You are already in a queue!")

    await insert_washer_queue(session, user)

@laundry_router.delete("/laundry")
async def post_washer(user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    proccess = await check_user_in_queue(session, user)
    if (proccess == None):
        raise HTTPException(status_code=404, detail="User not in queue!")
    # if (proccess.washer_id != None):
    #     raise HTTPException(status_code=403, detail="Washing can not be canceled, because it is running!")
        
    await delete_washer_queue(session, proccess)
    
