import base64
import hashlib
import secrets
from jose import jwt
from typing import Union, Any
from datetime import datetime, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.auth.models import AuthUser
from src.config import PBKDF2_HASH_NAME, PBKDF2_ITERATIONS, JWT_REFRESH_SECRET_KEY, JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM


def get_password_hash(password: str, salt: str = secrets.token_hex(16), iterations: int = PBKDF2_ITERATIONS) -> str:
    hash = hashlib.pbkdf2_hmac(
        PBKDF2_HASH_NAME,
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    b64_hash = base64.b64encode(hash).decode("ascii").strip()

    return "{}${}${}".format(iterations, salt, b64_hash)


def verify_password(password: str, password_hash: str) -> bool:
    password_correct = False

    if password_hash.count("$") == 2:
        iterations, salt, _ = password_hash.split("$", 2)
        iterations = int(iterations)

        compare_hash = get_password_hash(password, salt, iterations)
        password_correct = secrets.compare_digest(password_hash, compare_hash)

    return password_correct


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt


async def get_user_by_username(username: str, session: AsyncSession) -> AuthUser:
    statement = select(AuthUser).where(AuthUser.username == username)
    result = await session.execute(statement)
    user = result.first()
    
    if user:
        user = user[0]

    return user