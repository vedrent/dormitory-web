from sqlmodel import SQLModel, Field


class Washer_Queue(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int
    washer_id: int

class Washer(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    status: int

# statuses:
# 0 - washer unavailable
# 1 - washer is free
# 2 - washer is occupied