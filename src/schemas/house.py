from pydantic import BaseModel


class HomeAdd(BaseModel):
    title: str
    city: str
    street: str
    number_house: str
    square: int
    description: str
    number: str
    rooms: int
    price: int


class House(HomeAdd):
    id: int


class HomePATCH(BaseModel):
    title: str | None = None
    city: str | None = None
    street: str | None = None
    number_house: str | None = None
    square: int | None = None
    price: int | None = None
    description: str | None = None
    number: str | None = None
    rooms: int | None = None
