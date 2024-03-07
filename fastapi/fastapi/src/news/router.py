from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException

from src.database import get_session
from src.news.schemas import CreateNewScheme, GetNewsScheme, NewScheme
from src.news.utils import insert_new, read_news, read_new_by_id, delete_new, update_new
from src.news.models import New

from src.auth.models import AuthUser, Role
from src.auth.dependencies import get_current_user

from sqlmodel.ext.asyncio.session import AsyncSession


news_router = APIRouter(tags=["lodgers"])
base_url = "/news"

@news_router.post(base_url)
async def post_new(scheme: CreateNewScheme, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if (user.role != Role.admin):
        raise HTTPException(status_code=403, detail="You are not an admin!")

    new = New(
        title = scheme.title,
        content = scheme.content,
        source = scheme.source
    )

    await insert_new(new, session)


@news_router.get(base_url, response_model=GetNewsScheme)
async def get_news(user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    news = await read_news(session)
    return GetNewsScheme(items = news)


@news_router.get(base_url + "/{new_id}", response_model=NewScheme)
async def get_news(new_id: int, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    new = await read_new_by_id(new_id, session)
    if (not new):
        raise HTTPException(status_code=404, detail="New not found!")

    return new
    

@news_router.delete(base_url + "/{id}")
async def delete_new(id: int, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if (user.role != Role.admin):
        raise HTTPException(status_code=403, detail="You are not an admin!")
    
    new = await read_new_by_id(id, session)
    if (not new):
        raise HTTPException(status_code=404, detail="New not found!")

    await delete_new(new, session)
    

@news_router.put(base_url)
async def put_new(scheme: NewScheme, user: AuthUser = Depends(get_current_user), session: AsyncSession = Depends(get_session)): 
    if (user.role != Role.admin):
        raise HTTPException(status_code=403, detail="You are not an admin!")
        
    current_new = await read_new_by_id(scheme.id, session)

    if (not current_new):
        raise HTTPException(status_code=404, detail="New not found, you cant update it!")

    new = New(
        id = scheme.id,
        title = scheme.title,
        content = scheme.content,
        source = scheme.source
    )

    await update_new(new, current_new.date, session)