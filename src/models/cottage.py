import typing

from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

if typing.TYPE_CHECKING:
    from src.models import FacilitiesCottageModel


class CottageModel(Base):
    __tablename__ = "cottage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id", ondelete="CASCADE")
    )
    name_house: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(400))
    people: Mapped[int]
    price: Mapped[int]

    facilities: Mapped[list["FacilitiesCottageModel"]] = relationship(
        "FacilitiesCottageModel",  # type: ignore
        secondary="facilities_and_cottage",
        back_populates="cottage",
        lazy="selectin",
    )  # type: ignore
