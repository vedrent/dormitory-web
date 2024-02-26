from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.auth.models import AuthUser
from src.auth.dependencies import get_current_user

from src.repair.schemas import RepairClaimScheme, ReadRoomClaim
from src.repair.models import Repair_list
from src.repair.utils import insert_repair_list, read_repair_list_by_room

from src.database import get_session

from sqlmodel.ext.asyncio.session import AsyncSession


repair_router = APIRouter(tags=["repair"])
base_url = "/repair"
request_url = base_url + "/claims"


@repair_router.get(base_url + "/{room_id}", response_model=List[Repair_list])
async def check_washer(room_id: int, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    repairs = await read_repair_list_by_room(session, room_id)
    return repairs


@repair_router.post(base_url)
async def post_washer(repair_scheme: RepairClaimScheme, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    entity = Repair_list(
        room_id = repair_scheme.room_id,
        description = repair_scheme.description,
        open_date = repair_scheme.open_date.replace(tzinfo=None),
        close_date = repair_scheme.close_date.replace(tzinfo=None)
    )
    
    await insert_repair_list(session, entity)


@repair_router.delete(base_url)
async def delete_washer(user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return