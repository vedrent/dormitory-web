from pydantic import BaseModel

from src.auth.models import Role


class SignupUserSchema(BaseModel):
    username: str
    password: str

class ReturnUserSchema(BaseModel):
    id: int
    username: str
    role: Role

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str