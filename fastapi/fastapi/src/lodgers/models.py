from sqlmodel import SQLModel, Field
from datetime import datetime


class Room(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    number: str
    floor: int
    capacity: int