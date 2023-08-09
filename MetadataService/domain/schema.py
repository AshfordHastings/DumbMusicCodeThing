from marshmallow import Schema, fields, post_load
from domain.model import Song, Artist, Playlist, User, PlaylistSongAssociation

class SongSchema(Schema):
    songId = fields.Integer(dump_only=True)
    title = fields.Str()

    artistId = fields.Integer()

    @post_load
    def make_song(self, data, **kwargs):
        return Song(**data)

class ArtistSchema(Schema):
    artistId = fields.Integer(dump_only=True)
    name = fields.Str(required=True)

    @post_load
    def make_artist(self, data, **kwargs):
        return Artist(**data)


class PlaylistSchema(Schema):
    playlistId =fields.Integer(dump_only=True)
    name = fields.Str()

    @post_load
    def make_playlist(self, data, **kwargs):
        return Playlist(**data)
    
class PlaylistSongAssociationSchema(Schema):
    playlistId = fields.Integer()
    songId = fields.Integer()
    date_added = fields.DateTime(dump_only=True)
    song = fields.Nested(SongSchema)

    @post_load
    def make_association(self, data, **kwargs):
        return PlaylistSongAssociation(**data)

class UserSchema(Schema):
    userId = fields.Integer(dump_only=True)
    username = fields.Str()
    displayName = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
    

class SongAssociationRequestSchema(Schema):
    songId = fields.Integer(required=True)

    @post_load
    def make_data(self, data, **kwargs):
        return data
    
class UserRequestSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    displayName = fields.Str()

    @post_load
    def make_data(self, data, **kwargs):
        return data