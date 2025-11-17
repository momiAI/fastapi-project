from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from src.database import Base


class ImagesModel(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    name_img: Mapped[str] = mapped_column(unique=True)


class AsociationImagesCottageModel(Base):
    __tablename__ = " asociationimages"
    id_img: Mapped[int] = mapped_column(ForeignKey("images.id"))
    id_cottage: Mapped[int] = mapped_column(ForeignKey("cottage.id"))

    __table_args__ = (
        PrimaryKeyConstraint("id_img", "id_cottage", name="asociationimages_pkey"),
    )
