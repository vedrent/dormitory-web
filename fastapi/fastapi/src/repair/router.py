from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.auth.models import AuthUser
from src.auth.dependencies import get_current_user

from src.repair.schemas import RepairClaimScheme, ReadRoomClaim
from src.repair.models import Repair_list
from src.repair.utils import insert_repair_list, read_repair_list_by_room, read_repair_list_by_id, delete_repair_list
from src.lodgers.utils import read_lodger_by_user_id, read_lodgers_by_room_id

from src.database import get_session
from src.config import REPAIR_CLAIMS_LIMIT

from sqlmodel.ext.asyncio.session import AsyncSession


repair_router = APIRouter(tags=["repair"])
base_url = "/repair"
request_url = base_url + "/claims"


@repair_router.get(base_url + "/{room_id}", response_model=List[Repair_list])
async def get_room_claims(room_id: int, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    repairs = await read_repair_list_by_room(session, room_id)
    return repairs


@repair_router.post(base_url)
async def create_claim(repair_scheme: RepairClaimScheme, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    lodger = await read_lodger_by_user_id(session, user.id)
    if (not lodger):
        raise HTTPException(status_code=404, detail="Lodger are not found! Try registrate lodger at first.")
    
    claims = await read_repair_list_by_room(session, lodger.room_id)
    if (len(claims) >= REPAIR_CLAIMS_LIMIT):
        raise HTTPException(status_code=400, detail="Too many repair claims for the room! Claims limit: " + str(REPAIR_CLAIMS_LIMIT))
    
    entity = Repair_list(
        room_id = lodger.room_id,
        description = repair_scheme.description,
        open_date = repair_scheme.open_date.replace(tzinfo=None),
        close_date = repair_scheme.close_date.replace(tzinfo=None)
    )
    
    await insert_repair_list(session, entity)


@repair_router.delete(base_url + "/{claim_id}")
async def delete_claim(claim_id: int, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    claim = await read_repair_list_by_id(session, claim_id)
    if (not claim):
        raise HTTPException(status_code=404, detail="Repair claim not found!")
    
    lodgers = await read_lodgers_by_room_id(session, claim.room_id)
    user_ids = [l.user_id for l in lodgers]
    
    if (user.id not in user_ids):
        raise HTTPException(status_code=403, detail="This claim is not attached to your room!")

    await delete_repair_list(session, claim)