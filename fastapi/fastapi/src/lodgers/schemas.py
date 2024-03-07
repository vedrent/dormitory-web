from pydantic import BaseModel
from datetime import datetime


class CreateRoomScheme(BaseModel):
    number: str
    floor: int
    capacity: int


class LodgerRoomScheme(BaseModel):
    number: str
    floor: int


class PassportRoomScheme(BaseModel):
    name: str
    lastname: str
    middlename: str
    is_male: bool
    serias: int
    number: int

    births_date: datetime
    births_place: str
    issuance_date: datetime
    issuance_place: str


class RegistrateLodgerScheme(BaseModel):
    room: LodgerRoomScheme
    passport: PassportRoomScheme
