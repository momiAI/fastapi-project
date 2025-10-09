from src.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String, Integer,ForeignKey

class CottageModel(Base):
    __tablename__ = 'cottage'

    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    organization_id : Mapped[int] = mapped_column(ForeignKey("organization.id"))
    name_house : Mapped[str] = mapped_column(String(100))
    description : Mapped[str] = mapped_column(String(400))
    people : Mapped[int] 
    price : Mapped[int]  
    animals : Mapped [bool]