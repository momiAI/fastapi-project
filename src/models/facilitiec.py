import typing

from src.database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String, Integer,ForeignKey,PrimaryKeyConstraint
if typing.TYPE_CHECKING:
    from src.models import CottageModel



class FacilitiesCottageModel(Base):
    __tablename__ = 'facilities_cottage'
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    title : Mapped[str] = mapped_column(String(200))
    cottage : Mapped[list["CottageModel"]] = relationship("CottageModel", # type: ignore noqa: F821
                                                          secondary="facilities_and_cottage",
                                                          back_populates="facilities",
                                                         
                                                          ) 

class AsociationFacilitiesCottageModel(Base):
    __tablename__ = 'facilities_and_cottage'
    id_facilities : Mapped[int] =  mapped_column(Integer, ForeignKey('facilities_cottage.id',ondelete="CASCADE"))
    id_cottage : Mapped[int] = mapped_column(Integer, ForeignKey('cottage.id',ondelete="CASCADE"))

    __table_args__ = (
    PrimaryKeyConstraint('id_facilities', 'id_cottage', name='facilities_and_cottage_pkey'),
)