from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey

class AgentModel(Base):
    __tablename__ = "agent"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100))
    number : Mapped[str] = mapped_column(String())
    hotels_id : Mapped[int] = mapped_column(ForeignKey("houses.id"))
