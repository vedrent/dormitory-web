from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException

from src.database import get_session
from src.lodgers.utils import insert_room, check_room_exists
from src.lodgers.schemas import CreateRoomScheme
from src.lodgers.models import Room

from src.auth.models import AuthUser, Role
from src.auth.dependencies import get_current_user
# from src.lodgers.schemas import LaundryGetScheme

from sqlmodel.ext.asyncio.session import AsyncSession

lodgers_router = APIRouter(tags=["lodgers"])
base_url = "/lodgers"

@lodgers_router.post(base_url)
async def create_room(scheme: CreateRoomScheme, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if user.role != Role.admin:
        raise HTTPException(status_code=403, detail="You are not an admin!")
    
    room = Room(number=scheme.number, floor=scheme.floor, capacity=scheme.capacity)
    room_exists = await check_room_exists(room, session)

    if room_exists:
        raise HTTPException(status_code=400, detail="Room with thus number and floor number already exists!")

    await insert_room(room, session)