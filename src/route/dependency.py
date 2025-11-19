from typing import Annotated
from datetime import date, datetime, timedelta
from fastapi import Query, Request, HTTPException, Depends
from pydantic import BaseModel
from src.utis.db_manager import DbManager
from src.database import async_session_maker
from src.service.auth import authservice

today = datetime.now().date()
tomorrow = today + timedelta(1)


class HomePagination(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(5, ge=0, lt=30)]


class HomeSelection(HomePagination):
    city: Annotated[str | None, Query(None)]
    title: Annotated[str | None, Query(None)]


class DateDep(BaseModel):
    date_start: Annotated[date, Query(today)]
    date_end: Annotated[date, Query(tomorrow)]

def check_date(date : BaseModel = Depends(DateDep)):
    if date.date_start > date.date_end:
        raise HTTPException(status_code=400, detail="Не правильно введена дата")
    return date

def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if token is None:
        return HTTPException(status_code=401, detail="Пользователь не аунтифицирован")
    return token


def get_role(token: str = Depends(get_token)):
    user_role = authservice.decode_token(token).get("user_role", None)
    return user_role

def get_super_user(token: str = Depends(get_token)):
    user_role = authservice.decode_token(token).get("user_role", None)
    if user_role != 2:
        raise HTTPException(status_code=403, detail="Недостаточно прав.")
    return True

def get_auth_user_id(token: str = Depends(get_token)):
    user_id = authservice.decode_token(token).get("user_id", None)
    if user_id is None:
        return HTTPException(status_code=401, detail="Пользователь не найден")
    return user_id


async def get_db():
    async with DbManager(async_session_maker) as db:
        yield db


UserIdDep = Annotated[int, Depends(get_auth_user_id)]
UserRoleDep = Annotated[int, Depends(get_role)]
SuperUserDep = Annotated[bool,Depends(get_super_user)]
DbDep = Annotated[DbManager, Depends(get_db)]
SerchNotBook = Annotated[BaseModel, Depends(check_date)]
