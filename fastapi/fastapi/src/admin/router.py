from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.database import get_session
from src.admin.dependencies import is_admin
from src.admin.schemas import CreateUserSchema
from src.auth.utils import get_password_hash, get_user_by_username
from src.auth.schemas import ReturnUserSchema
from src.auth.models import AuthUser


admin_router = APIRouter(tags=["Admin"], dependencies=[Depends(is_admin)]) 


@admin_router.get("/users", response_model=List[ReturnUserSchema])
async def get_all_users(offset: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    statement = select(AuthUser).offset(offset).limit(limit)
    result = await session.execute(statement)
    users = result.scalars().all()

    return users


@admin_router.get("/users/{id}", response_model=ReturnUserSchema)
async def get_user(id: int, session: AsyncSession = Depends(get_session)):
    statement = select(AuthUser).where(AuthUser.id == id)
    result = await session.execute(statement)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@admin_router.post("/users", response_model=ReturnUserSchema)
async def create_user(form_data: CreateUserSchema, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_username(form_data.username, session)
    if user:
        raise HTTPException(status_code=400, detail="This username is taken")

    user = AuthUser(
        username=form_data.username,
        password=get_password_hash(form_data.password),
        role=form_data.role,
    )

    session.add(user)
    await session.commit()

    return user


@admin_router.delete("/users/{id}", response_model=ReturnUserSchema)
async def delete_user(id: int, session: AsyncSession = Depends(get_session)):
    statement = select(AuthUser).where(AuthUser.id == id)
    result = await session.execute(statement)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()

    return user