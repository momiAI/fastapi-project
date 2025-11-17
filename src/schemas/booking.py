from datetime import date
from pydantic import BaseModel


class Booking(BaseModel):
    cottage_id: int
    user_id: int
    date_start: date
    date_end: date
    price: int


class BookingRequest(BaseModel):
    cottage_id: int
    date_start: date
    date_end: date
