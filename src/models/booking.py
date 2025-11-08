from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,ForeignKey
from src.database import Base


class BookingModel(Base):
    __tablename__ = 'booking'

    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    cottage_id : Mapped[int] = mapped_column(ForeignKey("cottage.id",ondelete="CASCADE"))
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date_start : Mapped[date]
    date_end : Mapped[date] 
    price : Mapped[int]


    @hybrid_property
    def cost(self) -> int:
        return self.price * (self.date_end - self.date_start).days