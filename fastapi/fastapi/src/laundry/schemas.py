from pydantic import BaseModel
from typing import List
from src.laundry.models import Washer


class LaundryGetScheme(BaseModel):
    washers: List[Washer]
    queue_position: int = -1
    occupied_washer_id: int = -1