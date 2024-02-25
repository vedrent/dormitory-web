from sqlmodel import SQLModel, Field
from datetime import datetime


class Repair_list(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    room_id: int
    description: str
    open_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    close_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
