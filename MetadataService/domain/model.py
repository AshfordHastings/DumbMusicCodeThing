import datetime
from sqlalchemy import String, Integer, ForeignKey, Table, Column, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from domain import Base

# playlists_to_songs_table = Table(
#     "playlists_to_songs",
#     Base.metadata,
#     Column("playlistId", ForeignKey("playlists.playlistId"), primary_key=True),
#     Column("songId", ForeignKey("songs.songId"), primary_key=True)
# )

# followers_to_playlists_table = Table(
#     "followers_to_playlists",
#     Base.metadata,
#     Column("followerId", ForeignKey("users.userId"), primary_key=True),
#     Column("playlistId", ForeignKey("playlists.playlistId"), primary_key=True)
# )

class PlaylistSongAssociation(Base):
    __tablename__ = 'playlists_to_songs'
    playlistId: Mapped[int]= mapped_column(ForeignKey('playlists.playlistId'), primary_key=True)
    songId: Mapped[int]= mapped_column(ForeignKey('songs.songId'), primary_key=True)
    date_added: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.now())

    # Relationships
    playlist: Mapped['Playlist'] = relationship(back_populates="song_associations")
    song: Mapped['Song'] = relationship(back_populates="playlist_associations")

class Song(Base):
    __tablename__ = "songs"
    songId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    artistId: Mapped[int] = mapped_column(ForeignKey("artists.artistId"), nullable=False)

    artist: Mapped['Artist'] = relationship(back_populates="songs")
    playlist_associations: Mapped[List['PlaylistSongAssociation']] = relationship(back_populates='song', cascade="all, delete-orphan")

class Artist(Base):
    __tablename__ = "artists"
    artistId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    songs: Mapped[List['Song']] = relationship(back_populates='artist', cascade="all, delete-orphan")

class Playlist(Base):
    __tablename__ = "playlists"
    playlistId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    #createdBy: Mapped[int] = mapped_column(ForeignKey("users.userId"), nullable=False)

    song_associations: Mapped[List['PlaylistSongAssociation']] = relationship(back_populates='playlist', cascade="all, delete-orphan")
    #followers: Mapped[List['User']] = relationship(secondary=followers_to_playlists_table, back_populates="playlistsFollowing")
    # songs: Mapped[List['Song']] = relationship(secondary=playlists_to_songs_table)
    
    
class User(Base):
    __tablename__ = "users"
    userId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    email: Mapped[str]
    displayName: Mapped[str]
    date_registered: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.now())

    role_associations: Mapped['UserRoleAssociation'] = relationship(back_populates='user', cascade="all, delete-orphan")


class Role(Base):
    __tablename__ = 'roles'
    roleId: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    user_associations: Mapped['UserRoleAssociation'] = relationship(back_populates='role', cascade="all, delete-orphan")

class UserRoleAssociation(Base):
    __tablename__='users_to_roles'
    userId: Mapped[int]= mapped_column(ForeignKey('users.userId'), primary_key=True)
    roleId: Mapped[int]= mapped_column(ForeignKey('roles.roleId'), primary_key=True)
    date_added: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=func.now())

    # Relationships
    user: Mapped['User'] = relationship(back_populates="role_associations")
    role: Mapped['Role'] = relationship(back_populates="user_associations")

    #playlistsFollowing: Mapped[List['Playlist']] = relationship(secondary=followers_to_playlists_table, back_populates="followers")
