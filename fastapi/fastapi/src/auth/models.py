from sqlmodel import SQLModel, Field, Enum


class Role(str, Enum):
    admin = "admin"
    user = "user"
    company = "company"
    moderator = "moderator"

class AuthUser(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    role: Role
    username: str
    password: str