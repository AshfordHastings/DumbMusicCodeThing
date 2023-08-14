import factory
from factory.alchemy import SQLAlchemyModelFactory
from MetadataService.domain.model import (
    Artist, Song, Playlist, PlaylistSongAssociation
)
from factory_boy.db import Session

session = Session()

class ArtistFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Artist
        sqlalchemy_session_persistence = 'flush'
    class Params:
        _session = None

    name = factory.Faker('name')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('_session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

class SongFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Song
        sqlalchemy_session_persistence = 'flush'
    class Params:
        _session = None

    title = factory.Faker('sentence', nb_words=3)
    artist = factory.SubFactory(ArtistFactory)
    #release_date = factory.Faker('date_this_decade')
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('_session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

class PlaylistFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Playlist
        sqlalchemy_session_persistence = 'flush'
    class Params:
        _session = None

    name = factory.Faker('sentence', nb_words=2)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('_session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

class PlaylistSongAssociationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = PlaylistSongAssociation
        sqlalchemy_session_persistence = 'flush'
    class Params:
        _session = None

    playlist = factory.SubFactory(PlaylistFactory)
    song = factory.SubFactory(SongFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('_session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)
