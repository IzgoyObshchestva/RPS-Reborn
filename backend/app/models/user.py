from ..db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, BigInteger
from datetime import datetime, timezone

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_id = mapped_column(BigInteger, unique=True, index=True)

    win: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    loss: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    add_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)