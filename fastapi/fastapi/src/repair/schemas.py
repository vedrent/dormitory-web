from pydantic import BaseModel
from datetime import datetime


class RepairClaimScheme(BaseModel):
    description: str
    open_date: datetime 
    close_date: datetime
    
class ReadRoomClaim(BaseModel):
    room_id: int
