from pydantic import BaseModel


class CreateRoomScheme(BaseModel):
    number: str
    floor: int
    capacity: int