from sqlmodel import SQLModel, select
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD
from src.auth.models import AuthUser, Role
from src.auth.utils import get_password_hash
from src import engine

    

async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def add_admin(session: AsyncSession):
    statement = select(AuthUser).where(AuthUser.role == Role.admin)
    result = await session.execute(statement)
    admin = result.first()
    
    if not admin:
        hashed_password = get_password_hash(DEFAULT_ADMIN_PASSWORD)
        admin = AuthUser(username=DEFAULT_ADMIN_USERNAME, password=hashed_password, role=Role.admin)
        session.add(admin)
        await session.commit()