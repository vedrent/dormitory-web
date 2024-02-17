from fastapi import HTTPException, Depends

from src.auth.models import AuthUser, Role
from src.auth.dependencies import get_current_user


async def is_admin(user: AuthUser = Depends(get_current_user)):
    if user.role != Role.admin:
        raise HTTPException(status_code=403, detail=f"Expected admin role, recieved: {user.role}")