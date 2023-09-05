from enum import Enum 
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Table, Column, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class FollowedType(Enum):
    user = "user"
    artist = "artist"
    playlist = "playlist"

class FollowRecordModel(Base):
    __tablename__ = 'follows'
    __table_args__ = (
        UniqueConstraint('followerId', 'followeeId', name='unique_follow_record'),
    )

    followRecordId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    followerId: Mapped[int] = mapped_column(nullable=False)
    followeeId: Mapped[int] = mapped_column(nullable=False)
    followed_type: Mapped[FollowedType] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())


