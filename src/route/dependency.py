from pydantic import BaseModel
from typing import Annotated
from fastapi import Query

class HomePagination(BaseModel):
    page : Annotated[int | None, Query(1, ge = 1)]
    per_page : Annotated[int | None,Query(None, ge=0, lt= 30)]

class HomeSelection(HomePagination):
    city : Annotated[str | None, Query(None)]
    title : Annotated[str | None, Query(None)] 

