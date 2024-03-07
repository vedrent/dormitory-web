from sqlmodel import SQLModel, Field
from datetime import datetime


class New(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    source: str
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
