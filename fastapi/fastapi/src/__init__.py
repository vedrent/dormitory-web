from fastapi import FastAPI
from src.config import POSTGRES_URL
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine
from sqlmodel import SQLModel


app = FastAPI()
engine = AsyncEngine(create_engine(POSTGRES_URL, future=True))