from jose import jwt
from datetime import timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException

from src.database import get_session
from src.auth.models import AuthUser, Role
from src.auth.dependencies import get_current_user
from src.auth.schemas import SignupUserSchema, ReturnUserSchema, TokenSchema
from src.auth.utils import get_password_hash, get_user_by_username, create_access_token, create_refresh_token, verify_password
from src.config import JWT_REFRESH_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM


auth_router = APIRouter(tags=["Authorization"])


@auth_router.post("/signup", response_model=ReturnUserSchema)
async def signup(form_data: SignupUserSchema, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_username(form_data.username, session)
    if user:
        raise HTTPException(status_code=400, detail="This username is taken")

    user = AuthUser(
        username=form_data.username,
        password=get_password_hash(form_data.password),
        role=Role.user,
    )

    session.add(user)
    await session.commit()

    return user


@auth_router.post("/login", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await get_user_by_username(form_data.username, session)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(user.id, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(user.id, expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/refresh", response_model=TokenSchema)
async def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    access_token = create_access_token(user_id, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)


@auth_router.get("/whoami", response_model=ReturnUserSchema)
async def whoami(user: AuthUser = Depends(get_current_user)):
    return user
