from src.repositories.base import BaseRepository
from src.models.images import ImagesModel, AsociationImagesCottageModel
from src.repositories.mappers.mappers import ImagesMapper, AsociationImagesCottageMapper


class ImagesRepository(BaseRepository):
    model = ImagesModel
    mapper = ImagesMapper


class AsociationImagesCottageRepository(BaseRepository):
    model = AsociationImagesCottageModel
    mapper = AsociationImagesCottageMapper
