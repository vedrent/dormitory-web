from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class RepairClaimScheme(BaseModel):
    description: str
    open_date: datetime
    

class ReadRoomClaim(BaseModel):
    room_id: int


class ClaimScheme(BaseModel):
    id: int
    room_id: int
    description: str
    open_date: datetime
    close_date: Optional[datetime] = None


class GetRepairScheme(BaseModel):
    list: List[ClaimScheme]

class RequestFloorRepairScheme(BaseModel):
    floor: int