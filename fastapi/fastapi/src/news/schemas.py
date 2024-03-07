from pydantic import BaseModel
from typing import List


class CreateNewScheme(BaseModel):
    title: str
    content: str
    source: str


class NewScheme(BaseModel):
    id: int
    title: str
    content: str
    source: str


class GetNewsScheme(BaseModel):
    items: List[NewScheme]