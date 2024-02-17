from pydantic import BaseModel

from src.auth.models import Role


class CreateUserSchema(BaseModel):
    role: Role
    username: str
    password: str