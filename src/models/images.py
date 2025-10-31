from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer,ForeignKey
from src.database import Base


class ImagesModel(Base):
    __tablename__ = 'images'
    id : Mapped[int] = mapped_column(primary_key=True)
    name_img : Mapped[str]

class AsociationImagesCottageModel(Base):
    __tablename__ = ' asociationimages'
    id_img : Mapped[int] = mapped_column(ForeignKey('images.id'))
    id_cottage : Mapped[int] = mapped_column(ForeignKey('cottage.id'))