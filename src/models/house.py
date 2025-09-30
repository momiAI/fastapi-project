from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

class HouseModel(Base):
    __tablename__ = "houses"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(String(100))
    city : Mapped[str] = mapped_column(String(20))
    street : Mapped[str | None] = mapped_column(String(150))
    number_house : Mapped[str | None] = mapped_column(String(10))
    square : Mapped[int | None] 
    price : Mapped[int] 
    description : Mapped[str] = mapped_column(String(300))
    number : Mapped[str] = mapped_column(String())
    rooms : Mapped[int]
