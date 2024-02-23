from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException

from src.database import get_session, read_washers

from src.auth.models import AuthUser, Role
from src.auth.dependencies import get_current_user
from src.laundry.schemas import LaundryGetScheme

from sqlmodel.ext.asyncio.session import AsyncSession
laundry_router = APIRouter(tags=["laundry"])


@laundry_router.get("/laundry", response_model=LaundryGetScheme)
async def check_washer(user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    washers = await read_washers(session)
    print(type(washers))
    return LaundryGetScheme(washers = washers)

@laundry_router.post("/laundry", response_model=int)
async def post_washer(user: AuthUser = Depends(get_current_user)):
    return 10

@laundry_router.delete("/laundry")
async def post_washer(user: AuthUser = Depends(get_current_user)):
    return
