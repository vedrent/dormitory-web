from src import app, engine
from src.example.router import example_router
from src.auth.router import auth_router
from src.admin.router import admin_router
from src.laundry.router import laundry_router
from src.repair.router import repair_router
from src.database import add_admin, async_session

from sqlmodel import SQLModel


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(laundry_router)
app.include_router(example_router)
app.include_router(repair_router)

async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.on_event("startup")
async def on_startup():
    await create_all_tables()
    async with async_session() as session:
        await add_admin(session)