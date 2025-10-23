from src.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String, Integer,ForeignKey,PrimaryKeyConstraint

class FacilitiesCottageModel(Base):
    __tablename__ = 'facilities_cottage'
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    title : Mapped[str] = mapped_column(String(200))

class AsociationFacilitiesCottageModel(Base):
    __tablename__ = 'facilities_and_cottage'
    id_facilities : Mapped[int] =  mapped_column(Integer, ForeignKey('facilities_cottage.id'))
    id_cottage : Mapped[int] = mapped_column(Integer, ForeignKey('cottage.id'))
    __table_args__ = (
    PrimaryKeyConstraint('id_facilities', 'id_cottage', name='facilities_and_cottage_pkey'),
)