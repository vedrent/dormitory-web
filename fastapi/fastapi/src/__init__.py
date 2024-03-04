from fastapi import FastAPI
from src.config import POSTGRES_URL
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [
    "http://localhost:*",
    "https://localhost:*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
engine = AsyncEngine(create_engine(POSTGRES_URL, future=True))