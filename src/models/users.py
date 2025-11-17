from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class UsersModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    phone_number: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(200), nullable=True, unique=True)
    hash_password: Mapped[str] = mapped_column(String(200))
    role: Mapped[int] = mapped_column(Integer, default=1)
