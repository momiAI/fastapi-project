from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey


class OrganizationModel(Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(500))
    city: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(100))
