from sqlalchemy import insert
from pydantic import BaseModel
from src.repositories.base import BaseRepository
from src.models.facilitiec import FacilitiesCottageModel,AsociationFacilitiesCottageModel
from src.schemas.facilities import FacilitiesCottage, AsociationFacilitiesCottage


class FacilitiesCottageRepository(BaseRepository):
    model = FacilitiesCottageModel
    schema = FacilitiesCottage
    

class AsociationFacilitiesCottageRepository(BaseRepository):
    model = AsociationFacilitiesCottageModel
    schema = AsociationFacilitiesCottage