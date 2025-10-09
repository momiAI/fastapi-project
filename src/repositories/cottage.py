from .base import BaseRepository
from src.models.cottage import CottageModel
from src.schemas.cottage import Cottage


class CottageRepository(BaseRepository):
    model = CottageModel
    schema = Cottage