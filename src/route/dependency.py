from pydantic import BaseModel
from typing import Annotated
from fastapi import Query,Request,HTTPException,Depends
from src.service.auth import authservice

class HomePagination(BaseModel):
    page : Annotated[int | None, Query(1, ge = 1)]
    per_page : Annotated[int | None,Query(None, ge=0, lt= 30)]

class HomeSelection(HomePagination):
    city : Annotated[str | None, Query(None)]
    title : Annotated[str | None, Query(None)] 


def get_token(request : Request):
    token = request.cookies.get("access_token", None)
    if token is None:
        return HTTPException(status_code=401, detail="Пользователь не аунтифицирован")
    return token

def get_auth_user_id (token : str = Depends(get_token)):
    user_id = authservice.decode_token(token).get("user_id",None)
    if user_id is None: 
        return HTTPException(status_code=401, detail="Пользователь не найден")
    return user_id

UserIdDep = Annotated[int, Depends(get_auth_user_id)]
