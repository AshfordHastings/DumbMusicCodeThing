from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from .schema import ArtistSchema, SongSchema, UserSchema, PlaylistSchema