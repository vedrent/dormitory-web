from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.utils import get_password_hash
from src.auth.models import AuthUser, Role
from src.database import get_session


example_router = APIRouter(tags=["Examples"])


@example_router.get("/")
async def index():
    return {"message": "Hello, World!"}



@example_router.get("/test_postgres_query")
async def test_postgres(session: AsyncSession = Depends(get_session)):
    hashed_password = get_password_hash("12345")
    admin = AuthUser(username="test_user", password=hashed_password, role=Role.user)

    session.add(admin)
    await session.commit()

    return {"message": "OK"}