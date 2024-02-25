from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException

from src.auth.models import AuthUser
from src.auth.dependencies import get_current_user

from src.repair.models import Repair_list
from src.database import get_session

from sqlmodel.ext.asyncio.session import AsyncSession


repair_router = APIRouter(tags=["repair"])
base_url = "/repair"
request_url = base_url + "/request"


@repair_router.get(request_url, response_model=int)
async def check_washer(user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return 4

@repair_router.post(base_url, response_model=int)
async def post_washer(user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return 10

@repair_router.delete(base_url)
async def delete_washer(user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return