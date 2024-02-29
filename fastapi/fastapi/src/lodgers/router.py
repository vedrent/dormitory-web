from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException

from src.database import get_session
from src.lodgers.utils import insert_room, read_room_id, check_room_exists, insert_lodger, read_lodger_by_user_id, insert_passport
from src.lodgers.schemas import CreateRoomScheme, RegistrateLodgerScheme
from src.lodgers.models import Room, Lodger, Passport

from src.auth.models import AuthUser, Role
from src.auth.dependencies import get_current_user

from sqlmodel.ext.asyncio.session import AsyncSession

lodgers_router = APIRouter(tags=["lodgers"])
base_url = "/lodgers"
room_url = base_url + "/rooms"

@lodgers_router.post(room_url)
async def create_room(scheme: CreateRoomScheme, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if user.role != Role.admin:
        raise HTTPException(status_code=403, detail="You are not an admin!")
    
    room = Room(number=scheme.number, floor=scheme.floor, capacity=scheme.capacity)
    room_exists = await check_room_exists(room, session)

    if room_exists:
        raise HTTPException(status_code=400, detail="Room with thus number and floor number already exists!")

    await insert_room(room, session)


@lodgers_router.post(base_url)
async def registrate_lodger(scheme: RegistrateLodgerScheme, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    print(user.username)
    lodger_exists = await read_lodger_by_user_id(session, user.id)
    if lodger_exists:
        raise HTTPException(status_code=400, detail="Lodger already exists!")
    
    room = Room(number = scheme.room.number, floor = scheme.room.floor)
    room_exists = await check_room_exists(room, session)
    if not room_exists:
        raise HTTPException(status_code=404, detail="Room not found!")
    
    room_id = await read_room_id(scheme.room.number, scheme.room.floor, session)

    passport = Passport(
        name = scheme.passport.name,
        lastname = scheme.passport.lastname,
        middlename = scheme.passport.middlename,
        is_male = scheme.passport.is_male,
        serias = scheme.passport.serias,
        number = scheme.passport.number,

        births_date = scheme.passport.births_date.replace(tzinfo=None),
        births_place = scheme.passport.births_place,
        issuance_date = scheme.passport.issuance_date.replace(tzinfo=None),
        issuance_place = scheme.passport.issuance_place
    )

    passport = await insert_passport(passport, session)

    lodger = Lodger(
        room_id = room_id,
        user_id = user.id,
        passport_id = passport
    )
    
    await insert_lodger(lodger, session)
    