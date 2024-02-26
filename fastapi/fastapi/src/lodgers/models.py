from sqlmodel import SQLModel, Field
from datetime import datetime


class Room(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    number: str
    floor: int
    capacity: int


class Lodger(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    room_id: int
    user_id: int
    passport_id: int


class Passport(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    lastname: str
    middlename: str
    is_male: bool
    serias: int
    number: int

    births_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    births_place: str
    issuance_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    issuance_place: str