from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException

from src.auth.models import AuthUser, Role
from src.auth.dependencies import get_current_user
from src.auth.schemas import SignupUserSchema, ReturnUserSchema, TokenSchema

repair_router = APIRouter(tags=["repair"])
base_url = "/repair"


@repair_router.get(base_url, response_model=int)
async def check_washer(user: AuthUser = Depends(get_current_user)):
    return 4

@repair_router.post(base_url, response_model=int)
async def post_washer(user: AuthUser = Depends(get_current_user)):
    return 10

@repair_router.delete(base_url)
async def post_washer(user: AuthUser = Depends(get_current_user)):
    return