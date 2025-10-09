from .base import BaseRepository
from src.models.organization import OrganizationModel
from src.schemas.organization import Organization
from sqlalchemy import select

class OrganizationRepository(BaseRepository):
    model = OrganizationModel
    schema = Organization