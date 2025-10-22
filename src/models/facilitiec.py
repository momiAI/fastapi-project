from src.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String, Integer,ForeignKey

class FacilitiesCottageModel(Base):
    __tablename__ = 'facilities_cottage'
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    title : Mapped[str] = mapped_column(String(200))

class AsociationFacilitiesCottageModel(Base):
    __tablename__ = 'facilities_and_cottage'
    id_facilities : Mapped[int] =  mapped_column(Integer, ForeignKey('facilities_cottage.id'), primary_key=True )
    id_cottage : Mapped[int] = mapped_column(Integer, ForeignKey('cottage.id'), primary_key=True)