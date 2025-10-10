from src.repositories.base import BaseRepository
from src.models.booking import BookingModel
from src.schemas.booking import Booking


class BookingRepository(BaseRepository):
    model = BookingModel
    schema = Booking