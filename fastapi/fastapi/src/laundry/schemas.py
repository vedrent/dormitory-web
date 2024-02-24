from pydantic import BaseModel
from typing import List
from src.laundry.models import Washer


class LaundryGetScheme(BaseModel):
    washers: List[Washer]
    queue_position: int = -1